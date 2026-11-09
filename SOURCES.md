# Design sources and provenance

Lumenbook is a new implementation under the LaTeX Project Public License,
version 1.3c or (at your option) any later version. The unmodified license
text is in `LICENSE` (copied from the local subook distribution). The new
class and style files form the maintained work `lumenbook`; its maintenance
status is author-maintained by the owner of this workspace.

## Primary source: subook

The local `references/subook/subook.cls` identifies Changxing Su as its author, dates
the class to 2021/12/27, and permits distribution and modification under
LPPL 1.3 or later.

Retained design direction:

- Standard `book` as the underlying document class.
- A4 text block with a large right sidebar, approximately 5 cm wide.
- Short text-note commands `\mn` and `\sn`, rich margin figures and tables.
- Colors that distinguish definitions, theorems and examples.
- Separately useful chapter headings and running page furniture.

Reimplemented rather than copied: option handling, geometry, all note and
environment definitions, typography and the chapter/title-page design.
In particular, the private `\@mn@@@marginnote` override was not carried
forward. Native one-sided/two-sided page layout now controls the side.

## Secondary design reference: kaobook

The local kaobook snapshot identifies version 0.9.8 (2021/08/23), Federico
Marotta, work by Ken Arroyo Ohori and Tufte-LaTeX, and template changes by
Vel at LaTeXTemplates.com. Its license is LPPL 1.3 or later.

Reference files: `references/kaobook-master/kaobook.cls`, `kao.sty`, and
`kaotheorems.sty`. The design references are modular configuration,
calm shaded panels, breakable theorem backgrounds, and outer margins
for book spreads. Lumenbook does not load kaobook or KOMA-Script and does
not copy their internal layout commands or theorem declarations.

The original project snapshots are grouped under `references/`. Their file
contents remain unchanged, and they are not dependencies of the new class.
Their own licenses continue to apply to them. TeX build intermediates are
excluded from Git by the repository's ignore rules.

## Other packages

CTeX, fontspec, unicode-math, tcolorbox, fvextra, marginnote, geometry,
caption, fancyhdr and the other dependencies retain their respective
licenses. They are loaded from the user's TeX distribution, not bundled
or modified here. The mathematical demonstration text and test fixtures
were written for this template; they do not reproduce a textbook excerpt.

## Local fonts in v1.1

The `fonts/` directory contains the user's existing files. They are loaded
by filename in preference to distribution fonts for the matching roles.
The source-code LPPL does not relicense third-party font files. Font roles,
character-coverage boundaries and fallback behavior are recorded in
`fonts/README.md` and `VALIDATION.md`.

## Reading marks in v1.2

`lumen-mark.sty` provides one interface over xeCJKfntef (XeLaTeX) or
lua-ul / luacolor (LuaLaTeX). These dependencies are unmodified and retain
their own licenses. The wrapper commands, palette, paragraph background,
math-fragment wrapper, annotation example and Lua wave drawing are new
template code.

## Study tools in v1.3

`lumen-study.sty` adds original study panels, checklist drawings, manually
specified progress bars and version switches. It loads unmodified cleveref
for reference formatting and comment for skipping hidden solution/hint
bodies. Their licenses remain their own. A small guarded adapter delegates
old cleveref reset-parent lookup through the 2026 kernel's real counter;
the observed cross-chapter compatibility issue and checks are recorded in
`VALIDATION.md`. The mathematical study gallery is an original template
example rather than an excerpt from an external textbook.
