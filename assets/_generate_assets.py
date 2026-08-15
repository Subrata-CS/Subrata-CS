#!/usr/bin/env python3
"""Generate every SVG asset for the README, tuned for legibility on GitHub.

Design rules applied everywhere:
  * GitHub renders a 1200px-wide SVG at ~830px, i.e. ~0.69x. So the smallest
    font used here is 18 units (~12.4 real px) and body text is 22-26 units.
  * No blur, haze or gradient ever sits directly behind text. Text always has a
    solid panel under it.
  * Text never moves. Only decorative shapes animate.
  * Titles are pure white or near-white; colour carries meaning, not the text.

Run it from anywhere:   py assets\\_generate_assets.py
Output goes next to this file (assets/) and README.md one level up.
"""
import os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
os.makedirs(OUT, exist_ok=True)

# ── palette ──────────────────────────────────────────────────────────────────
BG0, BG1, BG2 = "#0A0620", "#151038", "#1C1447"
PANEL, PANEL_HI = "#171041", "#221A55"
INK, INK_2, INK_3 = "#FFFFFF", "#EDE7FF", "#C3B8EE"
VIOLET, CYAN, GREEN, AMBER, PINK, PURPLE = (
    "#8B6BFF", "#2ED8F7", "#2FDCA0", "#FFB645", "#FF6EA0", "#B072FF")

SANS = "'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','DejaVu Sans Mono',Consolas,ui-monospace,monospace"

RM = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body.strip() + "\n")
    print(f"{name:24s} {os.path.getsize(path)/1024:6.1f} KB")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def approx_w(text, size, bold=False):
    """Rough advance width for the sans stack."""
    k = 0.68 if bold else 0.60
    return len(text) * size * k


def wrap_to(text, size, max_w, bold=False, max_lines=2):
    if approx_w(text, size, bold) <= max_w:
        return [text]
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if approx_w(trial, size, bold) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines[:max_lines]


GRID = ('<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
        '<path d="M40 0H0V40" fill="none" stroke="#8B6BFF" stroke-opacity="0.09" '
        'stroke-width="1"/></pattern>')


