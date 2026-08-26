# Advanced Syllabus Generator

A professional, feature-rich course syllabus generator that combines the best capabilities of multiple tools into one unified application.

## 🎯 What It Does

Creates complete, Canvas-ready course syllabi with:
- ✅ Gated workflow with validation (ensures data integrity)
- ✅ Multi-document support (PDF, DOCX, CSV, XLSX)
- ✅ Automatic curriculum extraction (units, outcomes, weights)
- ✅ Intelligent pacing calculation (based on real instructional days)
- ✅ Alberta-specific statutory holidays (auto-included)
- ✅ Professional color-coded formatting
- ✅ Multi-format exports (HTML, DOCX, CSV, ZIP)
- ✅ Week-by-week + day-by-day instructional plans
- ✅ Complete offline capability (no internet required)
- ✅ No installation needed (single HTML file)

## 🚀 Quick Start

### Option A: Direct File Open (Easiest)
1. Navigate to the Advanced Syllabus Generator folder
2. Double-click `index.html`
3. It opens in your default browser
4. **Recommended browsers:** Chrome, Edge, Firefox

### Option B: Local Server (Recommended)
If you encounter issues with local file uploads, use a local server:

```bash
# Python 3
python -m http.server 8080

# Node.js
npx serve .

# PHP
php -S localhost:8080
```

Then open `http://localhost:8080` in your browser.

## 📋 Workflow Overview

The application guides you through **6 phases**:

### Phase 1: Instructor & Course Information
- Instructor name and contact details
- Course title, code, emoji
- Course dates and duration
- Materials and overview
- Office hours

### Phase 2: Document Upload & Parsing
- **Program of Studies** (PDF, DOCX, CSV, XLSX) — extracts units and outcomes
- **School Calendar** (PDF, CSV, XLSX) — detects holidays, breaks, PD days
- **Class Schedule** (PDF, CSV, XLSX) — identifies meeting days and times
- *All uploads are optional* — manual entry fallback available

### Phase 3: Calendar & Class Schedule
- Select meeting days (Monday–Friday)
- Set class start/end times
- Add custom holidays and PD days
- Alberta statutory holidays auto-included

### Phase 4: Curriculum & Grading
- Define course units with percentages and estimated weeks
- Create grade categories
- Set up letter grade scale (A+ through F)
- Enter course policies:
  - Late work policy
  - Attendance requirements
  - Academic integrity expectations
  - Classroom conduct rules
  - AI use policy

### Phase 5: Review & Customize
- Preview your syllabus
- Add optional sections:
  - Learning outcomes & competencies
  - Expectations for success
  - Big idea / essential question
  - Required technology
  - Accessibility & accommodations

### Phase 6: Export
- **HTML** — Canvas-ready (paste directly into Canvas pages)
- **DOCX** — Professional Word document with color-coding
- **CSV** — Pacing guide for spreadsheet planning
- **ZIP** — All formats in one downloadable package

## 🎨 Features Merged from Both Applications

### From *syllabus-generator*
- ✅ Gated workflow with hard-stop validation
- ✅ Advanced document parsing (PDF, XLSX, CSV)
- ✅ Curriculum unit extraction
- ✅ Pacing calculation based on real instructional days
- ✅ CSV exports (pacing + weekly schedule)
- ✅ Weekly instructional plan generation

### From *HTML Syllabus Generator*
- ✅ Simple 5-step guided workflow
- ✅ Professional DOCX export with color-coding
- ✅ Alberta-specific statutory holidays
- ✅ Day-by-day lesson plan support
- ✅ No installation required
- ✅ Fully offline capable
- ✅ Emoji support
- ✅ Color-coded sections

### NEW Features (Unique to This Merged Version)
- ✅ Unified interface combining best of both
- ✅ Multi-format export (HTML + DOCX + CSV + ZIP)
- ✅ Enhanced preview before final generation
- ✅ Complete offline capability
- ✅ Larger, more flexible form sections
- ✅ Better input validation with helpful error messages

## 📥 Document Upload Requirements

### Program of Studies (Optional)
**Best format:** CSV or XLSX
- Columns should include: `Unit`, `Weight`/`Percentage`, `Description`
- Alternative formats: PDF, DOCX (text extraction with heuristics)
- If auto-extraction fails, you can enter units manually

**Example CSV:**
```
Unit,Weight,Description
Cell Biology,25,Structure and function of cells
Genetics,25,Heredity and DNA
Evolution,25,Natural selection and adaptation
Ecology,25,Organisms and their environments
```

### School Calendar (Optional)
**Best format:** CSV or XLSX
- Columns should include: `Date`, `Status`, `Notes`
- Status values: Holiday, PD Day, Break, Instructional
- Alternative format: PDF (with date-based calendar)

**Example CSV:**
```
Date,Status,Notes
2025-09-01,Instructional,
2025-09-02,Holiday,Labor Day
2025-10-13,PD Day,Professional Development
```

