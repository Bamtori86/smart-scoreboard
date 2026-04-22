import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스마트 점수판", layout="wide", page_icon="🏆")

st.markdown("""
<style>
#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stAppViewContainer"] { background:#111 !important; padding:0 !important; }
[data-testid="stMainBlockContainer"] { padding:0 !important; max-width:100% !important; }
[data-testid="stMain"] { padding:0 !important; }
.block-container { padding:0 !important; }
</style>
""", unsafe_allow_html=True)

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html, body { width:100%; height:100%; overflow:hidden; }
body {
  background:#111; color:#fff;
  font-family:'Segoe UI','Malgun Gothic',sans-serif;
  user-select:none; -webkit-user-select:none;
}

/* ── 가로 전환 유도 오버레이 ── */
#rotate-overlay {
  display:none;
  position:fixed; inset:0; z-index:9999;
  background:#111;
  flex-direction:column;
  align-items:center; justify-content:center;
  gap:20px; text-align:center; padding:30px;
}
#rotate-overlay .icon { font-size:4rem; animation:spin 1.6s ease-in-out infinite; }
@keyframes spin {
  0%   { transform:rotate(0deg); }
  40%  { transform:rotate(90deg); }
  100% { transform:rotate(90deg); }
}
#rotate-overlay .msg { font-size:1.2rem; font-weight:700; color:#fff; line-height:1.6; }
#rotate-overlay .sub { font-size:.85rem; color:#666; }
@media (orientation:portrait) {
  #rotate-overlay { display:flex; }
}

/* ── 공통 컴포넌트 ── */
.press-ring {
  position:absolute; border-radius:50%;
  border:6px solid rgba(255,255,255,0.6);
  width:100px; height:100px;
  transform:scale(0); opacity:0;
  transition:transform .6s ease, opacity .6s ease;
  pointer-events:none;
}
.press-ring.active { transform:scale(3); opacity:1; }

.set-box {
  flex:1; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:clamp(2rem,5vw,3.8rem); font-weight:900; color:#fff;
  cursor:pointer; position:relative; overflow:hidden;
  touch-action:none; -webkit-touch-callout:none;
}
.set-box:active { filter:brightness(1.4); }

