\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{div}
\LoadClass[12pt, letter]{article}

% Centering fixed width column
\usepackage{array}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}

% To avoid too many math letters error
\newcommand\hmmax{0}
\newcommand\bmmax{0}

% Headers and footers
\RequirePackage{fancyhdr}


% Misc Packages
\RequirePackage{comment}
\RequirePackage{enumitem}
\RequirePackage{etoolbox}
\RequirePackage[svgnames]{xcolor}

% Math
\RequirePackage{bm}
\RequirePackage{array}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsfonts}
\RequirePackage{amsthm}
\RequirePackage{mathtools}

% Font
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english]{babel}
\RequirePackage{textcomp}
%\usepackage{mathpazo}
%\usepackage{mathdesign}
%\RequirePackage{microtype}
%\RequirePackage[adobe-utopia]{mathdesign} 
\RequirePackage[bitstream-charter]{mathdesign} 


% Figures/Graphics
\RequirePackage{morefloats}
\RequirePackage{graphicx}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage[capposition=top]{floatrow}
\setlength{\belowcaptionskip}{0em}
\captionsetup{labelfont=sc, textfont=sc}
\captionsetup[floatfoot]{footfont={normal,footnotesize}, singlelinecheck=off, format=hang, width=\linewidth}

% Tables
\RequirePackage{array, multirow}
\RequirePackage{booktabs, siunitx}
\RequirePackage{tabularx}
\RequirePackage[para,flushleft]{threeparttable}
\renewcommand{\arraystretch}{1}	% spacing in tables
\AtBeginEnvironment{tablenotes}{\setstretch{1} \footnotesize}	% notes font
\newcolumntype{P}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\centering\arraybackslash}X}
\newcolumntype{C}[1]{>{\centering\arraybackslash}m{#1}}
\RequirePackage{makecell}

% Colors
\definecolor{red}{RGB}{175 , 0 , 0}
\newcommand{\red}{\textcolor{red}}
\definecolor{blue}{RGB}{0 , 0 , 170}
\newcommand{\blue}{\textcolor{blue}}

% Spacing 
\RequirePackage{setspace}
\RequirePackage{titlesec}
%\RequirePackage{indentfirst}
\setlength{\parindent}{1em}						% Paragraph Indentation
\setlength{\skip\footins}{1cm} 					% Footnote Space
\setlength{\parskip}{1mm} 						% Paragraph Skip
%\setstretch{1} 									% Line Space
\RequirePackage[margin=0.75in]{geometry} 		% Margins
\titlespacing*{\section}{0pt}{0.85\baselineskip}{0.15\baselineskip}
\titlespacing*{\subsection}{0pt}{0.85\baselineskip}{0.15\baselineskip}


% Sections & Subsections 
\titleformat*{\section}{\large \normalfont \sc}
\titleformat*{\subsection}{\fontsize{13}{1} \normalfont \itshape}

% Links
\RequirePackage{xr-hyper}
\RequirePackage[colorlinks, allcolors=NavyBlue]{hyperref}
\renewcommand\thefootnote{\textcolor{black}{\arabic{footnote}}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
