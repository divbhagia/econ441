"""Single source of truth for the course schedule.

Emits two artifacts from one data definition:
  syllabus/schedule.tex   - rows for the LaTeX syllabus table (print)

Run from the project root:  python3 syllabus/create_schedule.py
"""
import datetime as dt
import pathlib

YEAR = 2026
FIRST, LAST = (8, 24), (12, 9)
FINAL_EXAM = ("Mon 12/14", "5:00--6:50 PM")

HOLIDAYS = {
    dt.date(YEAR, 9, 7): "Labor Day",
    dt.date(YEAR, 11, 11): "Veterans Day",
    dt.date(YEAR, 11, 23): "Fall Recess",
    dt.date(YEAR, 11, 25): "Fall Recess",
}

MODULE_SLUG = {"Preliminaries":"preliminaries","Linear Algebra":"linear-algebra",
               "Calculus":"calculus","Optimization":"optimization"}

MODULES = [
    ("Preliminaries",     dt.date(YEAR, 8, 24),  dt.date(YEAR, 8, 26)),
    ("Linear Algebra",    dt.date(YEAR, 8, 31),  dt.date(YEAR, 9, 16)),
    ("Calculus",          dt.date(YEAR, 9, 28),  dt.date(YEAR, 10, 14)),
    ("Optimization",      dt.date(YEAR, 10, 26), dt.date(YEAR, 11, 18)),
    ("Additional Topics", dt.date(YEAR, 11, 30), dt.date(YEAR, 12, 2)),
]

# date -> (lecture number or None, topics, references, [(worksheet file, label), ...])
LECTURES = {
 dt.date(YEAR,8,24):  (1,"Course introduction; numbers and sets","2.2, 2.3",[("Handout-Sets.pdf","Sets")]),
 dt.date(YEAR,8,26):  (2,"Functions, summation notation, and logical conditions","2.4-2.6, p. 163, 5.1",[("Handout-Functions.pdf","Functions"),
                       ("Handout-Summation-Notation.pdf","Summations")]),
 dt.date(YEAR,8,31):  (3,"Matrices; addition, subtraction, scalar and matrix multiplication","4.1, 4.2",[("Handout-Matrix-Operations.pdf","Matrix Operations")]),
 dt.date(YEAR,9,2):   (4,"Matrix multiplication; vectors; linear dependence; identity, null, idempotent, and transpose matrices","4.2-4.6",[]),
 dt.date(YEAR,9,9):   (5,"Inverse of a matrix; conditions for nonsingularity","4.6, 5.1",[]),
 dt.date(YEAR,9,14):  (6,"Inverse; nonsingularity; rank; the determinant","4.6, 5.1, 5.2",[("Handout-Determinant-and-Inverse.pdf","Determinant and Inverse")]),
 dt.date(YEAR,9,16):  (7,"Computing determinants; inversion; Cramer's rule; applications","5.2-5.5, 4.7",[("Handout-Solving-System-of-Equations.pdf","Solving Systems of Equations")]),
 dt.date(YEAR,9,28):  (None,"Limit definition of a derivative; limits","6.2-6.4",[]),
 dt.date(YEAR,9,30):  (None,"Continuity; rules of differentiation","6.7, 7.1-7.3",[]),
 dt.date(YEAR,10,5):  (None,"Exponential and log functions","10.5",[]),
 dt.date(YEAR,10,7):  (None,"Partial derivatives; total differential and derivative","7.4, 8.1, 8.2, 8.4",[]),
 dt.date(YEAR,10,12): (None,"Implicit function theorem","8.5",[]),
 dt.date(YEAR,10,14): (None,"Integration","14.1-14.3",[]),
 dt.date(YEAR,10,26): (None,"Unconstrained single-variable optimization","9.1, 9.2",[]),
 dt.date(YEAR,10,28): (None,"Concave and convex functions","9.3, 9.4",[]),
 dt.date(YEAR,11,2):  (None,"Multivariable optimization: first-order conditions","11.1",[]),
 dt.date(YEAR,11,4):  (None,"Multivariable optimization: second-order conditions","11.2",[]),
 dt.date(YEAR,11,9):  (None,"Constrained optimization; the Lagrange method","12.1, 12.2",[]),
 dt.date(YEAR,11,16): (None,"Envelope theorem","11.5",[]),
 dt.date(YEAR,11,18): (None,"Quasiconcavity; convex sets; homogeneous functions","12.4, 12.6",[]),
 dt.date(YEAR,11,30): (None,"To be announced","",[]),
 dt.date(YEAR,12,2):  (None,"To be announced","",[]),
}

