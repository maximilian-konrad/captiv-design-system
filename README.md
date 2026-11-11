# Captiv Design System

Logo, Farben, Schrift, Stilelemente, Vorlagen und Brand Guidelines von Captiv (AI Value Assurance).
Alles, was Nutzer brauchen, liegt fertig in **`dist/Captiv-Brand-Package/`**. Die Regeln stehen in
[`00_Captiv-Brand-Guidelines.pdf`](dist/Captiv-Brand-Package/00_Captiv-Brand-Guidelines.pdf).

## Für Nutzer

| Ich brauche … | Datei |
|---|---|
| Logo | `dist/Captiv-Brand-Package/02_logo/` (SVG fürs Web, PDF für Druck, PNG für Office) |
| Präsentation | `dist/Captiv-Brand-Package/09_praesentation/Captiv-Master.potx` |
| Farben für Code | `dist/Captiv-Brand-Package/06_farben/farben.css` oder `farben.json` |
| Farben für Word/Excel | `dist/Captiv-Brand-Package/06_farben/office/Captiv.xml` |
| Alles als ZIP | Releases rechts auf der GitHub-Seite |

### Farben

| Name | Hex | Rolle |
|---|---|---|
| Indigo | `#3034C5` | Markenfarbe, Akzent, erste Chartfarbe |
| Tinte | `#16122D` | Überschriften, Logo, Hintergrund dunkler Folien |
| Graphit | `#434054` | Fließtext |
| Schiefer | `#706C7E` | gedämpfter Text, Quellen, „Sonstige“ in Charts |
| Indigo tief | `#1A1B6F` | zweite dunkle Fläche |
| Lavendel | `#A1A1F0` | Zweitfarbe, Flächen |
| Nebel | `#E9E6E0` | helle Flächen |
| Papier | `#F8F6F2` | Grund Website und Dokumente |
| Weiß | `#FFFFFF` | Grund Folien |

Chartfarben (Reihenfolge fest), auf Weiß: Indigo `#3034C5`, Lavendel `#7D87DE`, Petrol `#00897A`,
Amber `#C9831A`, Blau `#2E7FCF`, Koralle `#CF4F3A`. Auf Tinte die hellen Gegenstücke, siehe Guidelines.

## Für Pflege und Änderungen

`dist/` wird komplett aus `src/` und `scripts/` erzeugt. Änderungen immer an den Quellen machen und neu bauen,
nie Dateien in `dist/` von Hand bearbeiten.

```
src/
  wordmark.json        Wortmarke als Pfade (Geist SemiBold, −3 % Laufweite)
  guide.css            Layout der Guidelines
  fonts/               Geist (variabel) mit Lizenz
  screenshots/         Website- und Folienbilder für die Guidelines
  assets/              nicht generierte Dateien: Fotos, PowerPoint-Vorlage
  LIESMICH.md          Kurzanleitung im Paket
scripts/
  build.py             Zeichen, Logos, Icons, Favicons, Stilelemente, Social-Banner
  og.py                Vorschaubild für Links
  extras.py            Farbdateien (CSS, JSON, Office, Adobe), Schriftdateien, Kopie der Quell-Assets
  guide.py, pdf.py     Brand Guidelines als HTML und PDF
dist/Captiv-Brand-Package/   fertiges Paket (wird mit eingecheckt)
```

### Bauen

Voraussetzungen: [uv](https://docs.astral.sh/uv/), `rsvg-convert` (macOS: `brew install librsvg`), `make`, `zip`.

```bash
make setup     # einmalig: Chromium für den PDF-Export
make           # alles neu erzeugen
make release   # zusätzlich build/Captiv-Brand-Package-v<VERSION>.zip
```

Farbwerte stehen an drei Stellen und müssen zusammen geändert werden: `COL` in `scripts/build.py`,
`PAL` und `CHART` in `scripts/extras.py`, `PAL` und `CHART` in `scripts/guide.py`.
Die PowerPoint-Vorlage in `src/assets/09_praesentation/` wird separat gepflegt und hier nur abgelegt.

### Neue Version veröffentlichen

1. Änderungen an `src/` oder `scripts/`, dann `make`
2. `VERSION` und `CHANGELOG.md` anpassen
3. Committen und pushen, dann Release mit ZIP anlegen:
   ```bash
   make release
   git tag v$(cat VERSION) && git push --tags
   gh release create v$(cat VERSION) build/Captiv-Brand-Package-v$(cat VERSION).zip --notes-file CHANGELOG.md
   ```
