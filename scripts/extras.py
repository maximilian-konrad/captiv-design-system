# /// script
# dependencies = ["fonttools", "brotli"]
# ///
"""Colour files (shades, Office theme, Adobe swatches, tokens) and the Geist font files for the brand package."""
import json, os, shutil, struct
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # repository root
SRC, DIST, BUILD = ROOT / "src", ROOT / "dist", ROOT / "build"
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
OUT = str(DIST / "Captiv-Brand-Package") + "/"
PAL = [("Indigo", "#3034C5", "Markenfarbe: Akzente, Links, Buttons, erste Chartfarbe"), ("Tinte", "#16122D", "Überschriften, Logo, Hintergrund dunkler Folien"),
       ("Graphit", "#434054", "Fließtext auf Website und in Office"), ("Indigo tief", "#1A1B6F", "Zweite dunkle Fläche, Text 2 im hellen Master"),
       ("Lavendel", "#A1A1F0", "Zweitfarbe: Charts, Flächen, Highlights"), ("Schiefer", "#706C7E", "Gedämpfter Text, Quellen, Achsen, Sonstige in Charts"),
       ("Nebel", "#E9E6E0", "Helle Flächen, Boxen, Tabellenzeilen"), ("Papier", "#F8F6F2", "Grundfläche Website und Dokumente"),
       ("Weiß", "#FFFFFF", "Grundfläche Slides, Logo auf dunklem Grund")]
def rgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]
def hx(c): return "#" + "".join(f"{max(0, min(255, round(v))):02X}" for v in c)
def light(h, t): return hx([v + (255 - v) * t for v in rgb(h)])
def dark(h, t): return hx([v * (1 - t) for v in rgb(h)])
def cmyk(h):
    r, g, b = [v / 255 for v in rgb(h)]; k = 1 - max(r, g, b)
    if k >= 1: return [0, 0, 0, 100]
    return [round(v * 100) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k)]
F = OUT + "06_farben/"
tokens = {}
for n, h, u in PAL:
    tokens[n] = {"hex": h, "rgb": rgb(h), "cmyk_naeherung": cmyk(h), "verwendung": u}
    if n in ("Indigo", "Indigo tief", "Tinte", "Lavendel", "Schiefer"):
        tokens[n]["stufen"] = {"hell_80": light(h, .8), "hell_60": light(h, .6), "hell_40": light(h, .4), "dunkel_25": dark(h, .25), "dunkel_50": dark(h, .5)}
# chart colours: one row for light, one for dark backgrounds, same order and hues
CHART = [("Indigo", "#3034C5", "Indigo hell", "#6977F6"), ("Lavendel", "#7D87DE", "Lavendel hell", "#ADAEF6"),
         ("Petrol", "#00897A", "Petrol hell", "#1FB3A0"), ("Amber", "#C9831A", "Amber hell", "#E09A2C"),
         ("Blau", "#2E7FCF", "Blau hell", "#5A9BE0"), ("Koralle", "#CF4F3A", "Koralle hell", "#E86F58")]
tokens["Chartfarben"] = {
    "regel": "Serie 1 = Farbe 1 usw. Auf Weiß die helle Reihe (hell_hintergrund), auf Tinte die dunkle Reihe (dunkel_hintergrund). Sonstige: Schiefer.",
    "hell_hintergrund": [{"position": i + 1, "name": a, "hex": b} for i, (a, b, _, _) in enumerate(CHART)],
    "dunkel_hintergrund": [{"position": i + 1, "name": c, "hex": d} for i, (_, _, c, d) in enumerate(CHART)],
    "sonstige": "#706C7E"}
json.dump(tokens, open(F + "farben.json", "w"), indent=2, ensure_ascii=False)
slug = {"Weiß": "weiss", "Indigo tief": "indigo-tief"}
css = "/* Captiv Farben */\n:root {\n"
for n, h, u in PAL:
    k = slug.get(n, n.lower()); css += f"  --captiv-{k}: {h};   /* {u} */\n"
    for s, v in tokens[n].get("stufen", {}).items(): css += f"  --captiv-{k}-{s.replace('_', '-')}: {v};\n"
css += "\n  /* Chartfarben: Reihenfolge fest, auf Weiß chart-N, auf Indigo tief chart-dunkel-N */\n"
for i, (a, b, c, d) in enumerate(CHART):
    css += f"  --captiv-chart-{i + 1}: {b};   /* {a} */\n  --captiv-chart-dunkel-{i + 1}: {d};   /* {c} */\n"
