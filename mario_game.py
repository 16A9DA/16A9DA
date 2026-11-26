#!/usr/bin/env python3
"""Interactive Retro Mario GitHub Profile Game Engine for 16A9DA."""

from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"
SVG_PATH = ROOT / "game.svg"

STAGES = [
    {
        "label": "BMW",
        "kind": "start",
        "powerup": "LangChain",
        "title": "STAGE 0 :: BMW AGENTIC AI INTERN",
        "detail": "System Design · CS @ Univ. of Debrecen · Always learning",
    },
    {
        "label": "sol",
        "kind": "qblock",
        "powerup": "Ollama+RAG",
        "title": "UNLOCKED [sol] :: AGENTIC AI",
        "detail": "Offline terminal coding agent w/ multi-model council & RAG",
    },
    {
        "label": "rove",
        "kind": "qblock",
        "powerup": "MacAgent",
        "title": "UNLOCKED [rove] :: COMPUTER-USE AGENT",
        "detail": "macOS AI assistant w/ specialist agents, voice & approval gates",
    },
    {
        "label": "NEVERMISS",
        "kind": "qblock",
        "powerup": "1ST GOLD",
        "title": "UNLOCKED [NEVERMISSAI] :: KANZ AI GOLD MEDAL",
        "detail": "Autonomous voice agent (Twilio, Groq Llama 3.3, ChromaDB)",
    },
    {
        "label": "Lineage",
        "kind": "qblock",
        "powerup": "COSE+CBOR",
        "title": "UNLOCKED [lineage-revocation] :: RESEARCH",
        "detail": "Verifier-side delegation revocation via COSE_Sign1 & RFC 8949 CBOR",
    },
    {
        "label": "JobFind",
        "kind": "qblock",
        "powerup": "90% MLP",
        "title": "UNLOCKED [Job-Finder] :: MODEL TRAINING",
        "detail": "Tesseract OCR + Llama 3 parser + TF-IDF MLP (90% val accuracy)",
    },
    {
        "label": "SensML",
        "kind": "qblock",
        "powerup": "F1=0.68",
        "title": "UNLOCKED [predictive-maintenance] :: MODEL TRAINING",
        "detail": "10k sensor anomaly pipeline (3.4% fail); GBDT F1 0.68 minority",
    },
    {
        "label": "RESET",
        "kind": "pipe",
        "powerup": "SwiftUI",
        "title": "WARP PIPE [RESET] :: LOCAL-FIRST AI HEALTH APP",
        "detail": "Native iOS (SwiftUI + SwiftData) auto-tracking & AI guidance",
    },
    {
        "label": "CO-OP",
        "kind": "flag",
        "powerup": "1-UP!",
        "title": "COURSE CLEAR! :: CONNECT FOR CO-OP",
        "detail": "LinkedIn: /in/16a9da | Email: rayyan.tanweer@gmail.com",
    },
]

# 12x14 Pixel Mario Sprite (@Documents/me palette)
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


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {
        "x": 4,
        "y": 1,
        "facing": "right",
        "coins": 1,
        "score": 200,
        "unlocked": [4],
        "last_player": "16A9DA",
        "moves": 1,
    }


def apply_move(state: dict, command: str, player: str) -> dict:
    clean_player = re.sub(r"[^A-Za-z0-9_-]", "", player)[:20] or "guest"
    x = min(max(int(state.get("x", 0)), 0), len(STAGES) - 1)
    coins = int(state.get("coins", 0))
    score = int(state.get("score", 0))
    unlocked = list(state.get("unlocked", []))
    facing = state.get("facing", "right")
    y = 0

    if command == "left":
        x = max(0, x - 1)
        facing = "left"
    elif command == "right":
        x = min(len(STAGES) - 1, x + 1)
        facing = "right"
    elif command == "jump":
        y = 1
        if x not in unlocked:
            unlocked.append(x)
            coins += 1
            score += 200
        else:
            score += 50
    elif command == "reset":
        return {
            "x": 0,
            "y": 0,
            "facing": "right",
            "coins": 0,
            "score": 0,
            "unlocked": [],
            "last_player": clean_player,
            "moves": 0,
        }

    return {
        "x": x,
        "y": y,
        "facing": facing,
        "coins": coins,
        "score": score,
        "unlocked": sorted(set(unlocked)),
        "last_player": clean_player,
        "moves": int(state.get("moves", 0)) + 1,
    }


