# tolgaozden.net

Plain HTML and one stylesheet (`css/style.css`); no build step.

Push to master; GitHub Pages serves tolgaozden.net within a minute or two.

Editing later:
- Colors and fonts live at the top of `css/style.css`. The root `style.css` is a stale copy that no page uses.
- Six pages: `index.html`, `research.html`, `policy.html`, `code.html` (nav label "Codes"),
  `hetlearn.html` (nav label "HetLearn Toolbox"), `contact.html`.
- The sidebar is repeated in all six; if you change a link, change it in every page and move `class="on"` to the page's own link.
- `research.html` holds research only. `policy.html` holds policy work, with the ADO items in their own
  "Asian Development Outlook" section at the bottom. `research.html` redirects `#policy` to `policy.html` so old links keep working.
- `code.html` lists scenario codes and replication packages in one list; `hetlearn.html` describes the HetLearn Toolbox and links to its documentation.
- To add an item, copy one `<div class="card">…</div>` block into the right page or section.
  Tag classes: `published`, `wp` (working/policy paper), `review` (under review), `code` (code collection), `repl` (replication package).
  For boxes or other sub-contributions, add a `<ul class="subs"><li>…</li></ul>` inside the card; for a one-line description, add `<p class="d">…</p>`.
