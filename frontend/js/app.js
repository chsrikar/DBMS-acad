/**
 * ========================================
 * Campus Canteen - Main Application
 * Core app logic and UI interactions
 * ========================================
 */

// Global state
let menuItems = [];
let currentCategory = 'all';
let vegOnly = false;

/**
 * Initialize application
 */
document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    initNavbar();
    initCategoryTabs();
    initVegFilter();
    loadMenuItems();
    cart.render();
});

/**
 * Initialize navbar scroll effect
 */
function initNavbar() {
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu() {
    const menu = document.getElementById('navMenu');
    menu.classList.toggle('active');
}

/**
 * Show a section and hide others
 */
function showSection(sectionName) {
    // Hide mobile menu
    document.getElementById('navMenu').classList.remove('active');

    // Update sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`section-${sectionName}`).classList.add('active');

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.section === sectionName) {
            link.classList.add('active');
        }
    });

    // Load section-specific data
    if (sectionName === 'cart') {
        cart.render();
    } else if (sectionName === 'orders') {
        loadOrders();
    } else if (sectionName === 'profile') {
        loadProfile();
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Initialize category tabs
 */
function initCategoryTabs() {
    document.getElementById('categoryTabs').addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-tab')) {
            document.querySelectorAll('.filter-tab').forEach(tab => tab.classList.remove('active'));
            e.target.classList.add('active');
            currentCategory = e.target.dataset.category;
            renderMenuItems();
        }
    });
}

/**
 * Initialize veg filter
 */
function initVegFilter() {
    document.getElementById('vegOnlyFilter').addEventListener('change', (e) => {
        vegOnly = e.target.checked;
        renderMenuItems();
    });
}

/**
 * Load menu items from API
 */
async function loadMenuItems() {
    const menuGrid = document.getElementById('menuGrid');

    try {
        menuItems = await API.Menu.getAll();
        renderMenuItems();
    } catch (error) {
        menuGrid.innerHTML = `
            <div class="loading-spinner">
                <div class="empty-icon">❌</div>
                <p>Failed to load menu. Please try again.</p>
                <button class="btn btn-primary" onclick="loadMenuItems()">Retry</button>
            </div>
        `;
    }
}

/**
 * Get food emoji based on category/name
 */
function getFoodEmoji(item) {
    const name = item.item_name.toLowerCase();
    const category = (item.category || '').toLowerCase();

    if (name.includes('dosa')) return '🥞';
    if (name.includes('idli')) return '🍚';
    if (name.includes('poha') || name.includes('upma')) return '🍛';
    if (name.includes('biryani')) return '🍛';
    if (name.includes('thali')) return '🍱';
    if (name.includes('samosa')) return '🥟';
    if (name.includes('vada pav')) return '🍔';
    if (name.includes('fries')) return '🍟';
    if (name.includes('maggi')) return '🍜';
    if (name.includes('paneer')) return '🧀';
    if (name.includes('chole') || name.includes('bhature')) return '🥘';
    if (name.includes('coffee')) return '☕';
    if (name.includes('tea') || name.includes('chai')) return '🍵';
    if (name.includes('cold coffee')) return '🧊';
    if (name.includes('lassi')) return '🥛';
    if (name.includes('soda') || name.includes('lemon')) return '🍋';

    if (category === 'breakfast') return '🌅';
    if (category === 'lunch') return '🍽️';
    if (category === 'snacks') return '🍿';
    if (category === 'beverages') return '🥤';

    return '🍴';
}

/**
 * Render menu items based on filters
 */