### Class Schedule (Optional)
**Best format:** CSV or XLSX
- Columns should include: `Day`, `Start`, `End`
- Days: Monday, Tuesday, Wednesday, Thursday, Friday
- Time format: HH:MM (24-hour)

**Example CSV:**
```
Day,Start,End
Monday,08:00,16:00
Tuesday,08:00,16:00
Wednesday,08:00,16:00
Thursday,08:00,16:00
Friday,08:00,16:00
```

## 💾 Export Formats Explained

### HTML (Canvas-Ready)
- Clean, professional formatting
- Inline CSS (no external stylesheets)
- Can be pasted directly into Canvas
- Responsive and print-friendly
- Preserves all formatting

### DOCX (Word Document)
- Professional color-coded sections
- Table of contents support
- Easy to edit and customize further
- Works with Microsoft Word, Google Docs, LibreOffice
- High-quality typography

### CSV (Pacing Guide)
- Spreadsheet-ready format
- Columns: Unit, Percentage, Weeks, Start Week, End Week
- Import into Excel/Sheets for further planning
- Simple data format for sharing

### ZIP (Complete Package)
- Contains all three formats above
- Organized file structure
- Backup your complete syllabus
- Easy distribution to colleagues

## 🔒 Data Privacy

- **No data is sent anywhere** — everything runs in your browser
- **No internet required** after page loads (except for file uploads)
- **No servers** — your syllabus data never leaves your computer
- **No accounts** — no login required, no tracking
- **Local storage** — all data stored in browser's local storage
- **Offline mode** — works completely without internet

## ⚙️ System Requirements

- **Browser:** Chrome, Edge, Firefox (Safari supported but with limitations)
- **Internet:** Required only for initial page load and file uploads
- **Space:** ~5 MB (fits in browser cache)
- **JavaScript:** Must be enabled

## 🐛 Troubleshooting

### "Files won't upload"
- Use a local server (see Quick Start section)
- Try a different browser (Chrome recommended)
- Ensure files are the correct format (PDF, DOCX, CSV, XLSX)

### "Percentages error when advancing"
- Ensure grade categories total exactly 100%
- Ensure units total exactly 100%
- Use decimal values if needed (e.g., 33.33%)

### "Export not downloading"
- Check your browser's download settings
- Try a different export format
- Clear browser cache and try again

### "Preview is blank"
- Ensure at least one unit is defined
- Check that all required Phase 1 fields are filled
- Reload the page

## 📱 Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Recommended |
| Edge | ✅ Full | Recommended |
| Firefox | ✅ Full | Fully supported |
| Safari | ⚠️ Partial | File downloads may be limited |
| IE 11 | ❌ Not supported | Use modern browser |

## 🔄 Workflow Rules

- **Phase 1:** All marked fields (*) must be filled before advancing
- **Phase 2:** All uploads are optional
- **Phase 3:** At least one meeting day must be selected
- **Phase 4:** 
  - At least one unit required
  - Unit percentages must total 100%
  - Grade categories must total 100%
- **Phase 5:** Preview generates automatically
- **Phase 6:** Export any or all formats

## 📚 Advanced Tips

### Creating Multiple Syllabi
- Each browser tab/window maintains separate state
- Use "Start Over" to begin a new syllabus
- Browser storage persists between sessions

### Customizing Exports
- Export HTML and open in Word for further customization
- Export DOCX and edit freely
- CSV can be imported to Excel/Sheets for complex pacing

### Shared Use in a School
- Colleagues can use the same file independently
- No setup required — just open index.html
- No account conflicts or data sharing

### Integration with Canvas
**To import HTML into Canvas:**
1. Go to Modules → Add Module → Add a Page
2. Click Page title, then HTML Editor
3. Paste the exported HTML
4. Click Save

## 🎓 Perfect For

- 👨‍🏫 Individual instructors creating their own syllabi
- 🏫 Departments standardizing syllabus formats
- 👥 Teachers sharing syllabi templates
- 📋 Curriculum coordinators managing course documents
- 🎯 Online/blended course designers
- 📞 Substitute teachers needing quick reference

## 📄 File Structure

```
Advanced Syllabus Generator/
├── index.html          Main application (single file)
└── README.md          This file
```

That's it! Everything needed is in the HTML file.

## 🚀 Future Enhancement Ideas

- PDF export
- Email syllabus directly
- Templates for different course types
- Shared templates library
- Multi-teacher collaboration
- Canvas API integration for direct import
- Syllabus version history
- Import existing Canvas pages
- AI-assisted policy writing

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Try opening in Chrome or Edge
3. Clear browser cache and reload
4. Try using a local server instead of direct file open

## 📝 Version

**Advanced Syllabus Generator v1.0**

Merges best features from:
- Syllabus & Yearly Plan Generator
- Canvas Syllabus Generator
- New unified capabilities

Last updated: 2024

---

**Created by:** Claude (Teacher Tools Suite)
**License:** Free for educational use
