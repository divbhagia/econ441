"""WCAG 2.1 AA audit of the built site (docs/).

Run from the project root:  python3 scripts/audit_a11y.py   (or: make audit)

Two passes over every page outside site_libs:
  1. axe-core (vendored, scripts/axe.min.js) with the WCAG 2.1 A/AA rulesets.
  2. Reflow (WCAG 1.4.10): at a 320px viewport, with every <details> opened,
     the page must not scroll horizontally. Slides are exempt (a deck scales
     rather than reflows).

  3. veraPDF: every PDF in docs/ must validate as PDF/UA-2 (one batch run).

Exit status is nonzero if anything fails, so the Makefile can refuse to call
a build clean. Needs playwright (chromium) and verapdf (brew install verapdf).
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AXE = (ROOT / "scripts" / "axe.min.js").read_text()
DOCS = ROOT / "docs"

def main():
    from playwright.sync_api import sync_playwright
    pages = sorted(p for p in DOCS.rglob("*.html") if "site_libs" not in str(p))
    failures = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for page_path in pages:
            rel = str(page_path.relative_to(DOCS))
            is_slide = "/slides/" in str(page_path)
            pg = b.new_page(viewport={"width": 1280, "height": 900})
            pg.goto("file://" + str(page_path)); pg.wait_for_timeout(2500)
            pg.evaluate(AXE)
            viols = pg.evaluate("""async () => {
              const r = await axe.run(document, {runOnly:{type:'tag',
                values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});
              return r.violations.map(v=>({id:v.id, impact:v.impact,
                nodes:v.nodes.slice(0,3).map(n=>n.target.join(' '))}));
            }""")
            pg.close()
            reflow_ok = True
            if not is_slide:
                pg = b.new_page(viewport={"width": 320, "height": 800})
                pg.goto("file://" + str(page_path)); pg.wait_for_timeout(2200)
                pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                pg.wait_for_timeout(900)
                w = pg.evaluate("document.documentElement.scrollWidth")
                reflow_ok = w <= 320
                pg.close()
            ok = not viols and reflow_ok
            if not ok: failures += 1
            marks = []
            if viols: marks.append(", ".join(v["id"] for v in viols))
            if not reflow_ok: marks.append("horizontal scroll at 320px (1.4.10)")
            print(f"  {'PASS' if ok else 'FAIL'}  {rel}" + ("   <-- " + "; ".join(marks) if marks else ""))
            for v in viols:
                for t in v["nodes"]:
                    print(f"          [{v['impact']}] {v['id']}: {t[:100]}")
        b.close()
    pdfs = sorted(str(p) for p in DOCS.rglob("*.pdf"))
    r = subprocess.run(["verapdf", "--flavour", "ua2", "--format", "text", *pdfs],
                       capture_output=True, text=True)
    pdf_fail = 0
    for line in r.stdout.splitlines():
        if line.startswith(("PASS", "FAIL")):
            status, path = line.split(maxsplit=1)
            path = path.rsplit(" ua2", 1)[0]
            rel = str(pathlib.Path(path).relative_to(DOCS))
            if status == "FAIL": pdf_fail += 1
            print(f"  {status:4s}  {rel}  (PDF/UA-2)")
    failures += pdf_fail
    print(f"\naudit: {len(pages)} pages + {len(pdfs)} PDFs, {failures} failing")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
