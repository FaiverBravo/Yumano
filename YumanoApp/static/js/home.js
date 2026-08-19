/**
 * YÚMANO - Home Page Interactivity
 * Parallax de Video de Fondo y Desplazamiento Suave
 */

document.addEventListener('DOMContentLoaded', function() {
    // Parallax Effect for Hero Video/Background
    const heroVideo = document.getElementById('heroVideo');
    window.addEventListener('scroll', function() {
        if (heroVideo && window.innerWidth > 768) {
            let scrollPosition = window.pageYOffset;
            // Move the video at 35% of scroll speed
            heroVideo.style.transform = 'translate(-50%, calc(-50% + ' + (scrollPosition * 0.35) + 'px))';
        }
    });

    // Smooth Scroll for Hero Indicator
    const scrollLink = document.querySelector('.scroll-link');
    if (scrollLink) {
        scrollLink.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
});
