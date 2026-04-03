# ============================================================
# PROFESSIONAL ESG PDF REPORT GENERATOR
# Full rewrite — pixel-perfect layout, borders, aligned images
# ============================================================

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from datetime import date
import os

# ============================================================
# PATHS — UPDATE THESE TO MATCH YOUR SYSTEM
# ============================================================

BASE = r"C:\Users\eshaa\Desktop\ESG_Dashboard"

DATA_CSV      = os.path.join(BASE, "esg_scored.csv")
INDUSTRY_CSV  = os.path.join(BASE, "esg_industry.csv")
PDF_OUTPUT    = os.path.join(BASE, "ESG_Report_Pro.pdf")

CHART_TOP10   = os.path.join(BASE, "chart1_top10.png")
CHART_CAT     = os.path.join(BASE, "chart2_categories.png")
CHART_IND     = os.path.join(BASE, "chart3_industries.png")
CHART_HEAT    = os.path.join(BASE, "chart4_heatmap.png")
CHART_ML      = os.path.join(BASE, "chart7_ml_predictions.png")
CHART_FEAT    = os.path.join(BASE, "chart8_feature_importance.png")

# ============================================================
# LOAD DATA
# ============================================================

df       = pd.read_csv(DATA_CSV)
industry = pd.read_csv(INDUSTRY_CSV)

# ============================================================
# COLOR PALETTE
# ============================================================

C_DARK_BLUE   = colors.HexColor("#0D1B2A")
C_MID_BLUE    = colors.HexColor("#1A5276")
C_ROYAL       = colors.HexColor("#2E86C1")
C_LIGHT_BLUE  = colors.HexColor("#D6EAF8")
C_PALE_BLUE   = colors.HexColor("#EBF5FB")
C_GREEN       = colors.HexColor("#1E8449")
C_RED         = colors.HexColor("#C0392B")
C_AMBER       = colors.HexColor("#D4AC0D")
C_WHITE       = colors.white
C_OFF_WHITE   = colors.HexColor("#F8F9FA")
C_LIGHT_GRAY  = colors.HexColor("#ECF0F1")
C_MID_GRAY    = colors.HexColor("#7F8C8D")
C_DARK_GRAY   = colors.HexColor("#2C3E50")
C_BORDER      = colors.HexColor("#AED6F1")
C_GOLD        = colors.HexColor("#D4AC0D")

# ============================================================
# PAGE DIMENSIONS
# ============================================================

PW, PH = A4
ML = 1.8 * cm
MR = 1.8 * cm
MT = 1.8 * cm
MB = 1.8 * cm
W  = PW - ML - MR  # usable content width

# ============================================================
# PARAGRAPH STYLE FACTORY
# ============================================================

def S(name, **kw):
    return ParagraphStyle(name, **kw)

# ============================================================
# DOCUMENT TEMPLATE WITH HEADER / FOOTER
# ============================================================

class ESGDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(ML, MB + 0.4*cm, W, PH - MT - MB - 0.8*cm,
                      leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        template = PageTemplate(id="main", frames=[frame],
                                onPage=self._draw_chrome)
        self.addPageTemplates([template])

    def _draw_chrome(self, cv, doc):
        if doc.page == 1:
            return  # Cover page has no header/footer chrome
        cv.saveState()

        # Top rule
        cv.setStrokeColor(C_ROYAL)
        cv.setLineWidth(1.5)
        cv.line(ML, PH - 1.0*cm, PW - MR, PH - 1.0*cm)

        # Header left
        cv.setFont("Helvetica-Bold", 7)
        cv.setFillColor(C_DARK_BLUE)
        cv.drawString(ML, PH - 0.72*cm, "ESG SCORE ANALYTICS & SUSTAINABILITY REPORT")

        # Header right
        cv.setFont("Helvetica", 7)
        cv.setFillColor(C_MID_GRAY)
        cv.drawRightString(PW - MR, PH - 0.72*cm,
                           f"Report Date: {date.today().strftime('%B %d, %Y')}")

        # Bottom rule
        cv.setStrokeColor(C_ROYAL)
        cv.setLineWidth(0.8)
        cv.line(ML, 0.9*cm, PW - MR, 0.9*cm)

        # Footer left
        cv.setFont("Helvetica", 6.5)
        cv.setFillColor(C_MID_GRAY)
        cv.drawString(ML, 0.55*cm,
                      "ESG Analytics Dashboard  |  Data: 722 S&P Companies  |  Model: Weighted ESG v1.0")

        # Footer right — page number
        cv.setFont("Helvetica-Bold", 7)
        cv.setFillColor(C_ROYAL)
        cv.drawRightString(PW - MR, 0.55*cm, f"Page {doc.page}")

        cv.restoreState()

# ============================================================
# HELPERS
# ============================================================

def spacer(h=0.15):
    return Spacer(1, h * inch)

def divider(color=C_ROYAL, thick=1.5):
    return HRFlowable(width="100%", thickness=thick,
                      color=color, spaceAfter=6, spaceBefore=2)

def section_header(num, title):
    """Dark banner header with accent number swatch."""
    data = [[
        Paragraph(num, S("N", fontSize=9, fontName="Helvetica-Bold",
                         textColor=C_WHITE, alignment=TA_CENTER)),
        Paragraph(title, S("T", fontSize=11, fontName="Helvetica-Bold",
                           textColor=C_WHITE, alignment=TA_LEFT)),
    ]]
    t = Table(data, colWidths=[0.48*inch, W - 0.48*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), C_DARK_BLUE),
        ("BACKGROUND",    (0,0), (0,0),   C_ROYAL),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    return t

def kpi_cell(value, label, val_color=C_DARK_BLUE):
    """Single KPI tile with value, colored underline, and label."""
    data = [
        [Paragraph(str(value), S("V", fontSize=18, fontName="Helvetica-Bold",
                                 textColor=val_color, alignment=TA_CENTER))],
        [Paragraph(label,      S("L", fontSize=6.5, fontName="Helvetica",
                                 textColor=C_MID_GRAY, alignment=TA_CENTER))],
    ]
    t = Table(data, colWidths=[W / 6 - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), C_WHITE),
        ("BOX",           (0,0), (-1,-1), 0.8, C_BORDER),
        ("LINEBELOW",     (0,0), (-1,0), 3, val_color),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def safe_img(path, w, h):
    """Return an Image or a placeholder table if path missing."""
    if os.path.exists(path):
        i = Image(path, width=w, height=h)
        i.hAlign = "CENTER"
        return i
    # Placeholder
    ph = Table([[Paragraph(f"[Chart: {os.path.basename(path)}]",
                           S("P", fontSize=8, textColor=C_MID_GRAY,
                             alignment=TA_CENTER))]],
               colWidths=[w], rowHeights=[h])
    ph.setStyle(TableStyle([
        ("BOX",        (0,0), (-1,-1), 0.5, C_BORDER),
        ("BACKGROUND", (0,0), (-1,-1), C_LIGHT_GRAY),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
    ]))
    return ph

def framed_chart(path, w, h, caption):
    """Image inside a labelled bordered frame."""
    cap  = Paragraph(caption, S("Cap", fontSize=7.5, fontName="Helvetica-Bold",
                                textColor=C_MID_GRAY, alignment=TA_CENTER))
    img  = safe_img(path, w - 0.3*cm, h - 0.1*cm)
    data = [[cap], [img]]
    t = Table(data, colWidths=[w])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), C_PALE_BLUE),
        ("BACKGROUND",    (0,1), (-1,1), C_WHITE),
        ("BOX",           (0,0), (-1,-1), 0.8, C_BORDER),
        ("LINEBELOW",     (0,0), (-1,0), 0.5, C_BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def side_by_side_charts(p1, c1, p2, c2, total_w, h):
    """Two framed charts sitting side by side."""
    half = (total_w - 0.15*cm) / 2
    left  = framed_chart(p1, half, h, c1)
    right = framed_chart(p2, half, h, c2)
    row = Table([[left, right]], colWidths=[half, half])
    row.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    return row

# Table cell helpers
def th(text, align="CENTER"):
    a = TA_CENTER if align != "LEFT" else TA_LEFT
    return Paragraph(f"<b>{text}</b>",
                     S("TH", fontSize=8, fontName="Helvetica-Bold",
                       textColor=C_WHITE, alignment=a))

def td(text, bold=False, color=C_DARK_GRAY, align="CENTER", size=8):
    a = {"CENTER": TA_CENTER, "LEFT": TA_LEFT, "RIGHT": TA_RIGHT}.get(align, TA_CENTER)
    fn = "Helvetica-Bold" if bold else "Helvetica"
    return Paragraph(str(text)[:36],
                     S("TD", fontSize=size, fontName=fn,
                       textColor=color, alignment=a))

# Base table style
BASE_TS = [
    ("BACKGROUND",    (0,0), (-1,0),  C_DARK_BLUE),
    ("GRID",          (0,0), (-1,-1), 0.35, C_BORDER),
    ("LINEBELOW",     (0,0), (-1,0),  1.5,  C_ROYAL),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 5),
    ("RIGHTPADDING",  (0,0), (-1,-1), 5),
]

def alt_rows(n, ca=colors.HexColor("#EBF5FB"), cb=C_WHITE):
    return [("BACKGROUND", (0, i+1), (-1, i+1), ca if i % 2 == 0 else cb)
            for i in range(n)]

