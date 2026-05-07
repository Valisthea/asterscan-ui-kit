# AsterScan — UI Partner Kit

Static asset library for designers / motion / video / social producing content on **AsterScan** by Kairos Lab.

> Browse interactive: open `index.html` in any browser, or visit the deployed URL once Vercel is connected.

## Inventory

```
.
├── index.html                            ← gallery (open this first)
├── README.md                             ← this file
├── vercel.json                           ← static deploy config
│
├── logos/                                drag-drop SVG into Figma / Illustrator
│   ├── asterscan-logo-compact.svg
│   ├── asterscan-logo-white.svg
│   └── asterscan-icon-mark.svg
│
├── colors.json                           raw palette (HEX, RGB, role)
├── figma-tokens.json                     Tokens Studio for Figma format
├── palette-card.html                     printable A4 landscape palette
│
├── typography/
│   └── typography-card.html              DM Sans + JetBrains Mono specimen
│
├── components.html                       buttons, badges, cards, stat numbers,
│                                          data-age pills, hover-state tables
│
├── frames/                               1920×1080 video templates
│   ├── title-card-1920x1080.html
│   ├── lower-third-1920x1080.html
│   └── end-card-1920x1080.html
│
└── social/                               brand-skinned social cards (empty copy)
    ├── og-card-1200x630.html             Facebook / LinkedIn / Discord
    ├── twitter-card-1200x675.html        X large card
    ├── instagram-1080x1080.html          IG / Threads
    ├── twitter-banner-1500x500.html      X profile banner
    └── github-social-1280x640.html       repo social preview
```

## How the designer uses these

Each HTML file is a **self-contained brand frame** at native pixel size. No external CSS dependencies, just Google Fonts loaded inline.

### To produce a static image

1. Open the HTML in Chrome / Arc
2. Use a clean-screenshot tool (Cleanshot Mac, Snagit Win, Polish, native browser DevTools "Capture full size screenshot")
3. Capture at 1× — the rendered dimensions match the export target exactly

### To produce video / motion

1. Open the relevant `frames/*.html`
2. Edit the placeholder copy directly in the HTML, OR overlay text via After Effects / Premiere
3. Capture the rendered frame and drop into the composition

### To use brand colors / fonts in any tool

- **Figma**: install **Tokens Studio for Figma** → Load JSON → pick `figma-tokens.json` → Apply
- **Photoshop / Illustrator / After Effects**: copy HEX values from `colors.json`
- **CSS / Tailwind**: copy the role-named tokens (`primary`, `surface`, `success`, etc.)

## Brand basics

- Primary cream: `#F4D5B1 → #FFD29F` gradient
- Background: `#0E0E0F` near-black
- Type: DM Sans (UI) + JetBrains Mono (numbers, addresses)
- Long / Short: `#22C55E` / `#EF4444`
- Cliff / warning: `#F59E0B`

## Deploy on Vercel

This repo deploys as a **static site** with zero build step. Three steps:

1. **Vercel dashboard** → **Add new** → **Project**
2. **Import Git Repository** → pick this repo
3. **Framework Preset: Other** · **Build Command: (empty)** · **Output Directory: `.`** → Deploy

Done. Vercel auto-detects this is a static site from `vercel.json`.

**Optional**: bind a custom domain (e.g. `kit.aster-scan.com`) via Vercel project → Domains. CNAME or A record on your DNS provider, Vercel handles the SSL automatically.

## License

© Kairos Lab. Free for AsterScan-related content (Aster team videos, partner work, press articles). Do not redistribute as standalone assets.

Brand questions: brand@kairos-lab.org
