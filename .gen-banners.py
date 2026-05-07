#!/usr/bin/env python3
"""
Generate the 7 alpha banners + 1 suite overview at 1200x630.

Each banner reproduces the live <AlphaCardVisual> animation for that
theme exactly (privacy / time / insight / mirror / xray / cascade /
iceberg) so the press kit ships the same animated thumbnails the
designer sees on /alpha. Pure SVG + CSS keyframes — no JS.

Tool list mirrors src/app/alpha/page.tsx FEATURES exactly:
  Private Mirror     · privacy · v1
  Time Machine       · time    · v0.5
  Insight Engine     · insight · v0.5
  Smart Money Mirror · mirror  · v0.5
  Validator X-Ray    · xray    · v0.5
  Liquidation F.     · cascade · v0.5
  Iceberg Hunter     · iceberg · v0.5

Run from C:\\Users\\admin\\Desktop\\asterscan-ui-kit:
  python .gen-banners.py
"""

from pathlib import Path

OUT = Path(__file__).parent / "alpha"
OUT.mkdir(parents=True, exist_ok=True)

# ── Shared stylesheet + keyframes ─────────────────────────────
COMMON_CSS = r"""
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #2a2a2c; padding: 24px;
  font-family: 'DM Sans', system-ui, sans-serif;
}
.banner {
  width: 1200px; height: 630px;
  background:
    radial-gradient(ellipse at top right, rgba(244, 213, 177, 0.10), transparent 55%),
    linear-gradient(180deg, #0E0E0F 0%, #161618 100%);
  color: #F2F0EE;
  padding: 60px 70px;
  display: grid; grid-template-rows: auto 1fr auto;
  gap: 32px;
  position: relative; overflow: hidden;
  border-radius: 18px;
}
.banner::after {
  content: ''; position: absolute; left: 0; bottom: 0;
  width: 100%; height: 4px;
  background: linear-gradient(90deg, transparent, #F4D5B1, #FFD29F, transparent);
}

/* Top row — brand + version */
.head { display: flex; align-items: center; justify-content: space-between; }
.brand { display: flex; align-items: center; gap: 14px; }
.brand .mark { width: 48px; height: 48px; border-radius: 12px;
  background: linear-gradient(135deg, #F4D5B1, #FFD29F);
  display: grid; place-items: center; color: #0E0E0F;
  font-weight: 800; font-size: 24px; }
.brand .wordmark { font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em;
  display: inline-flex; align-items: baseline; gap: 1px; font-size: 16px; }
.brand .wordmark .aster { font-weight: 700; color: #F4D5B1; }
.brand .wordmark .scan  { font-weight: 400; color: #B9B5B0; opacity: 0.7; }
.brand .meta { font-family: 'JetBrains Mono', monospace;
  font-size: 10px; color: #7A7770; letter-spacing: 0.18em;
  text-transform: uppercase; margin-top: 4px; }

.version-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px; border-radius: 6px;
  background: rgba(244, 213, 177, 0.15);
  color: #F4D5B1;
  font-family: 'JetBrains Mono', monospace; font-weight: 700;
  font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase;
  border: 1px solid rgba(244, 213, 177, 0.25);
}

/* Animated visual card — mimics .alpha-visual on the live site */
.visual-card {
  position: relative;
  width: 100%; height: 280px;
  border-radius: 12px;
  border: 1px solid rgba(250, 204, 21, 0.40);
  background: linear-gradient(135deg, rgba(250, 204, 21, 0.10) 0%, rgba(14, 14, 15, 0.60) 50%, rgba(250, 204, 21, 0.15) 100%);
  overflow: hidden;
  box-shadow: inset 0 1px 4px rgba(0,0,0,0.3);
}

/* Title row */
.title-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; }
.title-row .lhs { max-width: 720px; }
.title-row h1 {
  font-size: 56px; font-weight: 800; letter-spacing: -0.025em;
  line-height: 1.05;
}
.title-row h1 .accent { color: #F4D5B1; }
.title-row .tag {
  font-family: 'JetBrains Mono', monospace; font-style: italic;
  font-size: 18px; color: #B9B5B0; line-height: 1.5;
  margin-top: 16px;
}
.title-row .url {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; color: #7A7770;
  letter-spacing: 0.18em; text-transform: uppercase;
  text-align: right; flex-shrink: 0;
}

/* ── Animation keyframes ── */
@keyframes alpha-scroll-y { 0% { transform: translateY(-100%); } 100% { transform: translateY(0); } }
@keyframes alpha-sweep    { 0% { transform: translateX(-10%); } 100% { transform: translateX(110%); } }
@keyframes alpha-bob      { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
@keyframes alpha-pulse    { 0%,100% { opacity: 0.4; } 50% { opacity: 1; } }
@keyframes alpha-drop     { 0% { transform: scaleY(0.05); transform-origin: top; opacity: 0; } 10% { opacity: 1; } 100% { transform: scaleY(1); transform-origin: top; opacity: 1; } }
@keyframes alpha-fade-up  { 0% { opacity: 0; transform: translateY(4px); } 20% { opacity: 1; transform: translateY(0); } 80% { opacity: 1; } 100% { opacity: 0; transform: translateY(-4px); } }
@keyframes alpha-trail    { 0% { transform: translateX(0); } 100% { transform: translateX(82%); } }
"""

