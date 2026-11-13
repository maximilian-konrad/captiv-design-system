# /// script
# dependencies = []
# ///
"""Captiv brand guidelines (A4 landscape, HTML that is printed to PDF afterwards)."""
import base64, math
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # repository root
SRC, DIST, BUILD = ROOT / "src", ROOT / "dist", ROOT / "build"

P = str(DIST / "Captiv-Brand-Package") + "/"
SH = str(SRC / "screenshots") + "/"

IND, TIN, LAV, SCH, NEB, PAP, WEI = "#3034C5", "#16122D", "#A1A1F0", "#706C7E", "#E9E6E0", "#F8F6F2", "#FFFFFF"
ITF, GRA = "#1A1B6F", "#434054"
CHART = [("Indigo", "#3034C5", "Indigo hell", "#6977F6"), ("Lavendel", "#7D87DE", "Lavendel hell", "#ADAEF6"), ("Petrol", "#00897A", "Petrol hell", "#1FB3A0"),
         ("Amber", "#C9831A", "Amber hell", "#E09A2C"), ("Blau", "#2E7FCF", "Blau hell", "#5A9BE0"), ("Koralle", "#CF4F3A", "Koralle hell", "#E86F58")]
PAL = [("Indigo", IND, "Markenfarbe", "Akzente, Links, Buttons, ausgewählte Elemente, erste Chartfarbe"),
       ("Tinte", TIN, "Schrift, Logo", "Überschriften, Logo, Hintergrund dunkler Folien"),
       ("Graphit", GRA, "Fließtext", "Fließtext auf Website und in Office"),
       ("Indigo tief", ITF, "Dunkle Fläche", "Zweite dunkle Fläche, dunkle Boxen"),
       ("Lavendel", LAV, "Zweitfarbe", "Charts, Flächen und Highlights neben Indigo"),
       ("Schiefer", SCH, "Neutral", "Gedämpfter Text, Quellen, Achsen, Sonstige in Charts"),
       ("Nebel", NEB, "Fläche", "Boxen, Tabellenzeilen, Hintergründe für Zitate"),
       ("Papier", PAP, "Grund", "Hintergrund der Website und von Dokumenten"),
       ("Weiß", WEI, "Grund", "Hintergrund von Slides, Logo auf dunklen Flächen")]

def rgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]
def hx(c): return "#" + "".join(f"{max(0, min(255, round(v))):02X}" for v in c)
def light(h, t): return hx([v + (255 - v) * t for v in rgb(h)])
def dark(h, t): return hx([v * (1 - t) for v in rgb(h)])
def lum(h):
    c = [v / 255 for v in rgb(h)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
def cmyk(h):
    r, g, b = [v / 255 for v in rgb(h)]; k = 1 - max(r, g, b)
    if k >= 1: return "0 0 0 100"
    return " ".join(str(round(v * 100)) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))
def uri(path, mime): return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()
def svgf(rel): return uri(P + rel, "image/svg+xml")
def jpg(name): return uri(SH + name + ".jpg", "image/jpeg")
def png(rel): return uri(P + rel, "image/png")

LOGO_T = svgf("02_logo/horizontal/captiv-logo-horizontal_tinte.svg")
LOGO_I = svgf("02_logo/horizontal/captiv-logo-horizontal_indigo.svg")
LOGO_W = svgf("02_logo/horizontal/captiv-logo-horizontal_weiss.svg")
STACK_T = svgf("02_logo/gestapelt/captiv-logo-gestapelt_tinte.svg")
MARK_T = svgf("01_zeichen/captiv-zeichen_tinte.svg")
MARK_I = svgf("01_zeichen/captiv-zeichen_indigo.svg")
MARK_W = svgf("01_zeichen/captiv-zeichen_weiss.svg")
WORD_T = svgf("02_logo/wortmarke/captiv-wortmarke_tinte.svg")