def callout_box(html_text, border_color=C_ROYAL, bg=C_LIGHT_BLUE):
    data = [[Paragraph(html_text, S("CB", fontSize=8.5, fontName="Helvetica",
                                    textColor=C_DARK_GRAY, leading=14))]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("BOX",           (0,0), (-1,-1), 1, border_color),
        ("LINEABOVE",     (0,0), (-1,0), 3, border_color),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    return t

# ============================================================
# COMPUTE KPIs
# ============================================================

total       = len(df)
leaders     = len(df[df["ESG_Category"].str.strip() == "Leader"])
average     = len(df[df["ESG_Category"].str.strip() == "Average"])
laggards    = len(df[df["ESG_Category"].str.strip() == "Laggard"])
avg_score   = round(df["Weighted_ESG_Score"].mean(), 1)
top_score   = round(df["Weighted_ESG_Score"].max(), 2)
leader_pct  = round(leaders  / total * 100, 1)
average_pct = round(average  / total * 100, 1)
laggard_pct = round(laggards / total * 100, 1)

top10    = df.sort_values("Weighted_ESG_Score", ascending=False).head(10).reset_index(drop=True)
top_co   = df.sort_values("Weighted_ESG_Score", ascending=False).iloc[0]
top12_ind= industry.head(12)
best_ind = industry.iloc[0]
worst_ind= industry.iloc[-1]
best_env = industry.sort_values("Avg_Env_Score",    ascending=False).iloc[0]
best_soc = industry.sort_values("Avg_Social_Score", ascending=False).iloc[0]
best_gov = industry.sort_values("Avg_Gov_Score",    ascending=False).iloc[0]
worst_env= industry.sort_values("Avg_Env_Score",    ascending=True).iloc[0]
worst_soc= industry.sort_values("Avg_Social_Score", ascending=True).iloc[0]
worst_gov= industry.sort_values("Avg_Gov_Score",    ascending=True).iloc[0]

# ============================================================
# BUILD CONTENT
# ============================================================

content = []

# ===========================================================
# PAGE 1  —  COVER
# ===========================================================

# Dark header band
cover_band = Table([[""]], colWidths=[W], rowHeights=[3.9*inch])
cover_band.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), C_DARK_BLUE)]))
content.append(cover_band)
content.append(Spacer(1, -3.9*inch))  # float text over the band

content.append(Spacer(1, 0.55*inch))
content.append(Paragraph("ESG SCORE ANALYTICS",
                          S("CT1", fontSize=30, fontName="Helvetica-Bold",
                            textColor=C_WHITE, alignment=TA_CENTER, leading=36)))
content.append(Paragraph("&amp; SUSTAINABILITY REPORT",
                          S("CT2", fontSize=30, fontName="Helvetica-Bold",
                            textColor=C_WHITE, alignment=TA_CENTER, leading=36, spaceAfter=6)))
content.append(Spacer(1, 0.06*inch))
content.append(Paragraph("Environmental &nbsp;&nbsp;·&nbsp;&nbsp; Social &nbsp;&nbsp;·&nbsp;&nbsp; Governance",
                          S("CS", fontSize=12, fontName="Helvetica",
                            textColor=colors.HexColor("#AED6F1"),
                            alignment=TA_CENTER, spaceAfter=4)))
content.append(Paragraph(
    f"Report Date: {date.today().strftime('%B %d, %Y')} &nbsp;|&nbsp; "
    f"Data: 722 S&amp;P Companies &nbsp;|&nbsp; Model: Weighted ESG v1.0",
    S("CD", fontSize=8.5, fontName="Helvetica",
      textColor=colors.HexColor("#D6E4F7"), alignment=TA_CENTER)))
content.append(Spacer(1, 0.42*inch))

# KPI row
kpi_row = [[
    kpi_cell(total,     "Total Companies", C_DARK_BLUE),
    kpi_cell(leaders,   "ESG Leaders",     C_GREEN),
    kpi_cell(average,   "ESG Average",     C_AMBER),
    kpi_cell(laggards,  "ESG Laggards",    C_RED),
    kpi_cell(avg_score, "Avg ESG Score",   C_ROYAL),
    kpi_cell(top_score, "Top ESG Score",   C_MID_BLUE),
]]
kpi_t = Table(kpi_row, colWidths=[W/6]*6)
kpi_t.setStyle(TableStyle([
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0), (-1,-1), 3),
    ("RIGHTPADDING",  (0,0), (-1,-1), 3),
    ("TOPPADDING",    (0,0), (-1,-1), 0),
    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
]))
content.append(kpi_t)
content.append(Spacer(1, 0.28*inch))

# Methodology panel
content.append(callout_box(
    "<b>METHODOLOGY</b><br/><br/>"
    "This report applies a <b>Weighted ESG Scoring Model</b> across <b>722 publicly listed S&amp;P companies</b>. "
    "Each company is evaluated across three pillars — <b>Environmental (40%)</b>, <b>Social (35%)</b>, "
    "and <b>Governance (25%)</b>. Raw scores are normalized to a 0–100 scale using Min-Max normalization "
    "before weighting, ensuring fair cross-industry comparison. Companies are then categorized as "
    "<b>Leader</b> (score ≥ 60), <b>Average</b> (40–60), or <b>Laggard</b> (below 40).",
    border_color=C_ROYAL, bg=C_LIGHT_BLUE
))
content.append(Spacer(1, 0.22*inch))

