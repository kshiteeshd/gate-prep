/* Typesets <span class="tex"> / <div class="texd"> elements with KaTeX (bundled, works offline). */
(() => {
  const draw = root => {
    if (!window.katex) return;
    (root || document).querySelectorAll('.tex:not(.done),.texd:not(.done)').forEach(el => {
      const src = el.getAttribute('data-tex') || el.textContent;
      try { katex.render(src, el, {displayMode: el.classList.contains('texd'), throwOnError: false, strict: 'ignore', trust: false, output: 'html'}); el.classList.add('done'); }
      catch (e) { el.classList.add('done'); }
    });
  };
  window.GPMath = {render: draw};
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => draw()); else draw();
})();
