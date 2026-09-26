(function () {
  // Hide embedded PDF panels whose file is not on the server, instead of
  // showing an empty viewer (or GitHub's 404 page inside it).
  if (!/^https?:$/.test(location.protocol)) return;
  document.querySelectorAll(".archive-pdf-embed object[data]").forEach((obj) => {
    const panel = obj.closest(".archive-panel") || obj.closest(".archive-pdf-embed");
    panel.style.display = "none";
    fetch(obj.getAttribute("data"), { method: "HEAD" })
      .then((res) => {
        if (res.ok) panel.style.display = "";
      })
      .catch(() => {});
  });
})();

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