# the dot C drawn inline (for the construction drawing)
PTS = [[90,222],[90,280],[90,338],[90,396],[90,454],[90,512],[90,570],[148,164],[148,222],[148,280],[148,338],[148,396],[148,454],[148,512],[148,570],[148,628],[206,106],[206,164],[206,222],[206,280],[206,338],[206,396],[206,454],[206,512],[206,570],[206,628],[206,686],[264,48],[264,106],[264,164],[264,222],[264,570],[264,628],[264,686],[264,744],[322,48],[322,106],[322,164],[322,628],[322,686],[322,744],[380,48],[380,106],[380,164],[380,628],[380,686],[380,744],[438,48],[438,106],[438,164],[438,628],[438,686],[438,744],[496,48],[496,106],[496,164],[496,222],[496,570],[496,628],[496,686],[496,744],[554,106],[554,164],[554,222],[554,280],[554,512],[554,570],[554,628],[554,686],[612,106],[612,164],[612,222],[612,280],[612,512],[612,570],[612,628],[612,686],[670,164],[670,222],[670,280],[670,512],[670,570]]
def construction():
    grid = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{SCH}" opacity=".45"/>' for x in range(32, 760, 58) for y in range(-10, 800, 58))
    lines = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="790" stroke="{SCH}" stroke-opacity=".18" stroke-width="1.5"/>' for x in range(32, 760, 58)) + \
            "".join(f'<line x1="0" y1="{y}" x2="790" y2="{y}" stroke="{SCH}" stroke-opacity=".18" stroke-width="1.5"/>' for y in range(-10, 800, 58))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{11.6 + 14.5 * (1 - (x - 90) / 580):.1f}" fill="{IND}"/>' for x, y in PTS)
    ann = (f'<line x1="64" y1="790" x2="116" y2="790" stroke="{TIN}" stroke-width="3"/><text x="90" y="830" text-anchor="middle" font-size="30" fill="{TIN}">90 %</text>'
           f'<line x1="658" y1="790" x2="682" y2="790" stroke="{TIN}" stroke-width="3"/><text x="670" y="830" text-anchor="middle" font-size="30" fill="{TIN}">40 %</text>')
    return f'<svg viewBox="0 -20 790 870" style="width:100%;height:auto">{lines}{grid}{dots}{ann}</svg>'

def foot(n, title): return f'<div class="foot"><span>Captiv · Brand Guidelines · {title}</span><span>{n}</span></div>'
def page(n, kicker, title, body, lead=""):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="p"><div class="kicker">{kicker}</div><h1>{title}</h1>{l}{body}{foot(n, kicker)}</section>'

css = open(SRC / "guide.css").read().replace("FONT", base64.b64encode(open(SRC / "fonts/Geist-Variable.woff2", "rb").read()).decode())
pages = []

# 1 cover
field = "".join(f'<circle cx="{x}" cy="{y}" r="{6.5 * max(0.0, min(1, (x - 520) / 560)) ** 1.1:.2f}" fill="{IND}"/>' for x in range(14, 1123, 28) for y in range(14, 794, 28))
pages.append(f'''<section class="p cover" style="background:{PAP};padding:0">
<svg viewBox="0 0 1123 794" style="position:absolute;inset:0;width:100%;height:100%" preserveAspectRatio="none">{field}</svg>
<div style="position:absolute;left:18mm;top:18mm;right:18mm;bottom:18mm;display:flex;flex-direction:column;justify-content:space-between">
<img src="{LOGO_T}" style="height:15mm;align-self:flex-start">
<div><div class="kicker" style="color:{IND}">Brand Guidelines · Version 1.3</div>
<div style="font-size:46px;font-weight:500;letter-spacing:-.035em;color:{TIN};line-height:1.02">Logo, Farben, Schrift<br>und Stilelemente</div>
<div style="font-size:13px;color:{SCH};margin-top:4mm">Stand November 2026</div></div></div></section>''')

# 2 contents + brand core
toc = ["Marke", "Logo: Zeichen und Konstruktion", "Logo: Varianten und Flächen", "Logo: Schutzzone, Größen, Don'ts", "Farben", "Farben: Abstufungen und Kontraste",
       "Farben: Chartfarben", "Typografie", "Stilelemente", "Bildsprache", "Anwendung: Website", "Anwendung: Slides und Social", "Inhalt des Pakets"]
