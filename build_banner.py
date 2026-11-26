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
    w, h = (178, 52) if icon else (len(text) * 8 + 26, 30)
    body = (f'<g transform="translate(20,{(h - 24) / 2})">{ICONS[name]}</g><text x="{w / 2 + 18}" y="{h / 2 + 6}" text-anchor="middle" fill="#1A1A1A" style="font:800 18px ui-monospace,Menlo,Consolas,monospace">{e(text)}</text>' if icon else
            f'<text x="{w / 2}" y="{h / 2 + 4}" text-anchor="middle" fill="#1A1A1A" style="font:800 12px ui-monospace,Menlo,Consolas,monospace">{e(text)}</text>')
    (out / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 5}" height="{h + 5}" viewBox="0 0 {w + 5} {h + 5}" role="img" aria-label="{e(text)}">'
        f'<rect x="5" y="5" width="{w}" height="{h}" fill="#1A1A1A"/>'
        f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" fill="{fill}" stroke="#1A1A1A" stroke-width="3"/>{body}</svg>\n', encoding="utf-8")
    links[name] = f'<a href="{url}"><img src="./btn/{name}.svg" alt="{e(text)}" height="{h + 5}" /></a>'
Path(__file__).with_name("README.md").write_text(
    '<div align="center">\n\n'
    f'<a href="{GH}?tab=repositories"><img src="./mario-run.svg" alt="Rayyan Ahmed: Mario runs from CS at University of Debrecen through Job-Finder, sol, InnerScript, NEVERMISSAI (Kanz AI gold), lineage-revocation, rove, BMW (Agentic AI Intern, Oct 2026) and RESET to the co-op flag" width="800" /></a>\n\n'
    + links["play"] + "\n\n" + "&nbsp;\n".join(v for n, v in links.items() if n != "play") + "\n\n</div>\n", encoding="utf-8")

# ---- playable version (GitHub Pages): arrows / WASD / touch ----
import json
URLS = {"JobFind": GH + "/Job-Finder", "sol": GH + "/sol", "NEVERMISS": GH + "/NEVERMISSAI", "Lineage": GH + "/lineage-revocation",
        "rove": GH + "/rove", "RESET": GH + "/RESET", "InnerScript": "https://innerscript.ca/", "BMW": "https://linkedin.com/in/16a9da",
        "CO-OP": "https://linkedin.com/in/16a9da"}
data = [dict(label=a, kind=b, date=c, title=d, detail=f, cm=g, rp=h, url=URLS.get(a, "")) for a, b, c, d, f, g, h in S] if False else \
       [dict(label=r[0], kind=r[1], date=r[2], title=r[3], detail=r[4], cm=r[5], rp=r[6], url=URLS.get(r[0], "")) for r in S]
