/* The existing site.js owns all theme/language preferences; this file manages gallery browsing and the viewer. */
(() => {
  const grid = document.getElementById('galleryGrid');
  const artworks = [...document.querySelectorAll('.gallery-artwork')];
  const allLinks = [...document.querySelectorAll('[data-gallery-index]')];
  let links = allLinks;
  const filters = [...document.querySelectorAll('[data-gallery-filter]')];
  const viewOptions = [...document.querySelectorAll('[data-gallery-view]')];
  const empty = document.querySelector('.gallery-empty');
  if (grid) {
    document.querySelector('.gallery-toolbar').hidden = false;
    filters.forEach(button => button.addEventListener('click', () => {
      const category = button.dataset.galleryFilter;
      filters.forEach(option => option.setAttribute('aria-pressed', String(option === button)));
      artworks.forEach(artwork => {
        artwork.hidden = category !== 'all' && !artwork.dataset.categories.split(' ').includes(category);
      });
      links = allLinks.filter(link => !link.closest('.gallery-artwork').hidden);
      empty.hidden = links.length > 0;
      document.dispatchEvent(new Event('studio:content-resize'));
    }));
    viewOptions.forEach(button => button.addEventListener('click', () => {
      grid.dataset.view = button.dataset.galleryView;
      viewOptions.forEach(option => option.setAttribute('aria-pressed', String(option === button)));
      document.dispatchEvent(new Event('studio:content-resize'));
    }));
  }
  const dialog = document.getElementById('galleryViewer');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('galleryViewerImage');
  const title = document.getElementById('galleryViewerTitle');
  const position = document.getElementById('galleryViewerPosition');
  const error = dialog.querySelector('.gallery-viewer-error');
  const closeButton = dialog.querySelector('[data-viewer-close]');
  let current = 0;
  let opener = null;
  let savedBodyStyle = null;
  let scrollY = 0;

  function updatePosition() {
    const template = document.getElementById('galleryPositionTemplate').textContent;
    position.textContent = template.replace('{current}', current + 1).replace('{total}', links.length);
  }

  function showArtwork(index) {
    current = (index + links.length) % links.length;
    const source = links[current].querySelector('img');
    title.textContent = source.alt;
    image.hidden = true;
    error.hidden = true;
    image.alt = source.alt;
    image.src = links[current].href;
    updatePosition();
  }

  image.addEventListener('load', () => { image.hidden = false; });
  image.addEventListener('error', () => { image.hidden = true; error.hidden = false; });

  function openViewer(index, link) {
    if (dialog.open) return;
    opener = link;
    scrollY = window.scrollY;
    savedBodyStyle = document.body.getAttribute('style');
    const gutter = window.innerWidth - document.documentElement.clientWidth;
    // Fix the background at its current position, including on mobile Safari.
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollY}px`;
    document.body.style.left = '0';
    document.body.style.right = `${gutter}px`;
    document.documentElement.classList.add('gallery-viewing');
    showArtwork(index);
    dialog.showModal();
    closeButton.focus({ preventScroll: true });
  }

  allLinks.forEach(link => {
    link.addEventListener('click', event => {
      // Retain the normal original-image link for modifier clicks or without JS.
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      openViewer(links.indexOf(link), link);
    });
  });
  closeButton.addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-viewer-previous]').addEventListener('click', () => showArtwork(current - 1));
  dialog.querySelector('[data-viewer-next]').addEventListener('click', () => showArtwork(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'Tab') {
      const controls = [...dialog.querySelectorAll('button:not([disabled])')];
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showArtwork(current + (event.key === 'ArrowLeft' ? -1 : 1));
    }
    // Escape uses the native dialog cancel/close behavior.
  });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('gallery-viewing');
    if (savedBodyStyle === null) document.body.removeAttribute('style');
    else document.body.setAttribute('style', savedBodyStyle);
    window.scrollTo({ top: scrollY, behavior: 'instant' });
    opener?.focus({ preventScroll: true });
    document.dispatchEvent(new Event('studio:content-resize'));
  });
  document.addEventListener('studio:language-change', () => {
    document.title = `${document.getElementById('gallery-title').textContent} — Qihang Studio`;
    if (dialog.open) updatePosition();
  });
})();
