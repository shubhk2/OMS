// Frontend/src/assets/js/auth.js
(function() {
  function getHtmlBasePath() {
    // We want the URL prefix up to (but not including) '/html/' so redirects work whether
    // PyCharm uses '/OMS/Frontend/src/html/..' or another prefix.
    const p = window.location.pathname;
    const idx = p.lastIndexOf('/html/');
    if (idx >= 0) return p.slice(0, idx);
    return '';
  }

  function absFromHtml(pathFromHtmlRoot) {
    // pathFromHtmlRoot must start with '/html/'
    return getHtmlBasePath() + pathFromHtmlRoot;
  }

  function makeLoginPath() {
    return absFromHtml('/html/authentication-login.html');
  }

  function makeIndexPath() {
    const roleRaw = localStorage.getItem('userRole');
    const roleId = roleRaw ? parseInt(roleRaw, 10) : NaN;

    // role id 14-admin, 11/12-hr, 8-tl and rest employees
    if (roleId === 14) return absFromHtml('/html/views/admin/index.html');
    if (roleId === 11 || roleId === 12) return absFromHtml('/html/views/hr/index.html');

    // TLs redirect to employee for now (and all other roles)
    return absFromHtml('/html/views/employee/index.html');
  }

  function redirectToIndex() {
    window.location.href = makeIndexPath();
  }

  function redirectToLogin() {
    window.location.href = makeLoginPath();
  }

  function handleLogout() {
    const logoutButton = document.querySelector('#logoutBtn, .logout-btn');
    if (logoutButton) {
      logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('userRole');
        redirectToLogin();
      });
    }
  }

  function enforceAuth() {
    const token = localStorage.getItem('accessToken');
    const path = window.location.pathname;

    // robust: treat any URL ending with authentication-login.html as login page
    const onLoginPage = /\/authentication-login\.html($|\?)/.test(path) || path.endsWith('/authentication-login.html');

    if (!token && !onLoginPage) {
      redirectToLogin();
      return;
    }

    if (token && onLoginPage) {
      redirectToIndex();
    }
  }

  window.omsAuth = {
    getHtmlBasePath,
    makeLoginPath,
    makeIndexPath,
    redirectToIndex,
    redirectToLogin,
  };

  document.addEventListener('DOMContentLoaded', () => {
    handleLogout();
    enforceAuth();
  });
})();
