\LoadClass[12pt]{article}
\setlength{\headheight}{15pt}
\addtolength{\topmargin}{-3pt}

% Page style
\RequirePackage{fancyhdr}

% Header and footer
\fancyhf{}
\fancyheadoffset{1cm}
% Short course tag, not the full name: the running head is left+right with no
% glue between them, and the full name plus a title ("Worksheet: Single
% Variable Unconstrained Optimization") runs the two into each other.
\lhead{\small ECON 441}
\rhead{\small \mytitle}
\rfoot{\center \thepage}
\pagestyle{fancy}

% Custom Header: Title
% Tagging (PDF/UA-2): the \framebox{\vbox{...}} produces paragraphs nested
% inside a paragraph, which veraPDF rejects (Table 5, P-P). Paragraph tagging
% is switched off inside the box so the header tags as a single <P>. The
% \hypersetup line writes the title into the XMP metadata (dc:title, clause
% 8.11.1 requires it).
\newcommand{\myheader}[1]{%
\hypersetup{pdftitle={#1}}%
\tagpdfparaOff
\begin{center}
  \framebox{
    \vbox{
    \vspace{0em}
     \Large \sc #1 \\ 
     \vspace{0.25em}
      \small ECON 441: Introduction to Mathematical Economics \hfill Instructor: Div Bhagia
      }
    }
\end{center}	
\tagpdfparaOn
%\vspace{1em}
}


% Misc packages
\RequirePackage{latexsym}
\RequirePackage{tgbonum}
\RequirePackage{amsfonts,epsfig}
\RequirePackage{docmute}

% Tables and columns
\RequirePackage{tabularx}
\RequirePackage{multicol}
\RequirePackage{subcaption}

% Figures and plots
\RequirePackage{tikz}
\RequirePackage{venndiagram}
\RequirePackage{pgfplots}
\RequirePackage{epsfig}

% Math and Font
\RequirePackage[default]{lato}
%\RequirePackage{mathastext}
\RequirePackage{newtxmath}
\RequirePackage[english]{babel}
\RequirePackage[utf8x]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{listings}
%\RequirePackage{amssymb, amsfonts, amsmath, amsthm}
\RequirePackage{bm}

% Sections & Subsections
\RequirePackage{sectsty}
\renewcommand{\thesection}{\arabic{section}} 
\renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}} 
\sectionfont{\large \normalfont \sc}
% \itshape, not \textit: sectsty prepends these tokens to the heading, and
% \textit takes an argument -- it swallows the heading machinery, so under
% tagging the H2 structure never closes and everything after nests inside it
% (veraPDF: Hn shall not contain P/Part/Hn/...). A font *switch* is safe.
\subsectionfont{\fontsize{13}{1} \normalfont \itshape}
\subsubsectionfont{\fontsize{12}{1} \normalfont \itshape}

% Itemize
\newenvironment{witemize}{\itemize\addtolength{\itemsep}{10pt}}{\enditemize}
\RequirePackage{tasks}
%\settasks{counter-format = (tsk[a])}

% Spacing 
\RequirePackage{xspace}
\RequirePackage{relsize}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\setlength{\parindent}{0em}						      % Paragraph Indentation
\setlength{\skip\footins}{1cm} 				      % Footnote Space
\setlength{\parskip}{3mm} 						      % Paragraph Skip
\setstretch{1.15} 								          % Line Space
\RequirePackage[margin=1.15in]{geometry} 		% Margins

% For pdftitle metadata (PDF/UA-2 requires dc:title). Loaded last, links hidden.
\RequirePackage[hidelinks]{hyperref}

% ToUnicode mappings for extensible-symbol pieces that newtx's txexs font
% leaves unmapped (PDF/UA-2 clause 8.4.5.8 requires every used glyph to map
% to Unicode). These are construction pieces of big parens and vertical bars.
\ifdefined\pdfglyphtounicode\else
  \protected\def\pdfglyphtounicode{\pdfextension glyphtounicode }
\fi
\pdfglyphtounicode{barex}{007C}
\pdfglyphtounicode{parenlefttpA}{0028}
\pdfglyphtounicode{parenleftexA}{0028}
\pdfglyphtounicode{parenleftbtA}{0028}
\pdfglyphtounicode{parenrighttpA}{0029}
\pdfglyphtounicode{parenrightexA}{0029}
\pdfglyphtounicode{parenrightbtA}{0029}
\pdfglyphtounicode{bracehext}{23AA}
