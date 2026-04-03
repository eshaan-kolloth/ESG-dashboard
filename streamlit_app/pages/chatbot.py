# ─────────────────────────────────────────────────────────────
# chatbot.py  —  Groq AI ESG Advice Page  (FIXED v7)
# ─────────────────────────────────────────────────────────────

import streamlit as st
import os
import re
from dotenv import load_dotenv
from groq import Groq

st.set_page_config(page_title="AI ESG Advisor", page_icon="🌿", layout="wide")

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE, ".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ─────────────────────────────────────────────────────────────
# NAVIGATION HANDLER — must be at the very top, before any widget
# ─────────────────────────────────────────────────────────────
if st.session_state.get("_nav_target"):
    target = st.session_state.pop("_nav_target")
    st.switch_page(target)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;0,800;1,700&family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --ink:    #0B1512; --forest: #0D4F3C; --emerald: #1A7A5E;
    --sage:   #3DAB7A; --fog:    #EEF5F1; --paper:   #F5F9F7;
    --amber:  #E8B84B; --gold:   #D4A847; --dim:     #5A7A6A;
    --border: #D6E8DF; --white:  #FFFFFF;
    --env:  #1A9E6E; --soc: #2E6FD8; --gov: #C8932A;
    --win:  #8B44CF; --road: #D05A1A; --gen: #4A6B80;
}

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background: var(--paper);
    background-image:
        radial-gradient(ellipse 70% 40% at 5% 0%,  rgba(13,79,60,0.07) 0%, transparent 65%),
        radial-gradient(ellipse 50% 30% at 95% 100%, rgba(76,175,138,0.05) 0%, transparent 55%);
}