function renderMenuItems() {
    const menuGrid = document.getElementById('menuGrid');

    let filtered = menuItems;

    // Category filter
    if (currentCategory !== 'all') {
        filtered = filtered.filter(item => item.category === currentCategory);
    }

    // Veg filter
    if (vegOnly) {
        filtered = filtered.filter(item => item.is_vegetarian);
    }

    if (filtered.length === 0) {
        menuGrid.innerHTML = `
            <div class="loading-spinner" style="grid-column: 1/-1;">
                <div class="empty-icon">🍽️</div>
                <p>No items found matching your filters</p>
            </div>
        `;
        return;
    }

    menuGrid.innerHTML = filtered.map(item => {
        const qty = cart.getQuantity(item.item_id);
        const emoji = getFoodEmoji(item);

        return `
            <div class="menu-item ${!item.is_available ? 'unavailable' : ''}">
                <div class="menu-item-image">${emoji}</div>
                <div class="menu-item-content">
                    <div class="menu-item-header">
                        <h3 class="menu-item-name">${item.item_name}</h3>
                        <div class="menu-item-badges">
                            ${item.is_vegetarian
                ? '<span class="badge badge-veg">Veg</span>'
                : '<span class="badge badge-nonveg">Non-Veg</span>'}
                            ${!item.is_available ? '<span class="badge badge-unavailable">Unavailable</span>' : ''}
                        </div>
                    </div>
                    <p class="menu-item-description">${item.description || 'Delicious food item'}</p>
                    <div class="menu-item-footer">
                        <span class="menu-item-price">₹${item.price.toFixed(2)}</span>
                        <div class="menu-item-actions">
                            ${item.is_available ? (qty > 0 ? `
                                <div class="quantity-control">
                                    <button class="quantity-btn" onclick="updateMenuItemQty(${item.item_id}, ${qty - 1})">−</button>
                                    <span class="quantity-value">${qty}</span>
                                    <button class="quantity-btn" onclick="updateMenuItemQty(${item.item_id}, ${qty + 1})">+</button>
                                </div>
                            ` : `
                                <button class="btn btn-primary btn-sm" onclick="addToCart(${item.item_id})">Add to Cart</button>
                            `) : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Add item to cart from menu
 */
function addToCart(itemId) {
    const item = menuItems.find(i => i.item_id === itemId);
    if (item) {
        cart.addItem(item);
        renderMenuItems();
    }
}

/**
 * Update menu item quantity
 */
function updateMenuItemQty(itemId, qty) {
    cart.updateQuantity(itemId, qty);
    renderMenuItems();
}

/**
 * Load user orders
 */
async function loadOrders() {
    const ordersContainer = document.getElementById('ordersContainer');
    const noOrders = document.getElementById('noOrders');

    if (!isLoggedIn()) {
        ordersContainer.innerHTML = `
            <div class="loading-spinner">
                <div class="empty-icon">🔐</div>
                <h3>Please login to view your orders</h3>
                <button class="btn btn-primary" onclick="openModal('loginModal')">Login</button>
            </div>
        `;
        noOrders.style.display = 'none';
        return;
    }

    ordersContainer.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading your orders...</p>
        </div>
    `;
    noOrders.style.display = 'none';

    try {
        const history = await API.Student.getOrders(currentUser.student_id);

        if (!history.orders || history.orders.length === 0) {
            ordersContainer.innerHTML = '';
            noOrders.style.display = 'block';
            return;
        }

        ordersContainer.innerHTML = history.orders.map(order => {
            const statusClass = `status-${order.order_status.toLowerCase()}`;
            const orderDate = new Date(order.order_date).toLocaleString();

            // Payment status badge
            let paymentBadge = '';
            let orderMessage = '';

            if (order.payment) {
                const paymentStatus = order.payment.payment_status;
                if (paymentStatus === 'COMPLETED') {
                    paymentBadge = '<span class="payment-badge payment-accepted">💳 Payment Accepted</span>';
                } else if (paymentStatus === 'FAILED') {
                    paymentBadge = '<span class="payment-badge payment-rejected">❌ Payment Rejected</span>';
                    orderMessage = '<div class="order-message order-message-error">Your payment was rejected and the order has been cancelled.</div>';
                } else if (paymentStatus === 'PENDING') {
                    paymentBadge = '<span class="payment-badge payment-pending">⏳ Payment Pending</span>';
                    orderMessage = '<div class="order-message order-message-warning">Waiting for admin to verify your payment...</div>';
                }
            } else {
                paymentBadge = '<span class="payment-badge payment-pending">⏳ No Payment</span>';
            }

            // Order status message
            if (order.order_status === 'PREPARING') {
                orderMessage = '<div class="order-message order-message-info">🍳 Your order is being prepared!</div>';
            } else if (order.order_status === 'READY') {
                orderMessage = '<div class="order-message order-message-success">✅ Your order is ready for pickup!</div>';
            } else if (order.order_status === 'DELIVERED') {
                orderMessage = '<div class="order-message order-message-success">📦 Order completed!</div>';
            } else if (order.order_status === 'CANCELLED') {
                orderMessage = '<div class="order-message order-message-error">❌ Order cancelled</div>';
            }

            return `
                <div class="order-card ${order.order_status === 'CANCELLED' ? 'order-cancelled' : ''}">
                    <div class="order-header">
                        <div>
                            <span class="order-id">Order #${order.order_id}</span>
                            <span class="order-date">${orderDate}</span>
                        </div>
                        <span class="order-status ${statusClass}">${order.order_status}</span>
                    </div>
                    <div class="order-body">
                        ${orderMessage}
                        <div class="order-total">
                            <span>Total Amount</span>
                            <span>₹${order.total_amount.toFixed(2)}</span>
                        </div>
                        <div class="order-meta">
                            <span>📦 ${order.order_type}</span>
                            ${paymentBadge}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        ordersContainer.innerHTML = `
            <div class="loading-spinner">
                <div class="empty-icon">❌</div>
                <p>Failed to load orders</p>
                <button class="btn btn-primary" onclick="loadOrders()">Retry</button>
            </div>
        `;
    }
}

/**
 * Load user profile
 */
async function loadProfile() {
    const profileContainer = document.getElementById('profileContainer');
    const loginPrompt = document.getElementById('profileLoginPrompt');

    if (!isLoggedIn()) {
        profileContainer.style.display = 'none';
        loginPrompt.style.display = 'block';
        return;
    }

    profileContainer.style.display = 'block';
    loginPrompt.style.display = 'none';

    const user = getCurrentUser();
    const initials = user.name.split(' ').map(n => n[0]).join('').toUpperCase();

    // Get order stats
    let orderStats = { total: 0, totalSpent: 0 };
    try {
        const history = await API.Student.getOrders(user.student_id);
        if (history.orders) {
            orderStats.total = history.orders.length;
            orderStats.totalSpent = history.orders.reduce((sum, o) => sum + (o.total_amount || 0), 0);
        }
    } catch (e) {
        console.error('Failed to load order stats:', e);
    }

    profileContainer.innerHTML = `
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-avatar">${initials}</div>
                <h2 class="profile-name">${user.name}</h2>
                <p class="profile-email">${user.email}</p>
            </div>
            <div class="profile-body">
                <div class="profile-section">
                    <h3 class="profile-section-title">Personal Information</h3>
                    <div class="profile-info-grid">
                        <div class="profile-info-item">
                            <div class="profile-info-label">Roll Number</div>
                            <div class="profile-info-value">🎓 ${user.roll_number}</div>
                        </div>
                        <div class="profile-info-item">
                            <div class="profile-info-label">Phone</div>
                            <div class="profile-info-value">📱 ${user.phone || 'Not provided'}</div>
                        </div>
                        <div class="profile-info-item">
                            <div class="profile-info-label">Hostel</div>
                            <div class="profile-info-value">🏠 ${user.hostel?.hostel_name || 'Not assigned'}</div>
                        </div>
                        <div class="profile-info-item">
                            <div class="profile-info-label">Department</div>
                            <div class="profile-info-value">📚 ${user.department?.department_name || 'Not assigned'}</div>
                        </div>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h3 class="profile-section-title">Order Statistics</h3>
                    <div class="profile-stats">
                        <div class="profile-stat">
                            <div class="profile-stat-value">${orderStats.total}</div>
                            <div class="profile-stat-label">Total Orders</div>
                        </div>
                        <div class="profile-stat">
                            <div class="profile-stat-value">₹${orderStats.totalSpent.toFixed(0)}</div>
                            <div class="profile-stat-label">Total Spent</div>
                        </div>
                        <div class="profile-stat">
                            <div class="profile-stat-value">⭐</div>
                            <div class="profile-stat-label">Loyal Customer</div>
                        </div>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h3 class="profile-section-title">Account</h3>
                    <div class="profile-info-grid">
                        <div class="profile-info-item">
                            <div class="profile-info-label">Member Since</div>
                            <div class="profile-info-value">📅 ${new Date(user.created_at).toLocaleDateString()}</div>
                        </div>
                        <div class="profile-info-item">
                            <div class="profile-info-label">Account Status</div>
                            <div class="profile-info-value">✅ Active</div>
                        </div>
                    </div>
                </div>
                
                <div class="profile-actions">
                    <button class="btn btn-outline" onclick="showSection('orders')">📋 View Orders</button>
                    <button class="btn btn-secondary" onclick="logout()">🚪 Logout</button>
                </div>
            </div>
        </div>
    `;
}

// ========================================
// MODAL FUNCTIONS
// ========================================

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    document.body.style.overflow = '';
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
