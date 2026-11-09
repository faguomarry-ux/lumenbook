# Validation record

Date: 2026-11-09 (Asia/Shanghai).

Current revision: v1.3, study-workflow edition, retaining local fonts,
numbered code and reading annotations.

## Environment

- Windows workspace, TeX Live 2026.
- XeTeX 0.999998; LuaHBTeX 1.24.0.
- latexmk 4.88.
- Local Times New Roman four-face family and 0xProto Nerd Font Mono Bold.
- System SimSun for ordinary Chinese, local SimSun-ExtB / SimSun-ExtG for
  extension characters; Fandol Hei / Fang / bold Song / Kai for CJK roles.
- TeX Gyre Heros for auxiliary labels and TeX Gyre Termes Math for mathematics.
- TeX Gyre Termes / Fandol / Latin Modern Mono in the portable font configuration.
- Poppler rendering, PyMuPDF PDF-coordinate inspection, Pillow contact sheets.

## Checks performed

The build script compiles each source until labels stabilize, then checks
its final log for errors, missing glyphs, undefined references, undefined
font shapes and overfull horizontal/vertical boxes.

| Input | Purpose | XeLaTeX | LuaLaTeX |
| --- | --- | --- | --- |
| `main.tex` | Actual starter document | Passed | Passed |
| `demo-screen.tex` | Default right sidebar, English and Chinese, all content types | Passed, 8 pages | Passed, 8 pages |
| `demo-print.tex` | Mirrored outer sidebar with 4 mm binding allowance | Passed, 8 pages | Passed, 8 pages |
| `examples/minimal-chinese.tex` | Chinese names, indigo theme, Chinese code and captions | Passed, 2 pages | Passed, 2 pages |
| `tests/features.tex` | Outer margins, 10 pt, pinned notes inside a box, scaled table, file input | Passed, 2 pages | Passed, 2 pages |
| `tests/features-screen.tex` | Right margins, 12 pt, grayscale, unboxed theorems | Passed, 2 pages | Passed, 2 pages |
| `tests/long-content.tex` | Theorem, reading panel and code across page breaks | Passed, 5 pages | Passed, 5 pages |
| `tests/fonts-code.tex` | Local font faces, extension characters, line numbering and language labels | Passed, 1 page | Passed, 1 page |
| `tests/portable-fonts.tex` | Explicit `fonts=tex` fallback without local font faces | Passed, 1 page | Passed, 1 page |
| `examples/annotations.tex` | Bilingual underlines, waves, strikeout, five highlights, annotated terms and PDF headings | Passed, 2 pages | Passed, 2 pages |
| `tests/annotations-print.tex` | Mirrored margin annotations and monochrome palette | Passed, 2 pages | Passed, 2 pages |
| `tests/annotations-long.tex` | Colored block across pages and math styles | Passed, 2 pages | Passed, 2 pages |
| `examples/study-tools.tex` | Study panels, references, solutions, checklist and progress | Passed, 3 pages | Passed, 3 pages |
| `tests/study-hidden.tex` | Chinese print edition without solutions or hints | Passed, 3 pages | Passed, 3 pages |
| `tests/study-nohints.tex` | Solutions visible but hints hidden | Passed, 3 pages | Passed, 3 pages |
| `tests/study-refs.tex` | All theorem types, cross-chapter sorting and links | Passed, 2 pages | Passed, 2 pages |

`scripts/inspect-pdfs.py` reads the generated PDFs rather than inferring
behavior from class option values. It verifies:

- An odd-page sidebar stays to the right in both modes.
- Body page 2 places the sidebar to the right in screen mode and to the
  left in print mode. The body block moves with it.
- The geometry is restored on body page 6 after `widepage`.
- All text spans of the two demonstrations stay inside the paper.
- Pinned and floating notes both follow the selected side, including a
  pinned note issued inside a tcolorbox and a pinned margin figure.
- The 10 pt and 12 pt options produce the corresponding actual PDF font sizes.
- Chinese and external code-file content are present in the feature PDFs.
- Start/end markers of the long theorem, reading box and code occur on
  different pages, with the final marker present.
- All four Times New Roman faces, 0xProto, SimSun-ExtB and SimSun-ExtG are
  actually embedded in the font/code test PDF.
- U+20000 and U+30000 survive extraction; the extension fonts are used.
- Optional and no-option verbatim environments both preserve their first
  source line, including a leading hash character and Chinese comments.
- `firstnumber=12` places the number 12 beside the first source line.
- File extension inference produces Python labels; an explicit override
  produces the requested Pseudo label.
- The portable configuration uses TeX fonts, without Times New Roman or
  0xProto being embedded.

For the XeLaTeX previews, the even-page glossary starts at approximately
464.98 pt from the left edge in screen mode and 73.79 pt in print mode.
The even-page section heading starts at approximately 109.78 pt and
234.51 pt, respectively. The glossary position includes its caption label;
it is not the sidebar's geometric edge.

Both full demonstration PDFs were rendered with Poppler. Contact sheets
were visually checked for title and contents layout, parity, headings,
color panels, table scaling, Chinese, mathematics, code and geometry
restoration. Feature and cross-page outputs were also rendered and checked.
Intermediate images and machine-readable reports are under `tmp/pdfs/`.
The coordinate and page-break checks also passed for the LuaLaTeX PDFs,
and the rendered LuaLaTeX print demonstration was visually checked.

