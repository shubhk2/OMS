
function handleLogout() {
    const logoutButton = document.querySelector('#logoutBtn, .logout-btn'); // Use a class for more flexibility
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('accessToken');
            window.location.href = './authentication-login.html';
        });
    }
}

// Add logout handler on DOM content loaded
document.addEventListener('DOMContentLoaded', handleLogout);
// Redirect to index if a logged-in user tries to access the login page.
(function() {
    const onLoginPage = window.location.pathname.endsWith('authentication-login.html');
    const token = localStorage.getItem('accessToken');
    if (token && onLoginPage) {
        window.location.href = './index.html';
    }
})();

