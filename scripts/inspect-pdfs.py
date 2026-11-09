"""Render contact sheets and check actual PDF geometry of the two demos.

Requires PyMuPDF and Pillow. Run from any directory after building the demos.
This checks output positions, not just the class option values.
"""
from pathlib import Path
import argparse
import json
import re
import pymupdf as fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--build-dir", default="build")
args = parser.parse_args()
BUILD = ROOT / args.build_dir
OUT = ROOT / "tmp" / "pdfs" / ("lua" if BUILD.name == "lua" else "xe")
OUT.mkdir(parents=True, exist_ok=True)
report = {}
for mode in ("screen", "print"):
    path = BUILD / f"demo-{mode}.pdf"
    doc = fitz.open(path)
    assert len(doc) == 8, (mode, len(doc))
    # Body page 2: both the table and code must live in the outer margin.
    page = doc[3]
    margin = page.search_for("A compact glossary")
    body = page.search_for("From derivatives")
    assert margin and body, (mode, "Missing expected text")
    if mode == "screen":
        assert margin[0].x0 > body[0].x1, (mode, margin, body)
    else:
        assert margin[0].x1 < body[0].x0, (mode, margin, body)
    # Body page 1 remains a right-hand margin in BOTH modes.
    odd = doc[2]
    reading = odd.search_for("Reading lens")
    odd_body = odd.search_for("A model problem")
    assert reading and odd_body
    assert reading[0].x0 > odd_body[0].x1
    # Body page 6 checks that widepage restored the mirrored geometry.
    restored = doc[7].search_for("Restored layout")
    restored_body = doc[7].search_for("Back to the margin")
    assert restored and restored_body
    if mode == "screen":
        assert restored[0].x0 > restored_body[0].x1
    else:
        assert restored[0].x1 < restored_body[0].x0
    # All rendered text must stay on the paper. Allow 0.5pt round-off.
    for p in doc:
        for block in p.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    x0, y0, x1, y1 = span["bbox"]
                    assert -0.5 <= x0 <= x1 <= p.rect.width + 0.5, (mode, p.number, span)
                    assert -0.5 <= y0 <= y1 <= p.rect.height + 0.5, (mode, p.number, span)
    thumbs = []
    for i, p in enumerate(doc):
        pix = p.get_pixmap(matrix=fitz.Matrix(0.8, 0.8), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.save(OUT / f"{mode}-{i+1}.png")
        thumbs.append(im)
    width, height = thumbs[0].size
    sheet = Image.new("RGB", (width * 4, (height + 28) * 2), "#dce1e5")
    draw = ImageDraw.Draw(sheet)
    for i, thumb in enumerate(thumbs):
        x, y = (i % 4) * width, (i // 4) * (height + 28)
        sheet.paste(thumb, (x, y + 28))
        draw.text((x + 10, y + 6), f"{mode} / PDF page {i+1}", fill="black")
    sheet.save(OUT / f"{mode}-contact.png")
    report[mode] = {
        "pages": len(doc),
        "even_margin_x_pt": round(margin[0].x0, 2),
        "even_body_x_pt": round(body[0].x0, 2),
        "odd_margin_x_pt": round(reading[0].x0, 2),
        "widepage_restoration": "passed",
        "text_inside_paper": "passed",
    }
    doc.close()

if BUILD.name != "lua":
    # An even-page comparison makes the main layout switch visible at a glance.
    output = ROOT / "output" / "pdf"
    output.mkdir(parents=True, exist_ok=True)
    pages = [Image.open(OUT / f"{mode}-4.png").convert("RGB") for mode in ("screen", "print")]
    w, h = pages[0].size
    preview = Image.new("RGB", (2 * w + 36, h + 52), "#e6ebe9")
    draw = ImageDraw.Draw(preview)
    for i, (mode, page) in enumerate(zip(("SCREEN / right margin", "PRINT / left outer margin"), pages)):
        x = 12 + i * (w + 12)
        preview.paste(page, (x, 40))
        draw.text((x + 10, 14), mode, fill="#216b60")
    preview.save(output / "layout-comparison.png")
    # A cover and a code-rich page show the typography and listing interface.
    design = Image.new("RGB", (2 * w + 36, h + 52), "#e6ebe9")
    draw = ImageDraw.Draw(design)
    for i, (label, name) in enumerate((("LUMENBOOK / local-font edition", "screen-1.png"),
                                     ("NUMBERED CODE / language labels", "screen-6.png"))):
        x = 12 + i * (w + 12)
        design.paste(Image.open(OUT / name).convert("RGB"), (x, 40))
        draw.text((x + 10, 14), label, fill="#17675c")
    design.save(output / "design-preview.png")

for name, outer, expected_size in (("features", True, 9.96), ("features-screen", False, 11.96)):
    doc = fitz.open(BUILD / f"{name}.pdf")
    assert len(doc) == 2
    odd_body = doc[0].search_for("ODD-BODY.")[0]
    even_body = doc[1].search_for("EVEN-BODY.")[0]
    for token in ("ODD-FLOAT.", "PINNED-ODD.", "INSIDE-BOX."):
        rects = doc[0].search_for(token)
        assert len(rects) == 1, (name, token, rects)
        assert rects[0].x0 > odd_body.x1, (name, token, rects)
    for token in ("EVEN-FLOAT.", "PINNED-EVEN.", "PINNED-FIGURE."):
        rects = doc[1].search_for(token)
        assert len(rects) == 1, (name, token, rects)
        if outer:
            assert rects[0].x1 < even_body.x0, (name, token, rects)
        else:
            assert rects[0].x0 > even_body.x1, (name, token, rects)
    sizes = [s["size"] for b in doc[0].get_text("dict")["blocks"]
             for line in b.get("lines", []) for s in line["spans"]
             if "ODD-BODY." in s["text"]]
    assert sizes and abs(sizes[0] - expected_size) < 0.1, (name, sizes)
    text = "".join(p.get_text() for p in doc)
    assert "def energy" in text and "中文" in text
    report[name] = {"pinned_and_floating_sides": "passed", "body_font_pt": round(sizes[0], 2)}
    for i, p in enumerate(doc):
        p.get_pixmap(matrix=fitz.Matrix(1.2, 1.2)).save(OUT / f"{name}-{i+1}.png")
    doc.close()

doc = fitz.open(BUILD / "long-content.pdf")
def page_of(token):
    pages = [p.number for p in doc if p.search_for(token)]
    assert len(pages) == 1, (token, pages)
    return pages[0]
assert page_of("LONG-THEOREM-START.") < page_of("LONG-THEOREM-END.")
assert page_of("LONG-READING-START.") < page_of("LONG-READING-END.")
assert page_of("value_001") < page_of("value_100") <= page_of("END-OF-TEST.")
for i, p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(0.8, 0.8)).save(OUT / f"long-content-{i+1}.png")
report["long-content"] = {"pages": len(doc), "theorem_reading_code_page_breaks": "passed"}
doc.close()

doc = fitz.open(BUILD / "fonts-code.pdf")
text = "".join(p.get_text() for p in doc)
fonts = {entry[3].split("+")[-1] for p in doc for entry in p.get_fonts()}
required_fonts = {"TimesNewRomanPSMT", "TimesNewRomanPS-BoldMT",
                  "TimesNewRomanPS-ItalicMT", "TimesNewRomanPS-BoldItalicMT",
                  "0xProtoNFM-Bold", "SimSun-ExtB", "SimSun-ExtG"}
assert required_fonts <= fonts, ("Required local fonts missing", required_fonts - fonts)
for token in ("# FIRST-LINE:", "# SIDE-FIRST-LINE", "# DEFAULT-FIRST-LINE",
              "Python / Discrete energy", "Pseudo / Explicit override", "𠀀", "𰀀"):
    assert token in text, ("Missing source text or label", token)
first_line = doc[0].search_for("# FIRST-LINE:")[0]
line12 = [r for r in doc[0].search_for("12")
          if r.x1 < first_line.x0 and abs(r.y1 - first_line.y1) < 6]
assert line12, "Custom firstnumber=12 is missing or not beside the first source line"
assert len(doc[0].search_for("Python")) >= 3, "File language inference failed"
report["fonts-code"] = {"local_faces_embedded": sorted(required_fonts),
    "extension_characters": "passed", "first_source_lines_preserved": "passed",
    "language_labels_and_line_numbers": "passed"}
doc[0].get_pixmap(matrix=fitz.Matrix(1.2, 1.2)).save(OUT / "fonts-code.png")
doc.close()
doc = fitz.open(BUILD / "portable-fonts.pdf")
fonts = {entry[3] for p in doc for entry in p.get_fonts()}
assert not any("TimesNewRoman" in name or "0xProto" in name for name in fonts)
assert any("TeXGyreTermes" in name for name in fonts)
report["portable-fonts"] = {"tex_only_font_fallback": "passed"}
doc.close()

annotation_palettes = ((1, 240/255, 181/255), (220/255, 239/255, 225/255),
                       (223/255, 236/255, 248/255), (247/255, 223/255, 228/255),
                       (235/255, 227/255, 245/255))
for name, mono in (("annotations", False), ("annotations-print", True)):
    doc = fitz.open(BUILD / f"{name}.pdf")
    assert len(doc) == 2, (name, len(doc))
    content = "".join(p.get_text() for p in doc)
    for token in ("HIGHLIGHT-START.", "HIGHLIGHT-END.",
                  "UNDERLINE-START.", "UNDERLINE-END.", "weak solution"):
        assert token in content, (name, token)
    assert doc[0].search_for("HIGHLIGHT-START.")[0].y0 < doc[0].search_for("HIGHLIGHT-END.")[0].y0
    assert doc[1].search_for("UNDERLINE-START.")[0].y0 < doc[1].search_for("UNDERLINE-END.")[0].y0
    assert any(row[1].endswith("Marked headings") for row in doc.get_toc()), doc.get_toc()
    # XeTeX may encode a highlighter rule as a thick stroke rather than a fill.
    fills = [d[key] for p in doc for d in p.get_drawings()
             for key in ("fill", "color") if d.get(key)]
    if mono:
        assert all(max(c)-min(c) < 0.015 for c in fills if len(c) == 3), (name, fills)
    else:
        for expected in annotation_palettes:
            assert any(len(c) == 3 and max(abs(a-b) for a,b in zip(c,expected)) < .025
                       for c in fills), (name, expected)
    report[name] = {"pages": len(doc), "text_wrapping": "passed",
                    "pdf_heading_plain_text": "passed", "palette": "passed"}
    for i, p in enumerate(doc):
        p.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(OUT / f"{name}-{i+1}.png")
    if name == "annotations" and BUILD.name != "lua":
        doc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),
                         clip=fitz.Rect(48,180,568,640)).save(ROOT / "output/pdf/annotations-preview.png")
    doc.close()
