#!/usr/bin/env python3
"""Generate mario-run.svg: self-playing, scrolling, looping Mario career run (no input)."""
import html
from pathlib import Path
MARIO_SPRITE = [
    "...RRRRR....",
    "..RRRRRRRRR.",
    "..BBBSSBS...",
    ".BSBSSSBSSS.",
    ".BSBBSSSBSSS",
    ".BBSSSSBBBB.",
    "...SSSSSSS..",
    "..RRCRRR....",
    ".RRRCRRRCR..",
    "RRRRCCCCRRRR",
    "SSRCYSYCRSS.",
    "SSSCCCCCCSSS",
    "..CCC..CCC..",
    ".BBBB..BBBB.",
]

PALETTE = {
    "R": "#E8857A",
    "S": "#F5D87A",
    "Y": "#F5D87A",
    "B": "#1A1A1A",
    "C": "#F2EDD7",
}

# (label, kind, date, title, detail, commits)  kind: start | repo | mile | pipe | flag
S = [  # repos/commits roll up everything created since the previous stop (dlml not shown)
 ("CS", "start", "", "START :: CS @ UNIVERSITY OF DEBRECEN", "Computer Science student. The run begins here.", 0, 0),
 ("JobFind", "repo", "JAN 2026", "Job-Finder", "OCR + Llama 3 resume parser + TF-IDF MLP (90% val acc)", 35, 3),
 ("sol", "repo", "JUN 2026", "sol", "Local-first open-source AI coding assistant, council + RAG", 155, 8),
 ("InnerScript", "mile", "JUL 2026", "TECH LEAD (VOLUNTEER) @ INNERSCRIPT", "Built a mental-health community platform: 8000+ users/followers", 0, 0),
 ("NEVERMISS", "mile", "JUL 2026", "NEVERMISSAI :: KANZ AI HACKATHON GOLD", "Autonomous voice agent (Twilio, Groq Llama 3.3, ChromaDB)", 59, 2),
 ("Orchestrate", "repo", "AUG 2026", "HACKERRANK ORCHESTRATE :: 300 / 1800", "LLM competition: WhatsApp notification router (OCR + speech + RAG)", 2, 1),
 ("Lineage", "repo", "AUG 2026", "lineage-revocation", "Research: COSE_Sign1 + RFC 8949 CBOR delegation revocation verifier", 64, 1),
 ("BMW", "mile", "1 OCT 2026", "JOINED BMW :: AGENTIC AI INTERN", "Practice builds (researchAgent, bot, offline) led here", 59, 3),
 ("rove", "repo", "OCT 2026", "rove", "macOS computer-use agent: specialists, voice, approval gates", 59, 1),
 ("RESET", "pipe", "OCT 2026", "RESET", "Local-first AI health app (SwiftUI + SwiftData)", 108, 2),
 ("CO-OP", "flag", "", "COURSE CLEAR! :: LET'S BUILD TOGETHER", "LinkedIn /in/16a9da · rayyan.tanweer@gmail.com · Discord", 0, 0),
]
W, H, GY, T, SP, FOCUS = 640, 250, 150, 5.5, 96, 190
N = len(S)
COL = [44 + i * SP for i in range(N)]
WORLD = COL[-1] + 120
TOTAL = N * T
e = html.escape
pct = lambda v: f"{v * 100:.3f}%"
cam = lambda x: -min(max(x - FOCUS, 0), WORLD - (W - 8))

css = ["*{animation-duration:%.1fs;animation-iteration-count:infinite;animation-timing-function:linear}" % TOTAL,
       ".m{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:800}.s{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;font-weight:600}"]

kx, kc = [], []
def stop(f, i):
    kx.append(f"{pct(f)}{{transform:translateX({COL[i]}px)}}")
    kc.append(f"{pct(f)}{{transform:translateX({cam(COL[i])}px)}}")
for i in range(N):
    stop(i / N if i == 0 else (i + .0) / N, i) if i == 0 else None
    stop((i + .62) / N, i)
    if i < N - 1:
        stop((i + 1) / N, i + 1)
stop((N - .06) / N, N - 1); stop(1, N - 1)
css.append("@keyframes run{" + "".join(kx) + "}.run{animation-name:run}@keyframes cam{" + "".join(kc) + "}.cam{animation-name:cam}")

ky = ["0%{transform:translateY(0)}"]
for i in range(N):
    a = i / N
    ky += [f"{pct(a + .02 / N)}{{transform:translateY(0);animation-timing-function:ease-out}}",
           f"{pct(a + .14 / N)}{{transform:translateY(-24px);animation-timing-function:ease-in}}",
           f"{pct(a + .28 / N)}{{transform:translateY(0)}}"]
