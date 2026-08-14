"""TQS indicator text, mirroring the checklist rendered in index.html.

Keyed by competency number (1-6); each value is an ordered list of
(code, indicator_text) tuples matching the order the ratings arrays are
built in on the front end, so ratings[str(comp)][i] lines up with
INDICATORS[comp][i].
"""

INDICATORS = {
    1: [
        ("1a", "I act consistently with fairness, respect and integrity in all my interactions with students, families, colleagues, and community members"),
        ("1b", "I demonstrate empathy and genuine care for the students and families I work with, and this is visible in my day-to-day practice"),
        ("1c", "I provide culturally appropriate and meaningful opportunities for students and parents/guardians, as partners in education, to actively support student learning"),
        ("1d", "I invite and welcome First Nations, Métis and Inuit parents/guardians, Elders/knowledge keepers, cultural advisors and local community members into my school and classroom"),
        ("1e", "I collaborate effectively with community service professionals (mental health, social services, justice, health, law enforcement) to support students' overall well-being"),
        ("1f", "I honour cultural diversity in my classroom and actively promote intercultural understanding among my students"),
    ],
    2: [
        ("2a", "I engage in ongoing critical reflection on my own teaching practice to identify areas for professional growth"),
        ("2b", "I collaborate with colleagues to build personal and collective professional capacities, sharing expertise and learning from others"),
        ("2c", "I actively seek out feedback from students, families, peers, and supervisors to enhance my teaching practice"),
        ("2d", "I build and maintain my capacity to support student success in inclusive, welcoming, caring, respectful and safe learning environments"),
        ("2e", "I seek out, critically review, and apply current educational research to continuously improve my practice"),
        ("2f", "I continually enhance my understanding of First Nations, Métis and Inuit worldviews, cultural beliefs, languages and values"),
        ("2g", "I maintain awareness of emerging technologies — including AI tools — and consider how they can ethically and effectively enhance my teaching and student learning"),
    ],
    3: [
        ("3a", "I plan and design learning activities that address Alberta curriculum outcomes, reflect short/medium/long-range planning, and incorporate varied, engaging, and relevant instructional strategies"),
        ("3b", "I incorporate appropriate digital technology and resources in my planning to build student capacity for acquiring knowledge, communicating, thinking critically, and evaluating information"),
        ("3c", "I plan by thoughtfully considering student variables including age, prior knowledge, cultural and linguistic background, social-emotional needs, and cognitive and physical abilities"),
        ("3d", "I use instructional strategies that engage students in meaningful learning, drawing on my specialized subject knowledge, understanding of how students develop, and knowledge of their backgrounds"),
        ("3e", "I apply assessment and evaluation practices that accurately reflect curriculum outcomes, generate evidence of learning through balanced formative and summative experiences, and provide timely, constructive feedback"),
        ("3f", "I offer students a variety of methods to demonstrate their achievement of learning outcomes, and I use reasoned professional judgment in determining and reporting the level of student learning"),
        ("3g", "I consistently communicate high expectations for all students and foster their understanding of how each learning activity connects to the intended outcomes"),
        ("3h", "I ensure that all students continuously develop their skills in literacy and numeracy, and I build student capacity for collaboration in my instructional design"),
        ("3i", "I consider relevant local, provincial, national and international contexts and issues when planning and designing learning activities"),
    ],
    4: [
        ("4a", "I foster equality and respect in my classroom with regard to rights as provided for in the Alberta Human Rights Act and the Canadian Charter of Rights and Freedoms"),
        ("4b", "I use appropriate universal and targeted strategies and supports to address the diverse strengths, learning challenges and areas for growth of all students"),
        ("4c", "I communicate a clear philosophy of education that affirms every student can learn and be successful, and I make this visible in my practice"),
        ("4d", "I am aware of, and proactively respond to, the emotional and mental health needs of my students"),
        ("4e", "I recognize and respond to the specific learning needs of individual students and, when needed, collaborate with specialists and service providers to design targeted supports"),
        ("4f", "I employ classroom management strategies that promote positive, engaging, and welcoming learning environments where every student feels safe and valued"),
        ("4g", "I incorporate students' personal and cultural strengths, backgrounds, and experiences into my teaching and learning activities"),
        ("4h", "I provide regular, meaningful opportunities for student leadership and agency within my classroom"),
    ],
    5: [
        ("5a", "I understand the historical, social, economic and political implications of treaties and agreements with First Nations, legislation negotiated with Métis, and the legacy and ongoing impact of residential schools"),
        ("5b", "I support student achievement by engaging in collaborative, whole-school approaches to building capacity in First Nations, Métis and Inuit education"),
        ("5c", "I use programs of study to provide opportunities for all students to develop knowledge of, and respect for, the histories, cultures, languages, contributions, perspectives and contemporary contexts of First Nations, Métis and Inuit"),
        ("5d", "I use resources that accurately reflect and demonstrate the strength and diversity of First Nations, Métis and Inuit to support the learning experiences of all students"),
    ],
    6: [
        ("6a", "I maintain awareness of, and respond in accordance with, requirements authorized under the Alberta Education Act and other relevant legislation applicable to my teaching context"),
        ("6b", "I engage consistently in practices that align with the policies and procedures established by my school authority"),
        ("6c", "I recognize and uphold the standards of professional conduct expected of a caring, knowledgeable and reasonable adult who is entrusted with the custody, care and education of students"),
    ],
}

RATING_LABELS = {
    1: "Rarely / Not Yet",
    2: "Beginning",
    3: "Developing",
    4: "Proficient",
    5: "Exemplary",
}
