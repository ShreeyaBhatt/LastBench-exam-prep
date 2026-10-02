"""ReportLab exports: unit revision booklets and Notes Studio study packs."""

import io
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak, Image, KeepTogether, PageBreak, Paragraph, Preformatted,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

INK = colors.HexColor("#16201c")
MUTED = colors.HexColor("#5b6b64")
LINE = colors.HexColor("#d5ddd8")
PAPER = colors.HexColor("#f2f5f3")
ACCENT = colors.HexColor("#1f63c6")
GOOD = colors.HexColor("#1f7a45")

# ---- fonts: use real TTFs when available so non-ASCII text renders ----------
SANS, SANS_B, SANS_I, MONO = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"
_FONT_DIRS = [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu"), Path("/Library/Fonts")]
_CANDIDATES = [
    ("SH-Sans", ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]),
    ("SH-Sans-B", ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]),
    ("SH-Sans-I", ["segoeuii.ttf", "ariali.ttf", "DejaVuSans-Oblique.ttf"]),
    ("SH-Mono", ["consola.ttf", "cour.ttf", "DejaVuSansMono.ttf"]),
]


def _register():
    global SANS, SANS_B, SANS_I, MONO
    found = {}
    for name, files in _CANDIDATES:
        for d in _FONT_DIRS:
            hit = next((d / f for f in files if (d / f).exists()), None)
            if hit:
                pdfmetrics.registerFont(TTFont(name, str(hit)))
                found[name] = True
                break
    if {"SH-Sans", "SH-Sans-B", "SH-Sans-I"} <= found.keys():
        pdfmetrics.registerFontFamily("SH-Sans", normal="SH-Sans", bold="SH-Sans-B", italic="SH-Sans-I", boldItalic="SH-Sans-B")
        SANS, SANS_B, SANS_I = "SH-Sans", "SH-Sans-B", "SH-Sans-I"
    if "SH-Mono" in found:
        MONO = "SH-Mono"


_register()

