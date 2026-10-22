"""Build index.html for tolgaozden.net from src/content.json.

Run:  python -I src/build_site.py
      Paths resolve relative to this file, so the working directory does not matter.
      Standard library only.

What it does
------------
Reads src/content.json and writes index.html at the repository root: one page with a sticky
profile card on the left and four tabs on the right (Research, Policy work, Codes, HetLearn
Toolbox). Every tab is a plain list rendered here at build time, so the page's JavaScript only
switches tabs and the day/night theme. Each tab has a deep link: index.html#research, #policy,
#codes and #hetlearn.

index.html is generated. Hand edits to it are overwritten on the next run; change
src/content.json (content) or this script (layout, colors, fonts) instead.

To add an item
--------------
1. In src/content.json, copy an entry in "research", "policy" or "codes" and edit the copy.
   Entries appear in file order. A "policy" entry with "section": "ado" goes to the Asian
   Development Outlook list at the foot of the Policy work tab.
2. Run  python -I src/build_site.py .
3. Commit src/content.json and index.html together.

Most fields are plain text and are escaped here. Fields that hold HTML go into the page as
written (bio, office, coauthors, code "summary" and "description", HetLearn "summary",
"paragraphs" and "note"), so an "&" or "<" in them must be written as &amp; or &lt;.

Colors and fonts
----------------
DAY and NIGHT below hold the two color themes as CSS custom properties (underscores become
hyphens: accent_soft -> --accent-soft). The page follows the system setting and has a day/night
switch in the profile card. FONTS and GOOGLE_FONTS set the typeface.
"""
import html
import json
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
CONTENT = SRC / "content.json"
OUTPUT = ROOT / "index.html"

# --------------------------------------------------------------------------------------------
# Day theme ("Violet"): cool grey page, white cards, violet accent and strip.
# --------------------------------------------------------------------------------------------
DAY = {
    # tags: publication status, code kind
    "pub_bg": "#DCFCE7", "pub_fg": "#15803D", "pub_dot": "#22C55E",
    "wp_bg": "#DBEAFE", "wp_fg": "#1D4ED8",
    "rev_bg": "#FEF3C7", "rev_fg": "#B45309",
    "tool_bg": "var(--accent-soft)", "tool_fg": "var(--link)",
    "repl_bg": "#E2E8F0", "repl_fg": "#334155",
    # tags: institutions (Policy work tab)
    "boc_bg": "#FEE2E2", "boc_fg": "#B91C1C",
    "ecb_bg": "#DBEAFE", "ecb_fg": "#1D4ED8",
    "dnb_bg": "#FFEDD5", "dnb_fg": "#C2410C",
    "boe_bg": "#CCFBF1", "boe_fg": "#0F766E",
    "adb_bg": "#E2E8F0", "adb_fg": "#475569",
    # page, cards, text, accent
    "bg": "#E9EDF3", "card": "#FFFFFF", "text": "#111827", "muted": "#5B6472", "border": "#D2D9E4",
    "accent": "#7C3AED", "accent_hover": "#6D28D9", "accent_soft": "#EDE9FE", "on_accent": "#FFFFFF",
    "link": "#6D28D9", "focus": "#7C3AED", "glow": "rgba(124,58,237,.15)",
    "strip": "linear-gradient(90deg, #7C3AED, #A78BFA, #C084FC, #E879F9)",
    "shadow": "0 1px 3px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.05)",
    "shadow_hover": "0 12px 28px rgba(15,23,42,.12), 0 4px 10px rgba(15,23,42,.06)",
    "radius": "12px",
    # tile colors from the design build (not used by this layout)
    "tile_journal_bg": "#EDE9FE", "tile_journal_fg": "#5B21B6", "tile_bank_bg": "#E0E7FF", "tile_bank_fg": "#3730A3",
    "tile_draft_bg": "#FEF3C7", "tile_draft_fg": "#92400E", "tile_code_bg": "#E0F2FE", "tile_code_fg": "#0369A1",
    # day/night switch: knob under the sun
    "knob_y": "0px", "sun_fg": "var(--on-accent)", "moon_fg": "var(--muted)",
}

