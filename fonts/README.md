# Local font roles

These are the user's existing font files. They retain their own licenses;
the template's LPPL does not relicense them.

- `times.ttf`: Times New Roman Regular.
- `timesbd.ttf`: Times New Roman Bold.
- `timesi.ttf`: Times New Roman Italic.
- `timesbi.ttf`: Times New Roman Bold Italic.
- `0xProtoNerdFontMono-Bold.ttf`: 0xProto Nerd Font Mono Bold. This folder
  contains only the bold face, so code uses that real face directly.
- `simsunb.ttf`: SimSun-ExtB Regular, not SimSun Bold.
- `SimsunExtG.ttf`: SimSun-ExtG Regular.

Actual font character maps were inspected. Neither extension font contains
common Han characters in U+4E00--U+9FFF. They supplement a normal Song face.
If a licensed `simsun.ttc` is placed here, it takes priority over system
SimSun; otherwise ordinary Chinese uses system SimSun when available, then
Fandol Song. No system font file is copied into this folder by the template.

Use `fonts=tex` to disable local font preferences. Use `fontpath=.../` to
point the class at another folder. The supplied local starter ZIP includes
this folder for the user's local workflow.
