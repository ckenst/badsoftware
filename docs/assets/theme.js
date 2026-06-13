(function(){
  const KEY = 'badsw-theme';
  const btnId = 'theme-toggle';
  const body = document.documentElement; // toggle class on root for global effect

  function apply(theme){
    if(theme === 'light'){
      body.classList.add('theme-light');
      body.classList.remove('theme-dark');
    } else {
      body.classList.remove('theme-light');
      body.classList.add('theme-dark');
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
    const current = localStorage.getItem(KEY) || (body.classList.contains('theme-light') ? 'light' : 'dark');
    const next = current === 'light' ? 'dark' : 'light';
    localStorage.setItem(KEY, next);
    apply(next);
  }

  // initialize on DOMContentLoaded so button exists
  document.addEventListener('DOMContentLoaded', function(){
    const t = preferred();
    apply(t);
    const btn = document.getElementById(btnId);
    if(btn) btn.addEventListener('click', toggle);
  });
})();
