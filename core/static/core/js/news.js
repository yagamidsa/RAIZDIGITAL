/**
 * news.js
 * Script para la página de noticias de Raíz Digital
 * Inspirado en las mejores prácticas de Apple y Linux
 */

// Esperar a que se cargue completamente el DOM
document.addEventListener('DOMContentLoaded', function () {
    // Inicializar la biblioteca AOS para animaciones de scroll
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true, // Importante: los elementos solo se animan una vez
        mirror: false,
        disable: 'mobile' // Deshabilitar en móviles (screens < 768px)
    });

    // Referenciar elementos del DOM
    const backToTopButton = document.getElementById('backToTop');
    const newsCards = document.querySelectorAll('.news-card, .featured-article');
    const cyberGrid = document.querySelector('.cyber-grid');

    // Configurar animaciones para las tarjetas de noticias
    setupNewsCardAnimations(newsCards);

    // Configurar animación para el grid de fondo
    setupGridAnimation(cyberGrid);

    // Configurar el botón para volver arriba
    setupBackToTopButton(backToTopButton);

    // Configurar efectos especiales para los enlaces
    setupLinkEffects();

    // Comprobar si hay imágenes y precargadas para mejor rendimiento
    preloadNewsImages();

    // Configurar la navegación responsive
    setupResponsiveNavigation();

    // Iniciar animación de texto para el título
    animateNewsTitle();

    // Configurar interacción con la paginación
    setupPagination();
});

/**
 * Configura animaciones para las tarjetas de noticias
 * @param {NodeList} cards - Colección de tarjetas de noticias
 */
function setupNewsCardAnimations(cards) {
    // Animar tarjetas con un retraso escalonado para efecto secuencial
    cards.forEach((card, index) => {
        // Usar setTimeout para crear el efecto secuencial
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);

        // Añadir efecto "tilt" sutil al pasar el ratón
        card.addEventListener('mousemove', (e) => {
            if (window.innerWidth <= 768) return; // No aplicar en dispositivos móviles

            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const deltaX = (x - centerX) / centerX;
            const deltaY = (y - centerY) / centerY;

            // Rotar ligeramente la tarjeta según la posición del ratón
            card.style.transform = `translateY(-5px) rotateX(${deltaY * -2}deg) rotateY(${deltaX * 2}deg)`;
        });

        // Restaurar la posición original al quitar el ratón
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

/**
 * Configura la animación del grid cibernético
 * @param {HTMLElement} grid - El elemento grid de fondo
 */
function setupGridAnimation(grid) {
    if (!grid) return;

    // Añadir animación con mejor rendimiento usando transform
    grid.style.animation = 'gridMove 20s linear infinite';

    // El efecto parallax sutil al mover el ratón
    document.addEventListener('mousemove', (e) => {
        const moveX = (e.clientX - window.innerWidth / 2) * 0.005;
        const moveY = (e.clientY - window.innerHeight / 2) * 0.005;

        grid.style.transform = `perspective(500px) rotateX(60deg) translateY(calc(var(--scroll-y, 0) * 0.1px)) translateX(${moveX}px)`;
    });

    // Actualizar posición vertical basada en scroll
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY || window.pageYOffset;
        document.documentElement.style.setProperty('--scroll-y', scrollY);
    });
}

/**
 * Configura el botón para volver al inicio
 * @param {HTMLElement} button - El botón back-to-top
 */
function setupBackToTopButton(button) {
    if (!button) return;

    // Mostrar/ocultar botón basado en la posición de scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            button.classList.add('visible');
        } else {
            button.classList.remove('visible');
        }
    });

    // Añadir funcionalidad de scroll suave al hacer clic
    button.addEventListener('click', (e) => {
        e.preventDefault();

        // Animación suave al estilo iOS
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });

        // Efecto visual al hacer clic
        button.classList.add('clicked');
        setTimeout(() => {
            button.classList.remove('clicked');
        }, 300);
    });
}

/**
 * Configura efectos especiales para los enlaces
 */