pages.append(page(2, "Inhalt", "Captiv auf einen Blick", f'''
<div class="row" style="gap:14mm;margin-top:6mm"><div class="col">
<ol class="toc">{"".join(f"<li><span>{t}</span><b>{i + 2}</b></li>" for i, t in enumerate(toc))}</ol></div>
<div class="col"><div class="box" style="background:{TIN};color:{WEI}">
<div class="kicker" style="color:{LAV}">Markenkern</div>
<div style="font-size:30px;font-weight:500;letter-spacing:-.03em;margin:2mm 0 4mm">AI Value Assurance</div>
<p style="font-size:13px;line-height:1.55;margin:0;color:#DBD8D2">Captiv sorgt dafür, dass sich KI-Vorhaben in messbaren Ergebnissen niederschlagen: Von der Konzeption über die Umsetzung bis zur Adoption.</p></div>
<div class="kicker" style="margin-top:8mm">Haltung im Auftritt</div>
<ul class="bul"><li><b>Klar:</b> viel Weißraum, wenige Farben, eine klare Hierarchie</li>
<li><b>Präzise:</b> das Punktraster steht für Daten, Struktur und Messbarkeit</li>
<li><b>Fokussiert:</b> Indigo markiert nur das, worauf es ankommt</li></ul></div></div>'''))

# 3 logo construction
pages.append(page(3, "Logo", "Zeichen und Konstruktion", f'''
<div class="row" style="gap:12mm;margin-top:2mm"><div style="width:96mm">{construction()}</div>
<div class="col"><ul class="bul">
<li>Das Zeichen ist ein C aus <b>82 Punkten</b> auf einem quadratischen Raster mit 58 Einheiten Abstand.</li>
<li>Die Punkte werden von links nach rechts kleiner: <b>90 %</b> des Rasterabstands an der linken Kante, <b>40 %</b> an der Öffnung. Alle Punkte einer Spalte sind gleich groß.</li>
<li>Der Verlauf steht für Bewegung und Fokus: vom Großen zum Präzisen.</li>
<li>Die <b>Wortmarke</b> ist Geist SemiBold mit −3 % Laufweite, in Pfade umgewandelt. Sie wird nie neu gesetzt.</li>
<li>Im <b>horizontalen Logo</b> ist die Versalhöhe der Wortmarke 55 % der Zeichenhöhe, der Abstand zwischen Zeichen und Wortmarke 4 Rasterabstände.</li></ul>
<div class="row" style="gap:6mm;margin-top:8mm;align-items:flex-end">
<div class="tile" style="width:44mm;height:34mm;background:{PAP}"><img src="{MARK_T}" style="height:20mm"></div>
<div class="tile" style="flex:1;height:34mm;background:{PAP}"><img src="{LOGO_T}" style="height:12mm"></div>
<div class="tile" style="width:44mm;height:34mm;background:{PAP}"><img src="{STACK_T}" style="height:24mm"></div></div>
<div class="row caps" style="gap:6mm"><span style="width:44mm">Zeichen</span><span style="flex:1">Logo horizontal (Standard)</span><span style="width:44mm">Logo gestapelt</span></div>
</div></div>'''))

# 4 logo variants on surfaces
def tile(bg, img, h, label, border=False):
    b = "outline:1px solid #0001;" if border else ""
    return f'<div class="col"><div class="tile" style="height:44mm;background:{bg};{b}"><img src="{img}" style="height:{h}"></div><div class="caps">{label}</div></div>'
pages.append(page(4, "Logo", "Varianten und Flächen", f'''
<div class="row" style="gap:5mm;margin-top:2mm">{tile(PAP, LOGO_T, "11mm", "Tinte auf Papier · Standard")}{tile(WEI, LOGO_T, "11mm", "Tinte auf Weiß · Slides, Dokumente", True)}{tile(PAP, LOGO_I, "11mm", "Indigo auf Papier · Akzent")}</div>
<div class="row" style="gap:5mm;margin-top:6mm">{tile(IND, LOGO_W, "11mm", "Weiß auf Indigo · Titel, Social")}{tile(TIN, LOGO_W, "11mm", "Weiß auf Tinte · dunkle Flächen")}{tile(LAV, LOGO_T, "11mm", "Tinte auf Lavendel · sparsam")}</div>
<p class="note">Erlaubte Logofarben: Tinte, Indigo, Weiß und für Ausnahmen (z. B. Stempel, Fax) Schwarz. Auf Fotos nur auf ruhigen, dunklen oder hellen Bildstellen platzieren.</p>'''))

