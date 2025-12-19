

document.addEventListener('DOMContentLoaded', function() {
    console.log('%c🔮 Код Судьбы Активирован 🔮', 
        'color: #FFD700; font-size: 18px; font-weight: bold; text-shadow: 0 0 10px #FFD700');
    
    // Инициализация частиц для фона
    initFloatingParticles();
    
    // Плавная прокрутка к якорям
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') !== '#' && this.getAttribute('href') !== '#!') {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    // Добавляем эффект свечения при клике
                    this.classList.add('clicked');
                    setTimeout(() => this.classList.remove('clicked'), 300);
                    
                    // Плавная прокрутка
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Автоматическое заполнение текущего года
    const yearInput = document.getElementById('id_target_year');
    if (yearInput && !yearInput.value) {
        const currentYear = new Date().getFullYear();
        yearInput.value = currentYear;
        addInputEffect(yearInput);
    }
    
    // Автоматическое заполнение текущей даты для дня
    const dateInput = document.getElementById('id_target_date');
    if (dateInput && !dateInput.value) {
        const today = new Date();
        const formattedDate = today.toISOString().split('T')[0];
        dateInput.value = formattedDate;
        addInputEffect(dateInput);
    }
    
    // Эффекты при фокусе на полях ввода
    document.querySelectorAll('.mystic-input').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            createRippleEffect(this);
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Анимация чисел при появлении
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                if (entry.target.classList.contains('number-circle')) {
                    animateNumber(entry.target);
                }
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.number-circle, .calculator-section, .nav-card').forEach(element => {
        observer.observe(element);
    });
    
    // Подсветка активной навигации при прокрутке
    const sections = document.querySelectorAll('.calculator-section');
    const navLinks = document.querySelectorAll('.nav-card[href^="#"]');
    
    function highlightNavLink() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.scrollY >= (sectionTop - 100)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', highlightNavLink);
    
    // Эффект для кнопок при наведении
    document.querySelectorAll('.mystic-button, .details-button, .back-button').forEach(button => {
        button.addEventListener('mouseenter', function() {
            createButtonSparkle(this);
        });
    });
    
    // Показ/скрытие подробностей с анимацией
    document.querySelectorAll('[id$="-details-btn"], [id^="close-"]').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target') || 
                           this.id.replace('-btn', '-full').replace('close-', '').replace('-details', '-result-full');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                if (targetElement.style.display === 'none' || !targetElement.style.display) {
                    targetElement.style.display = 'block';
                    targetElement.classList.add('expanding');
                    setTimeout(() => {
                        targetElement.classList.remove('expanding');
                    }, 500);
                    
                    // Прокрутка к раскрытому блоку
                    setTimeout(() => {
                        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                } else {
                    targetElement.classList.add('collapsing');
                    setTimeout(() => {
                        targetElement.style.display = 'none';
                        targetElement.classList.remove('collapsing');
                    }, 300);
                }
            }
        });
    });
    
    // Магические эффекты при загрузке страницы
    setTimeout(() => {
        document.body.classList.add('loaded');
        createEntranceAnimation();
    }, 100);
    
    // Случайные вспышки звёзд на фоне
    setInterval(createRandomStarFlash, 3000);
});

/* ===========================================
   МИСТИЧЕСКИЕ ЭФФЕКТЫ И АНИМАЦИИ
=========================================== */