# --------------------------------------------------------------------------------------------
# Night theme ("Night"): deep blue-slate page, brass accent and strip.
# --------------------------------------------------------------------------------------------
NIGHT = {
    # tags: publication status, code kind
    "pub_bg": "#0F3326", "pub_fg": "#7EE0AE", "pub_dot": "#3CCB82",
    "wp_bg": "#172B47", "wp_fg": "#9DBDEB",
    "rev_bg": "#3A2A10", "rev_fg": "#F2C66D",
    "tool_bg": "var(--accent-soft)", "tool_fg": "var(--link)",
    "repl_bg": "#222D3D", "repl_fg": "#B8C2D0",
    # tags: institutions (Policy work tab)
    "boc_bg": "#3A1D1D", "boc_fg": "#F0A8A0",
    "ecb_bg": "#172B47", "ecb_fg": "#9DBDEB",
    "dnb_bg": "#3A2512", "dnb_fg": "#F2B77F",
    "boe_bg": "#12302D", "boe_fg": "#8BD6CB",
    "adb_bg": "#222D3D", "adb_fg": "#B8C2D0",
    # page, cards, text, accent
    "bg": "#0E1522", "card": "#161F2E", "text": "#E9E5DC", "muted": "#97A1B2", "border": "#263247",
    "accent": "#D4A24C", "accent_hover": "#E2B565", "accent_soft": "#2C2416", "on_accent": "#17110A",
    "link": "#E3B867", "focus": "#E3B867", "glow": "rgba(212,162,76,.22)",
    "strip": "linear-gradient(90deg, #7A5A22, #B98A3A, #D4A24C, #EBCB8B)",
    "shadow": "0 1px 3px rgba(0,0,0,.35)",
    "shadow_hover": "0 14px 30px rgba(0,0,0,.45), 0 4px 10px rgba(0,0,0,.25)",
    "radius": "12px",
    # tile colors from the design build (not used by this layout)
    "tile_journal_bg": "#2C2416", "tile_journal_fg": "#EBCB8B", "tile_bank_bg": "#1A2A3F", "tile_bank_fg": "#A9C1E0",
    "tile_draft_bg": "#2A2333", "tile_draft_fg": "#CDB8E6", "tile_code_bg": "#13302C", "tile_code_fg": "#86D3C3",
    # day/night switch: knob under the moon
    "knob_y": "26px", "sun_fg": "var(--muted)", "moon_fg": "var(--on-accent)",
}

# Type: Source Code Pro for all text, loaded from Google Fonts.
MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
FONTS = {"ui": f"'Source Code Pro', {MONO}", "title": f"'Source Code Pro', {MONO}", "body": f"'Source Code Pro', {MONO}"}
GOOGLE_FONTS = "family=Source+Code+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400"

TITLE = "Tolga Ozden | Economist"
THEME_KEY = "theme-violet-night"  # localStorage key that remembers the day/night choice
ANALYTICS = """<script>var clicky_site_ids = clicky_site_ids || []; clicky_site_ids.push(101237473);</script>
<script async src="https://static.getclicky.com/js"></script>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def _tok(d, indent="  "):
    return "".join(f"\n{indent}--{k.replace('_', '-')}: {v};" for k, v in d.items())


def theme_css():
    """Day tokens on :root; night tokens under the system dark preference (unless the switch says
    day) and under an explicit data-theme="dark"."""
    fonts = f"\n  --font-ui: {FONTS['ui']};\n  --font-title: {FONTS['title']};\n  --font-body: {FONTS['body']};"
    return (f":root {{{_tok(DAY)}{fonts}\n  color-scheme: light;\n}}\n"
            f"@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme=\"light\"]) {{"
            f"{_tok(NIGHT, '    ')}\n    color-scheme: dark;\n  }}\n}}\n"
            f":root[data-theme=\"dark\"] {{{_tok(NIGHT)}\n  color-scheme: dark;\n}}\n")


def head_html(content):
    p = content["profile"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(p.get('description', ''))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{esc(GOOGLE_FONTS + '&display=swap')}">
<script>(function(){{try{{var t=localStorage.getItem('{THEME_KEY}');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
"""


