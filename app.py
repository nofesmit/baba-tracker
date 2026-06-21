import math
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st

# ----------------------------------------------------------------------------
# Alapadatok
# ----------------------------------------------------------------------------
START_DATE = date(2026, 5, 4)                 # az IVF kezelés kezdete -> 1. hét eleje
DUE_DATE = START_DATE + timedelta(days=279)   # a 40. hét vége

HU_MONTHS = ["jan", "feb", "márc", "ápr", "máj", "jún",
             "júl", "aug", "szep", "okt", "nov", "dec"]

MILESTONES = {
    5:  ("🌱", "Beágyazódás", "Az embrió ezen a héten ágyazódik be a méhnyálkahártyába."),
    6:  ("💓", "Szívhang", "Ultrahangon már hallható lehet a szívhang."),
    8:  ("🔬", "Első ultrahang", "Az első részletes vizsgálat ideje."),
    10: ("🧬", "Korai szűrés", "Innentől elérhető a NIPT / korai szűrővizsgálat."),
    12: ("✨", "1. trimeszter vége", "NT-mérés, a kockázatok jelentősen csökkennek."),
    16: ("🦋", "Első mozgások", "Hamarosan érzékelhetővé válik a baba mozgása."),
    20: ("🔍", "Morfológiai UH", "Nagy részletességű szűrő ultrahang."),
    24: ("🏥", "Életképességi határ", "A magzat elérte az életképesség orvosi határát."),
    28: ("🌙", "3. trimeszter", "Kezdődik az utolsó szakasz."),
    34: ("🎯", "Erős fejlődés", "Intenzív súlygyarapodás és érés zajlik."),
    37: ("✅", "Érett terhesség", "A baba innentől éretten születhetne."),
    40: ("🎉", "Várható szülés", "A kiszámított határnap."),
}

SIZES = {
    4:  ("🟤", "mákszem", "🐜", "hangya"),
    5:  ("⚪", "szezámmag", "🐞", "katicabogár"),
    6:  ("🫘", "lencse", "🐭", "egér"),
    7:  ("🫐", "áfonya", "🐹", "hörcsög"),
    8:  ("🍇", "szőlőszem", "🐸", "béka"),
    9:  ("🍒", "cseresznye", "🐤", "kiscsibe"),
    10: ("🍓", "nagy eper", "🐰", "törpenyúl"),
    11: ("🫒", "fige", "🦔", "sündisznó"),
    12: ("🟢", "lime", "🐿️", "mókus"),
    13: ("🍑", "őszibarack", "🐦", "papagáj"),
    14: ("🍋", "citrom", "🐈", "kiscica"),
    15: ("🍎", "alma", "🐇", "üregi nyúl"),
    16: ("🥑", "avokádó", "🐕", "kiskutya"),
    17: ("🍐", "körte", "🦝", "mosómedve"),
    18: ("🫑", "paprika", "🦊", "rókakölyök"),
    19: ("🥭", "mangó", "🐢", "teknős"),
    20: ("🍌", "banán", "🐧", "pingvinfióka"),
    21: ("🥕", "sárgarépa", "🦦", "vidra"),
    22: ("🥒", "cukkini", "🦉", "bagolyfióka"),
    23: ("🍈", "grapefruit", "🐑", "báránykölyök"),
    24: ("🌽", "kukoricacső", "🐖", "kismalac"),
    25: ("🥦", "karfiol", "🦫", "hódkölyök"),
    26: ("🥬", "fejes saláta", "🦌", "őzgida"),
    27: ("🍆", "padlizsán", "🐐", "kecskegida"),
    28: ("🎃", "kis sütőtök", "🐻", "medvebocs"),
    29: ("🥥", "kókusz", "🦘", "kengurubébi"),
    30: ("🍍", "ananász", "🐼", "pandabocs"),
    31: ("🍈", "sárgadinnye", "🐯", "tigriskölyök"),
    32: ("🍈", "nagy sárgadinnye", "🦁", "oroszlánkölyök"),
    33: ("🎃", "nagy sütőtök", "🐨", "koalabocs"),
    34: ("🥥", "nagy kókusz", "🐘", "elefántborjú"),
    35: ("🍉", "kis görögdinnye", "🐂", "borjú"),
    36: ("🍉", "görögdinnye", "🐎", "csikó"),
    37: ("🍉", "nagy görögdinnye", "🦬", "bölénybocs"),
    38: ("🥬", "nagy fejes káposzta", "🐫", "tevecsikó"),
    39: ("🎃", "nagy tök", "🦒", "zsiráfbébi"),
    40: ("🍉", "érett görögdinnye", "🐘", "kiselefánt"),
    41: ("🍉", "extra nagy görögdinnye", "🦣", "mamutbébi"),
    42: ("🎃", "óriás sütőtök", "🐳", "bálnabébi"),
}


