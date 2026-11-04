/* A native button keeps Enter/Space, focus and expanded state accessible. */
(() => {
  const button = document.getElementById('artCollectionToggle');
  const panel = document.getElementById('artCollectionPanel');
  if (!button || !panel) return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let animation;
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    const startHeight = panel.hidden ? 0 : panel.getBoundingClientRect().height;
    animation?.cancel();
    button.setAttribute('aria-expanded', String(open));
    button.querySelector('.collection-indicator').textContent = open ? '−' : '+';
    panel.hidden = false;
    panel.inert = !open;
    const finish = () => {
      panel.hidden = !open;
      document.dispatchEvent(new Event('studio:content-resize'));
    };
    if (reducedMotion.matches || !panel.animate) {
      finish();
      return;
    }
    animation = panel.animate([
      { height: `${startHeight}px` },
      { height: `${open ? panel.scrollHeight : 0}px` }
    ], { duration: 240, easing: 'ease-in-out' });
    animation.onfinish = finish;
  });
})();
