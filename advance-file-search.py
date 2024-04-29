
"""
Main module of this app.
"""
from lib import QApplication
from lib import QMainWindow
from lib import load_css
from lib import FMain
from lib import CSS_COLORS_FILE_PATH
from lib import CSS_FILE_PATH


class WMain(QMainWindow):
    """
    Main Window of the app.
    """
    theme = load_css(CSS_FILE_PATH, CSS_COLORS_FILE_PATH)

    def __init__(self) -> None:
        super().__init__()
        self.setup_window()
        self.init_widgets()
    
    def init_widgets(self) -> None:
        """
        Initializes the main frame and other
        widgets.
        """
        self.fmain = FMain()
        self.setCentralWidget(self.fmain)
    
    def setup_window(self) -> None:
        """
        Setup window configuration
        """

        self.setGeometry(600, 400, 1300, 700)
        self.setMinimumSize(1300, 700)
        self.setWindowTitle("ADS")
        self.setStyleSheet(self.theme)

def run_app() -> None:
    """
    Create an qt application and instance
    of the main window to show the GUI.
    """
    app = QApplication([])
    window = WMain()
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_app()