/* Content lives in inert HTML templates, so local-file previews need no fetch.
   site.js remains the single source of language preferences and menu behavior. */
(() => {
  const article = document.querySelector('[data-multilingual-essay]');
  if (!article) return;
  const title = article.querySelector('h1');
  const body = article.querySelector('.essay-body');
  document.addEventListener('studio:language-change', ({ detail }) => {
    const template = document.querySelector(`template[data-essay-language="${detail.language}"]`);
    if (!template) return;
    const content = template.content;
    title.replaceChildren(...content.querySelector('h1').cloneNode(true).childNodes);
    title.lang = detail.tag;
    body.replaceChildren(...content.querySelector('.essay-body').cloneNode(true).childNodes);
    body.lang = detail.tag;
    article.lang = detail.tag;
    document.title = `${title.textContent} — Qihang Studio`;
    article.hidden = false;
  });
})();