# 5 clear space, sizes, don'ts
def dont(style, img, label, bg=PAP):
    return f'<div class="col"><div class="tile" style="height:30mm;background:{bg};position:relative"><img src="{img}" style="height:8mm;{style}"><span class="x">×</span></div><div class="caps">{label}</div></div>'
pages.append(page(5, "Logo", "Schutzzone, Mindestgrößen und Don'ts", f'''
<div class="row" style="gap:10mm;margin-top:2mm"><div class="col">
<div class="tile" style="height:52mm;background:{PAP};position:relative">
<div style="position:relative;padding:9mm;outline:1.5px dashed {LAV}"><img src="{LOGO_T}" style="height:12mm;display:block"><span class="cz" style="left:0;top:0;width:9mm;height:9mm"></span></div></div>
<div class="caps">Schutzzone: rundum mindestens die halbe Höhe des Zeichens</div></div>
<div class="col"><table class="tb"><tr><th></th><th>Digital</th><th>Druck</th></tr>
<tr><td>Logo horizontal</td><td>24 px Höhe</td><td>8 mm Höhe</td></tr><tr><td>Logo gestapelt</td><td>48 px Höhe</td><td>15 mm Höhe</td></tr>
<tr><td>Zeichen allein</td><td>16 px</td><td>6 mm</td></tr></table>
<p class="note">Darunter laufen die kleinen Punkte an der Öffnung zu.</p></div></div>
<div class="row" style="gap:4mm;margin-top:8mm">
{dont("transform:scaleX(1.5)", LOGO_T, "Nicht verzerren")}{dont("transform:rotate(-12deg)", LOGO_T, "Nicht drehen")}
{dont("filter:hue-rotate(160deg) saturate(3)", LOGO_I, "Keine anderen Farben")}{dont("filter:drop-shadow(2px 3px 2px #0008)", LOGO_T, "Keine Effekte")}
{dont("", LOGO_T, "Nicht auf unruhigem Grund", "repeating-linear-gradient(45deg,#A1A1F0 0 6px,#3034C5 6px 12px)")}</div>'''))

# 6 colours
cards = "".join(f'''<div class="pc"><div class="base" style="background:{h}"></div><b>{n}</b><span class="role">{r}</span><span class="hex">{h}</span>
<span class="meta">RGB {" ".join(map(str, rgb(h)))}<br>CMYK ca. {cmyk(h)}</span><span class="use">{u}</span></div>''' for n, h, r, u in PAL)
ratio = [(PAP, 45, "Papier / Weiß"), (TIN, 22, "Tinte"), (IND, 13, "Indigo"), (NEB, 9, "Nebel"), (LAV, 6, "Lavendel"), (SCH, 5, "Schiefer")]
bar = "".join(f'<div style="flex:{w};background:{c};color:{"#fff" if lum(c) < .3 else TIN}"><span>{l} {w} %</span></div>' for c, w, l in ratio)
pages.append(page(6, "Farben", "Palette", f'''
<div class="row" style="gap:3.5mm">{cards}</div>
<div class="kicker" style="margin-top:8mm">Mengenverhältnis (Richtwert)</div>
<div class="ratio">{bar}</div>
<p class="note">Indigo ist die einzige laute Farbe und wird gezielt eingesetzt: für das Wichtigste auf einer Seite, nicht als Fläche für alles. CMYK-Werte sind rechnerische Näherungen, für Druck bitte mit der Druckerei abstimmen.</p>'''))

# 7 shades + contrast
def shades(n, h):
    s = [("+80 %", light(h, .8)), ("+60 %", light(h, .6)), ("+40 %", light(h, .4)), ("Basis", h), ("−25 %", dark(h, .25)), ("−50 %", dark(h, .5))]
    return f'<div class="col"><b style="font-size:12px">{n}</b><div class="shades">' + "".join(
        f'<div class="sh" style="background:{c}"><span style="color:{"#111" if lum(c) > .35 else "#fff"}">{l}</span><span style="color:{"#111" if lum(c) > .35 else "#fff"}">{c}</span></div>' for l, c in s) + "</div></div>"
