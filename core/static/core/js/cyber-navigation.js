// cyber-navigation.js - Sistema de navegación consistente para Raíz Digital
// Versión 1.0.0

document.addEventListener('DOMContentLoaded', function() {
    // 1. Inicialización del menú
    console.log('📱 Cyber Navigation System - Initializing...');
    
    // 2. Inyectar estilos CSS si aún no existen
    if (!document.getElementById('cyber-navigation-styles')) {
        injectNavigationStyles();
    }
    
    // 3. Configurar la estructura del menú
    setupNavigation();
    
    // 4. Configurar la funcionalidad del menú móvil
    setupMobileMenu();
    
    // 5. Configurar efectos visuales avanzados
    setupVisualEffects();
    
    // 6. Ajustar el contenido principal para dejar espacio para el header
    adjustMainContent();
    
    console.log('✅ Cyber Navigation System - Initialized');
});

/**
 * Configura la estructura básica de navegación
 */
function setupNavigation() {
    // Verificar si ya existe un header
    let header = document.querySelector('.news-header');
    
    // Si no existe, crear uno nuevo
    if (!header) {
        console.log('🔨 Creating new navigation header');
        header = document.createElement('header');
        header.className = 'news-header';
        
        // Insertar al principio del body
        document.body.insertBefore(header, document.body.firstChild);
    }
    
    // Verificar si existe el logo y si no, crearlo
    if (!header.querySelector('.news-logo')) {
        const logoLink = document.createElement('a');
        logoLink.href = '/';
        logoLink.className = 'news-logo';
        logoLink.innerHTML = `
            <svg viewBox="0 0 24 24">
                <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                <path d="M12 4.5c-4.136 0-7.5 3.364-7.5 7.5s3.364 7.5 7.5 7.5 7.5-3.364 7.5-7.5-3.364-7.5-7.5-7.5zm0 14c-3.584 0-6.5-2.916-6.5-6.5s2.916-6.5 6.5-6.5 6.5 2.916 6.5 6.5-2.916 6.5-6.5 6.5z"/>
                <path d="M12 7c-2.757 0-5 2.243-5 5s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5zm0 9c-2.206 0-4-1.794-4-4s1.794-4 4-4 4 1.794 4 4-1.794 4-4 4z"/>
                <circle cx="12" cy="12" r="2.5"/>
            </svg>
            <span class="news-logo-text">Raíz Digital</span>
        `;
        header.appendChild(logoLink);
    }
    
    // Verificar y crear el botón de menú móvil si no existe
    if (!header.querySelector('.mobile-menu-toggle')) {
        const mobileMenuToggle = document.createElement('button');
        mobileMenuToggle.id = 'mobileMenuToggle';
        mobileMenuToggle.className = 'mobile-menu-toggle';
        mobileMenuToggle.setAttribute('aria-label', 'Menú');
        mobileMenuToggle.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        header.appendChild(mobileMenuToggle);
    }
    
    // Verificar y crear el menú de escritorio si no existe
    if (!header.querySelector('.desktop-nav')) {
        const desktopNav = document.createElement('nav');
        desktopNav.className = 'desktop-nav';
        
        // Obtener la URL actual para marcar el enlace activo
        const currentPath = window.location.pathname;
        
        desktopNav.innerHTML = `
            <a href="/marketplace/" class="nav-link ${currentPath.includes('marketplace') ? 'active' : ''}">Inicio</a>
            <a href="/noticias/" class="nav-link ${currentPath.includes('noticias') ? 'active' : ''}">Noticias</a>
            <a href="/eventos/" class="nav-link ${currentPath.includes('eventos') ? 'active' : ''}">Eventos</a>
            <a href="/productos/" class="nav-link ${currentPath.includes('productos') ? 'active' : ''}">Productos</a>
            <a href="/comunidades/" class="nav-link ${currentPath.includes('comunidades') ? 'active' : ''}">Comunidades</a>
        `;
        
        header.appendChild(desktopNav);
    }
    
    // Verificar y crear el menú móvil si no existe
    if (!document.querySelector('.mobile-nav')) {
        const mobileMenu = document.createElement('div');
        mobileMenu.id = 'mobileMenu';
        mobileMenu.className = 'mobile-nav';
        
        // Obtener la URL actual para marcar el enlace activo
        const currentPath = window.location.pathname;
        
        mobileMenu.innerHTML = `
            <div class="mobile-menu-backdrop"></div>
            <div class="mobile-menu-content">
                <a href="/marketplace/" class="mobile-nav-link ${currentPath.includes('marketplace') ? 'active' : ''}">
                    <div class="mobile-nav-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
                        </svg>
                    </div>
                    <span class="mobile-nav-text">Inicio</span>
                </a>
                <a href="/noticias/" class="mobile-nav-link ${currentPath.includes('noticias') ? 'active' : ''}">
                    <div class="mobile-nav-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-1 14H5c-.55 0-1-.45-1-1V7c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v10c0 .55-.45 1-1 1z" />
                            <path d="M8.5 15h2v2h-2zm0-8h2v6h-2zm3.5 0h2v2h-2zm0 3h2v5h-2zm3.5 0h2v2h-2zm0 3h2v2h-2z" />
                        </svg>
                    </div>
                    <span class="mobile-nav-text">Noticias</span>
                </a>
                <a href="/eventos/" class="mobile-nav-link ${currentPath.includes('eventos') ? 'active' : ''}">
                    <div class="mobile-nav-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V9h14v10zM5 7V5h14v2H5z" />
                            <path d="M7 11h10v2H7zm0 4h7v2H7z" />
                        </svg>
                    </div>
                    <span class="mobile-nav-text">Eventos</span>
                </a>
                <a href="/productos/" class="mobile-nav-link ${currentPath.includes('productos') ? 'active' : ''}">
                    <div class="mobile-nav-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M18 6h-2c0-2.21-1.79-4-4-4S8 3.79 8 6H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-6-2c1.1 0 2 .9 2 2h-4c0-1.1.9-2 2-2zm6 16H6V8h2v2c0 .55.45 1 1 1s1-.45 1-1V8h4v2c0 .55.45 1 1 1s1-.45 1-1V8h2v12z" />
                        </svg>
                    </div>
                    <span class="mobile-nav-text">Productos</span>
                </a>
                <a href="/comunidades/" class="mobile-nav-link ${currentPath.includes('comunidades') ? 'active' : ''}">
                    <div class="mobile-nav-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M16.24 13.65c-1.17-.52-2.61-.9-4.24-.9-1.63 0-3.07.39-4.24.9C6.68 14.13 6 15.21 6 16.39V18h12v-1.61c0-1.18-.68-2.26-1.76-2.74zM8.07 16c.09-.23.27-.42.49-.52 1.1-.49 2.26-.73 3.43-.73 1.18 0 2.33.25 3.43.73.23.1.4.29.49.52H8.07zm.49-4.56c.05-3.37 2.71-6.11 6.11-6.11 3.37 0 6.06 2.69 6.11 6.03C19.05 12.56 18 10.64 18 9c0-2.21-1.79-4-4-4-2.21 0-4 1.79-4 4 0 1.64-1.05 3.56-1.44 4.44z"/>
                            <circle cx="15" cy="8" r="2"/>
                            <circle cx="9" cy="8" r="2"/>
                        </svg>
                    </div>
                    <span class="mobile-nav-text">Comunidades</span>
                </a>
            </div>
        `;
        
        document.body.appendChild(mobileMenu);
    }
}

