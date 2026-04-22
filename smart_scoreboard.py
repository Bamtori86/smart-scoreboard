import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스마트 점수판", layout="wide", page_icon="🏆")

st.markdown("""
<style>
#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stAppViewContainer"] { background: #111 !important; padding: 0 !important; }
[data-testid="stMainBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
[data-testid="stMain"] { padding: 0 !important; }
.block-container { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
  body {
    background:#111; color:#fff;
    font-family:'Segoe UI','Malgun Gothic',sans-serif;
    height:700px; overflow:hidden; user-select:none;
  }
  .board {
    display:flex; gap:6px; height:700px; padding:6px;
  }

  /* ── 팀 패널 ── */
  .team-panel {
    flex:4; border-radius:16px;
    display:flex; align-items:center; justify-content:center;
    font-size:clamp(6rem,18vw,14rem); font-weight:900; color:#fff;
    cursor:pointer; transition:filter .15s;
    position:relative; overflow:hidden;
  }
  .team-panel:active { filter:brightness(1.3); }
  #teamA { background:#EE0000; }
  #teamB { background:#0033EE; }

  /* 롱프레스 오버레이 */
  .press-ring {
    position:absolute; border-radius:50%;
    border:6px solid rgba(255,255,255,0.6);
    width:120px; height:120px;
    transform:scale(0); opacity:0;
    transition:transform .6s ease, opacity .6s ease;
    pointer-events:none;
  }
  .press-ring.active { transform:scale(2.5); opacity:1; }

  /* ── 중앙 패널 ── */
  .center {
    flex:2.2; display:flex; flex-direction:column; gap:6px;
  }

  /* 세트 스코어 행 */
  .set-row {
    display:flex; gap:6px; height:130px; flex-shrink:0;
  }
  .set-box {
    flex:1; border-radius:12px;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    font-size:3rem; font-weight:900; color:#fff;
    cursor:pointer; gap:2px; transition:filter .15s;
  }
  .set-box:active { filter:brightness(1.4); }
  .set-box small { font-size:0.7rem; font-weight:400; opacity:.7; letter-spacing:.05em; }
  #setA { background:#BB0000; }
  #setB { background:#0022CC; }

  /* 타이머 박스 */
  .timer-box {
    flex:1;
    background:#1c1c1c; border:2px solid #2a2a2a; border-radius:14px;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:8px;
    padding:10px 8px;
  }
  .timer-label { font-size:.75rem; color:#555; letter-spacing:.12em; text-transform:uppercase; }
  .timer-time {
    font-family:'Courier New',monospace;
    font-size:clamp(2.4rem,5vw,3.4rem);
    font-weight:900; letter-spacing:.1em;
    transition:color .4s;
  }
  .timer-status { font-size:.72rem; color:#555; }
  .t-controls { display:flex; gap:6px; align-items:center; }
  .t-input {
    width:60px; padding:5px; border-radius:8px;
    background:#2a2a2a; border:1px solid #444; color:#fff;
    text-align:center; font-size:.9rem;
  }
  .t-input::-webkit-outer-spin-button,
  .t-input::-webkit-inner-spin-button { -webkit-appearance:none; }
  .tbtn {
    padding:6px 13px; border:none; border-radius:8px;
    font-size:.9rem; font-weight:700; cursor:pointer; transition:.15s;
  }
  .tbtn:active { transform:scale(.94); }
  #btnStart { background:#00cc55; color:#fff; }
  #btnPause { background:#ff8800; color:#fff; display:none; }
  #btnReset { background:#444; color:#ddd; }

  /* 액션 버튼 */
  .action-row { display:flex; flex-direction:column; gap:5px; flex-shrink:0; }
  .abtn {
    background:#2a2a2a; color:#ccc;
    border:1px solid #3a3a3a; border-radius:10px;
    padding:11px; font-size:.95rem; cursor:pointer;
    transition:.15s; text-align:center; font-weight:600;
  }
  .abtn:active { background:#3a3a3a; color:#fff; }

  /* 팀명 */
  .team-name-row {
    display:flex; gap:6px; flex-shrink:0; height:42px;
  }
  .tname {
    flex:1; background:transparent; border:none;
    border-bottom:2px solid #333; color:#fff;
    font-size:1.1rem; font-weight:700;
    text-align:center; outline:none; border-radius:0;
    padding:4px;
  }
  .tname:focus { border-bottom-color:#666; }
  .tname-a { color:#ff6666; }
  .tname-b { color:#6699ff; }
</style>
</head>
<body>
<div class="board">

  <!-- A팀 -->
  <div class="team-panel" id="teamA">
    <div class="press-ring" id="ringA"></div>
    <span id="scoreA">0</span>
  </div>

  <!-- 중앙 -->
  <div class="center">

    <!-- 팀명 입력 -->
    <div class="team-name-row">
      <input class="tname tname-a" id="nameA" value="A 팀" maxlength="8">
      <input class="tname tname-b" id="nameB" value="B 팀" maxlength="8">
    </div>

    <!-- 세트 스코어 -->
    <div class="set-row">
      <div class="set-box" id="setA" onclick="addSet('a')">
        <small>A 세트</small>
        <span id="setScoreA">0</span>
      </div>
      <div class="set-box" id="setB" onclick="addSet('b')">
        <small>B 세트</small>
        <span id="setScoreB">0</span>
      </div>
    </div>

    <!-- 타이머 -->
    <div class="timer-box">
      <div class="timer-label">⏱ 타이머</div>
      <div class="timer-time" id="timerDisp">10:00</div>
      <div class="t-controls">
        <input type="number" class="t-input" id="tInput" value="10" min="1" max="99">
        <button class="tbtn" id="btnStart" onclick="startTimer()">▶ START</button>
        <button class="tbtn" id="btnPause" onclick="pauseTimer()">⏸ PAUSE</button>
        <button class="tbtn" id="btnReset" onclick="resetTimer()">↺</button>
      </div>
      <div class="timer-status" id="tStatus">대기 중</div>
    </div>

    <!-- 액션 버튼 -->
    <div class="action-row">
      <div class="abtn" onclick="swapTeams()">🔄 팀 교체</div>
      <div class="abtn" onclick="resetScores()">🗑 점수 초기화</div>
      <div class="abtn" onclick="resetSets()">📋 세트 초기화</div>
    </div>
  </div>

  <!-- B팀 -->
  <div class="team-panel" id="teamB">
    <div class="press-ring" id="ringB"></div>
    <span id="scoreB">0</span>
  </div>
</div>

<script>
// ── 상태 ──────────────────────────────────────
let sA=0, sB=0, setA=0, setB=0;
let tLeft=600, tTotal=600, tRunning=false, tInterval=null;

// ── 점수 업데이트 ──────────────────────────────
function render(){
  document.getElementById('scoreA').textContent = sA;
  document.getElementById('scoreB').textContent = sB;
  document.getElementById('setScoreA').textContent = setA;
  document.getElementById('setScoreB').textContent = setB;
}

// ── 세트 ──────────────────────────────────────
function addSet(t){ if(t==='a') setA++; else setB++; render(); }

// ── 초기화 ────────────────────────────────────
function resetScores(){ sA=0; sB=0; render(); }
function resetSets(){ setA=0; setB=0; render(); }
function swapTeams(){
  [sA,sB]=[sB,sA]; [setA,setB]=[setB,setA];
  let na=document.getElementById('nameA').value;
  let nb=document.getElementById('nameB').value;
  document.getElementById('nameA').value=nb;
  document.getElementById('nameB').value=na;
  render();
  // flash
  ['teamA','teamB'].forEach(id=>{
    let el=document.getElementById(id);
    el.style.filter='brightness(1.5)';
    setTimeout(()=>el.style.filter='',300);
  });
}

// ── 롱프레스 ──────────────────────────────────
function setupPress(panelId, ringId, team){
  const panel = document.getElementById(panelId);
  const ring  = document.getElementById(ringId);
  let timer=null, fired=false;

  function onStart(e){
    fired=false;
    ring.style.left = ((e.touches?e.touches[0].clientX:e.clientX) - panel.getBoundingClientRect().left - 60)+'px';
    ring.style.top  = ((e.touches?e.touches[0].clientY:e.clientY) - panel.getBoundingClientRect().top  - 60)+'px';
    ring.classList.add('active');
    timer = setTimeout(()=>{
      fired=true;
      if(team==='a'&&sA>0) sA--;
      else if(team==='b'&&sB>0) sB--;
      render();
      ring.classList.remove('active');
    },600);
  }
  function onEnd(e){
    clearTimeout(timer);
    ring.classList.remove('active');
    if(!fired){
      if(team==='a') sA++;
      else sB++;
      render();
    }
    fired=false;
  }
  function onLeave(){ clearTimeout(timer); ring.classList.remove('active'); fired=true; }

  panel.addEventListener('mousedown', onStart);
  panel.addEventListener('mouseup', onEnd);
  panel.addEventListener('mouseleave', onLeave);
  panel.addEventListener('touchstart', onStart, {passive:true});
  panel.addEventListener('touchend', onEnd);
}
setupPress('teamA','ringA','a');
setupPress('teamB','ringB','b');

// ── 타이머 ────────────────────────────────────
function fmtTime(s){ return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }

function updateTimerUI(){
  let el=document.getElementById('timerDisp');
  el.textContent=fmtTime(tLeft);
  el.style.color = tLeft<=30?'#ff3333': tLeft<=60?'#ffaa00':'#ffffff';
}

function startTimer(){
  if(tRunning) return;
  let mins=parseInt(document.getElementById('tInput').value)||10;
  if(tLeft===0){ tLeft=mins*60; tTotal=tLeft; }
  tRunning=true;
  document.getElementById('btnStart').style.display='none';
  document.getElementById('btnPause').style.display='inline-block';
  document.getElementById('tStatus').textContent='⏱ 진행 중';
  tInterval=setInterval(()=>{
    if(tLeft>0){ tLeft--; updateTimerUI(); }
    else{
      clearInterval(tInterval); tRunning=false;
      document.getElementById('tStatus').textContent='✅ 종료!';
      document.getElementById('btnPause').style.display='none';
      document.getElementById('btnStart').style.display='inline-block';
    }
  },1000);
}
function pauseTimer(){
  clearInterval(tInterval); tRunning=false;
  document.getElementById('btnPause').style.display='none';
  document.getElementById('btnStart').style.display='inline-block';
  document.getElementById('tStatus').textContent='⏸ 일시정지';
}
function resetTimer(){
  clearInterval(tInterval); tRunning=false;
  let mins=parseInt(document.getElementById('tInput').value)||10;
  tLeft=mins*60; tTotal=tLeft;
  updateTimerUI();
  document.getElementById('btnPause').style.display='none';
  document.getElementById('btnStart').style.display='inline-block';
  document.getElementById('tStatus').textContent='대기 중';
}

updateTimerUI();
</script>
</body>
</html>
"""

components.html(HTML, height=712, scrolling=False)