GAME = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>Rayyan Ahmed · Play my résumé</title>
<style>
:root{--ink:#1A1A1A;--cream:#F2EDD7;--yel:#F5D87A;--pink:#E8857A;--sky:#6ECFCF}
*{box-sizing:border-box}html,body{margin:0;background:var(--ink);color:var(--cream);font-family:ui-monospace,Menlo,Consolas,monospace}
body{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:12px;touch-action:manipulation}
h1{margin:0;font-size:clamp(20px,3.2vw,34px);letter-spacing:.12em;color:var(--yel);text-shadow:3px 3px 0 var(--pink)}#sub{margin:0;font-size:clamp(11px,1.4vw,15px);opacity:.85;text-align:center}
#wrap{width:640px}canvas{display:block;width:100%;height:auto;border:4px solid var(--cream);box-shadow:8px 8px 0 #000;background:var(--sky)}
.row{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
a.b,button{font:800 14px ui-monospace,Menlo,Consolas,monospace;color:var(--ink);background:var(--yel);border:3px solid var(--ink);box-shadow:4px 4px 0 var(--cream);padding:12px 22px;text-decoration:none;cursor:pointer;user-select:none;-webkit-user-select:none}
a.b:active,button:active{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--cream)}
a.p{background:var(--pink)}a.c{background:var(--cream)}a.s{background:var(--sky)}
#pad{display:none;gap:14px}@media (pointer:coarse){#pad{display:flex}}#pad button{font-size:22px;padding:14px 26px}
#hint{font-size:12px;opacity:.75;text-align:center}#open{display:none}
</style></head><body>
<h1>RAYYAN AHMED</h1><p id="sub">Agentic AI Intern @ BMW · CS @ University of Debrecen</p>
<div id="wrap"><canvas id="c" width="640" height="250"></canvas></div>
<div id="hint">← → move · ↑ / SPACE jump · land on or bump the ★ and ? blocks, hop from block to block · reach the flag</div>
<div class="row" id="pad"><button id="L">◀</button><button id="J">▲</button><button id="R">▶</button></div>
<div class="row"><a class="b" id="open" target="_blank" rel="noopener">OPEN ↗</a>
<a class="b" href="https://linkedin.com/in/16a9da" target="_blank" rel="noopener">LinkedIn</a>
<a class="b p" href="mailto:rayyan.tanweer@gmail.com">Email</a>
<a class="b c" href="https://discordapp.com/users/584487184141254731" target="_blank" rel="noopener">Discord</a>
<a class="b s" href="https://github.com/16A9DA?tab=repositories" target="_blank" rel="noopener">GitHub</a></div>
<script>
const S=__DATA__;
const cv=document.getElementById('c'),g=cv.getContext('2d');g.imageSmoothingEnabled=false;
const W=640,GY=150,SP=96,COL=S.map((_,i)=>44+i*SP),WORLD=COL[COL.length-1]+120,N=S.length;
const INK='#1A1A1A',CREAM='#F2EDD7',YEL='#F5D87A',PINK='#E8857A',SKY='#6ECFCF';
const SPR=%SPRITE%,PAL=%PALETTE%;
const sp=document.createElement('canvas');sp.width=36;sp.height=42;{const q=sp.getContext('2d');SPR.forEach((r,y)=>[...r].forEach((ch,x)=>{if(PAL[ch]){q.fillStyle=PAL[ch];q.fillRect(x*3,y*3,3,3)}}))}
const BLK=[];{let k=0;S.forEach((s,i)=>{if(s.kind==='repo'||s.kind==='mile'){BLK.push({i,cx:COL[i],w:s.kind==='mile'?40:30,top:k%2?62:78});k++}})}
const BH=28,PW=9,PH=42;
const keys={};let st,K=1;
function fit(){const hh=document.querySelector('h1').offsetHeight+document.getElementById('sub').offsetHeight+document.getElementById('hint').offsetHeight+(innerWidth<700?150:90)+60;
 const w=Math.max(320,Math.min(innerWidth-28,1040,(innerHeight-hh)*W/250));document.getElementById('wrap').style.width=w+'px';
 const d=Math.min(devicePixelRatio||1,3);K=w*d/W;cv.width=Math.round(W*K);cv.height=Math.round(250*K);g.setTransform(K,0,0,K,0,0);g.imageSmoothingEnabled=false}
addEventListener('resize',fit);
function reset(){st={x:COL[0],y:GY,vy:0,gr:true,face:1,hit:new Set([0]),cur:0,coins:[],bump:{},t:0,won:false}}
reset();
addEventListener('keydown',e=>{const k=e.key;if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(k))e.preventDefault();keys[k.toLowerCase()]=1;if(st.won&&(k==='Enter'||k===' '))reset()});
addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=0});
for(const [id,k] of [['L','arrowleft'],['R','arrowright'],['J','arrowup']]){const b=document.getElementById(id);
 const on=e=>{e.preventDefault();keys[k]=1},off=e=>{e.preventDefault();keys[k]=0};
 b.addEventListener('pointerdown',on);b.addEventListener('pointerup',off);b.addEventListener('pointerleave',off);b.addEventListener('pointercancel',off)}
