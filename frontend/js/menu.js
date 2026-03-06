/**
 * ========================================
 * Campus Canteen - Menu Page
 * Menu browsing and cart functionality
 * ========================================
 */

// Global state
let menuItems = [];
let currentCategory = 'all';
let vegOnly = false;

/**
 * Initialize menu page
 */
document.addEventListener('DOMContentLoaded', () => {
    initCategoryTabs();
    initVegFilter();
    loadMenuItems();
});

/**
 * Initialize category tabs
 */
function initCategoryTabs() {
    const tabs = document.getElementById('categoryTabs');
    if (tabs) {
        tabs.addEventListener('click', (e) => {
            if (e.target.classList.contains('filter-tab')) {
                document.querySelectorAll('.filter-tab').forEach(tab => tab.classList.remove('active'));
                e.target.classList.add('active');
                currentCategory = e.target.dataset.category;
                renderMenuItems();
            }
        });
    }
}

/**
 * Initialize veg filter
 */
function initVegFilter() {
    const filter = document.getElementById('vegOnlyFilter');
    if (filter) {
        filter.addEventListener('change', (e) => {
            vegOnly = e.target.checked;
            renderMenuItems();
        });
    }
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
 * Get cart from localStorage
 */
function getCart() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
}

/**
 * Save cart to localStorage
 */
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
}

/**
 * Get quantity of an item in cart
 */
function getCartQuantity(itemId) {
    const cart = getCart();
    const item = cart.find(i => i.item_id === itemId);
    return item ? item.quantity : 0;
}

/**
 * Add item to cart
 */
function addToCart(itemId) {
    const item = menuItems.find(i => i.item_id === itemId);
    if (!item) return;

    const cart = getCart();
    const existingItem = cart.find(i => i.item_id === itemId);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            item_id: item.item_id,
            item_name: item.item_name,
            price: item.price,
            quantity: 1,
            is_vegetarian: item.is_vegetarian
        });
    }

    saveCart(cart);
    renderMenuItems();
    showToast(`${item.item_name} added to cart!`, 'success');
}

/**
 * Update item quantity in cart
 */
function updateMenuItemQty(itemId, qty) {
    const cart = getCart();
    const itemIndex = cart.findIndex(i => i.item_id === itemId);

    if (itemIndex > -1) {
        if (qty <= 0) {
            cart.splice(itemIndex, 1);
        } else {
            cart[itemIndex].quantity = qty;
        }
        saveCart(cart);
        renderMenuItems();
    }
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
        const qty = getCartQuantity(item.item_id);
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

// Make functions globally available
window.addToCart = addToCart;
window.updateMenuItemQty = updateMenuItemQty;
window.loadMenuItems = loadMenuItems;
