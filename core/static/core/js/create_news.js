document.addEventListener('DOMContentLoaded', function() {
    // Inicializar AOS para animaciones de scroll
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        mirror: false
    });
    
    // Vista previa de imagen
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    
    if (imageInput && imagePreview && previewImg) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    imagePreview.style.display = 'block';
                    
                    // Aplicar efecto de aparición
                    anime({
                        targets: imagePreview,
                        opacity: [0, 1],
                        translateY: [20, 0],
                        duration: 500,
                        easing: 'easeOutQuad'
                    });
                }
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Función para hacer drag and drop de imágenes
    const imageUploadContainer = document.getElementById('imageUploadContainer');
    
    if (imageUploadContainer) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            imageUploadContainer.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            imageUploadContainer.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            imageUploadContainer.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            imageUploadContainer.classList.add('highlight');
        }
        
        function unhighlight() {
            imageUploadContainer.classList.remove('highlight');
        }
        
        imageUploadContainer.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files && files[0]) {
                imageInput.files = files;
                
                // Disparar el evento change para actualizar la vista previa
                const event = new Event('change');
                imageInput.dispatchEvent(event);
            }
        }
    }
    
    // Toggle destacado
    const toggleInput = document.getElementById('destacado');
    const toggleText = document.querySelector('.toggle-text');
    
    if (toggleInput && toggleText) {
        toggleInput.addEventListener('change', function() {
            toggleText.textContent = this.checked ? 'Sí' : 'No';
            
            // Efecto visual al cambiar estado
            anime({
                targets: toggleText,
                opacity: [0.5, 1],
                translateX: [5, 0],
                easing: 'easeOutQuad',
                duration: 300
            });
        });
    }
    
    // Efectos para el formulario
    const formGroups = document.querySelectorAll('.form-group');
    if (formGroups.length > 0) {
        // Aplicar efecto de entrada escalonado a los campos del formulario
        anime.timeline({
            easing: 'easeOutQuad'
        }).add({
            targets: formGroups,
            opacity: [0, 1],
            translateY: [15, 0],
            delay: anime.stagger(100),
            duration: 500
        });
        
        // Efecto de foco en los campos
        const formInputs = document.querySelectorAll('.form-input, .form-textarea, .form-select');
        formInputs.forEach(input => {
            input.addEventListener('focus', function() {
                const parent = this.closest('.form-group');
                if (parent) {
                    anime({
                        targets: parent,
                        translateX: [5, 0],
                        duration: 300,
                        easing: 'easeOutQuad'
                    });
                }
            });
        });
    }
    
    // Validación del formulario
    const newsForm = document.getElementById('newsForm');
    if (newsForm) {
        newsForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validar título
            const titulo = document.getElementById('titulo');
            if (titulo && titulo.value.trim() === '') {
                isValid = false;
                showFieldError(titulo, 'El título es obligatorio');
            }
            
            // Validar resumen
            const resumen = document.getElementById('resumen');
            if (resumen && resumen.value.trim() === '') {
                isValid = false;
                showFieldError(resumen, 'El resumen es obligatorio');
            } else if (resumen && resumen.value.length > 200) {
                isValid = false;
                showFieldError(resumen, 'El resumen debe tener máximo 200 caracteres');
            }
            
            // Validar contenido
            const contenido = document.getElementById('contenido');
            if (contenido && contenido.value.trim() === '') {
                isValid = false;
                showFieldError(contenido, 'El contenido es obligatorio');
            }
            
            // Si no es válido, evitar el envío
            if (!isValid) {
                e.preventDefault();
                
                // Mostrar mensaje de error general
                const errorMsg = document.createElement('div');
                errorMsg.className = 'error-message';
                errorMsg.innerHTML = `
                    <svg class="error-icon" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                    <span>Por favor, corrige los errores en el formulario</span>
                `;
                
                // Insertar mensaje al inicio del formulario
                newsForm.insertBefore(errorMsg, newsForm.firstChild);
                
                // Hacer scroll al inicio del formulario
                window.scrollTo({
                    top: newsForm.offsetTop - 100,
                    behavior: 'smooth'
                });
                
                // Remover mensaje después de un tiempo
                setTimeout(() => {
                    if (errorMsg.parentNode) {
                        anime({
                            targets: errorMsg,
                            opacity: [1, 0],
                            height: [errorMsg.offsetHeight, 0],
                            marginBottom: [16, 0],
                            duration: 500,
                            easing: 'easeOutQuad',
                            complete: () => {
                                if (errorMsg.parentNode) {
                                    errorMsg.parentNode.removeChild(errorMsg);
                                }
                            }
                        });
                    }
                }, 5000);
            } else {
                // Si el formulario es válido, mostrar un indicador de carga
                const submitBtn = document.querySelector('.btn-submit-news');
                if (submitBtn) {
                    // Cambiar texto del botón
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<span class="spinner"></span> Publicando...';
                    
                    // Desactivar botón
                    submitBtn.disabled = true;
                    
                    // Aplicar estilo de desactivado
                    submitBtn.style.opacity = '0.7';
                    submitBtn.style.cursor = 'wait';
                    
                    // No evitamos el envío del formulario porque queremos que se envíe
                }
            }
        });
        
        // Función para mostrar error en un campo
        function showFieldError(field, message) {
            // Añadir clase de error
            field.classList.add('field-error');
            
            // Crear mensaje de error
            const errorSpan = document.createElement('span');
            errorSpan.className = 'field-error-message';
            errorSpan.textContent = message;
            
            // Insertar después del campo
            field.parentNode.appendChild(errorSpan);
            
            // Efecto visual de error
            anime({
                targets: field,
                translateX: [10, -10, 10, -10, 0],
                duration: 400,
                easing: 'easeInOutQuad'
            });
            
            // Remover mensaje al corregir
            field.addEventListener('input', function() {
                this.classList.remove('field-error');
                if (errorSpan.parentNode) {
                    errorSpan.parentNode.removeChild(errorSpan);
                }
            }, { once: true });
        }
    }
    
    // Botón volver arriba
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Contador de caracteres para el resumen
    const resumenTextarea = document.getElementById('resumen');
    if (resumenTextarea) {
        // Crear contador
        const counterSpan = document.createElement('span');
        counterSpan.className = 'char-counter';
        counterSpan.textContent = `0/200 caracteres`;
        resumenTextarea.parentNode.appendChild(counterSpan);
        
        // Actualizar contador en cada cambio
        resumenTextarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            counterSpan.textContent = `${currentLength}/200 caracteres`;
            
            // Cambiar color si excede el límite
            if (currentLength > 200) {
                counterSpan.classList.add('counter-exceeded');
            } else {
                counterSpan.classList.remove('counter-exceeded');
            }
        });
    }
    
    console.log('Efectos del formulario de noticias inicializados correctamente');
});