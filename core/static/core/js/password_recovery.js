// password-recovery-effects.js
document.addEventListener('DOMContentLoaded', () => {
    // Obtener elementos del DOM
    const form = document.getElementById('recoveryForm');
    const submitBtn = document.getElementById('submitBtn');
    const successModal = document.getElementById('successModal');
    const closeModalBtn = document.getElementById('closeModal');

    // Efecto de partículas en el fondo
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    document.body.appendChild(particlesContainer);

    // Crear partículas
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
    const recoveryTimeline = anime.timeline({
        easing: 'easeOutExpo'
    });

    recoveryTimeline
        // Efecto de aparición del contenedor
        .add({
            targets: '.recovery-container',
            scale: [0.9, 1],
            opacity: [0, 1],
            translateY: [-50, 0],
            rotate: [-3, 0],
            duration: 1200,
            easing: 'spring(1, 80, 10, 0)'
        })
        // Título con efecto de destello
        .add({
            targets: '.recovery-title',
            opacity: [0, 1],
            scale: [0.8, 1],
            duration: 800,
            complete: () => initShimmerEffect()
        }, '-=500')
        // Descripción
        .add({
            targets: '.recovery-description',
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 800
        }, '-=400')
        // Campos del formulario con efecto de cyber
        .add({
            targets: '.form-group',
            translateX: [-30, 0],
            opacity: [0, 1],
            duration: 800,
            delay: anime.stagger(150)
        }, '-=500');

    // Efecto de shimmer para el título
    function initShimmerEffect() {
        anime({
            targets: '.recovery-title',
            textShadow: [
                { value: '0 0 5px rgba(0, 246, 255, 0.5)', duration: 1000 },
                { value: '0 0 20px rgba(0, 246, 255, 0.8)', duration: 1000 },
                { value: '0 0 5px rgba(0, 246, 255, 0.5)', duration: 1000 }
            ],
            loop: true,
            easing: 'easeInOutSine'
        });
    }

    // Efecto hover para el botón
    const buttonHover = anime({
        targets: '.btn-submit',
        scale: 1.05,
        boxShadow: [
            '0 0 10px rgba(0, 246, 255, 0.5)',
            '0 0 20px rgba(0, 246, 255, 0.5)',
            '0 0 30px rgba(0, 246, 255, 0.5)'
        ],
        backgroundColor: 'rgba(0, 246, 255, 0.2)',
        color: '#fff',
        duration: 400,
        autoplay: false
    });

    submitBtn.addEventListener('mouseenter', () => buttonHover.play());
    submitBtn.addEventListener('mouseleave', () => buttonHover.reverse());

    // Efecto de pulso para el icono de email
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

    // Efecto de onda al hacer click en el input
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

    // Manejar el envío del formulario
    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevenir el envío real del formulario
        
        // Obtener el valor del correo
        const email = form.querySelector('input[name="email"]').value;
        
        if (!email || !validateEmail(email)) {
            showError('Por favor, ingresa un correo electrónico válido.');
            return;
        }
        
        // Efecto de carga en el botón
        const loadingTimeline = anime.timeline({
            easing: 'easeOutExpo'
        });
        
        loadingTimeline
            .add({
                targets: submitBtn,
                width: '60px',
                borderRadius: '30px',
                backgroundColor: 'rgba(0, 246, 255, 0.2)',
                duration: 700,
                update: function(anim) {
                    if (anim.progress > 50 && submitBtn.textContent !== '') {
                        // Crear el elemento loader
                        const loader = document.createElement('div');
                        loader.className = 'loader';
                        
                        submitBtn.innerHTML = '';
                        submitBtn.appendChild(loader);
                    }
                }
            })
            .add({
                duration: 1000,
                complete: function() {
                    // Simular proceso de envío
                    setTimeout(() => {
                        // Restaurar el botón
                        anime({
                            targets: submitBtn,
                            width: '100%',
                            borderRadius: '8px',
                            duration: 700,
                            complete: function() {
                                submitBtn.innerHTML = '<span>Enviar Instrucciones</span>';
                                
                                // Mostrar el modal de éxito
                                showSuccessModal();
                            }
                        });
                    }, 1500);
                }
            });
    });

    // Función para validar email
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    // Función para mostrar error
    function showError(message) {
        // Eliminar mensaje de error existente si hay
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Crear nuevo mensaje de error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <svg class="error-icon" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            <span>${message}</span>
        `;
        
        // Insertar antes del botón de envío
        form.insertBefore(errorDiv, submitBtn.parentNode);
        
        // Animar la aparición del error
        anime({
            targets: errorDiv,
            translateY: [20, 0],
            opacity: [0, 1],
            duration: 500,
            easing: 'easeOutQuad'
        });
    }

    // Función para mostrar el modal de éxito
    function showSuccessModal() {
        successModal.classList.add('active');
        
        anime({
            targets: '.modal-content',
            scale: [0.8, 1],
            opacity: [0, 1],
            duration: 800,
            easing: 'easeOutElastic(1, .6)'
        });
        
        // Efecto de pulso para el icono del modal
        anime({
            targets: '.modal-icon',
            scale: [1, 1.1],
            boxShadow: [
                '0 0 10px rgba(0, 255, 157, 0.2)',
                '0 0 20px rgba(0, 255, 157, 0.4)',
                '0 0 10px rgba(0, 255, 157, 0.2)'
            ],
            duration: 1500,
            loop: true,
            direction: 'alternate',
            easing: 'easeInOutQuad'
        });
    }
    
    // Cerrar el modal
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            anime({
                targets: '.modal-content',
                scale: [1, 0.8],
                opacity: [1, 0],
                duration: 500,
                easing: 'easeInOutQuad',
                complete: function() {
                    successModal.classList.remove('active');
                    // Limpiar el formulario
                    form.reset();
                }
            });
        });
    }

    // Añadir evento click al fondo del modal para cerrarlo
    successModal.addEventListener('click', (e) => {
        if (e.target === successModal) {
            closeModalBtn.click();
        }
    });
});