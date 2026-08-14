# -*- coding: utf-8 -*-
"""
Generates an Alberta Education Individualized Program Plan (IPP) as a fillable
.docx, mirroring the LYNX/ursa IPP template. Uses Word content controls so the
document stays fully editable (no form protection needed):
  - drop-down lists  (reporting period, strengths, areas to improve, goal topics)
  - check boxes      (accommodations, per-goal strategies)
  - plain-text boxes (fillable blanks: name, parent, ASN, address, phones, etc.)
Plus external hyperlinks (DSM-5, Alberta special education coding criteria).
"""
import os, zipfile, html

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- LYNX / ursa brand palette (sampled from the original logos) ------------
C_TEAL   = "003344"   # ursa dark teal  -> section bars, headings
C_ORANGE = "D77B28"   # LYNX orange     -> accent rules, goal band
C_OLIVE  = "999735"   # LYNX olive green
C_CREAM  = "F4D19F"   # LYNX cream
C_LABEL  = "DCE6EA"   # light teal tint -> label / header cells
C_GOAL   = "FBEAD9"   # light orange tint -> goal sentence band
C_GREY   = "595959"

# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
_uid = [1000]
def uid():
    _uid[0] += 1
    return _uid[0]

def esc(s):
    return html.escape(str(s), quote=True)

# collected external hyperlink relationships: rId -> url
RELS = []
def hyperlink_rel(url):
    rid = "rHl%d" % uid()
    RELS.append((rid, url))
    return rid

def run(text="", bold=False, italic=False, size=None, color=None, font=None,
        underline=False):
    rpr = []
    if font:
        rpr.append('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (font, font, font))
    if bold: rpr.append('<w:b/>')
    if italic: rpr.append('<w:i/>')
    if underline: rpr.append('<w:u w:val="single"/>')
    if color: rpr.append('<w:color w:val="%s"/>' % color)
    if size: rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
    rpr_xml = "<w:rPr>%s</w:rPr>" % "".join(rpr) if rpr else ""
    # preserve spaces
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr_xml, esc(text))

def para(inner="", jc=None, shade=None, spacing_after=60, spacing_before=0,
         bold_default=False, size_default=None, keepnext=False):
    ppr = []
    if keepnext: ppr.append('<w:keepNext/>')
    if shade: ppr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    ppr.append('<w:spacing w:before="%d" w:after="%d" w:line="240" w:lineRule="auto"/>' %
               (spacing_before, spacing_after))
    if jc: ppr.append('<w:jc w:val="%s"/>' % jc)
    rpr = []
    if bold_default: rpr.append('<w:b/>')
    if size_default: rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size_default, size_default))
    if rpr: ppr.append('<w:rPr>%s</w:rPr>' % "".join(rpr))
    return '<w:p><w:pPr>%s</w:pPr>%s</w:p>' % ("".join(ppr), inner)

def section_bar(text):
    """Full-width shaded section header bar."""
    return para(run(text, bold=True, size=24, color="FFFFFF"),
                shade=C_TEAL, spacing_before=140, spacing_after=60)

def subheading(text):
    return para(run(text, bold=True, size=22, color=C_TEAL),
                spacing_before=80, spacing_after=40)

def note(text):
    return para(run(text, italic=True, size=18, color=C_GREY), spacing_after=60)

def orange_rule(after=120):
    """Thin orange horizontal rule via a paragraph bottom border."""
    return ('<w:p><w:pPr><w:pBdr>'
            '<w:bottom w:val="single" w:sz="18" w:space="1" w:color="%s"/>'
            '</w:pBdr><w:spacing w:before="0" w:after="%d"/></w:pPr></w:p>'
            % (C_ORANGE, after))

def image_run(rid, w_emu, h_emu, name):
    did = uid()
    return (
        '<w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="%s"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
        % (w_emu, h_emu, did, name, did, name, rid, w_emu, h_emu)
    )

