from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt

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

def apply_theme(dark_theme_enabled, canvas=None, axes=None):
    app = QApplication.instance()
    
    # Applies palette based on theme setting for Qt components
    if dark_theme_enabled:
        # Use custom DarkPalette
        app.setPalette(DarkPalette())
    else:
        # Light theme, which is the default
        app.setPalette(app.style().standardPalette())
    
    # Set consistent formatting for both modes
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
    
    if axes is not None:
        apply_matplotlib_theme(dark_theme_enabled, axes, canvas)

def apply_matplotlib_theme(dark_theme_enabled, axes, canvas=None):
    if dark_theme_enabled:
        # Dark theme for matplotlib
        plt.style.use('dark_background')
        label_color = 'white'
        spine_color = 'white'
        tick_color = 'white'
        bg_color = '#353535'  # Match QPalette.Window color
    else:
        # Light theme for matplotlib
        plt.style.use('default')
        label_color = 'black'
        spine_color = 'black'
        tick_color = 'black'
        bg_color = 'white'
    
    # Set figure background color
    if canvas:
        canvas.figure.patch.set_facecolor(bg_color)
    
    # Apply to all axes
    for ax in axes:
        # Set axis background color
        ax.set_facecolor(bg_color)
        
        ax.tick_params(colors=tick_color)
        
        # Update spine colors
        for spine in ax.spines.values():
            spine.set_color(spine_color)
        
        # Update axis labels
        ax.xaxis.label.set_color(label_color)
        ax.yaxis.label.set_color(label_color)
        
        # Update tick labels
        for text in ax.get_xticklabels() + ax.get_yticklabels():
            text.set_color(label_color)
    
    # Update canvas
    if canvas:
        canvas.draw()