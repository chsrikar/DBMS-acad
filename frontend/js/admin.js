/**
 * ========================================
 * Campus Canteen - Admin Dashboard
 * Order management and reporting
 * ========================================
 */

const API_BASE = 'http://localhost:8000/api';

// State
let allOrders = [];
let currentFilter = 'all';
let menuItems = [];

// Initialize
// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAdminLogin();
});

/**
 * Check Admin Authentication
 */
function checkAdminLogin() {
    const isAuthenticated = sessionStorage.getItem('admin_authenticated');

    if (!isAuthenticated) {
        document.getElementById('adminLoginModal').classList.add('active');
        document.querySelector('main').style.filter = 'blur(10px) grayscale(100%)';
        document.querySelector('main').style.pointerEvents = 'none';
    } else {
        initAdminPanel();
    }
}

/**
 * Handle Admin Login
 */
function handleAdminLogin(event) {
    event.preventDefault();
    const password = document.getElementById('adminPassword').value;

    // Simple password check (In a real app, this should be a backend call)
    if (password === 'admin123') {
        sessionStorage.setItem('admin_authenticated', 'true');
        document.getElementById('adminLoginModal').classList.remove('active');
        document.querySelector('main').style.filter = 'none';
        document.querySelector('main').style.pointerEvents = 'auto';
        initAdminPanel();
        showToast('Welcome back, Admin!', 'success');
    } else {
        showToast('Incorrect password', 'error');
        document.getElementById('adminPassword').value = '';
    }
}

/**
 * Initialize Admin Panel Data
 */
function initAdminPanel() {
    loadAllOrders();
    loadMenuItems();
    initReportDate();

    // Auto-refresh every 30 seconds
    setInterval(loadAllOrders, 30000);
}

/**
 * Show tab
 */
function showTab(tabName) {
    document.querySelectorAll('.admin-tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(`tab-${tabName}`).classList.add('active');

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.tab === tabName) link.classList.add('active');
    });

    if (tabName === 'menu') loadMenuItems();
    if (tabName === 'reports') loadReport();
}

/**
 * Load all orders for canteen
 */
async function loadAllOrders() {
    const grid = document.getElementById('ordersGrid');

    try {
        // Load orders by different statuses
        const [placed, preparing, ready, delivered] = await Promise.all([
            fetchOrders('PLACED'),
            fetchOrders('PREPARING'),
            fetchOrders('READY'),
            fetchOrders('DELIVERED')
        ]);

        allOrders = [...placed, ...preparing, ...ready, ...delivered];

        // Update counts
        document.getElementById('count-all').textContent = allOrders.length;
        document.getElementById('count-placed').textContent = placed.length;
        document.getElementById('count-preparing').textContent = preparing.length;
        document.getElementById('count-ready').textContent = ready.length;
        document.getElementById('count-delivered').textContent = delivered.length;

        renderOrders();

    } catch (error) {
        grid.innerHTML = `
            <div class="loading-spinner" style="grid-column: 1/-1;">
                <p>❌ Failed to load orders</p>
                <button class="btn btn-primary" onclick="loadAllOrders()">Retry</button>
            </div>
        `;
    }
}

async function fetchOrders(status) {
    try {
        const response = await fetch(`${API_BASE}/orders/status/${status}`);
        if (!response.ok) return [];
        return await response.json();
    } catch {
        return [];
    }
}

/**
 * Filter orders by status
 */
function filterOrders(status) {
    currentFilter = status;

    document.querySelectorAll('.status-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.status === status) tab.classList.add('active');
    });

    renderOrders();
}

/**
 * Render orders grid
 */
