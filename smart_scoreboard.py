import streamlit as st
import time

st.set_page_config(page_title="스마트 점수판", layout="wide", page_icon="🏆")

# ── session state 초기화 ──────────────────────────────────────────
def init():
    defaults = {
        "a_name": "A팀", "b_name": "B팀",
        "a_score": 0, "b_score": 0,
        "a_set": 0, "b_set": 0,
        "timer_total": 600, "timer_left": 600,
        "running": False, "last_tick": None,
        "a_history": [], "b_history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ── 타이머 tick ───────────────────────────────────────────────────
if st.session_state.running:
    now = time.time()
    if st.session_state.last_tick is None:
        st.session_state.last_tick = now
    elapsed = now - st.session_state.last_tick
    if elapsed >= 1.0:
        ticks = int(elapsed)
        st.session_state.timer_left = max(0, st.session_state.timer_left - ticks)
        st.session_state.last_tick = now
        if st.session_state.timer_left == 0:
            st.session_state.running = False

# ── CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
/* 전체 배경 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #111 !important;
    color: #fff !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { background: #111 !important; }
[data-testid="stSidebar"] { display: none; }

/* 폰트 */
* { font-family: 'Segoe UI', sans-serif; box-sizing: border-box; }

/* 모든 버튼 기본 리셋 */
button[kind="secondary"], button[kind="primary"] { border: none !important; }

/* 상단 설정 바 정렬 */
div[data-testid="column"] { vertical-align: middle; }

/* 입력창 */
input[type="number"], input[type="text"] {
    background: #222 !important; color: #fff !important;
    border: 2px solid #444 !important; border-radius: 10px !important;
    font-size: 1.1rem !important; text-align: center !important;
}

/* ── A팀 점수 버튼 (1번째 컬럼 1번째 버튼) ── */
div[data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlock"] > div:nth-of-type(3) button {
    background: #FF0000 !important; color: #fff !important;
    font-size: 6rem !important; font-weight: 900 !important;
    height: 220px !important; width: 100% !important;
    border-radius: 20px !important; border: none !important;
    text-shadow: 2px 2px 8px #000;
    box-shadow: 0 6px 24px #ff000066;
}
/* ── B팀 점수 버튼 (3번째 컬럼 1번째 버튼) ── */
div[data-testid="column"]:nth-of-type(3) div[data-testid="stVerticalBlock"] > div:nth-of-type(3) button {
    background: #0055FF !important; color: #fff !important;
    font-size: 6rem !important; font-weight: 900 !important;
    height: 220px !important; width: 100% !important;
    border-radius: 20px !important; border: none !important;
    text-shadow: 2px 2px 8px #000;
    box-shadow: 0 6px 24px #0055ff66;
}

/* 취소 버튼 */
.cancel-btn button {
    background: #333 !important; color: #aaa !important;
    font-size: 1.2rem !important; height: 55px !important;
    width: 100% !important; border-radius: 12px !important;
    border: 2px solid #555 !important;
}
.cancel-btn button:hover { background: #444 !important; color: #fff !important; }

/* 교체 버튼 */
.swap-btn button {
    background: #ffaa00 !important; color: #111 !important;
    font-size: 1.4rem !important; font-weight: 800 !important;
    height: 60px !important; width: 100% !important;
    border-radius: 14px !important; border: none !important;
    box-shadow: 0 4px 16px #ffaa0066;
}

/* 세트 버튼 */
.set-btn button {
    background: #222 !important; color: #fff !important;
    font-size: 2.2rem !important; font-weight: 800 !important;
    height: 90px !important; width: 100% !important;
    border-radius: 14px !important;
    border: 2px solid #555 !important;
}

/* START 버튼 */
.start-btn button {
    background: #00cc44 !important; color: #fff !important;
    font-size: 1.2rem !important; font-weight: 700 !important;
    height: 54px !important; border-radius: 12px !important;
    border: none !important; width: 100% !important;
}
/* PAUSE 버튼 */
.pause-btn button {
    background: #ff8800 !important; color: #fff !important;
    font-size: 1.2rem !important; font-weight: 700 !important;
    height: 54px !important; border-radius: 12px !important;
    border: none !important; width: 100% !important;
}
/* 적용 버튼 */
.apply-btn button {
    background: #555 !important; color: #fff !important;
    font-size: 1.1rem !important; font-weight: 600 !important;
    height: 54px !important; border-radius: 12px !important;
    border: none !important; width: 100% !important;
}

/* 팀명 입력 */
.team-input input {
    font-size: 1.5rem !important; font-weight: 700 !important;
    text-align: center !important; height: 54px !important;
    background: #1a1a1a !important; border: 2px solid #444 !important;
    border-radius: 12px !important; color: #fff !important;
}

/* 타이머 박스 */
.timer-box {
    background: #1a1a1a;
    border-radius: 20px;
    border: 2px solid #333;
    text-align: center;
    padding: 10px 0 6px 0;
    margin: 10px 0 16px 0;
}
.timer-box .timer-time {
    font-family: 'Courier New', monospace !important;
    font-size: clamp(4rem, 12vw, 9rem);
    font-weight: 900;
    letter-spacing: 0.12em;
    line-height: 1.1;
}
.timer-box .timer-label {
    font-size: 0.95rem; color: #666; margin-top: 2px;
}

/* SET 섹션 제목 */
.set-title {
    text-align: center; font-size: 1.4rem; font-weight: 900;
    color: #888; letter-spacing: 0.2em; margin-bottom: 6px;
}

/* 점수판 이름 표시 */
.score-name {
    text-align: center; font-size: 1.8rem; font-weight: 800;
    margin-bottom: 4px; padding: 8px;
    border-radius: 12px;
}
.score-name-a { color: #FF4444; }
.score-name-b { color: #4488FF; }

/* 구분선 */
hr { border-color: #333 !important; margin: 8px 0 !important; }

/* 버튼 전체 width 100% 강제 */
.stButton { width: 100% !important; }
.stButton > button { width: 100% !important; }

/* number input 화살표 숨기기 */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

/* 스크롤바 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* padding 줄이기 */
[data-testid="stMainBlockContainer"] { padding-top: 1rem !important; padding-bottom: 0.5rem !important; }
div[data-testid="column"] > div { gap: 0.4rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 상단 설정 바 ──────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([2, 1.2, 1.2, 1], gap="small")
with c1:
    mins = st.number_input("⏱ 시간 설정 (분)", min_value=1, max_value=99,
                           value=st.session_state.timer_total // 60,
                           step=1, label_visibility="collapsed",
                           key="mins_input")
with c2:
    st.markdown('<div class="apply-btn">', unsafe_allow_html=True)
    if st.button("⚙️ 시간 적용", key="apply_time"):
        st.session_state.timer_total = int(mins) * 60
        st.session_state.timer_left = int(mins) * 60
        st.session_state.running = False
        st.session_state.last_tick = None
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    if st.session_state.running:
        st.markdown('<div class="pause-btn">', unsafe_allow_html=True)
        if st.button("⏸ PAUSE", key="pause_btn"):
            st.session_state.running = False
            st.session_state.last_tick = None
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("▶ START", key="start_btn"):
            if st.session_state.timer_left > 0:
                st.session_state.running = True
                st.session_state.last_tick = time.time()
        st.markdown('</div>', unsafe_allow_html=True)
with c4:
    if st.button("🔁 리셋", key="reset_timer"):
        st.session_state.timer_left = st.session_state.timer_total
        st.session_state.running = False
        st.session_state.last_tick = None

# ── 타이머 표시 ───────────────────────────────────────────────────
tl = st.session_state.timer_left
mm, ss = divmod(tl, 60)
timer_color = "#ff4444" if tl <= 30 else ("#ffaa00" if tl <= 60 else "#ffffff")
status_text = "⏸ 일시정지" if not st.session_state.running and tl < st.session_state.timer_total and tl > 0 else (
              "✅ 종료!" if tl == 0 else ("⏱ 진행 중" if st.session_state.running else "대기 중"))

st.markdown(f"""
<div class="timer-box">
  <div class="timer-time" style="color:{timer_color};">{mm:02d}:{ss:02d}</div>
  <div class="timer-label">{status_text}</div>
</div>
""", unsafe_allow_html=True)

# ── 메인 점수판 ───────────────────────────────────────────────────
col_a, col_mid, col_b = st.columns([4, 2, 4], gap="medium")

with col_a:
    st.markdown('<div class="team-input">', unsafe_allow_html=True)
    a_name = st.text_input("A팀 이름", value=st.session_state.a_name,
                           key="a_name_input", label_visibility="collapsed")
    st.session_state.a_name = a_name
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="score-name score-name-a">{st.session_state.a_name}</div>', unsafe_allow_html=True)
    if st.button(str(st.session_state.a_score), key="a_score_btn", use_container_width=True):
        st.session_state.a_score += 1
        st.session_state.a_history.append(st.session_state.a_score)
    st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
    if st.button("↩ 점수 취소", key="a_cancel", use_container_width=True):
        if st.session_state.a_score > 0:
            st.session_state.a_score -= 1
    st.markdown('</div>', unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="set-title">SET</div>', unsafe_allow_html=True)
    st.markdown('<div class="set-btn">', unsafe_allow_html=True)
    if st.button(f"🔴 {st.session_state.a_set}", key="a_set_btn", use_container_width=True):
        st.session_state.a_set += 1
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="set-btn">', unsafe_allow_html=True)
    if st.button(f"🔵 {st.session_state.b_set}", key="b_set_btn", use_container_width=True):
        st.session_state.b_set += 1
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="swap-btn">', unsafe_allow_html=True)
    if st.button("🔄 교체", key="swap_btn", use_container_width=True):
        (st.session_state.a_name, st.session_state.b_name) = (st.session_state.b_name, st.session_state.a_name)
        (st.session_state.a_score, st.session_state.b_score) = (st.session_state.b_score, st.session_state.a_score)
        (st.session_state.a_set, st.session_state.b_set) = (st.session_state.b_set, st.session_state.a_set)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    # 전체 초기화 버튼 (보너스)
    if st.button("🗑 전체 초기화", key="full_reset", use_container_width=True):
        for k in ["a_score","b_score","a_set","b_set","a_history","b_history"]:
            st.session_state[k] = 0 if k not in ["a_history","b_history"] else []
        st.rerun()

with col_b:
    st.markdown('<div class="team-input">', unsafe_allow_html=True)
    b_name = st.text_input("B팀 이름", value=st.session_state.b_name,
                           key="b_name_input", label_visibility="collapsed")
    st.session_state.b_name = b_name
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="score-name score-name-b">{st.session_state.b_name}</div>', unsafe_allow_html=True)
    if st.button(str(st.session_state.b_score), key="b_score_btn", use_container_width=True):
        st.session_state.b_score += 1
        st.session_state.b_history.append(st.session_state.b_score)
    st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
    if st.button("↩ 점수 취소", key="b_cancel", use_container_width=True):
        if st.session_state.b_score > 0:
            st.session_state.b_score -= 1
    st.markdown('</div>', unsafe_allow_html=True)

# ── 자동 rerun (타이머 작동 중) ───────────────────────────────────
if st.session_state.running:
    time.sleep(0.5)
    st.rerun()
