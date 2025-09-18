%% econ405.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{syllabus}

% Base class
\LoadClass[12pt]{article}

%% ----------------------------
%% Sections & Subsections
%% ----------------------------
\usepackage{titlesec}
\titleformat*{\section}{\fontsize{16}{1} \bfseries}
\titleformat*{\subsection}{\fontsize{13}{1} \bfseries}
\titleformat*{\subsubsection}{\fontsize{13}{1} \itshape}

%% ----------------------------
%% Language settings
%% ----------------------------
\usepackage[american]{babel}

%% ----------------------------
%% Font settings
%% ----------------------------
\usepackage{fontspec}
\setmainfont{Source Sans Pro}
\setsansfont{Fira Sans}
\setmonofont{TeX Gyre Cursor}

%% ----------------------------
%% Page layout and spacing
%% ----------------------------
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{setspace}
\onehalfspacing

%% ----------------------------
%% List customization
%% ----------------------------
\usepackage{enumitem}
\setlist[itemize]{itemsep=0pt, parsep=0pt, topsep=0.25\baselineskip}
\newlist{flatlist}{itemize}{1}
\setlist[flatlist]{label={}, leftmargin=0pt, itemsep=0pt, parsep=0pt, topsep=0pt}

%% ----------------------------
%% Figures, tables, captions
%% ----------------------------
\usepackage{graphicx}
\usepackage{array, multirow}
\usepackage{booktabs, siunitx}
\usepackage{tabularx}
\usepackage{makecell}
\newcolumntype{P}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\centering\arraybackslash}X}
\newcolumntype{C}[1]{>{\centering\arraybackslash}m{#1}}

%% ----------------------------
%% Tagging for accessibility
%% ----------------------------
\usepackage{tagpdf}
\tagpdfsetup{
  activate-all=true,
  interwordspace=true
}

%% ----------------------------
%% Color definitions
%% ----------------------------
\usepackage{xcolor}
\definecolor{annotationblue}{RGB}{0,77,153}
\definecolor{suggestionred}{RGB}{153,0,0}
\definecolor{NavyBlue}{RGB}{0 , 0 , 125}

%% ----------------------------
%% Hyperlinks and PDF metadata
%% ----------------------------
\usepackage[
  pdfusetitle,
  pdflang=en-US,
  pdfstartview=FitH,
  pdfdisplaydoctitle=true
]{hyperref}

\hypersetup{
  unicode=true,
  colorlinks=true,
  linkcolor=NavyBlue,
  urlcolor=NavyBlue,
  citecolor=NavyBlue,
  pdftitle={},
  pdfauthor={},
  pdfsubject={},
  pdfkeywords={},
  pdfborderstyle={/S/U/W 1}
}
\urlstyle{same}

%% ----------------------------
%% Accessibility enhancements
%% ----------------------------
\setlistdepth{3}

%% ----------------------------
%% Course header
%% ----------------------------
\newcommand{\courseheader}[4]{%
\begin{center}
\includegraphics[scale=0.5]{#4}  \vspace{0.35em} \\
{\fontsize{16}{1} \textbf{#3}} \vspace{0.35em} \\
{\fontsize{16}{1} \textbf{#1}} \\ \vspace{0.35em}
{\fontsize{16}{1} \textbf{#2}}
\end{center} \vspace{-0.75em}
}

%% ----------------------------
%% End of class
%% ----------------------------
\endinput