(function(){
  const KEY = 'badsw-theme-test-override';
  const LEGACY_KEY = 'badsw-theme';
  const root = document.documentElement; // html element
  const lightPreference = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)');

  try{
    localStorage.removeItem(LEGACY_KEY);
  }catch(e){/* ignore */}

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
  }

  function preferred(){
    const stored = localStorage.getItem(KEY);
    if(stored) return stored;
    return lightPreference && lightPreference.matches ? 'light' : 'dark';
  }

  function setOverride(theme){
    if(theme === 'light' || theme === 'dark'){
      localStorage.setItem(KEY, theme);
      apply(theme);
      return theme;
    }

    localStorage.removeItem(KEY);
    apply(preferred());
    return 'system';
  }

  function toggle(){
    const current = localStorage.getItem(KEY) || preferred();
    const next = current === 'light' ? 'dark' : 'light';
    return setOverride(next);
  }

  // Apply immediately so variables take effect before paint (reduces flash)
  try{
    const testTheme = new URLSearchParams(window.location.search).get('theme');
    if(testTheme === 'light' || testTheme === 'dark' || testTheme === 'system'){
      setOverride(testTheme);
    } else {
      apply(preferred());
    }
  }catch(e){/* ignore */}

  if(lightPreference){
    const onPreferenceChange = function(){
      if(!localStorage.getItem(KEY)) apply(preferred());
    };

    if(lightPreference.addEventListener){
      lightPreference.addEventListener('change', onPreferenceChange);
    } else if(lightPreference.addListener){
      lightPreference.addListener(onPreferenceChange);
    }
  }

  window.badSoftwareTheme = {
    set: setOverride,
    toggle: toggle,
    system: function(){
      return setOverride('system');
    },
    current: function(){
      return root.getAttribute('data-theme');
    }
  };
})();
