"""Alberta TQS competency metadata and TPGP drafting guidance.

This is the grounding text embedded in the generation prompt so the app
does not depend on live access to ata.ab.ca / alberta.ca at generation
time. Synthesized from:

- ATA - Professional Growth Planning
  https://teachers.ab.ca/professional-development/professional-growth-planning
- ATA - Develop Your Professional Growth Plan
  https://teachers.ab.ca/professional-development/professional-growth-planning/develop-your-professional-growth-plan
- ATA - Beginning Teachers
  https://teachers.ab.ca/teaching-career/beginning-teachers
- Government of Alberta - Professional Practice Standards / Teaching Quality Standard
  https://www.alberta.ca/professional-practice-standards
- Alberta Education - Teacher Growth, Supervision and Evaluation Policy
  https://open.alberta.ca/publications/teacher-growth-supervision-and-evaluation-policy
"""

COMPETENCIES = {
    1: {
        "title": "Fostering Effective Relationships",
        "statement": "A teacher builds positive and productive relationships with students, "
                      "parents/guardians, peers and others in the school and local community to "
                      "support student learning.",
    },
    2: {
        "title": "Engaging in Career-Long Learning",
        "statement": "A teacher engages in career-long professional learning and ongoing "
                      "critical reflection to improve teaching and learning.",
    },
    3: {
        "title": "Demonstrating a Professional Body of Knowledge",
        "statement": "A teacher applies a current and comprehensive repertoire of effective "
                      "planning, instruction and assessment practices to meet the learning "
                      "needs of every student.",
    },
    4: {
        "title": "Establishing Inclusive Learning Environments",
        "statement": "A teacher establishes, promotes and sustains inclusive learning "
                      "environments where diversity is embraced and every student is welcomed, "
                      "cared for, respected and safe.",
    },
    5: {
        "title": "Applying Foundational Knowledge about First Nations, Métis and Inuit",
        "statement": "A teacher develops and applies foundational knowledge about First "
                      "Nations, Métis and Inuit for the benefit of all students.",
    },
    6: {
        "title": "Adhering to Legal Frameworks and Policies",
        "statement": "A teacher demonstrates an understanding of and adherence to the legal "
                      "frameworks and policies that provide the foundations for the Alberta "
                      "education system.",
    },
}

TPGP_GUIDANCE = """
ALBERTA CONTEXT YOU MUST GROUND THIS DRAFT IN

Governing framework: the Teaching Quality Standard (Ministerial Order #001/2020,
amended 2023) and the Teacher Growth, Supervision and Evaluation Policy. A
Teacher Professional Growth Plan (TPGP) is a career-long, self-directed
professional learning tool, developed by the teacher (often in consultation
with a principal), NOT an evaluation instrument. Tone must always be
growth-oriented, professional, and written in first person ("I will...").

What makes a strong TPGP goal, per ATA guidance:
- Each goal is tied to one or more of the six TQS competencies below, chosen
  based on the teacher's own reflection - especially their lower self-ratings
  and stated areas to strengthen, not just their existing strengths.
- Each goal is SMART: Specific, Measurable, Achievable, Relevant, and
  Time-bound within the school year.
- Each goal includes: a short descriptive title, the competencies of focus,
  a timeframe (ending by June of the school year), 2-4 short-term objectives
  (concrete, observable changes in practice), 2-4 strategies/actions the
  teacher will take to get there, 2-3 measures or indicators of success
  (how the teacher will know the goal was met - artifacts, data, feedback),
  and 2-3 realistic resources or supports (people, PD, materials) that would
  help.
- Goals should read as though written by the teacher themselves, in their
  own voice, reflecting their actual subjects/grades, school context, and
  the evidence and priorities they shared - not generic boilerplate.
- Where the teacher's self-reflection, files, or notes mention specific
  students, curricula, FNMI content, technology/AI use, assessment
  practices, or school/division priorities, weave that specificity in.
- If the teacher supplied draft goals of their own, build on and refine
  them rather than replacing them outright, unless they are incomplete.
- Do not fabricate specific data, names, or achievements the teacher did
  not provide. Where evidence is thin, keep the goal appropriately general
  rather than inventing specifics.

The six TQS competencies (for reference - do not repeat their full text
back verbatim in every goal, just target the right ones):
""" + "\n".join(
    f"{n}. {c['title']} - {c['statement']}" for n, c in COMPETENCIES.items()
) + """

Output discipline:
- Produce a draft, not a finished document - it will be reviewed and
  personalised by the teacher before being discussed with their
  administrator.
- Keep objectives/strategies/measures/resources as concise bullet-style
  strings (no leading numbers or bullet characters - the document template
  supplies its own numbering).
- The "rationale" field is a short (2-4 sentence) note to the teacher,
  written to them directly, explaining how their reflection shaped the
  goals chosen - e.g. why particular competencies were prioritized.
"""
