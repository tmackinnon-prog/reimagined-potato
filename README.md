# reimagined-potato
just practicing

## Apps

- `index.html` — student matching card game
- `essay-feedback/` — **Essay Feedback Builder** for Alberta ELA and Social Studies
  (10/20/30, -1 and -2 streams). Pick subject → course → assignment, score each
  rubric criterion with descriptor dropdowns, choose matched feedback comments,
  and get a shareable summary with weighted scores. Open
  `essay-feedback/index.html` in any browser — no install needed.
- `tpgp-generator/` — **TPGP Generator**, a small Flask web app for Alberta
  teachers. Complete a Teaching Quality Standard self-reflection, optionally
  attach supporting files/links, and it drafts a Teacher Professional Growth
  Plan with Claude and hands it back as a Word document. Needs a Python
  backend (to call the Claude API and fill the Word template) — see
  `tpgp-generator/README.md` to run it.
- `advanced-syllabus-generator/` — **Advanced Syllabus Generator**, a guided
  6-phase wizard for building Canvas-ready course syllabi (instructor info,
  document upload/parsing, calendar & Alberta statutory holidays,
  curriculum & grading, review, and export to HTML/DOCX/CSV/ZIP). Fully
  offline and client-side — open `advanced-syllabus-generator/index.html` in
  any browser. See `advanced-syllabus-generator/README.md` and
  `User_Guide.html` for details.
