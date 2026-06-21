from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st

# ----------------------------------------------------------------------------
# Alapadatok
# ----------------------------------------------------------------------------
START_DATE = date(2026, 5, 4)  # az IVF kezelés kezdete -> 1. hét eleje

HU_MONTHS = ["jan", "feb", "márc", "ápr", "máj", "jún",
             "júl", "aug", "szep", "okt", "nov", "dec"]

MILESTONES = {
    5:  ("🌱", "Embrió beágyazódás (~5. hét)"),
    6:  ("💓", "Szívhang hallható (ultrahang)"),
    8:  ("🔬", "Első ultrahang (általában)"),
    10: ("🧬", "NIPT / Duplex ultrahang lehetséges"),
    12: ("✨", "1. trimeszter vége · NT-mérés"),
    16: ("🦋", "Első mozgások érzékelhetők"),
    20: ("🔍", "Nagy morfológiai ultrahang"),
    24: ("🏥", "Életképességi határ elérve"),
    28: ("🌙", "3. trimeszter kezdete"),
    34: ("🎯", "Intenzív fejlődési fázis"),
    37: ("✅", "Érett terhesség (37. hét)"),
    40: ("🎉", "Várható szülési dátum"),
}

SIZES = {
    4:  ("🌾", "mákszem (~1 mm)"),
    5:  ("🍎", "almamag (~2 mm)"),
    6:  ("🫛", "lencse (~5 mm)"),
    7:  ("🫐", "áfonya (~1 cm)"),
    8:  ("🫘", "vesebab (~1,6 cm)"),
    9:  ("🍇", "szőlőszem (~2,3 cm)"),
    10: ("🍓", "eper (~3 cm)"),
    11: ("🍈", "füge (~4 cm)"),
    12: ("🍋", "lime (~5,4 cm)"),
    13: ("🫛", "borsóhüvely (~7,4 cm)"),
    14: ("🍋", "citrom (~8,7 cm)"),
    15: ("🍎", "alma (~10 cm)"),
    16: ("🥑", "avokádó (~11,6 cm)"),
    17: ("🍐", "körte (~13 cm)"),
    18: ("🫑", "paprika (~14 cm)"),
    19: ("🍅", "nagy paradicsom (~15 cm)"),
    20: ("🍌", "banán (~25 cm*)"),
    21: ("🥕", "sárgarépa (~27 cm)"),
    22: ("🥥", "kókuszdió (~28 cm)"),
    23: ("🍆", "padlizsán (~29 cm)"),
    24: ("🌽", "kukoricacső (~30 cm)"),
    25: ("🥬", "karalábé (~34 cm)"),
    26: ("🥒", "uborka (~35 cm)"),
    27: ("🥦", "karfiol (~36 cm)"),
    28: ("🍆", "nagy padlizsán (~37 cm)"),
    29: ("🎃", "sütőtök (~38 cm)"),
    30: ("🥬", "káposzta (~40 cm)"),
    31: ("🥥", "nagy kókusz (~41 cm)"),
    32: ("🍈", "sárgadinnye (~43 cm)"),
    33: ("🍍", "ananász (~44 cm)"),
    34: ("🍈", "kantalupdinnye (~45 cm)"),
    35: ("🍯", "mézdinnye (~46 cm)"),
    36: ("🥬", "római saláta (~47 cm)"),
    37: ("🥬", "mángold (~48,5 cm)"),
    38: ("🎃", "kisebb tök (~49,5 cm)"),
    39: ("🍉", "kisebb görögdinnye (~50,5 cm)"),
    40: ("🎃", "nagy tök (~51 cm)"),
    41: ("🍉", "görögdinnye (~51,5 cm)"),
    42: ("🍉", "nagy görögdinnye (~52 cm)"),
}

TRIM_COLORS = {
    1: {"bg": "#FEF0F2", "border": "#F4A4B0", "dot": "#D96B7A", "label": "#C4566A"},
    2: {"bg": "#FEF5ED", "border": "#F0C4A0", "dot": "#D4885A", "label": "#B87040"},
    3: {"bg": "#EDF5F0", "border": "#A8D4B4", "dot": "#5A9E6E", "label": "#3D7D52"},
}
TRIM_NAMES = {1: "1. trimeszter", 2: "2. trimeszter", 3: "3. trimeszter"}


