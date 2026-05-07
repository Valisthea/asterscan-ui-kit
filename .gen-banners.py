#!/usr/bin/env python3
"""
Generate the 7 alpha banners + 1 suite overview at 1200x630.

Reproduces the *live* alpha card from src/app/alpha/page.tsx as it
ships on aster-scan.com/alpha — same .card background, same animated
<AlphaCardVisual> at the top, emoji + version pill, title, italic
mono tagline, description paragraph, capabilities list with yellow
arrow markers. No branded marketing chrome, no headline. The banner
IS the production card, scaled up to 1200x630.

Tool list, taglines, descriptions, capabilities, status pills, emojis
mirror src/app/alpha/page.tsx FEATURES exactly.

Run from C:\\Users\\admin\\Desktop\\asterscan-ui-kit:
  python .gen-banners.py
"""

from pathlib import Path

OUT = Path(__file__).parent / "alpha"
OUT.mkdir(parents=True, exist_ok=True)

# ── Common stylesheet — matches Tailwind tokens from the live site ──
COMMON_CSS = r"""
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg-primary: #0E0E0F;
  --surface: #161618;
  --surface-raised: #1C1C1F;
  --border: #26262A;
  --text-primary: #F2F0EE;
  --text-secondary: #B9B5B0;
  --text-muted: #7A7770;
  --primary: #F4D5B1;
  --yellow-400: rgb(250, 204, 21);
}
body {
  background: #2a2a2c; padding: 24px;
  font-family: 'DM Sans', system-ui, sans-serif;
  color: var(--text-primary);
}

/* The banner IS the .card from globals.css, scaled to 1200x630. */
.banner {
  width: 1200px; height: 630px;
  background: var(--surface-raised);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 60px;
  display: flex; flex-direction: column; gap: 24px;
  position: relative; overflow: hidden;
}

/* AlphaCardVisual — pixel-for-pixel from src/components/alpha/AlphaCardVisual.tsx */
.alpha-visual {
  position: relative;
  width: 100%; height: 200px;
  border-radius: 8px;
  border: 1px solid rgba(250, 204, 21, 0.40);
  overflow: hidden;
  box-shadow: inset 0 1px 4px rgba(0,0,0,0.3);
  background: linear-gradient(135deg,
    rgba(250, 204, 21, 0.10) 0%,
    rgba(14, 14, 15, 0.60) 50%,
    rgba(250, 204, 21, 0.15) 100%);
}

/* Header row: emoji left, version pill right */
.head-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
.emoji { font-size: 56px; line-height: 1; }
.status {
  font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600;
  color: var(--yellow-400); background: rgba(250, 204, 21, 0.10);
  border: 1px solid rgba(250, 204, 21, 0.30);
  padding: 5px 12px; border-radius: 5px;
  text-transform: uppercase; letter-spacing: 0.2em;
  white-space: nowrap; align-self: flex-start; margin-top: 14px;
}

/* Title + tagline + description */
.title { font-size: 44px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em; line-height: 1.1; margin-top: -8px; }
.tagline { font-family: 'JetBrains Mono', monospace; font-style: italic;
  font-size: 17px; color: var(--text-muted); margin-top: 6px; }
.description { font-size: 17px; color: var(--text-secondary); line-height: 1.55; }

/* Capabilities list */
.caps {
  list-style: none; padding-top: 16px; border-top: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 8px; margin-top: auto;
}
.caps li { font-size: 14px; color: var(--text-secondary); display: flex; align-items: flex-start; gap: 10px; line-height: 1.4; }
.caps li::before { content: "▸"; color: var(--yellow-400); flex-shrink: 0; margin-top: 1px; }

/* Brand stamp bottom-right (small, unobtrusive — matches what the explorer footer would show) */
.brand-stamp {
  position: absolute; bottom: 18px; right: 24px;
  font-family: 'JetBrains Mono', monospace; font-size: 10px;
  color: var(--text-muted); letter-spacing: 0.18em; text-transform: uppercase;
  display: flex; align-items: center; gap: 8px;
}
.brand-stamp .wm { display: inline-flex; align-items: baseline; gap: 1px; letter-spacing: 0.1em; font-size: 11px; }
.brand-stamp .wm .a { font-weight: 700; color: var(--primary); }
.brand-stamp .wm .s { font-weight: 400; color: var(--text-secondary); opacity: 0.7; }
.brand-stamp .sep { opacity: 0.4; }

/* Animation keyframes (1:1 from AlphaCardVisual.tsx) */
@keyframes alpha-scroll-y { 0% { transform: translateY(-100%); } 100% { transform: translateY(0); } }
@keyframes alpha-sweep    { 0% { transform: translateX(-10%); } 100% { transform: translateX(110%); } }
@keyframes alpha-bob      { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
@keyframes alpha-pulse    { 0%,100% { opacity: 0.4; } 50% { opacity: 1; } }
@keyframes alpha-drop     { 0% { transform: scaleY(0.05); transform-origin: top; opacity: 0; } 10% { opacity: 1; } 100% { transform: scaleY(1); transform-origin: top; opacity: 1; } }
@keyframes alpha-fade-up  { 0% { opacity: 0; transform: translateY(4px); } 20% { opacity: 1; transform: translateY(0); } 80% { opacity: 1; } 100% { opacity: 0; transform: translateY(-4px); } }
@keyframes alpha-trail    { 0% { transform: translateX(0); } 100% { transform: translateX(82%); } }
@media (prefers-reduced-motion: reduce) { .alpha-visual *, .alpha-visual { animation: none !important; } }
"""

