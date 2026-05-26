const deck = document.querySelector(".deck");
const slides = Array.from(document.querySelectorAll(".slide"));

function currentIndex() {
  const scrollTop = deck.scrollTop;
  let best = 0;
  let bestDistance = Infinity;
  slides.forEach((slide, index) => {
    const distance = Math.abs(slide.offsetTop - scrollTop);
    if (distance < bestDistance) {
      best = index;
      bestDistance = distance;
    }
  });
  return best;
}

function go(delta) {
  const next = Math.max(0, Math.min(slides.length - 1, currentIndex() + delta));
  slides[next].scrollIntoView({ behavior: "smooth" });
}

document.addEventListener("keydown", (event) => {
  if (["ArrowRight", "ArrowDown", "PageDown", " "].includes(event.key)) {
    event.preventDefault();
    go(1);
  }
  if (["ArrowLeft", "ArrowUp", "PageUp"].includes(event.key)) {
    event.preventDefault();
    go(-1);
  }
});

document.querySelector("[data-prev]")?.addEventListener("click", () => go(-1));
document.querySelector("[data-next]")?.addEventListener("click", () => go(1));

