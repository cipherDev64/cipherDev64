# Draws assets/activity.svg: my real GitHub contribution graph, week columns rising in one after another.
# Stdlib only, so a scheduled GitHub Action can refresh it. Usage: python3 build_activity.py [user] [out.svg]
import json, sys, os, urllib.request, datetime

USER = sys.argv[1] if len(sys.argv) > 1 else "cipherDev64"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "activity.svg")
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
PANEL, PANEL2, LINE, TEXT, MUTED, DIM, OR = "#161412", "#1d1a17", "#2b2723", "#f3eee7", "#a1978d", "#6a625b", "#ef6a3a"
LEVEL = ["#24201d", "#5c2d1c", "#9a4322", "#d65a2d", "#f68a55"]

req = urllib.request.Request(f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last", headers={"User-Agent": "profile-readme"})
data = json.load(urllib.request.urlopen(req, timeout=30))
days, total = data["contributions"], data["total"]["lastYear"]
today_iso = datetime.date.today().isoformat()
days = [d for d in days if d["date"] <= today_iso]

# weeks start on Sunday; pad the first column
first = datetime.date.fromisoformat(days[0]["date"])
pad = (first.weekday() + 1) % 7
cells = [None] * pad + days
weeks = [cells[i:i + 7] for i in range(0, len(cells), 7)]

# current streak (today with zero doesn't break it yet)
streak = 0
for i in range(len(days) - 1, -1, -1):
    if days[i]["count"] > 0:
        streak += 1
    elif i != len(days) - 1:
        break
today = days[-1]["count"]
best = max(days, key=lambda d: d["count"])
active = sum(1 for d in days if d["count"] > 0)

CELL, GAP = 13, 3.4
W, H = 960, 300
gx = (W - (len(weeks) * (CELL + GAP) - GAP)) / 2
gy = 132

cols, labels, last_m, last_x = [], [], None, -999
for wi, wk in enumerate(weeks):
    x = gx + wi * (CELL + GAP)
    rects = "".join(
        f'<rect x="{x:.1f}" y="{gy + di * (CELL + GAP):.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{LEVEL[d["level"]]}"/>'
        for di, d in enumerate(wk) if d)
    cols.append(f'<g class="c" style="animation-delay:{wi * 0.05:.2f}s">{rects}</g>')
    m = datetime.date.fromisoformat(next(d for d in wk if d)["date"]).strftime("%b")
    if m != last_m and wi < len(weeks) - 2 and x - last_x >= 44:
        labels.append(f'<text x="{x:.1f}" y="{gy - 9}" font-family="{SANS}" font-size="10.5" fill="{DIM}">{m}</text>')
        last_m, last_x = m, x
for di, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    labels.append(f'<text x="{gx - 8:.1f}" y="{gy + di * (CELL + GAP) + 10.5:.1f}" text-anchor="end" font-family="{SANS}" font-size="10" fill="{DIM}">{lab}</text>')


def stat(x, big, small, anchor="start"):
    return (f'<text x="{x:.1f}" y="88" text-anchor="{anchor}" font-family="{SANS}" font-size="24" font-weight="800" letter-spacing="-.5" fill="{TEXT}">{big}</text>'
            f'<text x="{x:.1f}" y="107" text-anchor="{anchor}" font-family="{SANS}" font-size="12" fill="{MUTED}">{small}</text>')


right = gx + len(weeks) * (CELL + GAP) - GAP
mid_big = f'<tspan class="fire">🔥</tspan> {streak}-day streak' if streak >= 3 else f"{active} active days"
mid_small = f"{today} today" if streak >= 3 else "in the last year"
legend_x = right
legend = "".join(f'<rect x="{legend_x - 16 * (5 - i) - 30:.1f}" y="{H - 34}" width="11" height="11" rx="2.5" fill="{LEVEL[i]}"/>' for i in range(5))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{total} GitHub contributions in the last year">
<defs><clipPath id="cl"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath></defs>
<style>
.c{{opacity:0;animation:rise 14s cubic-bezier(.2,.8,.2,1) infinite backwards}}
@keyframes rise{{0%{{opacity:0;transform:translateY(10px)}}4%{{opacity:1;transform:translateY(0)}}90%{{opacity:1}}96%,100%{{opacity:0}}}}
.fire{{animation:fire 1.6s ease-in-out infinite alternate}}
@keyframes fire{{from{{opacity:.75}}to{{opacity:1}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}.c{{opacity:1}}}}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{PANEL}"/><rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="17.5" fill="none" stroke="{LINE}"/>
<g clip-path="url(#cl)"><rect width="{W}" height="40" fill="{PANEL2}"/><rect y="40" width="{W}" height="1" fill="{LINE}"/></g>
<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>
<text x="{W/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">git log --author={USER}</text>
{stat(gx, f"{total:,}", "contributions in the last year")}
{stat(W/2, mid_big, mid_small, "middle")}
{stat(right, str(best["count"]), "best day, " + datetime.date.fromisoformat(best["date"]).strftime("%b %-d"), "end")}
{"".join(labels)}
{"".join(cols)}
<text x="{gx:.1f}" y="{H - 25}" font-family="{MONO}" font-size="10.5" fill="{DIM}">refreshed {today_iso}</text>
<text x="{legend_x - 16*5 - 36:.1f}" y="{H - 25}" text-anchor="end" font-family="{SANS}" font-size="10.5" fill="{DIM}">less</text>{legend}<text x="{legend_x - 14:.1f}" y="{H - 25}" font-family="{SANS}" font-size="10.5" fill="{DIM}">more</text>
</svg>'''
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(svg)
print(f"{total} contributions, {streak}-day streak, {len(weeks)} weeks, {len(svg)/1024:.1f} KB")