rows = [("Tinte auf Papier", TIN, PAP), ("Graphit auf Weiß", GRA, WEI), ("Schiefer auf Papier", SCH, PAP), ("Indigo auf Weiß", IND, WEI),
        ("Weiß auf Indigo", WEI, IND), ("Lavendel auf Weiß", LAV, WEI), ("Weiß auf Tinte", WEI, TIN), ("Lavendel hell auf Tinte", "#ADAEF6", TIN)]
def tag(c): return "Text" if c >= 4.5 else ("große Schrift, Grafik" if c >= 3 else "nur Fläche")
tbl = "".join(f'<tr><td><span class="sw" style="background:{b}"><i style="background:{a}"></i></span>{l}</td><td>{contrast(a, b):.1f} : 1</td><td>{tag(contrast(a, b))}</td></tr>' for l, a, b in rows)
pages.append(page(7, "Farben", "Abstufungen und Kontraste", f'''
<div class="row" style="gap:5mm">{shades("Indigo", IND)}{shades("Tinte", TIN)}{shades("Indigo tief", ITF)}{shades("Lavendel", LAV)}
<div class="col" style="flex:2.4"><b style="font-size:12px">Kontraste nach WCAG</b><table class="tb" style="margin-top:2mm">{tbl}</table>
<p class="note">Fließtext braucht mindestens 4,5 : 1, große Schrift und Grafiken 3 : 1. Lavendel nie für Text auf hellem Grund.</p></div></div>
'''))

# 8 chart colours
def minichart(bg, cols, fg, mu):
    hs = (88, 72, 60, 46, 34, 22)
    b = "".join(f'<div class="bar"><div style="height:{h}%;background:{c}"></div><span style="color:{mu}">{i + 1}</span></div>' for i, (h, c) in enumerate(zip(hs, cols)))
    return f'''<div class="slide" style="background:{bg};outline:1px solid #0002">
<div style="font-size:12px;font-weight:700;color:{fg}">Pricing trägt den größten Wertbeitrag</div>
<div style="font-size:8px;color:{mu};margin-top:.8mm">Beispiel, Serien 1 bis 6</div><div class="chart" style="border-color:{mu}55">{b}</div></div>'''
def chips(idx, labels):
    return "".join(f'<div class="col"><div style="height:11mm;border-radius:1.5mm;background:{c[idx + 1]};outline:1px solid #0001"></div><div class="caps"><b style="color:#16122D">{i + 1}. {c[idx]}</b><br>{c[idx + 1]}</div></div>' for i, c in enumerate(CHART))
pages.append(page(8, "Farben", "Chartfarben", f'''
<div class="row" style="gap:10mm"><div class="col" style="flex:1.35">
<div class="kicker">Auf Weiß (heller Master)</div><div class="row" style="gap:2.5mm">{chips(0, 0)}</div>
<div class="kicker" style="margin-top:6mm">Auf Tinte (dunkler Master)</div><div class="row" style="gap:2.5mm;background:{TIN};padding:3mm;border-radius:2mm">{"".join(f'<div class="col"><div style="height:11mm;border-radius:1.5mm;background:{d}"></div><div class="caps" style="color:#DCD9D3"><b style="color:#fff">{i + 1}. {c}</b><br>{d}</div></div>' for i, (_, _, c, d) in enumerate(CHART))}</div>
<ul class="bul" style="margin-top:6mm"><li>Reihenfolge immer gleich: Serie 1 Indigo, 2 Lavendel, 3 Petrol, 4 Amber, 5 Blau, 6 Koralle. Zwei Serien bleiben so markentreu in Indigo und Lavendel</li>
<li>Jede Farbe hat ein Paar: auf Weiß die Grundreihe, auf Tinte die helle Reihe mit gleichem Farbton</li>
<li>„Sonstige“ und Vergleichswerte in Schiefer, mehr als 6 Serien in „Sonstige“ zusammenfassen</li>
<li>In PowerPoint immer die Designfarben wählen, keine Hex-Werte eintippen. Dann wechseln Charts beim Kopieren zwischen hellem und dunklem Master automatisch die Reihe</li></ul></div>
<div class="col">{minichart(WEI, [c[1] for c in CHART], TIN, SCH)}<div class="caps">Heller Master</div>
<div style="height:4mm"></div>{minichart(TIN, [c[3] for c in CHART], WEI, "#B9B4CC")}<div class="caps">Dunkler Master</div></div></div>
<p class="note">Geprüft: alle Chartfarben mit mindestens 3 : 1 Kontrast zu ihrem Hintergrund, benachbarte Farben auch bei Rot-Grün-Sehschwäche unterscheidbar. Rot und Grün für gut und schlecht sind keine Chartfarben und werden nur gezielt eingesetzt.</p>'''))