.hero {
    background: linear-gradient(145deg, #071210 0%, #0D4F3C 52%, #122E24 100%);
    border-radius: 28px; padding: 50px 56px 44px;
    margin-bottom: 36px; position: relative; overflow: hidden;
    box-shadow: 0 28px 72px rgba(7,18,16,0.28);
}
.hero::before {
    content:''; position:absolute; top:-80px; right:-80px;
    width:380px; height:380px; border-radius:50%;
    background:radial-gradient(circle, rgba(61,171,122,0.20), transparent 65%);
    pointer-events:none;
}
.hero::after {
    content:''; position:absolute; bottom:0; right:0;
    width:260px; height:260px;
    background:radial-gradient(circle at bottom right, rgba(232,184,75,0.12), transparent 65%);
    pointer-events:none;
}
.hero-tag {
    display:inline-flex; align-items:center; gap:8px;
    background:rgba(61,171,122,0.18); border:1px solid rgba(61,171,122,0.32);
    border-radius:100px; padding:6px 18px;
    font-size:11px; font-weight:700; letter-spacing:2.5px;
    text-transform:uppercase; color:var(--sage); margin-bottom:22px;
}
.hero-title {
    font-family:'Cormorant Garamond',serif;
    font-size:52px; font-weight:800; color:#fff;
    line-height:1.1; margin-bottom:14px;
}
.hero-title em { color:var(--amber); font-style:normal; }
.hero-sub { font-size:15px; color:rgba(168,223,202,0.78); line-height:1.75; max-width:540px; }
.grade-pill {
    display:inline-flex; align-items:center; gap:10px;
    background:rgba(212,168,71,0.14); border:1px solid rgba(212,168,71,0.32);
    border-radius:100px; padding:9px 22px; margin-top:22px;
    font-size:13px; font-weight:700; color:var(--amber); letter-spacing:0.5px;
}
.score-strip {
    display:flex; gap:0; margin-top:30px; padding-top:26px;
    border-top:1px solid rgba(61,171,122,0.20);
}
.score-item { flex:1; text-align:center; position:relative; }
.score-item:not(:last-child)::after {
    content:''; position:absolute; right:0; top:50%;
    transform:translateY(-50%); width:1px; height:44px;
    background:rgba(61,171,122,0.22);
}
.sv { font-family:'Cormorant Garamond',serif; font-size:34px; font-weight:800; color:var(--amber); line-height:1; }
.sl { font-size:10px; color:rgba(168,223,202,0.60); text-transform:uppercase; letter-spacing:2px; font-weight:700; margin-top:5px; }

.sec-head { display:flex; align-items:center; gap:14px; margin:40px 0 22px; }
.sec-icon { width:50px; height:50px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }
.sec-title { font-family:'Cormorant Garamond',serif; font-size:28px; font-weight:800; color:var(--ink); }
.sec-desc  { font-size:13px; color:var(--dim); margin-top:2px; }
.sec-divider { flex:1; height:1px; background:linear-gradient(90deg,var(--border),transparent); margin-left:12px; }

.gen-wrap {
    background:white; border:2px dashed var(--border);
    border-radius:22px; padding:40px 36px; text-align:center; margin-bottom:20px;
}
.gen-wrap p { color:var(--dim); font-size:14px; margin-bottom:0; line-height:1.7; }

.adv-card {
    background:#fff; border-radius:22px; overflow:hidden;
    box-shadow:0 2px 20px rgba(11,21,18,0.06); border:1px solid var(--border);
    margin-bottom:20px;
}
.adv-stripe { height:5px; width:100%; }
.env-stripe  { background:linear-gradient(90deg,#1A9E6E,#A8DFCA); }
.soc-stripe  { background:linear-gradient(90deg,#2E6FD8,#A8C8F8); }
.gov-stripe  { background:linear-gradient(90deg,#C8932A,#F0CC78); }
.win-stripe  { background:linear-gradient(90deg,#8B44CF,#CFA8F8); }
.road-stripe { background:linear-gradient(90deg,#D05A1A,#F0A868); }
.gen-stripe  { background:linear-gradient(90deg,#4A6B80,#A8C4D8); }

.adv-header { display:flex; align-items:center; gap:16px; padding:24px 28px 16px; }
.adv-badge {
    font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:600; letter-spacing:1px;
    padding:5px 12px; border-radius:8px; flex-shrink:0;
}
.env-badge  { background:rgba(26,158,110,0.10); color:#1A9E6E; border:1px solid rgba(26,158,110,0.22); }
.soc-badge  { background:rgba(46,111,216,0.10); color:#2E6FD8; border:1px solid rgba(46,111,216,0.22); }
.gov-badge  { background:rgba(200,147,42,0.10);  color:#C8932A; border:1px solid rgba(200,147,42,0.22); }
.win-badge  { background:rgba(139,68,207,0.10);  color:#8B44CF; border:1px solid rgba(139,68,207,0.22); }
.road-badge { background:rgba(208,90,26,0.10);   color:#D05A1A; border:1px solid rgba(208,90,26,0.22); }
.gen-badge  { background:rgba(74,107,128,0.10);  color:#4A6B80; border:1px solid rgba(74,107,128,0.22); }

.adv-icon  { font-size:26px; }
.adv-title { font-family:'Cormorant Garamond',serif; font-size:21px; font-weight:800; color:var(--ink); line-height:1.2; }
.adv-body  { padding:0 28px 28px; }
.adv-intro { font-size:14px; color:#3A5248; line-height:1.9; margin-bottom:16px; padding-top:4px; }

.bullet-list { display:flex; flex-direction:column; gap:10px; }
.bullet-row {
    display:flex; gap:14px; align-items:flex-start;
    background:var(--fog); border-radius:12px; padding:14px 16px;
    font-size:14px; color:#2A4A3C; line-height:1.65;
}
.bullet-num {
    width:28px; height:28px; border-radius:8px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:600;
    margin-top:1px;
}
.env-num  { background:rgba(26,158,110,0.15); color:#1A9E6E; }
.soc-num  { background:rgba(46,111,216,0.15); color:#2E6FD8; }
.gov-num  { background:rgba(200,147,42,0.15); color:#C8932A; }
.win-num  { background:rgba(139,68,207,0.15); color:#8B44CF; }
.road-num { background:rgba(208,90,26,0.15);  color:#D05A1A; }
.gen-num  { background:rgba(74,107,128,0.15); color:#4A6B80; }
.bullet-label { font-weight:700; color:var(--ink); }

.quick-note {
    background:linear-gradient(140deg,#071210 0%,#0D4F3C 100%);
    border-radius:24px; padding:36px 40px; margin:32px 0 24px;
    position:relative; overflow:hidden;
}
.quick-note::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:260px; height:260px; border-radius:50%;
    background:radial-gradient(circle,rgba(232,184,75,0.15),transparent 65%);
    pointer-events:none;
}
.qn-label { font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:var(--sage); margin-bottom:6px; }
.qn-title { font-family:'Cormorant Garamond',serif; font-size:26px; font-weight:800; color:var(--amber); margin-bottom:24px; }
.qn-grid  { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.qn-item  {
    background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10);
    border-radius:14px; padding:14px 16px;
    display:flex; gap:12px; align-items:flex-start;
}
.qn-num  {
    font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:600;
    color:var(--amber); background:rgba(232,184,75,0.15);
    border-radius:6px; padding:3px 8px; flex-shrink:0; margin-top:1px; letter-spacing:1px;
}
.qn-text { font-size:13px; color:rgba(255,255,255,0.82); line-height:1.55; }

.legend {
    display:flex; flex-wrap:wrap; gap:10px;
    background:white; border:1px solid var(--border); border-radius:14px;
    padding:16px 20px; margin-top:14px;
}
.legend-dot { display:flex; align-items:center; gap:7px; font-size:12px; font-weight:600; color:var(--dim); }
.ldot { width:10px; height:10px; border-radius:50%; }

.stButton > button {
    font-family:'Syne',sans-serif !important; font-weight:700 !important;
    border-radius:12px !important; transition:all 0.2s !important; width:100% !important;
}
.btn-primary .stButton > button {
    background:linear-gradient(135deg,#0D4F3C,#1A7A5E) !important;
    color:white !important; font-size:15px !important; padding:13px 0 !important;
    border:none !important; box-shadow:0 6px 22px rgba(13,79,60,0.26) !important;
}
.btn-outline .stButton > button {
    background:transparent !important; color:var(--forest) !important;
    font-size:14px !important; padding:12px 0 !important;
    border:2px solid var(--border) !important;
}
.btn-outline .stButton > button:hover { background:var(--fog) !important; }

.success-bar {
    background:rgba(26,158,110,0.10); border:1px solid rgba(26,158,110,0.28);
    border-radius:12px; padding:14px 20px; color:var(--forest);
    font-size:14px; font-weight:600; display:flex; align-items:center; gap:10px; margin-bottom:28px;
}
.error-card {
    background:#FDE8E8; border-radius:16px; padding:24px;
    border-left:5px solid #C0392B; margin:20px 0; color:#5A1A1A; font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
company  = st.session_state.get('company_name', None)
env_s    = st.session_state.get('env_score',    None)
soc_s    = st.session_state.get('soc_score',    None)
gov_s    = st.session_state.get('gov_score',    None)
weighted = st.session_state.get('weighted',     None)
grade    = st.session_state.get('grade',        None)
industry = st.session_state.get('industry',     None)

# ─────────────────────────────────────────────────────────────
# SAFETY CHECK
# ─────────────────────────────────────────────────────────────
if company is None:
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">&#x1F916; AI Advisor</div>
        <div class="hero-title">No Data <em>Found</em></div>
        <div class="hero-sub">Please run the ESG Calculator first to generate your scores.</div>
    </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ No company data found! Please go to the Calculator page first.")
    _, c, _ = st.columns([1, 2, 1])
    with c:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("← Go to Calculator", use_container_width=True):
            st.session_state["_nav_target"] = "pages/calculator.py"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">&#x1F916; Powered by Groq AI &middot; llama-3.3-70b</div>
    <div class="hero-title">ESG <em>Improvement</em><br>Advisor</div>
    <div class="hero-sub">
        Personalised recommendations for <strong style="color:#fff">{company}</strong>
        &mdash; crafted specifically for the {industry} industry.
    </div>
    <div class="grade-pill">
        &#x1F4CA; Grade: {grade} &nbsp;&middot;&nbsp; Score: {weighted}/100 &nbsp;&middot;&nbsp; {industry}
    </div>
    <div class="score-strip">
        <div class="score-item"><div class="sv">{env_s}</div><div class="sl">&#x1F33F; Environmental</div></div>
        <div class="score-item"><div class="sv">{soc_s}</div><div class="sl">&#x1F91D; Social</div></div>
        <div class="score-item"><div class="sv">{gov_s}</div><div class="sl">&#x2696;&#xFE0F; Governance</div></div>
        <div class="score-item"><div class="sv">{weighted}</div><div class="sl">&#x1F4C8; Weighted</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
    if st.button("← Back to Calculator", key="top_back"):
        st.session_state["_nav_target"] = "pages/calculator.py"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SECTION METADATA
# ─────────────────────────────────────────────────────────────
SECTION_META = [
    ("OVERALL ASSESSMENT",     "📊", "gen-stripe",  "gen-badge",  "gen-num",  "01"),
    ("STRENGTHS TO CELEBRATE", "🏆", "win-stripe",  "win-badge",  "win-num",  "02"),
    ("ENVIRONMENTAL",          "🌿", "env-stripe",  "env-badge",  "env-num",  "03"),
    ("SOCIAL",                 "🤝", "soc-stripe",  "soc-badge",  "soc-num",  "04"),
    ("GOVERNANCE",             "⚖️", "gov-stripe",  "gov-badge",  "gov-num",  "05"),
    ("QUICK WINS",             "⚡", "win-stripe",  "win-badge",  "win-num",  "06"),
    ("LONG-TERM ROADMAP",      "🗺️", "road-stripe", "road-badge", "road-num", "07"),
    ("LONG TERM ROADMAP",      "🗺️", "road-stripe", "road-badge", "road-num", "07"),
    ("BENCHMARK TARGET",       "🎯", "gen-stripe",  "gen-badge",  "gen-num",  "08"),
]

def get_meta(title):
    t = title.upper()
    for kw, icon, stripe, badge, numcls, num in SECTION_META:
        if kw in t:
            return icon, stripe, badge, numcls, num
    return "📋", "gen-stripe", "gen-badge", "gen-num", "—"

# ─────────────────────────────────────────────────────────────
# GROQ CALL
# ─────────────────────────────────────────────────────────────
def get_groq_advice(company, industry, env_s, soc_s, gov_s, weighted, grade):
    if not GROQ_API_KEY:
        return None, "❌ GROQ_API_KEY not set in .env"
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""You are a senior ESG consultant. Write a structured ESG improvement report.

COMPANY: {company}
INDUSTRY: {industry}
GRADE: {grade}  |  OVERALL SCORE: {weighted}/100
Environmental: {env_s}/100  |  Social: {soc_s}/100  |  Governance: {gov_s}/100

OUTPUT FORMAT — follow this EXACTLY:

===SECTION: OVERALL ASSESSMENT===
2-3 sentences of plain text. No bullets. No markdown. No HTML.

===SECTION: STRENGTHS TO CELEBRATE===
2-3 sentences of plain text. No bullets. No markdown. No HTML.

===SECTION: PRIORITY IMPROVEMENTS — ENVIRONMENTAL===
1 sentence context.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.

===SECTION: PRIORITY IMPROVEMENTS — SOCIAL===
1 sentence context.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.

===SECTION: PRIORITY IMPROVEMENTS — GOVERNANCE===
1 sentence context.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.
BULLET: Short label | Full explanation sentence specific to {industry}.

===SECTION: QUICK WINS (Next 90 Days)===
1 sentence context.
BULLET: Short label | Full explanation sentence.
BULLET: Short label | Full explanation sentence.
BULLET: Short label | Full explanation sentence.
BULLET: Short label | Full explanation sentence.

===SECTION: LONG-TERM ROADMAP (1-3 Years)===
2-3 sentences of plain text. No bullets. No markdown. No HTML.

===SECTION: BENCHMARK TARGET===
2-3 sentences of plain text. No bullets. No markdown. No HTML.

STRICT RULES — breaking any rule makes the output unusable:
1. Section headers must be exactly ===SECTION: Title===
2. BULLET lines: "BULLET: label | explanation" — pipe character separates label from body
3. NO markdown symbols: no **, no ##, no *, no _
4. NO HTML at all: no <div>, no </div>, no <br>, no angle brackets whatsoever
5. Plain text only inside every section
6. Be specific to the {industry} sector throughout
"""
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an ESG expert. Output ONLY plain text following the exact format given. "
                        "CRITICAL: Never output any HTML tags. Never use angle brackets < or >. "
                        "Never write div, span, br or any HTML element names. "
                        "Never use markdown. Use BULLET: prefix only for bullet points."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2600,
            temperature=0.6
        )
        return resp.choices[0].message.content, None
    except Exception as e:
        return None, f"❌ Groq error: {e}"

# ─────────────────────────────────────────────────────────────
# HTML ESCAPE helper
# ─────────────────────────────────────────────────────────────
def _e(text: str) -> str:
    return (
        text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )

# ─────────────────────────────────────────────────────────────
# PARSER
# ─────────────────────────────────────────────────────────────
def parse_advice(raw: str):
    text = re.sub(r'<[^>]*>', '', raw)

    sections  = []
    current   = None
    sec_re    = re.compile(r'^={2,}\s*SECTION\s*:\s*(.+?)\s*={2,}$', re.IGNORECASE)
    bullet_re = re.compile(r'^BULLET\s*:\s*(.+?)\s*\|\s*(.+)$',      re.IGNORECASE)

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if '<' in line or '>' in line:
            continue
        if line.startswith(('#', '**', '* ')):
            continue

        m = sec_re.match(line)
        if m:
            if current:
                sections.append(current)
            current = {'title': m.group(1).strip(), 'intro_lines': [], 'bullets': []}
            continue

        if current is None:
            continue

        bm = bullet_re.match(line)
        if bm:
            current['bullets'].append((
                bm.group(1).strip().rstrip(':'),
                bm.group(2).strip()
            ))
            continue

        if not current['bullets']:
            current['intro_lines'].append(line)

    if current:
        sections.append(current)

    for s in sections:
        s['intro'] = ' '.join(s['intro_lines']).strip()
        del s['intro_lines']

    return sections

# ─────────────────────────────────────────────────────────────
# RENDER SECTIONS
# ─────────────────────────────────────────────────────────────
def render_sections(sections):
    for sec in sections:
        title   = sec['title']
        intro   = sec['intro']
        bullets = sec['bullets']
        icon, stripe_cls, badge_cls, num_cls, num_lbl = get_meta(title)

        intro_html = f'<p class="adv-intro">{_e(intro)}</p>' if intro else ''

        bullet_rows = ''
        for i, (label, body) in enumerate(bullets, 1):
            bullet_rows += (
                f'<div class="bullet-row">'
                f'<div class="bullet-num {num_cls}">{i:02d}</div>'
                f'<div><span class="bullet-label">{_e(label)}:</span>&nbsp;{_e(body)}</div>'
                f'</div>'
            )
        bullets_html = f'<div class="bullet-list">{bullet_rows}</div>' if bullet_rows else ''

        card = (
            f'<div class="adv-card">'
            f'<div class="adv-stripe {stripe_cls}"></div>'
            f'<div class="adv-header">'
            f'<span class="adv-badge {badge_cls}">#{num_lbl}</span>'
            f'<span class="adv-icon">{icon}</span>'
            f'<span class="adv-title">{_e(title)}</span>'
            f'</div>'
            f'<div class="adv-body">{intro_html}{bullets_html}</div>'
            f'</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# QUICK NOTE
# ─────────────────────────────────────────────────────────────
def render_quick_note(sections):
    all_bullets = []
    for sec in sections:
        all_bullets.extend(sec['bullets'])
    if not all_bullets:
        for sec in sections:
            if sec['intro']:
                all_bullets.append((sec['title'], sec['intro']))

    top = all_bullets[:8]
    if not top:
        return

    items_html = ''
    for i, (label, body) in enumerate(top, 1):
        short = (_e(body)[:82] + '…') if len(body) > 82 else _e(body)
        items_html += (
            f'<div class="qn-item">'
            f'<span class="qn-num">{i:02d}</span>'
            f'<span class="qn-text"><strong style="color:rgba(255,255,255,0.95)">{_e(label)}:</strong> {short}</span>'
            f'</div>'
        )

    st.markdown(
        f'<div class="quick-note">'
        f'<div class="qn-label">&#x26A1; Quick Reference</div>'
        f'<div class="qn-title">Key Takeaways at a Glance</div>'
        f'<div class="qn-grid">{items_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────
# GENERATE UI
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-icon" style="background:linear-gradient(135deg,#0D4F3C,#3DAB7A)">&#x2728;</div>
    <div>
        <div class="sec-title">Generate Your Improvement Plan</div>
        <div class="sec-desc">Groq AI will analyse your scores and build a personalised, actionable ESG roadmap</div>
    </div>
    <div class="sec-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="gen-wrap">
    <p>
        Click below to generate your <strong>full personalised ESG report</strong> &mdash; 8 colour-coded sections
        with actionable bullet points and a quick-reference summary panel.
        Powered by Groq&#39;s <strong>llama-3.3-70b-versatile</strong> model.
    </p>
</div>
""", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    generate = st.button("✨ Generate My ESG Improvement Plan", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="legend">
    <div class="legend-dot"><div class="ldot" style="background:#1A9E6E"></div> Environmental</div>
    <div class="legend-dot"><div class="ldot" style="background:#2E6FD8"></div> Social</div>
    <div class="legend-dot"><div class="ldot" style="background:#C8932A"></div> Governance</div>
    <div class="legend-dot"><div class="ldot" style="background:#8B44CF"></div> Quick Wins</div>
    <div class="legend-dot"><div class="ldot" style="background:#D05A1A"></div> Roadmap</div>
    <div class="legend-dot"><div class="ldot" style="background:#4A6B80"></div> General</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────
if generate:
    with st.spinner("🤖 Groq AI is building your personalised ESG plan… (5–10 seconds)"):
        advice, error = get_groq_advice(
            company, industry, env_s, soc_s, gov_s, weighted, grade
        )

    if error:
        st.markdown(
            f'<div class="error-card"><strong>Error:</strong><br>{error}</div>',
            unsafe_allow_html=True
        )
    else:
        st.session_state["_last_advice"] = advice

if st.session_state.get("_last_advice") and not generate:
    advice = st.session_state["_last_advice"]
    _show_results = True
elif generate and not st.session_state.get("_advice_error"):
    advice = st.session_state.get("_last_advice")
    _show_results = advice is not None
else:
    _show_results = False

# Re-check: show results if we just generated successfully
if generate and "advice" in dir() and advice and not (st.session_state.get("_last_advice") is None):
    _show_results = True

if _show_results and st.session_state.get("_last_advice"):
    advice = st.session_state["_last_advice"]

    st.markdown(
        '<div class="success-bar">&#x2705; &nbsp; Your ESG Improvement Plan is ready &mdash; explore all 8 sections below!</div>',
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="sec-head">
        <div class="sec-icon" style="background:linear-gradient(135deg,#8B6914,#E8B84B)">&#x1F4CB;</div>
        <div>
            <div class="sec-title">Your Personalised ESG Plan</div>
            <div class="sec-desc">Generated by Groq AI &middot; llama-3.3-70b-versatile</div>
        </div>
        <div class="sec-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    sections = parse_advice(advice)
    render_sections(sections)
    render_quick_note(sections)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── BOTTOM BUTTONS ────────────────────────────────────────
    # KEY FIX: Set _nav_target in session_state and call st.rerun().
    # The navigation handler at the TOP of the script then calls
    # st.switch_page() on the very next run — before any widgets
    # are drawn — which is the only reliable pattern in Streamlit.
    b1, b2, b3 = st.columns(3)

    with b1:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        if st.button("← Back to Calculator", use_container_width=True, key="back_bottom"):
            st.session_state["_nav_target"] = "pages/calculator.py"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        if st.button("🏠 Go to Home", use_container_width=True, key="home_bottom"):
            st.session_state["_nav_target"] = "app.py"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with b3:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🔄 Generate Again", use_container_width=True, key="regen_bottom"):
            st.session_state.pop("_last_advice", None)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)