def render_mario(cx: int, ground_y: int, jumping: bool, facing: str) -> str:
    px = 3
    w = 12 * px
    h = 14 * px
    top_y = ground_y - h - (20 if jumping else 0)
    left_x = cx - w // 2
    rects = []
    for row_idx, row in enumerate(MARIO_SPRITE):
        line = row[::-1] if facing == "left" else row
        for col_idx, ch in enumerate(line):
            color = PALETTE.get(ch)
            if color:
                rects.append(
                    f'<rect x="{left_x + col_idx * px}" y="{top_y + row_idx * px}" '
                    f'width="{px}" height="{px}" fill="{color}" />'
                )
    return "\n    ".join(rects)


def render_svg(state: dict) -> str:
    x = min(max(int(state.get("x", 0)), 0), len(STAGES) - 1)
    jumping = bool(state.get("y", 0))
    facing = state.get("facing", "right")
    coins = int(state.get("coins", 0))
    score = int(state.get("score", 0))
    unlocked = set(state.get("unlocked", []))
    last_player = html.escape(str(state.get("last_player", "16A9DA")))
    stage = STAGES[x]

    ground_y = 180
    col_centers = [60 + i * 85 for i in range(len(STAGES))]

    stage_elements = []
    for idx, st in enumerate(STAGES):
        cx = col_centers[idx]
        is_here = idx == x
        is_hit = idx in unlocked
        kind = st["kind"]
        lbl = html.escape(st["label"])

        if kind == "qblock":
            fill = "#E8857A" if is_hit else "#F5D87A"
            symbol = "!" if is_hit else "?"
            bx = cx - 16
            by = 84
            stage_elements.append(
                f'<rect x="{bx + 3}" y="{by + 3}" width="32" height="32" fill="#1A1A1A" />'
                f'<rect x="{bx}" y="{by}" width="32" height="32" fill="{fill}" stroke="#1A1A1A" stroke-width="2.5" />'
                f'<text x="{cx}" y="{by + 22}" text-anchor="middle" class="mono" font-size="16" fill="#1A1A1A">{symbol}</text>'
                f'<text x="{cx}" y="76" text-anchor="middle" class="mono" font-size="9" fill="#1A1A1A">{lbl}</text>'
            )
            if is_here and jumping:
                pu = html.escape(st["powerup"])
                stage_elements.append(
                    f'<rect x="{cx - 34}" y="44" width="68" height="20" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2" />'
                    f'<text x="{cx}" y="57" text-anchor="middle" class="mono" font-size="9" fill="#1A1A1A">{pu}</text>'
                )
        elif kind == "pipe":
            stage_elements.append(
                f'<rect x="{cx - 22}" y="140" width="44" height="12" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5" />'
                f'<rect x="{cx - 17}" y="152" width="34" height="28" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2.5" />'
                f'<text x="{cx}" y="132" text-anchor="middle" class="mono" font-size="9" fill="#1A1A1A">{lbl}</text>'
            )
        elif kind == "flag":
            stage_elements.append(
                f'<line x1="{cx}" y1="88" x2="{cx}" y2="{ground_y}" stroke="#1A1A1A" stroke-width="3" />'
                f'<circle cx="{cx}" cy="86" r="5" fill="#F5D87A" stroke="#1A1A1A" stroke-width="2" />'
                f'<polygon points="{cx},91 {cx - 30},103 {cx},115" fill="#E8857A" stroke="#1A1A1A" stroke-width="2" />'
                f'<text x="{cx - 16}" y="76" text-anchor="middle" class="mono" font-size="9" fill="#1A1A1A">{lbl}</text>'
            )
        else:
            stage_elements.append(
                f'<rect x="{cx - 22}" y="88" width="44" height="24" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2.5" />'
                f'<text x="{cx}" y="104" text-anchor="middle" class="mono" font-size="10" fill="#1A1A1A">{lbl}</text>'
                f'<line x1="{cx}" y1="112" x2="{cx}" y2="122" stroke="#1A1A1A" stroke-width="2" />'
            )

        marker_fill = "#F5D87A" if is_here else "#F2EDD7"
        stage_elements.append(
            f'<circle cx="{cx}" cy="{ground_y + 13}" r="5" fill="{marker_fill}" stroke="#1A1A1A" stroke-width="2" />'
        )

    mario_svg = render_mario(col_centers[x], ground_y, jumping, facing)
    title_txt = html.escape(stage["title"])
    detail_txt = html.escape(stage["detail"])

    brick_lines = []
    for bx in range(48, 780, 48):
        brick_lines.append(
            f'<line x1="{bx}" y1="{ground_y}" x2="{bx}" y2="{ground_y + 26}" stroke="#1A1A1A" stroke-width="2" opacity="0.35" />'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 278" width="800" height="278" role="img" aria-label="Interactive Retro Mario Profile Game">
  <defs>
    <style>
      .mono {{ font-family: ui-monospace, 'SFMono-Regular', Menlo, Monaco, Consolas, monospace; font-weight: 800; }}
      .sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    </style>
  </defs>

  <!-- Outer Shadow & Sky Frame -->
  <rect x="8" y="8" width="784" height="202" fill="#1A1A1A" />
  <rect x="4" y="4" width="784" height="202" fill="#6ECFCF" stroke="#1A1A1A" stroke-width="3" />

  <!-- HUD Strip -->
  <rect x="4" y="4" width="784" height="34" fill="#F5D87A" stroke="#1A1A1A" stroke-width="3" />
  <text x="18" y="25" class="mono" font-size="11.5" fill="#1A1A1A">✳ 16A9DA · SCORE {score:05d}</text>
  <text x="396" y="25" text-anchor="middle" class="mono" font-size="11.5" fill="#1A1A1A">COINS x{coins:02d} · WORLD 1-{x + 1}</text>
  <text x="774" y="25" text-anchor="end" class="mono" font-size="11" fill="#1A1A1A">PLAYER: @{last_player}</text>

  <!-- Clouds -->
  <rect x="136" y="50" width="42" height="10" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2" />
  <rect x="146" y="44" width="22" height="8" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2" />
  <rect x="148" y="49" width="18" height="3" fill="#F2EDD7" />

  <rect x="556" y="52" width="46" height="10" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2" />
  <rect x="568" y="46" width="22" height="8" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="2" />
  <rect x="570" y="51" width="18" height="3" fill="#F2EDD7" />

  <!-- Ground -->
  <rect x="4" y="{ground_y}" width="784" height="26" fill="#E8857A" stroke="#1A1A1A" stroke-width="3" />
  {"".join(brick_lines)}

  <!-- Stage Objects -->
  {"".join(stage_elements)}

  <!-- Pixel Mario -->
  <g>
    {mario_svg}
  </g>

  <!-- Dialogue / Status Box -->
  <rect x="8" y="220" width="784" height="52" fill="#1A1A1A" />
  <rect x="4" y="216" width="784" height="52" fill="#F2EDD7" stroke="#1A1A1A" stroke-width="3" />
  <text x="18" y="237" class="mono" font-size="11.5" fill="#1A1A1A">▶ {title_txt}</text>
  <text x="18" y="256" class="sans" font-size="12.5" font-weight="600" fill="#1A1A1A">{detail_txt}</text>
</svg>
"""


def main() -> int:
    command = os.environ.get("MARIO_CMD", "").strip().lower()
    if not command and len(sys.argv) > 1:
        command = sys.argv[1].strip().lower()
    player = os.environ.get("MARIO_PLAYER", "16A9DA").strip()

    state = load_state()
    if command in {"left", "right", "jump", "reset"}:
        state = apply_move(state, command, player)

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    SVG_PATH.write_text(render_svg(state), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
