// Este archivo se encargará de la interfaz neural y los efectos holográficos
class NeuralInterface {
    constructor() {
        this.initThreeJS();
        this.initHologram();
        this.initFormSteps();
        this.initParticleSystem();
        this.initDataVisualization();
    }

    initThreeJS() {
        // Configuración de Three.js
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('holographic-container').appendChild(this.renderer.domElement);

        // Posición de la cámara
        this.camera.position.z = 5;

        // Luces
        const ambientLight = new THREE.AmbientLight(0x00ff9d, 0.5);
        this.scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0x00ff9d, 1);
        pointLight.position.set(5, 5, 5);
        this.scene.add(pointLight);
    }

    initHologram() {
        // Geometría del holograma
        const geometry = new THREE.TorusGeometry(2, 0.1, 16, 100);
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                color: { value: new THREE.Color(0x00ff9d) }
            },
            vertexShader: `
                varying vec2 vUv;
                uniform float time;
                
                void main() {
                    vUv = uv;
                    vec3 pos = position;
                    pos.y += sin(pos.x * 2.0 + time) * 0.1;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                varying vec2 vUv;
                uniform vec3 color;
                uniform float time;
                
                void main() {
                    float intensity = sin(vUv.y * 10.0 + time) * 0.5 + 0.5;
                    vec3 finalColor = color * intensity;
                    gl_FragColor = vec4(finalColor, 0.5);
                }
            `,
            transparent: true
        });

        this.hologram = new THREE.Mesh(geometry, material);
        this.scene.add(this.hologram);

        // Animación
        this.animate();
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        this.hologram.rotation.x += 0.01;
        this.hologram.rotation.y += 0.01;
        this.hologram.material.uniforms.time.value += 0.05;

        this.renderer.render(this.scene, this.camera);
    }

    initFormSteps() {
        const steps = document.querySelectorAll('.form-step');
        const nextBtns = document.querySelectorAll('.next-step-btn');
        let currentStep = 0;

        nextBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                this.validateStep(currentStep).then(isValid => {
                    if (isValid) {
                        this.animateStepTransition(steps[currentStep], steps[currentStep + 1]);
                        currentStep++;
                    }
                });
            });
        });

        // Código de verificación
        const codeInputs = document.querySelectorAll('.code-input');
        codeInputs.forEach((input, index) => {
            input.addEventListener('input', () => {
                if (input.value.length === 1) {
                    if (index < codeInputs.length - 1) {
                        codeInputs[index + 1].focus();
                    }
                }
            });

            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && input.value.length === 0) {
                    if (index > 0) {
                        codeInputs[index - 1].focus();
                    }
                }
            });
        });
    }

    async validateStep(step) {
        const validation = anime.timeline({
            duration: 1000,
            easing: 'easeInOutQuart'
        });

        validation
            .add({
                targets: '.neural-validation',
                scaleX: [0, 1],
                opacity: [0, 1]
            })
            .add({
                targets: '.validation-text',
                opacity: [0, 1],
                translateY: [-20, 0]
            });

        return new Promise(resolve => {
            setTimeout(() => resolve(true), 1500);
        });
    }

    animateStepTransition(currentStep, nextStep) {
        const timeline = anime.timeline({
            easing: 'easeOutExpo'
        });

        timeline
            .add({
                targets: currentStep,
                opacity: 0,
                translateX: -50,
                duration: 500
            })
            .add({
                targets: nextStep,
                opacity: [0, 1],
                translateX: [50, 0],
                duration: 500,
                begin: () => {
                    currentStep.classList.remove('active');
                    nextStep.classList.add('active');
                }
            });
    }

    initParticleSystem() {
        const particles = [];
        const particleCount = 50;

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: Math.random() * 2 + 1,
                speedX: (Math.random() - 0.5) * 2,
                speedY: (Math.random() - 0.5) * 2
            });
        }

        function updateParticles() {
            particles.forEach(particle => {
                particle.x += particle.speedX;
                particle.y += particle.speedY;

                if (particle.x < 0 || particle.x > window.innerWidth) particle.speedX *= -1;
                if (particle.y < 0 || particle.y > window.innerHeight) particle.speedY *= -1;
            });

            requestAnimationFrame(updateParticles);
        }

        updateParticles();
    }

    initDataVisualization() {
        const canvas = document.getElementById('dataCanvas');
        const ctx = canvas.getContext('2d');

        function drawData() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Onda de datos
            ctx.beginPath();
            ctx.strokeStyle = '#00ff9d';
            ctx.lineWidth = 2;

            for (let i = 0; i < canvas.width; i++) {
                const y = canvas.height / 2 + 
                         Math.sin(i * 0.02 + Date.now() * 0.001) * 30 +
                         Math.sin(i * 0.01 + Date.now() * 0.002) * 20;
                
                if (i === 0) {
                    ctx.moveTo(i, y);
                } else {
                    ctx.lineTo(i, y);
                }
            }

            ctx.stroke();
            requestAnimationFrame(drawData);
        }

        drawData();
    }
}

// Inicializar la interfaz
document.addEventListener('DOMContentLoaded', () => {
    const interface = new NeuralInterface();
});