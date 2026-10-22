# tolgaozden.net

One generated page, `index.html`, plus redirect stubs at the old page URLs. Plain static files on
GitHub Pages (`.nojekyll`, `CNAME`). Push to master and the live site updates within a minute or two.

## Update content

1. Edit `src/content.json`. Entries appear in file order. A `policy` entry with `"section": "ado"` goes
   to the Asian Development Outlook list at the foot of the Policy work tab.
2. Run `python -I src/build_site.py` (standard library only; any working directory).
3. Commit `src/content.json` and `index.html` together.

`index.html` is generated, so hand edits to it are lost on the next build. The docstring of
`src/build_site.py` lists the fields that hold HTML (escape `&` and `<` there).

## Colors and fonts

- `DAY` (Violet) and `NIGHT` (Night) dicts at the top of `src/build_site.py`, one CSS custom property
  per key (`accent_soft` becomes `--accent-soft`). The page follows the system setting; the switch in the
  profile card overrides it and the browser remembers the choice.
- `FONTS` and `GOOGLE_FONTS` just below them (Source Code Pro from Google Fonts).
- Layout and spacing: `LIST_CSS` in the same file.

## Tab deep links

| Tab | Link |
|---|---|
| Research | `index.html#research` |
| Policy work | `index.html#policy` |
| Codes | `index.html#codes` |
| HetLearn Toolbox | `index.html#hetlearn` |

## Redirect stubs

| Old page | Redirects to |
|---|---|
| `research.html` | `index.html#research` (`research.html#policy` goes to `#policy`) |
| `policy.html` | `index.html#policy` |
| `code.html` | `index.html#codes` |
| `hetlearn.html` | `index.html#hetlearn` |
| `contact.html` | `index.html` (contact details are in the profile card) |

Each stub redirects by script and by meta refresh, carries a canonical link and shows one fallback
link. They hold no content.

## Files

- `index.html` (generated), the five redirect stubs, `src/` (content and builder).
- `img/tolga.jpg` (photo) and `doc/CV_tolga.pdf` (CV), linked from the page; `doc/ozdenwouters2020_draft.pdf`
  is the paper draft linked from the Research tab.
- Kept although the page does not link them, because outside pages may: the older paper drafts and the BLE
  online appendix in `doc/`, `CV_pic.jpg`, `img/CV_pic.jpg` and `img/partywizard.gif`.
- `CNAME` (custom domain) and `.nojekyll` (serve files as they are).

The Start Bootstrap template files (`vendor/`, `scss/`, `js/`, npm and gulp build files) were removed on
22 October 2026.

Restructured on 22 October 2026 from six hand-written pages into one generated page.
