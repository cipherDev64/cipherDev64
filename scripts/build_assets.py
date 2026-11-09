# Draws every static SVG in assets/ (banner, now strip, studio card, project cards, toolbox, dock).
# Stdlib only. Run: python3 scripts/build_assets.py
# The contribution graph is drawn separately by build_activity.py (a GitHub Action refreshes it).
import os
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

BG, PANEL, PANEL2, LINE = "#0f0e0d", "#161412", "#1d1a17", "#2b2723"
TEXT, MUTED, DIM = "#f3eee7", "#a1978d", "#6a625b"
OR, OR2 = "#ef6a3a", "#f6a172"
GREEN, AMBER, VIOLET = "#4ade80", "#fbbf24", "#a78bfa"

REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, label, body, style="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}"><defs>{defs}</defs><style>{style}{REDUCE}</style>{body}</svg>')


def t(x, y, s, size=14, fill=TEXT, weight=400, family=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def tw(s, size=14, k=0.56):
    """rough text width for the sans stack"""
    return len(s) * size * k


def write(name, data):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w") as f:
        f.write(data)
    print(f"{name:28s} {len(data)/1024:5.1f} KB")


def frame(w, h, r=18):
    """the dark rounded panel every asset sits on"""
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="{PANEL}"/>'
            f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="{r-.5}" fill="none" stroke="{LINE}"/>')


def dots_pattern(pid="dots", step=22, op=.07):
    return (f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1" fill="{TEXT}" fill-opacity="{op}"/></pattern>')


# ───────────────────────────── banner ─────────────────────────────
def banner():
    W, H = 960, 380
    style = f"""
.w{{opacity:0;animation:word 9s infinite}}
@keyframes word{{0%{{opacity:0;transform:translateY(14px)}}4%,30%{{opacity:1;transform:translateY(0)}}34%,100%{{opacity:0;transform:translateY(-14px)}}}}
.glow{{animation:glow 6s ease-in-out infinite alternate}}
@keyframes glow{{from{{opacity:.55;transform:translate(0,0)}}to{{opacity:.9;transform:translate(-30px,12px)}}}}
.p{{stroke-dasharray:10 400;stroke-dashoffset:410;animation:flow 3.2s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:0}}}}
.n{{transform-box:fill-box;transform-origin:center;animation:node 3.2s ease-in-out infinite}}
@keyframes node{{0%,100%{{fill:{PANEL2}}}50%{{fill:{OR}}}}}
.bar{{transform-box:fill-box;transform-origin:left center;animation:bar 6.4s cubic-bezier(.2,.8,.2,1) infinite}}
@keyframes bar{{0%{{transform:scaleX(0)}}12%,82%{{transform:scaleX(1)}}92%,100%{{transform:scaleX(0)}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(3);opacity:0}}}}
@media (prefers-reduced-motion: reduce){{.w{{opacity:0}}.w0{{opacity:1}}.bar{{transform:none}}}}
"""
    defs = (dots_pattern() +
            f'<radialGradient id="g1"><stop offset="0" stop-color="{OR}" stop-opacity=".28"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>')

    b = [frame(W, H)]
    b.append(f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#dots)"/>'
             f'<g class="glow"><circle cx="780" cy="90" r="260" fill="url(#g1)"/></g></g>')

    # name pill
    pill = "Atulya Manikandan  ·  Bengaluru, IN"
    pw = tw(pill, 13) + 46
    b.append(f'<rect x="48" y="52" width="{pw:.0f}" height="32" rx="16" fill="{PANEL2}" stroke="{LINE}"/>'
             f'<circle class="pulse" cx="66" cy="68" r="4" fill="{OR}"/><circle cx="66" cy="68" r="4" fill="{OR}"/>'
             + t(80, 72.5, pill, 13, MUTED, 500))

    # headline
    b.append(t(46, 158, "AI/ML engineer,", 50, TEXT, 400, SERIF, extra='letter-spacing="-1"'))
    # textLength pins the width so the rotating word lands in the same spot on every OS font
    b.append(t(46, 216, "from model to", 50, TEXT, 400, SERIF, extra='textLength="300" lengthAdjust="spacing"'))
    for i, word in enumerate(["product.", "pixel.", "launch."]):
        b.append(f'<g class="w w{i}" style="animation-delay:{i*3}s">'
                 + t(362, 216, word, 50, OR, 400, SERIF, extra='font-style="italic" letter-spacing="-1"') + '</g>')

    b.append(t(48, 262, "AI/ML  ·  Product design  ·  Front-end  ·  Co-founder, Second Algorithm", 15, MUTED, 500))

    # terminal-ish line
    b.append(t(48, 318, "~ $ ship --from model --to product", 13, DIM, 400, MONO)
             + f'<rect class="blink" x="{48 + tw("~ $ ship --from model --to product", 13, .6) + 4:.0f}" y="307" width="8" height="14" fill="{OR}"/>')

    # right: a tiny neural net feeding a UI window
    layers = [[(600, y) for y in (130, 190, 250)],
              [(668, y) for y in (100, 160, 220, 280)],
              [(736, y) for y in (150, 230)]]
    edges, pulses = [], []
    k = 0
    for a, c in zip(layers, layers[1:]):
        for (x1, y1) in a:
            for (x2, y2) in c:
                edges.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" stroke-width="1.2"/>')
                if (k * 7) % 3 == 0:
                    pulses.append(f'<line class="p" style="animation-delay:{-(k*0.37)%3.2:.2f}s" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{OR}" stroke-width="2" stroke-linecap="round"/>')
                k += 1
    # last layer into the window
    for (x1, y1) in layers[-1]:
        edges.append(f'<line x1="{x1}" y1="{y1}" x2="780" y2="190" stroke="{LINE}" stroke-width="1.2"/>')
        pulses.append(f'<line class="p" style="animation-delay:{-y1/100:.2f}s" x1="{x1}" y1="{y1}" x2="780" y2="190" stroke="{OR}" stroke-width="2" stroke-linecap="round"/>')
    b += edges + pulses
    j = 0
    for layer in layers:
        for (x, y) in layer:
            b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>'
                     f'<circle class="n" style="animation-delay:{-(j*0.41)%3.2:.2f}s" cx="{x}" cy="{y}" r="5"/>')
            j += 1

    # UI window being assembled
    wx, wy, ww, wh = 780, 112, 140, 156
    b.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="10" fill="{PANEL2}" stroke="{LINE}"/>'
             f'<rect x="{wx}" y="{wy+22}" width="{ww}" height="1" fill="{LINE}"/>'
             + "".join(f'<circle cx="{wx+12+i*10}" cy="{wy+11}" r="3" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))))
    rows = [(14, 18, 70, OR), (14, 46, 112, MUTED), (14, 58, 92, MUTED), (14, 82, 50, DIM), (70, 82, 56, DIM), (14, 108, 52, OR)]
    for i, (dx, dy, w_, c) in enumerate(rows):
        h_ = 10 if i == 0 else 6 if c == MUTED else 18
        y_ = wy + 22 + dy
        op = ".9" if c == OR else ".55"
        b.append(f'<rect class="bar" style="animation-delay:{i*0.18:.2f}s" x="{wx+dx}" y="{y_}" width="{w_}" height="{h_}" rx="{min(h_/2,4)}" fill="{c}" fill-opacity="{op}"/>')
    b.append(t(wx + ww / 2, wy + wh + 22, "model → product", 11.5, DIM, 500, MONO, "middle"))

    return svg(W, H, "Atulya Manikandan. AI/ML engineer, from model to product. Co-founder, Second Algorithm.", "".join(b), style, defs)


# ───────────────────────────── now strip ─────────────────────────────
def now():
    W, H = 960, 64
    items = [("co-founding Second Algorithm", OR, True),
             ("researching agent memory", VIOLET, False),
             ("AI intern @ FlyRank", AMBER, False),
             ("open to collabs", GREEN, False)]
    style = """
.fl{animation:fl 4.4s ease-in-out infinite alternate}
@keyframes fl{from{transform:translateY(0)}to{transform:translateY(-3px)}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.6}100%{transform:scale(3.2);opacity:0}}
"""
    widths = [tw(s, 14, .55) + 52 for s, _, _ in items]
    gap = 12
    x = (W - sum(widths) - gap * (len(items) - 1)) / 2
    b = []
    for i, ((s, c, live), w) in enumerate(zip(items, widths)):
        b.append(f'<g transform="translate({x:.1f} 10)"><g class="fl" style="animation-delay:-{i*1.1:.1f}s">'
                 f'<rect width="{w:.0f}" height="40" rx="20" fill="{PANEL}" stroke="{LINE}"/>'
                 + (f'<circle class="pulse" cx="22" cy="20" r="4.5" fill="{c}"/>' if live else "")
                 + f'<circle cx="22" cy="20" r="4.5" fill="{c}"/>'
                 + t(36, 25, s, 14, TEXT, 500) + '</g></g>')
        x += w + gap
    return svg(W, H, "Right now: co-founding Second Algorithm, researching agent memory, AI intern at FlyRank, open to collabs.", "".join(b), style)


# ───────────────────────────── studio (about Second Algorithm) ─────────────────────────────
def sa_mark(x, y, s=1.0):
    """a small mark for the studio: two interlocking rounded squares"""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="0" y="0" width="22" height="22" rx="6" fill="none" stroke="{TEXT}" stroke-width="2.4"/>'
            f'<rect x="10" y="10" width="22" height="22" rx="6" fill="none" stroke="{OR}" stroke-width="2.4"/></g>')


def studio():
    W, H = 960, 372
    steps = [("01", "Listen", "a call, lots of questions"),
             ("02", "Sketch", "real options, not one guess"),
             ("03", "Build", "design + code, side by side"),
             ("04", "Launch", "docs, walkthrough, the keys")]
    style = f"""
.run{{animation:run 8s cubic-bezier(.6,0,.3,1) infinite}}
@keyframes run{{0%,6%{{transform:translateX(0)}}25%,31%{{transform:translateX(264px)}}50%,56%{{transform:translateX(528px)}}75%,94%{{transform:translateX(792px)}}100%{{transform:translateX(0)}}}}
.trail{{transform-box:fill-box;transform-origin:left center;animation:trail 8s cubic-bezier(.6,0,.3,1) infinite}}
@keyframes trail{{0%,6%{{transform:scaleX(0)}}25%,31%{{transform:scaleX(.3333)}}50%,56%{{transform:scaleX(.6667)}}75%,94%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
.s0{{animation:s0 8s infinite}}.s1{{animation:s1 8s infinite}}.s2{{animation:s2 8s infinite}}.s3{{animation:s3 8s infinite}}
@keyframes s0{{0%,94%{{fill:{OR}}}100%{{fill:{OR}}}}}
@keyframes s1{{0%,22%{{fill:{PANEL2}}}25%,94%{{fill:{OR}}}100%{{fill:{PANEL2}}}}}
@keyframes s2{{0%,47%{{fill:{PANEL2}}}50%,94%{{fill:{OR}}}100%{{fill:{PANEL2}}}}}
@keyframes s3{{0%,72%{{fill:{PANEL2}}}75%,94%{{fill:{OR}}}100%{{fill:{PANEL2}}}}}
.sheen{{animation:sheen 10s ease-in-out infinite}}
@keyframes sheen{{0%{{transform:translateX(-200px) skewX(-18deg)}}25%,100%{{transform:translateX(1200px) skewX(-18deg)}}}}
@media (prefers-reduced-motion: reduce){{.s1,.s2,.s3{{fill:{OR}}}.trail{{transform:none}}.run{{transform:translateX(792px)}}}}
"""
    defs = (f'<clipPath id="cl"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>'
            f'<linearGradient id="shg" x1="0" x2="1"><stop offset="0" stop-color="{OR}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{OR}" stop-opacity=".08"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></linearGradient>')
    b = [frame(W, H), f'<g clip-path="url(#cl)"><rect class="sheen" x="0" y="0" width="120" height="{H}" fill="url(#shg)"/></g>']

    b.append(sa_mark(48, 44, 1))
    b.append(t(98, 66, "Second Algorithm", 20, TEXT, 700))
    b.append(t(912, 66, "secondalgorithm.space ↗", 13.5, OR, 600, SANS, "end"))
    b.append(t(48, 124, "Design you'll notice. Systems you won't.", 34, TEXT, 400, SERIF, extra='letter-spacing="-.6"'))
    b.append(t(48, 160, "An independent creative technology studio in Bengaluru that I co-founded. We design and build", 15, MUTED))
    b.append(t(48, 182, "websites, brand systems and the automations behind them, then hand the client the keys.", 15, MUTED))

    # process track
    y = 244
    x0 = 72
    b.append(f'<rect x="{x0}" y="{y-1}" width="792" height="2" fill="{LINE}"/>')
    b.append(f'<rect class="trail" x="{x0}" y="{y-1}" width="792" height="2" fill="{OR}"/>')
    for i, (n, name, sub) in enumerate(steps):
        cx = x0 + i * 264
        b.append(f'<circle cx="{cx}" cy="{y}" r="11" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>'
                 f'<circle class="s{i}" cx="{cx}" cy="{y}" r="6" fill="{OR}"/>')
        anchor = "start" if i == 0 else "end" if i == 3 else "middle"
        ax = cx - 24 if i == 0 else cx + 24 if i == 3 else cx
        b.append(t(ax, y + 38, f"{n}  {name}", 15, TEXT, 600, SANS, anchor))
        b.append(t(ax, y + 58, sub, 12.5, DIM, 400, SANS, anchor))
    b.append(f'<g class="run"><circle cx="{x0}" cy="{y}" r="16" fill="{OR}" fill-opacity=".18"/></g>')

    # service chips
    chips = ["Web engineering", "UI/UX", "AI & ML", "Branding", "Automation", "Growth"]
    cx = 48
    for c in chips:
        w = tw(c, 12, .58) + 24
        b.append(f'<rect x="{cx}" y="330" width="{w:.0f}" height="24" rx="12" fill="{PANEL2}" stroke="{LINE}"/>'
                 + t(cx + w / 2, 346, c, 12, MUTED, 600, SANS, "middle"))
        cx += w + 8
    b.append(t(912, 346, "honest timelines · code you own", 12.5, DIM, 500, SANS, "end"))
    return svg(W, H, "Second Algorithm: an independent creative technology studio in Bengaluru. Design you'll notice. Systems you won't.", "".join(b), style, defs)


# ───────────────────────────── project cards ─────────────────────────────
PROJECTS = [
    # slug, title, status, (line1, line2), tags, tile colour, tile glyph
    ("second-algorithm", "Second Algorithm", ("live", GREEN),
     ("the studio I co-founded, and the site that", "has to prove what the studio says."),
     ["React", "Vite", "TypeScript"], "#2a2724", "SA"),
    ("urban-premium-coworks", "Urban Premium Coworks", ("live", GREEN),
     ("a prerendered, SEO-first site for a premium", "coworking space in Bengaluru."),
     ["React", "Motion", "Prerender"], "#8a5a44", "U"),
    ("windecor-interiors", "Windecor Interiors", ("live", GREEN),
     ("a film-led website for an interior studio:", "homes, cafés and boutiques."),
     ["TypeScript", "Video", "Web design"], "#4a4d5c", "W"),
    ("supportops-ai", "SupportOps AI", ("open source", OR2),
     ("an environment that scores AI agents on", "support triage under SLA pressure."),
     ["Python", "OpenEnv", "Docker"], "#6b5aa8", "⚡"),
    ("habitual", "Habitual", ("live", GREEN),
     ("a habit tracker with a consistency heatmap", "and an AI habit assistant."),
     ["Next.js", "TypeScript", "Tailwind"], "#6f7a52", "H"),
    ("evidence-calibrated-memory", "Evidence-Calibrated Memory", ("research", VIOLET),
     ("agent memory as revisable beliefs, with", "evidence, provenance and contradictions."),
     ["LLM agents", "Memory", "Evals"], "#7a4f6e", "M"),
]


def card(i, slug, title, status, lines, tags, tile, glyph):
    W, H = 420, 206
    label, scol = status
    style = f"""
.bob{{animation:bob 3.4s ease-in-out infinite alternate}}
@keyframes bob{{from{{transform:translateY(0)}}to{{transform:translateY(-4px)}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(3);opacity:0}}}}
.sheen{{animation:sheen 9s ease-in-out infinite}}
@keyframes sheen{{0%{{transform:translateX(-160px) skewX(-18deg)}}22%,100%{{transform:translateX(580px) skewX(-18deg)}}}}
.nudge{{animation:nudge 1.8s ease-in-out infinite alternate}}
@keyframes nudge{{from{{transform:translateX(0)}}to{{transform:translateX(5px)}}}}
"""
    defs = (f'<clipPath id="cl"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>'
            f'<linearGradient id="shg" x1="0" x2="1"><stop offset="0" stop-color="{TEXT}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{TEXT}" stop-opacity=".06"/><stop offset="1" stop-color="{TEXT}" stop-opacity="0"/></linearGradient>')
    d = i * 1.3
    b = [frame(W, H),
         f'<g clip-path="url(#cl)"><rect class="sheen" style="animation-delay:{d:.1f}s" x="0" y="0" width="70" height="{H}" fill="url(#shg)"/></g>']
    # icon tile
    gsize = 20 if len(glyph) == 1 else 15
    b.append(f'<g class="bob" style="animation-delay:-{d:.1f}s"><rect x="24" y="24" width="44" height="44" rx="12" fill="{tile}" stroke="{TEXT}" stroke-opacity=".12"/>'
             + (sa_mark(32, 32, .78) if glyph == "SA" else t(46, 46 + gsize * .36, glyph, gsize, TEXT, 700, SANS, "middle"))
             + '</g>')
    b.append(t(84, 44, title, 20 if len(title) < 22 else 17.5, TEXT, 700, extra='letter-spacing="-.3"'))
    b.append(f'<circle class="pulse" style="animation-delay:-{d:.1f}s" cx="89" cy="61" r="3.5" fill="{scol}"/><circle cx="89" cy="61" r="3.5" fill="{scol}"/>'
             + t(99, 65.5, label, 12.5, MUTED, 500))
    b.append(t(24, 104, lines[0], 15, "#d9d2c9"))
    b.append(t(24, 125, lines[1], 15, "#d9d2c9"))
    x = 24
    for tag in tags:
        w = tw(tag, 11.5, .6) + 22
        b.append(f'<rect x="{x:.1f}" y="152" width="{w:.0f}" height="24" rx="12" fill="{PANEL2}" stroke="{LINE}"/>'
                 + t(x + w / 2, 168, tag, 11.5, MUTED, 600, SANS, "middle"))
        x += w + 6
    cta = "view source →" if slug == "supportops-ai" else "view case →"
    b.append(f'<g class="nudge" style="animation-delay:-{d:.1f}s">' + t(396, 168, cta, 12.5, OR, 700, SANS, "end") + '</g>')
    return svg(W, H, f"{title}: {lines[0]} {lines[1]}", "".join(b), style, defs)


# ───────────────────────────── toolbox ─────────────────────────────
def stack():
    rows = [("models", ["Python", "PyTorch", "TensorFlow", "scikit-learn", "Pandas", "Jupyter"]),
            ("agents", ["LLM APIs", "RAG", "Evals", "OpenEnv"]),
            ("product", ["TypeScript", "React", "Next.js", "Vite", "Tailwind", "Motion"]),
            ("data", ["Supabase", "Firebase", "Postgres", "DuckDB"]),
            ("design", ["Figma", "Framer"]),
            ("ship", ["Vercel", "Docker", "Git", "GitHub Actions"])]
    W = 960
    top = 56
    rh = 42
    H = top + 22 + rh * len(rows) + 16
    cyc = 12
    style = f"""
.r{{opacity:0;animation:row {cyc}s infinite}}
@keyframes row{{0%{{opacity:0;transform:translateX(-8px)}}3%,92%{{opacity:1;transform:translateX(0)}}97%,100%{{opacity:0}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion: reduce){{.r{{opacity:1}}}}
"""
    defs = f'<clipPath id="cl"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>'
    b = [frame(W, H),
         f'<g clip-path="url(#cl)"><rect x="0" y="0" width="{W}" height="40" fill="{PANEL2}"/><rect x="0" y="40" width="{W}" height="1" fill="{LINE}"/></g>']
    b += [f'<circle cx="{24+i*20}" cy="20" r="6" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))]
    b.append(t(W / 2, 25, "~/toolbox", 13, MUTED, 500, MONO, "middle"))
    for i, (dirname, tools) in enumerate(rows):
        y = top + 22 + i * rh
        g = [t(32, y, "$", 13.5, OR, 600, MONO), t(48, y, f"ls {dirname}/", 13.5, DIM, 400, MONO)]
        x = 190
        for tool in tools:
            w = tw(tool, 13, .53) + 24
            g.append(f'<rect x="{x:.1f}" y="{y-17}" width="{w:.0f}" height="26" rx="7" fill="{PANEL2}" stroke="{LINE}"/>'
                     + t(x + w / 2, y + .5, tool, 13, TEXT, 500, SANS, "middle"))
            x += w + 8
        b.append(f'<g class="r" style="animation-delay:{i*0.35:.2f}s">' + "".join(g) + '</g>')
    yl = top + 22 + len(rows) * rh - 6
    b.append(t(32, yl, "$", 13.5, OR, 600, MONO) + f'<rect class="blink" x="48" y="{yl-12}" width="8" height="15" fill="{OR}"/>')
    return svg(W, H, "Toolbox: Python, PyTorch, TensorFlow, scikit-learn, TypeScript, React, Next.js, Supabase, Figma, Vercel and more", "".join(b), style, defs)


# ───────────────────────────── dock ─────────────────────────────
ICON = {
    "portfolio": lambda: t(28, 36, "A.", 22, TEXT, 700, SERIF, "middle"),
    "studio": lambda: sa_mark(13, 13, .9),
    "linkedin": lambda: t(28, 37, "in", 24, "#ffffff", 800, SANS, "middle"),
    "instagram": lambda: (f'<rect x="15" y="15" width="26" height="26" rx="8" fill="none" stroke="#fff" stroke-width="2.6"/>'
                          f'<circle cx="28" cy="28" r="6" fill="none" stroke="#fff" stroke-width="2.6"/><circle cx="35.5" cy="20.5" r="1.8" fill="#fff"/>'),
    "email": lambda: (f'<rect x="13" y="17" width="30" height="22" rx="4" fill="none" stroke="{TEXT}" stroke-width="2.4"/>'
                      f'<path d="M14 19l14 11 14-11" fill="none" stroke="{OR}" stroke-width="2.4" stroke-linejoin="round"/>'),
    "call": lambda: (f'<rect x="14" y="16" width="28" height="26" rx="5" fill="#fff"/><rect x="14" y="16" width="28" height="8" rx="4" fill="{OR}"/>'
                     f'<rect x="14" y="21" width="28" height="3" fill="{OR}"/>'
                     + t(28, 38.5, "15", 12, "#1a1715", 800, SANS, "middle")),
}
DOCK_BG = {"portfolio": "#2a2724", "studio": "#1d1a17", "linkedin": "#0a66c2",
           "instagram": "#c13584", "email": "#2a2724", "call": "#3a2a22"}


def dock(i, key):
    style = """
.hop{animation:hop 5s ease-in-out infinite}
@keyframes hop{0%{transform:translateY(0)}6%{transform:translateY(-14px)}12%{transform:translateY(0)}17%{transform:translateY(-5px)}22%,100%{transform:translateY(0)}}
"""
    body = (f'<g class="hop" style="animation-delay:{i*0.45:.2f}s"><g transform="translate(8 20)">'
            f'<rect width="56" height="56" rx="15" fill="{DOCK_BG[key]}"/>'
            f'<rect x=".5" y=".5" width="55" height="55" rx="14.5" fill="none" stroke="#fff" stroke-opacity=".14"/>'
            f'{ICON[key]()}</g></g>')
    return svg(72, 92, key, body, style)


if __name__ == "__main__":
    write("banner.svg", banner())
    write("now.svg", now())
    write("studio.svg", studio())
    for i, p in enumerate(PROJECTS):
        write(f"card-{p[0]}.svg", card(i, *p))
    write("stack.svg", stack())
    for i, k in enumerate(ICON):
        write(f"dock-{k}.svg", dock(i, k))
