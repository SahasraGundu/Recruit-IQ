# # modules/pdf_generator.py
# import io
# import os
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import cm
# from reportlab.lib import colors
# from reportlab.platypus import (
#     SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
#     HRFlowable, PageBreak,
# )
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# # ─── Color Palette ─────────────────────────────────────────────────────────
# INDIGO = colors.HexColor("#4F46E5")
# VIOLET = colors.HexColor("#7C3AED")
# LIGHT_BG = colors.HexColor("#EEF2FF")
# DARK_TEXT = colors.HexColor("#1E1B4B")
# GRAY = colors.HexColor("#6B7280")
# SUCCESS = colors.HexColor("#059669")
# DANGER = colors.HexColor("#DC2626")
# WARNING = colors.HexColor("#D97706")

# def _styles():
#     styles = getSampleStyleSheet()
#     custom = {
#         "Title": ParagraphStyle("Title", fontSize=24, textColor=INDIGO,
#                                  spaceAfter=6, fontName="Helvetica-Bold", alignment=TA_CENTER),
#         "H1": ParagraphStyle("H1", fontSize=16, textColor=INDIGO,
#                                spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold"),
#         "H2": ParagraphStyle("H2", fontSize=13, textColor=VIOLET,
#                                spaceBefore=8, spaceAfter=4, fontName="Helvetica-Bold"),
#         "Body": ParagraphStyle("Body", fontSize=10, textColor=DARK_TEXT,
#                                 spaceAfter=4, fontName="Helvetica"),
#         "Small": ParagraphStyle("Small", fontSize=8, textColor=GRAY, fontName="Helvetica"),
#         "Caption": ParagraphStyle("Caption", fontSize=9, textColor=GRAY,
#                                    alignment=TA_CENTER, fontName="Helvetica-Oblique"),
#         "Subtitle": ParagraphStyle("Subtitle", fontSize=12, textColor=DARK_TEXT,
#                                     alignment=TA_CENTER, fontName="Helvetica"),
#     }
#     return custom

# def _header_table(drive_name: str, company: str, role: str, date_str: str):
#     data = [[
#         Paragraph(f"<b>{drive_name}</b>", ParagraphStyle("t", fontSize=14, textColor=INDIGO,
#                                                           fontName="Helvetica-Bold")),
#         Paragraph(f"{company} | {role}<br/><font size=9 color='#6B7280'>{date_str}</font>",
#                   ParagraphStyle("s", fontSize=10, textColor=DARK_TEXT, fontName="Helvetica")),
#         Paragraph("<b>AI Recruiter Report</b>",
#                   ParagraphStyle("r", fontSize=10, textColor=VIOLET, alignment=TA_RIGHT,
#                                  fontName="Helvetica-Bold")),
#     ]]
#     t = Table(data, colWidths=[7*cm, 8*cm, 5*cm])
#     t.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
#         ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_BG]),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
#         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#         ("PADDING", (0, 0), (-1, -1), 8),
#         ("ROUNDEDCORNERS", [4]),
#     ]))
#     return t

# def generate_recruitment_report(drive: dict, candidates: list, jd_parsed: dict) -> bytes:
#     """Generate full PDF recruitment report. Returns bytes."""
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4,
#                              rightMargin=2*cm, leftMargin=2*cm,
#                              topMargin=2*cm, bottomMargin=2*cm)
#     S = _styles()
#     story = []
#     date_str = datetime.now().strftime("%d %B %Y")
#     drive_name = drive.get("drive_name", "Recruitment Drive")
#     company = drive.get("company", "Company")
#     role = drive.get("role", "Role")
#     budget = drive.get("budget_ctc", 0)

#     # ── Cover Page ──
#     story.append(Spacer(1, 3*cm))
#     story.append(Paragraph("AI RECRUITMENT REPORT", S["Title"]))
#     story.append(Spacer(1, 0.5*cm))
#     story.append(HRFlowable(width="100%", thickness=2, color=INDIGO))
#     story.append(Spacer(1, 0.3*cm))
#     story.append(Paragraph(drive_name, ParagraphStyle("dn", fontSize=18, textColor=DARK_TEXT,
#                                                        alignment=TA_CENTER, fontName="Helvetica-Bold")))
#     story.append(Paragraph(f"{company} • {role}", S["Subtitle"]))
#     story.append(Paragraph(f"Generated: {date_str}", S["Caption"]))
#     story.append(Spacer(1, 1*cm))

