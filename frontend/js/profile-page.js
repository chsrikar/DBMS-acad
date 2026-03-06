/**
 * ========================================
 * Campus Canteen - Profile Page
 * User profile and account management
 * ========================================
 */

/**
 * Initialize profile page
 */
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
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
 * Logout user
 */
function logout() {
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

/**
 * Load user profile
 */
async function loadProfile() {
    const profileContainer = document.getElementById('profileContainer');
    const loginPrompt = document.getElementById('profileLoginPrompt');

    if (!isLoggedIn()) {
        if (profileContainer) profileContainer.style.display = 'none';
        if (loginPrompt) loginPrompt.style.display = 'block';
        return;
    }

    if (profileContainer) profileContainer.style.display = 'block';
    if (loginPrompt) loginPrompt.style.display = 'none';

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
                    <a href="orders.html" class="btn btn-outline">📋 View Orders</a>
                    <button class="btn btn-secondary" onclick="logout()">🚪 Logout</button>
                </div>
            </div>
        </div>
    `;
}

// Make functions globally available
window.loadProfile = loadProfile;
window.logout = logout;