/**
 * Configura la funcionalidad del menú móvil
 */
function setupMobileMenu() {
    const menuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (!menuToggle || !mobileMenu) {
        console.error('❌ Mobile menu elements not found');
        return;
    }
    
    console.log('📱 Setting up mobile menu interaction');
    
    // Añadir estilos inline para solucionar problemas urgentes
    mobileMenu.style.display = 'block';
    
    // Escuchar eventos de clic en el botón de menú
    menuToggle.addEventListener('click', function() {
        console.log('🔄 Menu button clicked');
        
        // Toggle de clases para activar/desactivar
        menuToggle.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        
        // Verificar si se aplicó correctamente
        console.log(`Menu state: ${mobileMenu.classList.contains('active') ? 'ACTIVE' : 'INACTIVE'}`);
        
        // Forzar visibilidad si está activo
        if (mobileMenu.classList.contains('active')) {
            mobileMenu.style.opacity = '1';
            mobileMenu.style.visibility = 'visible';
            mobileMenu.style.pointerEvents = 'auto';
            
            // Forzar visibilidad del contenido
            const content = mobileMenu.querySelector('.mobile-menu-content');
            if (content) {
                content.style.opacity = '1';
                content.style.transform = 'translate(-50%, -50%) scale(1)';
            }
            
            // Forzar visibilidad del backdrop
            const backdrop = mobileMenu.querySelector('.mobile-menu-backdrop');
            if (backdrop) {
                backdrop.style.opacity = '1';
            }
            
            // Bloquear scroll del body
            document.body.style.overflow = 'hidden';
        } else {
            // Restaurar estado normal
            mobileMenu.style.opacity = '0';
            mobileMenu.style.visibility = 'hidden';
            mobileMenu.style.pointerEvents = 'none';
            
            // Restaurar scroll
            document.body.style.overflow = '';
        }
    });
    
    // Cerrar menú al hacer clic en el backdrop
    const backdrop = mobileMenu.querySelector('.mobile-menu-backdrop');
    if (backdrop) {
        backdrop.addEventListener('click', closeMenu);
    }
    
    // Cerrar menú al hacer clic en los enlaces
    const mobileLinks = mobileMenu.querySelectorAll('.mobile-nav-link');
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });
    
    function closeMenu() {
        menuToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        mobileMenu.style.opacity = '0';
        mobileMenu.style.visibility = 'hidden';
        mobileMenu.style.pointerEvents = 'none';
        document.body.style.overflow = '';
    }
    
    // Cerrar el menú al cambiar el tamaño de la ventana a desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && mobileMenu.classList.contains('active')) {
            closeMenu();
        }
    });
}