# Pillar weight banner
pillar_data = [[
    Paragraph("<b>ENVIRONMENTAL</b><br/>40% Weight",
              S("P", fontSize=8.5, fontName="Helvetica-Bold", textColor=C_WHITE, alignment=TA_CENTER)),
    Paragraph("<b>SOCIAL</b><br/>35% Weight",
              S("P", fontSize=8.5, fontName="Helvetica-Bold", textColor=C_WHITE, alignment=TA_CENTER)),
    Paragraph("<b>GOVERNANCE</b><br/>25% Weight",
              S("P", fontSize=8.5, fontName="Helvetica-Bold", textColor=C_WHITE, alignment=TA_CENTER)),
]]
pillar_t = Table(pillar_data, colWidths=[W/3]*3)
pillar_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (0,0), C_GREEN),
    ("BACKGROUND",    (1,0), (1,0), C_ROYAL),
    ("BACKGROUND",    (2,0), (2,0), C_MID_BLUE),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("GRID",          (0,0), (-1,-1), 1, C_WHITE),
]))
content.append(pillar_t)
content.append(Spacer(1, 0.18*inch))

# Summary distribution row
sum_data = [[
    Paragraph(f'<font color="#1E8449"><b>{leader_pct}%</b></font>'
              f'<br/><font color="#7F8C8D" size="7">ESG Leaders ({leaders} companies)</font>',
              S("SI", fontSize=13, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18)),
    Paragraph(f'<font color="#D4AC0D"><b>{average_pct}%</b></font>'
              f'<br/><font color="#7F8C8D" size="7">ESG Average ({average} companies)</font>',
              S("SI", fontSize=13, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18)),
    Paragraph(f'<font color="#C0392B"><b>{laggard_pct}%</b></font>'
              f'<br/><font color="#7F8C8D" size="7">ESG Laggards ({laggards} companies)</font>',
              S("SI", fontSize=13, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18)),
]]
sum_t = Table(sum_data, colWidths=[W/3]*3)
sum_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), C_OFF_WHITE),
    ("BOX",           (0,0), (-1,-1), 0.8, C_BORDER),
    ("GRID",          (0,0), (-1,-1), 0.5, C_BORDER),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 12),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
]))
content.append(sum_t)
content.append(PageBreak())

# ===========================================================
# PAGE 2  —  TOP 10 ESG COMPANIES
# ===========================================================

content.append(section_header("01", "TOP 10 ESG PERFORMING COMPANIES"))
content.append(spacer(0.1))
content.append(Paragraph(
    "The companies below represent the highest-performing ESG entities in our dataset, ranked by "
    "Weighted ESG Score. These organizations demonstrate industry-leading practices across "
    "environmental stewardship, social responsibility, and corporate governance.",
    S("B", fontSize=8.5, fontName="Helvetica", textColor=C_DARK_GRAY,
      leading=13, alignment=TA_JUSTIFY)))
content.append(spacer(0.1))

rows = [[th("Rank"), th("Company"), th("Industry"),
         th("Env"), th("Social"), th("Gov"), th("ESG Score"), th("Grade")]]
for i, row in top10.iterrows():
    rows.append([
        td(i+1, bold=True, color=C_ROYAL),
        td(row["Company"][:28],  align="LEFT"),
        td(row["Industry"][:22], color=C_MID_GRAY, align="LEFT", size=7),
        td(row["Env_Score"]),
        td(row["Social_Score"]),
        td(row["Gov_Score"]),
        td(row["Weighted_ESG_Score"], bold=True, color=C_GREEN),
        td(row["Total_Grade"], bold=True, color=C_ROYAL),
    ])

t10 = Table(rows, colWidths=[
    0.42*inch, 1.95*inch, 1.55*inch,
    0.52*inch, 0.52*inch, 0.52*inch, 0.74*inch, 0.53*inch
])
t10.setStyle(TableStyle(BASE_TS + alt_rows(10)))
content.append(t10)

# ── FIGURE 1 pushed down 3 lines ──
content.append(spacer(0.18))
content.append(framed_chart(
    CHART_TOP10, W, 2.9*inch,
    "Figure 1 — Top 10 Companies by Weighted ESG Score"))
content.append(PageBreak())

# ===========================================================
# PAGE 3  —  INDUSTRY COMPARISON
# ===========================================================

content.append(section_header("02", "INDUSTRY ESG COMPARISON"))
content.append(spacer(0.1))
content.append(Paragraph(
    "Average ESG scores aggregated by industry sector enable investors and stakeholders to identify "
    "high-performing sectors and benchmark individual companies against their industry peers.",
    S("B", fontSize=8.5, fontName="Helvetica", textColor=C_DARK_GRAY,
      leading=13, alignment=TA_JUSTIFY)))
