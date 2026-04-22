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
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
  body {
    background:#111; color:#fff;
    font-family:'Segoe UI','Malgun Gothic',sans-serif;
    height:700px; overflow:hidden; user-select:none;
  }
  .board { display:flex; gap:6px; height:700px; padding:6px; }

  .team-panel {
    flex:4; border-radius:16px;
    display:flex; align-items:center; justify-content:center;
    font-size:clamp(6rem,18vw,14rem); font-weight:900; color:#fff;
    cursor:pointer; transition:filter .15s;
    position:relative; overflow:hidden;
  }
  .team-panel:active { filter:brightness(1.3); }

  .press-ring {
    position:absolute; border-radius:50%;
    border:6px solid rgba(255,255,255,0.6);
    width:120px; height:120px;
    transform:scale(0); opacity:0;
    transition:transform .6s ease, opacity .6s ease;
    pointer-events:none;
  }
  .press-ring.active { transform:scale(2.5); opacity:1; }

  .center { flex:2.2; display:flex; flex-direction:column; gap:6px; }

  .set-row { display:flex; gap:6px; height:130px; flex-shrink:0; }
  .set-box {
    flex:1; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:3.8rem; font-weight:900; color:#fff;
    cursor:pointer; transition:filter .15s;
  }
  .set-box:active { filter:brightness(1.4); }

  .timer-box {
    flex:1; background:#1c1c1c; border:2px solid #2a2a2a; border-radius:14px;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:10px;
    padding:12px 8px;
  }
  .timer-label { font-size:1.05rem; color:#666; letter-spacing:.15em; text-transform:uppercase; font-weight:700; }
  .timer-time {
    font-family:'Orbitron', 'Courier New', monospace;
    font-size:clamp(3rem,6vw,4.2rem);
    font-weight:900; letter-spacing:.08em;
    transition:color .4s;
  }
  .timer-status { font-size:.9rem; color:#555; font-weight:600; }
  .t-controls { display:flex; gap:6px; align-items:center; }
  .t-input {
    width:64px; padding:6px; border-radius:8px;
    background:#2a2a2a; border:1px solid #444; color:#fff;
    text-align:center; font-size:1rem; font-weight:700;
  }
  .t-input::-webkit-outer-spin-button,
  .t-input::-webkit-inner-spin-button { -webkit-appearance:none; }
  .tbtn {
    padding:8px 16px; border:none; border-radius:8px;
    font-size:1rem; font-weight:700; cursor:pointer; transition:.15s;
  }
  .tbtn:active { transform:scale(.94); }
  #btnStart { background:#00cc55; color:#fff; }
  #btnPause { background:#ff8800; color:#fff; display:none; }
  #btnReset { background:#444; color:#ddd; }

  .action-row { display:flex; flex-direction:column; gap:5px; flex-shrink:0; }
  .abtn {
    background:#2a2a2a; color:#ccc;
    border:1px solid #3a3a3a; border-radius:10px;
    padding:11px; font-size:.95rem; cursor:pointer;
    transition:.15s; text-align:center; font-weight:600;
  }
  .abtn:active { background:#3a3a3a; color:#fff; }

  .team-name-row { display:flex; gap:6px; flex-shrink:0; height:42px; }
  .tname {
    flex:1; background:transparent; border:none;
    border-bottom:2px solid #333; color:#fff;
    font-size:1.1rem; font-weight:700;
    text-align:center; outline:none; border-radius:0; padding:4px;
    transition: color .3s, border-bottom-color .3s;
  }
  .tname:focus { border-bottom-color:#666; }
  .tname-red  { color:#ff6666; border-bottom-color:#ff6666; }
  .tname-blue { color:#6699ff; border-bottom-color:#6699ff; }
</style>
</head>
<body>
<div class="board">

  <div class="team-panel" id="teamA">
    <div class="press-ring" id="ringA"></div>
    <span id="scoreA">0</span>
  </div>

  <div class="center">
    <div class="team-name-row">
      <input class="tname tname-red"  id="nameA" value="A 팀" maxlength="8">
      <input class="tname tname-blue" id="nameB" value="B 팀" maxlength="8">
    </div>

    <div class="set-row">
      <div class="set-box" id="setA" onclick="addSet('a')"><span id="setScoreA">0</span></div>
      <div class="set-box" id="setB" onclick="addSet('b')"><span id="setScoreB">0</span></div>
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

    <div class="action-row">
      <div class="abtn" onclick="swapTeams()">팀 교체</div>
      <div class="abtn" onclick="resetScores()">점수 초기화</div>
      <div class="abtn" onclick="resetSets()">세트 초기화</div>
    </div>
  </div>

  <div class="team-panel" id="teamB">
    <div class="press-ring" id="ringB"></div>
    <span id="scoreB">0</span>
  </div>
</div>

<script>
let sA=0, sB=0, setA=0, setB=0;
let tLeft=600, tTotal=600, tRunning=false, tInterval=null;
let colorsNormal = true;

const COLOR_RED  = '#EE0000', COLOR_BLUE = '#0033EE';
const SET_RED    = '#BB0000', SET_BLUE   = '#0022CC';

function applyColors(){
  if(colorsNormal){
    document.getElementById('teamA').style.background = COLOR_RED;
    document.getElementById('teamB').style.background = COLOR_BLUE;
    document.getElementById('setA').style.background  = SET_RED;
    document.getElementById('setB').style.background  = SET_BLUE;
    document.getElementById('nameA').className = 'tname tname-red';
    document.getElementById('nameB').className = 'tname tname-blue';
  } else {
    document.getElementById('teamA').style.background = COLOR_BLUE;
    document.getElementById('teamB').style.background = COLOR_RED;
    document.getElementById('setA').style.background  = SET_BLUE;
    document.getElementById('setB').style.background  = SET_RED;
    document.getElementById('nameA').className = 'tname tname-blue';
    document.getElementById('nameB').className = 'tname tname-red';
  }
}
applyColors();

function render(){
  document.getElementById('scoreA').textContent = sA;
  document.getElementById('scoreB').textContent = sB;
  document.getElementById('setScoreA').textContent = setA;
  document.getElementById('setScoreB').textContent = setB;
}

function addSet(t){ if(t==='a') setA++; else setB++; render(); }
function resetScores(){ sA=0; sB=0; render(); }
function resetSets(){ setA=0; setB=0; render(); }

function swapTeams(){
  [sA,sB]=[sB,sA];
  [setA,setB]=[setB,setA];
  let na=document.getElementById('nameA').value;
  let nb=document.getElementById('nameB').value;
  document.getElementById('nameA').value=nb;
  document.getElementById('nameB').value=na;
  colorsNormal = !colorsNormal;
  applyColors();
  render();
  ['teamA','teamB'].forEach(id=>{
    let el=document.getElementById(id);
    el.style.filter='brightness(1.5)';
    setTimeout(()=>el.style.filter='',300);
  });
}

function setupPress(panelId, ringId, team){
  const panel = document.getElementById(panelId);
  const ring  = document.getElementById(ringId);
  let timer=null, fired=false;

  function onStart(e){
    fired=false;
    let cx = e.touches ? e.touches[0].clientX : e.clientX;
    let cy = e.touches ? e.touches[0].clientY : e.clientY;
    let rect = panel.getBoundingClientRect();
    ring.style.left = (cx - rect.left - 60) + 'px';
    ring.style.top  = (cy - rect.top  - 60) + 'px';
    ring.classList.add('active');
    timer = setTimeout(()=>{
      fired=true;
      if(team==='a'&&sA>0) sA--;
      else if(team==='b'&&sB>0) sB--;
      render();
      ring.classList.remove('active');
    },600);
  }
  function onEnd(){
    clearTimeout(timer); ring.classList.remove('active');
    if(!fired){ if(team==='a') sA++; else sB++; render(); }
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

function playAlarm(){
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const pattern = [
      {freq:880, start:0,    dur:0.18},
      {freq:880, start:0.22, dur:0.18},
      {freq:880, start:0.44, dur:0.18},
      {freq:1046,start:0.7,  dur:0.35},
      {freq:880, start:1.1,  dur:0.18},
      {freq:1046,start:1.35, dur:0.55},
    ];
    pattern.forEach(({freq,start,dur})=>{
      const osc=ctx.createOscillator(), gain=ctx.createGain();
      osc.connect(gain); gain.connect(ctx.destination);
      osc.type='square'; osc.frequency.value=freq;
      gain.gain.setValueAtTime(0.35, ctx.currentTime+start);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime+start+dur);
      osc.start(ctx.currentTime+start);
      osc.stop(ctx.currentTime+start+dur+0.05);
    });
  } catch(e){ console.warn('Audio error',e); }
}

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
  document.getElementById('tStatus').textContent='진행 중';
  tInterval=setInterval(()=>{
    if(tLeft>0){ tLeft--; updateTimerUI(); }
    else{
      clearInterval(tInterval); tRunning=false;
      document.getElementById('tStatus').textContent='종료!';
      document.getElementById('btnPause').style.display='none';
      document.getElementById('btnStart').style.display='inline-block';
      playAlarm();
    }
  },1000);
}

function pauseTimer(){
  clearInterval(tInterval); tRunning=false;
  document.getElementById('btnPause').style.display='none';
  document.getElementById('btnStart').style.display='inline-block';
  document.getElementById('tStatus').textContent='일시정지';
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
