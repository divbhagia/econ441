\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{div_teaching_slides}
\LoadClass[14pt, aspectratio=169, t]{beamer} % normal is 43
\usetheme{default}

% Misc Packages
\RequirePackage{comment}
\RequirePackage{changepage}
\RequirePackage{animate}
\RequirePackage{setspace}
\RequirePackage{soul} % Highlighting
\RequirePackage{venndiagram}
\RequirePackage{tikz}
\RequirePackage{pgfplots}
\usetikzlibrary{arrows.meta}

% Figures/Graphics
\RequirePackage{morefloats}
\RequirePackage{graphicx}
\RequirePackage{caption}
\RequirePackage{subcaption}

% Itemize
\newenvironment{witemize}{\itemize\addtolength{\itemsep}{10pt}}{\enditemize}
\newenvironment{mitemize}{\vspace{1pt}\itemize\addtolength{\itemsep}{5pt}}{\enditemize}
\setbeamertemplate{itemize items}[circle]
\setbeamertemplate{itemize subitems}[circle]


% Fonts & Text
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english]{babel}
\RequirePackage[default]{lato}
\RequirePackage[charter]{mathdesign}

% Math
\RequirePackage{amsthm}
\RequirePackage{amsmath} 
\RequirePackage{amsfonts}
\RequirePackage{mathabx}
\RequirePackage{exscale, relsize}

% Tables and Graphics
\RequirePackage[scr]{rsfso}
\RequirePackage{tabularx}
\RequirePackage{booktabs}
\RequirePackage{graphicx}
\RequirePackage{dcolumn}
\RequirePackage{tikz}
\RequirePackage{tikzsymbols}
\usetikzlibrary{positioning,calc,matrix,shapes.multipart,backgrounds,arrows}
\RequirePackage{xsavebox}
\newcolumntype{P}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\centering\arraybackslash}X}

% Colors
\definecolor{red}{RGB}{175 , 0 , 0}
\definecolor{blue}{RGB}{0 , 0, 175}
\definecolor{green}{RGB}{75, 150 ,0}
\definecolor{purple}{RGB}{108, 0 ,108}
\definecolor{grey}{RGB}{225 , 225 ,225}
\definecolor{dgrey}{RGB}{125 , 125 ,125}
\definecolor{ddgrey}{RGB}{60 , 60 ,60}
\definecolor{midgrey}{RGB}{100 , 100 ,100}
\definecolor{bgcolor}{RGB}{255 , 255 , 255}
\definecolor{maroon}{RGB}{145, 0.0, 0.0}

% Text Color Macros
\newcommand{\blue}{\textcolor{blue}}
\newcommand{\red}{\textcolor{red}}
\newcommand{\green}{\textcolor{green}}
\newcommand{\purple}{\textcolor{purple}}
\newcommand{\ddgrey}{\textcolor{ddgrey}}
\newcommand{\maroon}{\textcolor{maroon}}
\renewcommand{\alert}{\textcolor{maroon}}

% Theorems & Assumptions
\setbeamertemplate{blocks}[rounded][shadow=false]
\makeatletter
\def\th@mystyle{%
\normalfont 
\setbeamercolor{block title example}{bg=ddgrey,fg=bgcolor}
\setbeamercolor{block body example}{bg=grey!20, fg=ddgrey}
\def\inserttheoremblockenv{exampleblock}
}
\makeatother
\theoremstyle{plain}
\theoremstyle{mystyle}
\setbeamertemplate{theorems}[numbered]
\newtheorem{assump}{Assumption}
\newtheorem{prop}{Proposition}
\newtheorem{corr}{Corollary}

% Margins
\setbeamersize{text margin left=2em, text margin right=2em} 
\addtolength{\headsep}{0.25cm}
\setbeamertemplate{frametitle}{
    \insertframetitle \\ \vspace{0.1em}
}

% Footer
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{\hspace{14cm}\footnotesize \insertframenumber{} / \inserttotalframenumber \vspace{1em}}


% Section page
\AtBeginSection[]{
  \begin{frame}
  \vfill
  \centering
  \begin{beamercolorbox}[center, sep=6em]{title}
    \usebeamerfont{title}{\insertsectionhead}\par%
  \end{beamercolorbox}
  \vfill
  \end{frame}
}


% Setting Colors
\setbeamercolor{normal text}{fg=black}
\setbeamercolor{title}{fg=maroon}
\setbeamercolor{frametitle}{fg=maroon}
\setbeamercolor{structure}{fg=black}
%\setbeamercolor{author}{fg=red}
%\setbeamercolor{institute}{fg=blue}
\setbeamercolor{alerted text}{fg=red}
\setbeamercolor{background canvas}{bg=bgcolor}
\setbeamercolor{button}{fg=ddgrey, bg=grey}

% Tikz Symbols
\tikzstyle{arrow} = [thick,->,>=stealth]
\tikzstyle{box} = [rectangle, rounded corners, minimum width=1cm, minimum height=1cm,text centered, draw=black, fill=dgrey, fill opacity=0.1, text opacity=1]
\tikzstyle{boxW} = [rectangle, rounded corners, text centered, draw=black]
\tikzstyle{boxd} = [rectangle, thick, rounded corners, text centered, draw=red]
\tikzstyle{box1} = [rectangle, thick, rounded corners, minimum width=1cm, minimum height=1cm,text centered, draw=red, fill=red, fill opacity=0.02, text opacity=1]
\tikzstyle{box2} = [rectangle, thick, rounded corners, minimum width=1cm, minimum height=1cm,text centered, draw=blue, fill=blue, fill opacity=0.02, text opacity=1]

% Custom Definitions
\newcommand{\E}{\index{Expected Value}\text{$\mathbb{E}$\kern.3pt}}
\newcommand{\I}{\index{Indicator Function}\text{$\mathbb{I}$\kern.3pt}}

% Appendix Numbering
\newcommand{\backupbegin}{
   \newcounter{framenumberappendix}
   \setcounter{framenumberappendix}{\value{framenumber}}
   \addtocounter{framenumber}{-\value{framenumber}}
   \setbeamertemplate{footline}{\hspace{13.25cm}APPENDIX \hspace{0.25em} SLIDE \hspace{0.25em}  \insertframenumber{} \vspace{0.4em}}
}
\newcommand{\backupend}{
   \addtocounter{framenumberappendix}{-\value{framenumber}}
   \addtocounter{framenumber}{\value{framenumberappendix}} 
}