.timer-box {
  background:#1c1c1c; border:2px solid #2a2a2a; border-radius:14px;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:8px;
  padding:10px 8px; flex:1;
}
.timer-label { font-size:1rem; color:#666; letter-spacing:.15em; font-weight:700; }
.timer-time {
  font-family:'Orbitron','Courier New',monospace;
  font-weight:900; letter-spacing:.08em; transition:color .4s;
  font-size:clamp(2.4rem,6vw,4.2rem);
}
.timer-status { font-size:.85rem; color:#555; font-weight:600; }
.t-controls { display:flex; gap:5px; align-items:center; flex-wrap:wrap; justify-content:center; }
.t-input {
  width:56px; padding:5px; border-radius:8px;
  background:#2a2a2a; border:1px solid #444; color:#fff;
  text-align:center; font-size:.95rem; font-weight:700;
}
.t-input::-webkit-outer-spin-button,
.t-input::-webkit-inner-spin-button { -webkit-appearance:none; }
.tbtn {
  padding:7px 13px; border:none; border-radius:8px;
  font-size:.9rem; font-weight:700; cursor:pointer; transition:.15s;
  touch-action:manipulation;
}
.tbtn:active { transform:scale(.94); }
#btnStart { background:#00cc55; color:#fff; }
#btnPause { background:#ff8800; color:#fff; display:none; }
#btnReset { background:#444; color:#ddd; }

.abtn {
  background:#2a2a2a; color:#ccc;
  border:1px solid #3a3a3a; border-radius:10px;
  padding:10px 6px; font-size:.88rem; cursor:pointer;
  transition:.15s; text-align:center; font-weight:600;
  touch-action:manipulation; flex:1;
}
.abtn:active { background:#3a3a3a; color:#fff; }

.tname {
  flex:1; background:transparent; border:none;
  border-bottom:2px solid #333; color:#fff;
  font-size:1rem; font-weight:700;
  text-align:center; outline:none; padding:4px;
  transition:color .3s, border-bottom-color .3s; min-width:0;
}
.tname-red  { color:#ff6666; border-bottom-color:#ff6666; }
.tname-blue { color:#6699ff; border-bottom-color:#6699ff; }

.copyright { text-align:center; font-size:.58rem; color:#2a2a2a; padding:2px 0; }

/* ── 가로 레이아웃 ── */
.board {
  display:flex; flex-direction:row;
  gap:6px; width:100%; height:100%; padding:6px;
}
.team-panel {
  flex:4; border-radius:16px;
  display:flex; align-items:center; justify-content:center;
  font-size:clamp(4rem,12vw,13rem); font-weight:900; color:#fff;
  cursor:pointer; position:relative; overflow:hidden;
  touch-action:none; -webkit-touch-callout:none;
}
.team-panel:active { filter:brightness(1.3); }
.center {
  flex:2.2; display:flex; flex-direction:column; gap:6px; min-width:0;
}
.name-row { display:flex; gap:6px; flex-shrink:0; height:40px; }
.set-row  { display:flex; gap:6px; flex-shrink:0; height:clamp(90px,14vh,130px); }
.action-btns { display:flex; gap:5px; }
</style>
</head>
<body>

<!-- 세로 모드 오버레이 -->
<div id="rotate-overlay">
  <div class="icon">📱</div>
  <div class="msg">화면을 가로로 돌려주세요</div>
  <div class="sub">스마트 점수판은 가로 모드에서<br>최적으로 표시됩니다.</div>
</div>

<div class="board">
  <div class="team-panel" id="teamA">
    <div class="press-ring" id="ringA"></div>
    <span id="scoreA">0</span>
  </div>

  <div class="center">
    <div class="name-row">
      <input class="tname tname-red"  id="nameA" value="A 팀" maxlength="8">
      <input class="tname tname-blue" id="nameB" value="B 팀" maxlength="8">
    </div>
    <div class="set-row">
      <div class="set-box" id="setA">
        <div class="press-ring" id="ringSetA"></div>
        <span id="setScoreA">0</span>
      </div>
      <div class="set-box" id="setB">
        <div class="press-ring" id="ringSetB"></div>
        <span id="setScoreB">0</span>
      </div>
    </div>
    <div class="timer-box">
      <div class="timer-label">타이머</div>
      <div class="timer-time" id="timerDisp">10:00</div>
      <div class="t-controls">
        <input type="number" class="t-input" id="tInput" value="10" min="1" max="99">
        <button class="tbtn" id="btnStart" onclick="startTimer()">▶ START</button>
        <button class="tbtn" id="btnPause" onclick="pauseTimer()">⏸ PAUSE</button>
        <button class="tbtn" id="btnReset" onclick="resetTimer()">↺ 리셋</button>
      </div>
      <div class="timer-status" id="tStatus">대기 중</div>
    </div>
    <div class="action-btns">
      <div class="abtn" onclick="swapTeams()">팀 교체</div>
      <div class="abtn" onclick="resetScores()">점수 초기화</div>
      <div class="abtn" onclick="resetSets()">세트 초기화</div>
    </div>
    <div class="copyright">ⓒ AI-ON 교과연구회 All rights reserved.</div>
  </div>

  <div class="team-panel" id="teamB">
    <div class="press-ring" id="ringB"></div>
    <span id="scoreB">0</span>
  </div>
</div>

<script>
// ── 상태 ─────────────────────────────────────────────
let sA=0, sB=0, setA=0, setB=0;
let tLeft=600, tTotal=600, tRunning=false, tInterval=null;
let colorsNormal=true;
const COLOR_RED='#EE0000', COLOR_BLUE='#0033EE';
const SET_RED='#BB0000',   SET_BLUE='#0022CC';

function applyColors(){
  document.getElementById('teamA').style.background = colorsNormal?COLOR_RED:COLOR_BLUE;
  document.getElementById('teamB').style.background = colorsNormal?COLOR_BLUE:COLOR_RED;
  document.getElementById('setA').style.background  = colorsNormal?SET_RED:SET_BLUE;
  document.getElementById('setB').style.background  = colorsNormal?SET_BLUE:SET_RED;
  document.getElementById('nameA').className='tname '+(colorsNormal?'tname-red':'tname-blue');
  document.getElementById('nameB').className='tname '+(colorsNormal?'tname-blue':'tname-red');
}
applyColors();

function render(){
  document.getElementById('scoreA').textContent   = sA;
  document.getElementById('scoreB').textContent   = sB;
  document.getElementById('setScoreA').textContent = setA;
  document.getElementById('setScoreB').textContent = setB;
}

function resetScores(){ sA=0; sB=0; render(); }
function resetSets(){   setA=0; setB=0; render(); }

function swapTeams(){
  [sA,sB]=[sB,sA]; [setA,setB]=[setB,setA];
  let na=document.getElementById('nameA').value;
  let nb=document.getElementById('nameB').value;
  document.getElementById('nameA').value=nb;
  document.getElementById('nameB').value=na;
  colorsNormal=!colorsNormal;
  applyColors(); render();
  ['teamA','teamB'].forEach(id=>{
    let el=document.getElementById(id);
    el.style.filter='brightness(1.6)';
    setTimeout(()=>el.style.filter='',280);
  });
}

// ── 롱프레스 핵심: touchstart에서 preventDefault() 호출
//    → 브라우저가 mouse 이벤트를 추가로 발생시키지 않음 (2점 버그 완전 차단)
function setupPress(el, ringEl, onShort, onLong){
  let timer=null, fired=false;

  function startPress(x, y){
    fired=false;
    let rect=el.getBoundingClientRect();
    ringEl.style.left=(x-rect.left-50)+'px';
    ringEl.style.top =(y-rect.top -50)+'px';
    ringEl.classList.add('active');
    timer=setTimeout(()=>{
      fired=true; onLong();
      ringEl.classList.remove('active');
    },600);
  }
  function endPress(){
    clearTimeout(timer);
    ringEl.classList.remove('active');
    if(!fired) onShort();
    fired=false;
  }
  function cancelPress(){
    clearTimeout(timer);
    ringEl.classList.remove('active');
    fired=true;
  }

  // 터치 이벤트 (모바일) — passive:false + preventDefault 로 마우스 이벤트 차단
  el.addEventListener('touchstart', e=>{
    e.preventDefault();
    startPress(e.touches[0].clientX, e.touches[0].clientY);
  }, {passive:false});

  el.addEventListener('touchend', e=>{
    e.preventDefault();
    endPress();
  }, {passive:false});

  el.addEventListener('touchcancel', e=>{
    e.preventDefault();
    cancelPress();
  }, {passive:false});

  // 마우스 이벤트 (데스크탑) — 터치 기기에서는 위 preventDefault 덕분에 발동 안 됨
  el.addEventListener('mousedown', e=>{ startPress(e.clientX, e.clientY); });
  el.addEventListener('mouseup',   ()=>{ endPress(); });
  el.addEventListener('mouseleave',()=>{ cancelPress(); });
  el.addEventListener('contextmenu', e=>e.preventDefault());
}

setupPress(document.getElementById('teamA'), document.getElementById('ringA'),
  ()=>{ sA++; render(); }, ()=>{ if(sA>0) sA--; render(); });
setupPress(document.getElementById('teamB'), document.getElementById('ringB'),
  ()=>{ sB++; render(); }, ()=>{ if(sB>0) sB--; render(); });
setupPress(document.getElementById('setA'), document.getElementById('ringSetA'),
  ()=>{ setA++; render(); }, ()=>{ if(setA>0) setA--; render(); });
setupPress(document.getElementById('setB'), document.getElementById('ringSetB'),
  ()=>{ setB++; render(); }, ()=>{ if(setB>0) setB--; render(); });

// ── 알람 ─────────────────────────────────────────────
function playAlarm(){
  try{
    const ctx=new(window.AudioContext||window.webkitAudioContext)();
    [{f:880,s:0,d:.18},{f:880,s:.22,d:.18},{f:880,s:.44,d:.18},
     {f:1046,s:.7,d:.35},{f:880,s:1.1,d:.18},{f:1046,s:1.35,d:.55}]
    .forEach(({f,s,d})=>{
      const o=ctx.createOscillator(),g=ctx.createGain();
      o.connect(g);g.connect(ctx.destination);
      o.type='square';o.frequency.value=f;
      g.gain.setValueAtTime(.35,ctx.currentTime+s);
      g.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+s+d);
      o.start(ctx.currentTime+s);o.stop(ctx.currentTime+s+d+.05);
    });
  }catch(e){}
}

// ── 타이머 ───────────────────────────────────────────
function fmt(s){ return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }
function updateTimerUI(){
  let el=document.getElementById('timerDisp');
  el.textContent=fmt(tLeft);
  el.style.color=tLeft<=30?'#ff3333':tLeft<=60?'#ffaa00':'#ffffff';
}
function startTimer(){
  if(tRunning)return;
  let m=parseInt(document.getElementById('tInput').value)||10;
  if(tLeft===0){tLeft=m*60;tTotal=tLeft;}
  tRunning=true;
  document.getElementById('btnStart').style.display='none';
  document.getElementById('btnPause').style.display='inline-block';
  document.getElementById('tStatus').textContent='진행 중';
  tInterval=setInterval(()=>{
    if(tLeft>0){tLeft--;updateTimerUI();}
    else{
      clearInterval(tInterval);tRunning=false;
      document.getElementById('tStatus').textContent='종료!';
      document.getElementById('btnPause').style.display='none';
      document.getElementById('btnStart').style.display='inline-block';
      playAlarm();
    }
  },1000);
}
function pauseTimer(){
  clearInterval(tInterval);tRunning=false;
  document.getElementById('btnPause').style.display='none';
  document.getElementById('btnStart').style.display='inline-block';
  document.getElementById('tStatus').textContent='일시정지';
}
function resetTimer(){
  clearInterval(tInterval);tRunning=false;
  let m=parseInt(document.getElementById('tInput').value)||10;
  tLeft=m*60;tTotal=tLeft;updateTimerUI();
  document.getElementById('btnPause').style.display='none';
  document.getElementById('btnStart').style.display='inline-block';
  document.getElementById('tStatus').textContent='대기 중';
}
updateTimerUI();
</script>
</body>
</html>
"""

components.html(HTML, height=820, scrolling=False)
