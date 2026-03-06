/**
 * ========================================
 * Campus Canteen - Authentication Module
 * Handles user login, registration, and session
 * ========================================
 */

// Current user state
let currentUser = null;

/**
 * Initialize authentication state
 */
function initAuth() {
    // Check for saved user in localStorage
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            updateAuthUI();
        } catch (e) {
            localStorage.removeItem('user');
        }
    }
    updateAuthUI();
    loadRegistrationData();
}

/**
 * Update UI based on authentication state
 */
function updateAuthUI() {
    const navAuth = document.getElementById('navAuth');
    if (!navAuth) return;

    if (currentUser) {
        navAuth.innerHTML = `
            <div class="user-menu">
                <span class="user-greeting">Hi, ${currentUser.name.split(' ')[0]}!</span>
                <button class="btn btn-ghost btn-sm" onclick="logout()">Logout</button>
            </div>
        `;
    } else {
        navAuth.innerHTML = `
            <button class="btn btn-ghost btn-sm" onclick="openModal('loginModal')">Login</button>
            <button class="btn btn-primary btn-sm" onclick="openModal('registerModal')">Register</button>
        `;
    }
}

/**
 * Load hostels and departments for registration form
 */
async function loadRegistrationData() {
    try {
        const [hostels, departments] = await Promise.all([
            API.Hostel.getAll(),
            API.Department.getAll()
        ]);

        const hostelSelect = document.getElementById('regHostel');
        const deptSelect = document.getElementById('regDepartment');

        if (hostelSelect) {
            hostelSelect.innerHTML = '<option value="">Select Hostel</option>';
            hostels.forEach(h => {
                hostelSelect.innerHTML += `<option value="${h.hostel_id}">${h.hostel_name}</option>`;
            });
        }

        if (deptSelect) {
            deptSelect.innerHTML = '<option value="">Select Department</option>';
            departments.forEach(d => {
                deptSelect.innerHTML += `<option value="${d.department_id}">${d.department_name} (${d.department_code})</option>`;
            });
        }
    } catch (error) {
        console.error('Failed to load registration data:', error);
    }
}

/**
 * Handle login form submission
 */
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const user = await API.Student.login(email, password);
        currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));

        closeModal('loginModal');
        updateAuthUI();
        showToast('Welcome back, ' + user.name + '!', 'success');

        // Reload current page to refresh data
        window.location.reload();
    } catch (error) {
        showToast(error.message || 'Login failed. Please check your credentials.', 'error');
    }
}

/**
 * Handle registration form submission
 */
async function handleRegister(event) {
    event.preventDefault();

    const email = document.getElementById('regEmail').value;

    // Validate Email Domain
    if (!email.endsWith('@visat.ac.in')) {
        showToast('Only @visat.ac.in emails are allowed.', 'error');
        return;
    }

    const formData = {
        name: document.getElementById('regName').value,
        email: email,
        roll_number: document.getElementById('regRoll').value,
        phone: document.getElementById('regPhone').value || null,
        password: document.getElementById('regPassword').value,
        hostel_id: parseInt(document.getElementById('regHostel').value) || null,
        department_id: parseInt(document.getElementById('regDepartment').value) || null
    };

    try {
        const user = await API.Student.register(formData);
        currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));

        closeModal('registerModal');
        updateAuthUI();
        showToast('Welcome to SENZA, ' + user.name + '!', 'success');

        // Reload current page to refresh data
        window.location.reload();
    } catch (error) {
        showToast(error.message || 'Registration failed. Please try again.', 'error');
    }
}

/**
 * Logout current user
 */
function logout() {
    currentUser = null;
    localStorage.removeItem('user');
    localStorage.removeItem('cart');
    updateAuthUI();
    showToast('You have been logged out.', 'success');

    // Redirect to home page
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 500);
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return currentUser !== null;
}

/**
 * Get current user
 */
function getCurrentUser() {
    return currentUser;
}

/**
 * Require login - shows login modal if not logged in
 */
function requireLogin() {
    if (!isLoggedIn()) {
        openModal('loginModal');
        return false;
    }
    return true;
}

// Make functions globally available
window.initAuth = initAuth;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.logout = logout;
window.isLoggedIn = isLoggedIn;
window.getCurrentUser = getCurrentUser;
window.requireLogin = requireLogin;