# ---- content controls -------------------------------------------------------
def sdt_text(alias, width_hint=None, placeholder="Click or tap to enter text."):
    i = uid()
    return (
        '<w:sdt><w:sdtPr>'
        '<w:rPr><w:rStyle w:val="PlaceholderText"/></w:rPr>'
        '<w:alias w:val="%s"/><w:tag w:val="%s"/><w:id w:val="%d"/>'
        '<w:placeholder><w:docPart w:val="DefaultPlaceholder_-1854013440"/></w:placeholder>'
        '<w:showingPlcHdr/><w:text/></w:sdtPr>'
        '<w:sdtContent><w:r><w:rPr><w:rStyle w:val="PlaceholderText"/></w:rPr>'
        '<w:t>%s</w:t></w:r></w:sdtContent></w:sdt>'
        % (esc(alias), esc(alias), i, esc(placeholder))
    )

def sdt_dropdown(alias, items, placeholder="Choose an item."):
    i = uid()
    li = ['<w:listItem w:displayText="%s" w:value=""/>' % esc(placeholder)]
    for it in items:
        li.append('<w:listItem w:displayText="%s" w:value="%s"/>' % (esc(it), esc(it)))
    return (
        '<w:sdt><w:sdtPr>'
        '<w:rPr><w:rStyle w:val="PlaceholderText"/></w:rPr>'
        '<w:alias w:val="%s"/><w:tag w:val="%s"/><w:id w:val="%d"/>'
        '<w:placeholder><w:docPart w:val="DefaultPlaceholder_-1854013440"/></w:placeholder>'
        '<w:showingPlcHdr/>'
        '<w:dropDownList>%s</w:dropDownList></w:sdtPr>'
        '<w:sdtContent><w:r><w:rPr><w:rStyle w:val="PlaceholderText"/></w:rPr>'
        '<w:t>%s</w:t></w:r></w:sdtContent></w:sdt>'
        % (esc(alias), esc(alias), i, "".join(li), esc(placeholder))
    )

def sdt_checkbox():
    i = uid()
    return (
        '<w:sdt><w:sdtPr>'
        '<w:rPr><w:rFonts w:ascii="MS Gothic" w:eastAsia="MS Gothic" w:hAnsi="MS Gothic" w:hint="eastAsia"/></w:rPr>'
        '<w:id w:val="%d"/>'
        '<w14:checkbox><w14:checked w14:val="0"/>'
        '<w14:checkedState w14:val="2612" w14:font="MS Gothic"/>'
        '<w14:uncheckedState w14:val="2610" w14:font="MS Gothic"/></w14:checkbox>'
        '</w:sdtPr>'
        '<w:sdtContent><w:r><w:rPr><w:rFonts w:ascii="MS Gothic" w:eastAsia="MS Gothic" w:hAnsi="MS Gothic" w:hint="eastAsia"/></w:rPr>'
        '<w:t>☐</w:t></w:r></w:sdtContent></w:sdt>' % i
    )

def checkbox_line(label):
    inner = sdt_checkbox() + run("  " + label, size=20)
    return para(inner, spacing_after=20)

def hyperlink(url, text):
    rid = hyperlink_rel(url)
    return ('<w:hyperlink r:id="%s"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/>'
            '<w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:hyperlink>'
            % (rid, esc(text)))

# ---- tables -----------------------------------------------------------------
def cell(content_xml, w, shade=None, gridspan=None, valign="top", vmerge=None):
    tcpr = ['<w:tcW w:w="%d" w:type="dxa"/>' % w]
    if gridspan: tcpr.append('<w:gridSpan w:val="%d"/>' % gridspan)
    if vmerge: tcpr.append('<w:vMerge w:val="%s"/>' % vmerge)
    if shade: tcpr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    tcpr.append('<w:vAlign w:val="%s"/>' % valign)
    if not content_xml.strip():
        content_xml = para("")
    return '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % ("".join(tcpr), content_xml)

def row(cells_xml, header=False):
    trpr = '<w:trPr><w:tblHeader/></w:trPr>' if header else ''
    return '<w:tr>%s%s</w:tr>' % (trpr, "".join(cells_xml))

