# Snake Game — Forest Edition

A classic Snake game with a forest theme. Play on desktop (Python + pygame) or in the browser (HTML5).

## Play in the browser

Open `snake_game.html` in any browser, or deploy it to GitHub Pages (see below).

## Deploy to GitHub Pages

1. Push your code to GitHub (including `snake_game.html`).
2. In your repo: **Settings** → **Pages**.
3. Under **Source**, choose **Deploy from a branch**.
4. Select branch `main` and folder `/ (root)`.
5. Click **Save**. Your game will be at `https://<username>.github.io/<repo-name>/snake_game.html`.

---

## Desktop version (Python + pygame)

### Requirements

- Python 3.9 or newer (recommended)
- `pip` (Python package manager)

All Python dependencies are listed in `requirements.txt`.

### Set up a virtual environment (Windows / PowerShell)

From the project folder, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If execution policy blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Run the desktop game

```powershell
python snake_game.py
```

---

## Controls

- **Arrow keys** or **W / A / S / D** to move the snake.
- The snake wraps around screen edges.
- The game ends when the snake collides with itself.

**Main menu:** ↑/↓ to choose difficulty (Easy, Normal, Hard), ENTER to start.

**After game over:**
- **ENTER** — play again
- **M** — back to menu
- **ESC** — quit (desktop) or back to menu (web)