PAGE_TPL = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AsterScan Alpha — {title}</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
<div class="banner">
  <div class="alpha-visual">{visual}</div>

  <div class="head-row">
    <div>
      <span class="emoji">{emoji}</span>
    </div>
    <span class="status">{status}</span>
  </div>

  <div>
    <h1 class="title">{title}</h1>
    <p class="tagline">{tagline}</p>
  </div>

  <p class="description">{description}</p>

  <ul class="caps">
    {caps_html}
  </ul>

  <div class="brand-stamp">
    <span class="wm"><span class="a">ASTER</span><span class="s">SCAN</span></span>
    <span class="sep">·</span>
    <span>aster-scan.com/alpha</span>
  </div>
</div>
</body>
</html>
"""


# ── Per-theme animated visuals (1:1 from AlphaCardVisual.tsx) ──

def visual_privacy() -> str:
    cols = ["1f", "9c", "0a", "e3", "5b", "47", "8d", "22", "c0"] * 2
    columns = ""
    for i in range(8):
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
        align-items: stretch; padding: 0 18px; font-family: 'JetBrains Mono', monospace;
        font-size: 14px; color: rgba(250, 204, 21, 0.55); user-select: none; }}
      .pcol {{ display: flex; flex-direction: column; align-items: center; line-height: 1.2; }}
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
        justify-content: center; padding: 0 24px; font-family: 'JetBrains Mono', monospace;
        font-size: 14px; color: rgba(250, 204, 21, 0.75); line-height: 1.7;
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
        justify-content: space-around; padding: 0 14px 8px; }}
      .cwrap .bar {{ width: 12px; border-radius: 2px 2px 0 0;
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

# ── 7 features mirroring src/app/alpha/page.tsx FEATURES verbatim ──
FEATURES = [
    {
        "slug": "alpha-private-mirror",
        "emoji": "🌑",
        "theme": "privacy",
        "title": "Private Mirror",
        "tagline": "Inferring signal from encrypted on-chain traffic.",
        "description":
            "Around 70-90% of Aster Chain traffic uses privacy mode — encrypted order payloads. "
            "Every other explorer treats those as black holes. Private Mirror reads the metadata that's "
            "still public (timing, size class, sender, validator) and infers aggregate flows.",
        "capabilities": [
            "Long/short bias gauge with confidence interval",
            "Privacy whale heatmap (size-classed, anonymized)",
            "Correlated address clusters via co-occurrence inference",
        ],
        "status": "v1",
    },
    {
        "slug": "alpha-time-machine",
        "emoji": "⏳",
        "theme": "time",
        "title": "Time Machine",
        "tagline": "Rewind any moment of Aster Chain.",
        "description":
            "Pick a block height — see the full state of the network at that exact instant. "
            "Validator set, total stake, top tickers, oracle prices, average APY, privacy adoption. "
            "Built for forensics, journalists, and traders post-morteming a cascade or oracle spike.",
        "capabilities": [
            "Block-level scrubber across full chain history",
            "Snapshot of network stats at any height",
            "Compare two moments side by side",
        ],
        "status": "v0.5",
    },
    {
        "slug": "alpha-insight-engine",
        "emoji": "🎙",
        "theme": "insight",
        "title": "Insight Engine",
        "tagline": "Aster Chain narrated in plain English.",
        "description":
            "A rule-based engine watching the chain in real time and producing observations the way "
            "a quant analyst would. Whale moves contextualized, validator anomalies surfaced, privacy "
            "adoption shifts annotated. Generates a Daily Brief at 00:00 UTC.",
        "capabilities": [
            "Live observation feed (10–30 events/hour)",
            "Daily Brief auto-generated at 00:00 UTC",
            "Per-event evidence trail (the underlying tx / metric chain)",
        ],
        "status": "v0.5",
    },
    {
        "slug": "alpha-smart-money-mirror",
        "emoji": "🪞",
        "theme": "mirror",
        "title": "Smart Money Mirror",
        "tagline": "Wallets that move BEFORE the move.",
        "description":
            "We identify the wallets whose whale orders preceded favorable price moves over a rolling "
            "30-day window. Each address gets a predictive accuracy score, weighted by sample size and "
            "decayed for inactive periods. Top of the leaderboard = the addresses worth watching.",
        "capabilities": [
            "Per-address predictive accuracy (1h / 6h / 24h)",
            "Sample-size-weighted scoring (no one-shot luck)",
            "Top-100 leaderboard with side-distribution",
        ],
        "status": "v0.5",
    },
    {
        "slug": "alpha-validator-xray",
        "emoji": "🎯",
        "theme": "xray",
        "title": "Validator X-Ray",
        "tagline": "Per-validator forensics ahead of external set opening.",
        "description":
            "The Aster oracle is a stake-weighted median across 6 validators. When external validators "
            "open in Q2 2026, the difference between a good validator and a bad one starts mattering. "
            "X-Ray decomposes each validator's behavior — deviation, latency, stake concentration.",
        "capabilities": [
            "Oracle deviation per validator (rolling 24h)",
            "Stake concentration (Gini) + delegation churn",
            "Slashing risk score with full evidence trail",
        ],
        "status": "v0.5",
    },
    {
        "slug": "alpha-liquidation-forecaster",
        "emoji": "🌪️",
        "theme": "cascade",
        "title": "Liquidation Forecaster",
        "tagline": "Cascade simulation across leverage tiers.",
        "description":
            "Aster's leverage ladder (Pro up to 100x, 1001x mode on BTC/ETH) means liquidation cascades "
            "hit different tiers at different prices. The Forecaster simulates: at -1% / -2% / -5% / -10% "
            "from spot, what tier liquidates first, total notional unwound, projected funding spike.",
        "capabilities": [
            "Forward cascade simulation (-1% to -10% bands)",
            "Per-tier breakdown (Pro 5x→100x, 1001x BTC/ETH)",
            "Cross vs isolated margin separation",
        ],
        "status": "v0.5",
    },
    {
        "slug": "alpha-iceberg-hunter",
        "emoji": "🧊",
        "theme": "iceberg",
        "title": "Iceberg Hunter",
        "tagline": "Whales splitting orders to hide their hand.",
        "description":
            "Some whales avoid market impact by splitting one $5M order into 50 smaller privacy orders "
            "fired in a tight time window. Iceberg Hunter focuses on the intra-wallet pattern: same "
            "sender + N privacy orders within W seconds + size-class clustering = iceberg signal.",
        "capabilities": [
            "Per-wallet iceberg score (intra-window cohesion)",
            "Live feed of detected icebergs (last 6h)",
            "Methodology disclosed: false-positive rate calibration",
        ],
        "status": "v0.5",
    },
]


def write_page(slug: str, html: str) -> None:
    path = OUT / f"{slug}.html"
    path.write_text(html, encoding="utf-8")
    print(f"  wrote {path.relative_to(OUT.parent)}")


def gen_individual() -> None:
    for f in FEATURES:
        visual = VISUALS[f["theme"]]()
        caps_html = "\n    ".join(f"<li>{c}</li>" for c in f["capabilities"])
        html = PAGE_TPL.format(
            title=f["title"],
            css=COMMON_CSS,
            visual=visual,
            emoji=f["emoji"],
            status=f["status"],
            tagline=f["tagline"],
            description=f["description"],
            caps_html=caps_html,
        )
        write_page(f["slug"], html)


def gen_overview() -> None:
    """Suite overview — same 3-column grid as the live /alpha page,
    showing all 7 cards as compact tiles. Reproduces the live gallery."""
    tiles_html = ""
    for f in FEATURES:
        v = VISUALS[f["theme"]]()
        tiles_html += f"""
        <div class="tile">
          <div class="tile-visual">{v}</div>
          <div class="tile-meta">
            <span class="t-emoji">{f["emoji"]}</span>
            <div>
              <div class="t-title">{f["title"]}</div>
              <div class="t-tag">{f["tagline"]}</div>
            </div>
            <span class="t-ver">{f["status"]}</span>
          </div>
        </div>
        """

    overview_css = COMMON_CSS + r"""