def table(rows_xml, col_widths):
    total = sum(col_widths)
    grid = "".join('<w:gridCol w:w="%d"/>' % w for w in col_widths)
    tblpr = (
        '<w:tblPr>'
        '<w:tblW w:w="%d" w:type="dxa"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '</w:tblBorders>'
        '<w:tblCellMar>'
        '<w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
        '</w:tblCellMar>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
        '</w:tblPr>' % total
    )
    return '<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>%s' % (
        tblpr, grid, "".join(rows_xml), para("", spacing_after=40))

def label_cell(text, w, shade=C_LABEL):
    return cell(para(run(text, bold=True, size=20, color=C_TEAL), spacing_after=20), w, shade=shade)

# ----------------------------------------------------------------------------
# option lists
# ----------------------------------------------------------------------------
PAGE_W = 12240
MARG = 1080
CONTENT_W = PAGE_W - 2 * MARG   # 10080

STRENGTHS = [
    "Curiosity / Love of learning", "Perseverance", "Creativity",
    "Kindness and caring", "Great sense of humour", "Teamwork / Cooperation",
    "Fairness", "Honesty / Integrity", "Leadership", "Zest / Enthusiasm",
    "Social-emotional intelligence", "Interacts well with peers and adults",
    "Strong visual memory", "Strong oral/verbal communication",
    "Hands-on / kinesthetic learner", "Artistic / musical ability",
    "Athletic ability", "Technology skills", "Attention to detail",
    "Resilience", "Self-motivation",
]

AREAS_TO_IMPROVE = [
    "Independence", "Self-Advocacy", "Emotional Regulation",
    "Cognitive Flexibility", "Social Awareness", "Attention / Focus",
    "Organization", "Time Management", "Reading Comprehension",
    "Written Expression", "Numeracy", "Working Memory", "Task Initiation",
    "Impulse Control", "Frustration Tolerance", "Fine Motor Skills",
    "Peer Relationships",
]

GOAL_TOPICS = [
    "Numeracy", "Literacy", "Time-Management", "Self-Advocacy",
    "Best Work", "Organization", "Attention", "Emotional Regulation",
]

# online synchronous strategies
STRATEGIES = [
    "Frequent teacher check-ins / 1:1 breakout support",
    "Chunk tasks into smaller steps",
    "Visual schedule / agenda shared on screen",
    "Screen-share exemplars and models",
    "Use the chat feature to ask questions",
    "Scheduled movement / brain breaks",
    "Digital graphic organizers",
    "Text-to-speech / speech-to-text tools",
    "Extended time on tasks and assessments",
    "Frequent, specific positive feedback / praise",
    "Recorded lessons available for review",
    "On-screen visual timer",
    "Guided practice (model, then do)",
    "Shared collaborative documents",
    "Pin / spotlight teacher for focus",
    "Sentence starters and writing frames",
    "Virtual manipulatives",
    "Choice of alternate quiet workspace",
    "Checklists shared digitally",
    "Option to work in an alternate space or take a break",
]

ACCOMMODATIONS = [
    "Avoid timed tasks", "Break assignments into shorter tasks",
    "Concrete examples", "Exemplars", "Extra time", "Extra assessment time",
    "Flexible deadlines", "Preferential seating / pinned view",
    "Reduced workload / fewer questions", "Use of assistive technology",
    "Text-to-speech / audiobooks", "Speech-to-text software",
    "Frequent breaks", "Chunking of information",
    "Visual aids / graphic organizers", "Access to a reader or scribe",
    "Alternate setting for assessments", "Use of a calculator",
    "Digital or recorded notes", "Movement breaks",
    "Checklists and visual agendas", "Reduced visual / auditory distractions",
    "Verbal and written instructions", "Advance notice of changes to routine",
]

DELIVERY = ["Whole class", "Small group", "Individual"]

# external links
URL_DSM = "https://ia800707.us.archive.org/15/items/info_munsha_DSM5/DSM-5.pdf"
URL_CODES = "https://open.alberta.ca/dataset/ee2ccea8-97fe-41a1-aa11-ed9f21421364/resource/2f1b4aea-bb14-4ce5-bdc7-abca6bd03da8/download/ecc-special-education-coding-criteria-2026-2027.pdf"
URL_INCLUSIVE = "https://www.alberta.ca/inclusive-education"

# ----------------------------------------------------------------------------
# build body
# ----------------------------------------------------------------------------
body = []
A = body.append

