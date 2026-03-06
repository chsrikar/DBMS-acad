/**
 * ========================================
 * Campus Canteen - API Service
 * Handles all backend API communication
 * ========================================
 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Generic API request handler
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'API request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ========================================
// STUDENT API
// ========================================

const StudentAPI = {
    register: async (studentData) => {
        return apiRequest('/students/register', {
            method: 'POST',
            body: JSON.stringify(studentData)
        });
    },

    login: async (email, password) => {
        return apiRequest('/students/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },

    getById: async (studentId) => {
        return apiRequest(`/students/${studentId}`);
    },

    getOrders: async (studentId) => {
        return apiRequest(`/students/${studentId}/orders`);
    },

    update: async (studentId, updateData) => {
        return apiRequest(`/students/${studentId}`, {
            method: 'PUT',
            body: JSON.stringify(updateData)
        });
    }
};

// ========================================
// MENU API
// ========================================

const MenuAPI = {
    getAll: async (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.canteen_id) params.append('canteen_id', filters.canteen_id);
        if (filters.category) params.append('category', filters.category);
        if (filters.available_only) params.append('available_only', 'true');
        if (filters.vegetarian_only) params.append('vegetarian_only', 'true');

        const queryString = params.toString();
        return apiRequest(`/menu${queryString ? '?' + queryString : ''}`);
    },

    getById: async (itemId) => {
        return apiRequest(`/menu/${itemId}`);
    },

    getPopular: async (limit = 10) => {
        return apiRequest(`/menu/popular/items?limit=${limit}`);
    }
};

// ========================================
// ORDER API
// ========================================

const OrderAPI = {
    create: async (orderData) => {
        return apiRequest('/orders', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
    },

    getById: async (orderId) => {
        return apiRequest(`/orders/${orderId}`);
    },

    getByStudent: async (studentId, skip = 0, limit = 50) => {
        return apiRequest(`/orders/student/${studentId}?skip=${skip}&limit=${limit}`);
    },

    getByStatus: async (status, canteenId = null) => {
        const params = canteenId ? `?canteen_id=${canteenId}` : '';
        return apiRequest(`/orders/status/${status}${params}`);
    },

    updateStatus: async (orderId, status) => {
        return apiRequest(`/orders/${orderId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ order_status: status })
        });
    }
};

// ========================================
// PAYMENT API
// ========================================

const PaymentAPI = {
    create: async (paymentData) => {
        return apiRequest('/payments', {
            method: 'POST',
            body: JSON.stringify(paymentData)
        });
    },

    updateStatus: async (paymentId, status, transactionId = null) => {
        const data = { payment_status: status };
        if (transactionId) data.transaction_id = transactionId;

        return apiRequest(`/payments/${paymentId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    getByOrder: async (orderId) => {
        return apiRequest(`/payments/order/${orderId}`);
    }
};

// ========================================
// CANTEEN & MASTER DATA API
// ========================================

const CanteenAPI = {
    getAll: async (activeOnly = false) => {
        return apiRequest(`/canteens?active_only=${activeOnly}`);
    },

    getById: async (canteenId) => {
        return apiRequest(`/canteens/${canteenId}`);
    }
};

const HostelAPI = {
    getAll: async () => {
        return apiRequest('/hostels');
    }
};

const DepartmentAPI = {
    getAll: async () => {
        return apiRequest('/departments');
    }
};

// ========================================
// REPORT API
// ========================================

const ReportAPI = {
    getDailyRevenue: async (date = null) => {
        const params = date ? `?report_date=${date}` : '';
        return apiRequest(`/reports/revenue${params}`);
    }
};

// Export for use in other modules
window.API = {
    Student: StudentAPI,
    Menu: MenuAPI,
    Order: OrderAPI,
    Payment: PaymentAPI,
    Canteen: CanteenAPI,
    Hostel: HostelAPI,
    Department: DepartmentAPI,
    Report: ReportAPI
};
