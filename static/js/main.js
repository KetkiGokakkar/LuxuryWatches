// LuxWatch — Main JavaScript
document.addEventListener('DOMContentLoaded', function() {

    // Mobile menu toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileToggle.classList.toggle('active');
        });
    }

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }
    });

    // Auto-dismiss flash messages
    document.querySelectorAll('.message').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(30px)';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });

    // AJAX add to cart
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = this.action;
            const formData = new FormData(this);
            const btn = this.querySelector('button');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            btn.disabled = true;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    btn.innerHTML = '<i class="fas fa-check"></i> Added!';
                    btn.style.background = '#4ade80';
                    btn.style.color = '#0a0a0a';
                    btn.style.borderColor = '#4ade80';

                    // Update cart badge
                    let badge = document.getElementById('cartBadge');
                    if (badge) {
                        badge.textContent = data.cart_count;
                    } else {
                        const cartIcon = document.querySelector('.cart-icon');
                        if (cartIcon) {
                            badge = document.createElement('span');
                            badge.className = 'cart-badge';
                            badge.id = 'cartBadge';
                            badge.textContent = data.cart_count;
                            cartIcon.appendChild(badge);
                        }
                    }

                    // Show toast notification
                    showToast(data.message || 'Added to cart!');

                    setTimeout(() => {
                        btn.innerHTML = originalHTML;
                        btn.disabled = false;
                        btn.style.background = '';
                        btn.style.color = '';
                        btn.style.borderColor = '';
                    }, 2000);
                }
            })
            .catch(() => {
                btn.innerHTML = originalHTML;
                btn.disabled = false;
                form.submit(); // Fallback to normal form submit
            });
        });
    });

    // Payment option selection
    document.querySelectorAll('.payment-option').forEach(opt => {
        opt.addEventListener('click', function() {
            document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
            this.querySelector('input').checked = true;
        });
    });
});

// Toast notification
function showToast(message) {
    const container = document.querySelector('.messages-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = 'message message-success';
    toast.innerHTML = `<span>${message}</span><button class="message-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(30px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}
