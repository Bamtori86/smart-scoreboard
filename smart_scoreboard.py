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
html { width:100%; height:100%; }
body {
  background:#111; color:#fff;
  font-family:'Segoe UI','Malgun Gothic',sans-serif;
  user-select:none; -webkit-user-select:none;
  width:100%; overflow:hidden;
}

/* ── 세로 모드 오버레이 ── */
#rotate-overlay {
  display:none;
  position:fixed; inset:0; z-index:9999;
  background:#111;
  flex-direction:column;
  align-items:center; justify-content:center;
  gap:20px; text-align:center; padding:40px;
}
#rotate-overlay .icon { font-size:4rem; animation:tilt 1.8s ease-in-out infinite; }
@keyframes tilt {
  0%,100% { transform:rotate(0deg); }
  50%      { transform:rotate(90deg); }
}
#rotate-overlay .msg { font-size:1.2rem; font-weight:700; color:#fff; line-height:1.7; }
#rotate-overlay .sub { font-size:.82rem; color:#555; }

/* ── 메인 보드 ── */
#board {
  display:flex; flex-direction:row;
  gap:6px; width:100%; padding:6px;
  /* height는 JS가 window.innerHeight 기준으로 동적 설정 */
}

/* ── 팀 패널 ── */
.team-panel {
  flex:4; border-radius:16px;
  display:flex; align-items:center; justify-content:center;
  font-weight:900; color:#fff;
  cursor:pointer; position:relative; overflow:hidden;
  touch-action:none; -webkit-touch-callout:none;
  /* 폰트 크기: 패널 높이 기준 동적 적용 (JS) */
  font-size:5rem;
}
.team-panel:active { filter:brightness(1.3); }

/* ── 중앙 패널 ── */
.center {
  flex:2.4; display:flex; flex-direction:column;
  gap:5px; min-width:0;
}

