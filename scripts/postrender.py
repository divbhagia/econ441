"""Post-render: bake MathJax output into the HTML pages.

The math engine is the largest asset on the site (1.3MB); as a synchronous
script it blanks the page until it arrives, and even loaded async it saturates
slow links while the render-blocking head assets crawl ("practice problems not
loading"). So the engine now runs once, here, at build time: each math-bearing
page is typeset in headless Chromium, the rendered markup and MathJax's
generated stylesheet are written into the page, and the engine script tags are
dropped. Pages arrive as plain HTML+CSS -- equations render with the text on
any network, including offline. The reveal decks keep the runtime engine
(self-hosted): their plugin loads it without blocking.

Runs as a Quarto post-render script (headless Chromium via playwright, same
dependency as the audit).
"""
import os, pathlib, re, sys

out = pathlib.Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs")).resolve()
SITE = "https://dbhagia.com/econ441/"
pages = [p for p in out.rglob("*.html")
         if "site_libs" not in str(p) and "assets/mathjax" in p.read_text(encoding="utf-8")
         and "/slides/" not in str(p).replace("\\", "/")]
if not pages:
    print("postrender: no math pages"); sys.exit(0)

from playwright.sync_api import sync_playwright

def reroute(route):
    url = route.request.url
    if url.startswith(SITE):
        f = out / url[len(SITE):].split("?")[0]
        if f.exists():
            ct = ("application/javascript" if f.suffix == ".js" else
                  "font/woff" if f.suffix == ".woff" else "text/css" if f.suffix == ".css" else "text/html")
            route.fulfill(path=str(f), content_type=ct); return
    route.abort()

SPAN = re.compile(r'<span class="math (?:inline|display)">.*?</span>', re.S)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for page_path in pages:
        src = page_path.read_text(encoding="utf-8")
        n_src = len(SPAN.findall(src))
        if n_src == 0:
            continue
        pg = b.new_page(viewport={"width": 1150, "height": 900})
        pg.route(SITE + "**", reroute)
        pg.goto("file://" + str(page_path), timeout=60000)
        pg.evaluate("() => MathJax.startup.promise.then(() => true)")
        rendered = pg.evaluate(
            "() => [...document.querySelectorAll('span.math')].map(e => e.outerHTML)")
        styles = pg.evaluate(
            "() => (document.getElementById('MJX-CHTML-styles') || {outerHTML: ''}).outerHTML")
        pg.close()
        if len(rendered) != n_src or not styles:
            print(f"postrender: SKIP {page_path.relative_to(out)} "
                  f"(rendered {len(rendered)} of {n_src})"); continue
        it = iter(rendered)
        s = SPAN.sub(lambda m: next(it), src)
        s = s.replace("</head>", styles + "\n</head>", 1)
        s = re.sub(r'<script src="[^"]*(?:assets/mathjax/tex-chtml-full\.js|polyfill\.min\.js[^"]*)"[^>]*>\s*</script>', "", s)
        page_path.write_text(s, encoding="utf-8")
        print(f"postrender: baked {n_src} equations into {page_path.relative_to(out)}")
    b.close()
