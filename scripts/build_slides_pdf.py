r"""Tagged-PDF slide decks from the same .qmd sources as the web decks.

Usage (from the project root):  python3 scripts/build_slides_pdf.py 1 2

Route: pandoc's beamer writer emits the frames, then the beamer template is
discarded and the body is compiled under ltx-talk, the LaTeX team's
tagging-aware presentation class (beamer itself refuses \DocumentMetadata).
The output passes veraPDF PDF/UA-2; the build fails if it does not.

Deliberate choices:
  - Overlay specs are stripped: the PDF is the downloadable study artifact,
    complete slides, one page per frame (like pdf-separate-fragments: false).
  - .fragment divs from the reveal decks are inlined by pandoc already.
  - fig-alt survives via assets/beamer-deck.lua (pandoc's writers drop it).
"""
import pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Theme: the website's palette and type (assets/custom.scss, assets/slides.scss)
# -- maroon structure colour, Lato body, Fira Sans Condensed headings. Fira Sans
# Condensed is a system font on this machine (fontspec finds it by name); Lato
# comes from the TeX tree. ltx-talk's template keys are experimental, so if a
# tlmgr update breaks an \EditInstance line, the visual theme is all that is
# lost -- tagging does not depend on it.
PREAMBLE = r"""\DocumentMetadata{pdfstandard=UA-2,pdfversion=2.0,lang=en-US,tagging=on}
\documentclass[frame-title-arg]{ltx-talk}
\usepackage{amsmath,graphicx}
\providecommand{\tightlist}{}
\setmainfont{Lato}
\setsansfont{Lato}
\newfontfamily\headingfont{Fira Sans Condensed}
\DeclareColor{structure}[HTML]{912040}
\EditInstance{header}{std}{color = structure, font = \Large\bfseries\headingfont, height = 1.35cm}
\EditInstance{frametitle}{header}{color = structure, font = \Large\bfseries\headingfont}
\EditInstance{titlepage-element}{title}{color = structure, font = \LARGE\bfseries\headingfont}
\EditInstance{titlepage-element}{subtitle}{font = \large\bfseries}
\EditInstance{footer}{std}{element-order = {title, framenumber}}
\date{}
"""

def meta_from_qmd(text):
    def grab(key):
        m = re.search(r'^%s:\s*"?(.*?)"?\s*$' % key, text, re.M)
        return m.group(1) if m else None
    title = grab("title") or "Slides"
    subtitle = (grab("subtitle") or "").replace("<br>", r"\\")
    author = grab("author") or ""
    out = f"\\title{{{title}}}\n"
    if subtitle: out += f"\\subtitle{{{subtitle}}}\n"
    if author: out += f"\\author{{{author}}}\n"
    return out

def build(n):
    qmd = ROOT / "content" / "slides" / f"slides{n}.qmd"
    with tempfile.TemporaryDirectory() as td:
        tdp = pathlib.Path(td)
        # figures: svg -> pdf, raster copied, under assets/ relative to the tex
        adir = tdp / "assets"; adir.mkdir()
        for f in (ROOT / "assets").rglob("*"):
            rel = f.relative_to(ROOT / "assets")
            if f.suffix == ".svg":
                (adir / rel).parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["rsvg-convert", "-f", "pdf", "-o",
                                str(adir / rel.with_suffix(".pdf")), str(f)], check=True)
            elif f.suffix in (".png", ".jpg", ".jpeg"):
                (adir / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(f, adir / rel)
        # frames from pandoc's beamer writer (body only; template discarded)
        r = subprocess.run(["quarto", "pandoc", str(qmd), "-t", "beamer",
                            "--lua-filter", str(ROOT / "assets" / "beamer-deck.lua"),
                            "--standalone"], capture_output=True, text=True, check=True)
        tex = r.stdout
        body = tex.split(r"\begin{document}", 1)[1].rsplit(r"\end{document}", 1)[0]
        # With frame-title-arg every frame must carry a title argument, and a
        # bare \maketitle gets wrapped in an argument-less frame that then eats
        # the *next* frame as its argument (veraPDF: Hn shall not contain Sect).
        # So the title page is an explicit frame; the wallpaper style keeps the
        # header from printing the title twice.
        qtitle = re.search(r'^title:\s*"?(.*?)"?\s*$', qmd.read_text(), re.M).group(1)
        body = body.replace("\\frame{\\titlepage}",
                            "\\begin{frame}{%s}\\maketitle[framestyle = wallpaper]\\end{frame}" % qtitle)
        body = re.sub(r"\\begin\{columns\}\[[^\]]*\]", r"\\begin{columns}", body)
        body = re.sub(r"\[<\+\+?->?\]", "", body)          # itemize[<+->]
        body = re.sub(r"<\d+(-\d*)?>", "", body)           # \item<2-> etc.
        doc = PREAMBLE + meta_from_qmd(qmd.read_text()) + "\\begin{document}\n" + body + "\n\\end{document}\n"
        (tdp / "deck.tex").write_text(doc)
        for _ in range(2):
            subprocess.run(["lualatex", "-interaction=nonstopmode", "deck.tex"],
                           cwd=td, capture_output=True)
        pdf = tdp / "deck.pdf"
        if not pdf.exists():
            log = (tdp / "deck.log").read_text(errors="replace")
            errs = [l for l in log.splitlines() if l.startswith("!")]
            sys.exit(f"lecture {n}: compile failed:\n" + "\n".join(errs[:6]))
        v = subprocess.run(["verapdf", "--flavour", "ua2", "--format", "xml", str(pdf)],
                           capture_output=True, text=True)
        fails = re.findall(r'clause="([^"]*)"[^>]*testNumber="[^"]*"[^>]*status="failed"'
                           r'[^>]*failedChecks="([^"]*)"', v.stdout)
        if fails:
            keep = ROOT / "scripts" / f"failed-deck{n}.pdf"
            shutil.copy(pdf, keep)
            sys.exit(f"lecture {n}: deck does not pass veraPDF UA-2 "
                     f"({', '.join(f'{c} x{k}' for c, k in fails)}); kept {keep.name} for inspection")
        dest = ROOT / "content" / "slides" / f"slides{n}.pdf"
        shutil.copy(pdf, dest)
        pages = subprocess.run(["pdfinfo", str(dest)], capture_output=True, text=True)
        np = re.search(r"Pages:\s+(\d+)", pages.stdout).group(1)
        print(f"    lecture {n}: {np} pages, tagged, veraPDF ua2 PASS -> {dest.relative_to(ROOT)}")

if __name__ == "__main__":
    for n in sys.argv[1:]:
        build(n)