# 9 typography
sample = lambda w, s, t, extra="": f'<div style="font-weight:{w};font-size:{s};letter-spacing:{extra or "-.01em"};line-height:1.1;color:{TIN}">{t}</div>'
pages.append(page(9, "Typografie", "Geist", f'''
<div class="row" style="gap:12mm;margin-top:2mm"><div class="col">
<div style="font-size:96px;font-weight:500;letter-spacing:-.04em;color:{TIN};line-height:1">Aa Gg</div>
<div class="row" style="gap:5mm;margin-top:6mm;flex-wrap:wrap">{"".join(f'<div style="font-weight:{w};font-size:20px;color:{TIN}">{n}</div>' for w, n in ((300, "Light"), (400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")))}</div>
<p class="note" style="margin-top:6mm">Geist (Vercel) ist eine klare, technische Grotesk und frei nutzbar (SIL Open Font License). Die Schriftdateien liegen im Paket unter 07_schrift. In <b>PowerPoint, Word und Excel gilt Arial</b>, damit Dateien bei allen Empfängern gleich aussehen. Überschriften in Tinte, Fließtext in Graphit, Quellen in Schiefer, Hervorhebungen in Indigo, wie auf der Website.</p></div>
<div class="col"><table class="tb ty">
<tr><th>Rolle</th><th>Website (Geist)</th><th>Slides (Arial)</th><th>Schnitt</th></tr>
<tr><td>{sample(500, "22px", "Display", "-.035em")}</td><td>72 px</td><td>40 pt</td><td>Medium, −3,5 %</td></tr>
<tr><td>{sample(400, "18px", "Überschrift", "-.02em")}</td><td>44 px</td><td>24 bis 28 pt</td><td>Regular oder SemiBold</td></tr>
<tr><td>{sample(400, "15px", "Lead-Text", "-.02em")}</td><td>20 bis 28 px</td><td>16 bis 18 pt</td><td>Regular</td></tr>
<tr><td>{sample(400, "13px", "Fließtext")}</td><td>16 px, Zeilenabstand 1,5</td><td>12 bis 14 pt</td><td>Regular</td></tr>
<tr><td>{sample(700, "10px", "LABEL", ".04em")}</td><td>12 px, Versalien</td><td>9 bis 10 pt</td><td>Bold, +3 %</td></tr>
<tr><td><span style="font-size:10px;color:{SCH}">Quellen, Fußnoten</span></td><td>12 px</td><td>8 pt</td><td>Regular, Schiefer</td></tr></table></div></div>'''))

# 9 style elements
def el(rel, label, bg=PAP, h="38mm"):
    return f'<div class="col"><div class="tile" style="height:{h};background:{bg};padding:4mm"><img src="{svgf(rel)}" style="max-width:100%;max-height:100%"></div><div class="caps">{label}</div></div>'
