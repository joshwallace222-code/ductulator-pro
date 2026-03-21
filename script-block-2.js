
// ===== DuctCalc Pro — Navigation Handler =====
(function() {
  // Bottom nav items
  var bottomNav = document.getElementById('bottomNav');
  var morePanel = document.getElementById('morePanel');
  var morePanelOverlay = document.getElementById('morePanelOverlay');
  var moreNavBtn = document.getElementById('moreNavBtn');

  // Bottom nav page navigation
  bottomNav.addEventListener('click', function(e) {
    var item = e.target.closest('.bottom-nav-item');
    if (!item) return;
    if (item.id === 'moreNavBtn') {
      openMorePanel();
      return;
    }
    var page = item.dataset.page;
    if (page && typeof showPage === 'function') {
      showPage(page);
      updateBottomNav(page);
    }
  });

  // More panel tools
  morePanel.addEventListener('click', function(e) {
    var tool = e.target.closest('.more-tool');
    if (tool) {
      var page = tool.dataset.page;
      if (page && typeof showPage === 'function') {
        showPage(page);
        updateBottomNav(null);
        closeMorePanel();
      }
    }
  });

  // More panel overlay dismiss
  morePanelOverlay.addEventListener('click', closeMorePanel);

  function openMorePanel() {
    morePanel.classList.add('open');
  }

  function closeMorePanel() {
    morePanel.classList.remove('open');
  }

  function updateBottomNav(activePage) {
    var items = bottomNav.querySelectorAll('.bottom-nav-item');
    items.forEach(function(item) {
      if (item.id === 'moreNavBtn') {
        item.classList.remove('active');
      } else {
        item.classList.toggle('active', item.dataset.page === activePage);
      }
    });
  }

  // Listen for external showPage calls (from within the app JS)
  // Override to sync bottom nav
  var origShowPage = window.showPage;
  if (typeof origShowPage === 'function') {
    // Will be patched after original is defined
  }

  // Patch after DOM loads
  window.addEventListener('load', function() {
    if (typeof window.showPage === 'function') {
      var _orig = window.showPage;
      window.showPage = function(key) {
        _orig(key);
        // Sync bottom nav
        var bottomPages = ['roomcfm', 'system'];
        if (bottomPages.indexOf(key) >= 0) {
          updateBottomNav(key);
        } else {
          updateBottomNav(null);
        }
      };
    }
  });
})();
