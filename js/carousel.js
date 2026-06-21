(function () {
  function startCarousel() {
    const track = document.querySelector(".logo-carousel-track");
    if (!track || track.dataset.carouselInit === "1") return;

    const items = [...track.children];
    if (items.length < 2) return;

    track.dataset.carouselInit = "1";
    items.forEach((item) => track.appendChild(item.cloneNode(true)));

    let offset = 0;
    const speed = 0.5;

    function step() {
      const half = track.scrollWidth / 2;
      if (half > 1) {
        offset += speed;
        if (offset >= half) offset = 0;
        track.style.transform = "translateX(-" + offset + "px)";
      }
      requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  if (document.readyState === "complete") {
    startCarousel();
  } else {
    window.addEventListener("load", startCarousel, { once: true });
  }
})();
