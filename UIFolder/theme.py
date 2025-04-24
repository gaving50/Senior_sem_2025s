from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication

class DarkPalette(QPalette):
    def __init__(self):
        super().__init__()
        
        # Set color values for dark theme
        self.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setColor(QPalette.Base, QColor(25, 25, 25))
        self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        self.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        self.setColor(QPalette.Text, QColor(255, 255, 255))
        self.setColor(QPalette.Button, QColor(53, 53, 53))
        self.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setColor(QPalette.BrightText, QColor(255, 0, 0))
        self.setColor(QPalette.Link, QColor(42, 130, 218))
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        # Set disabled colors
        self.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        self.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        self.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        self.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        self.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))

def apply_theme(dark_theme_enabled, canvas=None):

    app = QApplication.instance()
    
    # Applies palette based on theme setting
    if dark_theme_enabled:
        # Use custom DarkPalette
        app.setPalette(DarkPalette())
    else:
        # Light theme (default)
        app.setPalette(app.style().standardPalette())
    
    # Sets consistent formatting for both modes
    app.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid;
        }
        QTabBar::tab {
            padding: 5px;
            margin: 2px;
        }
        QSplitter::handle {
            width: 1px;
            height: 1px;
        }
        QPushButton {
            padding: 5px;
            border-radius: 3px;
            border: 1px solid;
        }
        QLineEdit {
            padding: 3px;
            border-radius: 2px;
        }
    """)