SPECIAL = {
 dt.date(YEAR,9,21): "Midterm 1 review",
 dt.date(YEAR,9,23): "Midterm Exam 1",
 dt.date(YEAR,10,19):"Midterm 2 review",
 dt.date(YEAR,10,21):"Midterm Exam 2",
 dt.date(YEAR,12,7): "Final review",
 dt.date(YEAR,12,9): "Final review",
}
# Lectures whose materials have been vetted and published.
# Add numbers here as each module is checked, then rerun ./build.sh all
PUBLISHED = {1, 2, 3, 4}

QUIZZES = {dt.date(YEAR,9,9):1, dt.date(YEAR,10,12):2, dt.date(YEAR,11,9):3, dt.date(YEAR,11,30):4}


def class_dates():
    out, d = [], dt.date(YEAR, *FIRST)
    end = dt.date(YEAR, *LAST)
    while d <= end:
        if d.weekday() in (0, 2):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def module_for(d):
    for name, a, b in MODULES:
        if a <= d <= b:
            return name
    return None


DATES = class_dates()
SPANS = {}
for _d in DATES:
    _m = module_for(_d)
    if _m:
        SPANS[_m] = SPANS.get(_m, 0) + 1


def build_latex():
    lines, seen, prev_mod = [], set(), object()
    for d in DATES:
        ds = d.strftime("%a %-m/%-d")
        m = module_for(d)
        rule = "\\hline\n" if (lines and m != prev_mod) else ""
        prev_mod = m
        if m and m not in seen:
            seen.add(m)
            mod = f"\\textbf{{{m}}}"   # multirow breaks across longtable pages
        else:
            mod = ""
        quiz = f"\\textbf{{Quiz {QUIZZES[d]}}}; " if d in QUIZZES else ""
        if d in HOLIDAYS:
            lines.append(rule + f"{mod} & {ds} & \\multicolumn{{2}}{{l}}{{\\textit{{No class ({HOLIDAYS[d]})}}}} \\\\")
        elif d in SPECIAL:
            lines.append(rule + f"{mod} & {ds} & \\multicolumn{{2}}{{l}}{{\\textbf{{{SPECIAL[d]}}}}} \\\\")
        elif d in LECTURES:
            _, tp, rf, _ = LECTURES[d]
            lines.append(rule + f"{mod} & {ds} & {quiz}{tp} & {rf} \\\\")
        else:
            lines.append(rule + f"{mod} & {ds} & {quiz} & \\\\")
    lines.append(f" & {FINAL_EXAM[0]} & \\multicolumn{{2}}{{l}}{{\\textbf{{Final Exam}}, {FINAL_EXAM[1]}}} \\\\")
    body = "\n".join(lines)
    if body.rstrip().endswith("\\\\"):
        body = body.rstrip()[:-2].rstrip()   # drop trailing \\ on the last row
    pathlib.Path("syllabus/schedule.tex").write_text(body + "\n")
    return len(lines)


def icons(n, sheets):
    o = [f'<a href="content/slides/slides{n}.html" target="_blank" rel="noopener" '
         f'aria-label="Lecture {n} slides (opens in a new tab)"><span aria-hidden="true">🖥️</span></a>',
         # The tagged PDF of the same deck: complete slides, no overlays, the
         # version to study from or print.
         f'<a href="content/slides/slides{n}.pdf" target="_blank" rel="noopener" '
         f'aria-label="Lecture {n} slides as tagged PDF (opens in a new tab)">'
         f'<span aria-hidden="true">📑</span></a>']
    # One icon per worksheet; the aria-label names it, so two sheets on the same
    # lecture stay distinguishable to a screen reader.
    for ws, wsl in sheets:
        o.append(f'<a href="content/handouts/{ws.lower()}" target="_blank" rel="noopener" '
                 f'aria-label="Lecture {n} worksheet: {wsl}, PDF (opens in a new tab)"><span aria-hidden="true">🗒️</span></a>')
    o.append(f'<a href="content/practice/practice{n}.html" target="_blank" rel="noopener" '
             f'aria-label="Practice Problems {n} (opens in a new tab)"><span aria-hidden="true">✍️</span></a>')
    return " ".join(o)


def esc(t):
    return t.replace("'", "&rsquo;").replace("-", "&ndash;") if False else t.replace("'", "&rsquo;")