/**
 * Configura efectos visuales avanzados para el menú
 */
function setupVisualEffects() {
    // Verificar si anime.js está disponible
    const animeAvailable = typeof anime !== 'undefined';
    
    if (!animeAvailable) {
        console.log('⚠️ Anime.js not loaded, applying simplified effects');
        
        // Cargar anime.js dinámicamente
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js';
        script.onload = function() {
            console.log('✅ Anime.js loaded dynamically');
            applyAnimations();
        };
        document.head.appendChild(script);
    } else {
        applyAnimations();
    }
    
    function applyAnimations() {
        if (typeof anime === 'undefined') return;
        
        console.log('✨ Setting up navigation visual effects');
        
        // Efecto hover en los enlaces de escritorio
        const desktopLinks = document.querySelectorAll('.desktop-nav .nav-link');
        
        desktopLinks.forEach(link => {
            link.addEventListener('mouseenter', () => {
                anime({
                    targets: link,
                    scale: 1.05,
                    translateY: -2,
                    color: '#00ff9d',
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });
            
            link.addEventListener('mouseleave', () => {
                anime({
                    targets: link,
                    scale: 1,
                    translateY: 0,
                    color: link.classList.contains('active') ? '#00ff9d' : 'rgba(255, 255, 255, 0.8)',
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });
        });
        
        // Efecto de aurora para el botón de menú
        const menuButton = document.querySelector('.mobile-menu-toggle');
        if (menuButton) {
            menuButton.addEventListener('mouseenter', () => {
                anime({
                    targets: menuButton,
                    boxShadow: '0 0 20px rgba(0, 255, 157, 0.5)',
                    scale: 1.05,
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });
            
            menuButton.addEventListener('mouseleave', () => {
                anime({
                    targets: menuButton,
                    boxShadow: '0 0 10px rgba(0, 255, 157, 0.2)',
                    scale: 1,
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });
        }
        
        // Efecto de brillo en el logo
        const logoText = document.querySelector('.news-logo-text');
        if (logoText) {
            anime({
                targets: logoText,
                textShadow: [
                    { value: '0 0 5px rgba(0, 255, 157, 0.5)', duration: 1000 },
                    { value: '0 0 15px rgba(0, 255, 157, 0.7)', duration: 1000 }
                ],
                loop: true,
                direction: 'alternate',
                easing: 'easeInOutSine'
            });
        }
        
        // Efecto de aparecer para el header al cargar la página
        const header = document.querySelector('.news-header');
        if (header) {
            anime({
                targets: header,
                opacity: [0, 1],
                translateY: [-20, 0],
                duration: 800,
                easing: 'easeOutQuad'
            });
        }
    }
}

/**
 * Función para añadir los estilos CSS requeridos
 * Esta función crea un tag <style> con todos los estilos necesarios para el menú
 */
function injectNavigationStyles() {
    // Crear elemento de estilo
    const styleElement = document.createElement('style');
    styleElement.id = 'cyber-navigation-styles';
    
    // Definir estilos CSS
    styleElement.textContent = `
    /* Estilos del header y navegación*/
    .news-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background: rgba(10, 25, 47, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5%;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .news-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        color: rgba(255, 255, 255, 0.85);
    }

    .news-logo svg {
        width: 32px;
        height: 32px;
        fill: #00ff9d;
    }

    .news-logo-text {
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        background: linear-gradient(90deg, #00ff9d, #00f6ff);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .desktop-nav {
        display: flex;
        gap: 32px;
    }

    .nav-link {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
        position: relative;
    }

    .nav-link:hover {
        color: #00ff9d;
    }

    .nav-link::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -5px;
        left: 0;
        background: #00ff9d;
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    .nav-link:hover::after {
        width: 100%;
    }

    .nav-link.active {
        color: #00ff9d;
    }

    .nav-link.active::after {
        width: 100%;
    }

    /* Menú para móviles */
    .mobile-menu-toggle {
        display: none;
        flex-direction: column;
        justify-content: space-between;
        width: 38px;
        height: 38px;
        background: rgba(10, 25, 47, 0.3);
        border: 1.5px solid #00ff9d;
        border-radius: 50%;
        padding: 9px;
        cursor: pointer;
        z-index: 1001;
        position: relative;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.2), inset 0 0 6px rgba(0, 255, 157, 0.1);
        overflow: hidden;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    .mobile-menu-toggle::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: linear-gradient(45deg, transparent 25%, rgba(0, 255, 157, 0.2) 50%, rgba(0, 246, 255, 0.3) 75%, transparent 100%);
        background-size: 200% 200%;
        filter: blur(8px);
        opacity: 0;
        transition: opacity 0.6s ease;
        z-index: -1;
        animation: aurora 6s infinite;
    }

    .mobile-menu-toggle:hover::after {
        opacity: 1;
    }

    @keyframes aurora {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    .mobile-menu-toggle span {
        display: block;
        width: 65%;
        margin: 0 auto;
        height: 3px;
        background-color: #00ff9d;
        border-radius: 5px;
        transition: all 0.4s cubic-bezier(0.68, -0.6, 0.32, 1.6);
        box-shadow: 0 0 15px #00ff9d;
    }

    .mobile-menu-toggle.active {
        background: rgba(0, 255, 157, 0.15);
        transform: rotate(180deg) scale(0.9);
    }

    .mobile-menu-toggle.active span:nth-child(1) {
        transform: translateY(8px) rotate(45deg);
        width: 75%;
        background: linear-gradient(90deg, #00ff9d, #00f6ff);
    }

    .mobile-menu-toggle.active span:nth-child(2) {
        opacity: 0;
        transform: translateX(-30px) scale(0);
    }

    .mobile-menu-toggle.active span:nth-child(3) {
        transform: translateY(-8px) rotate(-45deg);
        width: 75%;
        background: linear-gradient(90deg, #00f6ff, #00ff9d);
    }

    .mobile-nav {
        display: block !important;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 999;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        will-change: opacity, visibility;
    }

    .mobile-nav.active {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
    }

    .mobile-menu-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(ellipse at center, rgba(10, 25, 47, 0.85) 0%, rgba(6, 28, 30, 0.95) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        opacity: 0;
        transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        will-change: opacity;
    }

    .mobile-nav.active .mobile-menu-backdrop {
        opacity: 1;
        animation: gradient-shift 15s linear infinite;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    .mobile-menu-backdrop::before {
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        background: radial-gradient(ellipse at 30% 30%, rgba(0, 255, 157, 0.1) 0%, transparent 50%), radial-gradient(ellipse at 70% 70%, rgba(0, 246, 255, 0.1) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 1.5s ease;
        animation: fluid-waves 20s ease infinite alternate;
        mix-blend-mode: screen;
    }

    @keyframes fluid-waves {
        0% { transform: rotate(0deg) scale(1); filter: hue-rotate(0deg); }
        25% { transform: rotate(1deg) scale(1.05); }
        50% { transform: rotate(0deg) scale(1); filter: hue-rotate(45deg); }
        75% { transform: rotate(-1deg) scale(0.95); }
        100% { transform: rotate(0deg) scale(1); filter: hue-rotate(0deg); }
    }

    .mobile-nav.active .mobile-menu-backdrop::before {
        opacity: 1;
    }

    .mobile-menu-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -55%) scale(0.85);
        width: 85%;
        max-width: 350px;
        background: rgba(10, 25, 47, 0.3);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border-radius: 40px;
        padding: 35px 25px;
        opacity: 0;
        transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), 0 0 80px rgba(0, 255, 157, 0.1), inset 0 0 20px rgba(0, 255, 157, 0.05);
        overflow-y: auto;
        scrollbar-width: none;
        -ms-overflow-style: none;
        max-height: 85vh;
        will-change: transform, opacity;
        border: none;
    }

    .mobile-menu-content::-webkit-scrollbar {
        display: none;
    }

    .mobile-menu-content::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.4) 0%, rgba(0, 246, 255, 0.4) 50%, rgba(0, 255, 157, 0.4) 100%);
        border-radius: 42px;
        z-index: -1;
        opacity: 0.4;
        filter: blur(15px);
        animation: border-glow 6s linear infinite;
    }

    @keyframes border-glow {
        0% { opacity: 0.3; filter: blur(15px) hue-rotate(0deg); }
        50% { opacity: 0.5; filter: blur(18px) hue-rotate(30deg); }
        100% { opacity: 0.3; filter: blur(15px) hue-rotate(0deg); }
    }

    .mobile-nav.active .mobile-menu-content {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
        animation: floating-content 8s ease-in-out infinite alternate;
    }

    @keyframes floating-content {
        0% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -52%) scale(1.02); }
        100% { transform: translate(-50%, -50%) scale(1); }
    }

    .mobile-menu-content::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 40px;
        background: radial-gradient(circle at 25% 25%, rgba(0, 255, 157, 0.03) 0%, transparent 15%), radial-gradient(circle at 75% 75%, rgba(0, 246, 255, 0.03) 0%, transparent 15%);
        opacity: 0.3;
        animation: ambient-light 15s ease infinite alternate;
        pointer-events: none;
    }

    @keyframes ambient-light {
        0% { background-position: 0% 0%; opacity: 0.2; }
        50% { background-position: 100% 100%; opacity: 0.4; }
        100% { background-position: 0% 0%; opacity: 0.2; }
    }

    .mobile-nav-link {
        display: flex;
        align-items: center;
        gap: 15px;
        color: white;
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 500;
        padding: 18px 25px;
        margin-bottom: 16px;
        border-radius: 25px;
        background: rgba(0, 255, 157, 0.05);
        transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        opacity: 0;
        transform: translateY(20px);
        will-change: transform, opacity, background;
        border: none;
    }

    .mobile-nav-link::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 25px;
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.3) 0%, rgba(0, 246, 255, 0.3) 50%, rgba(0, 255, 157, 0.3) 100%);
        opacity: 0;
        transition: opacity 0.5s ease;
        z-index: -1;
        filter: blur(5px);
    }

    .mobile-nav-link:hover::before {
        opacity: 0.6;
    }

    .mobile-nav-link::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 70%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: skewX(-25deg);
        transition: all 0.7s cubic-bezier(0.19, 1, 0.22, 1);
        z-index: 1;
    }

    .mobile-nav-link:hover::after {
        left: 130%;
    }

    .mobile-nav.active .mobile-nav-link {
        opacity: 1;
        transform: translateY(0);
    }

    .mobile-nav.active .mobile-nav-link:nth-child(1) {
        transition-delay: 0.1s;
    }
    .mobile-nav.active .mobile-nav-link:nth-child(2) {
        transition-delay: 0.18s;
    }
    .mobile-nav.active .mobile-nav-link:nth-child(3) {
        transition-delay: 0.26s;
    }
    .mobile-nav.active .mobile-nav-link:nth-child(4) {
        transition-delay: 0.34s;
    }
    .mobile-nav.active .mobile-nav-link:nth-child(5) {
        transition-delay: 0.42s;
    }

    .mobile-nav-link:hover {
        background: rgba(0, 255, 157, 0.1);
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1), 0 0 20px rgba(0, 255, 157, 0.15);
    }

    .mobile-nav-link.active {
        background: rgba(0, 255, 157, 0.12);
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.1), inset 0 0 15px rgba(0, 255, 157, 0.05);
    }

    .mobile-nav-icon {
        width: 30px;
        height: 30px;
        fill: #00ff9d;
        filter: drop-shadow(0 0 8px rgba(0, 255, 157, 0.7));
        transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        position: relative;
        z-index: 2;
        opacity: 0.9;
    }

    @keyframes pulse-glow {
        0% { filter: drop-shadow(0 0 8px rgba(0, 255, 157, 0.7)); }
        50% { filter: drop-shadow(0 0 15px rgba(0, 255, 157, 1)); }
        100% { filter: drop-shadow(0 0 8px rgba(0, 255, 157, 0.7)); }
    }

    .mobile-nav-link:hover .mobile-nav-icon {
        transform: rotate(15deg) scale(1.25);
        animation: pulse-glow 2s infinite;
        opacity: 1;
    }

    .mobile-nav-text {
        position: relative;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 2;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: inline-block;
        background: linear-gradient(90deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .mobile-nav-link:hover .mobile-nav-text {
        transform: translateX(8px);
        background: linear-gradient(90deg, rgba(0, 255, 157, 0.9), rgba(0, 246, 255, 0.9));
        -webkit-background-clip: text;
        background-clip: text;
        letter-spacing: 1px;
    }

    .mobile-nav-link.active::after {
        content: '';
        position: absolute;
        top: 50%;
        right: 15px;
        width: 10px;
        height: 10px;
        background: #00ff9d;
        border-radius: 50%;
        transform: translateY(-50%);
        box-shadow: 0 0 10px #00ff9d;
        opacity: 0.7;
        animation: star-pulse 2s ease infinite;
    }

    @keyframes star-pulse {
        0% { transform: translateY(-50%) scale(1); opacity: 0.7; }
        50% { transform: translateY(-50%) scale(1.3); opacity: 1; }
        100% { transform: translateY(-50%) scale(1); opacity: 0.7; }
    }

    /* Media queries para responsividad */
    @media (max-width: 768px) {
        .desktop-nav {
            display: none !important;
        }
        
        .mobile-menu-toggle {
            display: flex !important;
        }
        
        .news-header {
            padding: 0 16px;
            height: 60px;
        }
    }

    /* Ajustes de espaciado para el contenido principal */
    .content-wrapper,
    .news-content,
    .main-content,
    main {
        padding-top: 80px !important;
    }
    `;
    
    // Añadir el estilo al documento
    document.head.appendChild(styleElement);
}

/**
 * Ajusta el contenido principal para asegurar que no quede oculto detrás del header fijo
 */
function adjustMainContent() {
    // Detectar los posibles contenedores principales
    const mainContainers = [
        document.querySelector('.content-wrapper'),
        document.querySelector('.news-content'),
        document.querySelector('.main-content'),
        document.querySelector('main')
    ].filter(Boolean);
    
    if (mainContainers.length === 0) {
        console.log('⚠️ No main containers detected for adjustment');
        return;
    }
    
    // Agregar padding top a los contenedores detectados
    mainContainers.forEach(container => {
        if (container) {
            container.style.paddingTop = '80px';
        }
    });
    
    console.log(`✅ Adjusted ${mainContainers.length} main containers`);
}

// Asegurarse de que el DOM está listo antes de inicializar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    // Inyectar estilos CSS
    injectNavigationStyles();
    
    // Configurar la estructura del menú
    setupNavigation();
    
    // Configurar la funcionalidad del menú móvil
    setupMobileMenu();
    
    // Configurar efectos visuales avanzados
    setupVisualEffects();
    
    // Ajustar el contenido principal
    adjustMainContent();
    
    console.log('✅ Cyber Navigation System - Initialized');
}