# ---- Title block (letterhead: LYNX logo | title | ursa logo) ----
LYNX_CX, LYNX_CY = 531266, 640080     # 0.70" tall
URSA_CX, URSA_CY = 797384, 548640     # 0.60" tall
hc1, hc3 = 2200, 2200
hc2 = CONTENT_W - hc1 - hc3
title_center = (
    para(run("Individualized Program Plan", bold=True, size=40, color=C_TEAL),
         jc="center", spacing_after=20) +
    para(run("LYNX / ursa", bold=True, size=24, color=C_ORANGE) +
         run("     •     2025–2026", size=22, color=C_GREY), jc="center", spacing_after=20) +
    para(run("Alberta Education – Special Education / Inclusive Education", italic=True,
         size=18, color=C_GREY), jc="center", spacing_after=0))
header_tbl = (
    '<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/>'
    '<w:tblBorders>'
    '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '</w:tblBorders>'
    '<w:tblLook w:val="0000" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="1" w:noVBand="1"/>'
    '</w:tblPr>'
    '<w:tblGrid><w:gridCol w:w="%d"/><w:gridCol w:w="%d"/><w:gridCol w:w="%d"/></w:tblGrid>'
    '<w:tr>%s%s%s</w:tr></w:tbl>' % (
        CONTENT_W, hc1, hc2, hc3,
        cell(para(image_run("rIdLynx", LYNX_CX, LYNX_CY, "LYNX logo"), jc="left", spacing_after=0), hc1, valign="center"),
        cell(title_center, hc2, valign="center"),
        cell(para(image_run("rIdUrsa", URSA_CX, URSA_CY, "ursa logo"), jc="right", spacing_after=0), hc3, valign="center"),
    )
)
A(header_tbl)
A(orange_rule(after=120))

# ---- Reporting period ----
rp_inner = (run("Reporting Period:   ", bold=True, size=22, color=C_TEAL) +
            sdt_dropdown("Reporting Period", ["1", "2", "3"], "Select 1, 2 or 3") +
            run("        Date Updated:  ", bold=True, size=22, color=C_TEAL) +
            sdt_text("Date Updated", placeholder="M/D/Y"))
A(para(rp_inner, shade=C_LABEL, spacing_before=60, spacing_after=60))
A(note("Reporting Period 1 = fall (baseline)   •   Reporting Period 2 = winter/March review   •   "
       "Reporting Period 3 = spring/June review."))
A(note("For Reporting Periods 2 and 3: open the student’s previous IPP, then copy each prior "
       "objective, strategy and result into the matching November / March / June cell below so the "
       "plan collates the full year in one document before you add the new review."))

# ---- Student Information ----
A(section_bar("Student Information"))
w1, w2 = 3600, CONTENT_W - 3600
def info_row(lbl, alias, ph="Click or tap to enter text."):
    return row([label_cell(lbl, w1),
                cell(para(sdt_text(alias, placeholder=ph)), w2)])
si_rows = [
    info_row("Student Name (first, last):", "Student Name"),
    info_row("Date of Birth (M/D/Y):", "Date of Birth", "M/D/Y"),
    info_row("Alberta Education ID # (ASN):", "ASN", "9-digit ASN"),
    info_row("Gender:", "Gender"),
    info_row("Grade / Learning Group:", "Grade/Learning Group"),
    info_row("Parent(s) / Guardian(s):", "Parent/Guardian"),
    info_row("Address (#, street, suite or apt.):", "Address Line 1"),
    info_row("Address (city, province, postal code):", "Address Line 2"),
    info_row("Telephone – Home:", "Telephone Home", "___-___-____"),
    info_row("Telephone – Cell (father):", "Telephone Cell Father", "___-___-____"),
    info_row("Telephone – Cell (mother):", "Telephone Cell Mother", "___-___-____"),
    info_row("Email (student):", "Email Student"),
    info_row("Email (father):", "Email Father"),
    info_row("Email (mother):", "Email Mother"),
    info_row("Alberta Education Code:", "Alberta Education Code"),
]
A(table(si_rows, [w1, w2]))
A(note("Alberta Education coding criteria (mild/moderate, severe, gifted and talented): ") )
A(para(hyperlink(URL_CODES, "ECS to Grade 12 Special Education Coding Criteria 2026/2027 (open.alberta.ca)"),
       spacing_after=40))
