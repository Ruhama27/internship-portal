import os
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from routes.auth        import auth_bp
    from routes.student     import student_bp
    from routes.company     import company_bp
    from routes.internship  import internship_bp
    from routes.admin       import admin_bp
    from routes.main        import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,       url_prefix='/auth')
    app.register_blueprint(student_bp,    url_prefix='/student')
    app.register_blueprint(company_bp,    url_prefix='/company')
    app.register_blueprint(internship_bp, url_prefix='/internships')
    app.register_blueprint(admin_bp,      url_prefix='/admin')

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        # Seed initial data
        from seed import seed_data
        seed_data()
    app.run(debug=True, port=5000)
