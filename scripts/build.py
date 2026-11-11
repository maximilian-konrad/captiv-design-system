# /// script
# dependencies = []
# ///
"""Builds the Captiv logo package (SVG sources, then PDF/PNG/ICO via rsvg-convert)."""
import json, math, os, shutil, subprocess, struct
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # repository root
SRC, DIST, BUILD = ROOT / "src", ROOT / "dist", ROOT / "build"

OUT = str(DIST / "Captiv-Brand-Package")
PITCH = 58.0
RMAX, RMIN = 0.90 * PITCH / 2, 0.40 * PITCH / 2   # diameter 90 % and 40 % of the grid pitch

COL = {
    "indigo": "#3034C5", "tinte": "#16122D", "lavendel": "#A1A1F0", "schiefer": "#706C7E",
    "nebel": "#E9E6E0", "papier": "#F8F6F2", "weiss": "#FFFFFF",
}

P = [[90,222],[90,280],[90,338],[90,396],[90,454],[90,512],[90,570],[148,164],[148,222],[148,280],[148,338],[148,396],[148,454],[148,512],[148,570],[148,628],[206,106],[206,164],[206,222],[206,280],[206,338],[206,396],[206,454],[206,512],[206,570],[206,628],[206,686],[264,48],[264,106],[264,164],[264,222],[264,570],[264,628],[264,686],[264,744],[322,48],[322,106],[322,164],[322,628],[322,686],[322,744],[380,48],[380,106],[380,164],[380,628],[380,686],[380,744],[438,48],[438,106],[438,164],[438,628],[438,686],[438,744],[496,48],[496,106],[496,164],[496,222],[496,570],[496,628],[496,686],[496,744],[554,106],[554,164],[554,222],[554,280],[554,512],[554,570],[554,628],[554,686],[612,106],[612,164],[612,222],[612,280],[612,512],[612,570],[612,628],[612,686],[670,164],[670,222],[670,280],[670,512],[670,570]]

def r_of(x):  # fade: large on the left, small towards the opening
    k = 1 - (x - 90) / 580
    return RMIN + (RMAX - RMIN) * k

DOTS = [(x, y, r_of(x)) for x, y in P]
BX0 = min(x - r for x, y, r in DOTS); BX1 = max(x + r for x, y, r in DOTS)
BY0 = min(y - r for x, y, r in DOTS); BY1 = max(y + r for x, y, r in DOTS)
MW, MH = BX1 - BX0, BY1 - BY0

def f(v): return f"{v:.2f}".rstrip("0").rstrip(".")

def mark_g(fill, tx=0.0, ty=0.0, s=1.0):
    c = "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in DOTS)
    return f'<g fill="{fill}" transform="translate({f(tx)} {f(ty)}) scale({s}) translate({f(-BX0)} {f(-BY0)})">{c}</g>'

WM = json.load(open(SRC / "wordmark.json"))
WX0, WY0, WX1, WY1 = WM["bounds"]          # font units, y up
CAP = WM["cap"]

def word_g(fill, tx, ty, s):  # ty = baseline
    return f'<g fill="{fill}" transform="translate({f(tx)} {f(ty)}) scale({s}) translate({f(-WX0)} 0)"><path d="{WM["d"]}"/></g>'

def svg(w, h, body, bg=None, title="Captiv"):
    b = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}">'
            f'<title>{title}</title>{b}{body}</svg>\n')

def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content); return p

def export(p, pdf=True, pngs=()):
    base = p[:-4]
    if pdf: subprocess.run(["rsvg-convert", "-f", "pdf", "-o", base + ".pdf", p], check=True)
    for w in pngs:
        subprocess.run(["rsvg-convert", "-w", str(w), "-o", f"{base}_{w}px.png", p], check=True)

# ---------------------------------------------------------------- 01 Zeichen
VARIANTS = [("tinte", COL["tinte"]), ("indigo", COL["indigo"]), ("weiss", "#FFFFFF"), ("schwarz", "#000000")]
for name, c in VARIANTS:
    p = write(f"01_zeichen/captiv-zeichen_{name}.svg", svg(MW, MH, mark_g(c), title="Captiv Zeichen"))
    export(p, pngs=(256, 1024, 2048))
# with clear space (1 pitch on each side) on backgrounds
PAD = PITCH * 1.5
for name, fg, bg in [("tinte-auf-papier", COL["tinte"], COL["papier"]), ("indigo-auf-papier", COL["indigo"], COL["papier"]), ("weiss-auf-indigo", "#FFFFFF", COL["indigo"]), ("weiss-auf-tinte", "#FFFFFF", COL["tinte"])]:
    S = max(MW, MH) + 2 * PAD
    p = write(f"01_zeichen/flaeche/captiv-zeichen_{name}.svg", svg(S, S, mark_g(fg, (S - MW) / 2, (S - MH) / 2), bg=bg))
    export(p, pngs=(1024,))