# Inline SVG icons (short paths). Stroke icons carry class "st".
ICONS = {
    "mail": '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "gh": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.9 1.2 1.9 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17.3 4.7 18.3 5 18.3 5c.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/></svg>',
    "scholar": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 1 9.5l11 6.5 9-5.3V17h2V9.5z"/><path d="M5.5 13.6v3.9L12 21l6.5-3.5v-3.9L12 17.4z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 10h4v11H3zM9.5 10h3.8v1.6c.6-1 1.9-1.9 3.8-1.9 4 0 4.6 2.6 4.6 6V21h-4v-4.6c0-1.5 0-3.3-2-3.3s-2.3 1.6-2.3 3.2V21h-3.9z"/></svg>',
    "right": '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "moon": '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/></svg>',
    "sun": '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>',
}

# --------------------------------------------------------------------------------------------
# Page CSS: 320px sticky profile card left, tabs right, every tab one plain list, max 1140px;
# one column below 1024px. Colors and fonts come from the tokens above.
# --------------------------------------------------------------------------------------------
LIST_CSS = r"""
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
[hidden] { display: none !important; }
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body {
  font-family: var(--font-ui); font-size: 14px; line-height: 1.6;
  background: var(--bg); color: var(--text); min-height: 100vh;
  transition: background-color .3s, color .3s;
}
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); background: var(--bg); z-index: 10; }
img { max-width: 100%; }
a { color: var(--link); }
button { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
svg { flex-shrink: 0; }
svg.st { fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

/* page grid */
.layout {
  max-width: 1140px; margin: 0 auto; display: grid;
  grid-template-columns: 320px minmax(0, 1fr); gap: 40px; align-items: start;
  padding-block: 40px 16px;
  padding-left: max(24px, env(safe-area-inset-left, 0px));
  padding-right: max(24px, env(safe-area-inset-right, 0px));
}
.sidebar { position: sticky; top: 24px; min-width: 0; }
.main { min-width: 0; }

/* profile card */
.profile-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden; transition: background-color .3s, border-color .3s; }
.strip { height: 6px; background: var(--strip); }
.profile-body { padding: 28px 24px 24px; }
.profile-header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
.avatar { width: 64px; height: 64px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 3px solid var(--accent-soft); box-shadow: 0 4px 12px var(--glow); }
.who { min-width: 0; }
.name { font-family: var(--font-title); font-size: 20px; font-weight: 700; line-height: 1.2; text-wrap: balance; }
.handle { font-size: 13px; font-weight: 500; color: var(--link); }
.meta { font-size: 13px; color: var(--muted); margin-bottom: 16px; }
.meta span { white-space: nowrap; }
.bio { font-family: var(--font-body); font-size: 13px; line-height: 1.7; margin-bottom: 20px; max-width: 68ch; }
.label { font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 4px; }
.contact { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; margin-bottom: 20px; font-size: 12px; }
.contact a {
  color: var(--link); font-weight: 500; text-decoration: none; overflow-wrap: anywhere;
  -webkit-user-select: text; user-select: text; -webkit-user-drag: none;  /* drag selects the address */
}
.contact a:hover { text-decoration: underline; }
.office { margin-top: 6px; color: var(--muted); line-height: 1.55; }
.social { display: flex; flex-wrap: wrap; gap: 10px; }
.social a {
  width: 40px; height: 40px; border-radius: 10px; border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  color: var(--muted); text-decoration: none; transition: all .2s;
}
.social a:hover { border-color: var(--accent); color: var(--link); background: var(--accent-soft); }
.social svg { width: 18px; height: 18px; fill: currentColor; }
.social svg.st { fill: none; }
.social .cv { font-family: var(--font-ui); font-size: 12px; font-weight: 700; letter-spacing: .02em; }

/* day/night switch, sun over moon: the knob sits under the active icon; its position comes from the theme tokens */
.daynight {
  position: relative; margin-left: auto; align-self: flex-start; flex-shrink: 0;
  display: inline-flex; flex-direction: column; align-items: center; padding: 3px; border-radius: 16px;
  border: 1px solid var(--border); background: var(--bg); cursor: pointer; transition: border-color .2s;
}
.daynight:hover { border-color: var(--accent); }
.daynight .knob {
  position: absolute; top: 3px; left: 3px; width: 28px; height: 26px; border-radius: 13px;
  background: var(--accent); transform: translateY(var(--knob-y)); transition: transform .25s cubic-bezier(.4, 0, .2, 1), background-color .3s;
}
.daynight .dn { position: relative; width: 28px; height: 26px; display: flex; align-items: center; justify-content: center; transition: color .2s; }
.daynight .dn svg { width: 15px; height: 15px; }
.daynight .sun { color: var(--sun-fg); }
.daynight .moon { color: var(--moon-fg); }

/* tabs */
.tabs { margin-bottom: 28px; }
.tab-row { display: flex; gap: 8px; }
.tab {
  flex: 1 1 0; min-width: max-content; padding: 12px 18px; text-align: center; white-space: nowrap;
  font-size: 14px; font-weight: 600; border: 1px solid var(--border); border-radius: 10px;
  background: var(--card); color: var(--muted); cursor: pointer; transition: all .2s;
}
.tab[aria-selected="true"] { background: var(--accent); color: var(--on-accent); border-color: var(--accent); }
.tab:not([aria-selected="true"]):hover { background: var(--accent-soft); color: var(--link); border-color: var(--accent); }

/* panels */
.panel { animation: rise .35s cubic-bezier(.4, 0, .2, 1); }
@keyframes rise { from { transform: translateY(6px); } to { transform: none; } }
.section-title { font-family: var(--font-title); font-size: 18px; font-weight: 700; margin-bottom: 14px; }

/* entries: the Policy-work log style, used on every tab */
.log-list { display: flex; flex-direction: column; gap: 12px; }
.log {
  min-width: 0; background: var(--card); border: 1px solid var(--border); border-left: 3px solid var(--border);
  border-radius: var(--radius); padding: 16px 20px; transition: border-color .2s, background-color .3s;
}
.log:hover, .log:focus-within { border-color: var(--accent); border-left-color: var(--accent); }
.log-title { font-family: var(--font-title); font-size: 14px; font-weight: 600; line-height: 1.45; margin-bottom: 8px; text-wrap: balance; overflow-wrap: break-word; }
.log-title a { color: inherit; text-decoration: none; }
.log-title a:hover { color: var(--link); text-decoration: underline; text-underline-offset: 3px; }
.log-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; font-size: 12px; color: var(--muted); }
.log-meta a, .ado-meta a { color: inherit; text-decoration: underline; text-decoration-color: var(--border); text-underline-offset: 2px; }
.log-meta a:hover, .ado-meta a:hover { color: var(--link); text-decoration-color: currentColor; }
.log-desc { font-family: var(--font-body); font-size: 12px; color: var(--muted); line-height: 1.6; padding-top: 8px; }
.tag { padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; white-space: nowrap; background: var(--repl-bg); color: var(--repl-fg); }
.tag.published { background: var(--pub-bg); color: var(--pub-fg); }
.tag.wp { background: var(--wp-bg); color: var(--wp-fg); }
.tag.review { background: var(--rev-bg); color: var(--rev-fg); }
.tag.codes { background: var(--tool-bg); color: var(--tool-fg); }
.tag.replication { background: var(--repl-bg); color: var(--repl-fg); }
.tag.boc { background: var(--boc-bg); color: var(--boc-fg); }
.tag.ecb { background: var(--ecb-bg); color: var(--ecb-fg); }
.tag.dnb { background: var(--dnb-bg); color: var(--dnb-fg); }
.tag.boe { background: var(--boe-bg); color: var(--boe-fg); }
.tag.adb { background: var(--adb-bg); color: var(--adb-fg); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; padding-top: 10px; }
.chip { padding: 2px 10px; border-radius: 20px; font-size: 11.5px; font-weight: 500; border: 1px solid var(--border); background: var(--bg); color: var(--muted); }
.links { display: flex; flex-wrap: wrap; gap: 6px; padding-top: 10px; }
.lnk {
  display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: 20px;
  border: 1px solid var(--border); background: var(--card); color: var(--muted);
  font-size: 11.5px; font-weight: 500; text-decoration: none; transition: all .2s; overflow-wrap: anywhere;
}
.lnk:hover { border-color: var(--accent); color: var(--link); }
.lnk.primary { background: var(--accent-soft); border-color: transparent; color: var(--link); font-weight: 600; }
.lnk.primary:hover { border-color: var(--accent); }
.lnk.gh { background: var(--text); border-color: var(--text); color: var(--card); font-weight: 600; }
.lnk.gh:hover { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }
.lnk svg { width: 13px; height: 13px; fill: currentColor; }
.lnk svg.st { fill: none; }
.prose { display: flex; flex-direction: column; gap: 10px; }
.prose p { font-family: var(--font-body); font-size: 13px; line-height: 1.75; max-width: 70ch; }
.note {
  font-family: var(--font-body); font-size: 12px; line-height: 1.65; color: var(--muted); max-width: 70ch;
  background: var(--bg); border: 1px dashed var(--border); border-radius: 8px; padding: 10px 14px; margin-top: 14px;
}

/* policy: quieter ADO sub-list at the bottom */
.ado { margin-top: 36px; }
.ado-head { margin-bottom: 8px; font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
.ado-list { list-style: none; border: 1px solid var(--border); border-radius: var(--radius); }
.ado-item { display: grid; grid-template-columns: 3.2em minmax(0, 1fr); gap: 2px 12px; padding: 12px 16px; }
.ado-item + .ado-item { border-top: 1px solid var(--border); }
.ado-yr { font-size: 11.5px; color: var(--muted); padding-top: 1px; }
.ado-main { min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.ado-title { font-family: var(--font-title); font-size: 13px; font-weight: 600; line-height: 1.45; }
.ado-meta { font-size: 11.5px; color: var(--muted); }
.ado-boxes { list-style: none; font-size: 11.5px; color: var(--muted); line-height: 1.5; display: flex; flex-direction: column; gap: 1px; }
.ado-boxes .bx { color: var(--text); font-weight: 600; margin-right: 4px; }
.ado .links { padding-top: 4px; }
.ado .lnk { font-size: 11px; padding: 1px 8px; }

/* footer */
.footer {
  text-align: center; font-size: 12px; color: var(--muted);
  padding-block: 32px 28px;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
}

/* responsive */
@media (max-width: 1024px) {
  .layout { grid-template-columns: minmax(0, 1fr); gap: 24px; padding-block: 20px 8px; }
  .sidebar { position: static; }
  .tabs {
    position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5;
    background: var(--bg); border-bottom: 1px solid var(--border); padding-block: 10px; margin-bottom: 20px;
  }
}
@media (max-width: 640px) {
  .layout {
    padding-block: 16px 8px;
    padding-left: max(16px, env(safe-area-inset-left, 0px));
    padding-right: max(16px, env(safe-area-inset-right, 0px));
  }
  .profile-header { gap: 12px; }
  .tab-row { gap: 6px; }
  .tab { padding: 10px 12px; font-size: 13px; }
  .log { padding: 14px 16px; }
}
@media (max-width: 520px) {  /* four tabs no longer fit on one line: two by two, all visible */
  .tab-row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .tab { min-width: 0; white-space: normal; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition-duration: .001ms !important; scroll-behavior: auto !important; }
}
"""

