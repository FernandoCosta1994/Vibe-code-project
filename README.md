# Snake Game — Forest Edition

A classic Snake game with a forest theme. Two versions:

- **Desktop** — Python + pygame (real-time, keyboard controls)
- **Streamlit** — Web version (snake moves continuously, click to steer)

## Requirements

- Python 3.9 or newer (recommended)
- `pip` (Python package manager)

All dependencies are in `requirements.txt`.

## Set up (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If execution policy blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Run the desktop game

```powershell
python snake_game.py
```

## Run the Streamlit version (local)

```powershell
streamlit run streamlit_snake.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repo, branch `main`, and file `streamlit_snake.py`.
4. Click **Deploy**. Your app will be live at `https://<your-app>.streamlit.app`.

---

## Controls

**Desktop:** Arrow keys or W/A/S/D. Main menu: ↑/↓ for difficulty, ENTER to start. After game over: ENTER = retry, M = menu, ESC = quit.

**Streamlit:** Same controls as desktop — ↑↓←→ or W A S D. Click the game area to focus, then use keyboard.
