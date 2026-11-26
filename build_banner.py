#!/usr/bin/env python3
"""Generate game.svg: self-playing, looping Mario banner (no input)."""
import html
from pathlib import Path
from mario_game import STAGES, MARIO_SPRITE, PALETTE

W, H, GY, T = 640, 250, 150, 2.4   # width, height, ground y, seconds per stage
N = len(STAGES)
COL = [52 + i * 67 for i in range(N)]
TOTAL = N * T
e = html.escape
pct = lambda v: f"{v * 100:.3f}%"

css = [".m{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:800}"
       ".s{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;font-weight:600}"
       "*{animation-duration:%.1fs;animation-iteration-count:infinite;animation-timing-function:linear}" % TOTAL]

# Mario run (X) : at col[i] until 70% of slot, then run to col[i+1]
kx = [f"0%{{transform:translateX({COL[0]}px)}}"]
for i in range(N):
    kx.append(f"{pct((i + .62) / N)}{{transform:translateX({COL[i]}px)}}")
    if i < N - 1:
        kx.append(f"{pct((i + 1) / N)}{{transform:translateX({COL[i + 1]}px)}}")
kx.append(f"{pct((N - .06) / N)}{{transform:translateX({COL[-1]}px)}}")
kx.append(f"100%{{transform:translateX({COL[-1]}px)}}")
css.append("@keyframes run{" + "".join(kx) + "}.run{animation-name:run}")

# Mario jump (Y): hop at start of every slot
ky = ["0%{transform:translateY(0)}"]
for i in range(N):
    a = i / N
    ky += [f"{pct(a + .02 / N)}{{transform:translateY(0);animation-timing-function:ease-out}}",
           f"{pct(a + .14 / N)}{{transform:translateY(-24px);animation-timing-function:ease-in}}",
           f"{pct(a + .28 / N)}{{transform:translateY(0)}}"]
ky.append("100%{transform:translateY(0)}")
css.append("@keyframes hop{" + "".join(ky) + "}.hop{animation-name:hop}")

# Per-slot show/hide + block states
for i in range(N):
    a, b = i / N, (i + 1) / N
    css.append(f"@keyframes v{i}{{0%,{pct(a)}{{opacity:0}}{pct(a + .02 / N)},{pct(b - .02 / N)}{{opacity:1}}{pct(b)},100%{{opacity:0}}}}.v{i}{{animation-name:v{i};opacity:0}}")
    hit = a + .14 / N
    css.append(f"@keyframes h{i}{{0%,{pct(hit)}{{opacity:0}}{pct(hit + .001)},99.9%{{opacity:1}}100%{{opacity:0}}}}.h{i}{{animation-name:h{i};opacity:0}}")
    css.append(f"@keyframes q{i}{{0%,{pct(hit)}{{opacity:1}}{pct(hit + .001)},99.9%{{opacity:0}}100%{{opacity:1}}}}.q{i}{{animation-name:q{i}}}")
    css.append(f"@keyframes c{i}{{0%,{pct(hit)}{{opacity:0;transform:translateY(0)}}{pct(hit + .02 / N)}{{opacity:1;transform:translateY(-10px)}}{pct(hit + .30 / N)}{{opacity:1;transform:translateY(-26px)}}{pct(hit + .34 / N)},100%{{opacity:0}}}}.c{i}{{animation-name:c{i};opacity:0}}")
    css.append(f"@keyframes b{i}{{0%,{pct(hit - .01 / N)}{{transform:translateY(0)}}{pct(hit + .03 / N)}{{transform:translateY(-5px)}}{pct(hit + .08 / N)},100%{{transform:translateY(0)}}}}.b{i}{{animation-name:b{i}}}")
# cloud drift + flag wave
css.append("@keyframes cl{0%{transform:translateX(0)}100%{transform:translateX(-40px)}}.cl{animation-name:cl;animation-direction:alternate;animation-duration:"+f"{TOTAL / 2:.1f}s}}")
css.append("@keyframes fl{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.7)}}.fl{animation-name:fl;animation-duration:.8s;transform-box:fill-box;transform-origin:left}")

px = 3
sprite = "".join(f'<rect x="{c * px - 18}" y="{r * px - 42}" width="{px}" height="{px}" fill="{PALETTE[ch]}"/>'
                 for r, row in enumerate(MARIO_SPRITE) for c, ch in enumerate(row) if ch in PALETTE)