# Tab switching with bare-hash deep links, sticky profile card, day/night switch.
LIST_JS = r"""
(function () {
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* tabs with bare-hash deep links */
  var TABS = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  var IDS = TABS.map(function (t) { return t.getAttribute('data-tab'); });
  function show(id, user) {
    if (IDS.indexOf(id) < 0) id = IDS[0];
    TABS.forEach(function (t) {
      var k = t.getAttribute('data-tab'), on = k === id;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById('panel-' + k).hidden = !on;
    });
    if (user) { try { history.replaceState(null, '', '#' + id); } catch (e) {} }
  }
  TABS.forEach(function (t, i) {
    t.addEventListener('click', function () { show(t.getAttribute('data-tab'), true); });
    t.addEventListener('keydown', function (e) {
      var j = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: TABS.length - 1 }[e.key];
      if (j === undefined) return;
      e.preventDefault();
      var n = TABS[(j + TABS.length) % TABS.length];
      n.focus();
      show(n.getAttribute('data-tab'), true);
    });
  });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-goto]');
    if (!a) return;
    e.preventDefault();
    show(a.getAttribute('data-goto'), true);
    document.querySelector('.tabs').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  });
  show(location.hash.replace(/^#/, ''), false);
  window.addEventListener('hashchange', function () { show(location.hash.replace(/^#/, ''), false); });

  /* sticky profile card: when it is taller than the window, stick by its bottom edge instead */
  var sb = document.querySelector('.sidebar');
  function fitSidebar() {
    if (getComputedStyle(sb).position !== 'sticky') { sb.style.top = ''; return; }
    sb.style.top = Math.min(24, window.innerHeight - sb.offsetHeight - 24) + 'px';
  }
  fitSidebar();
  window.addEventListener('resize', fitSidebar);
  if (window.ResizeObserver) new ResizeObserver(fitSidebar).observe(sb);

  /* day/night switch: sets <html data-theme>, remembered in localStorage; the CSS moves the knob */
  var root = document.documentElement, KEY = '__KEY__', btn = document.getElementById('theme-toggle');
  function sysDark() { return !!(window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches); }
  function eff() { var a = root.getAttribute('data-theme'); return a === 'light' || a === 'dark' ? a : (sysDark() ? 'dark' : 'light'); }
  function paint() {
    var label = eff() === 'dark' ? 'Switch to day theme' : 'Switch to night theme';
    btn.setAttribute('aria-label', label);
    btn.title = label;
  }
  btn.addEventListener('click', function () {
    var n = eff() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', n);
    try { localStorage.setItem(KEY, n); } catch (e) {}
    paint();
  });
  if (window.matchMedia) {
    var m = matchMedia('(prefers-color-scheme: dark)');
    if (m.addEventListener) m.addEventListener('change', paint);
  }
  paint();
})();
"""