/* ── 팀명 ── */
.name-row { display:flex; gap:6px; flex-shrink:0; }
.tname {
  flex:1; background:transparent; border:none;
  border-bottom:2px solid #333; color:#fff;
  font-weight:700; text-align:center;
  outline:none; padding:3px; min-width:0;
  transition:color .3s, border-bottom-color .3s;
  font-size:clamp(.8rem,2.5vw,1.1rem);
}
.tname-red  { color:#ff6666; border-bottom-color:#ff6666; }
.tname-blue { color:#6699ff; border-bottom-color:#6699ff; }

/* ── 세트 박스 ── */
.set-row { display:flex; gap:6px; flex-shrink:0; }
.set-box {
  flex:1; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-weight:900; color:#fff;
  cursor:pointer; position:relative; overflow:hidden;
  touch-action:none; -webkit-touch-callout:none;
  font-size:clamp(1.6rem,4vw,3.2rem);
}
.set-box:active { filter:brightness(1.4); }

/* ── 타이머 ── */
.timer-box {
  background:#1c1c1c; border:2px solid #2a2a2a; border-radius:14px;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  gap:6px; padding:8px; flex:1; min-height:0;
}
.timer-label {
  color:#666; letter-spacing:.12em; font-weight:700;
  font-size:clamp(.7rem,1.8vw,.95rem);
}
.timer-time {
  font-family:'Orbitron','Courier New',monospace;
  font-weight:900; letter-spacing:.06em; transition:color .4s;
  font-size:clamp(1.6rem,5vw,3.8rem);
  line-height:1.1;
}
.timer-status { color:#555; font-weight:600; font-size:clamp(.65rem,1.5vw,.85rem); }
.t-controls {
  display:flex; gap:4px; align-items:center;
  flex-wrap:wrap; justify-content:center;
}
.t-input {
  width:50px; padding:4px; border-radius:8px;
  background:#2a2a2a; border:1px solid #444; color:#fff;
  text-align:center; font-weight:700;
  font-size:clamp(.75rem,1.8vw,.95rem);
}
.t-input::-webkit-outer-spin-button,
.t-input::-webkit-inner-spin-button { -webkit-appearance:none; }
.tbtn {
  padding:5px 10px; border:none; border-radius:8px;
  font-weight:700; cursor:pointer; touch-action:manipulation;
  font-size:clamp(.7rem,1.6vw,.9rem);
}
.tbtn:active { transform:scale(.94); }
#btnStart { background:#00cc55; color:#fff; }
#btnPause { background:#ff8800; color:#fff; display:none; }
#btnReset { background:#444; color:#ddd; }

/* ── 액션 버튼 ── */
.action-btns { display:flex; gap:4px; flex-shrink:0; }
.abtn {
  background:#2a2a2a; color:#ccc;
  border:1px solid #3a3a3a; border-radius:10px;
  cursor:pointer; text-align:center; font-weight:600;
  touch-action:manipulation; flex:1;
  padding:8px 4px;
  font-size:clamp(.65rem,1.5vw,.88rem);
}
.abtn:active { background:#3a3a3a; color:#fff; }

/* ── 저작권 ── */
.copyright {
  text-align:center; color:#2a2a2a;
  font-size:clamp(.45rem,1vw,.6rem);
  flex-shrink:0; padding:1px 0;
}

/* ── 롱프레스 링 ── */
.press-ring {
  position:absolute; border-radius:50%;
  border:5px solid rgba(255,255,255,0.6);
  width:90px; height:90px;
  transform:scale(0); opacity:0;
  transition:transform .6s ease, opacity .6s ease;
  pointer-events:none;
}
.press-ring.active { transform:scale(3); opacity:1; }
</style>
</head>
<body>

<div id="rotate-overlay">
  <div class="icon">📱</div>
  <div class="msg">화면을 가로로 돌려주세요</div>
  <div class="sub">스마트 점수판은 가로 모드에서<br>최적으로 표시됩니다.</div>
</div>

<div id="board">
  <div class="team-panel" id="teamA">
    <div class="press-ring" id="ringA"></div>
    <span id="scoreA">0</span>
  </div>

  <div class="center">
    <div class="name-row">
      <input class="tname tname-red"  id="nameA" value="A 팀" maxlength="8">
      <input class="tname tname-blue" id="nameB" value="B 팀" maxlength="8">
    </div>
    <div class="set-row" id="setRow">
      <div class="set-box" id="setA">
        <div class="press-ring" id="ringSetA"></div>
        <span id="setScoreA">0</span>
      </div>
      <div class="set-box" id="setB">
        <div class="press-ring" id="ringSetB"></div>
        <span id="setScoreB">0</span>
      </div>
    </div>
    <div class="timer-box" id="timerBox">
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
// ══════════════════════════════════════════════════
// 레이아웃: window.innerHeight 기준으로 보드 높이 설정
// Streamlit iframe 높이도 postMessage로 동기화
// ══════════════════════════════════════════════════
function fitLayout(){
  const W = window.innerWidth;
  const H = window.innerHeight;

  // 1) 보드 높이를 실제 뷰포트에 맞춤
  const board = document.getElementById('board');
  board.style.height = H + 'px';

  // 2) Streamlit iframe 높이 동기화 (공식 방법)
  window.parent.postMessage({ type:'streamlit:setFrameHeight', height: H }, '*');

  // 3) 팀 패널 폰트: 패널 높이의 약 38%
  const panelH = H - 12; // padding 제외
  const panelFont = Math.max(40, Math.floor(panelH * 0.38));
  document.getElementById('teamA').style.fontSize = panelFont + 'px';
  document.getElementById('teamB').style.fontSize = panelFont + 'px';

  // 4) 세트 행 높이: 전체의 18%
  const setH = Math.max(60, Math.floor(H * 0.18));
  document.getElementById('setRow').style.height = setH + 'px';

  // 5) 팀명 행 높이: 전체의 7%
  const nameH = Math.max(32, Math.floor(H * 0.07));
  document.querySelector('.name-row').style.height = nameH + 'px';
  document.querySelectorAll('.tname').forEach(el => el.style.fontSize =
    Math.max(11, Math.floor(nameH * 0.55)) + 'px');
}

// 방향 감지 (JS 기반 — iframe 내에서 screen.orientation 사용)
function isPortrait(){
  if(screen.orientation && screen.orientation.type)
    return screen.orientation.type.startsWith('portrait');
  if(typeof window.orientation !== 'undefined')
    return window.orientation === 0 || window.orientation === 180;
  return window.innerHeight > window.innerWidth;
}
function checkOrientation(){
  document.getElementById('rotate-overlay').style.display =
    isPortrait() ? 'flex' : 'none';
  fitLayout();
}

// 초기 실행
checkOrientation();

// 이벤트 등록
window.addEventListener('resize', checkOrientation);
window.addEventListener('orientationchange', ()=>setTimeout(checkOrientation, 200));
if(screen.orientation) screen.orientation.addEventListener('change', ()=>setTimeout(checkOrientation, 200));

// ══════════════════════════════════════════════════
// 상태
// ══════════════════════════════════════════════════
let sA=0,sB=0,setA=0,setB=0;
let tLeft=600,tTotal=600,tRunning=false,tInterval=null;
let colorsNormal=true;
const CR='#EE0000',CB='#0033EE',SR='#BB0000',SB2='#0022CC';

function applyColors(){
  document.getElementById('teamA').style.background=colorsNormal?CR:CB;
  document.getElementById('teamB').style.background=colorsNormal?CB:CR;
  document.getElementById('setA').style.background =colorsNormal?SR:SB2;
  document.getElementById('setB').style.background =colorsNormal?SB2:SR;
  document.getElementById('nameA').className='tname '+(colorsNormal?'tname-red':'tname-blue');
  document.getElementById('nameB').className='tname '+(colorsNormal?'tname-blue':'tname-red');
}
applyColors();

function render(){
  document.getElementById('scoreA').textContent   =sA;
  document.getElementById('scoreB').textContent   =sB;
  document.getElementById('setScoreA').textContent=setA;
  document.getElementById('setScoreB').textContent=setB;
}
function resetScores(){sA=0;sB=0;render();}
function resetSets(){setA=0;setB=0;render();}
function swapTeams(){
  [sA,sB]=[sB,sA];[setA,setB]=[setB,setA];
  let na=document.getElementById('nameA').value;
  let nb=document.getElementById('nameB').value;
  document.getElementById('nameA').value=nb;
  document.getElementById('nameB').value=na;
  colorsNormal=!colorsNormal;
  applyColors();render();
  ['teamA','teamB'].forEach(id=>{
    let el=document.getElementById(id);
    el.style.filter='brightness(1.6)';
    setTimeout(()=>el.style.filter='',280);
  });
}

// ══════════════════════════════════════════════════
// 롱프레스 (touchstart preventDefault → 2점 버그 차단)
// ══════════════════════════════════════════════════
function setupPress(el,ringEl,onShort,onLong){
  let timer=null,fired=false;
  function startPress(x,y){
    fired=false;
    let r=el.getBoundingClientRect();
    ringEl.style.left=(x-r.left-45)+'px';
    ringEl.style.top =(y-r.top -45)+'px';
    ringEl.classList.add('active');
    timer=setTimeout(()=>{fired=true;onLong();ringEl.classList.remove('active');},600);
  }
  function endPress(){
    clearTimeout(timer);ringEl.classList.remove('active');
    if(!fired)onShort();fired=false;
  }
  function cancelPress(){
    clearTimeout(timer);ringEl.classList.remove('active');fired=true;
  }
  el.addEventListener('touchstart', e=>{e.preventDefault();startPress(e.touches[0].clientX,e.touches[0].clientY);},{passive:false});
  el.addEventListener('touchend',   e=>{e.preventDefault();endPress();},{passive:false});
  el.addEventListener('touchcancel',e=>{e.preventDefault();cancelPress();},{passive:false});
  el.addEventListener('mousedown',  e=>startPress(e.clientX,e.clientY));
  el.addEventListener('mouseup',    ()=>endPress());
  el.addEventListener('mouseleave', ()=>cancelPress());
  el.addEventListener('contextmenu',e=>e.preventDefault());
}

setupPress(document.getElementById('teamA'),document.getElementById('ringA'),
  ()=>{sA++;render();},()=>{if(sA>0)sA--;render();});
setupPress(document.getElementById('teamB'),document.getElementById('ringB'),
  ()=>{sB++;render();},()=>{if(sB>0)sB--;render();});
setupPress(document.getElementById('setA'),document.getElementById('ringSetA'),
  ()=>{setA++;render();},()=>{if(setA>0)setA--;render();});
setupPress(document.getElementById('setB'),document.getElementById('ringSetB'),
  ()=>{setB++;render();},()=>{if(setB>0)setB--;render();});

// ══════════════════════════════════════════════════
// 알람
// ══════════════════════════════════════════════════
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

// ══════════════════════════════════════════════════
// 타이머
// ══════════════════════════════════════════════════
function fmt(s){return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}
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

components.html(HTML, height=700, scrolling=False)