objs, info = [], []
coins = score = 0
for i, st in enumerate(STAGES):
    cx, k, lbl = COL[i], st["kind"], e(st["label"])
    if k == "qblock":
        objs.append(
            f'<g class="b{i}"><rect x="{cx - 14 + 3}" y="{74 + 3}" width="28" height="28" fill="#1A1A1A"/>'
            f'<g class="q{i}"><rect x="{cx - 14}" y="74" width="28" height="28" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5"/>'
            f'<text x="{cx}" y="94" text-anchor="middle" class="m" font-size="15">?</text></g>'
            f'<g class="h{i}"><rect x="{cx - 14}" y="74" width="28" height="28" fill="#E8857A" stroke="#1A1A1A" stroke-width="2.5"/>'
            f'<text x="{cx}" y="94" text-anchor="middle" class="m" font-size="15">!</text></g></g>'
            f'<circle class="c{i}" cx="{cx}" cy="64" r="6" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2"/>'
            f'<text x="{cx}" y="116" text-anchor="middle" class="m" font-size="8.5" fill="#1A1A1A">{lbl}</text>')
        coins += 1; score += 200
    elif k == "pipe":
        objs.append(
            f'<rect x="{cx - 20}" y="118" width="40" height="11" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5"/>'
            f'<rect x="{cx - 15}" y="129" width="30" height="{GY - 129}" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5"/>'
            f'<text x="{cx}" y="111" text-anchor="middle" class="m" font-size="8.5" fill="#1A1A1A">{lbl}</text>')
        score += 500
    elif k == "flag":
        objs.append(
            f'<line x1="{cx}" y1="66" x2="{cx}" y2="{GY}" stroke="#1A1A1A" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="64" r="5" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2"/>'
            f'<polygon class="fl" points="{cx},70 {cx - 28},81 {cx},92" fill="#E8857A" stroke="#1A1A1A" stroke-width="2"/>'
            f'<text x="{cx}" y="56" text-anchor="middle" class="m" font-size="8.5" fill="#1A1A1A">{lbl}</text>')
        score += 1000
    else:
        objs.append(
            f'<rect x="{cx - 22}" y="84" width="44" height="22" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2.5"/>'
            f'<text x="{cx}" y="99" text-anchor="middle" class="m" font-size="10" fill="#1A1A1A">{lbl}</text>')
    objs.append(f'<circle cx="{cx}" cy="{GY + 11}" r="4" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2"/>')
    info.append(
        f'<g class="v{i}"><text x="14" y="203" class="m" font-size="11" fill="#1A1A1A">▶ {e(st["title"])}</text>'
        f'<text x="14" y="224" class="s" font-size="12.5" fill="#1A1A1A">{e(st["detail"])}</text>'
        f'<text x="{W - 14}" y="25" text-anchor="end" class="m" font-size="11" fill="#1A1A1A">POWER-UP: {e(st["powerup"])}</text>'
        f'<text x="{W // 2}" y="25" text-anchor="middle" class="m" font-size="11" fill="#1A1A1A">COINS x{coins:02d} · WORLD 1-{i + 1}</text>'
        f'<text x="14" y="25" class="m" font-size="11" fill="#1A1A1A">SCORE {score:05d}</text></g>')

bricks = "".join(f'<line x1="{x}" y1="{GY}" x2="{x}" y2="{GY + 22}" stroke="#1A1A1A" stroke-width="2" opacity=".35"/>' for x in range(44, W, 40))
cloud = lambda x, y: (f'<g transform="translate({x},{y})"><rect width="42" height="10" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2"/>'
                      f'<rect x="10" y="-6" width="22" height="8" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2"/><rect x="12" y="-1" width="18" height="3" fill="#F2EDD7"/></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rayyan Ahmed - Mario runs through BMW, sol, rove, NEVERMISSAI, lineage-revocation, Job-Finder, predictive-maintenance, RESET, and the co-op flagpole">
<style>{"".join(css)}</style>
<rect x="6" y="6" width="{W - 8}" height="{H - 8}" fill="#1A1A1A"/>
<rect x="3" y="3" width="{W - 8}" height="{H - 8}" fill="#6ECFCF" stroke="#1A1A1A" stroke-width="3"/>
<rect x="3" y="3" width="{W - 8}" height="32" fill="#F5D87A" stroke="#1A1A1A" stroke-width="3"/>
<g class="cl">{cloud(520, 48)}{cloud(240, 44)}{cloud(640, 50)}</g>
<rect x="3" y="{GY}" width="{W - 8}" height="22" fill="#E8857A" stroke="#1A1A1A" stroke-width="3"/>{bricks}
{"".join(objs)}
<g class="run"><g class="hop"><g transform="translate(0,{GY})">{sprite}</g></g></g>
<rect x="3" y="180" width="{W - 8}" height="62" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="3"/>
{"".join(info)}
</svg>
'''
Path(__file__).with_name("game.svg").write_text(svg, encoding="utf-8")