def fmt_date(d: date) -> str:
    return f"{d.year}. {HU_MONTHS[d.month - 1]}. {d.day}."


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


# ----------------------------------------------------------------------------
# Számítás
# ----------------------------------------------------------------------------
today = datetime.now(ZoneInfo("Europe/Budapest")).date()
days_along = (today - START_DATE).days
current_week = max(1, days_along // 7 + 1)
display_week = min(max(current_week, 4), 42)
days_to_due = (DUE_DATE - today).days
progress = min(max(current_week / 40, 0), 1)
trimester = trimester_of(min(current_week, 40))

# ----------------------------------------------------------------------------
# Beállítások / stílus
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Hányadik héten?", page_icon="🌱", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

    #MainMenu, header, footer {visibility: hidden;}

    .stApp {
        background-color: #FBF7F0;
        font-family: 'Inter', sans-serif;
        color: #2E2A26;
    }
    .block-container { padding-top: 2.4rem; max-width: 560px; }

    .eyebrow {
        font-size: 0.78rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #5B7A63;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .page-title {
        font-family: 'Fraunces', serif;
        font-size: 1.7rem;
        font-weight: 600;
        text-align: center;
        margin: 0 0 1.1rem 0;
        color: #2E2A26;
    }
    .ring-wrap { display: flex; justify-content: center; margin: 0.2rem 0 0.6rem; }
    .ring-caption {
        text-align: center; font-size: 0.95rem; color: #6b6660; margin-bottom: 1.4rem;
    }
    .ring-caption b { color: #2E2A26; }

    .trimester-wrap { margin: 0 0 1.6rem 0; }
    .trimester-bar { display: flex; gap: 6px; }
    .trimester-seg { flex: 1; height: 8px; border-radius: 4px; background: #E3DDD2; }
    .trimester-seg.active { background: #5B7A63; }
    .trimester-labels {
        display: flex; justify-content: space-between; font-size: 0.72rem;
        color: #8a8479; margin-top: 0.35rem;
    }

    .card {
        background: #EDF1EA;
        border-radius: 18px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-family: 'Fraunces', serif;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.7rem;
        color: #2E2A26;
    }
    .size-row { display: flex; gap: 1.4rem; }
    .size-item { flex: 1; text-align: center; }
    .size-emoji { font-size: 2.1rem; display: block; margin-bottom: 0.2rem; }
    .size-name { font-size: 0.92rem; color: #44403a; }
    .size-label { font-size: 0.72rem; color: #8a8479; text-transform: uppercase; letter-spacing: 0.06em; }

    .milestone-card {
        background: #F6E9EA;
        border-left: 4px solid #C97B84;
        border-radius: 14px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 1rem;
    }
    .milestone-card .card-title { color: #8a4a52; margin-bottom: 0.3rem; }

    .week-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 0.55rem 0.3rem; border-bottom: 1px solid #E9E4D9; font-size: 0.9rem;
    }
    .week-row:last-child { border-bottom: none; }
    .week-row.current { background: #F1ECDF; border-radius: 10px; font-weight: 600; }
    .week-num { color: #5B7A63; font-weight: 600; width: 2.2rem; flex-shrink: 0; }
    .week-dates { color: #8a8479; font-size: 0.78rem; flex: 1; text-align: center; }
    .week-size { text-align: right; flex-shrink: 0; }

    .footer-note {
        text-align: center; font-size: 0.76rem; color: #a39d90; margin-top: 1.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Fejléc + növedékgyűrű
# ----------------------------------------------------------------------------
st.markdown('<div class="eyebrow">babanapló</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Hányadik héten?</div>', unsafe_allow_html=True)

r = 86
circumference = 2 * math.pi * r
filled = circumference * progress
ring_svg = f"""
<div class="ring-wrap">
<svg width="220" height="220" viewBox="0 0 220 220">
  <circle cx="110" cy="110" r="{r}" fill="none" stroke="#E3DDD2" stroke-width="14" />
  <circle cx="110" cy="110" r="{r}" fill="none" stroke="#5B7A63" stroke-width="14"
    stroke-linecap="round"
    stroke-dasharray="{filled:.1f} {circumference:.1f}"
    transform="rotate(-90 110 110)" />
  <text x="110" y="102" text-anchor="middle"
        style="font-family:'Fraunces',serif; font-size:46px; font-weight:600; fill:#2E2A26;">{min(current_week, 40)}.</text>
  <text x="110" y="130" text-anchor="middle"
        style="font-family:'Inter',sans-serif; font-size:15px; fill:#6b6660;">hét</text>
</svg>
</div>
"""
st.markdown(ring_svg, unsafe_allow_html=True)

if days_to_due >= 0:
    due_caption = f"Kb. <b>{days_to_due}</b> nap múlva érkezik · várható időpont: <b>{fmt_date(DUE_DATE)}</b>"
else:
    due_caption = f"A kiírt határnap ({fmt_date(DUE_DATE)}) már elmúlt — hajrá! 🎉"
st.markdown(f'<div class="ring-caption">{due_caption}</div>', unsafe_allow_html=True)

segs = "".join(
    f'<div class="trimester-seg{" active" if i + 1 <= trimester else ""}"></div>'
    for i in range(3)
)
st.markdown(
    f"""
    <div class="trimester-wrap">
      <div class="trimester-bar">{segs}</div>
      <div class="trimester-labels"><span>I. trimeszter</span><span>II. trimeszter</span><span>III. trimeszter</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Mekkora most a baba?
# ----------------------------------------------------------------------------
if current_week < 4:
    size_card = """
    <div class="card">
      <div class="card-title">Mekkora most a baba?</div>
      <div style="text-align:center; color:#6b6660; font-size:0.92rem;">
        Még csak most kezdődött az utazás — pár hét múlva itt lesz az első hasonlat. 🌱
      </div>
    </div>
    """
elif current_week > 42:
    size_card = """
    <div class="card">
      <div class="card-title">Mekkora most a baba?</div>
      <div style="text-align:center; color:#6b6660; font-size:0.92rem;">
        Itt a vége — mostanra már valószínűleg meg is érkezett! 🎉
      </div>
    </div>
    """
else:
    f_emoji, f_name, a_emoji, a_name = SIZES[display_week]
    size_card = f"""
    <div class="card">
      <div class="card-title">Mekkora most a baba?</div>
      <div class="size-row">
        <div class="size-item">
          <span class="size-emoji">{f_emoji}</span>
          <div class="size-name">{f_name}</div>
          <div class="size-label">gyümölcsben</div>
        </div>
        <div class="size-item">
          <span class="size-emoji">{a_emoji}</span>
          <div class="size-name">{a_name}</div>
          <div class="size-label">kedves hasonlat</div>
        </div>
      </div>
    </div>
    """
st.markdown(size_card, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Mérföldkő kiemelés
# ----------------------------------------------------------------------------
if current_week in MILESTONES:
    icon, title, text = MILESTONES[current_week]
    st.markdown(
        f"""
        <div class="milestone-card">
          <div class="card-title">{icon} {title} — ezen a héten</div>
          <div style="font-size:0.9rem; color:#5c4348;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    upcoming = sorted(w for w in MILESTONES if w > current_week)
    if upcoming:
        nw = upcoming[0]
        icon, title, _ = MILESTONES[nw]
        weeks_away = nw - current_week
        st.markdown(
            f"""
            <div class="milestone-card">
              <div class="card-title">{icon} Következő mérföldkő: {title}</div>
              <div style="font-size:0.9rem; color:#5c4348;">{weeks_away} hét múlva, a {nw}. héten.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Heti napló
# ----------------------------------------------------------------------------
st.markdown('<div class="card-title">Heti napló</div>', unsafe_allow_html=True)
show_all = st.toggle("Összes hét megjelenítése (ne csak a mérföldköveket)", value=False)

rows_html = []
for w in range(1, 43):
    start, end = week_range(w)
    is_milestone = w in MILESTONES
    is_current = w == current_week
    if not show_all and not is_milestone and not is_current:
        continue
    size = SIZES.get(w)
    size_txt = f"{size[0]} {size[1]}" if size else "—"
    milestone_icon = f" {MILESTONES[w][0]}" if is_milestone else ""
    current_cls = " current" if is_current else ""
    rows_html.append(
        f"""
        <div class="week-row{current_cls}">
          <span class="week-num">{w}.</span>
          <span class="week-dates">{fmt_date(start)} – {fmt_date(end)}</span>
          <span class="week-size">{size_txt}{milestone_icon}</span>
        </div>
        """
    )
st.markdown(f'<div class="card">{"".join(rows_html)}</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Játékos kísérő, nem orvosi forrás — a hiteles adatokért mindig a kezelőorvos/szülész irányadó. 💛</div>',
    unsafe_allow_html=True,
)