ky.append("100%{transform:translateY(0)}")
css.append("@keyframes hop{" + "".join(ky) + "}.hop{animation-name:hop}")

for i in range(N):
    a, b = i / N, (i + 1) / N
    hit = a + .14 / N
    css.append(f"@keyframes v{i}{{0%,{pct(a)}{{opacity:0}}{pct(a + .02 / N)},{pct(b - .02 / N)}{{opacity:1}}{pct(b)},100%{{opacity:0}}}}.v{i}{{animation-name:v{i};opacity:0}}")
    if S[i][1] in ("repo", "mile"):
        css.append(f"@keyframes h{i}{{0%,{pct(hit)}{{opacity:0}}{pct(hit + .001)},99.9%{{opacity:1}}100%{{opacity:0}}}}.h{i}{{animation-name:h{i};opacity:0}}")
        css.append(f"@keyframes q{i}{{0%,{pct(hit)}{{opacity:1}}{pct(hit + .001)},99.9%{{opacity:0}}100%{{opacity:1}}}}.q{i}{{animation-name:q{i}}}")
        css.append(f"@keyframes c{i}{{0%,{pct(hit)}{{opacity:0;transform:translateY(0)}}{pct(hit + .02 / N)}{{opacity:1;transform:translateY(-10px)}}{pct(hit + .30 / N)}{{opacity:1;transform:translateY(-12px)}}{pct(hit + .34 / N)},100%{{opacity:0}}}}.c{i}{{animation-name:c{i};opacity:0}}")
        css.append(f"@keyframes b{i}{{0%,{pct(hit - .01 / N)}{{transform:translateY(0)}}{pct(hit + .03 / N)}{{transform:translateY(-5px)}}{pct(hit + .08 / N)},100%{{transform:translateY(0)}}}}.b{i}{{animation-name:b{i}}}")
css.append("@keyframes fl{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.7)}}.fl{animation-name:fl;animation-duration:.8s;transform-box:fill-box;transform-origin:left}")

px = 3
sprite = "".join(f'<rect x="{c * px - 18}" y="{r * px - 42}" width="{px}" height="{px}" fill="{PALETTE[ch]}"/>'
                 for r, row in enumerate(MARIO_SPRITE) for c, ch in enumerate(row) if ch in PALETTE)

objs, info = [], []
repos = commits = 0
for i, (lbl, k, date, title, detail, cm, rp) in enumerate(S):
    cx, l = COL[i], e(lbl)
    if k in ("repo", "mile"):
        w, sym = (30, "?") if k == "repo" else (40, "★")
        x0 = cx - w // 2
        def box(fill, s):
            return (f'<rect x="{x0}" y="74" width="{w}" height="28" fill="{fill}" stroke="#1A1A1A" stroke-width="2.5"/>'
                    f'<text x="{cx}" y="94" text-anchor="middle" class="m" font-size="15" fill="#1A1A1A">{s}</text>')
        objs.append(f'<g class="b{i}"><rect x="{x0 + 3}" y="77" width="{w}" height="28" fill="#1A1A1A"/>'
                    f'<g class="q{i}">{box("#F5D87A", sym)}</g><g class="h{i}">{box("#E8857A", "!" if k == "repo" else "★")}</g></g>'
                    f'<circle class="c{i}" cx="{cx}" cy="52" r="6" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2"/>'
                    f'<text x="{cx}" y="68" text-anchor="middle" class="m" font-size="8.5" fill="#1A1A1A">{l}</text>')
    elif k == "start":
        objs.append(f'<rect x="{cx - 22}" y="84" width="44" height="22" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2.5"/>'
                    f'<text x="{cx}" y="99" text-anchor="middle" class="m" font-size="10" fill="#1A1A1A">{l}</text>')
    elif k == "pipe":
        objs.append(f'<rect x="{cx - 20}" y="118" width="40" height="11" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5"/>'
                    f'<rect x="{cx - 15}" y="129" width="30" height="{GY - 129}" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5"/>'
                    f'<text x="{cx}" y="111" text-anchor="middle" class="m" font-size="8.5" fill="#1A1A1A">{l}</text>')
    else:
        objs.append(f'<line x1="{cx}" y1="66" x2="{cx}" y2="{GY}" stroke="#1A1A1A" stroke-width="3"/>'
                    f'<circle cx="{cx}" cy="64" r="5" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2"/>'
                    f'<polygon class="fl" points="{cx},70 {cx - 28},81 {cx},92" fill="#E8857A" stroke="#1A1A1A" stroke-width="2"/>'
                    f'<text x="{cx}" y="56" text-anchor="middle" class="m" font-size="8.5" fill="#1A1A1A">{l}</text>')
    commits += cm; repos += rp
    objs.append(f'<circle cx="{cx}" cy="{GY + 11}" r="4" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2"/>')
    head = f"{date} :: {title}" if date and k in ("repo", "pipe") else (f"{date} :: {title}" if date else title)
    info.append(
        f'<g class="v{i}"><text x="14" y="203" class="m" font-size="11" fill="#1A1A1A">▶ {e(head)}</text>'
        f'<text x="14" y="224" class="s" font-size="12.5" fill="#1A1A1A">{e(detail)}</text>'
        f'<text x="{W - 14}" y="25" text-anchor="end" class="m" font-size="11" fill="#1A1A1A">COMMITS {commits:04d}</text>'
        f'<text x="{W // 2}" y="25" text-anchor="middle" class="m" font-size="11" fill="#1A1A1A">REPOS x{repos:02d}</text>'
        f'<text x="14" y="25" class="m" font-size="11" fill="#1A1A1A">STAGE {i:02d}/{N - 1}</text></g>')

