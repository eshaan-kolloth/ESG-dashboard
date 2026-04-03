# ─────────────────────────────────────────────────────────────
# calculator.py  —  ESG Score Calculator Page
# ─────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

st.set_page_config(page_title="ESG Calculator", page_icon="🧮", layout="wide")

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── ROOT ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(160deg, #EEF5F1 0%, #F5F9F7 50%, #EDF3F0 100%); }

/* ── STREAMLIT OVERRIDES ── */
.stTextInput label, .stSelectbox label, .stNumberInput label {
    color: #0F1923 !important; font-size: 13px !important;
    font-weight: 700 !important; letter-spacing: 0.4px !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border: 2px solid #C8DDD6 !important; border-radius: 12px !important;
    color: #0F1923 !important; font-size: 14px !important;
    font-weight: 500 !important; background: #FAFCFB !important;
    padding: 12px 16px !important; transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #0D4F3C !important;
    box-shadow: 0 0 0 4px rgba(13,79,60,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #A0B8AC !important; }
.stSelectbox > div > div {
    border: 2px solid #C8DDD6 !important; border-radius: 12px !important;
    background: #FAFCFB !important; color: #0F1923 !important; font-size: 14px !important;
}
.stSelectbox > div > div > div { color: #0F1923 !important; font-weight: 500 !important; }
.stNumberInput button {
    border-color: #C8DDD6 !important; color: #0D4F3C !important;
    background: #F0F7F4 !important; border-radius: 8px !important;
}
.stNumberInput button:hover { background: #0D4F3C !important; color: white !important; }

/* ── PAGE HEADER ── */
.page-header {
    background: linear-gradient(135deg, #0D4F3C 0%, #1C2B3A 55%, #0A2E45 100%);
    border-radius: 28px; padding: 48px 56px; margin-bottom: 36px;
    box-shadow: 0 24px 64px rgba(13,79,60,0.28);
    position: relative; overflow: hidden;
}
.page-header::before {
    content: ''; position: absolute; top: -80px; right: -80px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(76,175,138,0.18) 0%, transparent 70%);
}
.page-header::after {
    content: ''; position: absolute; bottom: -50px; left: 20%;
    width: 240px; height: 240px; border-radius: 50%;
    background: radial-gradient(circle, rgba(232,184,75,0.12) 0%, transparent 70%);
}
.ph-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(168,223,202,0.7); margin-bottom: 12px; }
.ph-title { font-family: 'Playfair Display', serif; font-size: 44px; font-weight: 900;
    color: white; margin-bottom: 10px; line-height: 1.1; }
.ph-title span { color: #E8B84B; font-style: italic; }
.ph-sub { font-size: 15px; color: rgba(168,223,202,0.82); line-height: 1.65; max-width: 540px; }
.ph-stats { display: flex; gap: 28px; flex-wrap: wrap; margin-top: 28px;
    padding-top: 24px; border-top: 1px solid rgba(76,175,138,0.22); }
.ph-stat .sv { font-size: 20px; font-weight: 800; color: #E8B84B; }
.ph-stat .sl { font-size: 10px; color: rgba(168,223,202,0.65); text-transform: uppercase;
    letter-spacing: 1.2px; font-weight: 600; margin-top: 2px; }
.ph-sep { width: 1px; background: rgba(76,175,138,0.25); align-self: stretch; }

/* ══════════════════════════════════════════
   🚨 RED WARNING BOX — HIGHLY VISIBLE
══════════════════════════════════════════ */
.warning-blast {
    background: linear-gradient(135deg, #6B0000 0%, #B71C1C 45%, #E53935 100%);
    border-radius: 20px; padding: 28px 32px;
    box-shadow:
        0 0 0 4px rgba(229,57,53,0.40),
        0 12px 40px rgba(183,28,28,0.55),
        inset 0 1px 0 rgba(255,255,255,0.15);
    display: flex; align-items: flex-start; gap: 22px;
    animation: warnPulse 1.8s ease-in-out infinite;
    margin: 18px 0 26px 0;
    position: relative; overflow: hidden;
}
.warning-blast::before {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 160px; height: 160px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
}
@keyframes warnPulse {
    0%, 100% {
        box-shadow: 0 0 0 4px rgba(229,57,53,0.40),
                    0 12px 40px rgba(183,28,28,0.55),
                    inset 0 1px 0 rgba(255,255,255,0.15);
    }
    50% {
        box-shadow: 0 0 0 8px rgba(229,57,53,0.20),
                    0 18px 56px rgba(183,28,28,0.70),
                    inset 0 1px 0 rgba(255,255,255,0.15);
    }
}
.wb-icon-wrap {
    background: rgba(0,0,0,0.25); border-radius: 14px;
    width: 58px; height: 58px; display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
    font-size: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.wb-body { flex: 1; }
.wb-title {
    font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 900;
    color: white; margin-bottom: 6px; letter-spacing: -0.3px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.wb-text {
    font-size: 14px; color: rgba(255,220,215,0.92); line-height: 1.6;
}
.wb-text strong { color: white; }

/* ── SECTION HEADS ── */
.sec-head { display: flex; align-items: center; gap: 14px; margin: 36px 0 18px 0; }
.sec-icon { width: 46px; height: 46px; border-radius: 15px;
    display: flex; align-items: center; justify-content: center; font-size: 21px; flex-shrink: 0; }
.sec-title { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 900; color: #0F1923; }
.sec-desc  { font-size: 13px; color: #6B8A7A; margin-top: 2px; }
.sec-divider { flex: 1; height: 1px; background: linear-gradient(90deg, #C8DDD6, transparent); margin-left: 12px; }

/* ── INPUT CARD ── */
.input-card {
    background: white; border-radius: 22px; padding: 36px;
    box-shadow: 0 4px 28px rgba(0,0,0,0.07); border: 1.5px solid #E4ECE8; margin-bottom: 24px;
}
.input-card-title {
    font-family: 'Playfair Display', serif; font-size: 19px; font-weight: 900; color: #0F1923;
    margin-bottom: 22px; padding-bottom: 14px;
    border-bottom: 2px solid #EEF5F1;
}
.field-label { font-size: 13px; font-weight: 700; color: #0F1923; margin-bottom: 8px;
    display: flex; align-items: center; gap: 6px; }
.fl-badge { background: linear-gradient(135deg, #EEF5F1, #D8EDDE); color: #1A7A5E;
    font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 20px;
    border: 1px solid rgba(26,122,94,0.2); }

/* ── TIPS STRIP ── */
.tips-strip { display: flex; gap: 10px; flex-wrap: wrap; margin: 0 0 28px 0; }
.tip-pill { background: white; border: 1.5px solid #DBE9E3; border-radius: 30px;
    padding: 8px 16px; font-size: 12px; font-weight: 600; color: #1A7A5E;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); }

/* ── PILLAR CARDS ── */
.pillar-card {
    background: white; border-radius: 20px; padding: 24px 20px 18px 20px;
    border: 1.5px solid #E4ECE8; margin-bottom: 10px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    position: relative; overflow: hidden;
}
.pillar-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
    border-radius: 20px 20px 0 0;
}
.pillar-env::before  { background: linear-gradient(90deg, #0D4F3C, #4CAF8A); }
.pillar-soc::before  { background: linear-gradient(90deg, #1A3A5C, #2E6DA4); }
.pillar-gov::before  { background: linear-gradient(90deg, #8B6914, #E8B84B); }
.pillar-emoji { font-size: 34px; display: block; margin-bottom: 8px; }
.pillar-name  { font-size: 15px; font-weight: 800; color: #0F1923; }
.pillar-desc  { font-size: 12px; color: #6B8A7A; margin-top: 5px; line-height: 1.6; }
.pillar-tags  { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
.pillar-range  { font-size: 11px; font-weight: 700; color: #1A7A5E; background: #EEF5F1;
    border-radius: 20px; padding: 3px 11px; }
.pillar-weight { font-size: 11px; font-weight: 700; color: #8B6914; background: #FEF3D0;
    border-radius: 20px; padding: 3px 11px; }

/* ── RESULTS ── */
.results-wrapper { background: white; border-radius: 28px; border: 1.5px solid #E4ECE8;
    box-shadow: 0 10px 48px rgba(13,79,60,0.12); overflow: hidden; margin-bottom: 28px; }
.results-top-bar { background: linear-gradient(135deg, #0D4F3C 0%, #1C2B3A 100%);
    padding: 16px 32px; display: flex; align-items: center; justify-content: space-between; }
.rtb-label { font-size: 11px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: rgba(168,223,202,0.75); }
.rtb-model { font-size: 11px; color: rgba(168,223,202,0.55); background: rgba(255,255,255,0.09);
    border-radius: 20px; padding: 4px 14px; }
.results-body { display: flex; align-items: stretch; }
.grade-panel { background: linear-gradient(175deg, #0D4F3C 0%, #0a3528 100%);
    padding: 40px 32px; min-width: 230px;
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }
.grade-company { font-size: 11px; color: rgba(168,223,202,0.45); text-align: center;
    letter-spacing: 2px; text-transform: uppercase; }
.grade-letter { font-family: 'Playfair Display', serif; font-size: 92px; font-weight: 900;
    color: #E8B84B; line-height: 1; text-shadow: 0 4px 24px rgba(232,184,75,0.3); }
.grade-score  { font-size: 15px; color: rgba(168,223,202,0.85); font-weight: 600; }
.grade-badge  { display: inline-block; margin-top: 6px; padding: 6px 20px; border-radius: 30px;
    font-size: 12px; font-weight: 700; letter-spacing: 1px; }
.cat-leader  { background: rgba(76,175,138,0.25); color: #A8DFCA; border: 1px solid rgba(76,175,138,0.4); }
.cat-average { background: rgba(232,184,75,0.20); color: #E8B84B; border: 1px solid rgba(232,184,75,0.4); }
.cat-laggard { background: rgba(192,57,43,0.20); color: #F1948A; border: 1px solid rgba(192,57,43,0.4); }
.stats-panel { flex: 1; padding: 28px; display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 16px; background: white; }
.stat-tile { background: linear-gradient(135deg, #F7FAF8, #F0F7F4); border-radius: 18px;
    padding: 20px; border: 1px solid #E0EDE7; display: flex; flex-direction: column; gap: 4px; }
.stat-tile .st-icon { font-size: 24px; margin-bottom: 6px; }
.stat-tile .st-num  { font-family: 'Playfair Display', serif; font-size: 32px;
    font-weight: 900; color: #0D4F3C; line-height: 1; }
.stat-tile .st-num.negative { color: #C0392B; }
.stat-tile .st-lbl  { font-size: 11px; font-weight: 700; color: #6B8A7A;
    text-transform: uppercase; letter-spacing: 1.2px; }
.stat-tile .st-sub  { font-size: 11px; color: #A0B8AC; margin-top: 2px; }

/* ── INSIGHTS ── */
.insight-box { background: white; border-radius: 18px; padding: 22px 26px;
    border-left: 5px solid #E8B84B; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    margin-bottom: 14px; transition: transform 0.2s, box-shadow 0.2s; }
.insight-box:hover { transform: translateX(4px); box-shadow: 0 6px 28px rgba(0,0,0,0.09); }
.insight-title { font-size: 14px; font-weight: 800; color: #0D4F3C; margin-bottom: 5px; }
.insight-text  { font-size: 13px; color: #3D5A4E; line-height: 1.65; }

/* ── AI BANNER ── */
.ai-advice-wrapper {
    background: linear-gradient(135deg, #0D4F3C 0%, #1C3A4A 100%);
    border-radius: 24px; padding: 40px 44px; margin: 32px 0 10px 0;
    border: 1px solid rgba(232,184,75,0.28);
    box-shadow: 0 16px 48px rgba(13,79,60,0.22);
    display: flex; align-items: center; gap: 36px;
    position: relative; overflow: hidden;
}
.ai-advice-wrapper::after {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 240px; height: 240px; border-radius: 50%;
    background: radial-gradient(circle, rgba(232,184,75,0.12) 0%, transparent 70%);
}
.ai-advice-icon { font-size: 56px; flex-shrink: 0; }
.ai-advice-text { flex: 1; }
.aat-label  { font-size: 10px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: rgba(232,184,75,0.72); margin-bottom: 8px; }
.aat-title  { font-family: 'Playfair Display', serif; font-size: 26px;
    font-weight: 900; color: white; margin-bottom: 8px; line-height: 1.2; }
.aat-title span { color: #E8B84B; font-style: italic; }
.aat-desc   { font-size: 13px; color: rgba(168,223,202,0.78); line-height: 1.65; max-width: 480px; }
.ai-chips   { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
.ai-chip    { background: rgba(255,255,255,0.10); border: 1px solid rgba(168,223,202,0.22);
    border-radius: 20px; padding: 5px 14px; font-size: 11px; font-weight: 600;
    color: rgba(168,223,202,0.80); }

/* ── CHART CARD ── */
.chart-card { background: white; border-radius: 22px; border: 1.5px solid #E4ECE8;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07); padding: 28px 28px 20px 28px; margin-bottom: 10px; }
.chart-card-title { font-family: 'Playfair Display', serif; font-size: 18px;
    font-weight: 900; color: #0F1923; margin-bottom: 4px; }
.chart-card-sub { font-size: 12px; color: #6B8A7A; margin-bottom: 18px; }

/* ── BUTTONS ── */
.ai-btn > button {
    background: linear-gradient(135deg, #E8B84B, #D4A03A) !important;
    color: #0F1923 !important; font-size: 15px !important; font-weight: 800 !important;
    border-radius: 14px !important; padding: 14px 0 !important; border: none !important;
    box-shadow: 0 8px 28px rgba(232,184,75,0.45) !important;
}
.back-btn > button {
    background: transparent !important; color: #0D4F3C !important;
    font-size: 14px !important; font-weight: 600 !important;
    border-radius: 10px !important; border: 2px solid #0D4F3C !important;
}
.stButton > button {
    background: linear-gradient(135deg, #0D4F3C, #1A7A5E) !important;
    color: white !important; font-size: 16px !important; font-weight: 800 !important;
    border-radius: 14px !important; padding: 14px 0 !important; border: none !important;
    box-shadow: 0 6px 20px rgba(13,79,60,0.25) !important;
}

/* hide streamlit default warning/info boxes */
div[data-testid="stAlert"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE, "esg_scored.csv"))

df = load_data()

# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
ENV_MIN, ENV_MAX = 200, 719
SOC_MIN, SOC_MAX = 160, 667
GOV_MIN, GOV_MAX = 75,  475

def normalize(value, min_val, max_val):
    return round((value - min_val) / (max_val - min_val) * 100, 2)

def get_grade(score):
    if score >= 80: return "AAA", "Leader",  "cat-leader"
    if score >= 70: return "AA",  "Leader",  "cat-leader"
    if score >= 60: return "A",   "Average", "cat-average"
    if score >= 50: return "BBB", "Average", "cat-average"
    if score >= 40: return "BB",  "Average", "cat-average"
    if score >= 30: return "B",   "Laggard", "cat-laggard"
    return               "CCC", "Laggard", "cat-laggard"

# ══════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <div class="ph-eyebrow">⚡ ESG Intelligence Platform</div>
    <div class="ph-title">ESG Score <span>Calculator</span></div>
    <div class="ph-sub">
        Enter your company's raw Environmental, Social and Governance scores.
        We'll calculate your weighted ESG rating, rank you among 722 real companies,
        and deliver AI-powered advice to help you improve.
    </div>
    <div class="ph-stats">
        <div class="ph-stat"><div class="sv">722</div><div class="sl">Companies in dataset</div></div>
        <div class="ph-sep"></div>
        <div class="ph-stat"><div class="sv">3</div><div class="sl">ESG pillars scored</div></div>
        <div class="ph-sep"></div>
        <div class="ph-stat"><div class="sv">40/35/25</div><div class="sl">E / S / G weights</div></div>
        <div class="ph-sep"></div>
        <div class="ph-stat"><div class="sv">🤖 AI</div><div class="sl">Groq-powered advice</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Dashboard"):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  COMPANY DETAILS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <div class="sec-icon" style="background:linear-gradient(135deg,#0D4F3C,#4CAF8A)">📋</div>
    <div>
        <div class="sec-title">Company Details</div>
        <div class="sec-desc">Tell us who we're analysing today</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tips-strip">
    <span class="tip-pill">💡 Scores from your ESG report</span>
    <span class="tip-pill">⚖️ Environmental carries 40% weight</span>
    <span class="tip-pill">🌍 Ranked against 722 real companies</span>
    <span class="tip-pill">🤖 AI advice unlocked after calculation</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-card-title">🏢 Who are we scoring today?</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="field-label">🏷️ Company Name <span class="fl-badge">REQUIRED</span></div>', unsafe_allow_html=True)
    company_name = st.text_input(
        "Company Name", placeholder="e.g. GreenTech Corp",
        label_visibility="collapsed", key="company_name_input"
    )
with col2:
    st.markdown('<div class="field-label">🏭 Industry Sector <span class="fl-badge">SELECT ONE</span></div>', unsafe_allow_html=True)
    industries = sorted(df['Industry'].dropna().unique().tolist())
    industry   = st.selectbox("Industry", industries, label_visibility="collapsed", key="industry_input")

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ESG PILLAR INPUTS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <div class="sec-icon" style="background:linear-gradient(135deg,#1A3A5C,#2E6DA4)">📊</div>
    <div>
        <div class="sec-title">ESG Pillar Scores</div>
        <div class="sec-desc">Raw scores directly from your ESG report</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("""
    <div class="pillar-card pillar-env">
        <span class="pillar-emoji">🌿</span>
        <div class="pillar-name">Environmental</div>
        <div class="pillar-desc">Carbon emissions, energy use, waste management, water and climate risk exposure.</div>
        <div class="pillar-tags">
            <span class="pillar-range">📏 200 – 719</span>
            <span class="pillar-weight">⚖️ 40% weight</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="field-label">✏️ Enter Environmental score</div>', unsafe_allow_html=True)
    env_score = st.number_input(
        "Environmental Score", min_value=ENV_MIN, max_value=ENV_MAX,
        value=400, step=1, label_visibility="collapsed", key="env_input"
    )

with p2:
    st.markdown("""
    <div class="pillar-card pillar-soc">
        <span class="pillar-emoji">🤝</span>
        <div class="pillar-name">Social</div>
        <div class="pillar-desc">Employee treatment, safety, diversity, labour rights and data privacy standards.</div>
        <div class="pillar-tags">
            <span class="pillar-range">📏 160 – 667</span>
            <span class="pillar-weight">⚖️ 35% weight</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="field-label">✏️ Enter Social score</div>', unsafe_allow_html=True)
    soc_score = st.number_input(
        "Social Score", min_value=SOC_MIN, max_value=SOC_MAX,
        value=350, step=1, label_visibility="collapsed", key="soc_input"
    )

with p3:
    st.markdown("""
    <div class="pillar-card pillar-gov">
        <span class="pillar-emoji">⚖️</span>
        <div class="pillar-name">Governance</div>
        <div class="pillar-desc">Board structure, executive pay, transparency and anti-corruption policies.</div>
        <div class="pillar-tags">
            <span class="pillar-range">📏 75 – 475</span>
            <span class="pillar-weight">⚖️ 25% weight</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="field-label">✏️ Enter Governance score</div>', unsafe_allow_html=True)
    gov_score = st.number_input(
        "Governance Score", min_value=GOV_MIN, max_value=GOV_MAX,
        value=250, step=1, label_visibility="collapsed", key="gov_input"
    )

# ══════════════════════════════════════════════════════════════
#  CALCULATE BUTTON
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    calculate = st.button("⚡ Calculate My ESG Score", use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  VALIDATION — custom blazing red warning
# ══════════════════════════════════════════════════════════════
if calculate:
    if not company_name.strip():
        st.markdown("""
        <div class="warning-blast">
            <div class="wb-icon-wrap">🚨</div>
            <div class="wb-body">
                <div class="wb-title">Company Name Required!</div>
                <div class="wb-text">
                    You must enter a <strong>Company Name</strong> before calculating your ESG score.
                    Please fill in the field above and click Calculate again.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── Calculate ──
    env_norm = normalize(env_score, ENV_MIN, ENV_MAX)
    soc_norm = normalize(soc_score, SOC_MIN, SOC_MAX)
    gov_norm = normalize(gov_score, GOV_MIN, GOV_MAX)
    weighted = round(env_norm * 0.40 + soc_norm * 0.35 + gov_norm * 0.25, 2)
    grade, category, cat_class = get_grade(weighted)

    st.session_state['calculated']   = True
    st.session_state['company_name'] = company_name
    st.session_state['industry']     = industry
    st.session_state['env_norm']     = env_norm
    st.session_state['soc_norm']     = soc_norm
    st.session_state['gov_norm']     = gov_norm
    st.session_state['weighted']     = weighted
    st.session_state['grade']        = grade
    st.session_state['category']     = category
    st.session_state['cat_class']    = cat_class
    st.session_state['env_score']    = env_norm
    st.session_state['soc_score']    = soc_norm
    st.session_state['gov_score']    = gov_norm

# ══════════════════════════════════════════════════════════════
#  SHOW RESULTS
# ══════════════════════════════════════════════════════════════
if st.session_state.get('calculated', False):

    company_name = st.session_state['company_name']
    industry     = st.session_state['industry']
    env_norm     = st.session_state['env_norm']
    soc_norm     = st.session_state['soc_norm']
    gov_norm     = st.session_state['gov_norm']
    weighted     = st.session_state['weighted']
    grade        = st.session_state['grade']
    category     = st.session_state['category']
    cat_class    = st.session_state['cat_class']

    ind_df      = df[df['Industry'] == industry]
    ind_avg     = round(ind_df['Weighted_ESG_Score'].mean(), 2) if len(ind_df) > 0 else 0
    vs_industry = round(weighted - ind_avg, 2)
    vs_arrow    = '▲' if vs_industry >= 0 else '▼'
    vs_word     = 'above' if vs_industry >= 0 else 'below'
    vs_class    = '' if vs_industry >= 0 else 'negative'
    better_than = len(df[df['Weighted_ESG_Score'] < weighted])
    percentile  = round((better_than / len(df)) * 100, 1)
    rank_pos    = len(df[df['Weighted_ESG_Score'] > weighted]) + 1

    st.markdown("""
    <div class="sec-head" style="margin-top:44px">
        <div class="sec-icon" style="background:linear-gradient(135deg,#8B6914,#E8B84B)">🏅</div>
        <div>
            <div class="sec-title">Your ESG Results</div>
            <div class="sec-desc">Weighted model — Environmental 40% · Social 35% · Governance 25%</div>
        </div>
        <div class="sec-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="results-wrapper">
        <div class="results-top-bar">
            <span class="rtb-label">🏢 {company_name}</span>
            <span class="rtb-model">Env 40% · Social 35% · Gov 25%</span>
        </div>
        <div class="results-body">
            <div class="grade-panel">
                <div class="grade-company">{company_name.upper()}</div>
                <div class="grade-letter">{grade}</div>
                <div class="grade-score">Score: <strong>{weighted}</strong> / 100</div>
                <div class="grade-badge {cat_class}">{category}</div>
            </div>
            <div class="stats-panel">
                <div class="stat-tile">
                    <span class="st-icon">🌍</span>
                    <div class="st-num">#{rank_pos}</div>
                    <div class="st-lbl">World Rank</div>
                    <div class="st-sub">out of 722 companies</div>
                </div>
                <div class="stat-tile">
                    <span class="st-icon">📈</span>
                    <div class="st-num">{percentile}%</div>
                    <div class="st-lbl">Percentile</div>
                    <div class="st-sub">better than {better_than} companies</div>
                </div>
                <div class="stat-tile">
                    <span class="st-icon">🌿</span>
                    <div class="st-num">{env_norm}</div>
                    <div class="st-lbl">Environmental</div>
                    <div class="st-sub">normalised / 100</div>
                </div>
                <div class="stat-tile">
                    <span class="st-icon">🏭</span>
                    <div class="st-num {vs_class}">{vs_arrow} {abs(vs_industry)}</div>
                    <div class="st-lbl">vs Industry Avg</div>
                    <div class="st-sub">{vs_word} {industry[:22]} avg</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts ──
    st.markdown("""
    <div class="sec-head" style="margin-top:8px">
        <div class="sec-icon" style="background:linear-gradient(135deg,#1A3A5C,#2E6DA4)">📊</div>
        <div>
            <div class="sec-title">How You Compare</div>
            <div class="sec-desc">Your score vs all 722 companies · pillar-by-pillar vs your industry</div>
        </div>
        <div class="sec-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-card-title">📍 Score Distribution — You vs The World</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-card-sub">All 722 companies in mint · {company_name} highlighted in gold · dashed lines show averages</div>', unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.patch.set_facecolor('white')
    all_scores = df['Weighted_ESG_Score'].dropna()

    ax1 = axes[0]
    ax1.set_facecolor('#F7FAF8')
    n, bins, patches = ax1.hist(all_scores, bins=28, color='#A8DFCA', edgecolor='white', linewidth=0.7, zorder=2)
    for patch, left_edge in zip(patches, bins[:-1]):
        if abs((left_edge + (bins[1] - bins[0]) / 2) - weighted) < 4:
            patch.set_facecolor('#E8B84B')
            patch.set_edgecolor('#C89A30')
            patch.set_linewidth(1.5)
    ax1.axvline(weighted,          color='#E8B84B', linewidth=2.5, linestyle='-',  zorder=5, label=f'{company_name}: {weighted}')
    ax1.axvline(ind_avg,           color='#2E6DA4', linewidth=1.8, linestyle='--', zorder=4, label=f'Industry avg: {ind_avg}')
    ax1.axvline(all_scores.mean(), color='#C0392B', linewidth=1.5, linestyle=':',  zorder=4, label=f'Global avg: {round(all_scores.mean(),1)}')
    ax1.set_xlabel('ESG Score', fontsize=10, color='#6B8A7A', labelpad=8)
    ax1.set_ylabel('Number of Companies', fontsize=10, color='#6B8A7A', labelpad=8)
    ax1.set_title('Score Distribution', fontsize=13, fontweight='bold', color='#0F1923', pad=12)
    ax1.legend(fontsize=8.5, frameon=True, framealpha=0.9, loc='upper left')
    ax1.spines[['top','right']].set_visible(False)
    ax1.spines[['left','bottom']].set_color('#E4ECE8')
    ax1.tick_params(colors='#6B8A7A', labelsize=9)
    ax1.grid(axis='y', color='#E4ECE8', linewidth=0.6, zorder=1)

    ax2 = axes[1]
    ax2.set_facecolor('#F7FAF8')
    ind_env_norm = round(ind_df['Env_Norm'].mean(),    2) if len(ind_df) > 0 else 50
    ind_soc_norm = round(ind_df['Social_Norm'].mean(), 2) if len(ind_df) > 0 else 50
    ind_gov_norm = round(ind_df['Gov_Norm'].mean(),    2) if len(ind_df) > 0 else 50

    labels    = ['Environmental\n(40%)', 'Social\n(35%)', 'Governance\n(25%)']
    your_vals = [env_norm, soc_norm, gov_norm]
    ind_vals  = [ind_env_norm, ind_soc_norm, ind_gov_norm]
    x         = np.arange(len(labels))
    width     = 0.34

    bars1 = ax2.bar(x - width/2, your_vals, width, color=['#1A7A5E','#2E6DA4','#E8B84B'],
                    edgecolor='white', linewidth=0.8, zorder=3, label=company_name)
    bars2 = ax2.bar(x + width/2, ind_vals,  width, color='#D0E8DC',
                    edgecolor='white', linewidth=0.8, zorder=3, label='Industry Avg')

    for bar in bars1:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 1, f'{h:.0f}',
                 ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0F1923')
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 1, f'{h:.0f}',
                 ha='center', va='bottom', fontsize=8.5, color='#6B8A7A')

    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9.5, color='#0F1923', fontweight='600')
    ax2.set_ylabel('Normalised Score (0–100)', fontsize=10, color='#6B8A7A', labelpad=8)
    ax2.set_title(f'You vs {industry[:22]}', fontsize=13, fontweight='bold', color='#0F1923', pad=12)
    ax2.set_ylim(0, 115)
    ax2.legend(fontsize=9, frameon=True, framealpha=0.9)
    ax2.spines[['top','right']].set_visible(False)
    ax2.spines[['left','bottom']].set_color('#E4ECE8')
    ax2.tick_params(colors='#6B8A7A', labelsize=9)
    ax2.grid(axis='y', color='#E4ECE8', linewidth=0.6, zorder=1)

    plt.tight_layout(pad=2.0)
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Insights ──
    st.markdown("""
    <div class="sec-head" style="margin-top:10px">
        <div class="sec-icon" style="background:linear-gradient(135deg,#0D4F3C,#4CAF8A)">💡</div>
        <div>
            <div class="sec-title">Key Insights</div>
            <div class="sec-desc">Personalised observations based on your scores</div>
        </div>
        <div class="sec-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    pillars_dict = {'Environmental': env_norm, 'Social': soc_norm, 'Governance': gov_norm}
    weakest      = min(pillars_dict, key=pillars_dict.get)
    strongest    = max(pillars_dict, key=pillars_dict.get)

    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">🏆 Strongest Pillar — {strongest}</div>
        <div class="insight-text">Your {strongest} score of <strong>{pillars_dict[strongest]}</strong> is your best ESG dimension. Keep maintaining this — it's a real competitive advantage in the {industry} sector.</div>
    </div>
    <div class="insight-box" style="border-left-color:#C0392B">
        <div class="insight-title">⚠️ Weakest Pillar — {weakest}</div>
        <div class="insight-text">Your {weakest} score of <strong>{pillars_dict[weakest]}</strong> needs the most attention. Focus improvement efforts here first for the biggest overall ESG impact.</div>
    </div>
    <div class="insight-box" style="border-left-color:#2E6DA4">
        <div class="insight-title">🏭 Industry Standing — {industry}</div>
        <div class="insight-text">The average ESG score in your industry is <strong>{ind_avg}</strong>. You are <strong>{vs_word}</strong> the industry average by <strong>{abs(vs_industry)} points</strong>.</div>
    </div>
    <div class="insight-box" style="border-left-color:#4CAF8A">
        <div class="insight-title">🌍 Global Ranking</div>
        <div class="insight-text">You rank <strong>#{rank_pos}</strong> out of 722 companies worldwide, scoring better than <strong>{percentile}%</strong> of all tracked companies.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── AI Banner ──
    st.markdown(f"""
    <div class="ai-advice-wrapper">
        <div class="ai-advice-icon">🤖</div>
        <div class="ai-advice-text">
            <div class="aat-label">✦ Powered by Groq AI</div>
            <div class="aat-title">Want <span>personalised advice</span> to boost your score?</div>
            <div class="aat-desc">
                Our AI will analyse your <strong style="color:#E8B84B">{grade}</strong> rating,
                pinpoint your weakest pillar, and give you specific actionable steps
                tailored to the <strong style="color:#A8DFCA">{industry}</strong> industry.
            </div>
            <div class="ai-chips">
                <span class="ai-chip">📋 Tailored to {industry[:20]}</span>
                <span class="ai-chip">🎯 Focused on {weakest}</span>
                <span class="ai-chip">⚡ Instant recommendations</span>
                <span class="ai-chip">🏆 Path to next grade</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    _, ai_col, _ = st.columns([1, 2, 1])
    with ai_col:
        st.markdown('<div class="ai-btn">', unsafe_allow_html=True)
        if st.button("🤖 Get AI Advice from Groq", use_container_width=True):
            st.switch_page("pages/chatbot.py")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)