pages.append(page(10, "Stilelemente", "Raster, Verlauf und Zoom", f'''
<div class="row" style="gap:5mm">{el("04_stilelemente/punktfelder/verlauf-horizontal_indigo.svg", "Verlauf: 90 bis 40 %, wie im Zeichen")}{el("04_stilelemente/punktfelder/zoom-radial_tinte.svg", "Zoom: klein in der Mitte, groß am Rand")}{el("04_stilelemente/punktfelder/aufloesung-horizontal_weiss.svg", "Auflösung: für Ränder von Bildern und Bannern", IND)}</div>
<div class="row" style="gap:5mm;margin-top:5mm">{el("04_stilelemente/zeichen-im-raster_indigo.svg", "Zeichen im Raster: Titel, Social", IND)}{el("04_stilelemente/punktfelder/zoom-radial-invers_lavendel.svg", "Zoom invers: Fokus in der Mitte")}<div class="col"><div class="tile" style="height:38mm;background:{PAP};flex-direction:column;gap:6mm;padding:6mm"><img src="{svgf("04_stilelemente/trenner/punkt-trenner_indigo.svg")}" style="width:100%"><img src="{svgf("04_stilelemente/trenner/aufzaehlungspunkte-3_tinte.svg")}" style="height:6mm"></div><div class="caps">Trenner und Aufzählungspunkte</div></div></div>
<ul class="bul" style="margin-top:6mm"><li>Alle Elemente bauen auf dem Raster des Zeichens auf: Punkte mit gleichem Abstand, Größen zwischen 40 und 90 % des Abstands.</li>
<li>Auf der Website ist das Raster animiert: feine Linien, Punkte, die zum Rand größer werden, und Pfade in Indigo, die kurz aufleuchten.</li>
<li>Stilelemente immer dezent einsetzen: maximal ein Punktfeld pro Seite oder Folie, nie hinter Fließtext.</li></ul>'''))

# 10 imagery
team = "".join(f'''<div class="col" style="align-items:center;display:flex;flex-direction:column"><div style="width:30mm;height:30mm;border-radius:50%;overflow:hidden;background:{bg};position:relative">
<img src="{png(f"08_bildsprache/team/{n}.png")}" style="width:100%;height:100%;{f}"></div><div class="caps" style="text-align:center">{l}</div></div>'''
               for n, bg, f, l in (("max", IND, "", "Ausgewählt: Farbe auf Indigo"), ("jan", "#EEEBE5", "filter:grayscale(1)", "Sonst: Schwarzweiß auf Raster"), ("svenja", LAV, "", "Alternative: Lavendel")))
pages.append(page(11, "Bildsprache", "Porträts und Fotos", f'''
<div class="row" style="gap:12mm;margin-top:2mm"><div class="col">
<div class="kicker">Porträts</div><div class="row" style="gap:4mm">{team}</div>
<ul class="bul" style="margin-top:5mm"><li>Freigestellt, frontal, freundlich, Tageslicht</li><li>Gleicher Ausschnitt für alle: Kopf gleich groß, Haaransatz knapp unter dem oberen Rand, Schultern füllen den Kreis unten</li>
<li>Immer im Kreis, Hintergrund in einer Markenfarbe oder dem Raster</li></ul></div>
<div class="col"><div class="kicker">Referenzfotos</div>
<img src="{uri(P + "08_bildsprache/referenzen/case-retail-motion.jpg", "image/jpeg")}" style="width:100%;height:44mm;object-fit:cover;border-radius:2mm">
<ul class="bul" style="margin-top:5mm"><li>Echte Arbeits- und Handelsumgebungen, keine gestellten Stockfotos</li><li>Waagerechte Bewegungsunschärfe: Formen bleiben erkennbar, Details nicht</li>
<li>Mit leichter Abdunklung oder Aufhellung, damit Text darauf lesbar bleibt</li></ul></div></div>'''))

# 11 website
pages.append(page(12, "Anwendung", "Website", f'''
<div class="row" style="gap:5mm">{"".join(f'<div class="col"><img class="shot" src="{jpg(n)}"><div class="caps">{l}</div></div>' for n, l in (("hero", "Hero mit animiertem Raster"), ("framework", "Value Framework"), ("team", "Team")))}</div>
<div class="row" style="gap:5mm;margin-top:5mm">{"".join(f'<div class="col"><img class="shot" src="{jpg(n)}"><div class="caps">{l}</div></div>' for n, l in (("problem", "Text und Hierarchie"), ("case", "Referenzen mit Fotos"), ("kontakt", "Kontaktformular")))}</div>'''))

