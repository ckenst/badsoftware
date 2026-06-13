(function(){
  const KEY = 'badsw-theme';
  const btnId = 'theme-toggle';
  const root = document.documentElement; // html element

  function apply(theme){
    if(theme === 'light'){
      root.classList.add('theme-light');
      root.classList.remove('theme-dark');
      root.setAttribute('data-theme','light');
    } else {
      root.classList.remove('theme-light');
      root.classList.add('theme-dark');
      root.setAttribute('data-theme','dark');
    }
    updateButton(theme);
  }

  function preferred(){
    const stored = localStorage.getItem(KEY);
    if(stored) return stored;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function updateButton(theme){
    const btn = document.getElementById(btnId);
    if(!btn) return;
    btn.setAttribute('aria-pressed', theme === 'light');
    btn.textContent = theme === 'light' ? '☀️' : '🌙';
  }

  function toggle(){
    const current = localStorage.getItem(KEY) || (root.classList.contains('theme-light') ? 'light' : 'dark');
    const next = current === 'light' ? 'dark' : 'light';
    localStorage.setItem(KEY, next);
    apply(next);
  }

  // Apply immediately so variables take effect before paint (reduces flash)
  try{
    apply(preferred());
  }catch(e){/* ignore */}

  // Wire up the button when DOM is ready
  document.addEventListener('DOMContentLoaded', function(){
    const btn = document.getElementById(btnId);
    if(btn) btn.addEventListener('click', toggle);
    // Ensure button reflects current state
    updateButton(localStorage.getItem(KEY) || (root.classList.contains('theme-light') ? 'light' : (root.getAttribute('data-theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'))));
  });
})();