doc = fitz.open(BUILD / "annotations-long.pdf")
starts = [p.number for p in doc if p.search_for("MARKBLOCK-START.")]
ends = [p.number for p in doc if p.search_for("MARKBLOCK-END.")]
assert len(starts) == len(ends) == 1 and starts[0] < ends[0]
assert any(p.search_for("AFTER-MARKBLOCK.") for p in doc)
report["annotations-long"] = {"pages": len(doc), "background_page_break": "passed"}
for i, p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(.8,.8)).save(OUT / f"annotations-long-{i+1}.png")
doc.close()
for name, show_solution, show_hint in (("study-tools", True, True),
                                      ("study-hidden", False, False),
                                      ("study-nohints", True, False)):
    doc = fitz.open(BUILD / f"{name}.pdf")
    assert len(doc) == 3, (name, len(doc))
    text = " ".join(" ".join(p.get_text() for p in doc).split())
    assert ("The time factor decays exponentially" in text) == show_solution, name
    assert ("decay_rate" in text) == show_solution, name
    assert ("Start with the separated form" in text) == show_hint, name
    aux = (BUILD / f"{name}.aux").read_text(encoding="utf-8")
    assert ("newlabel{eq:study-answer}" in aux) == show_solution, name
    assert re.search(r"newlabel\{ex:study-mode\}\{\{1\.4\}", aux), name
    if name == "study-hidden":
        for word in ("学习目标", "本章小结", "复习清单", "阅读进度"):
            assert word in text, (name, word)
    else:
        for phrase in ("Definition 1.1", "theorem 1.2", "lemma 1.3"):
            assert phrase in text, (name, phrase)
    bars = {}
    for p in doc:
        for d in p.get_drawings():
            r = d["rect"]
            if d.get("fill") and abs(r.height-3) < .1:
                bars.setdefault((p.number, round(r.y0,1)), []).append(r.width)
    assert len(bars) == 2, (name, bars)
    for widths in bars.values():
        assert len(widths) == 2 and abs(min(widths)/max(widths)-3/8) < .002, (name, widths)
    report[name] = {"pages": len(doc), "solution_visibility": "passed",
        "hint_visibility": "passed", "exercise_number_stable": "passed",
        "hidden_labels_not_executed": "passed", "drawn_progress_ratio": "3/8"}
    for i,p in enumerate(doc):
        p.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(OUT / f"{name}-{i+1}.png")
    if name == "study-tools" and BUILD.name != "lua":
        # Show the exercise/solution and review pages side by side.
        pics = [Image.open(OUT / f"{name}-{i}.png").convert("RGB") for i in (2,3)]
        w,h = pics[0].size
        preview = Image.new("RGB", (2*w+36,h+40), "#e6ebe9")
        draw = ImageDraw.Draw(preview)
        for i,(label,pic) in enumerate(zip(("PRACTICE / hints and solutions", "REVIEW / checklist and progress"),pics)):
            x=12+i*(w+12)
            preview.paste(pic,(x,28))
            draw.text((x+8,8),label,fill="#17675c")
        preview.save(ROOT / "output/pdf/study-preview.png")
    doc.close()
doc = fitz.open(BUILD / "study-refs.pdf")
assert len(doc) == 2
text = " ".join(" ".join(p.get_text() for p in doc).split())
for name in ("theorem", "definition", "lemma", "proposition", "corollary",
             "assumption", "example", "exercise", "remark"):
    assert re.search(r"\b"+name+r"\s+1\.", text, re.I), name
assert "Definitions 2.1 and 2.2" in text, text
assert "definitions 1.2 and 2.1" in text, text
assert {link["page"] for link in doc[1].get_links() if link.get("page",-1) >= 0} >= {0,1}
report["study-refs"] = {"distinct_theorem_types": "passed",
    "chapter_reset_and_sorting": "passed", "capitalized_plural": "passed",
    "cross_chapter_links": "passed"}
doc.close()
(OUT / "geometry-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
