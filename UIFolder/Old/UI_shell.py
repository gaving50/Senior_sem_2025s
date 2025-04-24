#yet to be connected to mongo

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QTextEdit, QTabWidget)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Sets window properties
        self.setWindowTitle("ProjectUIShell")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Create and add input tab
        self.input_tab = QWidget()
        self.tab_widget.addTab(self.input_tab, "Input")
        
        # Create and add performance tab
        self.performance_tab = QWidget()
        self.tab_widget.addTab(self.performance_tab, "Performance")

        # Create and add settings tab
        self.settings_tab = QWidget()
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        # Sets up tabs
        self.setup_input_tab()
        self.setup_performance_tab()
        self.setup_settings_tab()
    
    def setup_input_tab(self):
        # Create layout for input tab
        layout = QVBoxLayout(self.input_tab)
        
        # Creates text input
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter your text here...")
        
        # Create send button
        self.send_button = QPushButton("Send")
        # Button doesn't do anything
        
        # Add widgets to layout
        layout.addWidget(self.input_text)
        layout.addWidget(self.send_button)
    
    def setup_performance_tab(self):
        # Create layout for performance tab
        layout = QVBoxLayout(self.performance_tab)
        
        # Create the performance output - just a placeholder
        self.performance_output = QTextEdit()
        self.performance_output.setReadOnly(True)
        self.performance_output.setPlaceholderText("Performance data will go here")
        
        # Adds widgets to layout
        layout.addWidget(self.performance_output)
    
    def setup_settings_tab(self):
        # Create layout for the settings tab
        layout = QVBoxLayout(self.settings_tab)
        
        # Add a placeholder text
        settings_info = QTextEdit()
        settings_info.setReadOnly(True)
        settings_info.setPlaceholderText("Settings options will go here")
        
        layout.addWidget(settings_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())