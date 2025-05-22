// core/static/core/js/auto-logout.js
// Sistema de deslogueo automático por inactividad
// Versión 1.0.0 - Raíz Digital

class AutoLogoutSystem {
    constructor(options = {}) {
        // Configuración por defecto (3 minutos = 180,000 ms)
        this.timeout = options.timeout || 3 * 60 * 1000; // 3 minutos
        this.warningTime = options.warningTime || 30 * 1000; // 30 segundos antes
        this.checkInterval = options.checkInterval || 1000; // Verificar cada segundo
        this.logoutUrl = options.logoutUrl || '/login/';
        
        // Estado del sistema
        this.lastActivity = Date.now();
        this.isWarningShown = false;
        this.warningTimer = null;
        this.checkTimer = null;
        this.warningModal = null;
        
        // Eventos que resetean el temporizador
        this.activityEvents = [
            'mousedown', 'mousemove', 'keypress', 'scroll', 
            'touchstart', 'click', 'focus', 'blur'
        ];
        
        this.init();
    }
    
    init() {
        console.log('🕐 Iniciando sistema de deslogueo automático (3 minutos)');
        
        // Solo activar si el usuario está logueado
        if (!this.isUserLoggedIn()) {
            console.log('⏭️ Usuario no logueado, saltando auto-logout');
            return;
        }
        
        this.setupActivityListeners();
        this.createWarningModal();
        this.startChecking();
        
        console.log('✅ Sistema de auto-logout activado');
    }
    
    isUserLoggedIn() {
        // Verificar si hay indicadores de sesión activa
        return document.querySelector('.user-info') || 
               document.querySelector('.mobile-nav-link.logout') ||
               document.body.classList.contains('has-menu');
    }
    
    setupActivityListeners() {
        // Agregar listeners para detectar actividad
        this.activityEvents.forEach(event => {
            document.addEventListener(event, () => this.resetTimer(), true);
        });
        
        // Eventos específicos para formularios
        document.addEventListener('input', () => this.resetTimer(), true);
        document.addEventListener('change', () => this.resetTimer(), true);
        
        console.log('👂 Listeners de actividad configurados');
    }
    
    resetTimer() {
        this.lastActivity = Date.now();
        
        // Si hay una advertencia activa, ocultarla
        if (this.isWarningShown) {
            this.hideWarning();
        }
    }
    
    startChecking() {
        this.checkTimer = setInterval(() => {
            this.checkInactivity();
        }, this.checkInterval);
    }
    
    checkInactivity() {
        const now = Date.now();
        const timeSinceActivity = now - this.lastActivity;
        const timeUntilLogout = this.timeout - timeSinceActivity;
        
        // Si es tiempo de mostrar advertencia
        if (timeUntilLogout <= this.warningTime && !this.isWarningShown) {
            this.showWarning(Math.ceil(timeUntilLogout / 1000));
        }
        
        // Si es tiempo de hacer logout
        if (timeSinceActivity >= this.timeout) {
            this.performLogout();
        }
        
        // Actualizar contador en la advertencia
        if (this.isWarningShown && timeUntilLogout > 0) {
            this.updateWarningCounter(Math.ceil(timeUntilLogout / 1000));
        }
    }
    
    createWarningModal() {
        // Crear modal de advertencia
        this.warningModal = document.createElement('div');
        this.warningModal.className = 'auto-logout-warning';
        this.warningModal.innerHTML = `
            <div class="warning-backdrop"></div>
            <div class="warning-content">
                <div class="warning-icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                </div>
                <h3 class="warning-title">Sesión por expirar</h3>
                <p class="warning-message">
                    Tu sesión expirará en <span class="warning-counter">30</span> segundos por inactividad.
                </p>
                <div class="warning-actions">
                    <button class="btn-extend-session" id="extendSession">
                        Continuar sesión
                    </button>
                    <button class="btn-logout-now" id="logoutNow">
                        Cerrar sesión
                    </button>
                </div>
                <div class="warning-progress">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
            </div>
        `;
        
        // Agregar estilos
        this.addWarningStyles();
        
        // Configurar eventos
        document.body.appendChild(this.warningModal);
        
        // Event listeners para los botones
        document.getElementById('extendSession').addEventListener('click', () => {
            this.resetTimer();
            this.hideWarning();
        });
        
        document.getElementById('logoutNow').addEventListener('click', () => {
            this.performLogout();
        });
    }
    
