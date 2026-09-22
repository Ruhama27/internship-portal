// main.js - Helper functions for save toggle, file input display, auto-dismiss alerts

document.addEventListener('DOMContentLoaded', () => {
    // Auto dismiss flash alerts after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'all 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);

    // Save Internship Toggle
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            const id = btn.dataset.id;
            if (!id) return;

            try {
                const res = await fetch(`/student/save/${id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                if (res.ok) {
                    const data = await res.json();
                    if (data.saved) {
                        btn.classList.add('saved');
                        btn.innerHTML = '❤️';
                    } else {
                        btn.classList.remove('saved');
                        btn.innerHTML = '🤍';
                    }
                }
            } catch (err) {
                console.error('Error toggling save:', err);
            }
        });
    });

    // File input visual feedback
    document.querySelectorAll('.upload-zone input[type="file"]').forEach(input => {
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            const zone = e.target.closest('.upload-zone');
            if (file && zone) {
                zone.classList.add('has-file');
                const textElem = zone.querySelector('.upload-text');
                if (textElem) {
                    textElem.innerHTML = `<strong>Selected:</strong> ${file.name}`;
                }
            }
        });
    });
});