def week_range(week: int):
    start = START_DATE + timedelta(days=(week - 1) * 7)
    end = start + timedelta(days=6)
    return start, end


def trimester_of(week: int) -> int:
    if week <= 13:
        return 1
    if week <= 27:
        return 2
    return 3


def fmt_short(d: date, force_year: bool = False) -> str:
    year = f"{d.year}. " if (d.year != 2026 or force_year) else ""
    return f"{year}{HU_MONTHS[d.month - 1]}. {d.day}."


def fmt_range(s: date, e: date) -> str:
    same_month = s.month == e.month and s.year == e.year
    if same_month:
        year = f"{s.year}. " if s.year != 2026 else ""
        return f"{year}{HU_MONTHS[s.month - 1]}. {s.day}–{e.day}."
    return f"{fmt_short(s)} – {fmt_short(e, e.year != 2026)}"


# ----------------------------------------------------------------------------
# Számítás
# ----------------------------------------------------------------------------
today = datetime.now(ZoneInfo("Europe/Budapest")).date()
days_along = (today - START_DATE).days
raw_week = days_along // 7 + 1
current_week = min(max(raw_week, 1), 42)
is_overdue = raw_week > 42
trimester = trimester_of(min(current_week, 40))
progress = min(max(round((current_week - 1) / 40 * 100), 0), 100)

cw_start, cw_end = week_range(current_week)
due_date = week_range(40)[1]
t1_start, t1_end = week_range(1)[0], week_range(13)[1]
t2_start, t2_end = week_range(14)[0], week_range(27)[1]
t3_start, t3_end = week_range(28)[0], week_range(40)[1]

# ----------------------------------------------------------------------------
# Beállítások / stílus
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Terhességi naptár", page_icon="🌸", layout="centered")

if "show_all" not in st.session_state:
    st.session_state.show_all = False

