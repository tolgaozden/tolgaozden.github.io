# Deploying the new site

Files in this folder replace the old Start Bootstrap template.

1. In your repository, delete the old build files you no longer need:
   `css/`, `js/`, `scss/`, `vendor/`, `gulpfile.js`, `package.json`,
   `package-lock.json`, `.travis.yml`, `handler.php`, and the old `index.html`.
2. Keep `CNAME`, `img/` (your photo at `img/tolga.jpg`) and `doc/` (CV and PDFs).
3. Copy everything from this folder into the repository root:
   `index.html`, `research.html`, `contact.html`, `css/style.css`.
4. Commit and push to `master`. GitHub Pages will serve it at tolgaozden.net within a minute or two.

Editing later:
- Colours and fonts live at the top of `css/style.css`.
- The sidebar is repeated in each HTML file; if you change a link, change it in all five.
- To add a paper, copy one `<div class="card">…</div>` block in `research.html`.
  Tag classes: `published`, `wp` (working/policy paper), `review` (under review).
