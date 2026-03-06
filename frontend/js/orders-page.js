/**
 * ========================================
 * Campus Canteen - Orders Page
 * Order history and tracking functionality
 * ========================================
 */

/**
 * Initialize orders page
 */
document.addEventListener('DOMContentLoaded', () => {
    loadOrders();
});

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return localStorage.getItem('user') !== null;
}

/**
 * Get current user
 */
function getCurrentUser() {
    return JSON.parse(localStorage.getItem('user') || 'null');
}

/**
 * Load user orders
 */
async function loadOrders() {
    const ordersContainer = document.getElementById('ordersContainer');
    const noOrders = document.getElementById('noOrders');
    const loginPrompt = document.getElementById('loginPrompt');

    if (!isLoggedIn()) {
        if (ordersContainer) ordersContainer.style.display = 'none';
        if (noOrders) noOrders.style.display = 'none';
        if (loginPrompt) loginPrompt.style.display = 'block';
        return;
    }

    if (loginPrompt) loginPrompt.style.display = 'none';
    if (ordersContainer) ordersContainer.style.display = 'block';

    ordersContainer.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading your orders...</p>
        </div>
    `;

    try {
        const user = getCurrentUser();
        const history = await API.Student.getOrders(user.student_id);

        if (!history.orders || history.orders.length === 0) {
            if (ordersContainer) ordersContainer.style.display = 'none';
            if (noOrders) noOrders.style.display = 'block';
            return;
        }

        if (noOrders) noOrders.style.display = 'none';

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

// Make functions globally available
window.loadOrders = loadOrders;
