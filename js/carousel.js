(function () {
  const track = document.querySelector(".logo-carousel-track");
  if (!track) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const items = [...track.children];
  if (items.length < 2) return;

  items.forEach((item) => track.appendChild(item.cloneNode(true)));

  let offset = 0;
  const speed = 0.5;

  function step() {
    offset += speed;
    const half = track.scrollWidth / 2;
    if (offset >= half) offset = 0;
    track.style.transform = `translateX(-${offset}px)`;
    requestAnimationFrame(step);
  }

  requestAnimationFrame(step);
})();