def _href(u):
    return f'href="{esc(u)}"' + (' target="_blank" rel="noopener"' if u.startswith(("http://", "https://")) else "")


def _primary(ls):
    return next((l for l in ls if l.get("primary")), ls[0] if ls else None)


def _links(ls, gh_first=False):
    """Link pills; with gh_first, GitHub pills come first and are dark."""
    if not ls:
        return ""
    arr = sorted(ls, key=lambda l: "github.com" not in l["url"]) if gh_first else ls
    out = []
    for l in arr:
        gh = gh_first and "github.com" in l["url"]
        internal = l["url"].startswith("#")
        cls = "lnk" + (" primary" if l.get("primary") else "") + (" gh" if gh else "")
        goto = f' data-goto="{esc(l["url"][1:])}"' if internal else ""
        out.append(f'<a class="{cls}" {_href(l["url"])}{goto}>{ICONS["gh"] if gh else ""}'
                   f'{esc(l["label"])}{ICONS["right"] if internal else ""}</a>')
    return f'<div class="links">{"".join(out)}</div>'


def _log(title, url, tag, tag_cls, year, venue, extra, body, links):
    """One entry: title (linked when url), meta row (tag, year, venue in italics, extra), body, link pills.
    `extra` and `body` are HTML."""
    t = f"<a {_href(url)}>{esc(title)}</a>" if url else esc(title)
    meta = f'<span class="tag {esc(tag_cls)}">{esc(tag)}</span><span>{esc(year)}</span>'
    if venue:
        meta += f"<span><em>{esc(venue)}</em></span>"
    if extra:
        meta += f"<span>{extra}</span>"
    return f'<article class="log"><h3 class="log-title">{t}</h3><div class="log-meta">{meta}</div>{body}{links}</article>'


