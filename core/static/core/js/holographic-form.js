class HolographicForm {
    constructor() {
        this.initPasswordStrength();
        this.initTimer();
        this.initGlitchEffect();
    }

    initPasswordStrength() {
        const passwordInput = document.querySelector('input[type="password"]');
        const strengthBar = document.querySelector('.strength-bar');
        const strengthText = document.querySelector('.strength-text');

        passwordInput.addEventListener('input', (e) => {
            const password = e.target.value;
            const strength = this.calculatePasswordStrength(password);
            
            anime({
                targets: strengthBar,
                width: `${strength}%`,
                duration: 500,
                easing: 'easeOutExpo'
            });

            strengthText.textContent = `Fuerza Neural: ${strength}%`;
        });
    }

    calculatePasswordStrength(password) {
        let strength = 0;
        
        // Longitud
        if (password.length > 8) strength += 25;
        
        // Mayúsculas y minúsculas
        if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 25;
        
        // Números
        if (password.match(/\d/)) strength += 25;
        
        // Caracteres especiales
        if (password.match(/[^a-zA-Z\d]/)) strength += 25;
        
        return strength;
    }

    initTimer() {
        const timerText = document.querySelector('.timer-text');
        const timerCircle = document.querySelector('.timer-circle circle');
        let timeLeft = 300; // 5 minutos

        const updateTimer = () => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerText.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            const progress = (timeLeft / 300) * 151;
            timerCircle.style.strokeDashoffset = 151 - progress;

            if (timeLeft > 0) {
                timeLeft--;
                setTimeout(updateTimer, 1000);
            }
        };

        updateTimer();
    }

    initGlitchEffect() {
        const glitchText = document.querySelector('.glitch-text');
        
        setInterval(() => {
            const glitchTimeline = anime.timeline({
                duration: 100,
                easing: 'steps(1)'
            });

            glitchTimeline
                .add({
                    targets: glitchText,
                    translateX: 2,
                    translateY: -2,
                    color: '#0ff'
                })
                .add({
                    targets: glitchText,
                    translateX: -2,
                    translateY: 2,
                    color: '#f0f'
                })
                .add({
                    targets: glitchText,
                    translateX: 0,
                    translateY: 0,
                    color: '#0f0'
                });
        }, 3000);
    }
}

// Inicializar efectos del formulario
document.addEventListener('DOMContentLoaded', () => {
    const holographicForm = new HolographicForm();
});