// Создаём плавающие частицы энергии
function initFloatingParticles() {
    const container = document.querySelector('.space-background');
    if (!container) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'energy-particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 3 + 1}px;
            height: ${Math.random() * 3 + 1}px;
            background: ${Math.random() > 0.5 ? '#FFD700' : '#9D00FF'};
            border-radius: 50%;
            opacity: ${Math.random() * 0.5 + 0.2};
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            filter: blur(1px);
            animation: float-particle ${Math.random() * 20 + 10}s linear infinite;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float-particle {
                0% {
                    transform: translate(0, 0) rotate(0deg);
                    opacity: ${Math.random() * 0.3 + 0.1};
                }
                25% {
                    transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(90deg);
                }
                50% {
                    opacity: ${Math.random() * 0.7 + 0.3};
                }
                75% {
                    transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(180deg);
                }
                100% {
                    transform: translate(0, 0) rotate(360deg);
                    opacity: ${Math.random() * 0.3 + 0.1};
                }
            }
        `;
        document.head.appendChild(style);
        container.appendChild(particle);
    }
}

// Создаём эффект ряби при клике
function createRippleEffect(element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event ? event.clientX - rect.left - size / 2 : rect.width / 2 - size / 2;
    const y = event ? event.clientY - rect.top - size / 2 : rect.height / 2 - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(157, 0, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        width: ${size}px;
        height: ${size}px;
        top: ${y}px;
        left: ${x}px;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
    
    // Добавляем стиль для анимации, если его ещё нет
    if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Анимируем появление числа
function animateNumber(element) {
    const numberSpan = element.querySelector('span');
    if (!numberSpan) return;
    
    const finalNumber = parseInt(numberSpan.textContent);
    numberSpan.textContent = '0';
    
    let current = 0;
    const increment = finalNumber / 20;
    const timer = setInterval(() => {
        current += increment;
        if (current >= finalNumber) {
            numberSpan.textContent = finalNumber;
            clearInterval(timer);
            
            // Эффект при завершении
            element.style.animation = 'none';
            setTimeout(() => {
                element.style.animation = 'number-pulse 2s ease-in-out infinite';
            }, 10);
        } else {
            numberSpan.textContent = Math.floor(current);
        }
    }, 50);
}

// Эффект искр для кнопок
function createButtonSparkle(button) {
    for (let i = 0; i < 5; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'button-sparkle';
        sparkle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: ${Math.random() > 0.5 ? '#FFD700' : '#00D4FF'};
            border-radius: 50%;
            opacity: 0.8;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            pointer-events: none;
            animation: sparkle-fly ${Math.random() * 0.5 + 0.3}s ease-out forwards;
        `;
        
        button.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 500);
    }
    
    // Добавляем стиль для анимации, если его ещё нет
    if (!document.getElementById('sparkle-style')) {
        const style = document.createElement('style');
        style.id = 'sparkle-style';
        style.textContent = `
            @keyframes sparkle-fly {
                0% {
                    transform: translate(0, 0) scale(1);
                    opacity: 0.8;
                }
                100% {
                    transform: translate(${Math.random() * 40 - 20}px, ${Math.random() * 40 - 20}px) scale(0);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Эффект при входе на страницу
function createEntranceAnimation() {
    const elements = document.querySelectorAll('.calculator-section, .nav-card, .main-header');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

// Случайные вспышки звёзд
function createRandomStarFlash() {
    const container = document.querySelector('.space-background');
    if (!container) return;
    
    const flash = document.createElement('div');
    flash.style.cssText = `
        position: absolute;
        width: ${Math.random() * 5 + 2}px;
        height: ${Math.random() * 5 + 2}px;
        background: #FFFFFF;
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        filter: blur(1px);
        animation: star-flash ${Math.random() * 0.5 + 0.2}s ease-in-out;
        box-shadow: 0 0 ${Math.random() * 10 + 5}px #FFFFFF;
    `;
    
    container.appendChild(flash);
    setTimeout(() => flash.remove(), 500);
    
    if (!document.getElementById('star-flash-style')) {
        const style = document.createElement('style');
        style.id = 'star-flash-style';
        style.textContent = `
            @keyframes star-flash {
                0% { opacity: 0; transform: scale(0.1); }
                50% { opacity: 1; transform: scale(1.5); }
                100% { opacity: 0; transform: scale(0.1); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Эффект при заполнении полей
function addInputEffect(input) {
    input.style.boxShadow = '0 0 20px rgba(157, 0, 255, 0.5)';
    setTimeout(() => {
        input.style.boxShadow = '';
        input.style.transition = 'box-shadow 0.5s ease';
    }, 1000);
}

// Проверка валидности форм перед отправкой
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.classList.contains('needs-validation')) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            
            // Добавляем эффект ошибки
            form.classList.add('was-validated');
            const invalidInputs = form.querySelectorAll(':invalid');
            invalidInputs.forEach(input => {
                input.classList.add('invalid-shake');
                setTimeout(() => input.classList.remove('invalid-shake'), 600);
            });
        } else {
            // Эффект успешной отправки
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Расшифровываю...';
                submitButton.disabled = true;
            }
        }
    }
    
    // Добавляем стиль для анимации ошибки
    if (!document.getElementById('shake-style')) {
        const style = document.createElement('style');
        style.id = 'shake-style';
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
            .invalid-shake {
                animation: shake 0.6s ease-in-out;
                border-color: #ff6b6b !important;
            }
        `;
        document.head.appendChild(style);
    }
});

// Динамическое изменение темы (день/ночь)
const themeToggle = document.createElement('button');
themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
themeToggle.className = 'theme-toggle';
themeToggle.title = 'Сменить тему';
themeToggle.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--dark-purple);
    border: 2px solid var(--primary-gold);
    color: var(--primary-gold);
    cursor: pointer;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    transition: all 0.3s;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
`;

themeToggle.addEventListener('click', function() {
    document.body.classList.toggle('light-theme');
    this.innerHTML = document.body.classList.contains('light-theme') 
        ? '<i class="fas fa-sun"></i>' 
        : '<i class="fas fa-moon"></i>';
    
    // Эффект переключения
    this.style.transform = 'scale(1.2) rotate(180deg)';
    setTimeout(() => {
        this.style.transform = 'scale(1) rotate(0deg)';
    }, 300);
});

// Добавляем кнопку смены темы
document.body.appendChild(themeToggle);

// Добавляем стили для светлой темы
const lightThemeStyles = `
    .light-theme {
        --dark-purple: #F5F5F7;
        --deep-blue: #E8E8F0;
        --text-light: #1A1A2E;
        --text-gray: #4A4A6A;
        --glass-bg: rgba(245, 245, 247, 0.9);
        --glass-border: rgba(184, 134, 11, 0.3);
    }
    
    .light-theme .calculator-section::before {
        background: linear-gradient(45deg, 
            #B8860B, 
            #9D00FF, 
            #00D4FF, 
            #B8860B
        );
    }
`;

const styleElement = document.createElement('style');
styleElement.textContent = lightThemeStyles;
document.head.appendChild(styleElement);

// Таймер для показа мистических сообщений
const mysticalMessages = [
    "Цифры — это ключи к пониманию Вселенной...",
    "Каждая дата несёт свою уникальную вибрацию...",
    "Слушайте числа, они говорят с вами...",
    "Ваша судьба записана в числах...",
    "Сегодня — идеальный день для нового начала..."
];

setInterval(() => {
    if (Math.random() > 0.7 && document.visibilityState === 'visible') {
        const message = mysticalMessages[Math.floor(Math.random() * mysticalMessages.length)];
        showFloatingMessage(message);
    }
}, 30000);

function showFloatingMessage(text) {
    const messageEl = document.createElement('div');
    messageEl.className = 'floating-message';
    messageEl.textContent = text;
    messageEl.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 30px;
        background: rgba(15, 21, 37, 0.9);
        color: var(--primary-gold);
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 4px solid var(--primary-gold);
        max-width: 300px;
        z-index: 1000;
        animation: floatMessage 5s ease-in-out forwards;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
    `;
    
    document.body.appendChild(messageEl);
    setTimeout(() => messageEl.remove(), 5000);
    
    if (!document.getElementById('float-message-style')) {
        const style = document.createElement('style');
        style.id = 'float-message-style';
        style.textContent = `
            @keyframes floatMessage {
                0% { transform: translateY(100px); opacity: 0; }
                10% { transform: translateY(0); opacity: 1; }
                90% { transform: translateY(0); opacity: 1; }
                100% { transform: translateY(100px); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}