## Expected package messages

The installed `unicode-math` emits two compatibility notices for
`mathtools`: bracket-command selection and colon-command replacement.
These are retained in the logs. Unicode math uses its own colon glyphs;
the mathtools bracket commands remain available, with the Unicode variants
available under the names given in that package's notice. There are no
font substitutions, missing characters or unresolved labels in the final
XeLaTeX demonstrations.

LuaLaTeX additionally reports a microtype/luatexja configuration notice
about unknown protrusion slots, and an epstopdf notice because shell escape
is disabled. EPS conversion is not used; the examples use native TikZ/PDF
graphics. The long-content test's lipsum text falls back to English
hyphenation for its Latin filler paragraphs. These notices do not represent
missing characters in the rendered examples. No overfull boxes, missing
glyph errors or unresolved references were found in either build matrix.

## Font coverage and listing behavior

The actual supplied font character maps were inspected with PyMuPDF.
`simsunb.ttf` identifies itself as SimSun-ExtB Regular, not a bold face.
Neither it nor SimSun-ExtG contains U+4E00--U+9FFF common Han characters.
Common Chinese therefore uses a normal Song face. XeLaTeX uses xeCJK
fallback families; LuaLaTeX uses CTeX CharRange alternate families, preserving
the CJK font metrics needed for line spacing and punctuation.

The only local 0xProto face is Bold. It is used directly, rather than
claiming that a Regular face was provided. The math font is a Times-compatible
TeX font because the local folder does not supply a mathematical font.

Listing numbers count source lines, including blank lines. Wrapping a long
source line does not create a new source line number. The label indicates
the selected or inferred language; it does not imply syntax highlighting.

## Reading annotations (v1.2)

The annotation profiles form part of the build matrix under XeLaTeX and
LuaLaTeX. In addition to the earlier checks, PDF inspection verifies:

- Long underlined and highlighted passages wrap onto multiple lines with
  their start and end text preserved.
- All five predefined highlight colors occur in the actual drawing operations.
- The print/mono annotation sample uses grayscale drawing colors.
- A heading containing a highlight command has a plain-text PDF outline title.
- The start and end of a long `markblock` occur on different pages, followed
  by the expected text after the environment.

The annotation demonstrations were rendered and visually inspected for
Chinese and English line effects, background layering, math, numbered margin
annotations, lists and code. Standard emphasis remains italic. XeLaTeX uses
xeCJKfntef with normalem; LuaLaTeX uses lua-ul and luacolor, plus a small
custom wave pattern. The textual annotation interface is the same in both.

The downloadable annotation preview is two pages. Inline text commands are
intended for a single paragraph; long multi-paragraph passages use `markblock`.
Display math uses a block or the math-aware `mathmark`, which itself is an
unbreakable formula fragment. Extremely long words still need break points.

## Study workflow (v1.3)

The final 16-source matrix passed with XeLaTeX and LuaLaTeX (32 build
configurations). Both engines passed the PDF inspection script. The packaged
reading and hidden-answer editions also compiled after extraction into an
independent directory containing the bundled local fonts.

The study gallery is three pages. Independent profiles exercise both hidden
solutions/hints and visible solutions with hidden hints. The reference test
is two pages and spans two chapters, with all nine theorem-like types.
The PDF inspection script checks actual output for:

- Correct Definition, Theorem, Lemma and Exercise names alongside the shared
  numerical sequence.
- Correct cross-chapter order (definitions 1.2 and 2.1) and capitalized plural
  references (Definitions 2.1 and 2.2).
- Resolved links to both chapter destinations.
- Solution prose, its code block and the answer-equation label being absent
  from the hidden edition; visible exercise 1.4 stays the same in all editions.
- Hint prose being independently controlled.
- Chinese study-panel labels in the hidden print profile.
- Both the margin and body progress bars having an actual drawn fraction of
  3/8, matching the supplied values.

The installed cleveref 0.21.4 predates the 2026 kernel's native counter
aliases. Without an adapter, alias reference data loses its chapter prefix,
which sorts definition 2.1 before definition 1.2. `lumen-study` includes a
version-gated reset-parent adapter for that old cleveref version, while
retaining the original reference type. The cross-chapter test covers this
observed compatibility issue. Older kernels use public environment hooks
and cleveref aliases for the shared-counter names.

Solution/hint hiding uses the comment package to skip execution, including
verbatim code. End markers must stand alone at the start of a line.
Progress and checklist states are manually authored and do not claim to
measure comprehension automatically.

## Reproduce

```powershell
pwsh -File scripts/build.ps1 -Check
python scripts/inspect-pdfs.py
pwsh -File scripts/build.ps1 -Engine lualatex -Check
python scripts/inspect-pdfs.py --build-dir build/lua
```

The PDF inspection script requires `pymupdf` and `Pillow`; these are only
validation dependencies. Writing or compiling a document does not require
Python. The build script does not turn on shell escape.

This verifies the local examples, not every possible future combination
of third-party packages or page content. Margin blocks are single boxes
and cannot split across pages. Explicitly offset notes do not avoid each
other automatically; dense or unusually tall margin content still needs
visual review. Older TeX distributions and physical printers were not tested.
