"""
Snake Game — Forest Edition (Streamlit)
Turn-based version: each button press = one move.
"""
import streamlit as st
import random
from PIL import Image, ImageDraw

# Game config
COLS, ROWS = 24, 18
CELL = 20
W, H = COLS * CELL, ROWS * CELL

# Forest palette (RGB)
FOREST_TOP = (6, 26, 20)
FOREST_MID = (10, 45, 28)
FOREST_BOTTOM = (36, 26, 18)
TREE_DARK = (9, 25, 16)
TREE_LEAVES = (20, 70, 35)
SNAKE_HEAD = (170, 240, 120)
SNAKE_BODY = (90, 190, 90)
SNAKE_BELLY = (40, 110, 60)
SNAKE_OUTLINE = (15, 40, 20)
APPLE_RED = (215, 60, 60)
APPLE_HIGHLIGHT = (250, 210, 210)
APPLE_LEAF = (40, 130, 60)
APPLE_STEM = (90, 55, 30)
GRID_COLOR = (20, 45, 30)


def init_state():
    if "snake" not in st.session_state:
        st.session_state.snake = [(COLS // 2, ROWS // 2)]
        st.session_state.direction = (1, 0)
        st.session_state.grow_pending = 0
        st.session_state.food = random_food(st.session_state.snake)
        st.session_state.score = 0
        st.session_state.high_score = 0
        st.session_state.game_over = False
        st.session_state.screen = "menu"
        st.session_state.difficulty = 1


def random_food(snake_positions):
    positions = set(snake_positions)
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in positions]
    return random.choice(free) if free else (0, 0)


def move_snake():
    s = st.session_state
    h = s.snake[0]
    dx, dy = s.direction
    nx = (h[0] + dx) % COLS
    ny = (h[1] + dy) % ROWS

    if (nx, ny) in s.snake[1:]:
        s.game_over = True
        if s.score > s.high_score:
            s.high_score = s.score
        return

    s.snake.insert(0, (nx, ny))
    if s.grow_pending > 0:
        s.grow_pending -= 1
    else:
        s.snake.pop()

    if (nx, ny) == s.food:
        s.score += 1
        s.grow_pending += 1
        s.food = random_food(s.snake)


def render_board():
    img = Image.new("RGB", (W, H), FOREST_TOP)
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(H):
        t = y / H
        if t < 0.45:
            blend = t / 0.45
            r = int(FOREST_TOP[0] * (1 - blend) + FOREST_MID[0] * blend)
            g = int(FOREST_TOP[1] * (1 - blend) + FOREST_MID[1] * blend)
            b = int(FOREST_TOP[2] * (1 - blend) + FOREST_MID[2] * blend)
        else:
            blend = (t - 0.45) / 0.55
            r = int(FOREST_MID[0] * (1 - blend) + FOREST_BOTTOM[0] * blend)
            g = int(FOREST_MID[1] * (1 - blend) + FOREST_BOTTOM[1] * blend)
            b = int(FOREST_MID[2] * (1 - blend) + FOREST_BOTTOM[2] * blend)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Grid
    for x in range(0, W + 1, CELL):
        draw.line([(x, 0), (x, H)], fill=GRID_COLOR)
    for y in range(0, H + 1, CELL):
        draw.line([(0, y), (W, y)], fill=GRID_COLOR)

    # Snake
    for i, (gx, gy) in enumerate(st.session_state.snake):
        x, y = gx * CELL, gy * CELL
        is_head = i == 0
        draw.rectangle([x, y, x + CELL - 1, y + CELL - 1], outline=SNAKE_OUTLINE, fill=SNAKE_BODY)
        draw.rectangle([x + 2, y + CELL // 2, x + CELL - 3, y + CELL - 1], fill=SNAKE_BELLY)
        if is_head:
            draw.rectangle([x + 1, y + 1, x + CELL - 2, y + CELL - 2], fill=SNAKE_HEAD)
            dx, dy = st.session_state.direction
            if dx == 1:
                draw.ellipse([x + CELL - 10, y + 6, x + CELL - 4, y + 12], fill=(255, 255, 255))
                draw.ellipse([x + CELL - 10, y + CELL - 12, x + CELL - 4, y + CELL - 6], fill=(255, 255, 255))
            elif dx == -1:
                draw.ellipse([x + 4, y + 6, x + 10, y + 12], fill=(255, 255, 255))
                draw.ellipse([x + 4, y + CELL - 12, x + 10, y + CELL - 6], fill=(255, 255, 255))
            elif dy == -1:
                draw.ellipse([x + 6, y + 4, x + 12, y + 10], fill=(255, 255, 255))
                draw.ellipse([x + CELL - 12, y + 4, x + CELL - 6, y + 10], fill=(255, 255, 255))
            else:
                draw.ellipse([x + 6, y + CELL - 10, x + 12, y + CELL - 4], fill=(255, 255, 255))
                draw.ellipse([x + CELL - 12, y + CELL - 10, x + CELL - 6, y + CELL - 4], fill=(255, 255, 255))

    # Food (apple)
    fx, fy = st.session_state.food
    cx, cy = fx * CELL + CELL // 2, fy * CELL + CELL // 2
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=APPLE_RED)
    draw.ellipse([cx - 4, cy - 4, cx, cy], fill=APPLE_HIGHLIGHT)
    draw.rectangle([cx - 1, cy - 10, cx + 2, cy - 4], fill=APPLE_STEM)
    draw.polygon([(cx + 2, cy - 7), (cx + 10, cy - 12), (cx + 6, cy - 5)], fill=APPLE_LEAF)

    return img


def main():
    st.set_page_config(page_title="Snake — Forest", page_icon="🐍", layout="centered")
    st.markdown(
        "<h1 style='text-align:center;color:#c3e68c'>🐍 Snake — Forest Edition</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#6b8a6b'>Turn-based: press a direction to move</p>",
        unsafe_allow_html=True,
    )

    init_state()
    s = st.session_state

    if s.screen == "menu":
        st.subheader("Ready to play?")
        if st.button("Start Game"):
            s.screen = "play"
            s.snake = [(COLS // 2, ROWS // 2)]
            s.direction = (1, 0)
            s.grow_pending = 0
            s.food = random_food(s.snake)
            s.score = 0
            s.game_over = False
            st.rerun()
        return

    if s.game_over:
        st.error(f"Game Over! Score: {s.score} | Best: {s.high_score}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play Again"):
                s.game_over = False
                s.snake = [(COLS // 2, ROWS // 2)]
                s.direction = (1, 0)
                s.grow_pending = 0
                s.food = random_food(s.snake)
                s.score = 0
                st.rerun()
        with col2:
            if st.button("Back to Menu"):
                s.screen = "menu"
                st.rerun()
        return

    # Playing
    st.caption(f"Score: {s.score} | Best: {s.high_score}")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        img = render_board()
        st.image(img, use_container_width=True)

    st.markdown("---")
    st.markdown("**Direction** (click to move)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅️ Left"):
            if s.direction != (1, 0):
                s.direction = (-1, 0)
                move_snake()
                st.rerun()
    with col2:
        if st.button("⬆️ Up"):
            if s.direction != (0, 1):
                s.direction = (0, -1)
                move_snake()
                st.rerun()
    with col3:
        if st.button("⬇️ Down"):
            if s.direction != (0, -1):
                s.direction = (0, 1)
                move_snake()
                st.rerun()
    with col4:
        if st.button("➡️ Right"):
            if s.direction != (-1, 0):
                s.direction = (1, 0)
                move_snake()
                st.rerun()
    if st.button("🏠 Back to Menu"):
        s.screen = "menu"
        st.rerun()


if __name__ == "__main__":
    main()
