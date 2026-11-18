import io
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    HRFlowable, Image, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "Desarrollo_matematico.md"
DST = ROOT / "docs" / "Desarrollo_matematico.pdf"

FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DV", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DV-I", str(FONT_DIR / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DV-BI", str(FONT_DIR / "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("DVM", str(FONT_DIR / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch
FRAME_W = PAGE_W - 2 * MARGIN

INK = colors.HexColor("#0F172A")
ACCENT = colors.HexColor("#0369A1")
SOFT = colors.HexColor("#F1F5F9")
BORDER = colors.HexColor("#CBD5E1")

S = {
    "title": ParagraphStyle("title", fontName="DV-B", fontSize=17, leading=21, textColor=INK, spaceAfter=4),
    "meta": ParagraphStyle("meta", fontName="DV", fontSize=9, leading=12.5, textColor=colors.HexColor("#334155")),
    "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=13, leading=17, textColor=ACCENT, spaceBefore=12, spaceAfter=5),
    "h3": ParagraphStyle("h3", fontName="DV-B", fontSize=10.5, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="DV", fontSize=9, leading=13, textColor=INK, spaceAfter=4),
    "quote": ParagraphStyle("quote", fontName="DV", fontSize=9, leading=13, textColor=colors.HexColor("#334155"),
                            leftIndent=14, borderPadding=(3, 3, 3, 8), backColor=SOFT, spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8, leading=11, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="DV-B", fontSize=8, leading=11, textColor=INK),
    "code": ParagraphStyle("code", fontName="DVM", fontSize=7.2, leading=9, textColor=INK, backColor=SOFT,
                           borderPadding=5, spaceAfter=6),
    "mathfail": ParagraphStyle("mathfail", fontName="DVM", fontSize=7.5, leading=10, textColor=colors.HexColor("#475569"),
                               alignment=TA_CENTER, spaceAfter=4),
}

# ---------------------------------------------------------------- LaTeX -> marcado de reportlab (en línea)
SYMBOLS = {
    "zeta": "ζ", "omega": "ω", "alpha": "α", "beta": "β", "pi": "π", "lambda": "λ", "Delta": "Δ",
    "pm": "±", "approx": "≈", "times": "×", "cdot": "·", "le": "≤", "ge": "≥", "neq": "≠", "sim": "∼",
    "lesssim": "≲", "implies": "⟹", "Rightarrow": "⇒", "Longrightarrow": "⟹", "iff": "⟺", "to": "→",
    "dots": "…", "sum": "∑", "infty": "∞", "quad": " ", "qquad": "  ", "ln": "ln", "cos": "cos", "sin": "sin",
}
DROP = {"left", "right", "big", "bigl", "bigr", "!", ",", ";", "displaystyle"}


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _group(s, i):
    """Devuelve (contenido, índice siguiente) del grupo {..} que empieza en s[i]; o de un solo carácter."""
    if i >= len(s):
        return "", i
    if s[i] != "{":
        return s[i], i + 1
    depth, j = 0, i
    while j < len(s):
        depth += s[j] == "{"
        depth -= s[j] == "}"
        j += 1
        if depth == 0:
            break
    return s[i + 1:j - 1], j


def tex_inline(s):
    """LaTeX sencillo -> marcado de Paragraph (Unicode, <sub>, <super>, <b>)."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            cmd = m.group(1)
            i += m.end()
            if cmd in ("frac", "dfrac", "tfrac"):
                a, i = _group(s, i)
                b, i = _group(s, i)
                out.append(f"({tex_inline(a)})/({tex_inline(b)})")
            elif cmd == "sqrt":
                a, i = _group(s, i)
                out.append(f"√({tex_inline(a)})")
            elif cmd in ("text", "mathrm"):
                a, i = _group(s, i)
                out.append(_esc(a))
            elif cmd == "mathbf":
                a, i = _group(s, i)
                out.append(f"<b>{tex_inline(a)}</b>")
            elif cmd == "boxed":
                a, i = _group(s, i)
                out.append(tex_inline(a))
            elif cmd in DROP:
                pass
            elif cmd in SYMBOLS:
                out.append(SYMBOLS[cmd])
            elif cmd == " ":
                out.append(" ")
            else:
                out.append(_esc(cmd))
        elif c in "^_":
            a, i = _group(s, i + 1)
            tag = "super" if c == "^" else "sub"
            out.append(f"<{tag}>{tex_inline(a)}</{tag}>")
        elif c in "{}":
            i += 1
        else:
            out.append(_esc(c))
            i += 1
    return "".join(out)


def md_inline(text):
    """Markdown en línea + matemática $...$ -> marcado de Paragraph."""
    maths = []

    def stash(m):
        maths.append(tex_inline(m.group(1)))
        return f"\x00{len(maths) - 1}\x00"

    text = re.sub(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", stash, text)
    text = _esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r'<font face="DVM" size="8">\1</font>', text)
    return re.sub(r"\x00(\d+)\x00", lambda m: maths[int(m.group(1))], text)


# ---------------------------------------------------------------- ecuaciones en bloque (mathtext)
def _strip_boxed(tex):
    m = re.search(r"\\boxed\{", tex)
    if not m:
        return tex, False
    inner, end = _group(tex, m.end() - 1)
    return tex[:m.start()] + inner + tex[end:], True


def to_mathtext(tex):
    tex = tex.strip()
    tex = re.sub(r"\\(?:text|mathrm)\{([^{}]*)\}", lambda m: r"\mathrm{" + m.group(1).replace(" ", r"\ ") + "}", tex)
    for a, b in (("\\implies", "\\Rightarrow"), ("\\Longrightarrow", "\\Rightarrow"), ("\\iff", "\\Leftrightarrow"),
                 ("\\dots", "\\ldots"), ("\\!", ""), ("\\bigl", ""), ("\\bigr", ""), ("\\big", ""),
                 ("\\tfrac", "\\frac"), ("\\dfrac", "\\frac"), ("\\le ", "\\leq "), ("\\ge ", "\\geq "),
                 ("\\le\\", "\\leq\\"), ("\\ge\\", "\\geq\\"), ):
        tex = tex.replace(a, b)
    tex = re.sub(r"(?<!\\)%", r"\\%", tex)                           # % sin escapar -> \%
    tex = re.sub(r"\\frac(\d)(\d)", r"\\frac{\1}{\2}", tex)          # \frac32 -> \frac{3}{2}
    return tex


def render_math(tex, size=11):
    """LaTeX -> (BytesIO PNG, ancho_pt, alto_pt). Lanza excepción si mathtext no lo entiende."""
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, f"${to_mathtext(tex)}$", fontsize=size, color="#0F172A")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=220, bbox_inches="tight", pad_inches=0.04, transparent=True)
    plt.close(fig)
    buf.seek(0)
    from PIL import Image as PILImage
    w_px, h_px = PILImage.open(buf).size
    buf.seek(0)
    return buf, w_px / 220 * 72, h_px / 220 * 72


def math_flowables(tex):
    tex, boxed = _strip_boxed(tex)
    tex = tex.strip()
    lines = [tex]
    m = re.fullmatch(r"\\begin\{cases\}(.*)\\end\{cases\}", tex, re.S)
    if m:
        lines = [p.strip() for p in m.group(1).split("\\\\") if p.strip()]
    items = []
    for line in lines:
        try:
            buf, w, h = render_math(line)
            scale = min(1.0, (FRAME_W - 20) / w)
            items.append(Image(buf, width=w * scale, height=h * scale))
        except Exception as exc:  # mathtext no soporta el comando: se muestra el LaTeX tal cual
            print(f"  aviso: ecuación sin dibujar ({exc.__class__.__name__}): {line[:60]}", file=sys.stderr)
            items.append(Preformatted(line, S["mathfail"]))
    if boxed:
        box = Table([[it] for it in items], colWidths=[None])
        box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, ACCENT), ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                                 ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        return [box, Spacer(1, 5)]
    out = []
    for it in items:
        it.hAlign = "CENTER"
        out += [it, Spacer(1, 3)]
    return out


# ---------------------------------------------------------------- Markdown -> flowables
def table_flowable(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    header, body = cells[0], cells[2:]
    data = [[Paragraph(md_inline(c), S["cellh"]) for c in header]]
    data += [[Paragraph(md_inline(c), S["cell"]) for c in r] for r in body]
    weights = [max(6, max(len(r[i]) if i < len(r) else 0 for r in [header] + body)) for i in range(len(header))]
    weights = [min(w, 45) for w in weights]
    total = sum(weights)
    t = Table(data, colWidths=[FRAME_W * w / total for w in weights], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER), ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [t, Spacer(1, 6)]


def build_story(lines):
    story, para, i = [], [], 0
    first_h1_done = False

    def flush():
        nonlocal para
        if para:
            text = ""
            for k, (raw, hard) in enumerate(para):
                text += md_inline(raw) + ("<br/>" if hard and k < len(para) - 1 else " ")
            story.append(Paragraph(text.strip(), S["meta"] if first_h1_done and len(story) < 4 else S["body"]))
            para = []

    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):                      # bloque de código
            flush()
            block, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip("\n"))
                i += 1
            story.append(Preformatted("\n".join(block), S["code"]))
            i += 1
            continue

        if stripped.startswith("$$"):                       # ecuación en bloque (una o varias líneas)
            flush()
            tex = stripped
            while not (len(tex) > 2 and tex.endswith("$$")):
                i += 1
                tex += " " + lines[i].strip()
            story += math_flowables(tex[2:-2])
            i += 1
            continue

        if stripped.startswith("|"):                        # tabla
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            story += table_flowable(rows)
            continue

        if not stripped:
            flush()
        elif stripped == "---":
            flush()
            story += [Spacer(1, 3), HRFlowable(width="100%", thickness=0.6, color=BORDER), Spacer(1, 3)]
        elif line.startswith("# "):
            flush()
            story.append(Paragraph(md_inline(line[2:]), S["title"]))
            first_h1_done = True
        elif line.startswith("## "):
            flush()
            story.append(Paragraph(md_inline(line[3:]), S["h2"]))
        elif line.startswith("### "):
            flush()
            story.append(Paragraph(md_inline(line[4:]), S["h3"]))
        elif stripped.startswith(">"):
            flush()
            story.append(Paragraph(md_inline(stripped.lstrip("> ").strip()), S["quote"]))
        elif re.match(r"\s*(?:[-*]|\d+\.)\s+", line):
            flush()
            indent = len(line) - len(line.lstrip())
            marker = re.match(r"\s*([-*]|\d+\.)\s+", line)
            bullet = "•" if marker.group(1) in "-*" else marker.group(1)
            st = ParagraphStyle("li", parent=S["body"], leftIndent=16 + indent * 5, bulletIndent=4 + indent * 5)
            story.append(Paragraph(md_inline(line[marker.end():]), st, bulletText=bullet))
        elif line.startswith("  ") and story:               # continuación indentada de un ítem
            flush()
            indent = len(line) - len(line.lstrip())
            st = ParagraphStyle("lic", parent=S["body"], leftIndent=16 + (indent - 3) * 5)
            story.append(Paragraph(md_inline(stripped), st))
        else:
            para.append((stripped, line.endswith("  ")))
        i += 1
    flush()
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(MARGIN, 0.45 * inch, "Proyecto 4 · Resortes para animar — Desarrollo matemático")
    canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch, f"Página {doc.page}")
    canvas.restoreState()


def main():
    story = build_story(SRC.read_text(encoding="utf-8").splitlines(keepends=True))
    doc = SimpleDocTemplate(str(DST), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                            title="Proyecto 4: Resortes para animar — Desarrollo matemático",
                            author="Grupo 4")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF generado: {DST.relative_to(ROOT)} ({doc.page} páginas)")


if __name__ == "__main__":
    main()
