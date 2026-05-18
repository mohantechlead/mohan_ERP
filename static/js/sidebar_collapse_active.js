/* Syncs "clicked/open" look for sidebar collapse toggles (WIP, MR, etc.) */
(function () {
  var side = document.getElementById('sidebar');
  if (!side) return;

  function toggleFor(collapseEl) {
    if (!collapseEl.id) return null;
    return side.querySelector(
      'a.dropdown-toggle[href="#' + collapseEl.id + '"]'
    );
  }

  function syncOne(collapseEl) {
    var link = toggleFor(collapseEl);
    if (!link) return;
    if (collapseEl.classList.contains('show')) {
      link.classList.add('sidebar-nav-toggle-active');
    } else {
      link.classList.remove('sidebar-nav-toggle-active');
    }
  }

  side.querySelectorAll('.collapse').forEach(function (el) {
    syncOne(el);
    el.addEventListener('shown.bs.collapse', function () {
      syncOne(el);
    });
    el.addEventListener('hidden.bs.collapse', function () {
      syncOne(el);
    });
  });
})();
