# /// script
# dependencies = ["playwright==1.63.0"]
# ///
"""Prints build/guide.html to the guidelines PDF (A4 landscape). Needs Chromium once: uv run --with playwright playwright install chromium"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
html = ROOT / "build" / "guide.html"
pdf = ROOT / "dist" / "Captiv-Brand-Package" / "00_Captiv-Brand-Guidelines.pdf"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(html.as_uri(), wait_until="load")
    page.wait_for_timeout(500)
    page.pdf(path=str(pdf), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True)
    browser.close()
print("ok", pdf.relative_to(ROOT))