S = {
    "title": ParagraphStyle("title", fontName=SANS_B, fontSize=22, leading=27, textColor=INK, spaceAfter=4),
    "kicker": ParagraphStyle("kicker", fontName=SANS_B, fontSize=8.5, leading=11, textColor=MUTED),
    "h1": ParagraphStyle("h1", fontName=SANS_B, fontSize=15, leading=19, textColor=INK, spaceBefore=10, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName=SANS_B, fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("body", fontName=SANS, fontSize=9.6, leading=13.6, textColor=INK, alignment=TA_LEFT, spaceAfter=4),
    "small": ParagraphStyle("small", fontName=SANS, fontSize=8.4, leading=11.4, textColor=MUTED),
    "cell": ParagraphStyle("cell", fontName=SANS, fontSize=8.6, leading=11.4, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName=SANS_B, fontSize=8.6, leading=11.4, textColor=INK),
    "bullet": ParagraphStyle("bullet", fontName=SANS, fontSize=9.6, leading=13.4, textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=1.5),
    "code": ParagraphStyle("code", fontName=MONO, fontSize=7.8, leading=9.6, textColor=INK, backColor=PAPER,
                           borderPadding=5, leftIndent=4, rightIndent=4, spaceBefore=4, spaceAfter=7),
    "q": ParagraphStyle("q", fontName=SANS_B, fontSize=10, leading=14, textColor=INK, spaceAfter=3),
    "opt": ParagraphStyle("opt", fontName=SANS, fontSize=9.4, leading=12.6, textColor=INK, leftIndent=10),
    "ans": ParagraphStyle("ans", fontName=SANS_B, fontSize=9.6, leading=13, textColor=GOOD, spaceBefore=2, spaceAfter=2),
}


# ---- markdown -> flowables -------------------------------------------------

def inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", rf'<font name="{MONO}">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"(?<![\w])_(?!\s)([^_]+?)(?<!\s)_(?![\w])", r"<i>\1</i>", text)
    return text


def _table(rows, width):
    rows = [r for r in rows if not re.fullmatch(r"\|?\s*:?-{2,}.*", r.strip())]
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    ncol = max(len(r) for r in cells)
    cells = [r + [""] * (ncol - len(r)) for r in cells]
    data = [[Paragraph(inline(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(cells)]
    t = Table(data, colWidths=[width / ncol] * ncol, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PAPER),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [t, Spacer(1, 6)]


def md(text, width):
    out, lines, i = [], (text or "").splitlines(), 0
    para = []

    def flush():
        if para:
            out.append(Paragraph(inline(" ".join(para)), S["body"]))
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            out.append(Preformatted("\n".join(block), S["code"]))
        elif s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.extend(_table(rows, width))
            continue
        elif re.match(r"^#{1,4}\s", s):
            flush()
            out.append(Paragraph(inline(s.lstrip("#").strip()), S["h2"]))
        elif re.match(r"^[-*]\s+", s):
            flush()
            out.append(Paragraph(inline(re.sub(r"^[-*]\s+", "", s)), S["bullet"], bulletText="\u2022"))
        elif re.match(r"^\d+[.)]\s+", s):
            flush()
            num, rest = re.match(r"^(\d+)[.)]\s+(.*)$", s).groups()
            out.append(Paragraph(inline(rest), S["bullet"], bulletText=f"{num}."))
        elif not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return out


# ---- page decoration ----------------------------------------------------------

def _decorator(label, colour):
    def draw(canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(colour)
        canvas.rect(0, h - 6 * mm, w, 6 * mm, stroke=0, fill=1)
        canvas.setFont(SANS, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 10 * mm, label)
        canvas.drawRightString(w - 18 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def _doc(buf, title):
    return SimpleDocTemplate(
        buf, pagesize=A4, title=title, author="LastBench",
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
    )


def _kv_table(rows, width, head):
    data = [[Paragraph(head[0], S["cellb"]), Paragraph(head[1], S["cellb"])]]
    data += [[Paragraph(inline(a), S["cellb"]), Paragraph(inline(b), S["cell"])] for a, b in rows]
    t = Table(data, colWidths=[width * 0.34, width * 0.66], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PAPER), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# ---- unit booklet ---------------------------------------------------------------

def unit_pdf(course, unit, questions, diagram_dir):
    buf = io.BytesIO()
    doc = _doc(buf, f"{course['code']} Unit {unit['id']} - {unit['title']}")
    width = doc.width
    colour = LINE if unit["fibre"] == "White" else colors.HexColor(unit["colour"])
    notes = unit["notes"]
    st = []
    st.append(Paragraph(f"{course['name'].upper()}  \u00b7  UNIT {unit['id']}  \u00b7  FIBRE {unit['fibre'].upper()}", S["kicker"]))
    st.append(Paragraph(inline(unit["title"]), S["title"]))
    st.append(Paragraph(inline(notes["summary"]), S["body"]))
    st.append(Paragraph(f"Practice book Q{unit['range'][0]}-Q{unit['range'][1]}  \u00b7  "
                        f"{unit['counts']['mcq']} MCQ, {unit['counts']['numerical']} numerical, {unit['counts']['theory']} theory  \u00b7  "
                        f"Source: {inline(unit['source'])}", S["small"]))
    st.append(Spacer(1, 8))
    st.append(Paragraph("One-minute notes", S["h1"]))
    for sec in notes["sections"]:
        block = [Paragraph(inline(sec["h"]), S["h2"])]
        block += [Paragraph(inline(p), S["bullet"], bulletText="\u2022") for p in sec["points"]]
        st.append(KeepTogether(block))
    if notes["formulas"]:
        st.append(CondPageBreak(40 * mm))
        st.append(Paragraph("Formulas and rules", S["h1"]))
        st.append(_kv_table(notes["formulas"], width, ("Name", "Formula")))
    st.append(Paragraph("Exam traps", S["h1"]))
    st += [Paragraph(inline(t), S["bullet"], bulletText="!") for t in notes["traps"]]

    st.append(PageBreak())
    st.append(Paragraph("Practice book solutions", S["h1"]))
    for q in questions:
        kind = {"mcq": "MCQ", "numerical": "Numerical", "theory": "Theory"}[q["kind"]]
        head = [Paragraph(f'<font color="#5b6b64">Q{q["id"]} \u00b7 {kind} \u00b7 {q["marks"]} mark{"s" if q["marks"] > 1 else ""}</font>', S["small"]),
                Paragraph(inline(q["text"]), S["q"])]
        img = diagram_dir / f"q{q['id']}.png"
        if q.get("diagram") and img.exists():
            im = Image(str(img))
            scale = min(1, (width * 0.6) / im.imageWidth, (55 * mm) / im.imageHeight)
            im.drawWidth, im.drawHeight = im.imageWidth * scale, im.imageHeight * scale
            im.hAlign = "LEFT"
            head.append(im)
        for i, o in enumerate(q["options"]):
            letter = "ABCD"[i]
            mark = "  <b>(correct)</b>" if letter == q["answer"] else ""
            head.append(Paragraph(f"{letter}. {inline(o)}{mark}", S["opt"]))
        ans = f"Answer: {q['answer']}. {q['answer_text']}" if q["answer"] else f"Answer: {q['answer_text']}"
        head.append(Paragraph(inline(ans), S["ans"]))
        st.append(KeepTogether(head))
        st += md(q["explanation"], width)
        st.append(Spacer(1, 4))
        st.append(Table([[""]], colWidths=[width], style=[("LINEABOVE", (0, 0), (-1, -1), 0.5, LINE)]))
    doc.build(st, onFirstPage=_decorator(f"{course['code']} \u00b7 Unit {unit['id']} \u00b7 {unit['title']}", colour),
              onLaterPages=_decorator(f"{course['code']} \u00b7 Unit {unit['id']} \u00b7 {unit['title']}", colour))
    return buf.getvalue()


# ---- formula sheet ----------------------------------------------------------------

def formulas_pdf(course):
    buf = io.BytesIO()
    doc = _doc(buf, f"{course['code']} Formula sheet")
    width = doc.width
    st = [
        Paragraph(f"{course['name'].upper()}  ·  REVISE IN 5 MINUTES", S["kicker"]),
        Paragraph("Formula sheet", S["title"]),
        Paragraph("Every formula, rule and common trap from the ten units.", S["body"]),
    ]
    for unit in course["units"]:
        notes = unit["notes"]
        block = [Paragraph(f"Unit {unit['id']}: {inline(unit['title'])}  "
                           f"<font size='8.5' color='#5b6b64'>{unit['test']}</font>", S["h1"])]
        if notes["formulas"]:
            block.append(_kv_table(notes["formulas"], width, ("Name", "Formula")))
            block.append(Spacer(1, 4))
        # Keep each unit's heading with the start of its table so it never sits alone at a page foot.
        st.append(CondPageBreak(35 * mm))
        st += block
        if notes["traps"]:
            st.append(Paragraph("Exam traps", S["h2"]))
            st += [Paragraph(inline(t), S["bullet"], bulletText="!") for t in notes["traps"]]
    label = f"{course['code']} · Formula sheet"
    doc.build(st, onFirstPage=_decorator(label, ACCENT), onLaterPages=_decorator(label, ACCENT))
    return buf.getvalue()


# ---- Notes Studio pack ------------------------------------------------------------

def deck_pdf(subject, deck):
    data = deck["data"] or {}
    buf = io.BytesIO()
    doc = _doc(buf, data.get("title") or deck["title"])
    width = doc.width
    st = []
    engine = "Generated by Claude" if deck.get("engine") == "claude" else "Offline draft (no AI)"
    st.append(Paragraph(f"{subject['name'].upper()}  \u00b7  NOTES STUDIO  \u00b7  {engine.upper()}", S["kicker"]))
    st.append(Paragraph(inline(data.get("title") or deck["title"]), S["title"]))
    st.append(Paragraph(inline(data.get("summary", "")), S["body"]))
    st.append(Paragraph(f"Source file: {inline(deck['source_name'])}", S["small"]))

    st.append(Paragraph("Detailed notes", S["h1"]))
    for sec in data.get("sections", []):
        st.append(CondPageBreak(30 * mm))
        st.append(Paragraph(inline(sec["heading"]), S["h2"]))
        st += md(sec["content_md"], width)
        if sec.get("key_points"):
            kp = [[Paragraph("<b>Key points</b>", S["cell"])]] + [[Paragraph("\u2022 " + inline(p), S["cell"])] for p in sec["key_points"]]
            t = Table(kp, colWidths=[width], hAlign="LEFT")
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PAPER), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            st += [t, Spacer(1, 6)]

    if data.get("key_terms"):
        st.append(CondPageBreak(40 * mm))
        st.append(Paragraph("Key terms", S["h1"]))
        st.append(_kv_table([(t["term"], t["definition"]) for t in data["key_terms"]], width, ("Term", "Definition")))
    if data.get("formulas"):
        st.append(CondPageBreak(40 * mm))
        st.append(Paragraph("Formulas and rules", S["h1"]))
        st.append(_kv_table([(f["name"], f"{f['expression']}<br/>{f.get('note', '')}") for f in data["formulas"]], width, ("Name", "Formula")))
    if data.get("exam_questions"):
        st.append(PageBreak())
        st.append(Paragraph("Likely exam questions", S["h1"]))
        for i, q in enumerate(data["exam_questions"], 1):
            st.append(KeepTogether([Paragraph(f"{i}. {inline(q['question'])}  <font color='#5b6b64'>[{q.get('marks', '')} marks]</font>", S["q"])]))
            st += md(q["answer_md"], width)
    cards = data.get("flashcards", [])
    if cards:
        st.append(PageBreak())
        st.append(Paragraph("Flashcards", S["h1"]))
        st.append(Paragraph("Cut along the dashed lines, then fold each strip down the middle: question on the front, answer on the back.", S["small"]))
        st.append(Spacer(1, 6))
        rows = []
        for c in cards:
            rows.append([
                [Paragraph(f'<font color="#5b6b64" size="7">{inline(c.get("topic", ""))}</font>', S["cell"]),
                 Paragraph(inline(c["front"]), S["cellb"])],
                [Paragraph(inline(c["back"]), S["cell"])],
            ])
        t = Table(rows, colWidths=[width / 2, width / 2], hAlign="LEFT")
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.6, MUTED, None, (3, 3)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        st.append(t)
    label = f"{subject['code']} \u00b7 {data.get('title') or deck['title']}"
    doc.build(st, onFirstPage=_decorator(label, ACCENT), onLaterPages=_decorator(label, ACCENT))
    return buf.getvalue()
