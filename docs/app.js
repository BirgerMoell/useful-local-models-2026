const canvas = document.getElementById("traceCanvas");
const ctx = canvas.getContext("2d");
let width = 0;
let height = 0;
let points = [];

function resize() {
  const ratio = window.devicePixelRatio || 1;
  width = canvas.clientWidth;
  height = canvas.clientHeight;
  canvas.width = Math.floor(width * ratio);
  canvas.height = Math.floor(height * ratio);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  points = Array.from({ length: 42 }, (_, i) => ({
    x: width * (0.38 + Math.random() * 0.58),
    y: height * (0.12 + Math.random() * 0.78),
    r: 1.6 + Math.random() * 3.4,
    phase: Math.random() * Math.PI * 2,
    speed: 0.003 + Math.random() * 0.006,
    hue: i % 3,
  }));
}

function colorFor(index, alpha) {
  if (index === 0) return `rgba(43, 179, 163, ${alpha})`;
  if (index === 1) return `rgba(241, 109, 79, ${alpha})`;
  return `rgba(182, 212, 85, ${alpha})`;
}

function draw(time) {
  ctx.clearRect(0, 0, width, height);

  ctx.save();
  ctx.globalCompositeOperation = "screen";
  [
    { y: 0.2, amp: 46, speed: 0.0015, color: [43, 179, 163], phase: 0 },
    { y: 0.37, amp: 62, speed: 0.0011, color: [91, 92, 226], phase: 1.9 },
    { y: 0.55, amp: 52, speed: 0.0018, color: [241, 109, 79], phase: 3.1 },
  ].forEach((band) => {
    const gradient = ctx.createLinearGradient(width * 0.3, 0, width, 0);
    gradient.addColorStop(0, `rgba(${band.color[0]}, ${band.color[1]}, ${band.color[2]}, 0)`);
    gradient.addColorStop(0.48, `rgba(${band.color[0]}, ${band.color[1]}, ${band.color[2]}, 0.22)`);
    gradient.addColorStop(1, `rgba(${band.color[0]}, ${band.color[1]}, ${band.color[2]}, 0.02)`);
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 16;
    ctx.shadowBlur = 24;
    ctx.shadowColor = `rgba(${band.color[0]}, ${band.color[1]}, ${band.color[2]}, 0.38)`;
    ctx.beginPath();
    for (let i = 0; i <= 150; i += 1) {
      const t = i / 150;
      const x = width * (0.28 + t * 0.86);
      const wave = Math.sin(t * Math.PI * 3.1 + time * band.speed + band.phase);
      const fine = Math.sin(t * Math.PI * 11 + time * band.speed * 2.2 + band.phase) * 0.32;
      const y = height * band.y + (wave + fine) * band.amp;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  });
  ctx.restore();

  const grid = 68;
  ctx.strokeStyle = "rgba(255, 253, 248, 0.055)";
  ctx.lineWidth = 1;
  for (let x = width * 0.34; x < width; x += grid) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y < height; y += grid) {
    ctx.beginPath();
    ctx.moveTo(width * 0.34, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }

  points.forEach((point, i) => {
    const drift = Math.sin(time * point.speed + point.phase) * 10;
    const x = point.x + drift;
    const y = point.y + Math.cos(time * point.speed * 0.8 + point.phase) * 8;

    for (let j = i + 1; j < points.length; j += 7) {
      const other = points[j];
      const ox = other.x + Math.sin(time * other.speed + other.phase) * 10;
      const oy = other.y + Math.cos(time * other.speed * 0.8 + other.phase) * 8;
      const dx = x - ox;
      const dy = y - oy;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 210) {
        ctx.strokeStyle = colorFor(point.hue, Math.max(0.03, 0.16 - dist / 1400));
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(ox, oy);
        ctx.stroke();
      }
    }

    ctx.fillStyle = colorFor(point.hue, 0.82);
    ctx.beginPath();
    ctx.arc(x, y, point.r, 0, Math.PI * 2);
    ctx.fill();
  });

  const chartX = width * 0.58;
  const chartY = height * 0.7;
  ctx.strokeStyle = "rgba(255, 253, 248, 0.42)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i < 120; i++) {
    const x = chartX + i * 4;
    const decay = Math.exp(-i / 52);
    const wobble = Math.sin(i * 0.32 + time * 0.004) * 8;
    const y = chartY - 110 + decay * 130 + wobble;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  requestAnimationFrame(draw);
}

if (canvas) {
  window.addEventListener("resize", resize);
  resize();
  requestAnimationFrame(draw);
}

document.querySelectorAll(".copy-line").forEach((button) => {
  button.addEventListener("click", async () => {
    const text = button.getAttribute("data-copy") || button.textContent.trim();
    try {
      await navigator.clipboard.writeText(text);
      button.classList.add("copied");
      window.setTimeout(() => button.classList.remove("copied"), 900);
    } catch {
      button.classList.add("copied");
      window.setTimeout(() => button.classList.remove("copied"), 900);
    }
  });
});
