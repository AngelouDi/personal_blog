title: How to properly write Greek in LaTeX
description: Using Greek in LaTeX can be problematic. Solve your problems here!
date: 03/01/2021
tags: LaTeX, Greek

Today we are gonna see how to write Ελληνικά in LaTeX

# Introduction
Writing Greek letters in LaTeX may be a pain in the arse, unless you know how to do it correctly ;)
Searching the web may guide you to this:

```
\usepackage{ucs}
\usepackage[utf8x]{inputenc}
\usepackage[greek,english]{babel}
\newcommand{\en}{\selectlanguage{english}}
\newcommand{\gr}{\selectlanguage{greek}}
```
 where you will have to prepend `\gr`, `\en` before changing the language.
 Let's not do that mkay?
 
 # The correct way
 
 Firstly, remove code above and add these packages to your LaTeX document:
 ```
\usepackage{alphabeta}
\usepackage[utf8]{inputenc}
\usepackage[greek, english]{babel}
```

You are done! Now you can write Greek anywhere in the document and it will work flawlessly.