# ---------------------------------------------------------------- 02 Logo (Zeichen + Wortmarke)
# Wordmark cap height = 50 % of mark height, gap = 2.5 grid pitches, both vertically centred.
def lockup_h(fg, bg=None):
    s = (MH * 0.55) / CAP
    gap = PITCH * 4
    ww = (WX1 - WX0) * s
    W = MW + gap + ww
    base = MH / 2 + CAP * s / 2
    desc = -WY0 * s
    H = max(MH, base + desc)
    body = mark_g(fg) + word_g(fg, MW + gap, base, s)
    return W, H, body

def lockup_v(fg):
    s = (MH * 0.30) / CAP
    ww = (WX1 - WX0) * s
    gap = PITCH * 1.6
    W = max(MW, ww)
    base = MH + gap + CAP * s
    H = base - WY0 * s
    body = mark_g(fg, (W - MW) / 2, 0) + word_g(fg, (W - ww) / 2, base, s)
    return W, H, body

for name, c in VARIANTS[:3] + VARIANTS[3:]:
    W, H, body = lockup_h(c)
    export(write(f"02_logo/horizontal/captiv-logo-horizontal_{name}.svg", svg(W, H, body, title="Captiv Logo")), pngs=(800, 2400))
    W, H, body = lockup_v(c)
    export(write(f"02_logo/gestapelt/captiv-logo-gestapelt_{name}.svg", svg(W, H, body, title="Captiv Logo")), pngs=(600, 1800))
    # wordmark alone
    s = 1.0
    ww, wh = (WX1 - WX0), (WY1 - WY0)
    export(write(f"02_logo/wortmarke/captiv-wortmarke_{name}.svg", svg(ww, wh, word_g(c, 0, WY1, 1), title="Captiv Wortmarke")), pngs=(800,))

for name, fg, bg in [("tinte-auf-papier", COL["tinte"], COL["papier"]), ("tinte-auf-weiss", COL["tinte"], "#FFFFFF"), ("weiss-auf-indigo", "#FFFFFF", COL["indigo"]), ("weiss-auf-tinte", "#FFFFFF", COL["tinte"])]:
    W, H, body = lockup_h(fg)
    pad = MH * 0.5
    export(write(f"02_logo/flaeche/captiv-logo-horizontal_{name}.svg", svg(W + 2 * pad, H + 2 * pad, f'<g transform="translate({f(pad)} {f(pad)})">{body}</g>', bg=bg)), pngs=(1600,))

# ---------------------------------------------------------------- 03 Icons
def icon(fg, bg, radius_ratio=0.22, scale=0.66, S=1024):
    s = S * scale / max(MW, MH)
    tx, ty = (S - MW * s) / 2, (S - MH * s) / 2
    rr = S * radius_ratio
    return svg(S, S, f'<rect width="{S}" height="{S}" rx="{f(rr)}" fill="{bg}"/>' + mark_g(fg, tx, ty, s), title="Captiv Icon")

icons = {"weiss-auf-indigo": ("#FFFFFF", COL["indigo"]), "weiss-auf-tinte": ("#FFFFFF", COL["tinte"]),
         "indigo-auf-papier": (COL["indigo"], COL["papier"]), "tinte-auf-papier": (COL["tinte"], COL["papier"]),
         "tinte-auf-weiss": (COL["tinte"], "#FFFFFF")}
for name, (fg, bg) in icons.items():
    export(write(f"03_icons/app-icon_{name}.svg", icon(fg, bg)), pngs=(180, 512, 1024))
    # square (no radius) for platforms that crop themselves (LinkedIn, Google, etc.)
    export(write(f"03_icons/profilbild_{name}.svg", icon(fg, bg, radius_ratio=0, scale=0.58)), pdf=False, pngs=(400, 800))
# favicon: slightly larger mark on graphit tile
fav = write("03_icons/favicon/favicon.svg", icon("#FFFFFF", COL["tinte"], radius_ratio=0.2, scale=0.78, S=64))
favdir = os.path.dirname(fav)
pngs = []
for w in (16, 32, 48, 180, 192, 512):
    o = os.path.join(favdir, f"favicon-{w}.png" if w not in (180,) else "apple-touch-icon.png")
    subprocess.run(["rsvg-convert", "-w", str(w), "-o", o, fav], check=True)
    if w in (16, 32, 48): pngs.append((w, o))
# multi-size ICO with embedded PNGs
data = [open(o, "rb").read() for _, o in pngs]
hdr = struct.pack("<HHH", 0, 1, len(data)); off = 6 + 16 * len(data); ent = b""
for (w, _), d in zip(pngs, data):
    ent += struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(d), off); off += len(d)
