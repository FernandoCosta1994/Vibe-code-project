# Snake Game — Forest Edition

A classic Snake game with a forest theme, built with Python and `pygame`.

## Requirements

- Python 3.9 or newer (recommended)
- `pip` (Python package manager)

All Python dependencies are listed in `requirements.txt`.

## Set up a virtual environment (Windows / PowerShell)

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

## Run the game

```powershell
python snake_game.py
```

## Controls

- **Arrow keys** or **W / A / S / D** to move the snake.
- The snake wraps around screen edges.
- The game ends when the snake collides with itself.

**Main menu:** ↑/↓ to choose difficulty (Easy, Normal, Hard), ENTER to start.

**After game over:**
- **ENTER** — play again
- **M** — back to menu
- **ESC** — quit