function renderOrders() {
    const grid = document.getElementById('ordersGrid');

    let filtered = allOrders;
    if (currentFilter !== 'all') {
        filtered = allOrders.filter(o => o.order_status === currentFilter);
    }

    // Sort by date (newest first for placed, oldest first for others)
    filtered.sort((a, b) => {
        const dateA = new Date(a.order_date);
        const dateB = new Date(b.order_date);
        if (a.order_status === 'PLACED') return dateB - dateA;
        return dateA - dateB;
    });

    if (filtered.length === 0) {
        grid.innerHTML = `
            <div class="loading-spinner" style="grid-column: 1/-1;">
                <div class="empty-icon">📋</div>
                <p>No orders found</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = filtered.map(order => renderOrderCard(order)).join('');
}

/**
 * Parse pickup time from special instructions
 */
function parsePickupTime(instructions) {
    if (!instructions) return null;
    const match = instructions.match(/Pickup Time:\s*([^|]+)/);
    if (match) {
        const time = match[1].trim();
        // Convert time format for display
        if (time === '10:50-11:00') return '10:50 - 11:00 AM (Morning Break)';
        if (time === '12:30-13:00') return '12:30 - 1:00 PM (Lunch Break)';
        if (time === '14:50-15:00') return '2:50 - 3:00 PM (Afternoon Break)';
        return time;
    }
    return null;
}

/**
 * Parse other notes from special instructions (excluding pickup time)
 */
function parseOtherNotes(instructions) {
    if (!instructions) return null;
    const parts = instructions.split('|').map(p => p.trim());
    const notes = parts.filter(p => !p.startsWith('Pickup Time:'));
    return notes.length > 0 ? notes.join(' | ') : null;
}

/**
 * Render single order card
 */
function renderOrderCard(order) {
    const orderDate = new Date(order.order_date);
    const timeStr = orderDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    const dateStr = orderDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

    const statusClass = `status-${order.order_status.toLowerCase()}`;
    const studentName = order.student?.name || 'Customer';
    const studentRoll = order.student?.roll_number || '';
    const initials = studentName.split(' ').map(n => n[0]).join('').toUpperCase();

    // Parse pickup time
    const pickupTime = parsePickupTime(order.special_instructions);

    // Get items preview
    const itemsHtml = order.order_items?.slice(0, 3).map(item => `
        <div class="order-item-row">
            <span><span class="item-qty">${item.quantity}x</span> ${item.menu_item?.item_name || 'Item'}</span>
            <span>₹${item.subtotal?.toFixed(2) || '0.00'}</span>
        </div>
    `).join('') || '<div class="order-item-row">No items</div>';

    const moreItems = (order.order_items?.length || 0) > 3
        ? `<div class="order-item-row" style="color: var(--text-muted)">+${order.order_items.length - 3} more items</div>`
        : '';

    // Status action button
    let actionBtn = '';
    if (order.order_status === 'PLACED') {
        actionBtn = `<button class="btn btn-status-next" onclick="updateOrderStatus(${order.order_id}, 'PREPARING')">🍳 Start Preparing</button>`;
    } else if (order.order_status === 'PREPARING') {
        actionBtn = `<button class="btn btn-status-next" onclick="updateOrderStatus(${order.order_id}, 'READY')">✅ Mark Ready</button>`;
    } else if (order.order_status === 'READY') {
        actionBtn = `<button class="btn btn-status-next" onclick="updateOrderStatus(${order.order_id}, 'DELIVERED')">📦 Mark Delivered</button>`;
    }

    return `
        <div class="admin-order-card ${statusClass}">
            <div class="order-card-header">
                <div>
                    <div class="order-number">Order #${order.order_id}</div>
                    <div class="order-time">${timeStr} • ${dateStr}</div>
                </div>
                <div class="order-type-badge">
                    🏃 ${order.order_type}
                </div>
            </div>
            <div class="order-card-body">
                <div class="order-customer">
                    <div class="customer-avatar">${initials}</div>
                    <div class="customer-info">
                        <h4>${studentName}</h4>
                        <p>${studentRoll}</p>
                    </div>
                </div>
                ${pickupTime ? `
                <div class="pickup-time-badge">
                    <span>⏰ Pickup: ${pickupTime}</span>
                </div>
                ` : ''}
                <div class="order-items-preview">
                    ${itemsHtml}
                    ${moreItems}
                    <div class="order-total-row">
                        <span>Total</span>
                        <span>₹${order.total_amount?.toFixed(2) || '0.00'}</span>
                    </div>
                </div>
            </div>
            <div class="order-card-footer">
                <button class="btn btn-outline" onclick="viewOrderDetail(${order.order_id})">View Details</button>
                ${actionBtn}
            </div>
        </div>
    `;
}

/**
 * Update order status
 */
async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`${API_BASE}/orders/${orderId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_status: newStatus })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update status');
        }

        showToast(`Order #${orderId} updated to ${newStatus}`, 'success');
        loadAllOrders();

    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * View order detail
 */
