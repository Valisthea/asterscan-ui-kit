"""Generate 5 individual alpha-tool banners + 1 suite overview banner.
Run from the asterscan-ui-kit/ root.
Idempotent — overwrites files in alpha/."""
import pathlib

ALPHA_TOOLS = [
    {
        "slug":  "smart-money-mirror",
        "emoji": "&#x1FA9E;",
        "name":  "Smart Money Mirror",
        "tag":   "Wallets that move BEFORE the move.",
        "blurb": "Win-rate scoring across 1h / 6h / 24h horizons. Rolling 30-day window. Sample-size weighted to discourage one-shot lucky calls.",
        "tone":  "primary",
    },
    {
        "slug":  "private-mirror",
        "emoji": "&#x1F512;",
        "name":  "Private Mirror",
        "tag":   "Privacy adoption — what the chain hides.",
        "blurb": "Cipher vs transparent transaction breakdown. Per-action mix. Top private wallets. 7-day x 24-hour heatmap of when privacy peaks.",
        "tone":  "primary",
    },
    {
        "slug":  "validator-xray",
        "emoji": "&#x1F52C;",
        "name":  "Validator X-Ray",
        "tag":   "Concentration risk + sealing health.",
        "blurb": "Per-validator stake share with sigmoid-scored concentration. Sealing latency vs rolling baseline. Oracle deviation tracker.",
        "tone":  "warning",
    },
    {
        "slug":  "iceberg-hunter",
        "emoji": "&#x1F9CA;",
        "name":  "Iceberg Hunter",
        "tag":   "Heuristic detection of split orders.",
        "blurb": "Children + window + size cluster heuristic. Catches whales splitting big orders into stealth chunks across short windows.",
        "tone":  "primary",
    },
    {
        "slug":  "liquidation-forecaster",
        "emoji": "&#x1F32A;&#xFE0F;",
        "name":  "Liquidation Forecaster",
        "tag":   "Forward cascade, before it triggers.",
        "blurb": "0.5 percent price grid heatmap by side. Per-symbol drilldown - which symbol wipes first. Telegram alert at $10M cascade @ -2 percent.",
        "tone":  "danger",
    },
]

TONE_COLORS = {
    "primary": "#F4D5B1",
    "warning": "#F59E0B",
    "danger":  "#EF4444",
}


def hex_to_rgb_str(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def lighten(hex_color: str, factor: float = 0.35) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02X}{g:02X}{b:02X}"