# 13 slides + social
pages.append(page(13, "Anwendung", "Slides und Social", f'''
<div class="row" style="gap:4mm">{"".join(f'<div class="col"><img class="shot" src="{jpg(n)}"><div class="caps">{l}</div></div>' for n, l in (("master-titel-hell", "Titelfolie, heller Master"), ("master-titel-dunkel", "Titelfolie, dunkler Master"), ("master-haelfte-hell", "Layout 1/2 mit Nebel-Fläche"), ("master-kapitel-dunkel", "Kapitelfolie, dunkler Master")))}</div>
<ul class="bul" style="margin-top:4mm"><li>Vorlage: 09_praesentation/Captiv-Master.potx, mit hellem und dunklem Master und 31 Layouts</li>
<li>Heller Master für Inhalte, dunkler Master für Titel, Kapitel und Botschaften. Titel und Text in Arial</li></ul>
<div class="row" style="gap:5mm;margin-top:3mm"><div class="col" style="flex:2"><img class="shot" src="{png("05_anwendungen/linkedin-banner_1584x396.png")}"><div class="caps">LinkedIn-Banner (Profil)</div></div>
<div class="col"><img class="shot" src="{png("03_icons/profilbild_weiss-auf-indigo_400px.png")}" style="width:26mm"><div class="caps">Profilbild</div></div></div>'''))

# 14 package contents
items = [("00", "Brand Guidelines", "Dieses Dokument"), ("01_zeichen", "Zeichen", "Das C allein in Tinte, Indigo, Weiß, Schwarz; als SVG, PDF und PNG; auf Flächen"),
         ("02_logo", "Logo", "Horizontal (Standard), gestapelt, Wortmarke; alle Farbvarianten und auf Flächen"),
         ("03_icons", "Icons", "App-Icons, Profilbilder, Favicon-Set für Websites"),
         ("04_stilelemente", "Stilelemente", "Punktfelder (Verlauf, Zoom, Auflösung), Rasterkacheln, Trenner, Zeichen im Raster"),
         ("05_anwendungen", "Anwendungen", "LinkedIn-Banner für Profil (1584 × 396) und Unternehmensseite (1128 × 191), X-Banner, Vorschaubild für Links, Logo für die E-Mail-Signatur"),
         ("06_farben", "Farben", "CSS, JSON, Office-Designfarben hell und dunkel (PowerPoint, Word, Excel), Adobe-Farbfelder (ASE), Chartfarben"),
         ("07_schrift", "Schrift", "Geist zum Installieren (Light bis Bold, variabel) und für das Web, mit Lizenz"),
         ("08_bildsprache", "Bildsprache", "Freigestellte Team-Porträts und Referenzfotos mit Bewegungsunschärfe"),
         ("09_praesentation", "Präsentation", "PowerPoint-Vorlage (.potx) und Master (.pptx) mit hellem und dunklem Master, Designfarben und Chartfarben")]
pages.append(page(14, "Paket", "Inhalt des Pakets", f'''
<table class="tb pk" style="margin-top:2mm">{"".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in items)}</table>
<div class="row" style="gap:8mm;margin-top:7mm"><div class="col box" style="background:{NEB}"><div class="kicker">PowerPoint und Office einrichten</div>
<p class="note" style="margin:0"><b>Präsentationen:</b> Captiv-Master.potx doppelklicken oder unter Datei › Neu aus Vorlage öffnen.<br><b>Word, Excel:</b> 06_farben/office/Captiv.xml kopieren nach<br><b>Mac:</b> ~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/Theme Colors<br><b>Windows:</b> %APPDATA%\\Microsoft\\Templates\\Document Themes\\Theme Colors<br>Danach unter Entwurf › Varianten › Farben „Captiv“ wählen.</p></div>
<div class="col box" style="background:{NEB}"><div class="kicker">Welche Datei wofür?</div>
<p class="note" style="margin:0"><b>SVG:</b> Web, Figma, skalierbar<br><b>PDF:</b> Druck, InDesign, Illustrator<br><b>PNG:</b> PowerPoint, Word, E-Mail, Social Media</p></div></div>'''))

html = f"<!doctype html><html lang='de'><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>"
BUILD.mkdir(exist_ok=True); open(BUILD / "guide.html", "w").write(html)
print("pages", len(pages))