    addWarningStyles() {
        if (document.getElementById('auto-logout-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'auto-logout-styles';
        style.textContent = `
            .auto-logout-warning {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .auto-logout-warning.show {
                opacity: 1;
                visibility: visible;
            }
            
            .warning-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(10, 25, 47, 0.9);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }
            
            .warning-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(10, 25, 47, 0.95);
                border-radius: 20px;
                padding: 40px;
                max-width: 450px;
                width: 90%;
                text-align: center;
                border: 2px solid #ff4444;
                box-shadow: 
                    0 20px 60px rgba(0, 0, 0, 0.5),
                    0 0 40px rgba(255, 68, 68, 0.3);
                animation: modalPulse 2s infinite;
            }
            
            @keyframes modalPulse {
                0%, 100% { 
                    box-shadow: 
                        0 20px 60px rgba(0, 0, 0, 0.5),
                        0 0 40px rgba(255, 68, 68, 0.3);
                }
                50% { 
                    box-shadow: 
                        0 20px 60px rgba(0, 0, 0, 0.5),
                        0 0 60px rgba(255, 68, 68, 0.5);
                }
            }
            
            .warning-icon {
                width: 80px;
                height: 80px;
                margin: 0 auto 20px;
                background: rgba(255, 68, 68, 0.1);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid #ff4444;
            }
            
            .warning-icon svg {
                width: 50px;
                height: 50px;
                fill: #ff4444;
                animation: shake 0.5s infinite;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-2px); }
                75% { transform: translateX(2px); }
            }
            
            .warning-title {
                color: #ff4444;
                font-size: 1.8rem;
                margin-bottom: 15px;
                font-weight: 700;
            }
            
            .warning-message {
                color: #ffffff;
                margin-bottom: 30px;
                line-height: 1.6;
                font-size: 1.1rem;
            }
            
            .warning-counter {
                color: #ff4444;
                font-weight: bold;
                font-size: 1.3rem;
                text-shadow: 0 0 10px #ff4444;
            }
            
            .warning-actions {
                display: flex;
                gap: 15px;
                margin-bottom: 25px;
                flex-wrap: wrap;
            }
            
            .btn-extend-session,
            .btn-logout-now {
                flex: 1;
                min-width: 140px;
                padding: 12px 20px;
                border-radius: 30px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                border: none;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .btn-extend-session {
                background: var(--neon-green, #00ff9d);
                color: var(--dark-matter, #0a192f);
            }
            
            .btn-extend-session:hover {
                background: #00cc7d;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 157, 0.4);
            }
            
            .btn-logout-now {
                background: transparent;
                color: #ff4444;
                border: 2px solid #ff4444;
            }
            
            .btn-logout-now:hover {
                background: #ff4444;
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(255, 68, 68, 0.4);
            }
            
            .warning-progress {
                width: 100%;
                height: 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                overflow: hidden;
                position: relative;
            }
            
            .progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #ff4444, #ff6b6b);
                border-radius: 4px;
                transition: width 1s linear;
                width: 100%;
                animation: progressPulse 1s infinite;
            }
            
            @keyframes progressPulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            @media (max-width: 480px) {
                .warning-content {
                    padding: 25px 20px;
                }
                
                .warning-actions {
                    flex-direction: column;
                }
                
                .btn-extend-session,
                .btn-logout-now {
                    width: 100%;
                    min-width: auto;
                }
            }
        `;
        
        document.head.appendChild(style);
    }
    
    showWarning(secondsLeft) {
        if (this.isWarningShown) return;
        
        this.isWarningShown = true;
        this.warningModal.classList.add('show');
        
        // Actualizar contador inicial
        this.updateWarningCounter(secondsLeft);
        
        console.log(`⚠️ Mostrando advertencia de logout (${secondsLeft}s restantes)`);
        
        // Sonido de alerta (opcional)
        this.playWarningSound();
    }
    
    hideWarning() {
        if (!this.isWarningShown) return;
        
        this.isWarningShown = false;
        this.warningModal.classList.remove('show');
        
        console.log('✅ Advertencia de logout ocultada - sesión extendida');
    }
    
    updateWarningCounter(secondsLeft) {
        const counter = document.querySelector('.warning-counter');
        const progressBar = document.getElementById('progressBar');
        
        if (counter) {
            counter.textContent = secondsLeft;
        }
        
        if (progressBar) {
            const percentage = (secondsLeft / (this.warningTime / 1000)) * 100;
            progressBar.style.width = `${percentage}%`;
        }
    }
    
    playWarningSound() {
        // Crear sonido de advertencia (beep corto)
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.2);
        } catch (error) {
            console.log('🔇 No se pudo reproducir sonido de advertencia');
        }
    }
    
