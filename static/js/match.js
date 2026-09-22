// match.js - Animates match score progress bars on page load

document.addEventListener('DOMContentLoaded', () => {
    // Animate match bars
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fill = entry.target;
                const width = fill.getAttribute('data-width') || '0%';
                fill.style.width = width;
                observer.unobserve(fill);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.progress-bar-fill').forEach(fill => {
        const targetWidth = fill.style.width || fill.dataset.width || '0%';
        fill.style.width = '0%';
        fill.setAttribute('data-width', targetWidth);
        observer.observe(fill);
    });
});