PAGE_HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AsterScan Alpha — {title}</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
<div class="banner">
  <div class="head">
    <div class="brand">
      <div class="mark">✱</div>
      <div>
        <div class="wordmark"><span class="aster">ASTER</span><span class="scan">SCAN</span></div>
        <div class="meta">Alpha · {theme_label}</div>
      </div>
    </div>
    <div class="version-pill">{version}</div>
  </div>

  <div class="visual-card">{visual}</div>

  <div class="title-row">
    <div class="lhs">
      <h1>{headline_html}</h1>
      <div class="tag">{tagline}</div>
    </div>
    <div class="url">aster-scan.com/alpha</div>
  </div>
</div>
</body>
</html>
"""

# ── Per-theme animated visual HTML (1:1 from AlphaCardVisual.tsx) ──

def visual_privacy() -> str:
    cols = ["1f", "9c", "0a", "e3", "5b", "47", "8d", "22", "c0"] * 2
    columns = ""
    for i in range(8):  # more columns for the bigger banner canvas
        spans = ""
        for j, c in enumerate(cols):
            opacity = 0.3 + ((i + j) % 5) * 0.14
            spans += f'<span style="opacity:{opacity:.2f}">{c}</span>'
        delay = i * 0.15
        dur = 2.5 + i * 0.4
        columns += (
            f'<div class="pcol" style="animation: alpha-scroll-y {dur:.1f}s linear infinite;'
            f' animation-delay: {delay:.2f}s">{spans}</div>'
        )
    return f"""
    <style>
      .pgrid {{ position: absolute; inset: 0; display: flex; justify-content: space-around;
        align-items: stretch; padding: 0 30px; font-family: 'JetBrains Mono', monospace;
        font-size: 24px; color: rgba(250, 204, 21, 0.55); user-select: none; }}
      .pcol {{ display: flex; flex-direction: column; align-items: center; line-height: 1.15; }}
      .pcol span {{ display: block; }}
      .pfade {{ position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(to bottom, transparent, transparent, rgba(14, 14, 15, 0.85)); }}
    </style>
    <div class="pgrid">{columns}</div>
    <div class="pfade"></div>
    """


def visual_time() -> str:
    ticks = ""
    for i in range(21):
        x = 10 + i * 9
        is_major = (i % 5) == 0
        y1 = 30 if is_major else 38
        y2 = 50 if is_major else 45
        sw = 1 if is_major else 0.5
        ticks += (f'<line x1="{x}" x2="{x}" y1="{y1}" y2="{y2}" '
                  f'stroke="rgb(250 204 21 / 0.4)" stroke-width="{sw}"/>')
    return f"""
    <svg viewBox="0 0 200 80" preserveAspectRatio="none"
         style="position:absolute;inset:0;width:100%;height:100%">
      {ticks}
      <line x1="5" x2="195" y1="42" y2="42" stroke="rgb(250 204 21 / 0.3)" stroke-width="0.6"/>
      <text x="12" y="22" fill="rgb(250 204 21 / 0.55)" font-size="7" font-family="monospace">99,829k</text>
      <text x="150" y="22" fill="rgb(250 204 21 / 0.55)" font-size="7" font-family="monospace">99,830k</text>
      <g style="animation: alpha-sweep 4s ease-in-out infinite alternate; transform-origin: 0 0">
        <line x1="5" x2="5" y1="28" y2="56" stroke="rgb(250 204 21)" stroke-width="1.2"/>
        <circle cx="5" cy="42" r="2.5" fill="rgb(250 204 21)"/>
        <circle cx="5" cy="42" r="5" fill="rgb(250 204 21 / 0.25)"/>
      </g>
    </svg>
    """


def visual_insight() -> str:
    lines = [
        "→ 0xa1b2 placed BUY $312k BTCUSDT",
        "▲ Validator-2 oracle delta +18 bps",
        "◆ Privacy share rose to 47% (24h)",
        "→ Whale cluster #7 reactivated",
    ]
    items = ""
    for i, line in enumerate(lines):
        items += (f'<div class="iline" style="animation: alpha-fade-up {len(lines)*1.6}s '
                  f'ease-in-out infinite; animation-delay: {i*1.6}s">{line}</div>')
    return f"""
    <style>
      .ilines {{ position: absolute; inset: 0; display: flex; flex-direction: column;
        justify-content: center; padding: 0 36px; font-family: 'JetBrains Mono', monospace;
        font-size: 22px; color: rgba(250, 204, 21, 0.75); line-height: 1.7;
        font-weight: 500; }}
      .iline {{ opacity: 0; }}
    </style>
    <div class="ilines">{items}</div>
    """


def visual_mirror() -> str:
    return """
    <svg viewBox="0 0 200 80" preserveAspectRatio="none"
         style="position:absolute;inset:0;width:100%;height:100%">
      <line x1="20" x2="180" y1="55" y2="55" stroke="rgb(250 204 21 / 0.2)"
            stroke-width="0.5" stroke-dasharray="2 3"/>
      <line x1="20" x2="180" y1="28" y2="28" stroke="rgb(250 204 21 / 0.2)"
            stroke-width="0.5" stroke-dasharray="2 3"/>
      <text x="5" y="32" fill="rgb(250 204 21 / 0.55)" font-size="7" font-family="monospace">smart</text>
      <text x="5" y="59" fill="rgb(250 204 21 / 0.5)"  font-size="7" font-family="monospace">copy</text>
      <g style="animation: alpha-trail 3.5s ease-in-out infinite alternate">
        <circle cx="20" cy="28" r="3" fill="rgb(34 197 94)"/>
        <circle cx="20" cy="28" r="7" fill="rgb(34 197 94 / 0.25)"/>
      </g>
      <g style="animation: alpha-trail 3.5s ease-in-out infinite alternate; animation-delay: 0.6s">
        <circle cx="20" cy="55" r="2.5" fill="rgb(250 204 21)"/>
        <circle cx="20" cy="55" r="5" fill="rgb(250 204 21 / 0.2)"/>
      </g>
    </svg>
    """


def visual_xray() -> str:
    positions = [25, 55, 85, 115, 145, 175]
    dots = ""
    for i, x in enumerate(positions):
        h = 20 - (i * 3) % 7
        y = 20 + (i * 3) % 7
        dots += (
            f'<g style="animation: alpha-pulse 2.4s ease-in-out infinite; animation-delay: {i*0.4}s">'
            f'  <circle cx="{x}" cy="45" r="3" fill="rgb(250 204 21 / 0.7)"/>'
            f'  <circle cx="{x}" cy="45" r="6" fill="rgb(250 204 21 / 0.15)"/>'
            f'  <rect x="{x-1.5}" y="{y}" width="3" height="{h}" fill="rgb(250 204 21 / 0.4)"/>'
            f'</g>'
        )
    return f"""
    <svg viewBox="0 0 200 80" preserveAspectRatio="none"
         style="position:absolute;inset:0;width:100%;height:100%">
      <line x1="10" x2="190" y1="45" y2="45" stroke="rgb(250 204 21 / 0.15)" stroke-width="0.4"/>
      {dots}
      <line x1="0" x2="0" y1="5" y2="75" stroke="rgb(250 204 21 / 0.5)" stroke-width="1"
            style="animation: alpha-sweep 3s ease-in-out infinite alternate; transform-origin: 0 0"/>
    </svg>
    """


def visual_cascade() -> str:
    bars = [60, 75, 50, 85, 65, 90, 55, 70, 80, 62, 78, 58]
    bdivs = ""
    for i, h in enumerate(bars):
        bdivs += (f'<div class="bar" style="height:{h}%;animation: alpha-drop 2.6s ease-out infinite;'
                  f' animation-delay: {i*0.18}s"></div>')
    return f"""
    <style>
      .cwrap {{ position: absolute; inset: 0; display: flex; align-items: flex-end;
        justify-content: space-around; padding: 0 24px 12px; }}
      .cwrap .bar {{ width: 18px; border-radius: 3px 3px 0 0;
        background: linear-gradient(to top, rgba(239, 68, 68, 0.7) 0%,
          rgba(239, 68, 68, 0.5) 50%, rgba(250, 204, 21, 0.4) 100%); }}
    </style>
    <div class="cwrap">{bdivs}</div>
    """


def visual_iceberg() -> str:
    return """
    <svg viewBox="0 0 200 80" preserveAspectRatio="none"
         style="position:absolute;inset:0;width:100%;height:100%">
      <line x1="0" x2="200" y1="35" y2="35" stroke="rgb(56 189 248 / 0.5)"
            stroke-width="0.8" stroke-dasharray="3 2"/>
      <text x="5" y="32" fill="rgb(56 189 248 / 0.7)" font-size="6" font-family="monospace">visible</text>
      <text x="5" y="48" fill="rgb(250 204 21 / 0.6)" font-size="6" font-family="monospace">hidden</text>
      <g style="animation: alpha-bob 4s ease-in-out infinite">
        <polygon points="100,15 90,35 110,35" fill="rgb(250 204 21 / 0.85)"
                 stroke="rgb(250 204 21)" stroke-width="0.5"/>
        <polygon points="80,35 100,75 120,35 115,55 85,55" fill="rgb(250 204 21 / 0.25)"
                 stroke="rgb(250 204 21 / 0.4)" stroke-width="0.5"/>
      </g>
    </svg>
    """


VISUALS = {
    "privacy": visual_privacy,
    "time":    visual_time,
    "insight": visual_insight,
    "mirror":  visual_mirror,
    "xray":    visual_xray,
    "cascade": visual_cascade,
    "iceberg": visual_iceberg,
}

# ── 7 tools mirroring src/app/alpha/page.tsx FEATURES ──
FEATURES = [
    {
        "slug": "alpha-private-mirror",
        "title": "Private Mirror",
        "headline_html": 'Private <span class="accent">Mirror</span>',
        "theme": "privacy",
        "tagline": "Inferring signal from encrypted on-chain traffic.",
        "version": "v 1.0",
    },
    {
        "slug": "alpha-time-machine",
        "title": "Time Machine",
        "headline_html": 'Time <span class="accent">Machine</span>',
        "theme": "time",
        "tagline": "Rewind any moment of Aster Chain.",
        "version": "v 0.5",
    },
    {
        "slug": "alpha-insight-engine",
        "title": "Insight Engine",
        "headline_html": 'Insight <span class="accent">Engine</span>',
        "theme": "insight",
        "tagline": "Aster Chain narrated in plain English.",
        "version": "v 0.5",
    },
    {
        "slug": "alpha-smart-money-mirror",
        "title": "Smart Money Mirror",
        "headline_html": 'Smart Money <span class="accent">Mirror</span>',
        "theme": "mirror",
        "tagline": "Wallets that move BEFORE the move.",
        "version": "v 0.5",
    },
    {
        "slug": "alpha-validator-xray",
        "title": "Validator X-Ray",
        "headline_html": 'Validator <span class="accent">X-Ray</span>',
        "theme": "xray",
        "tagline": "Per-validator forensics ahead of external set opening.",
        "version": "v 0.5",
    },
    {
        "slug": "alpha-liquidation-forecaster",
        "title": "Liquidation Forecaster",
        "headline_html": 'Liquidation <span class="accent">Forecaster</span>',
        "theme": "cascade",
        "tagline": "Cascade simulation across leverage tiers.",
        "version": "v 0.5",
    },
    {
        "slug": "alpha-iceberg-hunter",
        "title": "Iceberg Hunter",
        "headline_html": 'Iceberg <span class="accent">Hunter</span>',
        "theme": "iceberg",
        "tagline": "Whales splitting orders to hide their hand.",
        "version": "v 0.5",
    },
]

THEME_LABELS = {
    "privacy": "ZK · Privacy mode",
    "time":    "Block-state replay",
    "insight": "Plain-language feed",
    "mirror":  "Lead-lag detection",
    "xray":    "Validator forensics",
    "cascade": "Liquidation cascade",
    "iceberg": "Hidden liquidity",
}


def write_page(slug: str, html: str) -> None:
    path = OUT / f"{slug}.html"
    path.write_text(html, encoding="utf-8")
    print(f"  wrote {path.relative_to(OUT.parent)}")


def gen_individual() -> None:
    for f in FEATURES:
        visual = VISUALS[f["theme"]]()
        html = PAGE_HEAD.format(
            title=f["title"],
            css=COMMON_CSS,
            theme_label=THEME_LABELS[f["theme"]],
            version=f["version"],
            visual=visual,
            headline_html=f["headline_html"],
            tagline=f["tagline"],
        )
        write_page(f["slug"], html)


def gen_overview() -> None:
    """Composite banner showing all 7 alpha tiles in a 4-3 grid."""
    tiles_html = ""
    for f in FEATURES:
        v = VISUALS[f["theme"]]()
        tiles_html += f"""
        <div class="tile">
          <div class="tile-visual">{v}</div>
          <div class="tile-meta">
            <div class="tile-title">{f["title"]}</div>
            <div class="tile-ver">{f["version"]}</div>
          </div>
        </div>
        """

    overview_css = COMMON_CSS + r"""