#     # Summary stats
#     total = len(candidates)
#     selected = len([c for c in candidates if c.get("status") == "Selected"])
#     avg_score = sum(c.get("match_score", 0) for c in candidates) / max(total, 1)
#     stats_data = [
#         ["Total Candidates", "Selected", "Avg Match Score", "Budget CTC"],
#         [str(total), str(selected), f"{avg_score:.1f}%", f"{budget} LPA"],
#     ]
#     stats_t = Table(stats_data, colWidths=[4.75*cm]*4)
#     stats_t.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#         ("BACKGROUND", (0, 1), (-1, 1), LIGHT_BG),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("FONTSIZE", (0, 0), (-1, -1), 10),
#         ("PADDING", (0, 0), (-1, -1), 10),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
#     ]))
#     story.append(stats_t)
#     story.append(PageBreak())

#     # ── Page 2: JD Analysis ──
#     story.append(Paragraph("Job Description Analysis", S["H1"]))
#     story.append(HRFlowable(width="100%", thickness=1, color=INDIGO))
#     story.append(Spacer(1, 0.3*cm))
#     req_skills = jd_parsed.get("required_skills", [])
#     pref_skills = jd_parsed.get("preferred_skills", [])
#     exp = jd_parsed.get("experience", {})
#     story.append(Paragraph(f"<b>Role:</b> {role}", S["Body"]))
#     story.append(Paragraph(f"<b>Company:</b> {company}", S["Body"]))
#     story.append(Paragraph(f"<b>Experience Required:</b> {exp.get('min',0)}-{exp.get('max',5)} years", S["Body"]))
#     story.append(Paragraph(f"<b>Budget CTC:</b> {budget} LPA", S["Body"]))
#     story.append(Spacer(1, 0.3*cm))
#     story.append(Paragraph("Required Skills:", S["H2"]))
#     story.append(Paragraph(", ".join(req_skills) if req_skills else "Not specified", S["Body"]))
#     if pref_skills:
#         story.append(Paragraph("Preferred Skills:", S["H2"]))
#         story.append(Paragraph(", ".join(pref_skills), S["Body"]))
#     story.append(PageBreak())

#     # ── Page 3: Candidate Rankings ──
#     story.append(Paragraph("Candidate Rankings", S["H1"]))
#     story.append(HRFlowable(width="100%", thickness=1, color=INDIGO))
#     story.append(Spacer(1, 0.3*cm))
#     rank_data = [["Rank", "Name", "Score", "Experience", "Notice Period", "Exp CTC", "Status"]]
#     sorted_candidates = sorted(candidates, key=lambda x: x.get("match_score", 0), reverse=True)
#     for c in sorted_candidates:
#         status = c.get("status", "Pending")
#         s_color = SUCCESS if status == "Selected" else (DANGER if status == "Rejected" else DARK_TEXT)
#         rank_data.append([
#             str(c.get("rank", "-")),
#             c.get("name", "N/A")[:20],
#             f"{c.get('match_score', 0):.1f}%",
#             f"{c.get('experience_years', 0)} yrs",
#             f"{c.get('notice_period', 90)} days",
#             f"{c.get('expected_ctc', 0)} LPA",
#             status,
#         ])
#     rank_t = Table(rank_data, colWidths=[1*cm, 4.5*cm, 1.8*cm, 2*cm, 2.2*cm, 2*cm, 2.5*cm])
#     rank_t.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("FONTSIZE", (0, 0), (-1, -1), 8),
#         ("PADDING", (0, 0), (-1, -1), 6),
#         ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
#     ]))
#     story.append(rank_t)
#     story.append(PageBreak())

