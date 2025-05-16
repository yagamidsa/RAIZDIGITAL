document.addEventListener('DOMContentLoaded', () => {
    // Animación de entrada
    const timeline = anime.timeline({
        easing: 'easeOutExpo'
    });

    timeline
        .add({
            targets: '.login-container',
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 1000
        })
        .add({
            targets: '.login-title',
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 800
        }, '-=500')
        .add({
            targets: '.form-group',
            opacity: [0, 1],
            translateX: [20, 0],
            delay: anime.stagger(100),
            duration: 800
        }, '-=500')
        .add({
            targets: '.btn-submit',
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 800
        }, '-=400')
        .add({
            targets: '.back-button',
            opacity: [0, 1],
            translateX: [-20, 0],
            duration: 800
        }, '-=800');

    // Efecto hover en inputs
    document.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('focus', () => {
            anime({
                targets: input,
                boxShadow: [
                    { value: '0 0 0 rgba(0,255,157,0)' },
                    { value: '0 0 15px rgba(0,255,157,0.3)' }
                ],
                duration: 500,
                easing: 'easeOutExpo'
            });
        });

        input.addEventListener('blur', () => {
            anime({
                targets: input,
                boxShadow: '0 0 0 rgba(0,255,157,0)',
                duration: 500,
                easing: 'easeOutExpo'
            });
        });
    });

    // Animación de iconos
    anime({
        targets: '.input-icon',
        opacity: [0.5, 1],
        scale: [0.95, 1.05],
        duration: 1500,
        loop: true,
        direction: 'alternate',
        easing: 'easeInOutSine'
    });

    // Efecto del borde
    anime({
        targets: '.login-border',
        background: [
            { value: 'linear-gradient(45deg, #00ff9d, #00f6ff, #00ff9d)' },
            { value: 'linear-gradient(225deg, #00ff9d, #00f6ff, #00ff9d)' }
        ],
        duration: 4000,
        easing: 'linear',
        loop: true
    });
});