/**
 * ========================================
 * Campus Canteen - Shopping Cart Module
 * Handles cart operations and persistence
 * ========================================
 */

// Payment state
let currentOrderData = null;
let paymentScreenshot = null;

class ShoppingCart {
    constructor() {
        this.items = [];
        this.load();
    }

    /**
     * Load cart from localStorage
     */
    load() {
        const saved = localStorage.getItem('canteen_cart');
        if (saved) {
            try {
                this.items = JSON.parse(saved);
            } catch (e) {
                this.items = [];
            }
        }
        this.updateBadge();
    }

    /**
     * Save cart to localStorage
     */
    save() {
        localStorage.setItem('canteen_cart', JSON.stringify(this.items));
        this.updateBadge();
    }

    /**
     * Add item to cart
     */
    addItem(menuItem, quantity = 1) {
        const existingIndex = this.items.findIndex(i => i.item_id === menuItem.item_id);

        if (existingIndex > -1) {
            this.items[existingIndex].quantity += quantity;
        } else {
            this.items.push({
                item_id: menuItem.item_id,
                item_name: menuItem.item_name,
                price: menuItem.price,
                quantity: quantity,
                is_vegetarian: menuItem.is_vegetarian
            });
        }

        this.save();
        showToast(`${menuItem.item_name} added to cart!`, 'success');
    }

    /**
     * Remove item from cart
     */
    removeItem(itemId) {
        this.items = this.items.filter(i => i.item_id !== itemId);
        this.save();
        this.render();
    }

    /**
     * Update item quantity
     */
    updateQuantity(itemId, quantity) {
        const item = this.items.find(i => i.item_id === itemId);
        if (item) {
            if (quantity <= 0) {
                this.removeItem(itemId);
            } else {
                item.quantity = quantity;
                this.save();
                this.render();
            }
        }
    }

    /**
     * Get item quantity in cart
     */
    getQuantity(itemId) {
        const item = this.items.find(i => i.item_id === itemId);
        return item ? item.quantity : 0;
    }

    /**
     * Calculate total
     */
    getTotal() {
        return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }

    /**
     * Get total item count
     */
    getCount() {
        return this.items.reduce((sum, item) => sum + item.quantity, 0);
    }

    /**
     * Clear cart
     */
    clear() {
        this.items = [];
        this.save();
        this.render();
    }

    /**
     * Update cart badge in navbar
     */
    updateBadge() {
        const badge = document.getElementById('cartBadge');
        if (badge) {
            const count = this.getCount();
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-flex' : 'none';
        }
    }

    /**
     * Get food emoji based on item name
     */
    getEmoji(itemName) {
        const name = itemName.toLowerCase();
        if (name.includes('dosa') || name.includes('idli')) return '🥞';
        if (name.includes('biryani')) return '🍛';
        if (name.includes('thali')) return '🍱';
        if (name.includes('samosa')) return '🥟';
        if (name.includes('coffee')) return '☕';
        if (name.includes('tea') || name.includes('chai')) return '🍵';
        if (name.includes('lassi')) return '🥛';
        if (name.includes('soda') || name.includes('lemon')) return '🍋';
        if (name.includes('maggi') || name.includes('noodle')) return '🍜';
        if (name.includes('fries')) return '🍟';
        if (name.includes('paneer')) return '🧀';
        if (name.includes('roti') || name.includes('bread')) return '🫓';
        if (name.includes('chole') || name.includes('bhature')) return '🥘';
        return '🍽️';
    }