cv.addEventListener('pointerdown',()=>{if(st.won)reset()});
const open=document.getElementById('open');
function setCur(i){if(st.cur===i&&open.href)return;st.cur=i;const u=S[i].url;if(u){open.style.display='';open.href=u;open.textContent=(S[i].kind==='repo'||S[i].kind==='pipe'?'OPEN '+S[i].title.toUpperCase():'VISIT')+' ↗'}else open.style.display='none'}
setCur(0);fit();
function trigger(i){if(!st.hit.has(i)){st.hit.add(i);if(S[i].kind==='repo'||S[i].kind==='mile')st.coins.push({x:COL[i],y:(BLK.find(b=>b.i===i)||{top:70}).top-8,t:0})}setCur(i)}
let last=performance.now();
function step(dt){
 const L=keys.arrowleft||keys.a,R=keys.arrowright||keys.d,J=keys.arrowup||keys.w||keys[' '];
 const v=(R?1:0)-(L?1:0),px0=st.x;st.x=Math.min(Math.max(st.x+v*175*dt,20),WORLD-40);if(v)st.face=v;
 // sideways: blocks are solid
 for(const b of BLK){const bot=b.top+BH;if(st.y>b.top+1&&st.y-PH<bot-1&&Math.abs(st.x-b.cx)<b.w/2+PW)st.x=b.cx+(px0<b.cx?-1:1)*(b.w/2+PW)}
 if(J&&st.gr&&!st.won){st.vy=-500}
 const py=st.y;st.vy+=1250*dt;st.y+=st.vy*dt;st.gr=false;
 for(const b of BLK){const bot=b.top+BH;if(Math.abs(st.x-b.cx)>=b.w/2+PW-1)continue;
  if(st.vy>=0&&py<=b.top+.5&&st.y>=b.top){st.y=b.top;st.vy=0;st.gr=true;trigger(b.i)}
  else if(st.vy<0&&py-PH>=bot-.5&&st.y-PH<bot){st.y=bot+PH;st.vy=40;st.bump[b.i]=.25;trigger(b.i)}}
 if(st.y>=GY){st.y=GY;st.vy=0;st.gr=true}
 S.forEach((s,i)=>{if(!(s.kind==='repo'||s.kind==='mile')&&Math.abs(st.x-COL[i])<26)trigger(i)});
 if(S[st.cur].kind==='flag'&&Math.abs(st.x-COL[N-1])<26)st.won=true;
 for(const k in st.bump){st.bump[k]-=dt;if(st.bump[k]<=0)delete st.bump[k]}
 st.coins.forEach(c=>c.t+=dt);st.coins=st.coins.filter(c=>c.t<.7);st.t+=dt}
