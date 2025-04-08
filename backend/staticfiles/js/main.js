// ============================================================================
// File Path: frontend/static/js/main.js
// Description: Main JavaScript file for Calibrify application
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initializeSidebar();
    initializeDropdowns();
    initializeAlerts();
    initializeFormValidation();
});

// Sidebar functionality
function initializeSidebar() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-hidden');

            // Store sidebar state in localStorage
            localStorage.setItem('sidebarActive', sidebar.classList.contains('active'));
        });

        // Restore sidebar state on page load
        const sidebarActive = localStorage.getItem('sidebarActive') === 'true';
        if (sidebarActive) {
            sidebar.classList.add('active');
            mainContent.classList.add('sidebar-hidden');
        }
    }
}

// Dropdown menus (notifications and user menu)
function initializeDropdowns() {
    // Notification dropdown
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationMenu = document.getElementById('notificationMenu');

    if (notificationDropdown && notificationMenu) {
        notificationDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationMenu.classList.toggle('active');
            // Close user menu if open
            if (userMenu && userMenu.classList.contains('active')) {
                userMenu.classList.remove('active');
            }
        });
    }

    // User menu dropdown
    const userMenuDropdown = document.getElementById('userMenuDropdown');
    const userMenu = document.getElementById('userMenu');

    if (userMenuDropdown && userMenu) {
        userMenuDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
            userMenu.classList.toggle('active');
            // Close notification menu if open
            if (notificationMenu && notificationMenu.classList.contains('active')) {
                notificationMenu.classList.remove('active');
            }
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (notificationMenu && notificationMenu.classList.contains('active') &&
            !notificationDropdown.contains(e.target) && !notificationMenu.contains(e.target)) {
            notificationMenu.classList.remove('active');
        }

        if (userMenu && userMenu.classList.contains('active') &&
            !userMenuDropdown.contains(e.target) && !userMenu.contains(e.target)) {
            userMenu.classList.remove('active');
        }
    });

    // Close dropdowns when pressing Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (notificationMenu && notificationMenu.classList.contains('active')) {
                notificationMenu.classList.remove('active');
            }
            if (userMenu && userMenu.classList.contains('active')) {
                userMenu.classList.remove('active');
            }
        }
    });
}

// Alert messages
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        }

        // Auto-hide alerts after 5 seconds
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            let isValid = true;

            // Required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    showFieldError(field, 'This field is required');
                } else {
                    clearFieldError(field);
                }
            });

            // Date validation
            const dateFields = form.querySelectorAll('input[type="date"]');
            dateFields.forEach(field => {
                if (field.value && !isValidDate(field.value)) {
                    isValid = false;
                    showFieldError(field, 'Please enter a valid date');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// Helper functions
function showFieldError(field, message) {
    clearFieldError(field);
    field.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('error');
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

function isValidDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

// CSRF Token handling for AJAX requests
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}

// Add CSRF token to all AJAX requests
document.addEventListener('DOMContentLoaded', function() {
    const token = getCsrfToken();
    if (token) {
        const headers = new Headers({
            'X-CSRFToken': token,
            'Content-Type': 'application/json'
        });
    }
});