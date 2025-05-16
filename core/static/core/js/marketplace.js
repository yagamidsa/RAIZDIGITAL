// marketplace.js - Funcionalidades para el marketplace indígena de Raíz Digital

// Esperar a que todo el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const navbar = document.getElementById('navbar');
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const backToTopBtn = document.getElementById('backToTop');
    const cartBtn = document.querySelector('.cart-btn');
    const cartModal = document.getElementById('cartModal');
    const closeModal = document.querySelector('.close-modal');
    const continueBtn = document.querySelector('.btn-continue');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const userBtn = document.querySelector('.user-btn');
    const userMenu = document.querySelector('.user-menu');
    
    // Animaciones de carga inicial
    animateOnLoad();
    
    // Cambio de estado del navbar al hacer scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            
            if (backToTopBtn) {
                backToTopBtn.classList.add('active');
            }
        } else {
            navbar.classList.remove('scrolled');
            
            if (backToTopBtn) {
                backToTopBtn.classList.remove('active');
            }
        }
        
        // Animar elementos cuando son visibles
        animateOnScroll();
    });
    
    // Menú móvil
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }
    
    // Modal del carrito
    if (cartBtn) {
        cartBtn.addEventListener('click', function() {
            cartModal.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Animar contenido del modal
            setTimeout(() => {
                cartModal.querySelector('.modal-content').classList.add('active');
            }, 10);
        });
    }
    
    // Cerrar modal
    if (closeModal) {
        closeModal.addEventListener('click', closeCartModal);
    }
    
    if (continueBtn) {
        continueBtn.addEventListener('click', closeCartModal);
    }
    
    // También cerrar al hacer clic fuera del modal
    if (cartModal) {
        cartModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeCartModal();
            }
        });
    }
    
    // Botón volver arriba
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Filtrado de productos
    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remover clase active de todos los botones
                filterBtns.forEach(b => b.classList.remove('active'));
                
                // Añadir clase active al botón clicado
                this.classList.add('active');
                
                // Obtener valor del filtro
                const filter = this.getAttribute('data-filter');
                
                // Aquí iría la lógica para filtrar los productos
                // Por ahora es solo para demostración de la UI
                console.log(`Filtrando productos por: ${filter}`);
                
                // Simular carga de nuevos productos con una pequeña animación
                const productsGrid = document.querySelector('.products-grid');
                if (productsGrid) {
                    productsGrid.style.opacity = '0.5';
                    
                    setTimeout(() => {
                        productsGrid.style.opacity = '1';
                    }, 300);
                }
            });
        });
    }
    
    // Tabs de noticias y eventos
    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remover clase active de todos los botones
                tabBtns.forEach(b => b.classList.remove('active'));
                
                // Añadir clase active al botón clicado
                this.classList.add('active');
                
                // Obtener id del tab
                const tabId = this.getAttribute('data-tab');
                
                // Ocultar todos los tabs
                document.querySelectorAll('.tab-pane').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Mostrar el tab seleccionado
                document.getElementById(tabId).classList.add('active');
            });
        });
    }
    
    // Menú de usuario (dropdown)
    if (userBtn && userMenu) {
        userBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenu.classList.toggle('active');
        });
        
        // Cerrar el menú al hacer clic fuera
        document.addEventListener('click', function() {
            if (userMenu.classList.contains('active')) {
                userMenu.classList.remove('active');
            }
        });
        
        // Evitar que se cierre al hacer clic dentro del menú
        userMenu.querySelector('.dropdown-menu').addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Botones de Añadir al carrito
    const addToCartBtns = document.querySelectorAll('.cart-add-btn');
    if (addToCartBtns.length > 0) {
        addToCartBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Animación de éxito
                const successAnimation = addToCartAnimation(this);
                
                // Actualizar contador del carrito
                updateCartCount(1);
                
                // Mostrar notificación
                showNotification('Producto añadido al carrito', 'success');
            });
        });
    }
    
    // Botones de Añadir a favoritos
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    if (wishlistBtns.length > 0) {
        wishlistBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Alternar estado activo
                this.classList.toggle('liked');
                
                // Cambiar color del icono
                if (this.classList.contains('liked')) {
                    this.querySelector('svg').style.fill = '#db3a34';
                    showNotification('Producto añadido a favoritos', 'success');
                } else {
                    this.querySelector('svg').style.fill = '';
                    showNotification('Producto eliminado de favoritos', 'info');
                }
            });
        });
    }
    
    // Formulario de Newsletter
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email && isValidEmail(email)) {
                // Simulación de envío exitoso
                showNotification('¡Te has suscrito correctamente!', 'success');
                emailInput.value = '';
            } else {
                showNotification('Por favor, introduce un email válido', 'error');
            }
        });
    }
    
    // Inicializar observadores de intersección para animaciones
    initIntersectionObservers();
});