def build_html():
    rows, seen, prev_mod = [], set(), object()
    for d in DATES:
        ds = d.strftime("%a %-m/%-d")
        m = module_for(d)
        starts = (m != prev_mod)   # only when the block actually changes
        prev_mod = m
        if m and m not in seen:
            seen.add(m)
            label = (f'<a href="content/{MODULE_SLUG[m]}.html">{m}</a>' if m in MODULE_SLUG else m)
            # Phones drop the module column and use this full-width heading row
            # in its place. Exactly one of the two is displayed at any width, so
            # the module name is never announced twice.
            rows.append(f'<tr class="module-head"><th scope="colgroup" colspan="5">{label}</th></tr>')
            mod = f'<th scope="rowgroup" rowspan="{SPANS[m]}" class="module">{label}</th>'
        elif m:
            mod = ""
        else:
            mod = '<td class="modblank"></td>'
        quiz = f"<strong>Quiz {QUIZZES[d]}</strong>; " if d in QUIZZES else ""
        edge = " module-start" if starts else ""
        date = f'<th scope="row">{ds}</th>'
        if d in HOLIDAYS:
            rows.append(f'<tr class="recess{edge}">{mod}{date}'
                        f'<td class="note" colspan="3">No class ({HOLIDAYS[d]})</td></tr>')
        elif d in SPECIAL:
            rows.append(f'<tr class="assessment{edge}">{mod}{date}'
                        f'<td class="note" colspan="3">{quiz}<strong>{SPECIAL[d]}</strong></td></tr>')
        else:
            if d in LECTURES:
                n, tp, rf, sheets = LECTURES[d]
                tp, mat = esc(tp), (icons(n, sheets) if (n and n in PUBLISHED) else "")
            else:
                tp, rf, mat = "", "", ""
            # References appear twice: as a column on wide screens, and folded
            # under the topic on phones. CSS shows one and hides the other.
            fold = f'<span class="refs-inline">Reference: {rf}</span>' if rf else ""
            rows.append(f'<tr class="{edge.strip()}">{mod}{date}'
                        f'<td class="topics">{quiz}{tp}{fold}</td>'
                        f'<td class="refs">{rf}</td><td class="mat">{mat}</td></tr>')
    rows.append(f'<tr class="assessment"><td class="modblank"></td><th scope="row">{FINAL_EXAM[0]}</th>'
                f'<td class="note" colspan="3"><strong>Final Exam</strong>, {FINAL_EXAM[1].replace("--","&ndash;")}</td></tr>')

    # Column widths live in assets/styles.css so that the media queries there
    # can override them; with table-layout:fixed only this row sets them.
    table = ('<div class="table-scroll" tabindex="0" role="region" aria-label="Semester schedule table">\n'
             '<table class="schedule-table" aria-label="Fall 2026 course schedule, '
             'one row per class meeting">\n'
             '<thead>\n<tr>\n'
             '  <th scope="col" class="col-module">Module</th>\n'
             '  <th scope="col" class="col-date">Date</th>\n'
             '  <th scope="col" class="col-topics">Topics</th>\n'
             '  <th scope="col" class="col-refs">References</th>\n'
             '  <th scope="col" class="col-mat">Materials</th>\n'
             '</tr>\n</thead>\n<tbody>\n'
             + "\n".join(rows) + '\n</tbody>\n</table>\n</div>\n')
    page = """---
title: "Schedule"
sidebar: false
---

This is a tentative schedule for the semester. Topics and their order may be adjusted as we establish a suitable pace for the class. Materials are linked next to each lecture as we reach it; for materials organized by module, see the [Content](content/preliminaries.qmd) pages.

Quizzes are given at the start of class on the dates marked below.

<p class="materials-legend">
<span aria-hidden="true">\U0001F5A5️</span> Slides &nbsp;
<span aria-hidden="true">\U0001F4D1</span> Slides (PDF) &nbsp;
<span aria-hidden="true">\U0001F5D2️</span> Worksheet (PDF) &nbsp;
<span aria-hidden="true">✍️</span> Practice problems
</p>

```{=html}
""" + table + """```
"""
    pathlib.Path("schedule.qmd").write_text(page)
    return len(rows)


if __name__ == "__main__":
    print("LaTeX rows:", build_latex(), "->", "syllabus/schedule.tex")
    print("HTML rows: ", build_html(), "-> schedule.qmd")
