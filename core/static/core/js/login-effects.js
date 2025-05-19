// login-effects.js
document.addEventListener('DOMContentLoaded', () => {
    // Efecto de partículas en el fondo
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    document.body.appendChild(particlesContainer);

    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particlesContainer.appendChild(particle);

        const x = anime.random(0, window.innerWidth);
        const y = anime.random(0, window.innerHeight);
        const size = anime.random(2, 6);

        particle.style.cssText = `
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
        `;

        anime({
            targets: particle,
            translateX: () => anime.random(-150, 150),
            translateY: () => anime.random(-150, 150),
            scale: [
                { value: 1.5, duration: 1000, delay: anime.random(0, 1000) },
                { value: 1, duration: 1000 }
            ],
            opacity: [
                { value: 0.8, duration: 1000 },
                { value: 0.2, duration: 1000 }
            ],
            easing: 'easeInOutQuad',
            loop: true,
            delay: anime.random(0, 1000)
        });
    }

    // Animación de entrada del formulario
    const loginTimeline = anime.timeline({
        easing: 'easeOutExpo'
    });

    loginTimeline
        // Efecto de aparición del contenedor
        .add({
            targets: '.login-container',
            scale: [0.9, 1],
            opacity: [0, 1],
            translateY: [-50, 0],
            rotate: [-5, 0],
            duration: 1500,
            easing: 'spring(1, 80, 10, 0)'
        })
        // Efecto de líneas neón
        .add({
            targets: '.neon-line',
            scaleX: [0, 1],
            opacity: [0, 1],
            duration: 1000,
            delay: anime.stagger(100),
            easing: 'easeOutQuart'
        }, '-=800')
        // Título - animación simple sin efecto glitch
        .add({
            targets: '.login-title',
            opacity: [0, 1],
            duration: 800,
            easing: 'easeOutQuad'
            // Ya no llamamos a initGlitchEffect() aquí
        }, '-=500')
        // Campos del formulario con efecto de cyber
        .add({
            targets: '.form-group',
            translateX: [-30, 0],
            opacity: [0, 1],
            duration: 800,
            delay: anime.stagger(150),
            begin: (anim) => {
                initCyberEffect(anim.targets);
            }
        }, '-=500');

    // La función initGlitchEffect se elimina o ya no se llama

    // Efecto Cyber para los inputs
    function initCyberEffect(targets) {
        anime({
            targets: targets,
            borderColor: [
                { value: '#0ff', duration: 500 },
                { value: '#f0f', duration: 500 },
                { value: '#0f0', duration: 500 }
            ],
            boxShadow: [
                { value: '0 0 10px #0ff', duration: 500 },
                { value: '0 0 10px #f0f', duration: 500 },
                { value: '0 0 10px #0f0', duration: 500 }
            ],
            loop: true,
            direction: 'alternate',
            easing: 'easeInOutSine'
        });
    }

    // Efecto hover para el botón
    const buttonHover = anime({
        targets: '.btn-submit',
        scale: 1.1,
        boxShadow: [
            '0 0 10px rgba(0, 255, 157, 0.5)',
            '0 0 20px rgba(0, 255, 157, 0.5)',
            '0 0 30px rgba(0, 255, 157, 0.5)'
        ],
        backgroundColor: 'rgba(0, 255, 157, 0.2)',
        color: '#fff',
        duration: 800,
        autoplay: false
    });

    document.querySelector('.btn-submit').addEventListener('mouseenter', () => buttonHover.play());
    document.querySelector('.btn-submit').addEventListener('mouseleave', () => buttonHover.reverse());

    // Efecto de pulso para los iconos
    anime({
        targets: '.input-icon',
        scale: [1, 1.2],
        opacity: [0.5, 1],
        filter: ['blur(0px)', 'blur(1px)'],
        duration: 1000,
        loop: true,
        direction: 'alternate',
        easing: 'easeInOutQuad'
    });

    // Efecto de onda al hacer click en los inputs
    document.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('click', (e) => {
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            input.appendChild(ripple);

            const rect = input.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            anime({
                targets: ripple,
                scale: [0, 5],
                opacity: [1, 0],
                duration: 1000,
                easing: 'easeOutExpo',
                complete: () => ripple.remove()
            });
        });
    });

    // Efecto de scanner para el borde del formulario
    const scannerEffect = anime({
        targets: '.scanner-line',
        translateY: ['-100%', '100%'],
        duration: 1500,
        loop: true,
        easing: 'linear'
    });
});