def _ado_item(p):
    boxes = "".join(f'<li><span class="bx">{esc(s["label"])}</span>{esc(s["title"])}'
                    + (f' ({esc(s["coauthors"])})' if s.get("coauthors") else "") + "</li>"
                    for s in p.get("subs") or [])
    boxes = f'<ul class="ado-boxes">{boxes}</ul>' if boxes else ""
    co = f' · {p["coauthors"]}' if p.get("coauthors") else ""
    return (f'<li class="ado-item"><span class="ado-yr">{esc(p["year"])}</span><div class="ado-main">'
            f'<p class="ado-title">{esc(p["title"])}</p><p class="ado-meta"><em>{esc(p["venue"])}</em>{co}</p>'
            f'{boxes}{_links(p["links"])}</div></li>')


def _panels(content):
    """Inner HTML of the four panels, keyed by tab id. Entries keep content.json order."""
    research = "".join(
        _log(r["title"], (_primary(r["links"]) or {}).get("url"), r["label"], r["status"], r["year"],
             r["venue"] if r["venue"] != r["label"] else "", r["coauthors"], "", _links(r["links"]))
        for r in content["research"])
    main = [p for p in content["policy"] if p["section"] != "ado"]
    ado = [p for p in content["policy"] if p["section"] == "ado"]
    policy = "".join(
        _log(p["title"], None, p["institution"], p["inst_abbr"].lower(), p["year"], p["venue"], p["coauthors"], "",
             _links(p["links"]))
        for p in main)
    ado_html = (f'<section class="ado">'
                f'<h3 class="ado-head">{esc(content["headings"]["ado"])}</h3>'
                f'<ul class="ado-list">{"".join(_ado_item(p) for p in ado)}</ul></section>') if ado else ""
    kind = {"codes": "Codes", "replication": "Replication"}
    codes = []
    for k in content["codes"]:
        body = f'<p class="log-desc">{k["description"]}</p>' if k.get("description") else ""
        if k.get("languages"):
            body += '<div class="chips">' + "".join(f'<span class="chip">{esc(x)}</span>' for x in k["languages"]) + "</div>"
        codes.append(_log(k["title"], (_primary(k["links"]) or {}).get("url"), kind.get(k["kind"], k["kind"]), k["kind"],
                          k["year"], k["venue"], k.get("summary", ""), body, _links(k["links"], gh_first=True)))
    H = content["hetlearn"]
    hp = (H.get("links") or [None])[0] or (
        {"url": H["docs_url"], "label": "Open the documentation"} if H.get("docs_url") else None)
    paras = "".join(f"<p>{x}</p>" for x in H.get("paragraphs") or [])
    het = (f'<article class="log"><h3 class="log-title">{H["summary"]}</h3>'
           + (f'<div class="prose">{paras}</div>' if paras else "")
           + (f'<div class="links"><a class="lnk primary" {_href(hp["url"])}>{esc(hp["label"])}</a></div>' if hp else "")
           + (f'<p class="note">{H["note"]}</p>' if H.get("note") else "") + "</article>")
    return {
        "research": f'<div class="log-list">{research}</div>',
        "policy": f'<div class="log-list">{policy}</div>{ado_html}',
        "codes": f'<div class="log-list">{"".join(codes)}</div>',
        "hetlearn": f'<div class="log-list">{het}</div>',
    }


