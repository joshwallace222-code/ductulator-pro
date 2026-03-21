
// ===== DuctCalc Pro V3 — Home Page & Navigation Enhancement =====
(function() {
  var pageHome = document.getElementById('page-home');
  var appHeader = document.getElementById('appHeaderHome');
  var bottomNav = document.getElementById('bottomNav');

  function showHomePage() {
    // Hide all .page divs
    document.querySelectorAll('.page').forEach(function(p) {
      p.classList.remove('active');
    });
    // Show home
    pageHome.classList.add('active');
    // Deactivate bottom nav
    bottomNav.querySelectorAll('.bottom-nav-item').forEach(function(b) {
      b.classList.remove('active');
    });
  }

  function navigateToPage(pageName) {
    // Hide home
    pageHome.classList.remove('active');
    // Use existing showPage
    if (typeof showPage === 'function') {
      showPage(pageName);
    }
    // Sync bottom nav
    bottomNav.querySelectorAll('.bottom-nav-item').forEach(function(b) {
      b.classList.remove('active');
      if (b.getAttribute('data-page') === pageName) b.classList.add('active');
    });
    // Close more panel if open
    var mp = document.getElementById('morePanel');
    if (mp) mp.classList.remove('open');
  }

  // Home card clicks
  document.querySelectorAll('[data-home-nav]').forEach(function(el) {
    el.addEventListener('click', function() {
      navigateToPage(this.getAttribute('data-home-nav'));
    });
  });

  // App header logo -> home
  if (appHeader) {
    appHeader.addEventListener('click', showHomePage);
  }

  // Override bottom nav to also hide home
  bottomNav.querySelectorAll('.bottom-nav-item[data-page]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var pg = this.getAttribute('data-page');
      if (pg) navigateToPage(pg);
    }, true);
  });

  // More panel tools also navigate
  document.querySelectorAll('.more-tool[data-page]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var pg = this.getAttribute('data-page');
      if (pg) navigateToPage(pg);
    }, true);
  });
})();