open(os.path.join(favdir, "favicon.ico"), "wb").write(hdr + ent + b"".join(data))

# ---------------------------------------------------------------- 04 Stilelemente
def field(cols, rows, kfun, fg, pitch=PITCH, bg=None, rmin=RMIN, rmax=RMAX, pad=None):
    pad = pitch / 2 if pad is None else pad
    W, H = cols * pitch, rows * pitch
    cs = []
    for j in range(rows):
        for i in range(cols):
            k = kfun(i / max(cols - 1, 1), j / max(rows - 1, 1), i, j)
            if k is None: continue
            r = rmin + (rmax - rmin) * k
            if r <= 0.3: continue
            cs.append(f'<circle cx="{f(pad + i * pitch)}" cy="{f(pad + j * pitch)}" r="{f(r)}"/>')
    return W, H, f'<g fill="{fg}">{"".join(cs)}</g>'

E = "04_stilelemente"
# (a) single dot, the base unit, with grid
write(f"{E}/punkt_einzeln.svg", svg(PITCH, PITCH, f'<circle cx="{PITCH/2}" cy="{PITCH/2}" r="{f(RMAX)}" fill="{COL["tinte"]}"/>', title="Punkt 90 %"))
write(f"{E}/punkt_einzeln_klein.svg", svg(PITCH, PITCH, f'<circle cx="{PITCH/2}" cy="{PITCH/2}" r="{f(RMIN)}" fill="{COL["tinte"]}"/>', title="Punkt 40 %"))
# (b) seamless pattern tiles (one dot per tile, uniform), 90 % and 40 %
for pct in (90, 40, 20):
    r = pct / 100 * PITCH / 2
    for name, c in (("tinte", COL["tinte"]), ("indigo", COL["indigo"]), ("schiefer", COL["schiefer"]), ("weiss", "#FFFFFF")):
        write(f"{E}/muster-kachel/raster-kachel_{pct}_{name}.svg", svg(PITCH, PITCH, f'<circle cx="{PITCH/2}" cy="{PITCH/2}" r="{f(r)}" fill="{c}"/>', title=f"Rasterkachel {pct} %"))
# (c) fields: fade horizontal, fade vertical, zoom radial, fade to zero (dissolve)
fields = {
    "verlauf-horizontal": (24, 8, lambda u, v, i, j: 1 - u),
    "verlauf-vertikal": (8, 24, lambda u, v, i, j: 1 - v),
    "verlauf-diagonal": (20, 12, lambda u, v, i, j: 1 - (u + v) / 2),
    "zoom-radial": (17, 17, lambda u, v, i, j: math.hypot(u - .5, v - .5) / math.hypot(.5, .5)),
    "zoom-radial-invers": (17, 17, lambda u, v, i, j: 1 - math.hypot(u - .5, v - .5) / math.hypot(.5, .5)),
}
for name, (c_, r_, kf) in fields.items():
    for cn, fg in (("tinte", COL["tinte"]), ("indigo", COL["indigo"]), ("lavendel", COL["lavendel"]), ("weiss", "#FFFFFF")):
        W, H, body = field(c_, r_, kf, fg)
        export(write(f"{E}/punktfelder/{name}_{cn}.svg", svg(W, H, body, title=name)), pngs=(1600,))
# dissolve: 90 % down to nothing (for edges of slides and banners)
for cn, fg in (("tinte", COL["tinte"]), ("indigo", COL["indigo"]), ("lavendel", COL["lavendel"]), ("weiss", "#FFFFFF")):
    W, H, body = field(24, 8, lambda u, v, i, j: 1 - u, fg, rmin=0)
    export(write(f"{E}/punktfelder/aufloesung-horizontal_{cn}.svg", svg(W, H, body, title="Auflösung")), pngs=(1600,))
# (d) divider: one row fading 90 to 40 % and 90 % to 0
for cn, fg in (("tinte", COL["tinte"]), ("indigo", COL["indigo"]), ("lavendel", COL["lavendel"]), ("weiss", "#FFFFFF")):
    W, H, body = field(16, 1, lambda u, v, i, j: 1 - u, fg)
    write(f"{E}/trenner/punkt-trenner_{cn}.svg", svg(W, H, body, title="Trenner"))
    W, H, body = field(16, 1, lambda u, v, i, j: 1 - u, fg, rmin=0)
    write(f"{E}/trenner/punkt-trenner-aufloesend_{cn}.svg", svg(W, H, body, title="Trenner"))
    W, H, body = field(3, 1, lambda u, v, i, j: 1 - u, fg)
    write(f"{E}/trenner/aufzaehlungspunkte-3_{cn}.svg", svg(W, H, body, title="Drei Punkte"))
