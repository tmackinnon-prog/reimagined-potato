# TPGP Generator

A small web app that drafts a **Teacher Professional Growth Plan (TPGP)** for
Alberta teachers. You complete a TQS self-reflection, optionally attach
supporting files and web links, and the app writes a first-draft growth
plan — grounded in Alberta's expectations — and hands it back as a
**Word (.docx)** document in the Third Schools template.

## Workflow

1. **Self-Reflection** – Rate yourself (1–5) on each indicator across the six
   TQS competencies, with optional notes, draft goals, and written
   reflections.
2. **Files & Notes** – Attach supporting files (**PDF, DOCX, DOC, TXT, MD**)
   and add any free-text considerations.
3. **Web Links** – List any URLs to take into account (optional).
4. **Generate** – The app parses everything, drafts the plan with Claude, and
   offers a **Download .docx** button after a live preview.

## Running it

```bash
cd tpgp-generator
pip install -r requirements.txt      # first time only
python app.py
```

Then open <http://127.0.0.1:8200> (the port can be changed with the
`TPGP_PORT` env var). On macOS/Linux you can instead double-click / run
`./start.sh`; on Windows, double-click `start.bat`. Both install
dependencies on first run and open the page for you.

The app binds to all interfaces, so if you run it on a shared machine or
inside a container/VM, it's also reachable at `http://<that machine's
address>:8200` from other devices on the same network — useful for hosting
it somewhere your whole staff can reach, not just `127.0.0.1`.

## API key

The app calls the Claude API and **never stores your key**. Provide it
either way:

- **Recommended:** set it once in your environment — `export
  ANTHROPIC_API_KEY="sk-ant-..."` (or `setx ANTHROPIC_API_KEY "sk-ant-..."`
  on Windows) before starting the app, then leave the field on Step 4
  blank; **or**
- Paste it into the optional field on Step 4 (used only for that single
  request, sent directly to Anthropic, never written to disk).

## How the draft is built to Alberta expectations

The generation prompt embeds guidance synthesized from:

- ATA – [Professional Growth Planning](https://teachers.ab.ca/professional-development/professional-growth-planning)
  and [Develop Your Professional Growth Plan](https://teachers.ab.ca/professional-development/professional-growth-planning/develop-your-professional-growth-plan)
- ATA – [Beginning Teachers](https://teachers.ab.ca/teaching-career/beginning-teachers)
- Government of Alberta – [Professional Practice Standards / TQS](https://www.alberta.ca/professional-practice-standards)
- Alberta Education – [Teacher Growth, Supervision and Evaluation Policy](https://open.alberta.ca/publications/teacher-growth-supervision-and-evaluation-policy)

Each drafted goal is **SMART**, tied to one or more of the **six TQS
competencies**, and includes short-term objectives, strategies,
measures/indicators of success, and resources. The result is a **draft**
for the teacher to review, personalise, and discuss with their
administrator — it is not an evaluation.

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask server: parses inputs, calls Claude, returns the .docx |
| `index.html` | The 4-step wizard front end |
| `docx_builder.py` | Fills the Word template with the generated plan (falls back to building from scratch if the template is missing) |
| `tpgp_template.docx` | The Third Schools TPGP Word template — logos, styles, layout. The generated plan is written into a copy of this file. |
| `tpgp_reference.py` | Embedded TQS competencies + Alberta TPGP drafting guidance |
| `indicators.py` | TQS indicator text (for the reflection summary sent to Claude) |
| `start.sh` / `start.bat` | Convenience launchers that install dependencies and open the app |

## Notes

- Legacy `.doc` files are read via `antiword` if it's on your `PATH`,
  otherwise via a LibreOffice (`soffice`) conversion. If neither is
  available, convert the file to `.docx` or `.pdf` first.
- Files and links are sent only to generate your plan; nothing is
  persisted server-side.
- If a link "could not be read," the plan is still generated from
  everything else — just remove or replace that link.