    performLogout() {
        console.log('🔓 Realizando logout automático por inactividad');
        
        // Limpiar timers
        if (this.checkTimer) {
            clearInterval(this.checkTimer);
        }
        
        // Mostrar mensaje de logout
        this.showLogoutMessage();
        
        // Hacer logout en el servidor de Django
        this.logoutFromServer();
        
        // Limpiar datos de sesión local
        this.clearSessionData();
        
        // Redirigir después de un breve delay
        setTimeout(() => {
            window.location.href = this.logoutUrl;
        }, 2000);
    }
    
    logoutFromServer() {
        // Hacer logout en el servidor Django
        fetch('/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reason: 'auto_logout_inactivity'
            })
        }).catch(error => {
            console.log('Error al hacer logout en servidor:', error);
        });
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    showLogoutMessage() {
        // Crear mensaje de logout
        const logoutMessage = document.createElement('div');
        logoutMessage.className = 'logout-message';
        logoutMessage.innerHTML = `
            <div class="logout-content">
                <div class="logout-icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                    </svg>
                </div>
                <h3>Sesión cerrada</h3>
                <p>Tu sesión ha sido cerrada por inactividad.</p>
                <p>Redirigiendo al login...</p>
            </div>
        `;
        
        // Agregar estilos para el mensaje de logout
        const style = document.createElement('style');
        style.textContent = `
            .logout-message {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(10, 25, 47, 0.95);
                z-index: 10001;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .logout-content {
                text-align: center;
                color: white;
                background: rgba(10, 25, 47, 0.9);
                padding: 40px;
                border-radius: 20px;
                border: 2px solid var(--neon-green, #00ff9d);
                box-shadow: 0 0 40px rgba(0, 255, 157, 0.3);
            }
            
            .logout-icon {
                width: 80px;
                height: 80px;
                margin: 0 auto 20px;
                background: rgba(0, 255, 157, 0.1);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid var(--neon-green, #00ff9d);
            }
            
            .logout-icon svg {
                width: 50px;
                height: 50px;
                fill: var(--neon-green, #00ff9d);
            }
            
            .logout-content h3 {
                margin-bottom: 15px;
                font-size: 1.5rem;
                color: var(--neon-green, #00ff9d);
            }
            
            .logout-content p {
                margin-bottom: 10px;
                opacity: 0.8;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(logoutMessage);
    }
    
    clearSessionData() {
        // Limpiar datos de sesión local si los hay
        try {
            localStorage.removeItem('user_session');
            sessionStorage.clear();
        } catch (error) {
            console.log('Error al limpiar datos de sesión:', error);
        }
    }
    
    destroy() {
        // Limpiar timers
        if (this.checkTimer) {
            clearInterval(this.checkTimer);
        }
        
        // Remover listeners
        this.activityEvents.forEach(event => {
            document.removeEventListener(event, this.resetTimer, true);
        });
        
        // Remover modal
        if (this.warningModal && this.warningModal.parentNode) {
            this.warningModal.parentNode.removeChild(this.warningModal);
        }
        
        console.log('🗑️ Sistema de auto-logout destruido');
    }
}

// Función para inicializar el sistema
function initAutoLogout() {
    // Solo inicializar en páginas donde el usuario está logueado
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.autoLogoutSystem = new AutoLogoutSystem();
        });
    } else {
        window.autoLogoutSystem = new AutoLogoutSystem();
    }
}

// Auto-inicializar
initAutoLogout();

// Exportar para uso manual si es necesario
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AutoLogoutSystem;
}