    /**
     * Render cart in the cart section
     */
    render() {
        const cartItemsEl = document.getElementById('cartItems');
        const cartSummaryEl = document.getElementById('cartSummary');
        const emptyCartEl = document.getElementById('emptyCart');
        const subtotalEl = document.getElementById('cartSubtotal');
        const totalEl = document.getElementById('cartTotal');

        if (this.items.length === 0) {
            cartItemsEl.style.display = 'none';
            cartSummaryEl.style.display = 'none';
            emptyCartEl.style.display = 'block';
            return;
        }

        cartItemsEl.style.display = 'flex';
        cartSummaryEl.style.display = 'block';
        emptyCartEl.style.display = 'none';

        cartItemsEl.innerHTML = this.items.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">${this.getEmoji(item.item_name)}</div>
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.item_name}</div>
                    <div class="cart-item-price">₹${item.price.toFixed(2)} each</div>
                </div>
                <div class="cart-item-actions">
                    <div class="quantity-control">
                        <button class="quantity-btn" onclick="cart.updateQuantity(${item.item_id}, ${item.quantity - 1})">−</button>
                        <span class="quantity-value">${item.quantity}</span>
                        <button class="quantity-btn" onclick="cart.updateQuantity(${item.item_id}, ${item.quantity + 1})">+</button>
                    </div>
                    <div class="cart-item-subtotal">₹${(item.price * item.quantity).toFixed(2)}</div>
                    <button class="cart-item-remove" onclick="cart.removeItem(${item.item_id})" title="Remove">✕</button>
                </div>
            </div>
        `).join('');

        // Update totals
        updateCartTotal();
    }
}

// Create global cart instance
const cart = new ShoppingCart();

/**
 * Update order options display - Pickup Only
 */
function updateOrderOptions() {
    // Force Pickup options to be visible
    const pickupOptions = document.getElementById('pickupOptions');
    if (pickupOptions) pickupOptions.style.display = 'block';

    // Update total
    updateCartTotal();
}

/**
 * Update cart total
 */
function updateCartTotal() {
    const subtotalEl = document.getElementById('cartSubtotal');
    const totalEl = document.getElementById('cartTotal');

    const subtotal = cart.getTotal();
    const total = subtotal;

    if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `₹${total.toFixed(2)}`;
}

/**
 * Place order function - Creates order and shows payment modal
 */
async function placeOrder() {
    if (!requireLogin()) {
        showToast('Please login to place an order', 'warning');
        return;
    }

    if (cart.items.length === 0) {
        showToast('Your cart is empty!', 'warning');
        return;
    }

    const instructions = document.getElementById('instructionsInput').value;
    const pickupTime = document.getElementById('pickupTimeSelect').value;

    // Build special instructions with pickup time
    let fullInstructions = '';
    if (pickupTime) {
        fullInstructions = `Pickup Time: ${pickupTime}`;
    }
    if (instructions) {
        fullInstructions += fullInstructions ? ` | ${instructions}` : instructions;
    }

    // Prepare order data (Pickup only)
    const orderData = {
        student_id: currentUser.student_id,
        canteen_id: 1,
        order_type: 'PICKUP',
        items: cart.items.map(item => ({
            item_id: item.item_id,
            quantity: item.quantity
        })),
        special_instructions: fullInstructions || null
    };

    try {
        // Disable button and show loading
        const checkoutBtn = document.getElementById('checkoutBtn');
        checkoutBtn.disabled = true;
        checkoutBtn.textContent = 'Processing...';

        const order = await API.Order.create(orderData);

        // Store order data for payment
        currentOrderData = {
            order_id: order.order_id,
            total_amount: order.total_amount
        };

        // Reset button
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = 'Place Order';

        // Show payment modal
        showPaymentModal(order);

    } catch (error) {
        const checkoutBtn = document.getElementById('checkoutBtn');
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = 'Place Order';
        showToast(error.message || 'Failed to place order. Please try again.', 'error');
    }
}

/**
 * Show payment modal with order details
 */
function showPaymentModal(order) {
    // Update payment details
    document.getElementById('paymentAmount').textContent = `₹${order.total_amount.toFixed(2)}`;
    document.getElementById('paymentOrderId').textContent = order.order_id;

    // Update QR code with actual amount
    const upiId = 'SENZA@upi';
    const amount = order.total_amount.toFixed(2);
    const qrData = `upi://pay?pa=${upiId}&pn=SENZA&am=${amount}&cu=INR`;
    document.getElementById('upiQrCode').src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrData)}`;

    // Reset screenshot state
    paymentScreenshot = null;
    document.getElementById('screenshotPreview').style.display = 'none';
    document.getElementById('screenshotInput').value = '';
    document.getElementById('confirmPaymentBtn').disabled = true;

    // Show upload label
    document.querySelector('.upload-label').style.display = 'flex';

    // Open modal
    openModal('paymentModal');
}

/**
 * Copy UPI ID to clipboard
 */
function copyUpiId() {
    const upiId = document.getElementById('upiIdDisplay').textContent;
    navigator.clipboard.writeText(upiId).then(() => {
        showToast('UPI ID copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy UPI ID', 'error');
    });
}

/**
 * Handle screenshot upload
 */
function handleScreenshotUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showToast('Please upload an image file', 'error');
        return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showToast('Image size should be less than 5MB', 'error');
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        paymentScreenshot = e.target.result;

        // Show preview
        document.getElementById('screenshotImage').src = paymentScreenshot;
        document.getElementById('screenshotPreview').style.display = 'block';

        // Hide upload label
        document.querySelector('.upload-label').style.display = 'none';

        // Enable confirm button
        document.getElementById('confirmPaymentBtn').disabled = false;

        showToast('Screenshot uploaded! You can now confirm payment.', 'success');
    };
    reader.readAsDataURL(file);
}

/**
 * Remove uploaded screenshot
 */
function removeScreenshot() {
    paymentScreenshot = null;
    document.getElementById('screenshotPreview').style.display = 'none';
    document.getElementById('screenshotInput').value = '';
    document.getElementById('confirmPaymentBtn').disabled = true;

    // Show upload label
    document.querySelector('.upload-label').style.display = 'flex';
}

/**
 * Confirm payment with screenshot
 */
async function confirmPayment() {
    if (!currentOrderData || !paymentScreenshot) {
        showToast('Please upload payment screenshot first', 'error');
        return;
    }

    const confirmBtn = document.getElementById('confirmPaymentBtn');
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Processing...';

    try {
        // Create payment record with screenshot
        const paymentData = {
            order_id: currentOrderData.order_id,
            amount_paid: currentOrderData.total_amount,
            payment_method: 'UPI',
            payment_screenshot: paymentScreenshot
        };

        await API.Payment.create(paymentData);

        // Close payment modal
        closeModal('paymentModal');

        // Clear cart
        cart.clear();

        // Reset state
        currentOrderData = null;
        paymentScreenshot = null;

        // Show success modal
        document.getElementById('successOrderId').textContent = paymentData.order_id;
        openModal('successModal');

    } catch (error) {
        confirmBtn.disabled = false;
        confirmBtn.textContent = '✓ I Have Paid';
        showToast(error.message || 'Failed to record payment. Please try again.', 'error');
    }
}

/**
 * Cancel payment and order
 */
function cancelPayment() {
    if (confirm('Are you sure you want to cancel this order?')) {
        closeModal('paymentModal');
        currentOrderData = null;
        paymentScreenshot = null;
        showToast('Order cancelled', 'warning');
    }
}

// Initialize order options on page load
document.addEventListener('DOMContentLoaded', () => {
    // Set initial state
    setTimeout(() => {
        updateOrderOptions();
    }, 100);
});