#     # ── Page 4: Selected Candidates ──
#     story.append(Paragraph("Selected Candidates", S["H1"]))
#     story.append(HRFlowable(width="100%", thickness=1, color=SUCCESS))
#     story.append(Spacer(1, 0.3*cm))
#     selected_list = [c for c in candidates if c.get("status") == "Selected"]
#     if selected_list:
#         for c in selected_list:
#             story.append(Paragraph(f"✓ {c.get('name','N/A')}", S["H2"]))
#             story.append(Paragraph(
#                 f"Score: {c.get('match_score',0):.1f}% | Experience: {c.get('experience_years',0)} yrs | "
#                 f"Expected: {c.get('expected_ctc',0)} LPA | Notice: {c.get('notice_period',90)} days",
#                 S["Body"]
#             ))
#             story.append(Paragraph(f"Skills: {', '.join(c.get('skills',[])[:10])}", S["Small"]))
#             story.append(Spacer(1, 0.3*cm))
#     else:
#         story.append(Paragraph("No candidates have been selected yet.", S["Body"]))
#     story.append(PageBreak())

#     # ── Page 5: AI Recommendations ──
#     story.append(Paragraph("AI Hiring Recommendations", S["H1"]))
#     story.append(HRFlowable(width="100%", thickness=1, color=VIOLET))
#     story.append(Spacer(1, 0.3*cm))
#     for c in sorted_candidates[:10]:
#         ai_rec = c.get("ai_recommendation")
#         if not ai_rec:
#             continue
#         story.append(Paragraph(f"► {c.get('name','N/A')} (Score: {c.get('match_score',0):.1f}%)", S["H2"]))
#         story.append(Paragraph(f"<b>Recommendation:</b> {ai_rec.get('hiring_recommendation','N/A')}", S["Body"]))
#         story.append(Paragraph(f"<b>Summary:</b> {ai_rec.get('summary','')}", S["Body"]))
#         story.append(Paragraph(f"<b>Risk:</b> {ai_rec.get('risk_analysis','')}", S["Body"]))
#         story.append(Spacer(1, 0.3*cm))
#     story.append(PageBreak())

#     # ── Page 6: Interview Questions ──
#     story.append(Paragraph("AI-Generated Interview Questions", S["H1"]))
#     story.append(HRFlowable(width="100%", thickness=1, color=INDIGO))
#     story.append(Spacer(1, 0.3*cm))
#     top_candidate = sorted_candidates[0] if sorted_candidates else None
#     if top_candidate and top_candidate.get("interview_questions"):
#         qs = top_candidate["interview_questions"]
#         for category, label in [("technical", "Technical"), ("behavioral", "Behavioral"), ("scenario", "Scenario")]:
#             story.append(Paragraph(f"{label} Questions", S["H2"]))
#             for i, q in enumerate(qs.get(category, []), 1):
#                 story.append(Paragraph(f"{i}. {q}", S["Body"]))
#             story.append(Spacer(1, 0.2*cm))
#     else:
#         story.append(Paragraph("Generate AI recommendations first to get interview questions.", S["Body"]))
#     story.append(PageBreak())

#     # ── Page 7: Final Decision ──
#     story.append(Paragraph("Final Hiring Decision", S["H1"]))
#     story.append(HRFlowable(width="100%", thickness=1, color=INDIGO))
#     story.append(Spacer(1, 0.3*cm))
#     story.append(Paragraph(
#         f"Based on AI analysis of {total} candidates for the {role} position at {company}:",
#         S["Body"]
#     ))
#     story.append(Spacer(1, 0.2*cm))
#     story.append(Paragraph(f"• <b>Total Screened:</b> {total}", S["Body"]))
#     story.append(Paragraph(f"• <b>Recommended for Selection:</b> {selected}", S["Body"]))
#     story.append(Paragraph(f"• <b>Average Match Score:</b> {avg_score:.1f}%", S["Body"]))
#     story.append(Spacer(1, 0.5*cm))
#     story.append(Paragraph(
#         "This report was generated by AI Recruiter Agent. Final hiring decisions should "
#         "consider factors beyond automated scoring including cultural fit, communication skills, "
#         "and in-person assessment.",
#         S["Small"]
#     ))

#     doc.build(story)
#     return buffer.getvalue() 







