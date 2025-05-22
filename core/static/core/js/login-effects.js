// login-effects.js - Versión Simplificada y Robusta
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Inicializando efectos de login - Versión Optimizada');
    
    // 1. Configurar toggle de contraseña PRIMERO
    setupPasswordToggle();
    
    // 2. Efectos de formulario simples (sin anime.js en campos de contraseña)
    setupFormEffects();
    
    // 3. Efectos de entrada suaves
    setupEntranceEffects();
});

/**
 * Configuración del toggle de contraseña con ícono de candado inicial
 */
function setupPasswordToggle() {
    const passwordInput = document.getElementById('passwordInput');
    const toggleBtn = document.getElementById('passwordToggle');
    const eyePath = document.getElementById('eyePath');
    
    if (!passwordInput || !toggleBtn || !eyePath) {
        console.log('❌ No se encontraron elementos del toggle de contraseña');
        return;
    }
    
    console.log('🔐 Configurando toggle de contraseña con candado inicial');
    
    let isVisible = false;
    let hasContent = false;
    
    // Íconos SVG
    const lockPath = "M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z";
    const eyeOpenPath = "M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z";
    const eyeClosedPath = "M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z";
    
    // Función para actualizar la visibilidad y tipo de ícono
    function updateToggleState() {
        const inputHasContent = passwordInput.value.length > 0;
        
        if (inputHasContent && !hasContent) {
            // Primera vez que escribe - cambiar de candado a ojo
            hasContent = true;
            eyePath.setAttribute('d', eyeOpenPath);
            toggleBtn.classList.add('visible');
            
            // Efecto de transición suave
            toggleBtn.style.transform = 'translateY(-50%) scale(1.2)';
            setTimeout(() => {
                toggleBtn.style.transform = 'translateY(-50%) scale(1)';
            }, 200);
            
            console.log('🔄 Cambiando de candado a ojo');
            
        } else if (!inputHasContent && hasContent) {
            // Se borró todo el contenido - volver al candado
            hasContent = false;
            isVisible = false;
            passwordInput.type = 'password';
            eyePath.setAttribute('d', lockPath);
            toggleBtn.classList.remove('visible');
            
            console.log('🔒 Volviendo al candado');
        }
        
        // Mostrar/ocultar botón según contenido
        if (inputHasContent) {
            toggleBtn.classList.add('visible');
        } else {
            toggleBtn.classList.remove('visible');
        }
    }
    
    // Función para cambiar la visibilidad de la contraseña (solo cuando hay contenido)
    function togglePasswordVisibility() {
        if (!hasContent) return; // No hacer nada si no hay contenido
        
        isVisible = !isVisible;
        passwordInput.type = isVisible ? 'text' : 'password';
        
        // Cambiar entre ojo abierto y cerrado
        if (isVisible) {
            eyePath.setAttribute('d', eyeClosedPath);
            toggleBtn.style.transform = 'translateY(-50%) scale(1.1)';
        } else {
            eyePath.setAttribute('d', eyeOpenPath);
            toggleBtn.style.transform = 'translateY(-50%) scale(1)';
        }
        
        // Efecto de pulso visual
        toggleBtn.style.filter = 'drop-shadow(0 0 10px var(--neon-green))';
        setTimeout(() => {
            toggleBtn.style.filter = '';
        }, 200);
        
        console.log(`👁️ Contraseña ${isVisible ? 'visible' : 'oculta'}`);
    }
    
    // Event listeners
    passwordInput.addEventListener('input', updateToggleState);
    toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        togglePasswordVisibility();
    });
    
    // Estado inicial - mostrar candado
    eyePath.setAttribute('d', lockPath);
    toggleBtn.classList.add('visible'); // Mostrar candado desde el inicio
    toggleBtn.style.opacity = '0.6'; // Un poco más tenue inicialmente
    
    console.log('✅ Toggle de contraseña configurado con candado inicial');
}

/**
 * Efectos de formulario simples (SIN anime.js para evitar conflictos)
 */
function setupFormEffects() {
    const formGroups = document.querySelectorAll('.form-group');
    const inputs = document.querySelectorAll('.form-input');
    
    // Animación de entrada simple con CSS
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        group.style.transitionDelay = `${index * 0.1}s`;
        
        setTimeout(() => {
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });
    
    // Efectos de foco suaves
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
            this.style.boxShadow = '0 0 20px rgba(0, 255, 157, 0.4)';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 0 15px rgba(0, 255, 157, 0.3)';
        });
        
        // Efecto de escritura
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.background = 'rgba(0, 255, 157, 0.12)';
            } else {
                this.style.background = 'rgba(0, 255, 157, 0.05)';
            }
        });
    });
    
    console.log('✅ Efectos de formulario configurados');
}

/**
 * Efectos de entrada para el contenedor principal
 */
function setupEntranceEffects() {
    const loginContainer = document.querySelector('.login-container');
    const title = document.querySelector('.login-title');
    
    if (loginContainer) {
        loginContainer.style.opacity = '0';
        loginContainer.style.transform = 'scale(0.9) translateY(20px)';
        loginContainer.style.transition = 'all 0.8s cubic-bezier(0.165, 0.84, 0.44, 1)';
        
        setTimeout(() => {
            loginContainer.style.opacity = '1';
            loginContainer.style.transform = 'scale(1) translateY(0)';
        }, 200);
    }
    
    if (title) {
        // Efecto de brillo en el título
        let glowInterval = setInterval(() => {
            title.style.textShadow = '0 0 20px var(--neon-green), 0 0 40px var(--neon-green)';
            setTimeout(() => {
                title.style.textShadow = '0 0 10px var(--neon-green)';
            }, 1000);
        }, 3000);
        
        // Limpiar intervalo después de 30 segundos
        setTimeout(() => {
            clearInterval(glowInterval);
        }, 30000);
    }
    
    console.log('✅ Efectos de entrada configurados');
}

/**
 * Efectos adicionales para mejorar la experiencia
 */
function setupAdditionalEffects() {
    // Efecto hover en el botón de submit
    const submitBtn = document.querySelector('.btn-submit');
    if (submitBtn) {
        submitBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 0 30px var(--neon-green)';
        });
        
        submitBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
        
        // Efecto de clic
        submitBtn.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    }
    
    // Efecto hover en el enlace de recuperación
    const recoveryLink = document.querySelector('.recovery-link');
    if (recoveryLink) {
        recoveryLink.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        recoveryLink.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    }
    
    console.log('✅ Efectos adicionales configurados');
}

// Ejecutar efectos adicionales después de que todo esté listo
setTimeout(setupAdditionalEffects, 1000);

// Función de limpieza para evitar conflictos
function cleanupConflicts() {
    // Remover elementos problemáticos si existen
    const problematicElements = document.querySelectorAll('.password-field svg:not(#passwordToggle):not(.password-icon)');
    problematicElements.forEach(el => {
        if (el.id !== 'passwordToggle' && !el.classList.contains('password-icon')) {
            el.remove();
        }
    });
}

// Ejecutar limpieza periódica
setInterval(cleanupConflicts, 5000);

console.log('🎉 Sistema de efectos de login inicializado correctamente');