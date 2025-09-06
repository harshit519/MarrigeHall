// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 1000,
    easing: 'ease-in-out',
    once: true,
    mirror: false
});

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('mainNav');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
    }
});

// Back to top button
const backToTopBtn = document.getElementById('backToTop');

window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTopBtn.style.display = 'block';
    } else {
        backToTopBtn.style.display = 'none';
    }
});

backToTopBtn.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Contact form enhancement
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading"></span> Sending...';
            submitBtn.disabled = true;
            
            // Simulate form submission (replace with actual AJAX call)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Show success message
                showNotification('Message sent successfully!', 'success');
                
                // Reset form
                this.reset();
            }, 2000);
        });
    }
    
    // Booking form enhancement
    const bookingForm = document.querySelector('.booking-form');
    if (bookingForm) {
        const dateInput = bookingForm.querySelector('input[type="date"]');
        if (dateInput) {
            // Set minimum date to today
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;
            
            // Update pricing based on date and venue
            dateInput.addEventListener('change', updatePricing);
        }
        
        const venueSelect = bookingForm.querySelector('select[name="venue"]');
        if (venueSelect) {
            venueSelect.addEventListener('change', updatePricing);
        }
    }
    
    // Restaurant menu enhancement
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        const addToCartBtn = item.querySelector('.add-to-cart');
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', function() {
                const itemName = this.closest('.menu-item').querySelector('.item-name').textContent;
                addToCart(itemName);
            });
        }
    });
});

// Update pricing function
function updatePricing() {
    const dateInput = document.querySelector('input[type="date"]');
    const venueSelect = document.querySelector('select[name="venue"]');
    const guestInput = document.querySelector('input[name="guests"]');
    const priceDisplay = document.querySelector('.price-display');
    
    if (dateInput && venueSelect && guestInput && priceDisplay) {
        const selectedDate = new Date(dateInput.value);
        const selectedVenue = venueSelect.value;
        const guestCount = parseInt(guestInput.value) || 0;
        
        // Base prices (you can make this dynamic from backend)
        const basePrices = {
            'hall': 50000,
            'lawn': 35000,
            'restaurant': 25000
        };
        
        let basePrice = basePrices[selectedVenue] || 0;
        
        // Weekend premium (Friday, Saturday, Sunday)
        const dayOfWeek = selectedDate.getDay();
        if (dayOfWeek === 5 || dayOfWeek === 6 || dayOfWeek === 0) {
            basePrice *= 1.2; // 20% premium
        }
        
        // Guest count adjustment
        const totalPrice = basePrice + (guestCount * 500);
        
        priceDisplay.innerHTML = `
            <div class="alert alert-info">
                <strong>Estimated Total:</strong> ₹${totalPrice.toLocaleString()}
                <br><small>Base: ₹${basePrice.toLocaleString()} + ₹500 per guest</small>
            </div>
        `;
    }
}

// Add to cart function
function addToCart(itemName) {
    // Get existing cart from localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Add item to cart
    const existingItem = cart.find(item => item.name === itemName);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            name: itemName,
            quantity: 1,
            price: 0 // You can add actual price here
        });
    }
    
    // Save cart
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Show notification
    showNotification(`${itemName} added to cart!`, 'success');
    
    // Update cart count
    updateCartCount();
}

// Update cart count
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        cartBadge.textContent = totalItems;
        cartBadge.style.display = totalItems > 0 ? 'inline' : 'none';
    }
}

// Show notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Gallery lightbox functionality
document.addEventListener('DOMContentLoaded', function() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                openLightbox(img.src, img.alt);
            }
        });
    });
});

// Lightbox function
function openLightbox(src, alt) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        cursor: pointer;
    `;
    
    lightbox.innerHTML = `
        <img src="${src}" alt="${alt}" style="max-width: 90%; max-height: 90%; object-fit: contain;">
        <button class="btn btn-light position-absolute top-0 end-0 m-3" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    lightbox.addEventListener('click', function(e) {
        if (e.target === this) {
            this.remove();
        }
    });
    
    document.body.appendChild(lightbox);
}

// Testimonial slider
function initTestimonialSlider() {
    const testimonials = document.querySelectorAll('.testimonial-card');
    let currentIndex = 0;
    
    function showTestimonial(index) {
        testimonials.forEach((testimonial, i) => {
            testimonial.style.display = i === index ? 'block' : 'none';
        });
    }
    
    function nextTestimonial() {
        currentIndex = (currentIndex + 1) % testimonials.length;
        showTestimonial(currentIndex);
    }
    
    // Auto-rotate testimonials
    if (testimonials.length > 1) {
        setInterval(nextTestimonial, 5000);
    }
}

// Initialize testimonial slider when page loads
document.addEventListener('DOMContentLoaded', initTestimonialSlider);

// Parallax effect for hero section
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero-section');
    
    if (parallax) {
        const speed = scrolled * 0.5;
        parallax.style.transform = `translateY(${speed}px)`;
    }
});

// Mobile menu enhancement
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }
});

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Simulate search results (replace with actual AJAX call)
            const results = [
                'Wedding Package',
                'Birthday Celebration',
                'Corporate Event',
                'Restaurant Menu'
            ].filter(item => item.toLowerCase().includes(query));
            
            if (results.length > 0) {
                searchResults.innerHTML = results.map(result => 
                    `<div class="search-result-item p-2 border-bottom">${result}</div>`
                ).join('');
                searchResults.style.display = 'block';
            } else {
                searchResults.innerHTML = '<div class="p-2 text-muted">No results found</div>';
                searchResults.style.display = 'block';
            }
        });
        
        // Hide search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
}

