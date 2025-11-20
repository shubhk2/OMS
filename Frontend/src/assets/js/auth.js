// Frontend/src/assets/js/auth.js
(function() {
  function handleLogout() {
    const logoutButton = document.querySelector('#logoutBtn, .logout-btn');
    if (logoutButton) {
      logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        window.location.href = './authentication-login.html';
      });
    }
  }

  function enforceAuth() {
    const token = localStorage.getItem('accessToken');
    const path = window.location.pathname;
    const onLoginPage = path.endsWith('authentication-login.html') || path.endsWith('/authentication-login.html');

    if (!token && !onLoginPage) {
      // Not authenticated and not on login page -> send to login
      window.location.href = './authentication-login.html';
      return;
    }

    if (token && onLoginPage) {
      // Already authenticated and on login page -> send to app
      window.location.href = './index.html';
      return;
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    handleLogout();
    enforceAuth();
  });
})();
