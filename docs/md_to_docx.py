#!/usr/bin/env python3
"""Convert DEV_GUIDE.md to a formatted .docx (headings, tables, code blocks, lists, bold)."""
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = "/home/user/F1-Race/docs/DEV_GUIDE.md"
DST = "/home/user/F1-Race/docs/F1-Race-Developer-Guide.docx"

doc = Document()

# Base style
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)


def add_runs(par, text):
    """Parse **bold** and `code` inline markup into runs."""
    # Split on **bold** first
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = par.add_run(part[2:-2])
            run.bold = True
        else:
            # handle inline code
            code_parts = re.split(r"(`[^`]+`)", part)
            for cp in code_parts:
                if not cp:
                    continue
                if cp.startswith("`") and cp.endswith("`"):
                    run = par.add_run(cp[1:-1])
                    run.font.name = "Consolas"
                    run.font.size = Pt(10)
                else:
                    par.add_run(cp)


def add_heading(text, level):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    return h


def add_code_block(lines):
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Inches(0.3)
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x1F, 0x1F, 0x1F)
        # light gray shading
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "F2F2F2")
        pPr.append(shd)


def add_table(rows):
    header = rows[0]
    body = rows[1:]
    table = doc.add_table(rows=len(rows), cols=len(header))
    table.style = "Light Grid Accent 1"
    for j, cell_text in enumerate(header):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        add_runs(p, cell_text)
        for r in p.runs:
            r.bold = True
    for i, row in enumerate(body, start=1):
        for j, cell_text in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            add_runs(p, cell_text)
    doc.add_paragraph()


def set_cell_text(cell, text):
    cell.text = ""
    add_runs(cell.paragraphs[0], text)


with open(SRC, encoding="utf-8") as f:
    lines = f.read().splitlines()

i = 0
in_code = False
code_buf = []
table_buf = []

def flush_table():
    global table_buf
    if table_buf:
        rows = [r for r in table_buf if not re.match(r"^\s*\|?[\s:-]+\|[\s:|-]*$", r)]
        if rows:
            parsed = []
            for r in rows:
                r = r.strip()
                if r.startswith("|"):
                    r = r[1:]
                if r.endswith("|"):
                    r = r[:-1]
                parsed.append([c.strip() for c in r.split("|")])
            if parsed:
                add_table(parsed)
        table_buf = []

while i < len(lines):
    line = lines[i]

    if line.strip().startswith("```"):
        if in_code:
            add_code_block(code_buf)
            code_buf = []
            in_code = False
        else:
            flush_table()
            in_code = True
        i += 1
        continue
    if in_code:
        code_buf.append(line)
        i += 1
        continue

    # Table row
    if line.strip().startswith("|"):
        table_buf.append(line)
        i += 1
        continue
    else:
        flush_table()

    # Headings
    m = re.match(r"^(#{1,4})\s+(.*)$", line)
    if m:
        level = len(m.group(1))
        add_heading(m.group(2).strip(), level)
        i += 1
        continue

    # Horizontal rule
    if re.match(r"^\s*---+\s*$", line):
        i += 1
        continue

    # Bullet list
    m = re.match(r"^(\s*)-\s+(.*)$", line)
    if m:
        p = doc.add_paragraph(style="List Bullet")
        add_runs(p, m.group(2).strip())
        i += 1
        continue

    # Numbered list
    m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
    if m:
        p = doc.add_paragraph(style="List Number")
        add_runs(p, m.group(3).strip())
        i += 1
        continue

    # Checkbox list
    m = re.match(r"^\s*-\s+\[( |x|X)\]\s+(.*)$", line)
    if m:
        p = doc.add_paragraph(style="List Bullet")
        mark = "☑" if m.group(1).lower() == "x" else "☐"
        add_runs(p, f"{mark} {m.group(2).strip()}")
        i += 1
        continue

    # Blank line
    if not line.strip():
        i += 1
        continue

    # Regular paragraph
    p = doc.add_paragraph()
    add_runs(p, line.strip())
    i += 1

flush_table()

# Document properties
doc.core_properties.title = "F1-Race — Developer Guide & Game Reference Document"
doc.core_properties.author = "F1-Race Team"
doc.save(DST)
print("Saved:", DST)
