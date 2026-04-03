import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="ESG Analytics Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    /* ── ROOT THEME ─────────────────────────────── */
    :root {
        --forest:   #0D4F3C;
        --emerald:  #1A7A5E;
        --sage:     #4CAF8A;
        --mint:     #A8DFCA;
        --gold:     #E8B84B;
        --amber:    #F0A500;
        --slate:    #1C2B3A;
        --ink:      #0F1923;
        --mist:     #F2F7F5;
        --cloud:    #FFFFFF;
        --silver:   #E4ECE8;
        --dim:      #6B8A7A;
    }

    /* ── GLOBAL ──────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background: linear-gradient(160deg, #EEF5F1 0%, #F5F9F7 50%, #EDF3F0 100%);
    }

    /* ── HEADER BAND ─────────────────────────────── */
    .header-band {
        background: linear-gradient(135deg, var(--forest) 0%, var(--slate) 60%, #0A2E45 100%);
        border-radius: 24px;
        padding: 48px 56px 40px 56px;
        margin-bottom: 36px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(13,79,60,0.25);
    }
    .header-band::before {
        content: '';
        position: absolute; top: -60px; right: -60px;
        width: 280px; height: 280px; border-radius: 50%;
        background: radial-gradient(circle, rgba(76,175,138,0.15) 0%, transparent 70%);
    }
    .header-band::after {
        content: '';
        position: absolute; bottom: -40px; left: 30%;
        width: 200px; height: 200px; border-radius: 50%;
        background: radial-gradient(circle, rgba(232,184,75,0.10) 0%, transparent 70%);
    }
    .header-logo {
        display: flex; align-items: center; gap: 18px; margin-bottom: 20px;
    }
    .logo-gem {
        width: 62px; height: 62px; border-radius: 18px;
        background: linear-gradient(135deg, var(--sage), var(--gold));
        display: flex; align-items: center; justify-content: center;
        font-size: 30px; box-shadow: 0 8px 24px rgba(76,175,138,0.4);
        flex-shrink: 0;
    }
    .logo-text .brand { font-family: 'Playfair Display', serif; font-size: 28px; color: white; font-weight: 900; line-height: 1; }
    .logo-text .tagline { font-size: 11px; color: var(--mint); font-weight: 600; letter-spacing: 3px; text-transform: uppercase; margin-top: 4px; }
    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: 46px; font-weight: 900; color: white;
        line-height: 1.1; margin-bottom: 12px;
    }
    .header-title span { color: var(--gold); }
    .header-subtitle { font-size: 16px; color: rgba(168,223,202,0.85); font-weight: 400; max-width: 520px; line-height: 1.6; }
    .header-pill {
        display: inline-block;
        background: rgba(76,175,138,0.2);
        border: 1px solid rgba(76,175,138,0.4);
        color: var(--mint); border-radius: 30px;
        padding: 6px 18px; font-size: 12px; font-weight: 600;
        letter-spacing: 1px; text-transform: uppercase; margin-top: 16px;
    }

    /* ── KPI CARDS ───────────────────────────────── */
    .kpi-card {
        background: var(--cloud);
        border-radius: 20px;
        padding: 28px 22px 22px 22px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        border: 1px solid var(--silver);
        position: relative; overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(0,0,0,0.10); }
    .kpi-card::after {
        content: ''; position: absolute;
        bottom: 0; left: 0; right: 0; height: 4px;
        border-radius: 0 0 20px 20px;
    }
    .kpi-forest::after  { background: linear-gradient(90deg, var(--forest), var(--sage)); }
    .kpi-gold::after    { background: linear-gradient(90deg, var(--amber), var(--gold)); }
    .kpi-blue::after    { background: linear-gradient(90deg, #2E6DA4, #5BA3D9); }
    .kpi-slate::after   { background: linear-gradient(90deg, var(--slate), #3A6B8A); }
    .kpi-icon { font-size: 32px; margin-bottom: 12px; display: block; }
    .kpi-num  { font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 900; color: var(--ink); line-height: 1; }
    .kpi-lbl  { font-size: 11px; font-weight: 700; color: var(--dim); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 8px; }
    .kpi-badge { font-size: 11px; font-weight: 600; color: var(--emerald); background: rgba(76,175,138,0.12); border-radius: 20px; padding: 2px 10px; margin-top: 10px; display: inline-block; }

    /* ── SECTION HEADERS ─────────────────────────── */
    .sec-head {
        display: flex; align-items: center; gap: 14px;
        margin: 40px 0 20px 0;
    }
    .sec-icon {
        width: 44px; height: 44px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; flex-shrink: 0;
    }
    .sec-icon-green { background: linear-gradient(135deg, var(--forest), var(--sage)); }
    .sec-icon-gold  { background: linear-gradient(135deg, #8B6914, var(--amber)); }
    .sec-icon-blue  { background: linear-gradient(135deg, #1A3A5C, #2E6DA4); }
    .sec-icon-fire  { background: linear-gradient(135deg, #8B1A1A, #C0392B); }
    .sec-title { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 900; color: var(--ink); }
    .sec-desc  { font-size: 13px; color: var(--dim); margin-top: 2px; font-weight: 400; }
    .sec-divider { flex: 1; height: 1px; background: linear-gradient(90deg, var(--silver), transparent); margin-left: 10px; }

    /* ── CHART BOXES ─────────────────────────────── */
    /* ── CHART HEADING BANNERS (full width, dark) ── */
    .chart-heading {
        width: 100%;
        border-radius: 16px 16px 0 0;
        padding: 18px 28px;
        display: flex; align-items: center;
        justify-content: space-between; gap: 16px;
        margin-bottom: 0;
        box-shadow: 0 4px 18px rgba(0,0,0,0.13);
    }
    .chart-heading-gold    { background: linear-gradient(120deg, #2C1A00 0%, #6B4200 60%, #8B6000 100%); }
    .chart-heading-teal    { background: linear-gradient(120deg, #052318 0%, #0A4A30 60%, #0D6140 100%); }
    .chart-heading-navy    { background: linear-gradient(120deg, #071828 0%, #0E3050 60%, #163D66 100%); }
    .chart-heading-crimson { background: linear-gradient(120deg, #1A0404 0%, #4A0E0E 60%, #6B1515 100%); }
    .ch-left {
        display: flex; align-items: center; gap: 16px; flex: 1;
    }
    .ch-icon {
        font-size: 26px; flex-shrink: 0;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    .ch-title {
        font-family: 'Playfair Display', serif;
        font-size: 20px; font-weight: 900;
        color: #FFFFFF; line-height: 1.2; letter-spacing: -0.3px;
    }
    .ch-sub {
        font-size: 11.5px; color: rgba(255,255,255,0.60);
        font-weight: 400; margin-top: 4px; letter-spacing: 0.2px;
    }
    .ch-pill {
        flex-shrink: 0; font-size: 10px; font-weight: 700;
        letter-spacing: 1.5px; text-transform: uppercase;
        border-radius: 20px; padding: 5px 14px;
        background: rgba(255,255,255,0.12);
        color: rgba(255,255,255,0.85);
        border: 1px solid rgba(255,255,255,0.22);
    }
    /* ── CHART FIGURE BOX (white card under heading) ── */
    .chart-fig-box {
        background: var(--cloud);
        border-radius: 0 0 16px 16px;
        padding: 20px 20px 16px 20px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        border: 1px solid var(--silver);
        border-top: none;
        margin-bottom: 8px;
    }

    /* ── TABLE STYLES ────────────────────────────── */
    .table-box {
        background: var(--cloud);
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 4px 28px rgba(0,0,0,0.07);
        border: 1px solid var(--silver);
    }
    div[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }

    /* ── CTA BLOCK ───────────────────────────────── */
    .cta-block {
        background: linear-gradient(135deg, var(--forest) 0%, var(--slate) 100%);
        border-radius: 24px; padding: 44px 48px;
        display: flex; align-items: center; justify-content: space-between;
        gap: 32px; box-shadow: 0 12px 40px rgba(13,79,60,0.20);
        margin: 40px 0;
    }
    .cta-copy .cta-title {
        font-family: 'Playfair Display', serif;
        font-size: 30px; font-weight: 900; color: white; margin-bottom: 10px;
    }
    .cta-copy .cta-sub { font-size: 15px; color: rgba(168,223,202,0.85); line-height: 1.6; }
    .cta-copy .cta-feats { display: flex; gap: 18px; margin-top: 18px; flex-wrap: wrap; }
    .cta-feat {
        display: flex; align-items: center; gap: 6px;
        color: var(--mint); font-size: 13px; font-weight: 600;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--gold), var(--amber)) !important;
        color: var(--ink) !important; font-size: 16px !important;
        font-weight: 800 !important; border-radius: 14px !important;
        padding: 16px 36px !important; border: none !important;
        letter-spacing: 0.5px; box-shadow: 0 8px 24px rgba(232,184,75,0.35) !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(232,184,75,0.50) !important;
    }

    /* ── FOOTER ──────────────────────────────────── */
    .footer {
        text-align: center; color: var(--dim);
        font-size: 13px; padding: 24px 0 10px 0;
        border-top: 1px solid var(--silver); margin-top: 20px;
    }
    .footer strong { color: var(--emerald); }

    /* ── BADGE PILLS ─────────────────────────────── */
    .badge-leader  { background:#d4f1e4; color:#0D4F3C; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-average { background:#fef3d0; color:#8B6914; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-laggard { background:#fde8e8; color:#8B1A1A; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }

    /* ── STAT ROW UNDER HEADER ───────────────────── */
    .stat-strip {
        display: flex; gap: 32px; flex-wrap: wrap;
        margin-top: 28px; padding-top: 24px;
        border-top: 1px solid rgba(76,175,138,0.25);
    }
    .stat-item { color: rgba(255,255,255,0.90); }
    .stat-item .sv { font-size: 22px; font-weight: 800; color: var(--gold); }
    .stat-item .sl { font-size: 11px; color: rgba(168,223,202,0.75); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-top: 2px; }
    .stat-sep { width: 1px; background: rgba(76,175,138,0.3); align-self: stretch; }
</style>
""", unsafe_allow_html=True)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_data():
    scored   = pd.read_csv(os.path.join(BASE, "esg_scored.csv"))
    industry = pd.read_csv(os.path.join(BASE, "esg_industry.csv"))
    return scored, industry

df, industry_df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
total    = len(df)
leaders  = len(df[df['ESG_Category'].str.strip().str.lower() == 'leader'])
avg_score = round(df['Weighted_ESG_Score'].mean(), 1)
top_score = round(df['Weighted_ESG_Score'].max(), 1)
industries = df['Industry'].nunique() if 'Industry' in df.columns else '—'

st.markdown(f"""
<div class="header-band">
    <div class="header-logo">
        <div class="logo-gem">🌱</div>
        <div class="logo-text">
            <div class="brand">ESG Analytics</div>
            <div class="tagline">Environmental · Social · Governance</div>
        </div>
    </div>
    <div class="header-title">Global ESG <span>Intelligence</span> Platform</div>
    <div class="header-subtitle">
        The world's most comprehensive ESG intelligence hub — tracking sustainability, 
        governance and social impact across leading corporations worldwide.
    </div>
    <div class="header-pill">📡 Live Dataset · {total} Companies · {industries} Industries</div>
    <div class="stat-strip">
        <div class="stat-item"><div class="sv">{total}</div><div class="sl">Companies Tracked</div></div>
        <div class="stat-sep"></div>
        <div class="stat-item"><div class="sv">{leaders}</div><div class="sl">ESG Leaders</div></div>
        <div class="stat-sep"></div>
        <div class="stat-item"><div class="sv">{avg_score}</div><div class="sl">Avg ESG Score</div></div>
        <div class="stat-sep"></div>
        <div class="stat-item"><div class="sv">{top_score}</div><div class="sl">Top Score</div></div>
        <div class="stat-sep"></div>
        <div class="stat-item"><div class="sv">{industries}</div><div class="sl">Sectors Covered</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class="kpi-card kpi-forest">
        <span class="kpi-icon">🏢</span>
        <div class="kpi-num">{total}</div>
        <div class="kpi-lbl">Companies Analysed</div>
        <span class="kpi-badge">Global Coverage</span>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="kpi-card kpi-gold">
        <span class="kpi-icon">🏆</span>
        <div class="kpi-num">{leaders}</div>
        <div class="kpi-lbl">ESG Leaders</div>
        <span class="kpi-badge">Top Tier</span>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="kpi-card kpi-blue">
        <span class="kpi-icon">📊</span>
        <div class="kpi-num">{avg_score}</div>
        <div class="kpi-lbl">Average ESG Score</div>
        <span class="kpi-badge">Benchmark</span>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="kpi-card kpi-slate">
        <span class="kpi-icon">⭐</span>
        <div class="kpi-num">{top_score}</div>
        <div class="kpi-lbl">Highest ESG Score</div>
        <span class="kpi-badge">Best in Class</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TOP 10 TABLE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-icon sec-icon-gold">🏆</div>
    <div>
        <div class="sec-title">Top 10 ESG Champions Worldwide</div>
        <div class="sec-desc">Ranked by composite weighted ESG score across all pillars</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

top10 = df.nsmallest(10, 'ESG_Rank')[['ESG_Rank','Company','Industry','Weighted_ESG_Score','ESG_Category']].reset_index(drop=True)
top10.columns = ['Rank', 'Company', 'Industry', 'ESG Score', 'Category']
top10['ESG Score'] = top10['ESG Score'].round(2)

st.dataframe(
    top10,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rank":      st.column_config.NumberColumn("🏅 Rank",     width="small"),
        "Company":   st.column_config.TextColumn("🏢 Company",   width="medium"),
        "Industry":  st.column_config.TextColumn("🏭 Industry",  width="medium"),
        "ESG Score": st.column_config.ProgressColumn("📈 ESG Score", min_value=0, max_value=100, format="%.2f"),
        "Category":  st.column_config.TextColumn("🎖️ Category", width="small"),
    }
)

# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW CHARTS — stacked vertically
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-icon sec-icon-green">📊</div>
    <div>
        <div class="sec-title">Performance at a Glance</div>
        <div class="sec-desc">ESG score leaders and category distribution across the dataset</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Chart 1 heading — full width dark banner ──
st.markdown("""
<div class="chart-heading chart-heading-gold">
    <div class="ch-left">
        <span class="ch-icon">🥇</span>
        <div>
            <div class="ch-title">Top 10 ESG Performing Companies</div>
            <div class="ch-sub">Highest composite scores among all tracked corporations</div>
        </div>
    </div>
    <span class="ch-pill">Rankings</span>
</div>
""", unsafe_allow_html=True)
# figure — medium width
_, fig1, _ = st.columns([1, 5, 1])
with fig1:
    st.markdown('<div class="chart-fig-box">', unsafe_allow_html=True)
    chart1 = os.path.join(BASE, "chart1_top10.png")
    if os.path.exists(chart1):
        st.image(chart1, use_container_width=True)
    else:
        st.info("Chart not found — place chart1_top10.png in the project root.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── Chart 2 heading — full width dark banner ──
st.markdown("""
<div class="chart-heading chart-heading-teal">
    <div class="ch-left">
        <span class="ch-icon">🎯</span>
        <div>
            <div class="ch-title">ESG Category Distribution</div>
            <div class="ch-sub">Proportion of Leaders, Averages and Laggards across all sectors</div>
        </div>
    </div>
    <span class="ch-pill">Distribution</span>
</div>
""", unsafe_allow_html=True)
# pie chart — narrower
_, fig2, _ = st.columns([2, 3, 2])
with fig2:
    st.markdown('<div class="chart-fig-box">', unsafe_allow_html=True)
    chart2 = os.path.join(BASE, "chart2_categories.png")
    if os.path.exists(chart2):
        st.image(chart2, use_container_width=True)
    else:
        st.info("Chart not found — place chart2_categories.png in the project root.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# INDUSTRY CHART
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-icon sec-icon-blue">🏭</div>
    <div>
        <div class="sec-title">Sector Sustainability Benchmarks</div>
        <div class="sec-desc">Average ESG score by industry — identifying sustainable leaders and improvement areas</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-heading chart-heading-navy">
    <div class="ch-left">
        <span class="ch-icon">📉</span>
        <div>
            <div class="ch-title">Industry-by-Industry ESG Comparison</div>
            <div class="ch-sub">Ranked average ESG score per sector across all tracked companies</div>
        </div>
    </div>
    <span class="ch-pill">Sectors</span>
</div>
""", unsafe_allow_html=True)
_, fig3, _ = st.columns([1, 5, 1])
with fig3:
    st.markdown('<div class="chart-fig-box">', unsafe_allow_html=True)
    chart3 = os.path.join(BASE, "chart3_industries.png")
    if os.path.exists(chart3):
        st.image(chart3, use_container_width=True)
    else:
        st.info("Chart not found — place chart3_industries.png in the project root.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEATMAP
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-icon sec-icon-fire">🔥</div>
    <div>
        <div class="sec-title">ESG Signal Heatmap</div>
        <div class="sec-desc">Intensity map of E · S · G pillars across industries</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-heading chart-heading-crimson">
    <div class="ch-left">
        <span class="ch-icon">🗺️</span>
        <div>
            <div class="ch-title">Cross-Industry ESG Heat Distribution</div>
            <div class="ch-sub">Colour intensity reflects score magnitude across Environmental · Social · Governance pillars</div>
        </div>
    </div>
    <span class="ch-pill">Heatmap</span>
</div>
""", unsafe_allow_html=True)
# heatmap — narrower
_, fig4, _ = st.columns([1, 4, 1])
with fig4:
    st.markdown('<div class="chart-fig-box">', unsafe_allow_html=True)
    chart4 = os.path.join(BASE, "chart4_heatmap.png")
    if os.path.exists(chart4):
        st.image(chart4, use_container_width=True)
    else:
        st.info("Chart not found — place chart4_heatmap.png in the project root.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CTA BLOCK
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-block">
    <div class="cta-copy">
        <div class="cta-title">How Does Your Company Score?</div>
        <div class="cta-sub">Enter your Environmental, Social and Governance pillars to receive an instant composite ESG rating, global percentile ranking, and AI-powered strategic recommendations.</div>
        <div class="cta-feats">
            <span class="cta-feat">✅ Instant Score</span>
            <span class="cta-feat">🌍 World Ranking</span>
            <span class="cta-feat">🤖 AI Advisory</span>
            <span class="cta-feat">📋 PDF Report</span>
        </div>
    </div>
""", unsafe_allow_html=True)

col_pad, col_btn, col_pad2 = st.columns([1, 2, 1])
with col_btn:
    if st.button("🚀  Calculate My ESG Score  →", use_container_width=True):
        st.switch_page("pages/calculator.py")

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌱 <strong>ESG Analytics Platform</strong> &nbsp;·&nbsp; Built with Python & Streamlit &nbsp;·&nbsp; 722 Global Companies &nbsp;·&nbsp; Real-time ESG Intelligence
</div>
""", unsafe_allow_html=True)