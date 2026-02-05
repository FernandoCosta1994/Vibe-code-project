# Snake Game — Forest Edition

A classic Snake game with a forest theme. Three ways to play:

- **Desktop** — Python + pygame (real-time, keyboard controls)
- **Streamlit** — Download HTML from the app, open in browser
- **HTML** — Open `snake_game.html` directly in any browser

## Requirements

- Python 3.9 or newer (recommended)
- `pip` (Python package manager)

All dependencies are in `requirements.txt`.

## Play in browser (no install)

Double-click `snake_game.html` or open it in Chrome/Edge. Use **↑↓←→** or **W A S D** to move.

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

**Streamlit:** Download the HTML file from the app, then open it in your browser. Same controls as desktop — ↑↓←→ or W A S D.
