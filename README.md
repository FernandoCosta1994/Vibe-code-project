# Snake Game (Python + pygame)

A simple classic Snake game built with Python and `pygame`.

## Requirements

- Python 3.9 or newer (recommended)
- `pip` (Python package manager)

All Python dependencies are listed in `requirements.txt`.

## Set up a virtual environment (Windows / PowerShell)

From the project folder (`Vibe coding project`), run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If execution policy blocks activation, you may need to allow scripts temporarily:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Running the game

With the virtual environment activated and dependencies installed:

```powershell
python snake_game.py
```

## Controls

- Arrow keys or `W / A / S / D` to move the snake.
- The snake wraps around screen edges.
- The game ends when the snake collides with itself.

After game over:

- Press **ENTER** to play again.
- Press **ESC** or close the window to quit.