css += "  --captiv-chart-sonstige: #706C7E;\n}\n"
open(F + "farben.css", "w").write(css)
# Office theme colours (PowerPoint, Word, Excel): the same schemes as in the Captiv master
SCHEMES = {
    "Captiv": {"dk1": "16122D", "lt1": "FFFFFF", "dk2": "1A1B6F", "lt2": "E9E6E0", "accent1": "3034C5", "accent2": "7D87DE", "accent3": "00897A",
               "accent4": "C9831A", "accent5": "2E7FCF", "accent6": "CF4F3A", "hlink": "3034C5", "folHlink": "7D87DE"},
    "Captiv Dunkel": {"dk1": "FFFFFF", "lt1": "16122D", "dk2": "E9E6E0", "lt2": "1A1B6F", "accent1": "6977F6", "accent2": "ADAEF6", "accent3": "1FB3A0",
                      "accent4": "E09A2C", "accent5": "5A9BE0", "accent6": "E86F58", "hlink": "ADAEF6", "folHlink": "E9E6E0"}}
os.makedirs(F + "office", exist_ok=True)
for name, theme in SCHEMES.items():
    xml = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<a:clrScheme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="{name}">' + \
          "".join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in theme.items()) + "</a:clrScheme>\n"
    open(F + f"office/{name.replace(' ', '-')}.xml", "w").write(xml)
# Adobe swatch exchange (Illustrator, InDesign, Photoshop)
def ase(cols):
    def block(name, h):
        nm = (name + "\0").encode("utf-16-be")
        body = struct.pack(">H", len(name) + 1) + nm + b"RGB " + struct.pack(">fff", *[v / 255 for v in rgb(h)]) + struct.pack(">H", 2)
        return struct.pack(">HI", 1, len(body)) + body
    data = b"ASEF" + struct.pack(">HHI", 1, 0, len(cols)) + b"".join(block("Captiv " + n, h) for n, h in cols)
    return data
open(F + "adobe/Captiv-Farben.ase" if os.makedirs(F + "adobe", exist_ok=True) is None else "", "wb").write(
    ase([(n, h) for n, h, _ in PAL] + [(f"Chart {a}", b) for a, b, _, _ in CHART] + [(f"Chart {c}", d) for _, _, c, d in CHART] +
        [(f"{n} {s}", v) for n, h, _ in PAL for s, v in tokens[n].get("stufen", {}).items()]))
# palette overview: brand colours, then chart colours for light and dark backgrounds
sw = "".join(f'<rect x="{i * 200}" y="0" width="200" height="200" fill="{h}"/>' for i, (_, h, _) in enumerate(PAL))
sw += "".join(f'<rect x="{i * 200}" y="220" width="200" height="120" fill="{b}"/>' for i, (_, b, _, _) in enumerate(CHART))
sw += f'<rect x="0" y="360" width="{200 * len(CHART)}" height="160" fill="#16122D"/>'
sw += "".join(f'<rect x="{i * 200 + 20}" y="380" width="160" height="120" fill="{d}"/>' for i, (_, _, _, d) in enumerate(CHART))
W = 200 * max(len(PAL), len(CHART))
open(F + "farbpalette.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="520" viewBox="0 0 {W} 520"><title>Captiv Farbpalette</title>{sw}</svg>')
# fonts: variable and static weights for desktop use, woff2 for the web
S = OUT + "07_schrift/"
for d in ("desktop", "web"): os.makedirs(S + d, exist_ok=True)
f = TTFont(SRC / "fonts/Geist-Variable.woff2"); f.flavor = None; f.save(S + "desktop/Geist-Variable.ttf")
for w, n in ((300, "Light"), (400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")):
    v = TTFont(S + "desktop/Geist-Variable.ttf")
    st = instancer.instantiateVariableFont(v, {"wght": w}, updateFontNames=False)
    for rec in st["name"].names:
        if rec.nameID in (2, 17): rec.string = n
        elif rec.nameID in (4,): rec.string = f"Geist {n}"
        elif rec.nameID in (6,): rec.string = f"Geist-{n}"
        elif rec.nameID in (1, 16): rec.string = "Geist"
    st["OS/2"].usWeightClass = w
    st.save(S + f"desktop/Geist-{n}.ttf")
shutil.copy(SRC / "fonts/Geist-Variable.woff2", S + "web/Geist-Variable.woff2")
shutil.copy(SRC / "fonts/GEIST-LICENSE.txt", S + "GEIST-LICENSE.txt")
# source assets that are not generated: photos and the PowerPoint template
for sub in ("08_bildsprache", "09_praesentation"):
    src = SRC / "assets" / sub
    if src.exists(): shutil.copytree(src, OUT + sub, dirs_exist_ok=True)
shutil.copy(SRC / "LIESMICH.md", OUT + "LIESMICH.md")
print("ok")
