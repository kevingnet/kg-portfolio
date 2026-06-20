/* Scroll page to trigger Wix lazy-loaded galleries and images. */
(async () => {
  const delay = (ms) => new Promise((r) => setTimeout(r, ms));
  const step = Math.max(400, Math.floor(window.innerHeight * 0.85));
  const maxY = Math.max(
    document.body.scrollHeight,
    document.documentElement.scrollHeight,
  );
  for (let y = 0; y <= maxY; y += step) {
    window.scrollTo(0, y);
    await delay(350);
  }
  window.scrollTo(0, 0);
  await delay(1500);
  // Nudge Wix pro-galleries / slideshows
  for (const btn of document.querySelectorAll(
    'button[aria-label*="Next"], button[aria-label*="next"], .slideshow-arrow',
  )) {
    try {
      btn.click();
      await delay(250);
    } catch (_) {}
  }
  await delay(2000);
})();
