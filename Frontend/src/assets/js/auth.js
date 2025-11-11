const API_URL = 'http://127.0.0.1:5000';

// Redirect to index if a logged-in user tries to access the login page.
(function() {
    const onLoginPage = window.location.pathname.endsWith('authentication-login.html');
    const token = localStorage.getItem('accessToken');
    if (token && onLoginPage) {
        window.location.href = './index.html';
    }
})();

async function ensureAuthenticated() {
    const token = localStorage.getItem('accessToken');
    const onLoginPage = window.location.pathname.endsWith('authentication-login.html');

    if (!token) {
        if (!onLoginPage) {
            window.location.href = './authentication-login.html';
        }
        return;
    }

    try {
        const response = await fetch(`${API_URL}/profile`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        // If token is invalid or expired the server should return 401/422.
        if (response.status === 401 || response.status === 422) {
            console.warn('Authentication failed: token invalid/expired', response.status);
            localStorage.removeItem('accessToken');
            if (!onLoginPage) {
                window.location.href = './authentication-login.html';
            }
            return;
        }

        if (!response.ok) {
            // Server returned 5xx or other non-auth error. Don't clear token on server/network errors.
            console.error('Unexpected response while checking profile:', response.status);
            // Optionally: show a notification to the user instead of logging out.
            return;
        }

        // If response.ok, we are authenticated. No action needed.
    } catch (error) {
        console.error('Authentication check failed (network or CORS error):', error);
        // Don't remove the token on network/CORS errors; keep the user on the page.
        // This prevents immediate redirect to login when the backend temporarily fails or when
        // preflight/CORS issues happen in the browser.
        return;
    }
}

function handleLogout() {
    const logoutButton = document.querySelector('#logoutBtn, .logout-btn');
    if (logoutButton) {
        logoutButton.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('accessToken');
            window.location.href = './authentication-login.html';
        });
    }
}

// Run authentication check on all pages except login
if (!window.location.pathname.endsWith('authentication-login.html')) {
    ensureAuthenticated();
}

document.addEventListener('DOMContentLoaded', handleLogout);
