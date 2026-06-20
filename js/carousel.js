(function () {
  const track = document.querySelector(".logo-carousel-track");
  if (!track) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const items = [...track.children];
  if (items.length < 2 || reduced) return;

  items.forEach((item) => track.appendChild(item.cloneNode(true)));

  let offset = 0;
  let speed = 0.45;
  let paused = false;

  track.closest(".logo-carousel")?.addEventListener("mouseenter", () => {
    paused = true;
  });
  track.closest(".logo-carousel")?.addEventListener("mouseleave", () => {
    paused = false;
  });

  function step() {
    if (!paused) {
      offset += speed;
      const half = track.scrollWidth / 2;
      if (offset >= half) offset = 0;
      track.style.transform = "translateX(-" + offset + "px)";
    }
    requestAnimationFrame(step);
  }

  requestAnimationFrame(step);
})();