# ═════════════════════════════════════════════════════════════ divider ══
def divider():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 28" width="1200" height="28" role="presentation" aria-hidden="true">
<defs>
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0"/>
<stop offset="18%" stop-color="{VIOLET}"/>
<stop offset="50%" stop-color="{CYAN}"/>
<stop offset="82%" stop-color="{PINK}"/>
<stop offset="100%" stop-color="{PINK}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="cm" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="#9BEFFF" stop-opacity="0"/><stop offset="100%" stop-color="#FFFFFF"/>
</linearGradient>
<style>
.run{{animation:run 6s cubic-bezier(.55,0,.45,1) infinite}}
@keyframes run{{0%{{transform:translateX(-220px);opacity:0}}12%{{opacity:1}}88%{{opacity:1}}100%{{transform:translateX(1260px);opacity:0}}}}
.nd{{animation:tw 3s ease-in-out infinite}}.nd.b{{animation-delay:1s}}.nd.c{{animation-delay:2s}}
@keyframes tw{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
{RM}
</style>
</defs>
<path d="M0 14 H1200" stroke="url(#ln)" stroke-width="3" stroke-linecap="round"/>
<g class="run"><rect x="0" y="12" width="180" height="4" rx="2" fill="url(#cm)"/><circle cx="180" cy="14" r="4.5" fill="#FFFFFF"/></g>
<g fill="{PURPLE}"><circle class="nd" cx="300" cy="14" r="3.4"/><circle class="nd b" cx="600" cy="14" r="4"/><circle class="nd c" cx="900" cy="14" r="3.4"/></g>
</svg>'''


# ══════════════════════════════════════════════════════════════ header ══
def header():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="Subrata Pramanik, Research Scholar in Computer Vision and Pattern Recognition, IIIT Allahabad, formerly TCS">
<title>Subrata Pramanik — Research Scholar, Computer Vision and Pattern Recognition, IIIT Allahabad</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="50%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
<radialGradient id="gl" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{CYAN}" stop-opacity="0.30"/><stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{VIOLET}"/><stop offset="60%" stop-color="{CYAN}"/><stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
{GRID}
<clipPath id="cp"><rect width="1200" height="380" rx="26"/></clipPath>
<style>
.net{{transform-box:fill-box;transform-origin:center;animation:spin 46s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.live{{animation:beat 2s ease-in-out infinite}}
@keyframes beat{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
.hz{{animation:drift 18s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes drift{{0%,100%{{transform:translate(0,0) scale(1)}}50%{{transform:translate(-50px,24px) scale(1.15)}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="380" fill="url(#bg)"/>
<rect width="1200" height="380" fill="url(#grid)"/>
<ellipse class="hz" cx="960" cy="200" rx="300" ry="220" fill="url(#gl)"/>

<!-- decorative network, kept clear of all text -->
<g transform="translate(1010,196)" class="net">
<g fill="none" stroke="{PURPLE}" stroke-opacity="0.45" stroke-width="1.6">
<path d="M-120-84 L-10-44 M-120-84 L-10 40 M-120 0 L-10-44 M-120 0 L-10 104 M-120 84 L-10 40 M-120 84 L-10 104"/>
<path d="M-10-104 L104-56 M-10-44 L104-56 M-10 40 L104 12 M-10 104 L104 76 M-10-44 L104 12 M-10 40 L104-56"/>
</g>
<g fill="{BG0}" stroke="{CYAN}" stroke-width="2.4">
<circle cx="-120" cy="-84" r="9"/><circle cx="-120" cy="0" r="9"/><circle cx="-120" cy="84" r="9"/>
</g>
<g fill="{BG0}" stroke="{PURPLE}" stroke-width="2.4">
<circle cx="-10" cy="-104" r="8"/><circle cx="-10" cy="-44" r="8"/><circle cx="-10" cy="40" r="8"/><circle cx="-10" cy="104" r="8"/>
</g>
<g fill="{BG0}" stroke="{GREEN}" stroke-width="2.4">
<circle cx="104" cy="-56" r="9"/><circle cx="104" cy="12" r="9"/><circle cx="104" cy="76" r="9"/>
</g>
</g>

<!-- identity block on a solid plate so every glyph stays high contrast -->
<rect x="48" y="44" width="778" height="292" rx="20" fill="{PANEL}" fill-opacity="0.92" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="1.5"/>

<g>
<rect x="74" y="70" width="288" height="42" rx="21" fill="{PANEL_HI}" stroke="{PURPLE}" stroke-opacity="0.75" stroke-width="1.5"/>
<circle class="live" cx="98" cy="91" r="6" fill="{GREEN}"/>
<text x="116" y="98" font-family="{MONO}" font-size="19" font-weight="700" letter-spacing="2.6" fill="{INK_2}">RESEARCH SCHOLAR</text>
</g>

<text x="74" y="182" font-family="{SANS}" font-size="55" font-weight="700" letter-spacing="0.5" fill="{INK}">SUBRATA PRAMANIK</text>
<path d="M74 204 H800" stroke="url(#rule)" stroke-width="3" stroke-linecap="round"/>

<text x="74" y="244" font-family="{SANS}" font-size="25" font-weight="600" fill="#8FEBFF">Computer vision · pattern recognition</text>
<text x="74" y="278" font-family="{SANS}" font-size="25" font-weight="600" fill="#8FEBFF">Visual document understanding</text>

<g font-family="{MONO}" font-size="19" font-weight="700" letter-spacing="1.6">
<rect x="74" y="296" width="220" height="40" rx="10" fill="{PANEL_HI}" stroke="{VIOLET}" stroke-width="1.5"/>
<text x="94" y="323" fill="{INK_2}">IIIT ALLAHABAD</text>
<rect x="306" y="296" width="148" height="40" rx="10" fill="{PANEL_HI}" stroke="{CYAN}" stroke-width="1.5"/>
<text x="326" y="323" fill="#9AEEFF">EX-TCSer</text>
<rect x="466" y="296" width="192" height="40" rx="10" fill="{PANEL_HI}" stroke="{GREEN}" stroke-width="1.5"/>
<text x="486" y="323" fill="#9AF0CE">OPEN SOURCE</text>
</g>

<rect x="0.75" y="0.75" width="1198.5" height="378.5" rx="26" fill="none" stroke="{VIOLET}" stroke-opacity="0.55" stroke-width="1.5"/>
</g>
</svg>'''


# ══════════════════════════════════════════════════════ section banners ══
def banner(title, sub, accent, accent2, cta=None):
    """cta: text for a call-to-action pill on the right, or None for dots."""
    if cta:
        pw = int(len(cta) * (19 * 0.66 + 1.9)) + 108
        px = 1160 - pw
        right = (f'<g><rect x="{px}" y="34" width="{pw}" height="48" rx="24" '
                 f'fill="{accent}" fill-opacity="0.20" stroke="{accent}" stroke-width="2"/>'
                 f'<text x="{px + 26}" y="64" font-family="{MONO}" font-size="19" font-weight="700" '
                 f'letter-spacing="1.6" fill="{INK}">{esc(cta)}</text>'
                 f'<g transform="translate({px + pw - 62},58)">'
                 f'<path class="fl" d="M0 0 H30" stroke="{accent2}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
                 f'<path d="M26 -7 L36 0 L26 7" fill="none" stroke="{accent2}" stroke-width="3.5" '
                 f'stroke-linecap="round" stroke-linejoin="round"/></g></g>')
    else:
        right = (f'<g transform="translate(0,58)" fill="{accent2}">'
                 f'<circle class="dt" cx="1120" cy="0" r="5"/><circle class="dt b" cx="1142" cy="0" r="5"/>'
                 f'<circle class="dt c" cx="1164" cy="0" r="5"/></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 116" width="1200" height="116" role="img" aria-label="{esc(title)} — {esc(sub)}">
<title>{esc(title)}</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{BG2}"/><stop offset="60%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
<linearGradient id="ac" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{accent}"/><stop offset="100%" stop-color="{accent2}"/>
</linearGradient>
<clipPath id="cp"><rect width="1200" height="116" rx="18"/></clipPath>
<style>
.gl{{transform-box:fill-box;transform-origin:center;animation:spin 11s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.bar{{animation:pulse 2.8s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.7}}50%{{opacity:1}}}}
.dt{{animation:br 2.2s ease-in-out infinite}}.dt.b{{animation-delay:.35s}}.dt.c{{animation-delay:.7s}}
@keyframes br{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
.fl{{stroke-dasharray:8 8;animation:fl 1.2s linear infinite}}
@keyframes fl{{to{{stroke-dashoffset:-32}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="116" fill="url(#bg)"/>
<rect x="0" y="0" width="10" height="116" fill="url(#ac)" class="bar"/>
<g class="gl" transform="translate(56,58)">
<circle r="18" fill="none" stroke="{accent}" stroke-width="2.4" stroke-dasharray="8 6"/>
<circle r="7" fill="{accent2}"/>
</g>
<text x="98" y="56" font-family="{SANS}" font-size="38" font-weight="700" letter-spacing="3" fill="{INK}">{esc(title)}</text>
<path d="M100 70 H{100 + int(approx_w(title, 38, True) + 60)}" stroke="{accent}" stroke-width="3" stroke-linecap="round" stroke-opacity="0.85"/>
<text x="100" y="96" font-family="{MONO}" font-size="19" font-weight="600" letter-spacing="2" fill="{INK_3}">{esc(sub)}</text>
{right}
<rect x="0.75" y="0.75" width="1198.5" height="114.5" rx="18" fill="none" stroke="{accent}" stroke-opacity="0.5" stroke-width="1.5"/>
</g>
</svg>'''


# ════════════════════════════════════════════════════════ focus diagram ══
def focus():
    sats = [
        ("LAYOUT-AWARE MODELS", "reading order + structure", VIOLET, 60, 60),
        ("OCR-FREE READING", "pixels straight to text", AMBER, 60, 208),
        ("DOCUMENT VQA", "answer from the page", PINK, 60, 356),
        ("RETRIEVAL (RAG)", "fetch the right region", CYAN, 800, 60),
        ("VLM PROBING", "what do they really see", GREEN, 800, 208),
        ("LEGIBILITY LIMITS", "how small is too small", PURPLE, 800, 356),
    ]
    boxes, wires = [], []
    for i, (name, sub, col, x, y) in enumerate(sats):
        left = x < 400
        boxes.append(f'''<g>
<rect x="{x}" y="{y}" width="358" height="112" rx="16" fill="{PANEL}" stroke="{col}" stroke-width="2.5"/>
<rect x="{x}" y="{y}" width="8" height="112" rx="4" fill="{col}"/>
<circle cx="{x + 328}" cy="{y + 88}" r="7" fill="{col}" class="pp" style="animation-delay:{i * .3}s"/>
<text x="{x + 30}" y="{y + 48}" font-family="{SANS}" font-size="22" font-weight="700" fill="{INK}">{esc(name)}</text>
<text x="{x + 30}" y="{y + 82}" font-family="{MONO}" font-size="18" fill="{INK_3}">{esc(sub)}</text>
</g>''')
        sx = (x + 358) if left else x
        ex = 480 if left else 720
        wires.append(f'<path class="wire" d="M{sx} {y + 56} C{(sx + ex) / 2:.0f} {y + 56} {(sx + ex) / 2:.0f} 256 {ex} 256" '
                     f'stroke="{col}" stroke-width="2.5" fill="none" stroke-opacity="0.75" style="animation-delay:{i * .25}s"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 512" width="1200" height="512" role="img" aria-label="Visual document understanding at the centre, connected to layout-aware models, OCR-free reading, document VQA, retrieval augmented generation, vision language model probing and legibility limits">
<title>Current research focus — visual document understanding and the six problems around it</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="50%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
<radialGradient id="core" cx="40%" cy="32%" r="80%">
<stop offset="0%" stop-color="#4B34B8"/><stop offset="100%" stop-color="#150E38"/>
</radialGradient>
{GRID}
<clipPath id="cp"><rect width="1200" height="512" rx="22"/></clipPath>
<style>
.wire{{stroke-dasharray:10 12;animation:flow 1.8s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-44}}}}
.pp{{animation:pp 2.6s ease-in-out infinite}}
@keyframes pp{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="512" fill="url(#bg)"/>
<rect width="1200" height="512" fill="url(#grid)"/>
{''.join(wires)}
<circle cx="600" cy="256" r="118" fill="none" stroke="{CYAN}" stroke-width="2" stroke-opacity="0.35">
<animate attributeName="r" values="104;146" dur="4s" repeatCount="indefinite"/>
<animate attributeName="stroke-opacity" values="0.5;0" dur="4s" repeatCount="indefinite"/>
</circle>
<circle cx="600" cy="256" r="104" fill="url(#core)" stroke="{CYAN}" stroke-width="3"/>
<text x="600" y="246" text-anchor="middle" font-family="{SANS}" font-size="44" font-weight="700" letter-spacing="2" fill="{INK}">VDU</text>
<text x="600" y="278" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="600" letter-spacing="1.4" fill="#9DEBFF">VISUAL DOCUMENT</text>
<text x="600" y="300" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="600" letter-spacing="1.4" fill="#9DEBFF">UNDERSTANDING</text>
{''.join(boxes)}
<text x="30" y="490" font-family="{MONO}" font-size="18" font-weight="600" letter-spacing="2" fill="{INK_3}">THE QUESTIONS I AM CHASING · IIIT ALLAHABAD · PhD TRACK</text>
<rect x="0.75" y="0.75" width="1198.5" height="510.5" rx="22" fill="none" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="1.5"/>
</g>
</svg>'''


# ═══════════════════════════════════════════════════════ workflow (RAG) ══
def workflow():
    stages = [
        ("01", "LAYOUT", "Detect regions", "title · paragraph · table · figure", VIOLET),
        ("02", "ENCODE", "Patch embeddings", "the page becomes vectors", CYAN),
        ("03", "RETRIEVE", "Top-k regions", "rank by similarity to the question", GREEN),
        ("04", "GENERATE", "Grounded answer", "with a citation back to the page", PINK),
    ]
    x0, w, gap = 26, 278, 16
    cards, arrows = [], []
    for i, (num, tag, title, sub, col) in enumerate(stages):
        x = x0 + i * (w + gap)
        cards.append(f'''<g>
<rect x="{x}" y="28" width="{w}" height="268" rx="18" fill="{PANEL}" stroke="{col}" stroke-width="2.5"/>
<rect x="{x}" y="28" width="{w}" height="56" rx="18" fill="{col}" fill-opacity="0.20"/>
<rect x="{x}" y="28" width="{w}" height="56" fill="{col}" fill-opacity="0.10"/>
<text x="{x + 22}" y="65" font-family="{MONO}" font-size="24" font-weight="700" letter-spacing="2" fill="{col}">{num} · {tag}</text>
<text x="{x + 22}" y="128" font-family="{SANS}" font-size="23" font-weight="700" fill="{INK}">{esc(title)}</text>
''' + "".join(
            f'<text x="{x + 22}" y="{160 + j * 28}" font-family="{MONO}" font-size="17" fill="{INK_3}">{esc(l)}</text>'
            for j, l in enumerate(wrap_to(sub, 17, w - 44))
        ) + f'''
<g transform="translate({x + 22},228)">{_glyph(i, col)}</g>
</g>''')
        if i < 3:
            ax = x + w + 1
            arrows.append(f'<path class="wire" d="M{ax} 162 H{ax + gap - 2}" stroke="{INK_3}" stroke-width="3" fill="none" marker-end="url(#ar)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 324" width="1200" height="324" role="img" aria-label="Four stage workflow: detect layout regions, encode into patch embeddings, retrieve the top matching regions, then generate a grounded answer with a citation">
<title>Document understanding workflow — layout, encode, retrieve, grounded answer</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="50%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
<marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{INK_3}"/></marker>
{GRID}
<clipPath id="cp"><rect width="1200" height="324" rx="22"/></clipPath>
<style>
.wire{{stroke-dasharray:8 8;animation:flow 1.4s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-32}}}}
.pp{{animation:pp 2.4s ease-in-out infinite}}
@keyframes pp{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="324" fill="url(#bg)"/>
<rect width="1200" height="324" fill="url(#grid)"/>
{''.join(cards)}
{''.join(arrows)}
<rect x="0.75" y="0.75" width="1198.5" height="322.5" rx="22" fill="none" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="1.5"/>
</g>
</svg>'''


def _glyph(i, col):
    if i == 0:  # page with detected regions
        return (f'<rect width="86" height="52" rx="6" fill="{BG0}" stroke="{col}" stroke-width="2"/>'
                f'<rect x="8" y="8" width="44" height="9" rx="3" fill="{col}"/>'
                f'<rect x="8" y="23" width="70" height="6" rx="3" fill="{INK_3}" opacity="0.55"/>'
                f'<rect x="8" y="34" width="34" height="12" rx="3" fill="none" stroke="{GREEN}" stroke-width="2"/>'
                f'<rect x="50" y="34" width="28" height="12" rx="3" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    if i == 1:  # patch grid
        cells = "".join(
            f'<rect class="pp" x="{c * 22}" y="{r * 22}" width="18" height="18" rx="4" fill="{col}" style="animation-delay:{(r * 4 + c) * .12}s"/>'
            for r in range(2) for c in range(4))
        return cells + f'<rect x="94" y="14" width="10" height="10" rx="5" fill="{INK_2}"/>'
    if i == 2:  # ranked bars
        widths = [(96, GREEN), (44, "#5A5288"), (72, GREEN), (28, "#5A5288")]
        return "".join(
            f'<rect y="{j * 15}" width="110" height="9" rx="4.5" fill="#2A2258"/>'
            f'<rect y="{j * 15}" width="{w}" height="9" rx="4.5" fill="{c}"/>'
            for j, (w, c) in enumerate(widths))
    return (f'<rect width="150" height="10" rx="5" fill="{INK_3}" opacity="0.5"/>'
            f'<rect y="18" width="120" height="10" rx="5" fill="{INK_3}" opacity="0.5"/>'
            f'<rect y="38" width="164" height="26" rx="8" fill="{BG0}" stroke="{GREEN}" stroke-width="2"/>'
            f'<text x="12" y="56" font-family="{MONO}" font-size="15" font-weight="700" fill="{GREEN}">cited · page 1</text>')


# ══════════════════════════════════════════════════════════ six ways ════
def five_ways():
    items = [
        ("Overview", "What it is, in short", VIOLET),
        ("Key concepts", "The ideas that matter", CYAN),
        ("Example", "Worked, with output", GREEN),
        ("Run your code", "Right in the browser", AMBER),
        ("Practice", "Questions to try", PURPLE),
        ("References", "Where to go next", PINK),
    ]
    x0, y0, w, h, gx, gy = 26, 100, 372, 150, 16, 16
    cards = []
    for i, (name, sub, col) in enumerate(items):
        x = x0 + (i % 3) * (w + gx)
        y = y0 + (i // 3) * (h + gy)
        cards.append(f'''<g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{PANEL}" stroke="{col}" stroke-width="2.5"/>
<rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{col}"/>
<circle cx="{x + 44}" cy="{y + 52}" r="22" fill="none" stroke="{col}" stroke-width="2.5"/>
<text x="{x + 44}" y="{y + 61}" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="700" fill="{col}">{i + 1}</text>
<text x="{x + 82}" y="{y + 52}" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">{esc(name)}</text>
<text x="{x + 82}" y="{y + 84}" font-family="{MONO}" font-size="17" fill="{INK_3}">{esc(sub)}</text>
<rect x="{x + 82}" y="{y + 104}" width="{w - 110}" height="6" rx="3" fill="{col}" fill-opacity="0.30"/>
<rect class="gw" x="{x + 82}" y="{y + 104}" width="{int((w - 110) * (0.5 + 0.08 * i))}" height="6" rx="3" fill="{col}" style="animation-delay:{i * .15}s"/>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 510" width="1200" height="510" role="img" aria-label="Every topic page opens the same six ways: overview, key concepts, example, run your code, practice questions and references — and a Code Lab you can open in the browser">
<title>Every topic page opens the same six ways</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="50%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
{GRID}
<clipPath id="cp"><rect width="1200" height="510" rx="22"/></clipPath>
<style>
.gw{{transform-box:fill-box;transform-origin:left;animation:gw 2.6s ease-in-out infinite}}
@keyframes gw{{0%,100%{{transform:scaleX(.55)}}50%{{transform:scaleX(1)}}}}
.fl{{stroke-dasharray:8 8;animation:fl 1.2s linear infinite}}
@keyframes fl{{to{{stroke-dashoffset:-32}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="510" fill="url(#bg)"/>
<rect width="1200" height="510" fill="url(#grid)"/>
<text x="26" y="52" font-family="{SANS}" font-size="30" font-weight="700" fill="{INK}">Every topic page opens the same six ways</text>
<text x="26" y="80" font-family="{MONO}" font-size="18" fill="{INK_3}">SAME SHAPE, EVERY SUBJECT — SO YOU NEVER HUNT FOR ANYTHING</text>
{''.join(cards)}
<g>
<rect x="420" y="440" width="360" height="52" rx="26" fill="{AMBER}" fill-opacity="0.20" stroke="{AMBER}" stroke-width="2.5"/>
<text x="454" y="473" font-family="{MONO}" font-size="21" font-weight="700" letter-spacing="2" fill="{INK}">CODE LAB</text>
<g transform="translate(688,466)">
<path class="fl" d="M0 0 H30" stroke="{AMBER}" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M26 -8 L37 0 L26 8" fill="none" stroke="{AMBER}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</g>
<rect x="0.75" y="0.75" width="1198.5" height="508.5" rx="22" fill="none" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="1.5"/>
</g>
</svg>'''


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  EDIT ZONE — change these lists, run the script, everything follows.  ║
# ╚══════════════════════════════════════════════════════════════════════╝

# Publications. Add a line and re-run; colours are picked automatically.
#   ("conference" | "journal" | "preprint" | "workshop", year, title, link)
PUBLICATIONS = [
    ("conference", 2026, "Demo Paper I — I will update",   "https://example.com/paper-2026-conference"),
    ("journal",    2026, "Demo Paper II — I will update",  "https://example.com/paper-2026-journal"),
    ("conference", 2027, "Demo Paper III — I will update", "https://example.com/paper-2027-conference"),
    ("journal",    2028, "Demo Paper IV — I will update",  "https://example.com/paper-2028-journal"),
    ("conference", 2029, "Demo Paper V — I will update",   "https://example.com/paper-2029-conference"),
]

# Learning Hub sections. Add or remove freely — the numbering, the grid
# height and the "N sections" heading all recalculate themselves.
# Write either  "Section name"  or  ("Section name", topic_count).
# If every entry carries a count the topic total is summed automatically;
# otherwise TOPIC_COUNT below is used.
TOPIC_COUNT = 578

# ═══════════════════════════════════════════════════════ topics grid ════
SECTIONS = [
    "Computer Fundamentals", "Programming Fundamentals", "Discrete Mathematics",
    "Linear Algebra", "Probability & Statistics", "Calculus",
    "Data Structures & Algorithms", "Computer Organization", "Operating Systems",
    "Computer Networks", "Database Systems", "Software Engineering",
    "Git & GitHub", "Web Development", "Mobile Development", "Cloud Computing",
    "Cybersecurity", "Compiler Design", "Theory of Computation",
    "Distributed Systems", "Parallel Computing", "Computer Graphics",
    "Human-Computer Interaction", "Embedded Systems", "Real-Time Systems",
    "Data Science", "Data Mining", "Information Retrieval",
    "Artificial Intelligence", "Machine Learning", "Deep Learning",
    "Specialized AI Fields", "MLOps", "DevOps", "Blockchain",
    "Internet of Things", "Robotics", "Quantum Computing",
    "Research Methodology", "Advanced Research Areas",
]
SECTION_NAMES = [x[0] if isinstance(x, (tuple, list)) else x for x in SECTIONS]
SECTION_TOPICS = [x[1] for x in SECTIONS if isinstance(x, (tuple, list))]
N_SECTIONS = len(SECTION_NAMES)
N_TOPICS = sum(SECTION_TOPICS) if len(SECTION_TOPICS) == N_SECTIONS else TOPIC_COUNT

TRACKS = [(1, 6, "FOUNDATIONS", VIOLET), (7, 12, "CORE CS", CYAN),
          (13, 25, "ENGINEERING", PURPLE), (26, 34, "AI & DATA", GREEN),
          (35, 38, "FRONTIER", AMBER), (39, 10 ** 6, "RESEARCH", PINK)]


def track_colour(n):
    for lo, hi, _, col in TRACKS:
        if lo <= n <= hi:
            return col
    return VIOLET


def topics_grid():
    cols, x0, y0, w, h, gx, gy = 4, 24, 176, 282, 92, 16, 14
    cards = []
    for i, name in enumerate(SECTION_NAMES):
        n = i + 1
        col = track_colour(n)
        x = x0 + (i % cols) * (w + gx)
        y = y0 + (i // cols) * (h + gy)
        avail = w - 90
        for size in (21, 20, 19, 18, 17):
            lines = wrap_to(name, size, avail, bold=True, max_lines=3)
            if len(lines) <= 2 and all(approx_w(l, size, True) <= avail for l in lines):
                break
        ty = 54 if len(lines) == 1 else 44
        txt = "".join(
            f'<text x="{x + 74}" y="{y + ty + j * 27}" font-family="{SANS}" font-size="{size}" font-weight="600" fill="{INK_2}">{esc(l)}</text>'
            for j, l in enumerate(lines))
        cards.append(f'''<g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PANEL}" stroke="{col}" stroke-width="2"/>
<rect x="{x}" y="{y}" width="7" height="{h}" rx="3.5" fill="{col}"/>
<text x="{x + 26}" y="{y + 56}" font-family="{MONO}" font-size="24" font-weight="700" fill="{col}">{n:02d}</text>
{txt}
</g>''')
    legend = []
    lx = 24
    for lo, hi, label, col in TRACKS:
        legend.append(f'<circle cx="{lx + 9}" cy="132" r="8" fill="{col}"/>'
                      f'<text x="{lx + 26}" y="140" font-family="{MONO}" font-size="18" font-weight="700" letter-spacing="1.4" fill="{INK_2}">{esc(label)}</text>')
        lx += 26 + int(len(label) * (18 * 0.66 + 1.4)) + 40
    rows = -(-N_SECTIONS // cols)          # ceiling division
    height = y0 + rows * (h + gy) + 66
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" width="1200" height="{height}" role="img" aria-label="{N_SECTIONS} computer science sections in the Learning Hub, grouped into six tracks: foundations, core CS, engineering, AI and data, frontier and research">
<title>The Learning Hub — {N_SECTIONS} sections, {N_TOPICS} topics</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="52%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
{GRID}
<clipPath id="cp"><rect width="1200" height="{height}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="{height}" fill="url(#bg)"/>
<rect width="1200" height="{height}" fill="url(#grid)"/>
<text x="24" y="60" font-family="{SANS}" font-size="36" font-weight="700" fill="{INK}">{N_SECTIONS} sections &#183; {N_TOPICS} topics</text>
<text x="24" y="92" font-family="{MONO}" font-size="19" fill="{INK_3}">EVERY SUBJECT ON THE SHELF, GROUPED INTO SIX TRACKS</text>
<path d="M24 106 H620" stroke="{VIOLET}" stroke-width="3" stroke-linecap="round"/>
{''.join(legend)}
{''.join(cards)}
<text x="24" y="{height - 24}" font-family="{MONO}" font-size="18" font-weight="600" fill="{INK_3}">SUBRATA-CS.GITHUB.IO/OPEN · FREE AND OPEN SOURCE</text>
<text x="1176" y="{height - 24}" text-anchor="end" font-family="{MONO}" font-size="18" font-weight="600" fill="{INK_3}">MIT License &#183; &#169; 2026 Subrata Pramanik</text>
<rect x="0.75" y="0.75" width="1198.5" height="{height - 1.5}" rx="22" fill="none" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="1.5"/>
</g>
</svg>'''


# ══════════════════════════════════════════════════════════════ footer ══
def footer():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 180" width="1200" height="180" role="img" aria-label="Subrata Pramanik — Research Scholar, Computer Vision and Pattern Recognition, IIIT Allahabad">
<title>Subrata Pramanik — Research Scholar, Computer Vision and Pattern Recognition, IIIT Allahabad</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="55%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</linearGradient>
<linearGradient id="w1" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.6"/><stop offset="100%" stop-color="{CYAN}" stop-opacity="0.6"/>
</linearGradient>
<linearGradient id="w2" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{PINK}" stop-opacity="0.4"/><stop offset="100%" stop-color="{PURPLE}" stop-opacity="0.4"/>
</linearGradient>
<clipPath id="cp"><rect width="1200" height="180" rx="22"/></clipPath>
<style>
.wv{{animation:slide 16s linear infinite}}.wv.b{{animation-duration:23s;animation-direction:reverse}}
@keyframes slide{{from{{transform:translateX(0)}}to{{transform:translateX(-600px)}}}}
.bc{{animation:beat 2.4s ease-in-out infinite}}
@keyframes beat{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="180" fill="url(#bg)"/>
<g transform="translate(0,96)">
<g class="wv b"><path d="M0 56 q150 -30 300 0 t300 0 t300 0 t300 0 t300 0 t300 0 V110 H0 Z" fill="url(#w2)"/></g>
<g class="wv"><path d="M0 68 q150 -26 300 0 t300 0 t300 0 t300 0 t300 0 t300 0 V110 H0 Z" fill="url(#w1)"/></g>
</g>
<text x="600" y="66" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="700" letter-spacing="3" fill="{INK}">SUBRATA PRAMANIK</text>
<text x="600" y="98" text-anchor="middle" font-family="{MONO}" font-size="18" font-weight="600" letter-spacing="1.8" fill="{INK_3}">RESEARCH SCHOLAR · COMPUTER VISION &amp; PATTERN RECOGNITION · IIIT ALLAHABAD</text>
<g class="bc">
<circle cx="566" cy="124" r="6" fill="{GREEN}"/><circle cx="600" cy="124" r="6" fill="{CYAN}"/><circle cx="634" cy="124" r="6" fill="{VIOLET}"/>
</g>
<rect x="0.75" y="0.75" width="1198.5" height="178.5" rx="22" fill="none" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="1.5"/>
</g>
</svg>'''



# ═══════════════════════════════════════════════════ animated hero line ══
def typing():
    """Colourful animated banner that cycles through three lines.

    Only line 1 carries opacity="1" as a presentation attribute, so if a
    renderer ignores CSS the banner degrades to a single readable line
    instead of three overlapping ones.
    """
    lines = [
        ("Computer Vision · Pattern Recognition", CYAN),
        ("Research Scholar at IIIT Allahabad", "#B9A8FF"),
        ("Ex-TCSer · Building the Learning Hub", GREEN),
    ]
    out = []
    for i, (txt, col) in enumerate(lines):
        half = approx_w(txt, 40, True) / 2
        out.append(
            f'<g class="ln l{i + 1}" opacity="{1 if i == 0 else 0}">'
            f'<text x="600" y="118" text-anchor="middle" font-family="{SANS}" font-size="40" '
            f'font-weight="700" fill="{col}">{esc(txt)}</text>'
            f'<rect class="car" x="{600 + half + 12:.0f}" y="90" width="6" height="38" rx="3" fill="{AMBER}"/>'
            f'</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200" width="1200" height="200" role="img" aria-label="Computer vision and pattern recognition · Research scholar at IIIT Allahabad · Ex-TCSer, building the Learning Hub">
<title>Computer Vision · Pattern Recognition — Research Scholar at IIIT Allahabad — Ex-TCSer</title>
<defs>
<linearGradient id="rain" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{VIOLET}"><animate attributeName="stop-color" values="{VIOLET};{PINK};{CYAN};{VIOLET}" dur="14s" repeatCount="indefinite"/></stop>
<stop offset="50%" stop-color="{PURPLE}"><animate attributeName="stop-color" values="{PURPLE};{AMBER};{GREEN};{PURPLE}" dur="14s" repeatCount="indefinite"/></stop>
<stop offset="100%" stop-color="{CYAN}"><animate attributeName="stop-color" values="{CYAN};{VIOLET};{PINK};{CYAN}" dur="14s" repeatCount="indefinite"/></stop>
</linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{VIOLET}"/><stop offset="25%" stop-color="{CYAN}"/><stop offset="50%" stop-color="{GREEN}"/>
<stop offset="75%" stop-color="{AMBER}"/><stop offset="100%" stop-color="{PINK}"/>
</linearGradient>
{GRID}
<clipPath id="cp"><rect width="1200" height="200" rx="22"/></clipPath>
<style>
.ln{{animation:cyc 13.5s ease-in-out infinite}}
.l2{{animation-delay:-9s}}.l3{{animation-delay:-4.5s}}
@keyframes cyc{{0%{{opacity:0}}3%{{opacity:1}}30%{{opacity:1}}34%{{opacity:0}}100%{{opacity:0}}}}
.car{{animation:blink 1.05s steps(1) infinite}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.sheen{{animation:sheen 9s linear infinite}}
@keyframes sheen{{from{{transform:translateX(-420px)}}to{{transform:translateX(1300px)}}}}
{RM}
</style>
</defs>
<g clip-path="url(#cp)">
<rect width="1200" height="200" fill="url(#rain)"/>
<rect width="1200" height="200" fill="{BG0}" fill-opacity="0.55"/>
<rect width="1200" height="200" fill="url(#grid)"/>
<g class="sheen"><rect x="0" y="0" width="220" height="200" fill="#FFFFFF" fill-opacity="0.05"/></g>
<rect x="34" y="52" width="1132" height="96" rx="18" fill="{BG0}" fill-opacity="0.82" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.5"/>
{"".join(out)}
<rect x="34" y="164" width="1132" height="6" rx="3" fill="url(#bar)" fill-opacity="0.9"/>
<rect x="0.75" y="0.75" width="1198.5" height="198.5" rx="22" fill="none" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1.5"/>
</g>
</svg>'''



# ══════════════════════════════════ publications table, written into README ══
PUB_COLOUR = {"conference": "6D5AF7", "journal": "22C9E8",
              "preprint": "F7A93B", "workshop": "22C58B", "thesis": "F65C8E"}
YEAR_COLOUR = ["F65C8E", "9B5CF6", "22C58B", "F7A93B", "22C9E8"]
BADGE = "https://img.shields.io/badge/{}-{}?style=for-the-badge&labelColor=160F3C"

# Colours of the three table headings. Change the hex to restyle the header.
HEAD_COLOUR = [("TYPE", "6D5AF7"), ("YEAR", "22C9E8"), ("PAPER", "F7A93B")]


def publications_table():
    head = "| " + " | ".join(
        f'<img src="{BADGE.format(label, colour)}" alt="{label.title()}" />'
        for label, colour in HEAD_COLOUR) + " |"
    rows = [head, "|:---:|:---:|:---|"]
    for i, (kind, year, title, link) in enumerate(PUBLICATIONS):
        kc = PUB_COLOUR.get(kind.lower(), "6D5AF7")
        yc = YEAR_COLOUR[i % len(YEAR_COLOUR)]
        rows.append(
            f'| <img src="{BADGE.format(kind.upper(), kc)}" alt="{kind}" /> '
            f'| <img src="{BADGE.format(year, yc)}" alt="{year}" /> '
            f'| [{title}]({link}) |')
    return "\n".join(rows)


def update_readme():
    """Rewrite the publications table in README.md between its markers."""
    path = os.path.join(os.path.dirname(OUT) or ".", "README.md")
    a, b = "<!-- PUBLICATIONS:START -->", "<!-- PUBLICATIONS:END -->"
    if not os.path.exists(path):
        print("README.md not found next to assets/ — table not updated")
        return
    doc = open(path, encoding="utf-8").read()
    if a not in doc or b not in doc:
        print("README.md has no PUBLICATIONS markers — table not updated")
        return
    new = doc[:doc.index(a) + len(a)] + "\n\n" + publications_table() + "\n\n" + doc[doc.index(b):]
    open(path, "w", encoding="utf-8").write(new)
    print(f"{'README.md':24s} {len(PUBLICATIONS)} publications written")


# ═══════════════════════════════════════════════════════════════ build ══
write("divider.svg", divider())
write("header.svg", header())
write("typing.svg", typing())
write("footer.svg", footer())
write("sec-about.svg", banner("ABOUT", "WHO IS BEHIND THIS PROFILE", VIOLET, PURPLE))
write("sec-focus.svg", banner("CURRENT FOCUS", "WHAT I AM READING, BUILDING AND MEASURING", GREEN, "#3FE0AE"))
write("sec-hub.svg", banner("LEARNING HUB", "ONE SHELF FOR EVERYTHING I AM LEARNING", CYAN, "#5FE4FF",
                            cta="OPEN THE LEARNING HUB"))
write("sec-publications.svg", banner("PUBLICATIONS", "PEER-REVIEWED WORK AND PREPRINTS", AMBER, "#FF9256"))
write("sec-reach.svg", banner("REACH ME", "MAIL, PROFILES AND REPOSITORIES", PINK, PURPLE))
write("focus-orbit.svg", focus())
write("vdu-rag.svg", workflow())
write("five-ways.svg", five_ways())
write("topics-grid.svg", topics_grid())
update_readme()
