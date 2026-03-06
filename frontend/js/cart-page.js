/**
 * ========================================
 * Campus Canteen - Cart Page
 * Shopping cart and checkout functionality
 * ========================================
 */

// Store order data for payment
let currentOrderData = null;
let paymentScreenshot = null;

/**
 * Initialize cart page
 */
document.addEventListener('DOMContentLoaded', () => {
    renderCart();
});

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
 * Get food emoji based on item name
 */
function getItemEmoji(itemName) {
    const name = itemName.toLowerCase();
    if (name.includes('dosa')) return '🥞';
    if (name.includes('idli')) return '🍚';
    if (name.includes('biryani')) return '🍛';
    if (name.includes('cold coffee')) return '🧊';
    if (name.includes('coffee')) return '☕';
    if (name.includes('tea') || name.includes('chai')) return '🍵';
    if (name.includes('lassi')) return '🥛';
    if (name.includes('samosa')) return '🥟';
    if (name.includes('maggi')) return '🍜';
    return '🍴';
}

/**
 * Render cart items
 */
function renderCart() {
    const cart = getCart();
    const cartItems = document.getElementById('cartItems');
    const cartContainer = document.getElementById('cartContainer');
    const emptyCart = document.getElementById('emptyCart');
    const cartSummary = document.getElementById('cartSummary');

    if (cart.length === 0) {
        if (cartContainer) cartContainer.style.display = 'none';
        if (emptyCart) emptyCart.style.display = 'block';
        return;
    }

    if (cartContainer) cartContainer.style.display = 'grid';
    if (emptyCart) emptyCart.style.display = 'none';

    // Render cart items
    if (cartItems) {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">${getItemEmoji(item.item_name)}</div>
                <div class="cart-item-details">
                    <h4 class="cart-item-name">${item.item_name}</h4>
                    <p class="cart-item-price">₹${item.price.toFixed(2)} each</p>
                    ${item.is_vegetarian ? '<span class="badge badge-veg">Veg</span>' : '<span class="badge badge-nonveg">Non-Veg</span>'}
                </div>
                <div class="cart-item-quantity">
                    <button class="quantity-btn" onclick="updateQuantity(${item.item_id}, ${item.quantity - 1})">−</button>
                    <span class="quantity-value">${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${item.item_id}, ${item.quantity + 1})">+</button>
                </div>
                <div class="cart-item-subtotal">
                    ₹${(item.price * item.quantity).toFixed(2)}
                </div>
                <button class="cart-item-remove" onclick="removeFromCart(${item.item_id})">✕</button>
            </div>
        `).join('');
    }

    // Update totals
    updateTotals();
}

/**
 * Update cart totals
 */
function updateTotals() {
    const cart = getCart();
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const total = subtotal;

    const subtotalEl = document.getElementById('cartSubtotal');
    const totalEl = document.getElementById('cartTotal');

    if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `₹${total.toFixed(2)}`;
}

/**
 * Update item quantity
 */
function updateQuantity(itemId, newQty) {
    const cart = getCart();
    const itemIndex = cart.findIndex(item => item.item_id === itemId);

    if (itemIndex > -1) {
        if (newQty <= 0) {
            cart.splice(itemIndex, 1);
        } else {
            cart[itemIndex].quantity = newQty;
        }
        saveCart(cart);
        renderCart();
    }
}

/**
 * Remove item from cart
 */
function removeFromCart(itemId) {
    const cart = getCart();
    const newCart = cart.filter(item => item.item_id !== itemId);
    saveCart(newCart);
    renderCart();
    showToast('Item removed from cart', 'success');
}

/**
 * Clear entire cart
 */
function clearCart() {
    localStorage.removeItem('cart');
    updateCartBadge();
    renderCart();
}

/**
 * Place order function
 */
async function placeOrder() {
    // Check if user is logged in
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    if (!user) {
        showToast('Please login to place an order', 'error');
        openModal('loginModal');
        return;
    }

    const cart = getCart();
    if (cart.length === 0) {
        showToast('Your cart is empty', 'error');
        return;
    }

    const checkoutBtn = document.getElementById('checkoutBtn');
    if (checkoutBtn) {
        checkoutBtn.disabled = true;
        checkoutBtn.innerHTML = '<span class="spinner"></span> Placing Order...';
    }

    try {
        // Build order data
        const orderData = {
            student_id: user.student_id,
            canteen_id: 1,
            order_type: 'PICKUP',
            items: cart.map(item => ({
                item_id: item.item_id,
                quantity: item.quantity,
                notes: null
            })),
            special_instructions: document.getElementById('instructionsInput')?.value || null
        };

        // Create order
        const order = await API.Order.create(orderData);

        // Store order data for payment
        currentOrderData = order;

        // Show payment modal
        showPaymentModal(order);

    } catch (error) {
        showToast(error.message || 'Failed to place order. Please try again.', 'error');
    } finally {
        if (checkoutBtn) {
            checkoutBtn.disabled = false;
            checkoutBtn.innerHTML = 'Place Order';
        }
    }
}

/**
 * Show payment modal with order details
 */
function showPaymentModal(order) {
    // Update payment details
    const amountEl = document.getElementById('paymentAmount');
    const orderIdEl = document.getElementById('paymentOrderId');
    const qrCodeEl = document.getElementById('upiQrCode');

    if (amountEl) amountEl.textContent = `₹${order.total_amount.toFixed(2)}`;
    if (orderIdEl) orderIdEl.textContent = order.order_id;

    // Generate QR code with amount
    if (qrCodeEl) {
        const upiUrl = `upi://pay?pa=SENZA@upi&pn=SENZA&am=${order.total_amount.toFixed(2)}&cu=INR`;
        qrCodeEl.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(upiUrl)}`;
    }

    // Reset screenshot
    paymentScreenshot = null;
    const previewEl = document.getElementById('screenshotPreview');
    const confirmBtn = document.getElementById('confirmPaymentBtn');
    if (previewEl) previewEl.style.display = 'none';
    if (confirmBtn) confirmBtn.disabled = true;

    openModal('paymentModal');
}

/**
 * Copy UPI ID to clipboard
 */
function copyUpiId() {
    const upiId = document.getElementById('upiIdDisplay')?.textContent || 'SENZA@upi';
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
    reader.onload = (e) => {
        paymentScreenshot = e.target.result;

        const imageEl = document.getElementById('screenshotImage');
        const previewEl = document.getElementById('screenshotPreview');
        const confirmBtn = document.getElementById('confirmPaymentBtn');

        if (imageEl) imageEl.src = paymentScreenshot;
        if (previewEl) previewEl.style.display = 'block';
        if (confirmBtn) confirmBtn.disabled = false;

        showToast('Screenshot uploaded! You can now confirm payment.', 'success');
    };
    reader.readAsDataURL(file);
}

/**
 * Remove uploaded screenshot
 */
function removeScreenshot() {
    paymentScreenshot = null;
    const previewEl = document.getElementById('screenshotPreview');
    const confirmBtn = document.getElementById('confirmPaymentBtn');
    const inputEl = document.getElementById('screenshotInput');

    if (previewEl) previewEl.style.display = 'none';
    if (confirmBtn) confirmBtn.disabled = true;
    if (inputEl) inputEl.value = '';
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
    if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = '<span class="spinner"></span> Processing...';
    }

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
        clearCart();

        // Reset payment state
        paymentScreenshot = null;
        currentOrderData = null;

        // Show success
        const successOrderId = document.getElementById('successOrderId');
        if (successOrderId) successOrderId.textContent = paymentData.order_id;
        openModal('successModal');

    } catch (error) {
        showToast(error.message || 'Failed to record payment. Please try again.', 'error');
    } finally {
        if (confirmBtn) {
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = '✓ I Have Paid';
        }
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

// Make functions globally available
window.updateQuantity = updateQuantity;
window.removeFromCart = removeFromCart;
window.clearCart = clearCart;
window.placeOrder = placeOrder;
window.copyUpiId = copyUpiId;
window.handleScreenshotUpload = handleScreenshotUpload;
window.removeScreenshot = removeScreenshot;
window.confirmPayment = confirmPayment;
window.cancelPayment = cancelPayment;