function setupLinkEffects() {
    // Seleccionar todos los enlaces con clase .read-more
    const readMoreButtons = document.querySelectorAll('.read-more');

    readMoreButtons.forEach(button => {
        // Efecto de destello al pasar el ratón
        button.addEventListener('mouseenter', () => {
            button.style.transition = 'all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1)';
        });

        // Efecto al hacer clic
        button.addEventListener('click', (e) => {
            // Crear el efecto de onda al hacer clic (estilo Material Design con estética Apple)
            const ripple = document.createElement('span');
            ripple.classList.add('button-ripple');

            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            ripple.style.cssText = `
                position: absolute;
                width: 100px;
                height: 100px;
                background: rgba(255, 255, 255, 0.4);
                border-radius: 50%;
                left: ${x - 50}px;
                top: ${y - 50}px;
                pointer-events: none;
                transform: scale(0);
                opacity: 1;
                transition: transform 0.6s, opacity 0.6s;
            `;

            button.appendChild(ripple);

            // Iniciar la animación después de un pequeño retardo para que el navegador procese el elemento
            setTimeout(() => {
                ripple.style.transform = 'scale(3)';
                ripple.style.opacity = '0';

                // Eliminar el elemento una vez terminada la animación
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            }, 10);
        });
    });

    // Configurar los enlaces de navegación
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            // Simular efecto de "expansión" de subrayado estilo macOS
            const underline = link.querySelector('::after') || link;
            if (underline) {
                link.style.transition = 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            }
        });
    });
}

/**
 * Precarga las imágenes de las noticias para mejorar el rendimiento
 */
