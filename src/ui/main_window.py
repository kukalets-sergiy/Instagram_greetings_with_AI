from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtCore import Qt

from src.algorithms.test_open_driver import open_driver


class MainWindow(QWidget):
    """Base class for main window in selenium projects"""

    def __init__(self, window_title: str = 'Base Window'):
        super().__init__()
        self.default_test_launch_button = None
        self.initUI(window_title)

    def initUI(self, window_title: str):
        """
        Initializes the main window with a given title and size.
        """
        self.setWindowTitle(window_title)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint |
                            Qt.WindowType.WindowMinimizeButtonHint)

        self.default_test_launch_button = QPushButton('Test Launch', self)
        self.default_test_launch_button.move(100, 100)
        self.default_test_launch_button.clicked.connect(open_driver)