async function viewOrderDetail(orderId) {
    const modal = document.getElementById('orderModal');
    const content = document.getElementById('orderModalContent');

    content.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';
    modal.classList.add('active');

    try {
        const response = await fetch(`${API_BASE}/orders/${orderId}`);
        const order = await response.json();

        const statusSteps = ['PLACED', 'PREPARING', 'READY', 'DELIVERED'];
        const currentIdx = statusSteps.indexOf(order.order_status);

        const progressHtml = statusSteps.map((status, idx) => {
            let stepClass = '';
            if (idx < currentIdx) stepClass = 'completed';
            else if (idx === currentIdx) stepClass = 'current';

            const icons = { PLACED: '📝', PREPARING: '👨‍🍳', READY: '✅', DELIVERED: '📦' };

            return `
                <div class="status-step ${stepClass}">
                    <div class="status-step-icon">${icons[status]}</div>
                    <span class="status-step-label">${status}</span>
                </div>
            `;
        }).join('');

        const itemsHtml = order.order_items?.map(item => `
            <div class="order-item-row">
                <span><span class="item-qty">${item.quantity}x</span> ${item.menu_item?.item_name}</span>
                <span>₹${item.subtotal?.toFixed(2)}</span>
            </div>
        `).join('') || '';

        // Payment section HTML
        let paymentHtml = '';
        if (order.payment) {
            const paymentStatus = order.payment.payment_status;
            let statusClass = 'payment-status-pending';
            if (paymentStatus === 'COMPLETED') statusClass = 'payment-status-completed';
            else if (paymentStatus === 'FAILED') statusClass = 'payment-status-rejected';

            // Payment action buttons (only show for pending payments)
            let paymentActions = '';
            if (paymentStatus === 'PENDING' && order.payment.payment_screenshot) {
                paymentActions = `
                    <div class="payment-actions-admin">
                        <button class="btn btn-accept-payment" onclick="acceptPayment(${order.payment.payment_id}, ${order.order_id})">
                            ✓ Accept Payment
                        </button>
                        <button class="btn btn-reject-payment" onclick="rejectPayment(${order.payment.payment_id}, ${order.order_id})">
                            ✕ Reject Payment
                        </button>
                    </div>
                `;
            }

            paymentHtml = `
                <div class="order-detail-section">
                    <h4>💳 Payment Details</h4>
                    <p>Method: <strong>UPI</strong></p>
                    <p>Amount: <strong>₹${order.payment.amount_paid?.toFixed(2)}</strong></p>
                    <p>Status: <span class="payment-status-badge ${statusClass}">${paymentStatus}</span></p>
                    ${order.payment.payment_screenshot ? `
                        <div class="payment-screenshot-container">
                            <p style="margin-top: 1rem; margin-bottom: 0.5rem; color: var(--text-secondary);">📸 Payment Screenshot:</p>
                            <div class="payment-screenshot-preview">
                                <img src="${order.payment.payment_screenshot}" alt="Payment Screenshot" onclick="viewFullScreenshot('${order.payment.payment_screenshot}')" style="cursor: pointer;" title="Click to view full size">
                            </div>
                        </div>
                        ${paymentActions}
                    ` : '<p style="color: var(--warning);">⚠️ No screenshot uploaded</p>'}
                </div>
            `;
        } else {
            paymentHtml = `
                <div class="order-detail-section">
                    <h4>💳 Payment Details</h4>
                    <p style="color: var(--warning);">⚠️ Payment not yet submitted</p>
                </div>
            `;
        }

        content.innerHTML = `
            <div class="order-detail-header">
                <h2>Order #${order.order_id}</h2>
                <span class="order-detail-status status-${order.order_status.toLowerCase()}">${order.order_status}</span>
            </div>
            
            <div class="status-progress">
                ${progressHtml}
            </div>
            
            <div class="order-detail-section">
                <h4>Customer</h4>
                <p><strong>${order.student?.name}</strong> (${order.student?.roll_number})</p>
                <p>📧 ${order.student?.email || 'N/A'}</p>
                <p>📱 ${order.student?.phone || 'N/A'}</p>
            </div>
            
            <div class="order-detail-section">
                <h4>Order Items</h4>
                <div class="order-detail-items">
                    ${itemsHtml}
                    <div class="order-total-row">
                        <span>Total Amount</span>
                        <span>₹${order.total_amount?.toFixed(2)}</span>
                    </div>
                </div>
            </div>
            
            ${paymentHtml}
            
            <div class="order-detail-section">
                <h4>Order Info</h4>
                <p>📦 Type: ${order.order_type}</p>
                <p>📅 Date: ${new Date(order.order_date).toLocaleString()}</p>
                ${order.order_type === 'PICKUP' && parsePickupTime(order.special_instructions) ? `<p>⏰ <strong>Pickup Time: ${parsePickupTime(order.special_instructions)}</strong></p>` : ''}
                ${parseOtherNotes(order.special_instructions) ? `<p>📝 Notes: ${parseOtherNotes(order.special_instructions)}</p>` : ''}
            </div>
            
            ${order.order_status !== 'DELIVERED' && order.order_status !== 'CANCELLED' ? `
                <div class="order-actions">
                    ${order.order_status === 'PLACED' ? `<button class="btn btn-status-next" onclick="updateOrderStatus(${order.order_id}, 'PREPARING'); closeModal('orderModal');">🍳 Start Preparing</button>` : ''}
                    ${order.order_status === 'PREPARING' ? `<button class="btn btn-status-next" onclick="updateOrderStatus(${order.order_id}, 'READY'); closeModal('orderModal');">✅ Mark Ready</button>` : ''}
                    ${order.order_status === 'READY' ? `<button class="btn btn-status-next" onclick="updateOrderStatus(${order.order_id}, 'DELIVERED'); closeModal('orderModal');">📦 Mark Delivered</button>` : ''}
                </div>
            ` : ''}
        `;

    } catch (error) {
        content.innerHTML = `<p>Failed to load order details</p>`;
    }
}

