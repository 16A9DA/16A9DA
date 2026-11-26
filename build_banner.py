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
S = [  # repos/commits roll up everything created since the previous stop
 ("CS", "start", "", "START :: CS @ UNIVERSITY OF DEBRECEN", "Computer Science student. The run begins here.", 0, 0),
 ("JobFind", "repo", "JAN 2026", "Job-Finder", "OCR + Llama 3 resume parser + TF-IDF MLP (90% val acc)", 35, 3),
 ("sol", "repo", "JUN 2026", "sol", "Local-first open-source AI coding assistant, council + RAG", 155, 8),
 ("InnerScript", "mile", "JUL 2026", "TECH LEAD (VOLUNTEER) @ INNERSCRIPT", "Built a mental-health community platform: 8000+ users/followers", 0, 0),
 ("NEVERMISS", "mile", "JUL 2026", "NEVERMISSAI :: KANZ AI HACKATHON GOLD", "Autonomous voice agent (Twilio, Groq Llama 3.3, ChromaDB)", 59, 2),
 ("Lineage", "repo", "AUG 2026", "lineage-revocation", "Research: COSE_Sign1 + RFC 8949 CBOR delegation revocation verifier", 73, 3),
 ("rove", "repo", "SEP 2026", "rove", "macOS computer-use agent: specialists, voice, approval gates", 118, 4),
 ("BMW", "mile", "1 OCT 2026", "JOINED BMW :: AGENTIC AI INTERN", "System design · LangChain · agentic AI in production", 0, 0),
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
