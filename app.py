"""Application entry point."""

from ui import create_ui
from theme import get_css, get_theme


if __name__ == "__main__":
    demo = create_ui()
    print("Starting Laptop Health AI Predictor...")
    print("Glassmorphic UI and local ML model are ready.")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        theme=get_theme(),
        css=get_css(),
    )
