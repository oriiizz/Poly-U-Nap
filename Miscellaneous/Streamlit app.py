# app.py
import streamlit as st, json

st.set_page_config(page_title='Sleep Rating System (Python)', layout='centered')

# Minimal CSS to preserve look/press-start font + pixel borders from original Figma/tailwind
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
body { font-family: 'Press Start 2P', monospace; background-color:#0b1020; color:#e6eef8; }
.container { max-width:900px; margin:20px auto; padding:18px; background:linear-gradient(180deg,#0f1724,#0b1020); border:2px solid #111827; border-radius:12px; }
.pixel-border { border:2px solid #00ff41; padding:10px; border-radius:8px; display:inline-block; }
.small-muted { color:#9ca3af; font-size:12px; opacity:0.85; }
.header-accent { color:#8b5cf6; }
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# QUESTIONS (extracted from your SleepQuiz.tsx)
QUESTIONS = [
  {
    "id": "mattress",
    "question": ">> SELECT YOUR SLEEP TERRAIN <<",
    "options": [
      {"value": "hard", "label": "HARD MODE (Firm Surface)", "emoji": "🪨"},
      {"value": "medium", "label": "NORMAL MODE (Medium)", "emoji": "🛏️"},
      {"value": "soft", "label": "EASY MODE (Cloud Nine)", "emoji": "☁️"},
      {"value": "floor", "label": "CHAOS MODE (Any Surface)", "emoji": "🌍"}
    ]
  },
  {
    "id": "blankets",
    "question": ">> CHOOSE YOUR ARMOR <<",
    "options": [
      {"value": "none", "label": "NO ARMOR (Raw-dogging life)", "emoji": "🔥"},
      {"value": "light", "label": "LIGHT ARMOR (Single Layer)", "emoji": "🧵"},
      {"value": "heavy", "label": "HEAVY ARMOR (Thicc Blanket)", "emoji": "🛌"},
      {"value": "burrito", "label": "TANK MODE (Full Burrito)", "emoji": "🌯"}
    ]
  },
  {
    "id": "sleepDepth",
    "question": ">> HOW DEEP DO YOU GO? <<",
    "options": [
      {"value": "light", "label": "LIGHT SLEEP (Easily Woken)", "emoji": "🌫️"},
      {"value": "normal", "label": "NORMAL SLEEP", "emoji": "🌙"},
      {"value": "deep", "label": "DEEP SLEEP", "emoji": "🛌"},
      {"value": "dead", "label": "DEAD TO THE WORLD", "emoji": "💀"}
    ]
  },
  {
    "id": "temperature",
    "question": ">> SET TEMPERATURE CONFIG <<",
    "options": [
      {"value": "cold", "label": "FROZEN TUNDRA (-20°C)", "emoji": "❄️"},
      {"value": "cool", "label": "COOL BREEZE (15-18°C)", "emoji": "🌬️"},
      {"value": "warm", "label": "COZY WARM (21-24°C)", "emoji": "🔥"},
      {"value": "hot", "label": "SURFACE OF SUN (27°C+)", "emoji": "🌴"}
    ]
  }
]

# PERSONALITIES (recreated from your TSX - trimmed descriptions)
PERSONALITIES = {
  "cloud_drifter": {
    "type":"cloud_drifter",
    "title":"THE CLOUD DRIFTER",
    "description":"Class: COMFORT MAGE | Thrives on soft, warm setups and comfort zones anywhere. Weakness: hard surfaces.",
    "emoji":"☁️",
    "recommendedLocations":["library_beanbags", "lounge_couches", "student_center"]
  },
  "minimalist_monk": {
    "type":"minimalist_monk",
    "title":"THE ASCETIC SLEEPER",
    "description":"Class: ZEN WARRIOR | Can sleep on literal rocks; low needs, high resilience.",
    "emoji":"🧘",
    "recommendedLocations":["lecture_hall", "study_room", "quiet_corner"]
  },
  "hibernation_hero": {
    "type":"hibernation_hero",
    "title":"THE DEEP SLEEPER",
    "description":"Class: BEAR MODE | Extremely deep sleep, may sleep through disturbances (and alarms).",
    "emoji":"🛌",
    "recommendedLocations":["quiet_corner", "study_room", "lounge_couches"]
  },
  "delicate_dreamer": {
    "type":"delicate_dreamer",
    "title":"THE PERFECTIONIST",
    "description":"Class: GLASS CANNON | Needs near-perfect conditions to get legendary rest.",
    "emoji":"🦋",
    "recommendedLocations":["quiet_corner", "study_room", "library_beanbags"]
  },
  "burrito_champion": {
    "type":"burrito_champion",
    "title":"THE BURRITO LORD",
    "description":"Class: TANK | Loves to be wrapped up — very defensive and comfy.",
    "emoji":"🌯",
    "recommendedLocations":["lounge_couches", "student_center", "library_beanbags"]
  },
  "adaptable_nomad": {
    "type":"adaptable_nomad",
    "title":"THE ADAPTABLE NOMAD",
    "description":"Flexible sleeper: can adapt to many setups and conditions.",
    "emoji":"🧭",
    "recommendedLocations":["student_center", "lounge_couches", "lecture_hall"]
  }
}

# Decision logic derived from SleepQuiz.tsx
def get_personality(answers):
    mattress = answers.get('mattress','')
    blankets = answers.get('blankets','')
    sleepDepth = answers.get('sleepDepth','')
    temperature = answers.get('temperature','')
    # priority logic kept consistent with original project
    if blankets in ('burrito','heavy'):
        return PERSONALITIES['burrito_champion']
    if mattress in ('floor','hard'):
        return PERSONALITIES['minimalist_monk']
    if sleepDepth in ('deep','dead'):
        return PERSONALITIES['hibernation_hero']
    if sleepDepth == 'light':
        return PERSONALITIES['delicate_dreamer']
    if mattress == 'soft' and temperature in ('warm','hot'):
        return PERSONALITIES['cloud_drifter']
    return PERSONALITIES['adaptable_nomad']

# Simple navigation
st.sidebar.title("Navigate")
page = st.sidebar.radio("", ["Home","Take Quiz","Profile","Achievements"])

if page == "Home":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h2 class="header-accent">Sleep Rating System</h2>', unsafe_allow_html=True)
    st.markdown('<p class="small-muted">A Streamlit conversion of your TSX project with preserved layout and font.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Take Quiz":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h3>Sleep Quiz</h3>', unsafe_allow_html=True)
    # keep answers in session state
    if 'answers' not in st.session_state:
        st.session_state['answers'] = {}
    answers = st.session_state['answers']
    for q in QUESTIONS:
        qid = q['id']
        opts = [f"{o['emoji']}  {o['label']}" for o in q['options']]
        # present radio and map back to value
        sel = st.radio(q['question'], opts, index=0, key=qid)
        for o in q['options']:
            if f"{o['emoji']}  {o['label']}" == sel:
                answers[qid] = o['value']
    if st.button("Finish Quiz"):
        p = get_personality(answers)
        st.session_state['last_personality'] = p
        st.success("Quiz completed — open Profile to view your Sleep Personality.")
    st.markdown('<div class="small-muted" style="margin-top:8px">[TIP: Choose wisely — your build determines your playstyle]</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Profile":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h3>Profile</h3>', unsafe_allow_html=True)
    p = st.session_state.get('last_personality', None)
    if p:
        st.markdown(f'<div class="pixel-border"><h4>{p["emoji"]} {p["title"]}</h4><p>{p["description"]}</p></div>', unsafe_allow_html=True)
        st.markdown('**Recommended locations:** ' + ', '.join(p['recommendedLocations']))
    else:
        st.info("No personality yet. Take the quiz!")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Achievements":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h3>Achievements</h3>', unsafe_allow_html=True)
    st.markdown('<p>Achievements were part of the original project. This page preserves the placeholder area where achievements appear.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; opacity:0.6; margin-top:16px">Converted from your .tsx project. Run: <code>streamlit run app.py</code></div>', unsafe_allow_html=True)