/**
 * View full size screenshot in new tab
 */
function viewFullScreenshot(base64Data) {
    const newTab = window.open();
    newTab.document.write(`
        <html>
            <head><title>Payment Screenshot</title></head>
            <body style="margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #1a1a2e;">
                <img src="${base64Data}" style="max-width: 100%; max-height: 100vh; object-fit: contain;">
            </body>
        </html>
    `);
}

/**
 * Accept payment - marks payment as COMPLETED and starts order processing
 */
async function acceptPayment(paymentId, orderId) {
    if (!confirm('Accept this payment and start preparing the order?')) return;

    try {
        // Update payment status to COMPLETED
        await fetch(`${API_BASE}/payments/${paymentId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payment_status: 'COMPLETED' })
        });

        // Update order status to PREPARING
        await fetch(`${API_BASE}/orders/${orderId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_status: 'PREPARING' })
        });

        showToast('Payment accepted! Order is now being prepared.', 'success');
        closeModal('orderModal');
        loadAllOrders();

    } catch (error) {
        showToast('Failed to accept payment: ' + error.message, 'error');
    }
}

/**
 * Reject payment - marks payment as FAILED and cancels the order
 */
async function rejectPayment(paymentId, orderId) {
    if (!confirm('Reject this payment and cancel the order? This action cannot be undone.')) return;

    try {
        // Update payment status to FAILED
        await fetch(`${API_BASE}/payments/${paymentId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payment_status: 'FAILED' })
        });

        // Update order status to CANCELLED
        await fetch(`${API_BASE}/orders/${orderId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_status: 'CANCELLED' })
        });

        showToast('Payment rejected. Order has been cancelled.', 'warning');
        closeModal('orderModal');
        loadAllOrders();

    } catch (error) {
        showToast('Failed to reject payment: ' + error.message, 'error');
    }
}


/**
 * Load menu items for admin
 */