bricks = "".join(f'<line x1="{x}" y1="{GY}" x2="{x}" y2="{GY + 22}" stroke="#1A1A1A" stroke-width="2" opacity=".35"/>' for x in range(-4, WORLD + 700, 40))
def cloud(x, y):
    return (f'<g transform="translate({x},{y})"><rect width="42" height="10" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2"/>'
            f'<rect x="10" y="-6" width="22" height="8" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2"/><rect x="12" y="-1" width="18" height="3" fill="#F2EDD7"/></g>')
clouds = "".join(cloud(120 + j * 310, 46 + (j % 3) * 4) for j in range(N * SP // 310 + 2))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rayyan Ahmed career as a Mario level: CS at University of Debrecen, 21 public repos, InnerScript, Kanz AI gold, BMW, RESET, co-op flag">
<style>{"".join(css)}</style>
<defs><clipPath id="v"><rect x="3" y="3" width="{W - 8}" height="{GY + 22 - 3}"/></clipPath></defs>
<rect x="6" y="6" width="{W - 8}" height="{H - 8}" fill="#1A1A1A"/>
<rect x="3" y="3" width="{W - 8}" height="{H - 8}" fill="#6ECFCF" stroke="#1A1A1A" stroke-width="3"/>
<g clip-path="url(#v)"><g class="cam">
{clouds}
<rect x="-700" y="{GY}" width="{WORLD + 1400}" height="22" fill="#E8857A" stroke="#1A1A1A" stroke-width="3"/>{bricks}
{"".join(objs)}
<g class="run"><g class="hop"><g transform="translate(0,{GY})">{sprite}</g></g></g>
</g></g>
<rect x="3" y="3" width="{W - 8}" height="32" fill="#F5D87A" stroke="#1A1A1A" stroke-width="3"/>
<rect x="3" y="180" width="{W - 8}" height="62" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="3"/>
{"".join(info)}
</svg>
'''
Path(__file__).with_name("mario-run.svg").write_text(svg, encoding="utf-8")
print(N, "stages", commits, "commits", repos, "repos", len(svg), "bytes")

# ---- clickable retro social buttons (GitHub can't click inside an <img> SVG) + README ----
C = "#1A1A1A"
T = 'fill="%s" text-anchor="middle" style="font:800 %dpx ui-monospace,Menlo,Consolas,monospace"'
ICONS = {  # 24x24 glyphs on a dark tile
 "linkedin": f'<text x="12" y="19" {T % (C, 22)}>in</text>',
 "email": f'<text x="12" y="20" {T % (C, 26)}>@</text>',
 "discord": (f'<rect x="0" y="6" width="24" height="13" fill="{C}"/><rect x="2" y="3" width="20" height="3" fill="{C}"/>'
             '<rect x="3.5" y="11" width="6" height="2.4" fill="FILL"/><rect x="5.3" y="9.2" width="2.4" height="6" fill="FILL"/>'
             '<rect x="14" y="10" width="3" height="3" fill="FILL"/><rect x="18" y="13" width="3" height="3" fill="FILL"/>'),
 "play": '<polygon points="5,1 23,12 5,23" fill="#1A1A1A"/>',
 "github": f'<text x="12" y="18" {T % (C, 17)}>&gt;_</text>',
}
GH = "https://github.com/16A9DA"
PAGES = "https://16a9da.github.io/16A9DA/"
BTNS = [  # file, text, fill, url
 ("play", "PLAY GAME", "#E8857A", PAGES),
 ("linkedin", "LinkedIn", "#F5D87A", "https://linkedin.com/in/16a9da"),
 ("email", "Email", "#E8857A", "mailto:rayyan.tanweer@gmail.com"),
 ("discord", "Discord", "#F2EDD7", "https://discordapp.com/users/584487184141254731"),
 ("github", "GitHub", "#6ECFCF", GH + "?tab=repositories"),
]
out = Path(__file__).with_name("btn")
out.mkdir(exist_ok=True)
for old in out.glob("*.svg"):
    old.unlink()
links = []
links = {}
for name, text, fill, url in BTNS:
    icon = name == "play"
    w, h = (68, 40) if icon else (len(text) * 7 + 22, 24)
    body = (f'<g transform="translate({(w - 24) / 2},{(h - 24) / 2})">{ICONS[name]}</g>' if icon else
            f'<text x="{w / 2}" y="{h / 2 + 4}" text-anchor="middle" fill="#1A1A1A" style="font:800 11px ui-monospace,Menlo,Consolas,monospace">{e(text)}</text>')
    (out / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 5}" height="{h + 5}" viewBox="0 0 {w + 5} {h + 5}" role="img" aria-label="{e(text)}">'
        f'<rect x="5" y="5" width="{w}" height="{h}" fill="#1A1A1A"/>'
        f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" fill="{fill}" stroke="#1A1A1A" stroke-width="3"/>{body}</svg>\n', encoding="utf-8")
    links[name] = f'<a href="{url}"><img src="./btn/{name}.svg" alt="{e(text)}" height="{h + 5}" /></a>'
ALT = "Rayyan Ahmed: Mario runs from CS at University of Debrecen through Job-Finder, sol, InnerScript, NEVERMISSAI (Kanz AI gold), lineage-revocation, rove, BMW (Agentic AI Intern, Oct 2026) and RESET to the co-op flag"
row = "&nbsp;".join(v.replace("<img ", '<img align="absmiddle" ') for n, v in links.items() if n != "play")
Path(__file__).with_name("README.md").write_text(
    '<div align="center">\n'
    f'<a href="{GH}?tab=repositories"><img src="./mario-run.svg" alt="{ALT}" width="640" /></a><br>\n'
    f'{links["play"]}<br>\n{row}\n</div>\n', encoding="utf-8")

# ---- playable version (GitHub Pages): arrows / WASD / touch ----
import json
URLS = {"JobFind": GH + "/Job-Finder", "sol": GH + "/sol", "NEVERMISS": GH + "/NEVERMISSAI", "Lineage": GH + "/lineage-revocation",
        "rove": GH + "/rove", "RESET": GH + "/RESET", "InnerScript": "https://innerscript.ca/", "BMW": "https://linkedin.com/in/16a9da",
        "CO-OP": "https://linkedin.com/in/16a9da"}
# Full chronological level for the playable game: every public repo (private ones are never listed).
FULL = [  # label, kind, date, title, detail, commits, repos, github repo, story
 ("CS", "start", "", "START :: CS @ UNIVERSITY OF DEBRECEN", "Computer Science student. The run begins here.", 0, 0, "", "Everything below was learned, built and shipped from here."),
 ("MovieNLP", "repo", "NOV 2025", "Movie-Sentiment", "NLP project: movie review sentiment classification", 29, 1, "Movie-Sentiment", "First ML project: getting hands-on with NLP."),
 ("CS50AI", "repo", "DEC 2025", "CS50AI", "Harvard CS50 AI course projects", 5, 1, "CS50AI", "Course learning: the stepping stone to Job-Finder."),
 ("JobFind", "repo", "JAN 2026", "Job-Finder", "OCR + Llama 3 resume parser + TF-IDF MLP (90% val acc)", 1, 1, "Job-Finder", "Built with what CS50AI taught me."),
 ("Studdy", "repo", "MAR 2026", "StuddyBuddy", "Collaborative study platform", 6, 1, "StuddyBuddy", "Where I learned how to build websites."),
 ("DataSci", "repo", "APR 2026", "Data-Science", "Data science portfolio: projects & notebooks", 12, 1, "Data-Science", "Learned data science here, then put it to work."),
 ("Claude", "repo", "APR 2026", "Claude", "Learning Claude Code: features, hooks, optimization", 3, 1, "Claude", "Understanding the tools I build with."),
 ("P2Exploit", "repo", "MAY 2026", "Prompt2Exploit", "Security study: AI-written vs human-written web apps", 1, 1, "Prompt2Exploit", "Data science applied to AI security."),
 ("SensML", "repo", "MAY 2026", "predictive-maintenance", "10k sensor anomaly pipeline; GBDT F1 0.68 on 3.4% failures", 16, 1, "predictive-maintenance-failure-detection", "Data science applied to machine failure."),
 ("Portfolio", "repo", "MAY 2026", "me", "My personal portfolio website", 28, 1, "me", "Built with the web skills from StuddyBuddy."),
 ("WidgetAI", "repo", "JUN 2026", "WidgetAI", "Desktop widget: many AI providers from one place", 17, 1, "WidgetAI", "A warm-up for building sol."),
 ("sol", "repo", "JUN 2026", "sol", "Local-first open-source AI coding assistant, council + RAG", 72, 1, "sol", "The real build, after WidgetAI."),
 ("InnerScript", "mile", "JUL 2026", "TECH LEAD (VOLUNTEER) @ INNERSCRIPT", "Mental-health community platform: 8000+ users/followers", 0, 0, "", "I built the whole website myself."),
 ("Orbit", "repo", "JUL 2026", "Orbit", "All-in-one AI dashboard: APIs, billing, alerts, automation", 43, 1, "Orbit", "Built to monitor my website's costs and usage."),
 ("NEVERMISS", "mile", "JUL 2026", "NEVERMISSAI :: KANZ AI HACKATHON GOLD", "Autonomous voice agent (Twilio, Groq Llama 3.3, ChromaDB)", 16, 1, "NEVERMISSAI", "Possible because of everything I learned on Orbit."),
 ("Orchestr.", "mile", "AUG 2026", "HACKERRANK ORCHESTRATE :: 300 / 1800", "LLM competition: WhatsApp notification router (OCR, speech, RAG, LLM)", 2, 1, "whatsapp-notification-router", "Placed 300th out of 1,800 participants."),
 ("Lineage", "repo", "AUG 2026", "lineage-revocation", "Research: COSE_Sign1 + RFC 8949 CBOR delegation revocation verifier", 64, 1, "lineage-revocation", "Research out of curiosity about agentic AI security."),
 ("Research", "repo", "AUG 2026", "researchAgent", "Local LLM research agent", 9, 1, "researchAgent", "Practice build to get sharper."),
 ("bot", "repo", "SEP 2026", "bot", "Python bot", 30, 1, "bot", "Practice build to get sharper."),
 ("offline", "repo", "SEP 2026", "offline", "Self-hosted AI companion: chat, documents, memory, automation", 20, 1, "offline", "Practice build. Proficiency that led to BMW."),
 ("BMW", "mile", "1 OCT 2026", "JOINED BMW :: AGENTIC AI INTERN", "System design · LangChain · agentic AI in production", 0, 0, "", "All that practice paid off."),
 ("rove", "repo", "SEP-OCT 2026", "rove", "macOS computer-use agent: specialists, voice, approval gates", 59, 1, "rove", "Built after joining BMW."),
 ("AgentNotes", "repo", "OCT 2026", "AgenticNotes", "Agentic AI theory notes", 4, 1, "AgenticNotes", "My contribution to the Generative AI class, shared by my professor."),
 ("RESET", "pipe", "OCT 2026", "RESET", "Local-first AI health app (SwiftUI + SwiftData)", 104, 1, "RESET", "Built after joining BMW."),
 ("CO-OP", "flag", "", "COURSE CLEAR! :: LET'S BUILD TOGETHER", "LinkedIn /in/16a9da · rayyan.tanweer@gmail.com · Discord", 0, 0, "", "Thanks for playing through the story."),
]
EXTRA_URL = {"InnerScript": "https://innerscript.ca/", "BMW": "https://linkedin.com/in/16a9da", "CO-OP": "https://linkedin.com/in/16a9da"}
data = [dict(label=r[0], kind=r[1], date=r[2], title=r[3], detail=r[4], cm=r[5], rp=r[6], story=r[8],
             url=(GH + "/" + r[7]) if r[7] else EXTRA_URL.get(r[0], "")) for r in FULL]
PITS = [4, 9, 13, 17, 21]  # a gap after these stages
GOOMBAS = [2, 6, 11, 15, 19, 22]  # a bug patrols between these stage and the next
GAME = Path(__file__).with_name("game.tpl.html").read_text(encoding="utf-8")
sprite_js = json.dumps(MARIO_SPRITE)
Path(__file__).with_name("index.html").write_text(
    GAME.replace("__DATA__", json.dumps(data)).replace("__PITS__", json.dumps(PITS)).replace("__GOOMBAS__", json.dumps(GOOMBAS)).replace("%SPRITE%", sprite_js).replace("%PALETTE%", json.dumps(PALETTE)), encoding="utf-8")
