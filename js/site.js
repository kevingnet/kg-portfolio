(function () {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) {
    document.querySelectorAll(".fade-in").forEach((el) => el.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
  );

  document.querySelectorAll(".fade-in").forEach((el) => observer.observe(el));

  document.querySelectorAll("[data-copy-email]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const email = btn.getAttribute("data-copy-email");
      if (!email || !navigator.clipboard) return;
      navigator.clipboard.writeText(email).then(() => {
        const prev = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => {
          btn.textContent = prev;
        }, 1600);
      });
    });
  });

  if (window.hljs) {
    document.querySelectorAll("pre.archive-code code").forEach((block) => {
      hljs.highlightElement(block);
    });
  }
})();
