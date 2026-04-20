"""Main application entry point."""
import sys
from PyQt6.QtWidgets import QApplication

from .gui.main_window import MainWindow
from .core.constants import PlayerColor


def main() -> None:
    """Run the Othello application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Create main window
    window = MainWindow()

    # Set default player configuration (Human vs AI - Medium)
    window.game_controller.menu_widget.set_player_config("Human", "AI - Medium")
    window.game_controller._update_players_from_menu()

    # Show window
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
