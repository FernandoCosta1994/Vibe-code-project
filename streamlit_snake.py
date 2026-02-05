"""
Snake Game — Forest Edition (Streamlit)
The embedded game doesn't work in Streamlit's iframe, so we offer a downloadable HTML file.
"""
import streamlit as st

# Difficulty: speed multiplier (higher = faster)
DIFFICULTIES = {"Easy": 0.8, "Normal": 1.0, "Hard": 1.3}


def get_game_html(speed_mult: float) -> str:
    """Generate full HTML5 Snake game with forest theme and keyboard controls."""
    tick_ms = int(150 / speed_mult)
    with open("snake_game.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html.replace("const TICK_MS=150;", f"const TICK_MS={tick_ms};")


def main():
    st.set_page_config(page_title="Snake — Forest", page_icon="🐍", layout="centered")
    st.markdown(
        "<h1 style='text-align:center;color:#c3e68c'>🐍 Snake — Forest Edition</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#6b8a6b'>Choose difficulty, then download and open the game in your browser</p>",
        unsafe_allow_html=True,
    )

    st.subheader("Choose difficulty")
    diff = st.radio(
        "Difficulty",
        list(DIFFICULTIES.keys()),
        index=1,
        horizontal=True,
        label_visibility="collapsed",
    )
    speed_mult = DIFFICULTIES[diff]

    html = get_game_html(speed_mult)
    st.download_button(
        label="📥 Download snake_game.html",
        data=html,
        file_name="snake_game.html",
        mime="text/html",
        type="primary",
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown("**How to play:**")
    st.markdown("1. Click the button above to download `snake_game.html`")
    st.markdown("2. Open the file in your browser (double-click or drag into Chrome/Edge)")
    st.markdown("3. Click the game area to focus, then use **↑↓←→** or **W A S D** to move")
    st.markdown("4. Eat the red apples, avoid hitting yourself!")

    st.markdown("---")
    st.caption("The embedded version doesn't render correctly in Streamlit. Use the download for the best experience.")


if __name__ == "__main__":
    main()