.banner {
  display: flex; flex-direction: column; gap: 28px;
  padding: 50px 60px;
}
.title-row h1 { font-size: 48px; }
.tiles {
  flex: 1;
  display: grid; grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 1fr;
  gap: 14px;
}
.tile {
  background: rgba(22, 22, 24, 0.7);
  border: 1px solid #26262A;
  border-radius: 10px;
  overflow: hidden;
  display: flex; flex-direction: column;
}
.tile-visual {
  position: relative; flex: 1; min-height: 90px;
  border-bottom: 1px solid rgba(250, 204, 21, 0.30);
  background: linear-gradient(135deg, rgba(250, 204, 21, 0.10) 0%, rgba(14, 14, 15, 0.60) 50%, rgba(250, 204, 21, 0.15) 100%);
}
.tile-meta { padding: 8px 12px; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.tile-title { font-size: 13px; font-weight: 600; color: #F2F0EE; }
.tile-ver { font-family: 'JetBrains Mono', monospace; font-size: 9px;
  color: #F4D5B1; background: rgba(244, 213, 177, 0.12);
  padding: 2px 6px; border-radius: 3px; letter-spacing: 0.1em; text-transform: uppercase; }
"""

    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AsterScan Alpha — Suite Overview</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>""" + overview_css + """</style>
</head>
<body>
<div class="banner">
  <div class="head">
    <div class="brand">
      <div class="mark">✱</div>
      <div>
        <div class="wordmark"><span class="aster">ASTER</span><span class="scan">SCAN</span></div>
        <div class="meta">Alpha suite · 7 experimental tools</div>
      </div>
    </div>
    <div class="version-pill">v 2026-05-07</div>
  </div>

  <div class="title-row">
    <div class="lhs">
      <h1>The <span class="accent">Alpha</span> suite.</h1>
      <div class="tag">Seven experimental tools — privacy mirror, replay, narration, copy-trading, validator forensics, cascade forecasting, hidden-liquidity detection.</div>
    </div>
    <div class="url">aster-scan.com/alpha</div>
  </div>

  <div class="tiles">""" + tiles_html + """</div>
</div>
</body>
</html>
"""
    write_page("alpha-suite-overview", html)


if __name__ == "__main__":
    print("Generating alpha banners → /alpha/")
    gen_individual()
    gen_overview()
    print(f"\nDone. {len(FEATURES) + 1} files in {OUT.relative_to(OUT.parent)}/")
