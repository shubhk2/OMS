// Frontend/src/assets/js/login.js
// Handles the login form submission and role-aware redirect.

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const usernameEl = document.getElementById('username');
    const passwordEl = document.getElementById('password');
    const errorMessage = document.getElementById('error-message');

    const username = usernameEl ? usernameEl.value : '';
    const password = passwordEl ? passwordEl.value : '';

    try {
      const response = await fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('accessToken', data.access_token);

        if (data.role !== undefined && data.role !== null) {
          localStorage.setItem('userRole', String(data.role));
        } else {
          localStorage.removeItem('userRole');
        }

        // Use shared redirect logic (handles /OMS/... prefixes etc.)
        if (window.omsAuth && typeof window.omsAuth.redirectToIndex === 'function') {
          window.omsAuth.redirectToIndex();
        } else {
          // Fallback relative to /html/authentication-login.html
          window.location.href = './views/employee/index.html';
        }
      } else {
        const errorData = await response.json().catch(() => ({}));
        if (errorMessage) {
          errorMessage.textContent = errorData.msg || errorData.error || 'Login failed. Please check your credentials.';
          errorMessage.style.display = 'block';
        }
      }
    } catch (e) {
      if (errorMessage) {
        errorMessage.textContent = 'An error occurred. Please try again later.';
        errorMessage.style.display = 'block';
      }
    }
  });
});