function box(x,y,w,h,f){g.fillStyle=INK;g.fillRect(x+3,y+3,w,h);g.fillStyle=f;g.fillRect(x,y,w,h);g.strokeStyle=INK;g.lineWidth=2.5;g.strokeRect(x,y,w,h)}
function txt(s,x,y,sz,al,mono=true,c=INK){g.fillStyle=c;g.textAlign=al;g.font=(mono?'800 ':'600 ')+sz+'px '+(mono?'ui-monospace,Menlo,Consolas,monospace':'-apple-system,Segoe UI,Helvetica,Arial,sans-serif');g.fillText(s,x,y)}
function draw(){
 g.setTransform(K,0,0,K,0,0);g.fillStyle=SKY;g.fillRect(0,0,W,250);
 const cam=Math.min(Math.max(st.x-190,0),WORLD-W);
 g.save();g.beginPath();g.rect(0,0,W,GY+22);g.clip();g.translate(-cam,0);
 for(let x=120;x<WORLD+400;x+=310){g.fillStyle=CREAM;g.strokeStyle=INK;g.lineWidth=2;g.fillRect(x,48,42,10);g.strokeRect(x,48,42,10);g.fillRect(x+10,42,22,8);g.strokeRect(x+10,42,22,8)}
 g.fillStyle=PINK;g.fillRect(cam-8,GY,W+16,22);g.strokeStyle=INK;g.lineWidth=3;g.strokeRect(cam-8,GY,W+16,22);
 g.lineWidth=2;g.globalAlpha=.35;for(let x=Math.floor(cam/40)*40;x<cam+W+40;x+=40){g.beginPath();g.moveTo(x+4,GY);g.lineTo(x+4,GY+22);g.stroke()}g.globalAlpha=1;
 S.forEach((s,i)=>{const cx=COL[i],hit=st.hit.has(i);
  if(s.kind==='repo'||s.kind==='mile'){const B=BLK.find(b=>b.i===i),w=B.w,by=B.top-(st.bump[i]?Math.sin(st.bump[i]/.25*Math.PI)*6:0);
   box(cx-w/2,by,w,28,hit?PINK:YEL);txt(s.kind==='mile'?'★':(hit?'!':'?'),cx,by+21,15,'center');txt(s.label,cx,B.top-6,8.5,'center')}
  else if(s.kind==='start'){box(cx-22,84,44,22,CREAM);txt(s.label,cx,99,10,'center')}
  else if(s.kind==='pipe'){box(cx-20,118,40,11,YEL);box(cx-15,129,30,GY-129,YEL);txt(s.label,cx,111,8.5,'center')}
  else{g.strokeStyle=INK;g.lineWidth=3;g.beginPath();g.moveTo(cx,66);g.lineTo(cx,GY);g.stroke();g.fillStyle=YEL;g.beginPath();g.arc(cx,64,5,0,7);g.fill();g.stroke();
   const wv=1-.3*Math.abs(Math.sin(st.t*4));g.fillStyle=PINK;g.beginPath();g.moveTo(cx,70);g.lineTo(cx-28*wv,81);g.lineTo(cx,92);g.closePath();g.fill();g.lineWidth=2;g.stroke();txt(s.label,cx,56,8.5,'center')}
  g.fillStyle=hit?YEL:CREAM;g.strokeStyle=INK;g.lineWidth=2;g.beginPath();g.arc(cx,GY+11,4,0,7);g.fill();g.stroke()});
 st.coins.forEach(c=>{g.fillStyle=YEL;g.strokeStyle=INK;g.lineWidth=2;g.beginPath();g.arc(c.x,c.y-c.t*60,6,0,7);g.fill();g.stroke()});
g.restore();
 // HUD
 let cm=0,rp=0;st.hit.forEach(i=>{cm+=S[i].cm;rp+=S[i].rp});
 g.fillStyle=YEL;g.fillRect(0,0,W,34);g.strokeStyle=INK;g.lineWidth=3;g.strokeRect(1.5,1.5,W-3,31);
 txt('STAGE '+String(st.cur).padStart(2,'0')+'/'+(N-1),14,22,11,'left');txt('REPOS x'+String(rp).padStart(2,'0'),W/2,22,11,'center');txt('COMMITS '+String(cm).padStart(4,'0'),W-14,22,11,'right');
 g.save();g.translate(-cam,0);g.translate(st.x,st.y);g.scale(st.face,1);g.drawImage(sp,-18,-42);g.restore();
 // panel
 g.fillStyle=CREAM;g.fillRect(0,180,W,70);g.strokeStyle=INK;g.lineWidth=3;g.strokeRect(1.5,181.5,W-3,67);
 const s=S[st.cur];txt('▶ '+(s.date?s.date+' :: ':'')+s.title,14,206,11,'left');txt(s.detail,14,228,12.5,'left',false);
 if(!st.hit.has(1)&&st.cur===0)txt('Run →  jump onto the blocks',W-14,243,10,'right');
 if(st.won){g.fillStyle='rgba(26,26,26,.7)';g.fillRect(0,34,W,146);txt('COURSE CLEAR!',W/2,100,26,'center',true,YEL);txt('Press ENTER / tap to play again',W/2,130,12,'center',true,CREAM)}
}
function loop(n){const dt=Math.min((n-last)/1000,.05);last=n;step(dt);draw();requestAnimationFrame(loop)}
requestAnimationFrame(loop);
</script></body></html>
"""
sprite_js = json.dumps(MARIO_SPRITE)
Path(__file__).with_name("index.html").write_text(
    GAME.replace("__DATA__", json.dumps(data)).replace("%SPRITE%", sprite_js).replace("%PALETTE%", json.dumps(PALETTE)), encoding="utf-8")
