/**
 * ========================================
 * Campus Canteen - Shared Utilities
 * Common functions across all pages
 * ========================================
 */

// Get current page name
function getCurrentPage() {
    const path = window.location.pathname;
    const page = path.split('/').pop().replace('.html', '') || 'index';
    return page === 'index' ? 'home' : page;
}

// Initialize navbar active state
function initNavbar() {
    const currentPage = getCurrentPage();

    // Set active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === currentPage) {
            link.classList.add('active');
        }
    });

    // Scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    });
}

// Toggle mobile menu
function toggleMobileMenu() {
    const menu = document.getElementById('navMenu');
    if (menu) {
        menu.classList.toggle('active');
    }
}

// Update cart badge on all pages
function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
        const count = cartItems.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    }
}

// ========================================
// MODAL FUNCTIONS
// ========================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function switchModal(closeId, openId) {
    closeModal(closeId);
    setTimeout(() => openModal(openId), 200);
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
        document.body.style.overflow = '';
    }
});

// ========================================
// TOAST NOTIFICATIONS
// ========================================

function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = { success: '✓', error: '✕', warning: '⚠' };

    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || '📢'}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    updateCartBadge();
    initAuth(); // from auth.js
});

// Make functions globally available
window.toggleMobileMenu = toggleMobileMenu;
window.openModal = openModal;
window.closeModal = closeModal;
window.switchModal = switchModal;
window.showToast = showToast;
window.updateCartBadge = updateCartBadge;