def render_banner(tool: dict) -> str:
    tone = TONE_COLORS[tool["tone"]]
    tone_rgb = hex_to_rgb_str(tone)
    tone_light = lighten(tone, 0.35)
    slug_short = tool["slug"].replace("-", " ")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AsterScan Alpha &mdash; {tool["name"]}</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #2a2a2c; padding: 24px; font-family: 'DM Sans', system-ui, sans-serif; }}
    .banner {{
      width: 1200px; height: 630px;
      background:
        radial-gradient(ellipse at top right, rgba({tone_rgb}, 0.10), transparent 55%),
        linear-gradient(180deg, #0E0E0F 0%, #161618 100%);
      color: #F2F0EE;
      padding: 70px 80px;
      display: flex; flex-direction: column; justify-content: space-between;
      position: relative; overflow: hidden;
      border-radius: 16px;
    }}
    .banner::after {{
      content: ''; position: absolute; top: 0; right: 0;
      width: 360px; height: 5px;
      background: linear-gradient(90deg, transparent, {tone});
    }}
    .head {{ display: flex; justify-content: space-between; align-items: flex-start; }}
    .brand {{ display: flex; align-items: center; gap: 14px; }}
    .icon-mark {{
      width: 50px; height: 50px;
      background: linear-gradient(135deg, #F4D5B1, #FFD29F);
      border-radius: 12px;
      display: grid; place-items: center;
      color: #0E0E0F; font-weight: 800; font-size: 26px;
    }}
    .wordmark {{ font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em; display: inline-flex; align-items: baseline; gap: 1px; font-size: 24px; }}
    .wordmark .aster {{ font-weight: 700; color: #F4D5B1; }}
    .wordmark .scan  {{ font-weight: 400; color: #B9B5B0; opacity: 0.7; }}
    .meta {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #7A7770; letter-spacing: 0.18em; text-transform: uppercase; margin-top: 4px; }}
    .alpha-tag {{
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 14px; border-radius: 9999px;
      background: rgba({tone_rgb}, 0.15);
      color: {tone};
      border: 1px solid rgba({tone_rgb}, 0.30);
      font-family: 'JetBrains Mono', monospace; font-size: 11px;
      letter-spacing: 0.2em; text-transform: uppercase; font-weight: 600;
    }}

    .body {{ display: flex; flex-direction: column; gap: 16px; }}
    .body .emoji {{ font-size: 48px; line-height: 1; }}
    .body .name {{ font-size: 64px; font-weight: 800; letter-spacing: -0.025em; line-height: 1.05; }}
    .body .name .accent {{
      background: linear-gradient(120deg, {tone}, {tone_light});
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .body .tag {{ font-size: 22px; color: #B9B5B0; line-height: 1.4; max-width: 820px; }}
    .body .blurb {{ font-size: 15px; color: #7A7770; line-height: 1.55; max-width: 820px; padding-top: 4px; }}

    .footer {{ display: flex; justify-content: space-between; align-items: flex-end; }}
    .url {{ font-family: 'JetBrains Mono', monospace; font-size: 16px; color: #F2F0EE; opacity: 0.85; }}
    .by  {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #7A7770; letter-spacing: 0.18em; text-transform: uppercase; }}
  </style>
</head>
<body>

<div class="banner">
  <div class="head">
    <div class="brand">
      <div class="icon-mark">&#10033;</div>
      <div>
        <div class="wordmark"><span class="aster">ASTER</span><span class="scan">SCAN</span></div>
        <div class="meta">Alpha suite</div>
      </div>
    </div>
    <div class="alpha-tag">Alpha &middot; {slug_short}</div>
  </div>

  <div class="body">
    <div class="emoji">{tool["emoji"]}</div>
    <div class="name">{tool["name"]}</div>
    <div class="tag">{tool["tag"]}</div>
    <div class="blurb">{tool["blurb"]}</div>
  </div>

  <div class="footer">
    <div class="url">aster-scan.com/alpha/{tool["slug"]}</div>
    <div class="by">Beta &middot; signal-grade analytics, not financial advice</div>
  </div>
</div>

</body>
</html>
"""


def render_overview() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AsterScan Alpha &mdash; Suite Overview</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #2a2a2c; padding: 24px; font-family: 'DM Sans', system-ui, sans-serif; }
    .banner {
      width: 1200px; height: 630px;
      background:
        radial-gradient(ellipse at top right, rgba(244, 213, 177, 0.10), transparent 55%),
        linear-gradient(180deg, #0E0E0F 0%, #161618 100%);
      color: #F2F0EE;
      padding: 60px 70px 50px;
      display: flex; flex-direction: column; gap: 28px;
      position: relative; overflow: hidden;
      border-radius: 16px;
    }
    .banner::after { content: ''; position: absolute; top: 0; right: 0; width: 360px; height: 5px; background: linear-gradient(90deg, transparent, #F4D5B1); }
    .head { display: flex; justify-content: space-between; align-items: flex-start; }
    .brand { display: flex; align-items: center; gap: 14px; }
    .icon-mark { width: 50px; height: 50px; background: linear-gradient(135deg, #F4D5B1, #FFD29F); border-radius: 12px; display: grid; place-items: center; color: #0E0E0F; font-weight: 800; font-size: 26px; }
    .wordmark { font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em; display: inline-flex; align-items: baseline; gap: 1px; font-size: 24px; }
    .wordmark .aster { font-weight: 700; color: #F4D5B1; }
    .wordmark .scan  { font-weight: 400; color: #B9B5B0; opacity: 0.7; }
    .meta { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #7A7770; letter-spacing: 0.18em; text-transform: uppercase; margin-top: 4px; }
    .alpha-tag { display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 9999px; background: rgba(244, 213, 177, 0.15); color: #F4D5B1; border: 1px solid rgba(244, 213, 177, 0.30); font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 600; }

    .title-block .name { font-size: 48px; font-weight: 800; letter-spacing: -0.025em; line-height: 1.05; }
    .title-block .name .accent { background: linear-gradient(120deg, #F4D5B1, #FFD29F); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
    .title-block .tag { font-size: 18px; color: #B9B5B0; margin-top: 6px; }

    .grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
    .tool { background: rgba(22, 22, 24, 0.6); border: 1px solid #26262A; border-radius: 12px; padding: 16px 14px; display: flex; flex-direction: column; gap: 6px; }
    .tool .tool-emoji { font-size: 24px; line-height: 1; }
    .tool .tool-name { font-size: 13px; font-weight: 700; line-height: 1.2; }
    .tool .tool-blurb { font-size: 11px; color: #7A7770; line-height: 1.4; }

    .footer { display: flex; justify-content: space-between; align-items: flex-end; padding-top: 4px; }
    .url { font-family: 'JetBrains Mono', monospace; font-size: 16px; color: #F2F0EE; opacity: 0.85; }
    .by  { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #7A7770; letter-spacing: 0.18em; text-transform: uppercase; }
  </style>
</head>
<body>

<div class="banner">
  <div class="head">
    <div class="brand">
      <div class="icon-mark">&#10033;</div>
      <div>
        <div class="wordmark"><span class="aster">ASTER</span><span class="scan">SCAN</span></div>
        <div class="meta">Alpha suite</div>
      </div>
    </div>
    <div class="alpha-tag">5 tools &middot; live</div>
  </div>

  <div class="title-block">
    <div class="name">The Alpha <span class="accent">suite.</span></div>
    <div class="tag">Five tools that read what the chain doesn&apos;t say out loud.</div>
  </div>

  <div class="grid">
    <div class="tool">
      <div class="tool-emoji">&#x1FA9E;</div>
      <div class="tool-name">Smart Money Mirror</div>
      <div class="tool-blurb">Wallets that move before the move.</div>
    </div>
    <div class="tool">
      <div class="tool-emoji">&#x1F512;</div>
      <div class="tool-name">Private Mirror</div>
      <div class="tool-blurb">Privacy adoption + cipher heatmap.</div>
    </div>
    <div class="tool">
      <div class="tool-emoji">&#x1F52C;</div>
      <div class="tool-name">Validator X-Ray</div>
      <div class="tool-blurb">Concentration + oracle deviation.</div>
    </div>
    <div class="tool">
      <div class="tool-emoji">&#x1F9CA;</div>
      <div class="tool-name">Iceberg Hunter</div>
      <div class="tool-blurb">Split-order heuristic detection.</div>
    </div>
    <div class="tool">
      <div class="tool-emoji">&#x1F32A;&#xFE0F;</div>
      <div class="tool-name">Liquidation Forecaster</div>
      <div class="tool-blurb">Forward cascade simulation.</div>
    </div>
  </div>

  <div class="footer">
    <div class="url">aster-scan.com/alpha</div>
    <div class="by">Beta &middot; signal-grade analytics</div>
  </div>
</div>

</body>
</html>
"""


def main():
    base = pathlib.Path("alpha")
    base.mkdir(exist_ok=True)
    for tool in ALPHA_TOOLS:
        (base / f"alpha-{tool['slug']}.html").write_text(render_banner(tool), encoding="utf-8")
        print(f"  alpha/alpha-{tool['slug']}.html")
    (base / "alpha-suite-overview.html").write_text(render_overview(), encoding="utf-8")
    print("  alpha/alpha-suite-overview.html")
    print(f"\nTotal: {len(ALPHA_TOOLS) + 1} banners")


if __name__ == "__main__":
    main()