A(para(hyperlink(URL_INCLUSIVE, "Alberta Inclusive Education – program planning guidance (alberta.ca)"),
       spacing_after=80))

# ---- Relevant Medical Information ----
A(section_bar("Relevant Medical Information"))
A(table([
    row([label_cell("Relevant Medical Information", w1),
         cell(para(sdt_text("Relevant Medical Information")), w2)]),
    row([label_cell("Medications", w1),
         cell(para(sdt_text("Medications")), w2)]),
], [w1, w2]))

# ---- Current Services Provided ----
A(section_bar("Current Services Provided"))
cw1, cw2, cw3 = 3400, 3340, CONTENT_W - 3400 - 3340
def service_row(service):
    return row([
        cell(para(run(service, size=20)), cw1),
        cell(para(sdt_text("Individual Responsible")), cw2),
        cell(para(sdt_dropdown("Delivery", DELIVERY, "Whole class / Small group / Individual")), cw3),
    ])
A(table([
    row([label_cell("Service", cw1), label_cell("Individual Responsible", cw2),
         label_cell("Delivery", cw3)], header=True),
    service_row("Lead Teacher / IPP (1:4)"),
    service_row("Classroom Teachers (1:20)"),
    service_row("Therapeutic Services"),
    service_row("OT / SLP Services"),
], [cw1, cw2, cw3]))

# ---- School History ----
A(section_bar("School History"))
sh1 = CONTENT_W // 2
sh2 = CONTENT_W - sh1
sh_rows = [row([label_cell("School Attended", sh1), label_cell("Year(s) Attended", sh2)], header=True)]
for _ in range(4):
    sh_rows.append(row([cell(para(sdt_text("School Attended")), sh1),
                        cell(para(sdt_text("Year Attended")), sh2)]))
A(table(sh_rows, [sh1, sh2]))

# ---- Family History ----
A(section_bar("Family History"))
A(para(sdt_text("Family History", placeholder="Describe the student’s family / living situation."),
       spacing_after=80))

# ---- Additional Information ----
A(section_bar("Additional Information"))
A(para(sdt_text("Additional Information"), spacing_after=80))

# ---- Professional / Psychoeducational Assessment ----
A(section_bar("Professional (Psychoeducational) Assessment"))
A(note("When recording a psychoeducational assessment, cross-reference the diagnosis and the "
       "Alberta Education special education code using the sources below."))
A(para(run("•  ", size=20) + hyperlink(URL_DSM, "DSM-5 – Diagnostic and Statistical Manual of Mental Disorders (PDF)"),
       spacing_after=20))
A(para(run("•  ", size=20) + hyperlink(URL_CODES, "Alberta Education Special Education Coding Criteria 2026/2027 (PDF)"),
       spacing_after=60))
pa1, pa2, pa3 = 2200, 3200, CONTENT_W - 2200 - 3200
pa_rows = [row([label_cell("Date", pa1), label_cell("Test / Assessor", pa2),
                label_cell("Results / Diagnosis & Alberta Code", pa3)], header=True)]
for _ in range(3):
    pa_rows.append(row([cell(para(sdt_text("Date")), pa1),
                        cell(para(sdt_text("Test / Assessor")), pa2),
                        cell(para(sdt_text("Results / Diagnosis")), pa3)]))
A(table(pa_rows, [pa1, pa2, pa3]))

# ---- Assessed Performance Level ----
A(section_bar("Assessed Performance Level"))
A(note("Example: teacher observation, interview, informal & formal testing."))
al1, al2, al3, al4 = 2200, 3080, 2400, CONTENT_W - 2200 - 3080 - 2400
al_rows = [row([label_cell("Date Given", al1), label_cell("Test", al2),
                label_cell("2025 Results", al3), label_cell("2026 Results", al4)], header=True)]