def render(content):
    p, L = content["profile"], content["profile"]["links"]
    tabs = content["tabs"]
    order = ["research", "policy", "codes", "hetlearn"]
    inner = _panels(content)
    tab_btns = "".join(
        f'<button type="button" class="tab" role="tab" id="tab-{k}" data-tab="{k}" aria-controls="panel-{k}" '
        f'aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else " tabindex=\"-1\""}>{esc(tabs[k])}</button>'
        for i, k in enumerate(order))
    panels = "".join(
        f'<section class="panel" id="panel-{k}" role="tabpanel" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}>'
        f'<h2 class="section-title">{esc(tabs[k])}</h2>{inner[k]}</section>'
        for i, k in enumerate(order))
    bio = "".join(f"<p>{b}</p>" for b in p["bio"])
    emails = "".join(f'<a href="mailto:{esc(e)}">{esc(e)}</a>' for e in p["emails"])
    office = "<br>".join(p["office"])
    ext = 'target="_blank" rel="noopener"'
    social = (
        f'<a href="mailto:{esc(p["emails"][0])}" aria-label="Email" title="Email">{ICONS["mail"]}</a>'
        f'<a href="{esc(L["github"])}" {ext} aria-label="GitHub" title="GitHub">{ICONS["gh"]}</a>'
        f'<a href="{esc(L["scholar"])}" {ext} aria-label="Google Scholar" title="Google Scholar">{ICONS["scholar"]}</a>'
        f'<a href="{esc(L["linkedin"])}" {ext} aria-label="LinkedIn" title="LinkedIn">{ICONS["linkedin"]}</a>'
        f'<a href="{esc(L["cv"])}" {ext} aria-label="CV (PDF)" title="CV (PDF)"><span class="cv">CV</span></a>')
    year = p["updated"].split()[-1]
    parts = p["meta"].split(" · ")
    meta = " ".join(f"<span>{esc(x)}{' ·' if i < len(parts) - 1 else ''}</span>" for i, x in enumerate(parts))
    return f"""{head_html(content)}<style>
/* Layout "list": 320px sticky profile card left, tabs right, every tab one plain list, max 1140px; one column below 1024px */
{theme_css()}{LIST_CSS}
</style>
<noscript><style>.panel[hidden] {{ display: block !important; }} .panel + .panel {{ margin-top: 36px; }} .tabs, .daynight {{ display: none; }}</style></noscript>
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <div class="profile-card">
      <div class="strip"></div>
      <div class="profile-body">
        <div class="profile-header">
          <img class="avatar" src="{esc(p['photo'])}" alt="{esc(p['name'])}" width="64" height="64">
          <div class="who">
            <h1 class="name">{esc(p['name'])}</h1>
            <p class="handle">{esc(p['handle'])}</p>
          </div>
          <button type="button" class="daynight" id="theme-toggle" aria-label="Switch to night theme" title="Switch to night theme"><span class="knob" aria-hidden="true"></span><span class="dn sun">{ICONS['sun']}</span><span class="dn moon">{ICONS['moon']}</span></button>
        </div>
        <p class="meta">{meta}</p>
        <div class="bio">{bio}</div>
        <p class="label">Contact</p>
        <div class="contact">{emails}<p class="office">{office}</p></div>
        <nav class="social" aria-label="Profiles">{social}</nav>
      </div>
    </div>
  </aside>
  <main class="main">
    <div class="tabs"><div class="tab-row" role="tablist" aria-label="Sections">{tab_btns}</div></div>
    {panels}
  </main>
</div>
<footer class="footer">© {esc(year)} {esc(p['name'])} · Last updated {esc(p['updated'])}</footer>
<script>{LIST_JS.replace('__KEY__', THEME_KEY)}</script>
{ANALYTICS}</body>
</html>
"""


def main():
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    page = render(content)
    OUTPUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT}  ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
