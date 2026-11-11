# Captiv Design System: alles neu erzeugen mit `make`, Release-ZIP mit `make release`
VERSION := $(shell cat VERSION)
PKG     := dist/Captiv-Brand-Package

.PHONY: all assets guide release clean setup

all: assets guide

setup:            ## einmalig: Chromium für den PDF-Export
	uv run --with playwright==1.63.0 playwright install chromium

assets:           ## Logos, Icons, Stilelemente, Farben, Schriften
	uv run scripts/build.py
	uv run scripts/og.py
	uv run scripts/extras.py

guide: assets     ## Brand Guidelines (HTML, dann PDF)
	uv run scripts/guide.py
	uv run scripts/pdf.py

release: all      ## ZIP für GitHub Releases
	mkdir -p build
	cd dist && rm -f ../build/Captiv-Brand-Package-v$(VERSION).zip && zip -qr ../build/Captiv-Brand-Package-v$(VERSION).zip Captiv-Brand-Package -x '*.DS_Store'
	@echo "build/Captiv-Brand-Package-v$(VERSION).zip"

clean:
	rm -rf build