async function loadMenuItems() {
    const grid = document.getElementById('menuAdminGrid');

    try {
        const response = await fetch(`${API_BASE}/menu`);
        menuItems = await response.json();

        grid.innerHTML = menuItems.map(item => {
            const emoji = getFoodEmoji(item);
            return `
                <div class="menu-admin-item ${!item.is_available ? 'unavailable' : ''}">
                    <div class="menu-item-emoji">${emoji}</div>
                    <div class="menu-item-info">
                        <h4>${item.item_name}</h4>
                        <span class="price">₹${item.price.toFixed(2)}</span>
                        <span class="category">${item.category || 'Uncategorized'}</span>
                    </div>
                    <div class="menu-item-actions">
                        <div class="menu-item-toggle">
                            <div class="toggle-switch ${item.is_available ? 'active' : ''}" onclick="toggleItemAvailability(${item.item_id})"></div>
                            <span class="toggle-label">${item.is_available ? 'Available' : 'Unavailable'}</span>
                        </div>
                        <button class="btn-delete-item" onclick="deleteMenuItem(${item.item_id})" title="Delete Item">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        grid.innerHTML = '<p>Failed to load menu</p>';
    }
}

/**
 * Toggle menu item availability
 */
async function toggleItemAvailability(itemId) {
    try {
        const response = await fetch(`${API_BASE}/menu/${itemId}/toggle`, {
            method: 'PUT'
        });

        if (response.ok) {
            showToast('Item availability updated', 'success');
            loadMenuItems();
        }
    } catch (error) {
        showToast('Failed to update item', 'error');
    }
}

/**
 * Delete Menu Item
 */
async function deleteMenuItem(itemId) {
    if (!confirm('Are you sure you want to delete this item? This cannot be undone.')) return;

    try {
        const response = await fetch(`${API_BASE}/menu/${itemId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showToast('Item deleted successfully', 'success');
            loadMenuItems();
        } else {
            throw new Error('Failed to delete item');
        }
    } catch (error) {
        showToast('Failed to delete item', 'error');
    }
}

/**
 * Get food emoji
 */
function getFoodEmoji(item) {
    const name = item.item_name.toLowerCase();
    if (name.includes('dosa')) return '🥞';
    if (name.includes('idli')) return '🍚';
    if (name.includes('biryani')) return '🍛';
    if (name.includes('thali')) return '🍱';
    if (name.includes('samosa')) return '🥟';
    if (name.includes('coffee')) return '☕';
    if (name.includes('tea')) return '🍵';
    if (name.includes('lassi')) return '🥛';
    if (name.includes('maggi')) return '🍜';
    if (name.includes('fries')) return '🍟';
    return '🍽️';
}

/**
 * Initialize report date
 */
function initReportDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('reportDate').value = today;
}

/**
 * Load daily report
 */
async function loadReport() {
    const date = document.getElementById('reportDate').value;

    try {
        const response = await fetch(`${API_BASE}/reports/revenue?report_date=${date}`);
        const report = await response.json();

        document.getElementById('totalOrders').textContent = report.total_orders || 0;
        document.getElementById('completedOrders').textContent = report.completed_orders || 0;
        document.getElementById('totalRevenue').textContent = `₹${(report.total_revenue || 0).toFixed(2)}`;
        document.getElementById('cashRevenue').textContent = `₹${(report.cash_revenue || 0).toFixed(2)}`;
        document.getElementById('upiRevenue').textContent = `₹${(report.upi_revenue || 0).toFixed(2)}`;

    } catch (error) {
        showToast('Failed to load report', 'error');
    }
}

/**
 * Open Add Item Modal
 */
function openAddItemModal() {
    openModal('addItemModal');
}

/**
 * Handle Add Menu Item Form Submission
 */
async function handleAddMenuItem(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Construct the payload
    const itemData = {
        item_name: formData.get('item_name'),
        description: formData.get('description'),
        price: parseFloat(formData.get('price')),
        category: formData.get('category'),
        is_vegetarian: formData.get('is_vegetarian') === 'on',
        is_available: true,
        canteen_id: 1 // Default to 1 for this demo
    };

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Adding...';
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/menu`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(itemData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add item');
        }

        // Success
        showToast('Menu item added successfully!', 'success');
        closeModal('addItemModal');
        form.reset();
        loadMenuItems(); // Refresh the list

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Modal functions
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

// Toast
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${type === 'success' ? '✓' : '✕'}</span>
        <span class="toast-message">${message}</span>
    `;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}