for _ in range(3):
    al_rows.append(row([cell(para(sdt_text("Date Given")), al1),
                        cell(para(sdt_text("Test")), al2),
                        cell(para(sdt_text("2025 Results")), al3),
                        cell(para(sdt_text("2026 Results")), al4)]))
A(table(al_rows, [al1, al2, al3, al4]))

# ---- Summary of Assessed Educational Performance ----
A(section_bar("Summary of Assessed Educational Performance"))
A(para(sdt_text("Summary of Assessed Educational Performance"), spacing_after=80))

# ---- Identified Student Academic & Personal Areas ----
A(section_bar("Identified Student Academic & Personal Areas"))
A(note("Select from the drop-down menus. Areas of strength are drawn from a strengths-based "
       "approach to supporting struggling learners (Gemm Learning)."))
half = CONTENT_W // 2
ia_rows = [row([label_cell("Areas of Strength", half), label_cell("Areas to Improve", half)], header=True)]
for _ in range(5):
    ia_rows.append(row([
        cell(para(sdt_dropdown("Area of Strength", STRENGTHS)), half),
        cell(para(sdt_dropdown("Area to Improve", AREAS_TO_IMPROVE)), half),
    ]))
A(table(ia_rows, [half, half]))

# ---- Required Classroom Accommodations ----
A(section_bar("Required Classroom Accommodations"))
A(note("Changes to instructional and evaluative strategies, materials and resources, facilities "
       "or equipment. Check all that apply."))
# two-column checkbox layout via a borderless-ish table
col = CONTENT_W // 2
mid = (len(ACCOMMODATIONS) + 1) // 2
left = ACCOMMODATIONS[:mid]
right = ACCOMMODATIONS[mid:]
acc_rows = []
for i in range(mid):
    lc = checkbox_line(left[i])
    rc = checkbox_line(right[i]) if i < len(right) else para("")
    acc_rows.append(row([cell(lc, col), cell(rc, col)]))
A(table(acc_rows, [col, col]))
A(para(run("Other: ", bold=True, size=20) + sdt_text("Other Accommodation"), spacing_after=80))

# ---- Long Term Goals ----
def goal_block(n):
    out = []
    out.append(section_bar("Long Term Goal #%d" % n))
    goal_sentence = (
        run("By ", size=22, bold=True) + sdt_text("Goal %d - By (date)" % n, placeholder="date") +
        run(", ", size=22) + sdt_text("Goal %d - Student" % n, placeholder="student") +
        run(" will ", size=22) +
        sdt_dropdown("Goal %d - Topic" % n, GOAL_TOPICS, "goal topic") +
        run(" ", size=22) + sdt_text("Goal %d - Detail" % n, placeholder="describe the observable behaviour") +
        run(" ", size=22) +
        run("out of five instances as observed by teacher.", size=22, bold=True))
    out.append(para(goal_sentence, shade=C_GOAL, spacing_before=40, spacing_after=80))

    # per-goal strategies checklist (online synchronous) — two columns, once per goal
    out.append(para(run("Strategies (online synchronous – check all that apply):",
                        bold=True, size=20, color=C_TEAL), spacing_before=40, spacing_after=20))
    scol = CONTENT_W // 2
    smid = (len(STRATEGIES) + 1) // 2
    sL, sR = STRATEGIES[:smid], STRATEGIES[smid:]
    srows = []
    for i in range(smid):
        lc = checkbox_line(sL[i])
        rc = checkbox_line(sR[i]) if i < len(sR) else para("")
        srows.append(row([cell(lc, scol), cell(rc, scol)]))
    out.append(table(srows, [scol, scol]))

    # objectives table (Short Term Objectives / Assessment Procedure / Review Comments)
    o1, o2, o3 = 4600, 2740, CONTENT_W - 4600 - 2740
    hdr = row([label_cell("Short Term Objectives", o1),
               label_cell("Assessment Procedure", o2),
               label_cell("Review Comments", o3)], header=True)
    def obj_row(period):
        return row([
            cell(para(run(period, bold=True, size=20) + sdt_text("%s objective" % period,
                     placeholder="objective")), o1),
            cell(para(sdt_text("Assessment Procedure")), o2),
            cell(para(sdt_text("Review Comments")), o3),
        ])
    out.append(table([hdr, obj_row("By Nov 2025,"), obj_row("By March 2026,"),
                      obj_row("By June 2026,")], [o1, o2, o3]))
    return "".join(out)