# (e) mark as ghost / watermark (outline grid + mark), big and tonal on graphit
gp = PITCH * 2
gs = "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(0.2*PITCH/2)}"/>' for x in [90 + PITCH*i for i in range(-2, 13)] for y in [48 + PITCH*j for j in range(-2, 16)])
GW, GH = MW + 2*gp, MH + 2*gp
ghost = f'<g transform="translate({f(gp - BX0)} {f(gp - BY0)})"><g fill="{COL["lavendel"]}" opacity="0.45">{gs}</g></g>' + mark_g("#FFFFFF", gp, gp)
export(write(f"{E}/zeichen-im-raster_indigo.svg", svg(GW, GH, ghost, bg=COL["indigo"], title="Zeichen im Raster")), pngs=(1600,))

# ---------------------------------------------------------------- 05 Anwendungen
A = "05_anwendungen"
def banner(Wt, Ht, fg, bg, logo_h_ratio, field_cols=None, name="", accent=None):
    W, H, body = lockup_h(fg)
    s = Ht * logo_h_ratio / H
    tx, ty = Ht * 0.16 if Wt / Ht > 3 else Wt * 0.08, (Ht - H * s) / 2
    pitch = Ht / 7
    cols = int(Wt * 0.48 / pitch); rows = 7
    fw, fh, fb = field(cols, rows, lambda u, v, i, j: u, accent or COL["schiefer"], pitch=pitch, rmin=0, rmax=0.9 * pitch / 2, pad=pitch / 2)
    fx = Wt - cols * pitch
    fgp = f'<g transform="translate({f(fx)} 0)" opacity="0.9">{fb}</g>'
    return svg(Wt, Ht, fgp + f'<g transform="translate({f(tx)} {f(ty)}) scale({s})">{body}</g>', bg=bg, title=name)
for nm, (Wt, Ht, ratio) in {"linkedin-banner_1584x396": (1584, 396, 0.26), "og-bild_1200x630": (1200, 630, 0.17), "x-banner_1500x500": (1500, 500, 0.24)}.items():
    p = write(f"{A}/{nm}.svg", banner(Wt, Ht, COL["tinte"], COL["papier"], ratio, name=nm, accent=COL["indigo"]))
    subprocess.run(["rsvg-convert", "-w", str(Wt * 2), "-o", p[:-4] + "@2x.png", p], check=True)
    subprocess.run(["rsvg-convert", "-w", str(Wt), "-o", p[:-4] + ".png", p], check=True)
# e-mail signature logo (PNG 2x, horizontal tinte)
W, H, body = lockup_h(COL["tinte"])
p = write(f"{A}/email-signatur_logo.svg", svg(W, H, body))
subprocess.run(["rsvg-convert", "-h", "64", "-o", p[:-4] + "_32px@2x.png", p], check=True)

# ---------------------------------------------------------------- 06 Farben
pal = [("Indigo", "indigo", "Markenfarbe: Akzente, Links, Buttons, Charts"), ("Tinte", "tinte", "Schrift, Logo, dunkle Flächen"),
       ("Lavendel", "lavendel", "Zweitfarbe: Charts, Flächen, Highlights"), ("Schiefer", "schiefer", "Sekundärtext, Linien, Achsen"),
       ("Nebel", "nebel", "Helle Flächen, Boxen, Tabellenzeilen"), ("Papier", "papier", "Grundfläche Website und Dokumente"),
       ("Weiß", "weiss", "Grundfläche Slides, Logo auf dunklem Grund")]
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def cmyk(h):
    r, g, b = [c / 255 for c in rgb(h)]; k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(v * 100) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))
os.makedirs(os.path.join(OUT, "06_farben"), exist_ok=True)
json.dump({n: {"hex": COL[k], "rgb": rgb(COL[k]), "cmyk_naeherung": cmyk(COL[k]), "verwendung": u} for n, k, u in pal},
          open(os.path.join(OUT, "06_farben/farben.json"), "w"), indent=2, ensure_ascii=False)
css = ":root {\n" + "".join(f"  --captiv-{k}: {COL[k]};\n" for _, k, _ in pal) + "}\n"
open(os.path.join(OUT, "06_farben/farben.css"), "w").write(css)
sw = "".join(f'<rect x="{i*200}" y="0" width="200" height="200" fill="{COL[k]}"/>' for i, (_, k, _) in enumerate(pal))
write("06_farben/farbpalette.svg", svg(200 * len(pal), 200, sw, title="Farbpalette"))

# ---------------------------------------------------------------- 07 Schrift


# metadata for the overview sheet
BUILD.mkdir(exist_ok=True)
json.dump({"MW": MW, "MH": MH, "RMAX": RMAX, "RMIN": RMIN, "PITCH": PITCH, "pal": [(n, COL[k], u, rgb(COL[k]), cmyk(COL[k])) for n, k, u in pal]}, open(BUILD / "meta.json", "w"))
print("ok", MW, MH)
