# /// script
# dependencies = []
# ///
"""Link preview image (Open Graph): white logo on Tinte, indigo dot field on the right."""
import re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # repository root
SRC, DIST, BUILD = ROOT / "src", ROOT / "dist", ROOT / "build"
P = str(DIST / "Captiv-Brand-Package") + "/"
lock = open(P + "02_logo/horizontal/captiv-logo-horizontal_weiss.svg").read()
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', lock).group(1).split()]
inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", lock, flags=re.S)
inner = re.sub(r"<title>.*?</title>", "", inner)
W, H = 1200, 630
lh = 104; s = lh / vb[3]; lw = vb[2] * s
x0, y0 = 96, (H - lh) / 2
dots = []
p = 30
for i in range(int(W / p) + 1):
    for j in range(int(H / p) + 1):
        x, y = i * p + p / 2, j * p + p / 2
        k = max(0.0, min(1.0, (x - 640) / 520))
        r = 12.6 * k ** 1.1
        if r > 0.4: dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#16122D"/>'
       f'<g fill="#3034C5">{"".join(dots)}</g>'
       f'<g transform="translate({x0} {y0}) scale({s}) translate({-vb[0]} {-vb[1]})">{inner}</g></svg>')
for path in (P + "05_anwendungen/og-bild_1200x630.svg",):
    open(path, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", "1200", "-o", path[:-4] + ".png", path], check=True)
    subprocess.run(["rsvg-convert", "-w", "2400", "-o", path[:-4] + "@2x.png", path], check=True)
print("ok", round(lw))
