"""
Snake Game — Forest Edition (Streamlit)
Embedded HTML5 version: plays like the pygame version with keyboard (↑↓←→ or WASD).
"""
import streamlit as st
import streamlit.components.v1 as components

# Difficulty: speed multiplier (higher = faster)
DIFFICULTIES = {"Easy": 0.8, "Normal": 1.0, "Hard": 1.3}


def get_game_html(speed_mult: float) -> str:
    """Generate full HTML5 Snake game with forest theme and keyboard controls."""
    tick_ms = int(150 / speed_mult)  # Base 150ms, slower for Easy, faster for Hard
    return f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ margin: 0; padding: 0; }}
body {{ background: #0a1410; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: system-ui; }}
#game {{ border-radius: 8px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }}
#c {{ display: block; background: #061a14; cursor: default; }}
#c:focus {{ outline: none; }}
.hud {{ background: #08100c; color: #fff; padding: 6px 12px; display: flex; justify-content: space-between; font-size: 14px; border-bottom: 1px solid #193723; }}
.hud span {{ color: #c3e68c; }}
</style>
</head>
<body>
<div id="game">
<div class="hud"><span>Score: <b id="score">0</b></span><span>Best: <b id="best">0</b></span></div>
<canvas id="c" width="800" height="568" tabindex="1" style="vertical-align:top"></canvas>
</div>
<script>
const C=document.getElementById('c'), ctx=C.getContext('2d');
const W=800,H=568,CELL=20,COLS=W/CELL,ROWS=H/CELL;
const TICK_MS={tick_ms};

const COLORS={{forestTop:'#061a14',forestMid:'#0a2d1c',forestBottom:'#241a12',treeDark:'#091910',treeLeaves:'#144623',
snakeHead:'#88ff44',snakeBody:'#44cc44',snakeBelly:'#228822',appleRed:'#d73c3c',appleHighlight:'#fad2d2',
appleLeaf:'#28823c',appleStem:'#5a371e',grid:'#142d1e',white:'#fff',black:'#111'}};

let snake=[], dir=[1,0], food, score=0, best=0, grow=0, tick=0, state='play', lastMove=0;

function rndFood(){{
  const set=new Set(snake.map(s=>s[0]+','+s[1]));
  const free=[];
  for(let x=0;x<COLS;x++)for(let y=0;y<ROWS;y++)if(!set.has(x+','+y))free.push([x,y]);
  return free[Math.floor(Math.random()*free.length)]||[0,0];
}}

function reset(){{
  snake=[[Math.floor(COLS/2),Math.floor(ROWS/2)]];
  dir=[1,0]; grow=0; food=rndFood(); score=0; state='play';
}}

function roundRect(x,y,w,h,r){{
  ctx.beginPath();
  ctx.moveTo(x+r,y);
  ctx.lineTo(x+w-r,y);
  ctx.quadraticCurveTo(x+w,y,x+w,y+r);
  ctx.lineTo(x+w,y+h-r);
  ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
  ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);
  ctx.lineTo(x,y+r);
  ctx.quadraticCurveTo(x,y,x+r,y);
  ctx.closePath();
}}

function drawBg(){{
  const g=ctx.createLinearGradient(0,0,0,H);
  g.addColorStop(0,COLORS.forestTop);
  g.addColorStop(0.45,COLORS.forestMid);
  g.addColorStop(1,COLORS.forestBottom);
  ctx.fillStyle=g;
  ctx.fillRect(0,0,W,H);
  const sway=Math.sin(tick*0.01)*4;
  for(let x=-60;x<W+60;x+=120){{
    const i=Math.floor((x+60)/120), bx=x+sway*(1+(i%3));
    ctx.fillStyle=COLORS.treeDark;
    ctx.fillRect(bx,H-180,22,140);
    ctx.fillStyle=COLORS.treeLeaves;
    ctx.beginPath();
    ctx.moveTo(bx+11,H-200);
    ctx.lineTo(bx-25,H-40);
    ctx.lineTo(bx+47,H-40);
    ctx.closePath();
    ctx.fill();
  }}
  ctx.fillStyle='rgba(78,160,120,0.25)';
  ctx.fillRect(0,H-120,W,100);
}}

function drawGrid(){{
  ctx.strokeStyle=COLORS.grid;
  ctx.lineWidth=1;
  for(let x=0;x<=W;x+=CELL){{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke(); }}
  for(let y=0;y<=H;y+=CELL){{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke(); }}
}}

function drawSnake(){{
  if(!snake.length) return;
  for(let i=0;i<snake.length;i++){{
    const seg=snake[i], gx=seg[0], gy=seg[1], x=gx*CELL, y=gy*CELL, head=(i===0);
    ctx.strokeStyle='#0a3010';
    ctx.lineWidth=2;
    ctx.fillStyle=COLORS.snakeBody;
    ctx.fillRect(x+1,y+1,CELL-2,CELL-2);
    ctx.strokeRect(x+1,y+1,CELL-2,CELL-2);
    if(head){{
      ctx.fillStyle=COLORS.snakeHead;
      ctx.fillRect(x,y,CELL,CELL);
      ctx.strokeStyle='#1a5020';
      ctx.strokeRect(x,y,CELL,CELL);
      const [dx,dy]=dir;
      let ex1,ey1,ex2,ey2;
      if(dx===1){{ ex1=x+CELL-6;ey1=y+6;ex2=x+CELL-6;ey2=y+CELL-6; }}
      else if(dx===-1){{ ex1=x+6;ey1=y+6;ex2=x+6;ey2=y+CELL-6; }}
      else if(dy===-1){{ ex1=x+6;ey1=y+6;ex2=x+CELL-6;ey2=y+6; }}
      else{{ ex1=x+6;ey1=y+CELL-6;ex2=x+CELL-6;ey2=y+CELL-6; }}
      ctx.fillStyle='#ffffff';
      ctx.beginPath();
      ctx.arc(ex1,ey1,3,0,6.28);
      ctx.arc(ex2,ey2,3,0,6.28);
      ctx.fill();
      ctx.fillStyle='#000000';
      ctx.beginPath();
      ctx.arc(ex1,ey1,1.5,0,6.28);
      ctx.arc(ex2,ey2,1.5,0,6.28);
      ctx.fill();
    }}
  }}
}}

function drawFood(){{
  const [fx,fy]=food, cx=fx*CELL+CELL/2, cy=fy*CELL+CELL/2, r=CELL/2-3;
  ctx.fillStyle=COLORS.appleRed;
  ctx.beginPath();
  ctx.arc(cx,cy,r,0,Math.PI*2);
  ctx.fill();
  ctx.fillStyle=COLORS.appleHighlight;
  ctx.beginPath();
  ctx.arc(cx-r/3,cy-r/3,Math.max(1,r/4),0,Math.PI*2);
  ctx.fill();
  ctx.fillStyle=COLORS.appleStem;
  ctx.fillRect(cx-1,cy-r-4,3,6);
  ctx.fillStyle=COLORS.appleLeaf;
  ctx.beginPath();
  ctx.moveTo(cx+2,cy-r);
  ctx.lineTo(cx+10,cy-r-6);
  ctx.lineTo(cx+6,cy-r+2);
  ctx.closePath();
  ctx.fill();
}}

function move(){{
  const h=snake[0], nx=(h[0]+dir[0]+COLS)%COLS, ny=(h[1]+dir[1]+ROWS)%ROWS;
  for(let i=1;i<snake.length;i++)if(snake[i][0]===nx&&snake[i][1]===ny){{ state='over'; if(score>best)best=score; return; }}
  snake.unshift([nx,ny]);
  if(grow>0)grow--; else snake.pop();
  if(nx===food[0]&&ny===food[1]){{ score++; grow++; food=rndFood(); }}
}}

function drawOver(){{
  ctx.fillStyle='rgba(0,0,0,0.7)';
  ctx.fillRect(0,0,W,H);
  ctx.fillStyle=COLORS.white;
  ctx.font='bold 36px system-ui';
  ctx.textAlign='center';
  ctx.fillText('Game Over',W/2,H/2-50);
  ctx.font='18px system-ui';
  ctx.fillText('Score: '+score,W/2,H/2);
  ctx.fillStyle='#c3e68c';
  ctx.fillText('Best: '+best,W/2,H/2+35);
  ctx.fillStyle='#fff';
  ctx.fillText('ENTER: play again   •   Click "Back to Menu" below',W/2,H/2+80);
}}

reset();
C.width=C.width;
C.focus();
document.getElementById('score').textContent=0;
document.getElementById('best').textContent=best;

document.addEventListener('keydown',e=>{{
  if(state==='over'){{
    if(e.key==='Enter'){{ reset(); e.preventDefault(); }}
    else if(e.key==='m'||e.key==='M'){{ /* User can click Back to Menu below */ e.preventDefault(); }}
    return;
  }}
  const opp=[-dir[0],-dir[1]];
  if(e.key==='ArrowUp'||e.key==='w'||e.key==='W'){{ if(opp[1]!==-1)dir=[0,-1]; e.preventDefault(); }}
  else if(e.key==='ArrowDown'||e.key==='s'||e.key==='S'){{ if(opp[1]!==1)dir=[0,1]; e.preventDefault(); }}
  else if(e.key==='ArrowLeft'||e.key==='a'||e.key==='A'){{ if(opp[0]!==-1)dir=[-1,0]; e.preventDefault(); }}
  else if(e.key==='ArrowRight'||e.key==='d'||e.key==='D'){{ if(opp[0]!==1)dir=[1,0]; e.preventDefault(); }}
}});

function loop(now){{
  tick++;
  if(state==='over'){{
    drawBg(); drawGrid(); drawSnake(); drawFood(); drawOver();
    document.getElementById('score').textContent=score;
    document.getElementById('best').textContent=best;
    requestAnimationFrame(loop);
    return;
  }}
  if(now-lastMove>=TICK_MS){{
    lastMove=now;
    move();
  }}
  document.getElementById('score').textContent=score;
  document.getElementById('best').textContent=best;
  drawBg();
  drawGrid();
  drawSnake();
  drawFood();
  if(snake.length>0){{
    const h=snake[0], px=h[0]*CELL, py=h[1]*CELL;
    ctx.strokeStyle='#00ff00';
    ctx.lineWidth=3;
    ctx.strokeRect(px-1,py-1,CELL+2,CELL+2);
  }}
  requestAnimationFrame(loop);
}}
let lastMove=0;
requestAnimationFrame(loop);
</script>
</body>
</html>
"""


def main():
    st.set_page_config(page_title="Snake — Forest", page_icon="🐍", layout="centered")
    st.markdown(
        "<h1 style='text-align:center;color:#c3e68c'>🐍 Snake — Forest Edition</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#6b8a6b'>↑↓←→ or W A S D to move · Same as the desktop version</p>",
        unsafe_allow_html=True,
    )

    if "screen" not in st.session_state:
        st.session_state.screen = "menu"

    if st.session_state.screen == "menu":
        st.subheader("Choose difficulty")
        diff = st.radio(
            "Difficulty",
            list(DIFFICULTIES.keys()),
            index=1,
            horizontal=True,
            label_visibility="collapsed",
        )
        speed_mult = DIFFICULTIES[diff]
        if st.button("Start Game", type="primary", use_container_width=True):
            st.session_state.screen = "game"
            st.session_state.difficulty = diff
            st.session_state.speed_mult = speed_mult
            st.rerun()
        st.caption("Use ↑/↓ to choose, ENTER to start — like the desktop game")
        return

    # Game screen
    speed_mult = st.session_state.get("speed_mult", 1.0)
    html = get_game_html(speed_mult)
    st.caption("👆 Click the game area below to focus, then use ↑↓←→ or W A S D")
    components.html(html, height=620, scrolling=False)

    if st.button("← Back to Menu"):
        st.session_state.screen = "menu"
        st.rerun()


if __name__ == "__main__":
    main()
