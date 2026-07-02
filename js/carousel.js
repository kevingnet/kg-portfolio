(function () {
  const STORAGE_KEY = "kg-portfolio-carousel-v2";
  const HASH_PREFIX = "kg-carousel=";
  const SPEED = 0.5;
  const FRAME_MS = 1000 / 60;

  function parsePayload(raw) {
    if (!raw) return null;
    const parts = String(raw).split(",");
    const ratio = parseFloat(parts[0]);
    const ts = parseFloat(parts[1]);
    if (!Number.isFinite(ratio) || ratio < 0) return null;
    return {
      ratio: ratio % 1,
      ts: Number.isFinite(ts) && ts > 0 ? ts : performance.now(),
    };
  }

  function readFromHash() {
    const hash = window.location.hash || "";
    const idx = hash.indexOf(HASH_PREFIX);
    if (idx === -1) return null;
    const end = hash.indexOf("&", idx);
    const raw = hash.slice(idx + HASH_PREFIX.length, end === -1 ? undefined : end);
    return parsePayload(decodeURIComponent(raw));
  }

  function readFromStorage() {
    for (const store of [sessionStorage, localStorage]) {
      try {
        const parsed = parsePayload(store.getItem(STORAGE_KEY));
        if (parsed) return parsed;
      } catch (e) {
        /* private mode */
      }
    }
    return null;
  }

  function clearHash() {
    if (!window.location.hash.includes(HASH_PREFIX)) return;
    try {
      window.history.replaceState(null, "", window.location.pathname + window.location.search);
    } catch (e) {
      /* ignore */
    }
  }

  function writeState(ratio, ts) {
    const payload = (ratio % 1).toFixed(6) + "," + Math.round(ts);
    try {
      sessionStorage.setItem(STORAGE_KEY, payload);
    } catch (e) {
      /* ignore */
    }
    try {
      localStorage.setItem(STORAGE_KEY, payload);
    } catch (e) {
      /* ignore */
    }
  }

  function advanceRatio(state, half) {
    if (!state || half <= 1) return 0;
    let ratio = state.ratio % 1;
    if (ratio < 0) ratio += 1;
    const frames = Math.max(0, (performance.now() - state.ts) / FRAME_MS);
    ratio = (ratio + (frames * SPEED) / half) % 1;
    return ratio;
  }

  function startCarousel() {
    const carousel = document.querySelector(".logo-carousel");
    const track = document.querySelector(".logo-carousel-track");
    if (!track || track.dataset.carouselInit === "1") return;

    const items = [...track.children];
    if (items.length < 2) return;

    track.dataset.carouselInit = "1";
    items.forEach((item) => track.appendChild(item.cloneNode(true)));

    const bootState = readFromHash() || readFromStorage();
    clearHash();

    let ratio = 0;
    let paused = false;
    let lastSave = 0;
    let hasBooted = false;

    function halfWidth() {
      return track.scrollWidth / 2;
    }

    function render() {
      const half = halfWidth();
      if (!hasBooted && bootState && half > 1) {
        ratio = advanceRatio(bootState, half);
        hasBooted = true;
      }
      if (half > 1) {
        const offset = (ratio % 1) * half;
        track.style.transform = "translateX(-" + offset + "px)";
      }
      return half;
    }

    function persist(force) {
      const t = performance.now();
      if (!force && t - lastSave < 200) return;
      lastSave = t;
      writeState(ratio, t);
    }

    function navHashForLink(link) {
      const half = halfWidth();
      if (half > 1) {
        ratio = (ratio % 1 + 1) % 1;
      }
      const ts = Math.round(performance.now());
      persist(true);
      const base = (link.getAttribute("href") || link.href || "").split("#")[0];
      if (!base) return;
      link.setAttribute(
        "href",
        base + "#" + HASH_PREFIX + ratio.toFixed(6) + "," + ts
      );
    }

    render();

    window.addEventListener("load", render);
    if (typeof ResizeObserver !== "undefined") {
      let resizeTimer = 0;
      new ResizeObserver(() => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(render, 50);
      }).observe(track);
    }

    function setPaused(value) {
      if (paused === value) return;
      paused = value;
      if (carousel) {
        carousel.classList.toggle("logo-carousel--paused", paused);
      }
      persist(true);
    }

    if (carousel) {
      carousel.addEventListener("mouseenter", () => setPaused(true));
      carousel.addEventListener("mouseleave", () => setPaused(false));
      carousel.addEventListener("focusin", () => setPaused(true));
      carousel.addEventListener("focusout", (e) => {
        if (!carousel.contains(e.relatedTarget)) setPaused(false);
      });
    }

    track.querySelectorAll("a.logo-carousel-link").forEach((link) => {
      const prime = () => navHashForLink(link);
      link.addEventListener("mousedown", prime);
      link.addEventListener("touchstart", prime, { passive: true });
      link.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") prime();
      });
      link.addEventListener("click", prime);
    });

    window.addEventListener("pagehide", () => persist(true));

    function step() {
      const half = render();
      if (!paused && half > 1) {
        ratio = (ratio + SPEED / half) % 1;
        const offset = ratio * half;
        track.style.transform = "translateX(-" + offset + "px)";
        persist(false);
      }
      requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startCarousel, { once: true });
  } else {
    startCarousel();
  }
})();