.banner { padding: 40px 50px; gap: 18px; }
.head-overview { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; }
.head-overview h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }
.head-overview .sub { font-family: 'JetBrains Mono', monospace; font-style: italic;
  font-size: 14px; color: var(--text-muted); margin-top: 4px; }
.head-overview .alpha-pill {
  font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600;
  color: var(--yellow-400); background: rgba(250, 204, 21, 0.10);
  border: 1px solid rgba(250, 204, 21, 0.30);
  padding: 4px 10px; border-radius: 5px;
  text-transform: uppercase; letter-spacing: 0.2em;
}
.tiles {
  flex: 1;
  display: grid; grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 1fr; gap: 12px;
}
.tile {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  display: flex; flex-direction: column;
}
.tile-visual {
  position: relative; height: 70px;
  border-bottom: 1px solid rgba(250, 204, 21, 0.30);
  background: linear-gradient(135deg, rgba(250, 204, 21, 0.10) 0%,
    rgba(14, 14, 15, 0.60) 50%, rgba(250, 204, 21, 0.15) 100%);
}
.tile-meta { padding: 10px 12px; display: flex; align-items: flex-start; gap: 10px; flex: 1; }
.tile-meta > div { flex: 1; min-width: 0; }
.t-emoji { font-size: 22px; line-height: 1; }
.t-title { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.t-tag { font-family: 'JetBrains Mono', monospace; font-style: italic;
  font-size: 10px; color: var(--text-muted); margin-top: 2px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.t-ver { font-family: 'JetBrains Mono', monospace; font-size: 9px;
  color: var(--yellow-400); background: rgba(250, 204, 21, 0.10);
  border: 1px solid rgba(250, 204, 21, 0.30);
  padding: 2px 5px; border-radius: 3px;
  text-transform: uppercase; letter-spacing: 0.18em;
  align-self: flex-start; }
"""

    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AsterScan Alpha — Suite</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>""" + overview_css + """</style>
</head>
<body>
<div class="banner">
  <div class="head-overview">
    <div>
      <h1>AsterScan Alpha</h1>
      <p class="sub">Experimental features pushing the boundaries of what's observable on Aster Chain.</p>
    </div>
    <span class="alpha-pill">7 tools</span>
  </div>

  <div class="tiles">""" + tiles_html + """</div>

  <div class="brand-stamp">
    <span class="wm"><span class="a">ASTER</span><span class="s">SCAN</span></span>
    <span class="sep">·</span>
    <span>aster-scan.com/alpha</span>
  </div>
</div>
</body>
</html>
"""
    write_page("alpha-suite-overview", html)


if __name__ == "__main__":
    print("Generating alpha banners -> /alpha/")
    gen_individual()
    gen_overview()
    print(f"\nDone. {len(FEATURES) + 1} files in {OUT.relative_to(OUT.parent)}/")