// Initialize search when page loads
document.addEventListener('DOMContentLoaded', initSearch);

// WhatsApp integration
function openWhatsApp(message = '') {
    const phone = '+919876543210'; // Replace with actual phone number
    const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
}

// Add WhatsApp button functionality
document.addEventListener('DOMContentLoaded', function() {
    const whatsappButtons = document.querySelectorAll('.whatsapp-btn');
    whatsappButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const message = this.dataset.message || 'Hello! I would like to know more about your services.';
            openWhatsApp(message);
        });
    });
});

// Initialize cart count on page load
document.addEventListener('DOMContentLoaded', updateCartCount);

// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.setAttribute('data-theme', savedTheme);
        updateDarkModeIcon(savedTheme === 'dark');
    }
    
    darkModeToggle.addEventListener('click', function() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateDarkModeIcon(newTheme === 'dark');
    });
    
    function updateDarkModeIcon(isDark) {
        const icon = darkModeToggle.querySelector('i');
        if (isDark) {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
});

// Hero Slider Initialization
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.hero-swiper')) {
        const heroSwiper = new Swiper('.hero-swiper', {
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            }
        });
    }
});

// Testimonials Slider
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.testimonials-swiper')) {
        const testimonialsSwiper = new Swiper('.testimonials-swiper', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                },
            },
        });
    }
});

// Gallery Filter Functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.gallery-filters .btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            galleryItems.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-category') === filter) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease-in';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});

// Countdown Timer
function initCountdownTimer() {
    const endDate = new Date('2024-12-31').getTime();
    
    function updateTimer() {
        const now = new Date().getTime();
        const distance = endDate - now;
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        const daysElement = document.getElementById('days');
        const hoursElement = document.getElementById('hours');
        const minutesElement = document.getElementById('minutes');
        const secondsElement = document.getElementById('seconds');
        
        if (daysElement) daysElement.textContent = days.toString().padStart(2, '0');
        if (hoursElement) hoursElement.textContent = hours.toString().padStart(2, '0');
        if (minutesElement) minutesElement.textContent = minutes.toString().padStart(2, '0');
        if (secondsElement) secondsElement.textContent = seconds.toString().padStart(2, '0');
    }
    
    updateTimer();
    setInterval(updateTimer, 1000);
}

// Initialize countdown timer
document.addEventListener('DOMContentLoaded', initCountdownTimer);

// Virtual Tour Functionality
window.openVirtualTour = function(venue) {
    const tourUrls = {
        'hall': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.2219901290355!2d-74.00369368400567!3d40.71312937933185!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a23e28c1191%3A0x49f75d3281df052a!2s150%20Park%20Row%2C%20New%20York%2C%20NY%2010007%2C%20USA!5e0!3m2!1sen!2sin!4v1640995200000!5m2!1sen!2sin',
        'lawn': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.2219901290355!2d-74.00369368400567!3d40.71312937933185!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a23e28c1191%3A0x49f75d3281df052a!2s150%20Park%20Row%2C%20New%20York%2C%20NY%2010007%2C%20USA!5e0!3m2!1sen!2sin!4v1640995200000!5m2!1sen!2sin',
        'restaurant': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.2219901290355!2d-74.00369368400567!3d40.71312937933185!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a23e28c1191%3A0x49f75d3281df052a!2s150%20Park%20Row%2C%20New%20York%2C%20NY%2010007%2C%20USA!5e0!3m2!1sen!2sin!4v1640995200000!5m2!1sen!2sin'
    };
    
    const modal = new bootstrap.Modal(document.getElementById('virtualTourModal'));
    const iframe = document.getElementById('virtualTourFrame');
    if (iframe) {
        iframe.src = tourUrls[venue];
    }
    modal.show();
};

// Live Chat Functionality
document.addEventListener('DOMContentLoaded', function() {
    const openChatBtn = document.getElementById('openChat');
    const closeChatBtn = document.getElementById('closeChat');
    const chatWidget = document.getElementById('liveChatWidget');
    const sendMessageBtn = document.getElementById('sendMessage');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    
    if (openChatBtn && closeChatBtn && chatWidget) {
        openChatBtn.addEventListener('click', function() {
            chatWidget.style.display = 'block';
            this.style.display = 'none';
        });
        
        closeChatBtn.addEventListener('click', function() {
            chatWidget.style.display = 'none';
            openChatBtn.style.display = 'block';
        });
    }
    
    if (sendMessageBtn && chatInput && chatMessages) {
        sendMessageBtn.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
    
    function sendChatMessage() {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message
            chatMessages.innerHTML += `
                <div class="message sent text-end mb-2">
                    <p class="bg-primary text-white p-2 rounded d-inline-block">${message}</p>
                    <small class="text-muted">Just now</small>
                </div>
            `;
            chatInput.value = '';
            
            // Auto reply
            setTimeout(() => {
                chatMessages.innerHTML += `
                    <div class="message received mb-2">
                        <p class="bg-light p-2 rounded d-inline-block">Thank you for your message! We'll get back to you soon.</p>
                        <small class="text-muted">Just now</small>
                    </div>
                `;
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
});

// Enhanced Form Validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill all required fields', 'warning');
            }
        });
    });
});

// Smooth Scrolling for Anchor Links
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add fadeIn animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);