content.append(spacer(0.1))

ind_rows = [[th("Industry", "LEFT"), th("Avg Env"), th("Avg Social"),
             th("Avg Gov"), th("Avg ESG"), th("Companies")]]
for _, row in top12_ind.iterrows():
    ind_rows.append([
        td(row["Industry"][:30], align="LEFT"),
        td(row["Avg_Env_Score"]),
        td(row["Avg_Social_Score"]),
        td(row["Avg_Gov_Score"]),
        td(row["Avg_ESG_Score"], bold=True, color=C_ROYAL),
        td(int(row["Company_Count"])),
    ])

ind_t = Table(ind_rows, colWidths=[
    2.55*inch, 0.84*inch, 0.84*inch, 0.84*inch, 0.84*inch, 0.79*inch
])
ind_t.setStyle(TableStyle(BASE_TS + alt_rows(12)))
content.append(ind_t)

# ── FIGURE 2 pushed down 3 lines ──
content.append(spacer(0.18))
content.append(framed_chart(
    CHART_IND, W, 2.75*inch,
    "Figure 2 — Top Industries by Average ESG Score"))
content.append(PageBreak())

# ===========================================================
# PAGE 4  —  KEY BUSINESS INSIGHTS (2-column grid)
# ===========================================================

content.append(section_header("03", "KEY BUSINESS INSIGHTS"))
content.append(spacer(0.1))
content.append(Paragraph(
    "The following insights are derived from the weighted ESG model applied across 722 companies "
    "spanning multiple industries, intended to support investment decision-making, ESG strategy "
    "planning, and sustainability reporting.",
    S("B", fontSize=8.5, fontName="Helvetica", textColor=C_DARK_GRAY,
      leading=13, alignment=TA_JUSTIFY)))
content.append(spacer(0.1))

insights = [
    ("Investment Opportunity",   C_GREEN,
     f"<b>{best_ind['Industry']}</b> ranks as the most ESG-friendly sector with an average score of "
     f"<b>{best_ind['Avg_ESG_Score']}</b>. Institutional investors seeking sustainable portfolios should "
     f"prioritize this sector."),

    ("High-Risk Sector",         C_RED,
     f"<b>{worst_ind['Industry']}</b> scores lowest on ESG metrics "
     f"(avg: <b>{worst_ind['Avg_ESG_Score']}</b>). Companies in this sector face elevated regulatory "
     f"and reputational risk."),

    ("Environmental Leader",     C_GREEN,
     f"<b>{best_env['Industry']}</b> leads in environmental performance "
     f"(avg Env Score: <b>{best_env['Avg_Env_Score']}</b>). This sector is well-positioned for "
     f"green bond financing and climate-focused mandates."),

    ("Social Responsibility",    C_ROYAL,
     f"<b>{best_soc['Industry']}</b> outperforms peers on social metrics "
     f"(avg Social Score: <b>{best_soc['Avg_Social_Score']}</b>), reflecting strong labor practices, "
     f"community engagement, and workforce diversity."),

    ("Governance Excellence",    C_MID_BLUE,
     f"<b>{best_gov['Industry']}</b> demonstrates the strongest governance standards "
     f"(avg Gov Score: <b>{best_gov['Avg_Gov_Score']}</b>), indicating transparent leadership, "
     f"board independence, and shareholder accountability."),

    ("Top ESG Company",          C_GOLD,
     f"<b>{top_co['Company']}</b> (Ticker: <b>{top_co['Ticker'].upper()}</b>) achieved the highest "
     f"Weighted ESG Score of <b>{top_co['Weighted_ESG_Score']}</b>, setting the benchmark for "
     f"sustainable corporate performance."),

    ("ESG Leader Concentration", C_GREEN,
     f"<b>{leader_pct}%</b> of companies ({leaders} out of {total}) qualify as ESG Leaders. This "
     f"signals a growing commitment to sustainability, but the majority still have room for improvement."),

    ("Laggard Risk Alert",       C_RED,
     f"<b>{laggard_pct}%</b> of companies ({laggards} out of {total}) are classified as ESG Laggards. "
     f"These firms carry heightened exposure to regulatory penalties, investor divestment, and "
     f"reputational damage."),

    ("Score Spread",             C_AMBER,
     f"ESG scores range from <b>{df['Weighted_ESG_Score'].min()}</b> to "
     f"<b>{df['Weighted_ESG_Score'].max()}</b> with an average of <b>{avg_score}</b>. "
     f"The wide spread indicates significant variation in ESG maturity across sectors."),

    ("Strategic Recommendation", C_MID_BLUE,
     f"Companies scoring below <b>40</b> should prioritize environmental compliance, supply chain "
     f"transparency, and board diversity as immediate ESG improvement levers. A 10-point ESG score "
     f"improvement can meaningfully impact access to green capital."),
]

half_w = (W - 0.15*cm) / 2