// Función para cerrar el modal del carrito
function closeCartModal() {
    const cartModal = document.getElementById('cartModal');
    
    if (cartModal) {
        cartModal.querySelector('.modal-content').classList.remove('active');
        
        setTimeout(() => {
            cartModal.classList.remove('active');
            document.body.style.overflow = '';
        }, 300);
    }
}

// Función para actualizar el contador del carrito
function updateCartCount(change) {
    const cartCount = document.querySelector('.cart-count');
    
    if (cartCount) {
        let currentCount = parseInt(cartCount.textContent);
        currentCount += change;
        
        // Animación de cambio
        cartCount.style.transform = 'scale(1.3)';
        cartCount.textContent = currentCount;
        
        setTimeout(() => {
            cartCount.style.transform = '';
        }, 300);
    }
}

// Animación para añadir al carrito
function addToCartAnimation(button) {
    // Crear elemento para la animación
    const animEl = document.createElement('div');
    animEl.style.cssText = `
        position: absolute;
        width: 20px;
        height: 20px;
        background-color: var(--primary);
        border-radius: 50%;
        z-index: 100;
        pointer-events: none;
    `;
    
    // Obtener posiciones
    const buttonRect = button.getBoundingClientRect();
    const cartBtn = document.querySelector('.cart-btn');
    const cartRect = cartBtn.getBoundingClientRect();
    
    // Posicionar elemento
    animEl.style.top = `${buttonRect.top + buttonRect.height/2}px`;
    animEl.style.left = `${buttonRect.left + buttonRect.width/2}px`;
    
    document.body.appendChild(animEl);
    
    // Animar el elemento hacia el carrito
    const anim = animEl.animate([
        { 
            top: `${buttonRect.top + buttonRect.height/2}px`,
            left: `${buttonRect.left + buttonRect.width/2}px`,
            opacity: 1,
            transform: 'scale(1)'
        },
        { 
            top: `${cartRect.top + cartRect.height/2}px`,
            left: `${cartRect.left + cartRect.width/2}px`,
            opacity: 0.8,
            transform: 'scale(0.5)'
        }
    ], {
        duration: 500,
        easing: 'ease-out'
    });
    
    anim.onfinish = () => {
        animEl.remove();
        
        // Animar el icono del carrito
        cartBtn.animate([
            { transform: 'scale(1)' },
            { transform: 'scale(1.2)' },
            { transform: 'scale(1)' }
        ], {
            duration: 300,
            easing: 'ease-out'
        });
    };
    
    return anim;
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento para la notificación
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Estilos base
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 12px 20px;
        background-color: white;
        color: var(--dark);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-md);
        z-index: 9999;
        transform: translateY(20px);
        opacity: 0;
        transition: all 0.3s ease;
    `;
    
    // Estilos según el tipo
    if (type === 'success') {
        notification.style.borderLeft = '4px solid var(--primary)';
    } else if (type === 'error') {
        notification.style.borderLeft = '4px solid var(--secondary)';
    } else if (type === 'info') {
        notification.style.borderLeft = '4px solid var(--accent)';
    }
    
    // Añadir al DOM
    document.body.appendChild(notification);
    
    // Mostrar con animación
    setTimeout(() => {
        notification.style.transform = 'translateY(0)';
        notification.style.opacity = '1';
    }, 10);
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateY(20px)';
        notification.style.opacity = '0';
        
        // Eliminar del DOM después de la animación
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Validar email
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Animar elementos al cargar la página
function animateOnLoad() {
    // Animar hero section
    const heroElements = document.querySelectorAll('.hero-title, .hero-subtitle, .hero-buttons, .decoration-element');
    
    if (heroElements.length) {
        heroElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.8s ease-out';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }
}

// Animar elementos al hacer scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('[data-animate]');
    
    elements.forEach(element => {
        if (isElementInViewport(element) && !element.classList.contains('animated')) {
            element.classList.add('animated');
        }
    });
}

// Detectar si un elemento está en el viewport
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
        rect.bottom >= 0
    );
}

// Inicializar observadores de intersección para animaciones
function initIntersectionObservers() {
    // Comprobar soporte para Intersection Observer
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    
                    // Animar sección
                    if (element.classList.contains('section-header')) {
                        animateSection(element.parentElement);
                    }
                    
                    // Animar cards
                    if (element.classList.contains('product-card') || 
                        element.classList.contains('community-card') ||
                        element.classList.contains('artisan-card') ||
                        element.classList.contains('news-card') ||
                        element.classList.contains('event-card')) {
                        
                        animateCard(element);
                    }
                    
                    // Dejar de observar después de la animación
                    observer.unobserve(element);
                }
            });
        }, observerOptions);
        
        // Observar secciones
        document.querySelectorAll('.section-header, .product-card, .community-card, .artisan-card, .news-card, .event-card').forEach(element => {
            observer.observe(element);
        });
    } else {
        // Fallback para navegadores sin soporte para Intersection Observer
        window.addEventListener('scroll', animateOnScroll);
        animateOnScroll(); // Animar elementos visibles inicialmente
    }
}

// Animar una sección completa
function animateSection(section) {
    if (!section) return;
    
    // Animar título y subtítulo
    const title = section.querySelector('.section-title');
    const subtitle = section.querySelector('.section-subtitle');
    
    if (title) {
        title.animate([
            { opacity: 0, transform: 'translateY(20px)' },
            { opacity: 1, transform: 'translateY(0)' }
        ], {
            duration: 800,
            easing: 'ease-out',
            fill: 'forwards'
        });
    }
    
    if (subtitle) {
        subtitle.animate([
            { opacity: 0, transform: 'translateY(20px)' },
            { opacity: 1, transform: 'translateY(0)' }
        ], {
            duration: 800,
            delay: 200,
            easing: 'ease-out',
            fill: 'forwards'
        });
    }
    
    // Animar botones o filtros
    const buttons = section.querySelectorAll('.filter-btn, .tab-btn');
    buttons.forEach((button, index) => {
        button.animate([
            { opacity: 0, transform: 'translateY(20px)' },
            { opacity: 1, transform: 'translateY(0)' }
        ], {
            duration: 800,
            delay: 300 + (50 * index),
            easing: 'ease-out',
            fill: 'forwards'
        });
    });
}

// Animar una card
function animateCard(card) {
    card.animate([
        { opacity: 0, transform: 'translateY(30px)' },
        { opacity: 1, transform: 'translateY(0)' }
    ], {
        duration: 600,
        easing: 'ease-out',
        fill: 'forwards'
    });
}

// Inicializar efectos de partículas en el canvas
function initParticles() {
    const canvas = document.getElementById('backgroundCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const particles = [];
    const particleCount = 50;
    
    // Configurar canvas
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Redimensionar canvas cuando cambia el tamaño de la ventana
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    
    // Crear partículas
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2 + 1,
            color: 'rgba(0, 246, 255, 0.5)',
            velocity: {
                x: (Math.random() - 0.5) * 0.5,
                y: (Math.random() - 0.5) * 0.5
            }
        });
    }
    
    // Función para dibujar partículas
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.fill();
            
            // Mover partícula
            particle.x += particle.velocity.x;
            particle.y += particle.velocity.y;
            
            // Rebotar en los bordes
            if (particle.x < 0 || particle.x > canvas.width) {
                particle.velocity.x = -particle.velocity.x;
            }
            
            if (particle.y < 0 || particle.y > canvas.height) {
                particle.velocity.y = -particle.velocity.y;
            }
            
            // Dibujar conexiones
            particles.forEach(otherParticle => {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(0, 246, 255, ${0.1 * (1 - distance / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particle.x, particle.y);
                    ctx.lineTo(otherParticle.x, otherParticle.y);
                    ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(drawParticles);
    }
    
    // Iniciar animación
    drawParticles();
}

// Inicializar todos los efectos visuales cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar partículas si existe el canvas
    initParticles();
});