for n in (1, 2, 3):
    A(goal_block(n))

# ---- Subject-area goals ----
def subject_goal(title):
    out = [subheading(title)]
    out.append(para(run("Long Term Goal:  ", bold=True, size=20) +
                    sdt_text("%s - Long Term Goal" % title), spacing_after=40))
    sg1 = CONTENT_W // 3
    sg_rows = [
        row([label_cell("November", sg1), label_cell("March", sg1), label_cell("June", CONTENT_W - 2*sg1)], header=True),
        row([cell(para(sdt_text("%s November" % title)), sg1),
             cell(para(sdt_text("%s March" % title)), sg1),
             cell(para(sdt_text("%s June" % title)), CONTENT_W - 2*sg1)]),
    ]
    out.append(table(sg_rows, [sg1, sg1, CONTENT_W - 2*sg1]))
    return "".join(out)

A(section_bar("Subject-Area & Service Goals"))
for t in ("Literacy", "Numeracy", "Therapeutic Services", "OT / SLP Services"):
    A(subject_goal(t))

# ---- Annual Review & Recommendations ----
A(section_bar("Annual Review & Recommendations"))
def review_row(lbl):
    return row([label_cell(lbl, 3600), cell(para(sdt_text(lbl)), CONTENT_W - 3600)])
A(table([
    review_row("Goals Achieved"),
    review_row("Strategies That Worked Well"),
    review_row("Goals Requiring Ongoing Focus"),
    review_row("Support Services Required"),
], [3600, CONTENT_W - 3600]))

# ---- Transition Plan ----
A(section_bar("Transition Plan"))
def transition(lbl, default):
    return (para(run(lbl, bold=True, size=20), spacing_after=20) +
            para(run(default, size=18, color=C_GREY), spacing_after=20) +
            para(sdt_text(lbl + " notes", placeholder="Add student-specific notes."), spacing_after=80))
A(transition("Transition In:",
   "Registration process, review school file, interview parents, observe student in classroom, "
   "conference with previous school teacher / other professionals, School Based Team to meet, "
   "develop IPP, further parental input."))
A(transition("Transition to Next Grade:",
   "School Based Team to review: IPP; pre & post testing, parent input, new professional assessments, "
   "ongoing implications of diagnosed disorders on ability to learn, review successful "
   "strategies / accommodations / supports, review IPP goals. School Based Team to make programming "
   "recommendations to parents."))
A(transition("Transition to Local School:",
   "Meet with new teacher / other professionals as requested to discuss successful strategies / "
   "accommodations / supports; discuss transition with parents / student; provide ongoing "
   "support / advocacy to student / family as student reintegrates."))

# ---- Signatures ----
A(section_bar("Signature of IPP Team Members"))
A(note("A signature indicates that you understand the IPP."))
g1, g2, g3, g4, g5 = 2400, 2600, CONTENT_W-2400-2600-1520-1520, 1520, 1520
g3 = CONTENT_W - 2400 - 2600 - 1520 - 1520
sig_rows = [row([label_cell("Role / Name", g1), label_cell("Signature", g2),
                 label_cell("Review Date 1", g3), label_cell("Review Date 2", g4),
                 label_cell("Review Date 3", g5)], header=True)]
for role in ("Parent / Guardian", "Principal", "Teacher", "Instructional Assistant",
             "Registered Psychologist", "OT / SLP"):
    sig_rows.append(row([
        cell(para(run(role, size=20) + run("  ", size=20) + sdt_text("Name")), g1),
        cell(para(sdt_text("Signature")), g2),
        cell(para(sdt_text("Date 1")), g3),
        cell(para(sdt_text("Date 2")), g4),
        cell(para(sdt_text("Date 3")), g5),
    ]))
A(table(sig_rows, [g1, g2, g3, g4, g5]))

BODY_XML = "".join(body)