def insight_card(idx, title, accent, detail):
    """Bordered insight card with coloured accent badge."""
    hdr = Table([[
        Paragraph(f"<b>{idx:02d}</b>",
                  S("IB", fontSize=9, fontName="Helvetica-Bold",
                    textColor=C_WHITE, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b>",
                  S("IT", fontSize=8.5, fontName="Helvetica-Bold",
                    textColor=C_WHITE, alignment=TA_LEFT)),
    ]], colWidths=[0.32*inch, half_w - 0.32*inch - 0.1*cm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), accent),
        ("BACKGROUND",    (1,0), (1,0), C_DARK_BLUE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (1,0), (1,0), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (0,0), 0),
    ]))
    body = Table([[
        Paragraph(detail, S("ID", fontSize=7.8, fontName="Helvetica",
                            textColor=C_DARK_GRAY, leading=12, alignment=TA_JUSTIFY))
    ]], colWidths=[half_w - 0.1*cm])
    body.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), C_OFF_WHITE),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    wrapper = Table([[hdr], [body]], colWidths=[half_w - 0.1*cm])
    wrapper.setStyle(TableStyle([
        ("BOX",           (0,0), (-1,-1), 0.8, C_BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    return wrapper

grid_data = []
left_ins  = insights[:5]
right_ins = insights[5:]
for i in range(5):
    l = insight_card(i+1,  left_ins[i][0],  left_ins[i][1],  left_ins[i][2])
    r = insight_card(i+6,  right_ins[i][0], right_ins[i][1], right_ins[i][2])
    grid_data.append([l, r])

grid = Table(grid_data, colWidths=[half_w, half_w])
grid.setStyle(TableStyle([
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 4),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
content.append(grid)
content.append(PageBreak())

# ===========================================================
# PAGE 5  —  ESG DISTRIBUTION & HEATMAP
# ===========================================================

content.append(section_header("04", "ESG DISTRIBUTION & SCORE ANALYSIS"))
content.append(spacer(0.1))
content.append(Paragraph(
    "The ESG Category Distribution visualises the proportion of Leaders, Average, and Laggard "
    "companies across the 722-company dataset. The heatmap provides a cross-industry view of "
    "performance across all three ESG pillars, enabling rapid identification of sectoral strengths.",
    S("B", fontSize=8.5, fontName="Helvetica", textColor=C_DARK_GRAY,
      leading=13, alignment=TA_JUSTIFY)))
content.append(spacer(0.1))

# ── FIGURES 3 & 4 pushed down 3 lines ──
content.append(spacer(0.18))
content.append(side_by_side_charts(
    CHART_CAT,  "Figure 3 — ESG Category Distribution (722 Companies)",
    CHART_HEAT, "Figure 4 — ESG Pillar Heatmap by Industry",
    W, 3.1*inch))
content.append(spacer(0.16))

# Pillar stats table
content.append(Paragraph(
    "ESG PILLAR STATISTICS", S("Sub", fontSize=9, fontName="Helvetica-Bold",
                                textColor=C_MID_BLUE, spaceBefore=4, spaceAfter=4)))

pil_rows = [[th("Pillar"), th("Weight"), th("Top Industry"), th("Best Score"),
             th("Lowest Industry"), th("Interpretation", "LEFT")]]
pil_rows += [
    [td("Environmental", bold=True, color=C_GREEN), td("40%", bold=True),
     td(best_env["Industry"][:18], align="LEFT"), td(best_env["Avg_Env_Score"], bold=True, color=C_GREEN),
     td(worst_env["Industry"][:18], align="LEFT"), td("Primary driver of ESG score", align="LEFT")],

    [td("Social", bold=True, color=C_ROYAL), td("35%", bold=True),
     td(best_soc["Industry"][:18], align="LEFT"), td(best_soc["Avg_Social_Score"], bold=True, color=C_ROYAL),
     td(worst_soc["Industry"][:18], align="LEFT"), td("Community & labour practices", align="LEFT")],

    [td("Governance", bold=True, color=C_MID_BLUE), td("25%", bold=True),
     td(best_gov["Industry"][:18], align="LEFT"), td(best_gov["Avg_Gov_Score"], bold=True, color=C_MID_BLUE),
     td(worst_gov["Industry"][:18], align="LEFT"), td("Board accountability & transparency", align="LEFT")],
]
pil_t = Table(pil_rows, colWidths=[0.88*inch, 0.55*inch, 1.25*inch, 0.78*inch, 1.25*inch, 1.99*inch])
pil_t.setStyle(TableStyle(BASE_TS + alt_rows(3)))
content.append(pil_t)
content.append(spacer(0.14))

# Category breakdown table
content.append(Paragraph(
    "CATEGORY BREAKDOWN", S("Sub", fontSize=9, fontName="Helvetica-Bold",
                             textColor=C_MID_BLUE, spaceBefore=4, spaceAfter=4)))
cat_rows = [[th("Category"), th("Count"), th("Share (%)"), th("Score Range"), th("Risk Profile", "LEFT")]]
cat_rows += [
    [td("Leader",  bold=True, color=C_GREEN),  td(leaders),  td(f"{leader_pct}%",  bold=True, color=C_GREEN),
     td("≥ 60"),  td("Low ESG risk — sustainable investment grade", align="LEFT")],
    [td("Average", bold=True, color=C_AMBER),  td(average),  td(f"{average_pct}%", bold=True, color=C_AMBER),
     td("40–60"), td("Moderate ESG maturity — improvement capacity", align="LEFT")],
    [td("Laggard", bold=True, color=C_RED),    td(laggards), td(f"{laggard_pct}%", bold=True, color=C_RED),
     td("< 40"),  td("High ESG risk — regulatory exposure likely", align="LEFT")],
]
cat_t = Table(cat_rows, colWidths=[0.88*inch, 0.7*inch, 0.82*inch, 0.85*inch, 3.45*inch])
cat_t.setStyle(TableStyle(BASE_TS + alt_rows(3)))
content.append(cat_t)
content.append(PageBreak())

# ===========================================================
# PAGE 6  —  MACHINE LEARNING MODEL RESULTS
# ===========================================================

content.append(section_header("05", "MACHINE LEARNING MODEL RESULTS"))
content.append(spacer(0.1))
content.append(Paragraph(
    "A machine learning pipeline was trained to predict Weighted ESG Scores based on Environmental, "
    "Social, and Governance raw scores. Two algorithms were benchmarked — <b>Linear Regression</b> and "
    "<b>Random Forest Regressor</b> — evaluated on a held-out test set using R² and RMSE metrics.",
    S("B", fontSize=8.5, fontName="Helvetica", textColor=C_DARK_GRAY,
      leading=13, alignment=TA_JUSTIFY)))
content.append(spacer(0.1))

# ── FIGURES 5 & 6 pushed down 3 lines ──
content.append(spacer(0.18))
content.append(side_by_side_charts(
    CHART_ML,   "Figure 5 — Actual vs Predicted ESG Scores",
    CHART_FEAT, "Figure 6 — Feature Importance (Random Forest)",
    W, 3.0*inch))
content.append(spacer(0.14))

# Model metrics
content.append(Paragraph(
    "MODEL PERFORMANCE METRICS", S("Sub", fontSize=9, fontName="Helvetica-Bold",
                                    textColor=C_MID_BLUE, spaceBefore=4, spaceAfter=4)))
ml_rows = [[th("Model"), th("Algorithm"), th("R²"), th("Key Advantage", "LEFT"), th("Verdict", "LEFT")]]
ml_rows += [
    [td("Model 1", bold=True), td("Linear Regression"),
     td("~1.00", bold=True, color=C_GREEN),
     td("Perfect fit on training data", align="LEFT"),
     td("Baseline reference model", align="LEFT")],
    [td("Model 2", bold=True), td("Random Forest"),
     td("0.9961", bold=True, color=C_GREEN),
     td("Captures non-linear pillar interactions", align="LEFT"),
     td("Recommended for production use", align="LEFT")],
]
ml_t = Table(ml_rows, colWidths=[0.7*inch, 1.35*inch, 0.65*inch, 2.0*inch, 2.0*inch])
ml_t.setStyle(TableStyle(BASE_TS + alt_rows(2)))
content.append(ml_t)
content.append(spacer(0.12))

# Feature importance
content.append(Paragraph(
    "FEATURE IMPORTANCE SUMMARY", S("Sub", fontSize=9, fontName="Helvetica-Bold",
                                     textColor=C_MID_BLUE, spaceBefore=4, spaceAfter=4)))
fi_rows = [[th("ESG Pillar"), th("ML Importance"), th("Model Weight"), th("Calibration"), th("Strategic Implication", "LEFT")]]
fi_rows += [
    [td("Environmental", bold=True, color=C_GREEN), td("90.2%", bold=True, color=C_GREEN),
     td("40%"), td("Well-calibrated", color=C_GREEN, bold=True),
     td("Primary lever for ESG score improvement", align="LEFT")],
    [td("Social", bold=True, color=C_ROYAL), td("7.2%", bold=True, color=C_ROYAL),
     td("35%"), td("Under-weighted by ML", color=C_AMBER, bold=True),
     td("Qualitative factors limit measurability", align="LEFT")],
    [td("Governance", bold=True, color=C_MID_BLUE), td("2.6%", bold=True, color=C_MID_BLUE),
     td("25%"), td("Under-weighted by ML", color=C_AMBER, bold=True),
     td("Governance gains reflect long-term value", align="LEFT")],
]
fi_t = Table(fi_rows, colWidths=[1.1*inch, 1.0*inch, 0.88*inch, 1.15*inch, 2.57*inch])
fi_t.setStyle(TableStyle(BASE_TS + alt_rows(3)))
content.append(fi_t)
content.append(spacer(0.12))

content.append(callout_box(
    "<b>Key ML Findings:</b><br/>"
    "&bull; &nbsp;Environmental Score dominates predictive power (90.2%), confirming its 40% model "
    "weight is well-calibrated.<br/>"
    "&bull; &nbsp;Random Forest outperforms Linear Regression by capturing non-linear pillar "
    "interactions absent from a linear model.<br/>"
    "&bull; &nbsp;R&sup2; &gt; 0.99 indicates the model explains virtually all ESG score variance "
    "in the held-out test set."
))
content.append(PageBreak())

# ===========================================================
# PAGE 7  —  DISCLAIMER & NOTES
# ===========================================================

content.append(section_header("06", "DISCLAIMER & REPORT NOTES"))
content.append(spacer(0.18))

disc_items = [
    ("Scope",         "This report is generated for educational and analytical purposes only and does not constitute financial or investment advice."),
    ("Model",         "ESG scores are derived from a public dataset using a proprietary weighted model (E: 40%, S: 35%, G: 25%)."),
    ("Normalization", "All raw pillar scores are normalized to a 0–100 scale using Min-Max scaling across the dataset population before weighting."),
    ("Limitations",   "Past ESG performance does not guarantee future sustainability outcomes."),
    ("Coverage",      "Industry averages are based on companies in the dataset and may not represent the full market or global indices."),
    ("Technology",    "Auto-generated using Python: Pandas, Scikit-learn, ReportLab, Matplotlib, and Seaborn."),
    ("Data Source",   "Underlying ESG data sourced from the Kaggle ESG Ratings Dataset."),
    ("Confidentiality", "This report is intended for internal analysis. Recipients should exercise independent judgment before making any decisions."),
]

disc_rows = [[th("Topic"), th("Note", "LEFT")]]
for topic, note in disc_items:
    disc_rows.append([
        td(topic, bold=True, color=C_ROYAL),
        td(note, align="LEFT"),
    ])

disc_t = Table(disc_rows, colWidths=[1.25*inch, W - 1.25*inch])
disc_t.setStyle(TableStyle(BASE_TS + alt_rows(len(disc_items))))
content.append(disc_t)
content.append(spacer(0.3))

# Signature / report footer block
sig_data = [[
    Paragraph(
        f"<b>ESG Analytics Dashboard</b><br/>"
        f"Generated: {date.today().strftime('%B %d, %Y')}<br/>"
        f"Data Source: Kaggle ESG Ratings Dataset",
        S("SL", fontSize=8, fontName="Helvetica",
          textColor=C_DARK_GRAY, alignment=TA_LEFT, leading=13)),
    Paragraph(
        "<b>Model: Weighted ESG v1.0</b><br/>"
        "E: 40% &nbsp;|&nbsp; S: 35% &nbsp;|&nbsp; G: 25%<br/>"
        "Normalization: Min-Max scaling",
        S("SR", fontSize=8, fontName="Helvetica",
          textColor=C_DARK_GRAY, alignment=TA_RIGHT, leading=13)),
]]
sig_t = Table(sig_data, colWidths=[W/2, W/2])
sig_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), C_PALE_BLUE),
    ("BOX",           (0,0), (-1,-1), 1, C_ROYAL),
    ("LINEABOVE",     (0,0), (-1,0), 3, C_DARK_BLUE),
    ("ALIGN",         (0,0), (0,0), "LEFT"),
    ("ALIGN",         (1,0), (1,0), "RIGHT"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 12),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ("LEFTPADDING",   (0,0), (-1,-1), 14),
    ("RIGHTPADDING",  (0,0), (-1,-1), 14),
]))
content.append(sig_t)
content.append(spacer(0.18))

content.append(Paragraph(
    "This document is auto-generated and intended for internal analysis only. "
    "All data is sourced from publicly available ESG ratings. "
    "The authors assume no liability for decisions made based on this report.",
    S("LN", fontSize=7.5, fontName="Helvetica", textColor=C_MID_GRAY,
      alignment=TA_CENTER, leading=11)))

# ============================================================
# BUILD PDF
# ============================================================

print("=" * 58)
print("  GENERATING PROFESSIONAL ESG PDF REPORT...")
print("=" * 58)

doc = ESGDocTemplate(
    PDF_OUTPUT,
    pagesize=A4,
    rightMargin=MR,
    leftMargin=ML,
    topMargin=MT + 0.55*cm,
    bottomMargin=MB + 0.55*cm,
    title="ESG Score Analytics & Sustainability Report",
    author="ESG Analytics Dashboard",
)
doc.build(content)

print(f"\n{'=' * 58}")
print(f"  ✅  Report saved to: {PDF_OUTPUT}")
print(f"  Pages: Cover | Top 10 | Industry | Insights |")
print(f"         Distribution | ML Results | Disclaimer")
print(f"{'=' * 58}")