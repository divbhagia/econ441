\ProvidesClass{div}
\LoadClass[12pt]{article}
\setlength{\headheight}{15pt}
\addtolength{\topmargin}{-3pt}

% Page style
\RequirePackage{fancyhdr}

% Header and footer
\fancyhf{}
\fancyheadoffset{1cm}
\lhead{ECON 441: Introduction to Mathematical Economics}
\rhead{Div Bhagia}
\rfoot{\center \thepage}
\pagestyle{fancy}

% Custom Header: Title
\newcommand{\myheader}[1]{%
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
\vspace{1em}
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
\subsectionfont{\fontsize{13}{1} \normalfont \textit}
\subsubsectionfont{\fontsize{12}{1} \normalfont \textit}

% Itemize
\newenvironment{witemize}{\itemize\addtolength{\itemsep}{10pt}}{\enditemize}
\RequirePackage{tasks}
%\settasks{counter-format = (tsk[a])}

% Spacing 
\RequirePackage{xspace}
\RequirePackage{relsize}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\setlength{\parindent}{0em}						% Paragraph Indentation
\setlength{\skip\footins}{1cm} 					% Footnote Space
\setlength{\parskip}{3mm} 						% Paragraph Skip
\setstretch{1.25} 								% Line Space
\RequirePackage[margin=1.15in]{geometry} 		% Margins