st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}

    .stApp {
        background-color: #FAF7F4;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif;
        color: #2D2420;
    }
    .block-container { padding-top: 1.6rem; padding-bottom: 2rem; max-width: 480px; }

    .hero {
        background: linear-gradient(145deg, #D96B7A 0%, #E8A08A 100%);
        border-radius: 20px;
        padding: 22px 20px;
        color: white;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: "";
        position: absolute; right: -20px; top: -20px;
        width: 120px; height: 120px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    .hero-eyebrow { font-size: 12px; opacity: 0.85; letter-spacing: 0.04em; text-transform: uppercase; }
    .hero-title { font-size: 26px; font-weight: 800; margin: 6px 0 4px; letter-spacing: -0.5px; }
    .hero-sub { font-size: 13px; opacity: 0.85; }
    .hero-date { font-size: 22px; font-weight: 700; margin-top: 2px; }
    .hero-pills { display: flex; gap: 10px; margin-top: 14px; position: relative; z-index: 1; }
    .hero-pill { background: rgba(255,255,255,0.18); border-radius: 8px; padding: 5px 8px; flex: 1; }
    .hero-pill-label { font-size: 10px; font-weight: 700; opacity: 0.8; }
    .hero-pill-range { font-size: 10px; opacity: 0.9; margin-top: 1px; }

    .card {
        background: white;
        border-radius: 16px;
        padding: 16px 16px 14px;
        margin-bottom: 16px;
    }
    .card-soft {
        background: white;
        border-radius: 14px;
        padding: 14px 14px 10px;
        margin-bottom: 16px;
    }

    .cw-top { display: flex; justify-content: space-between; align-items: flex-start; }
    .cw-tag { font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2px; }
    .cw-week { font-size: 32px; font-weight: 900; line-height: 1; }
    .cw-range { font-size: 13px; color: #9B8680; margin-top: 4px; }
    .cw-trim { font-size: 11px; color: #9B8680; text-align: right; }
    .cw-pct { font-size: 28px; font-weight: 800; text-align: right; }
    .cw-pct span { font-size: 14px; }
    .cw-pctlabel { font-size: 11px; color: #9B8680; text-align: right; }

    .progress-track { height: 6px; background: #F0EAE6; border-radius: 3px; margin-top: 12px; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 3px; }

    .fruit-box { margin-top: 10px; border-radius: 8px; padding: 7px 10px; }
    .fruit-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }
    .fruit-value { font-size: 14px; color: #2D2420; margin-top: 2px; }

    .ms-box { margin-top: 10px; border-radius: 8px; padding: 7px 10px; font-size: 13px; display: flex; align-items: center; gap: 6px; }
    .overdue-note { margin-top: 10px; border-radius: 8px; padding: 7px 10px; font-size: 13px; background: #FEF5ED; color: #B87040; }

    .qr-heading { font-size: 11px; font-weight: 700; color: #9B8680; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 10px; }
    .qr-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .qr-item { border-radius: 8px; padding: 8px 10px; }
    .qr-label { font-size: 11px; font-weight: 600; }
    .qr-date { font-size: 13px; font-weight: 700; color: #2D2420; margin-top: 1px; }

    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #D96B7A; border-color: #D96B7A; color: white;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #c65d6c; border-color: #c65d6c; color: white;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: white; color: #9B8680; border-color: #F0E8E4;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        border-color: #D96B7A; color: #D96B7A;
    }

    .trim-divider {
        font-size: 11px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
        padding: 12px 4px 4px; margin-top: 4px;
    }
    .week-card { border-radius: 10px; padding: 8px 12px; margin-bottom: 4px; }
    .week-top { display: flex; justify-content: space-between; align-items: center; }
    .week-left { display: flex; align-items: center; gap: 8px; }
    .week-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .week-num { font-size: 15px; }
    .badge { font-size: 10px; color: white; border-radius: 4px; padding: 1px 6px; font-weight: 700; }
    .week-dates { font-size: 12px; color: #9B8680; }
    .week-ms { margin-top: 5px; padding-left: 16px; font-size: 12px; display: flex; align-items: center; gap: 5px; }
    .week-size { margin-top: 5px; padding-left: 16px; font-size: 11.5px; color: #9B8680; }

    .footer-note { text-align: center; font-size: 11px; color: #BEB4B0; margin-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-eyebrow">IVF kezdete: {fmt_short(START_DATE, True)}</div>
        <div class="hero-title">Terhességi naptár</div>
        <div class="hero-sub">Várható szülési dátum (VSD)</div>
        <div class="hero-date">{fmt_short(due_date, True)}</div>
        <div class="hero-pills">
            <div class="hero-pill">
                <div class="hero-pill-label">1. trimeszter</div>
                <div class="hero-pill-range">{fmt_range(t1_start, t1_end)}</div>
            </div>
            <div class="hero-pill">
                <div class="hero-pill-label">2. trimeszter</div>
                <div class="hero-pill-range">{fmt_range(t2_start, t2_end)}</div>
            </div>
            <div class="hero-pill">
                <div class="hero-pill-label">3. trimeszter</div>
                <div class="hero-pill-range">{fmt_range(t3_start, t3_end)}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Jelen heti kártya
# ----------------------------------------------------------------------------
c = TRIM_COLORS[trimester]
fruit = SIZES.get(current_week)
milestone = MILESTONES.get(current_week)

fruit_html = ""
if fruit:
    f_emoji, f_text = fruit
    fruit_html = f"""
    <div class="fruit-box" style="background:{c['bg']};">
        <div class="fruit-label" style="color:{c['label']};">Gyümölcsben</div>
        <div class="fruit-value">{f_emoji} {f_text}</div>
    </div>
    """

milestone_html = ""
if milestone:
    m_icon, m_text = milestone
    milestone_html = f"""
    <div class="ms-box" style="background:{c['bg']}; color:{c['label']};">
        <span style="font-size:16px;">{m_icon}</span>{m_text}
    </div>
    """

overdue_html = ""
if is_overdue:
    overdue_html = """
    <div class="overdue-note">A 42. hét is letelt — addig is, jó eséllyel már meg is érkezett a baba! 🎉</div>
    """

st.markdown(
    f"""
    <div class="card" style="border: 2px solid {c['border']}; box-shadow: 0 4px 20px {c['border']}55;">
        <div class="cw-top">
            <div>
                <div class="cw-tag" style="color:{c['label']};">Most tartunk itt</div>
                <div class="cw-week" style="color:{c['dot']};">{current_week}. hét</div>
                <div class="cw-range">{fmt_range(cw_start, cw_end)}</div>
            </div>
            <div>
                <div class="cw-trim">{trimester}. trimeszter</div>
                <div class="cw-pct" style="color:{c['dot']};">{progress}<span>%</span></div>
                <div class="cw-pctlabel">haladás</div>
            </div>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width:{progress}%; background: linear-gradient(90deg, {c['dot']}, {c['border']});"></div>
        </div>
        {fruit_html}
        {milestone_html}
        {overdue_html}
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Fontos mérföldkövek - gyors áttekintés
# ----------------------------------------------------------------------------
key_weeks = [
    ("12. hét (NT)", 12),
    ("20. hét (nagy UH)", 20),
    ("24. hét (életképesség)", 24),
    ("28. hét (3. trim.)", 28),
    ("37. hét (érett)", 37),
    ("40. hét (VSD)", 40),
]
qr_items = ""
for label, w in key_weeks:
    wc = TRIM_COLORS[trimester_of(w)]
    w_start, _ = week_range(w)
    qr_items += f"""
    <div class="qr-item" style="background:{wc['bg']};">
        <div class="qr-label" style="color:{wc['label']};">{label}</div>
        <div class="qr-date">{fmt_short(w_start, w_start.year != 2026)}</div>
    </div>
    """

st.markdown(
    f"""
    <div class="card-soft">
        <div class="qr-heading">Fontos mérföldkövek</div>
        <div class="qr-grid">{qr_items}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Kattintható váltógombok
# ----------------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    clicked = st.button(
        "Mérföldkövek", use_container_width=True,
        type="primary" if not st.session_state.show_all else "secondary",
    )
    if clicked and st.session_state.show_all:
        st.session_state.show_all = False
        st.rerun()
with col2:
    clicked = st.button(
        "Mind a 42 hét", use_container_width=True,
        type="primary" if st.session_state.show_all else "secondary",
    )
    if clicked and not st.session_state.show_all:
        st.session_state.show_all = True
        st.rerun()

show_all = st.session_state.show_all

# ----------------------------------------------------------------------------
# Heti lista
# ----------------------------------------------------------------------------
rows = []
prev_trim = None
for w in range(1, 43):
    w_start, w_end = week_range(w)
    w_trim = trimester_of(w)
    w_is_current = w == current_week
    w_is_past = today > w_end
    w_milestone = MILESTONES.get(w)
    w_size = SIZES.get(w)

    if not (show_all or w_is_current or w_milestone or w == 40):
        continue

    wc = TRIM_COLORS[w_trim]

    if show_all and (w == 1 or (prev_trim is not None and prev_trim != w_trim)):
        rows.append(f'<div class="trim-divider" style="color:{wc["label"]};">{TRIM_NAMES[w_trim]}</div>')
    prev_trim = w_trim

    bg = wc["bg"] if w_is_current else "white"
    border = f"1.5px solid {wc['border']}" if w_is_current else "1px solid #F0E8E4"
    opacity = "0.5" if (w_is_past and not w_is_current) else "1"
    dot_color = wc["dot"] if w_is_current else ("#D4C8C4" if w_is_past else wc["border"])
    num_color = wc["dot"] if w_is_current else "#2D2420"
    num_weight = "800" if w_is_current else ("600" if w_milestone else "500")

    badges = ""
    if w_is_current:
        badges += f'<span class="badge" style="background:{wc["dot"]};">MOST</span>'
    if w == 40:
        badges += '<span class="badge" style="background:#5A9E6E;">VSD</span>'

    ms_line = ""
    if w_milestone:
        m_icon, m_text = w_milestone
        ms_line = f'<div class="week-ms" style="color:{wc["label"]};"><span>{m_icon}</span><span>{m_text}</span></div>'

    size_line = ""
    if w_size:
        s_emoji, s_text = w_size
        size_line = f'<div class="week-size">{s_emoji} {s_text}</div>'

    rows.append(
        f"""
        <div class="week-card" style="background:{bg}; border:{border}; opacity:{opacity};">
            <div class="week-top">
                <div class="week-left">
                    <div class="week-dot" style="background:{dot_color};"></div>
                    <span class="week-num" style="color:{num_color}; font-weight:{num_weight};">{w}. hét</span>
                    {badges}
                </div>
                <span class="week-dates">{fmt_range(w_start, w_end)}</span>
            </div>
            {ms_line}
            {size_line}
        </div>
        """
    )

st.markdown("".join(rows), unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Tájékoztató jellegű számítás · kérdéseiddel fordulj orvosodhoz</div>',
    unsafe_allow_html=True,
)