# ---- section properties (with header ref) ----
SECTPR = (
    '<w:sectPr>'
    '<w:headerReference w:type="default" r:id="rIdHeader"/>'
    '<w:footerReference w:type="default" r:id="rIdFooter"/>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
    'w:header="720" w:footer="720" w:gutter="0"/>'
    '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/>'
    '</w:sectPr>'
)

DOCUMENT = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'mc:Ignorable="w14">'
    '<w:body>%s%s</w:body></w:document>' % (BODY_XML, SECTPR)
)

# ----------------------------------------------------------------------------
# other package parts
# ----------------------------------------------------------------------------
HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    + para(
        run("Term: ", bold=True, size=16) + sdt_text("Term", placeholder="1/2/3") +
        run("    ASN: ", bold=True, size=16) + sdt_text("ASN Header", placeholder="ASN") +
        run("    Student: ", bold=True, size=16) + sdt_text("Student Name Header", placeholder="name") +
        run("    Student #: ", bold=True, size=16) + sdt_text("Student Number", placeholder="#"),
        spacing_after=0)
    + '</w:hdr>'
)

FOOTER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
    '<w:r><w:rPr><w:sz w:val="16"/><w:color w:val="808080"/></w:rPr>'
    '<w:t xml:space="preserve">Individualized Program Plan – Page </w:t></w:r>'
    '<w:r><w:rPr><w:sz w:val="16"/><w:color w:val="808080"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
    '<w:r><w:rPr><w:sz w:val="16"/><w:color w:val="808080"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
    '<w:r><w:rPr><w:sz w:val="16"/><w:color w:val="808080"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
    '</w:p></w:ftr>'
)

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:uiPriority w:val="99"/><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="PlaceholderText"><w:name w:val="Placeholder Text"/><w:basedOn w:val="DefaultParagraphFont"/><w:uiPriority w:val="99"/><w:semiHidden/><w:rPr><w:color w:val="808080"/></w:rPr></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>'''

SETTINGS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:defaultTabStop w:val="720"/>
<w:characterSpacingControl w:val="doNotCompress"/>
<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>
</w:settings>'''

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

RELS_ROOT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

# document rels: styles, settings, header, footer + external hyperlinks
doc_rel_items = [
    '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
    '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
    '<Relationship Id="rIdHeader" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>',
    '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>',
    '<Relationship Id="rIdLynx" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/lynx.png"/>',
    '<Relationship Id="rIdUrsa" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/ursa.png"/>',
]
for rid, url in RELS:
    doc_rel_items.append(
        '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="%s" TargetMode="External"/>'
        % (rid, esc(url)))
DOC_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(doc_rel_items) + '</Relationships>')

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>Individualized Program Plan (IPP)</dc:title>
<dc:subject>Alberta Education Special Education / Inclusive Education</dc:subject>
<dc:creator>Teacher</dc:creator>
<cp:keywords>IPP; Alberta Education; Special Education; Inclusive Education</cp:keywords>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
<Application>Microsoft Office Word</Application>
<Company>LYNX / ursa</Company>
</Properties>'''

# ----------------------------------------------------------------------------
# zip it
# ----------------------------------------------------------------------------
out_path = os.path.join(OUT_DIR, "IPP_Template_2025-2026.docx")
parts = {
    "[Content_Types].xml": CONTENT_TYPES,
    "_rels/.rels": RELS_ROOT,
    "word/document.xml": DOCUMENT,
    "word/_rels/document.xml.rels": DOC_RELS,
    "word/styles.xml": STYLES,
    "word/settings.xml": SETTINGS,
    "word/header1.xml": HEADER,
    "word/footer1.xml": FOOTER,
    "docProps/core.xml": CORE,
    "docProps/app.xml": APP,
}
media = {
    "word/media/lynx.png": open(os.path.join(OUT_DIR, "lynx.png"), "rb").read(),
    "word/media/ursa.png": open(os.path.join(OUT_DIR, "ursa.png"), "rb").read(),
}
if os.path.exists(out_path):
    os.remove(out_path)
with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
    # content types first
    z.writestr("[Content_Types].xml", parts.pop("[Content_Types].xml"))
    for name, data in parts.items():
        z.writestr(name, data)
    for name, data in media.items():
        z.writestr(name, data)
print("wrote", out_path)