# modules/pdf_generator.py
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ─── Colors ───────────────────────────────────────────────────────────────────
INDIGO    = colors.HexColor("#4F46E5")
VIOLET    = colors.HexColor("#7C3AED")
LIGHT_BG  = colors.HexColor("#EEF2FF")
DARK_TEXT = colors.HexColor("#1E1B4B")
GRAY      = colors.HexColor("#6B7280")
LIGHT_GRAY= colors.HexColor("#F8F9FF")
SUCCESS   = colors.HexColor("#059669")
DANGER    = colors.HexColor("#DC2626")
WARNING   = colors.HexColor("#D97706")
WHITE     = colors.white
BLACK     = colors.HexColor("#111827")

# ─── Styles ───────────────────────────────────────────────────────────────────
def _styles():
    return {
        "CoverTitle": ParagraphStyle(
            "CoverTitle", fontSize=28, textColor=INDIGO,
            fontName="Helvetica-Bold", alignment=TA_CENTER,
            spaceAfter=8, leading=34,
        ),
        "CoverDriveName": ParagraphStyle(
            "CoverDriveName", fontSize=20, textColor=BLACK,
            fontName="Helvetica-Bold", alignment=TA_CENTER,
            spaceAfter=6, leading=26,
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle", fontSize=13, textColor=GRAY,
            fontName="Helvetica", alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "CoverDate": ParagraphStyle(
            "CoverDate", fontSize=10, textColor=GRAY,
            fontName="Helvetica-Oblique", alignment=TA_CENTER,
        ),
        "H1": ParagraphStyle(
            "H1", fontSize=16, textColor=INDIGO,
            fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=6,
        ),
        "H2": ParagraphStyle(
            "H2", fontSize=12, textColor=VIOLET,
            fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=4,
        ),
        "Body": ParagraphStyle(
            "Body", fontSize=10, textColor=BLACK,
            fontName="Helvetica", spaceAfter=4, leading=15,
        ),
        "BodyWrap": ParagraphStyle(
            "BodyWrap", fontSize=9, textColor=BLACK,
            fontName="Helvetica", spaceAfter=4, leading=14,
            wordWrap="CJK",
        ),
        "Small": ParagraphStyle(
            "Small", fontSize=8, textColor=GRAY,
            fontName="Helvetica", leading=12,
        ),
        "Disclaimer": ParagraphStyle(
            "Disclaimer", fontSize=8, textColor=GRAY,
            fontName="Helvetica-Oblique", leading=12, spaceAfter=4,
        ),
    }

# ─── Page width (A4 minus margins) ────────────────────────────────────────────
PAGE_W = A4[0] - 4 * cm   # 2cm left + 2cm right

def generate_recruitment_report(drive: dict, candidates: list, jd_parsed: dict) -> bytes:
    buffer   = io.BytesIO()
    doc      = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm,   bottomMargin=2*cm,
    )
    S        = _styles()
    story    = []
    date_str = datetime.now().strftime("%d %B %Y")

    drive_name = drive.get("drive_name", "Recruitment Drive")
    company    = drive.get("company",    "Company")
    role       = drive.get("role",       "Role")
    budget     = drive.get("budget_ctc", 0)

    total     = len(candidates)
    selected  = len([c for c in candidates if c.get("status") == "Selected"])
    avg_score = sum(c.get("match_score", 0) for c in candidates) / max(total, 1)
    sorted_candidates = sorted(candidates, key=lambda x: x.get("match_score", 0), reverse=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — Cover
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 2.5*cm))

    story.append(Paragraph("AI RECRUITMENT REPORT", S["CoverTitle"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=2.5, color=INDIGO, spaceAfter=10))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(drive_name,          S["CoverDriveName"]))
    story.append(Paragraph(f"{company}  •  {role}", S["CoverSubtitle"]))
    story.append(Paragraph(f"Generated: {date_str}", S["CoverDate"]))
    story.append(Spacer(1, 1.2*cm))

    # Stats table — 4 equal columns
    col_w = PAGE_W / 4
    stats_header = [
        Paragraph("<b>Total Candidates</b>", ParagraphStyle("sh", fontSize=9,  textColor=WHITE,      fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Selected</b>",          ParagraphStyle("sh", fontSize=9,  textColor=WHITE,      fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Avg Match Score</b>",   ParagraphStyle("sh", fontSize=9,  textColor=WHITE,      fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Budget CTC</b>",        ParagraphStyle("sh", fontSize=9,  textColor=WHITE,      fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]
    stats_values = [
        Paragraph(str(total),              ParagraphStyle("sv", fontSize=18, textColor=INDIGO,    fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(str(selected),           ParagraphStyle("sv", fontSize=18, textColor=SUCCESS,   fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"{avg_score:.1f}%",     ParagraphStyle("sv", fontSize=18, textColor=WARNING,   fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"{budget} LPA",         ParagraphStyle("sv", fontSize=18, textColor=VIOLET,    fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]
    stats_t = Table([stats_header, stats_values], colWidths=[col_w]*4)
    stats_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), INDIGO),
        ("BACKGROUND",  (0,1), (-1,1), LIGHT_BG),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("PADDING",     (0,0), (-1,-1), 12),
        ("LINEBELOW",   (0,0), (-1,0), 0, INDIGO),
        ("BOX",         (0,0), (-1,-1), 0.5, INDIGO),
        ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(stats_t)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — JD Analysis
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Job Description Analysis", S["H1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=INDIGO, spaceAfter=8))

    req_skills  = jd_parsed.get("required_skills",  [])
    pref_skills = jd_parsed.get("preferred_skills", [])
    exp         = jd_parsed.get("experience", {})
    role_info   = jd_parsed.get("role_info",   {})

    # Info table
    info_data = [
        [Paragraph("<b>Role</b>",                S["Body"]), Paragraph(role,                                          S["Body"])],
        [Paragraph("<b>Company</b>",             S["Body"]), Paragraph(company,                                       S["Body"])],
        [Paragraph("<b>Experience Required</b>", S["Body"]), Paragraph(f"{exp.get('min',0)} – {exp.get('max',5)} years", S["Body"])],
        [Paragraph("<b>Budget CTC</b>",          S["Body"]), Paragraph(f"{budget} LPA",                               S["Body"])],
        [Paragraph("<b>Work Mode</b>",           S["Body"]), Paragraph(role_info.get("work_mode", "On-site"),         S["Body"])],
        [Paragraph("<b>Location</b>",            S["Body"]), Paragraph(role_info.get("location", "India"),            S["Body"])],
    ]
    info_t = Table(info_data, colWidths=[4*cm, PAGE_W - 4*cm])
    info_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (0,-1), LIGHT_BG),
        ("ALIGN",       (0,0), (0,-1), "RIGHT"),
        ("ALIGN",       (1,0), (1,-1), "LEFT"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("PADDING",     (0,0), (-1,-1), 7),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT_BG, WHITE]),
        ("BOX",         (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
        ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
    ]))
    story.append(info_t)
    story.append(Spacer(1, 0.5*cm))

    # Required Skills — wrapped properly
    if req_skills:
        story.append(Paragraph("Required Skills", S["H2"]))
        # Build skill tags as wrapped text
        skill_text = "  •  ".join(req_skills)
        story.append(Paragraph(skill_text, S["BodyWrap"]))
        story.append(Spacer(1, 0.3*cm))

    if pref_skills:
        story.append(Paragraph("Preferred Skills", S["H2"]))
        skill_text = "  •  ".join(pref_skills)
        story.append(Paragraph(skill_text, S["BodyWrap"]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — Candidate Rankings
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Candidate Rankings", S["H1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=INDIGO, spaceAfter=8))

    rank_data = [[
        Paragraph("<b>Rank</b>",          ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Name</b>",          ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Score</b>",         ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Experience</b>",    ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Notice</b>",        ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Exp CTC</b>",       ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("<b>Status</b>",        ParagraphStyle("rh", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]]

    for i, c in enumerate(sorted_candidates):
        status = c.get("status", "Pending")
        if status == "Selected":
            status_color = SUCCESS
        elif status == "Rejected":
            status_color = DANGER
        else:
            status_color = GRAY

        score = c.get("match_score", 0)
        score_color = SUCCESS if score >= 75 else (WARNING if score >= 50 else DANGER)

        row_bg = LIGHT_BG if i % 2 == 0 else WHITE
        rank_data.append([
            Paragraph(str(c.get("rank", "-")),               ParagraphStyle("rc", fontSize=8, textColor=DARK_TEXT,     fontName="Helvetica",      alignment=TA_CENTER)),
            Paragraph(c.get("name", "N/A")[:22],             ParagraphStyle("rc", fontSize=8, textColor=BLACK,         fontName="Helvetica-Bold", alignment=TA_LEFT)),
            Paragraph(f"{score:.1f}%",                       ParagraphStyle("rc", fontSize=8, textColor=score_color,   fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(f"{c.get('experience_years', 0)} yrs", ParagraphStyle("rc", fontSize=8, textColor=DARK_TEXT,     fontName="Helvetica",      alignment=TA_CENTER)),
            Paragraph(f"{c.get('notice_period', 90)}d",      ParagraphStyle("rc", fontSize=8, textColor=DARK_TEXT,     fontName="Helvetica",      alignment=TA_CENTER)),
            Paragraph(f"{c.get('expected_ctc', 0)} LPA",     ParagraphStyle("rc", fontSize=8, textColor=DARK_TEXT,     fontName="Helvetica",      alignment=TA_CENTER)),
            Paragraph(status,                                 ParagraphStyle("rc", fontSize=8, textColor=status_color,  fontName="Helvetica-Bold", alignment=TA_CENTER)),
        ])

    rank_t = Table(rank_data, colWidths=[1.2*cm, 4.8*cm, 1.6*cm, 2*cm, 1.6*cm, 2*cm, 2.8*cm])
    rank_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), INDIGO),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT_BG, WHITE]),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("ALIGN",       (1,1), (1,-1), "LEFT"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("PADDING",     (0,0), (-1,-1), 5),
        ("BOX",         (0,0), (-1,-1), 0.5, colors.HexColor("#C7D2FE")),
        ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
    ]))
    story.append(rank_t)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 — Selected Candidates
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Selected Candidates", S["H1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SUCCESS, spaceAfter=8))

    selected_list = [c for c in candidates if c.get("status") == "Selected"]
    if selected_list:
        for c in selected_list:
            block = []
            block.append(Paragraph(
                f"<font color='#059669'>✓</font>  <b>{c.get('name','N/A')}</b>",
                S["H2"]
            ))
            details_data = [
                ["Match Score",    f"{c.get('match_score',0):.1f}%",   "Experience",    f"{c.get('experience_years',0)} years"],
                ["Expected CTC",   f"{c.get('expected_ctc',0)} LPA",   "Notice Period", f"{c.get('notice_period',90)} days"],
                ["Current CTC",    f"{c.get('current_ctc',0)} LPA",    "Status",        c.get("status","")],
            ]
            dw = PAGE_W / 4
            det_t = Table(details_data, colWidths=[dw, dw, dw, dw])
            det_t.setStyle(TableStyle([
                ("BACKGROUND",  (0,0), (0,-1), LIGHT_BG),
                ("BACKGROUND",  (2,0), (2,-1), LIGHT_BG),
                ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
                ("FONTNAME",    (2,0), (2,-1), "Helvetica-Bold"),
                ("FONTSIZE",    (0,0), (-1,-1), 9),
                ("PADDING",     (0,0), (-1,-1), 6),
                ("BOX",         (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
                ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
            ]))
            block.append(det_t)

            skills = c.get("skills", [])[:12]
            if skills:
                block.append(Spacer(1, 0.2*cm))
                block.append(Paragraph("<b>Skills:</b>  " + "  •  ".join(skills), S["Small"]))

            block.append(Spacer(1, 0.4*cm))
            story.append(KeepTogether(block))
    else:
        story.append(Paragraph("No candidates have been selected yet.", S["Body"]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5 — AI Hiring Recommendations
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("AI Hiring Recommendations", S["H1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=VIOLET, spaceAfter=8))

    ai_found = False
    for c in sorted_candidates[:10]:
        ai_rec = c.get("ai_recommendation")
        if not ai_rec:
            continue
        ai_found = True

        rec   = ai_rec.get("hiring_recommendation", "Pending")
        rec_color = SUCCESS if "Proceed" in rec else (DANGER if "Reject" in rec else WARNING)

        block = []
        block.append(Paragraph(
            f"<b>{c.get('name','N/A')}</b>   "
            f"<font color='#6B7280' size=9>Score: {c.get('match_score',0):.1f}%</font>",
            S["H2"]
        ))

        rec_data = [
            [Paragraph("<b>Recommendation</b>", ParagraphStyle("rl", fontSize=9, textColor=GRAY,      fontName="Helvetica-Bold")),
             Paragraph(rec,                      ParagraphStyle("rv", fontSize=9, textColor=rec_color, fontName="Helvetica-Bold"))],
            [Paragraph("<b>Risk</b>",            ParagraphStyle("rl", fontSize=9, textColor=GRAY,      fontName="Helvetica-Bold")),
             Paragraph(ai_rec.get("risk_analysis",""),  ParagraphStyle("rv", fontSize=9, textColor=BLACK, fontName="Helvetica", wordWrap="CJK"))],
            [Paragraph("<b>Summary</b>",         ParagraphStyle("rl", fontSize=9, textColor=GRAY,      fontName="Helvetica-Bold")),
             Paragraph(ai_rec.get("summary",""), ParagraphStyle("rv", fontSize=9, textColor=BLACK, fontName="Helvetica", wordWrap="CJK"))],
        ]
        rec_t = Table(rec_data, colWidths=[3*cm, PAGE_W - 3*cm])
        rec_t.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (0,-1), LIGHT_BG),
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
            ("PADDING",     (0,0), (-1,-1), 6),
            ("BOX",         (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
            ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
        ]))
        block.append(rec_t)

        # Strengths & weaknesses side by side
        strengths  = ai_rec.get("strengths",  [])
        weaknesses = ai_rec.get("weaknesses", [])
        if strengths or weaknesses:
            sw_data = [[
                Paragraph("<b>✅ Strengths</b><br/>" + "<br/>".join(f"• {s}" for s in strengths),
                          ParagraphStyle("sw", fontSize=8, textColor=BLACK, fontName="Helvetica", leading=13)),
                Paragraph("<b>⚠ Weaknesses</b><br/>" + "<br/>".join(f"• {w}" for w in weaknesses),
                          ParagraphStyle("sw", fontSize=8, textColor=BLACK, fontName="Helvetica", leading=13)),
            ]]
            sw_t = Table(sw_data, colWidths=[PAGE_W/2, PAGE_W/2])
            sw_t.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (0,0), colors.HexColor("#ECFDF5")),
                ("BACKGROUND", (1,0), (1,0), colors.HexColor("#FEF2F2")),
                ("VALIGN",     (0,0), (-1,-1), "TOP"),
                ("PADDING",    (0,0), (-1,-1), 8),
                ("BOX",        (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
                ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
            ]))
            block.append(Spacer(1, 0.15*cm))
            block.append(sw_t)

        block.append(Spacer(1, 0.5*cm))
        story.append(KeepTogether(block))

    if not ai_found:
        story.append(Paragraph(
            "No AI recommendations generated yet. Open a candidate profile and click "
            "'Generate AI Recommendation' to add them here.",
            S["Body"]
        ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6 — Final Hiring Decision
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Final Hiring Decision", S["H1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=INDIGO, spaceAfter=8))

    story.append(Paragraph(
        f"Based on AI analysis of <b>{total}</b> candidates for the "
        f"<b>{role}</b> position at <b>{company}</b>:",
        S["Body"]
    ))
    story.append(Spacer(1, 0.3*cm))

    summary_data = [
        ["Total Screened",            str(total)],
        ["Recommended for Selection", str(selected)],
        ["Average Match Score",       f"{avg_score:.1f}%"],
        ["Budget CTC",                f"{budget} LPA"],
    ]
    sum_t = Table(summary_data, colWidths=[6*cm, PAGE_W - 6*cm])
    sum_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), LIGHT_BG),
        ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("PADDING",       (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [LIGHT_BG, WHITE]),
        ("BOX",           (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, colors.HexColor("#C7D2FE")),
    ]))
    story.append(sum_t)
    story.append(Spacer(1, 0.8*cm))

    story.append(Paragraph(
        "This report was generated by AI Recruiter Agent. Final hiring decisions should consider "
        "factors beyond automated scoring including cultural fit, communication skills, "
        "and in-person assessment.",
        S["Disclaimer"]
    ))

    doc.build(story)
    return buffer.getvalue()