function preloadNewsImages() {
    // Obtener todas las URL de las imágenes en las tarjetas de noticias
    const cardImages = document.querySelectorAll('.card-image, .featured-image');
    const imageUrls = [];

    cardImages.forEach(imgContainer => {
        const style = getComputedStyle(imgContainer);
        const url = style.backgroundImage.slice(4, -1).replace(/["']/g, "");

        if (url && !url.includes('none') && !imageUrls.includes(url)) {
            imageUrls.push(url);
        }
    });

    // Precargar las imágenes
    imageUrls.forEach(url => {
        const img = new Image();
        img.src = url;
    });
}

/**
 * Configura la navegación responsive para dispositivos móviles
 */
function setupResponsiveNavigation() {
    // En dispositivos móviles, mostrar/ocultar menú al hacer clic en un botón
    const mobileWidth = 768;

    // Comprobar si estamos en un dispositivo móvil
    if (window.innerWidth <= mobileWidth) {
        // Crear un botón de menú para móviles si no existe
        if (!document.querySelector('.mobile-menu-toggle')) {
            const menuToggle = document.createElement('button');
            menuToggle.className = 'mobile-menu-toggle';
            menuToggle.innerHTML = `
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            `;

            const header = document.querySelector('.news-header');
            const nav = document.querySelector('.news-nav');

            if (header && nav) {
                // Insertar el botón de menú en el encabezado
                header.appendChild(menuToggle);

                // Añadir clase para estilizar en móvil
                nav.classList.add('mobile-nav');

                // Toggler del menú móvil
                menuToggle.addEventListener('click', () => {
                    nav.classList.toggle('active');
                    menuToggle.classList.toggle('active');

                    // Animar apertura/cierre con estilo iOS
                    if (nav.classList.contains('active')) {
                        nav.style.transform = 'translateY(0)';
                        nav.style.opacity = '1';
                    } else {
                        nav.style.transform = 'translateY(-20px)';
                        nav.style.opacity = '0';
                    }
                });
            }
        }
    }
}

/**
 * Anima el título principal con efecto degradado animado
 */
function animateNewsTitle() {
    const title = document.querySelector('.news-title');
    if (!title) return;

    // Configurar la animación del título
    title.style.backgroundSize = '200% auto';
    title.style.animation = 'textGradient 4s linear infinite';

    // Definir la animación si no existe
    if (!document.querySelector('#title-animation')) {
        const style = document.createElement('style');
        style.id = 'title-animation';
        style.textContent = `
            @keyframes textGradient {
                0% { background-position: 0% center; }
                100% { background-position: 200% center; }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Configura la interacción con la paginación
 */
function setupPagination() {
    const paginationLinks = document.querySelectorAll('.page-link');

    paginationLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Prevenir navegación real ya que esto sería manejado por el backend
            e.preventDefault();

            // Quitar la clase active de todos los enlaces
            paginationLinks.forEach(l => l.classList.remove('active'));

            // Añadir la clase active al enlace clickeado
            link.classList.add('active');

            // En un sistema real, aquí iría el código para cargar la página seleccionada
            // Por ahora, solo añadimos un efecto visual

            // Simular efecto de "pulsación" estilo iOS
            link.style.transform = 'scale(0.95)';
            setTimeout(() => {
                link.style.transform = '';
            }, 200);

            // Simular carga de página (en implementación real, se cargarían los datos mediante AJAX)
            simulatePageChange(link);
        });
    });
}

/**
 * Simula un cambio de página para propósitos de demostración
 * @param {HTMLElement} link - El enlace de paginación clickeado
 */
function simulatePageChange(link) {
    // Obtener el número de página del enlace
    const page = link.textContent;

    // Verificar si es un número de página válido
    if (!isNaN(page)) {
        // Añadir indicador de carga
        const newsGrid = document.querySelector('.news-grid');
        if (newsGrid) {
            // Crear y añadir el indicador de carga
            const loadingIndicator = document.createElement('div');
            loadingIndicator.className = 'loading-indicator';
            loadingIndicator.innerHTML = `
                <svg class="spinner" viewBox="0 0 50 50">
                    <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                </svg>
                <p>Cargando página ${page}...</p>
            `;

            // Aplicar estilos al indicador de carga
            loadingIndicator.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: var(--news-accent);
                z-index: 10;
            `;

            const spinner = loadingIndicator.querySelector('.spinner');
            spinner.style.cssText = `
                animation: rotate 2s linear infinite;
                width: 50px;
                height: 50px;
                margin: 0 auto 20px;
            `;

            const circle = loadingIndicator.querySelector('.path');
            circle.style.cssText = `
                stroke: var(--news-accent);
                stroke-linecap: round;
                animation: dash 1.5s ease-in-out infinite;
            `;

            // Definir animaciones para el spinner
            const spinnerStyle = document.createElement('style');
            spinnerStyle.textContent = `
                @keyframes rotate {
                    100% { transform: rotate(360deg); }
                }
                @keyframes dash {
                    0% {
                        stroke-dasharray: 1, 150;
                        stroke-dashoffset: 0;
                    }
                    50% {
                        stroke-dasharray: 90, 150;
                        stroke-dashoffset: -35;
                    }
                    100% {
                        stroke-dasharray: 90, 150;
                        stroke-dashoffset: -124;
                    }
                }
            `;
            document.head.appendChild(spinnerStyle);

            // Aplicar efecto de "desenfoque" a las tarjetas existentes
            const allCards = document.querySelectorAll('.news-card, .featured-article');
            allCards.forEach(card => {
                card.style.opacity = '0.5';
                card.style.filter = 'blur(2px)';
                card.style.transition = 'opacity 0.3s, filter 0.3s';
            });

            // Añadir el indicador al grid
            newsGrid.appendChild(loadingIndicator);

            // Simular retardo de carga y luego restaurar las tarjetas
            setTimeout(() => {
                // Restaurar las tarjetas
                allCards.forEach(card => {
                    card.style.opacity = '1';
                    card.style.filter = 'none';
                });

                // Eliminar el indicador de carga
                loadingIndicator.remove();

                // Hacer scroll suave hacia arriba - experiencia tipo Apple
                window.scrollTo({
                    top: newsGrid.offsetTop - 100,
                    behavior: 'smooth'
                });
            }, 1000);
        }
    }
}

// Inicializar detector de color de fondo para ajustes de contraste
function initBackgroundColorDetector() {
    // Esta función detecta el color de fondo real y ajusta los elementos para mejor contraste
    // Útil para temas oscuros/claros o cuando el usuario tiene configuraciones personalizadas

    const bgColor = getComputedStyle(document.body).backgroundColor;
    const rgb = bgColor.match(/\d+/g);

    if (rgb && rgb.length >= 3) {
        const [r, g, b] = rgb.map(Number);
        const brightness = (r * 299 + g * 587 + b * 114) / 1000;

        // Si el fondo es claro, ajustar los colores para mejor contraste
        if (brightness > 125) {
            document.documentElement.classList.add('light-theme');
        } else {
            document.documentElement.classList.add('dark-theme');
        }
    }
}

// Detector de preferencias del sistema para adaptar la UI
function initSystemPreferences() {
    // Detector de preferencias de movimiento reducido
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.documentElement.classList.add('reduced-motion');
    }

    // Detector de tema del sistema
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('system-dark-theme');
    } else {
        document.documentElement.classList.add('system-light-theme');
    }
}

// Inicializar estas funciones al final
document.addEventListener('DOMContentLoaded', function () {
    initBackgroundColorDetector();
    initSystemPreferences();
});


