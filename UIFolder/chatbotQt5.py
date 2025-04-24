import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QTextEdit, QTabWidget, QSplitter,
                            QLabel, QLineEdit, QMessageBox, QHBoxLayout,
                            QCheckBox)
from PyQt5.QtCore import Qt, QTimer
import matplotlib
# Embeds graph in UI
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Import external modules
from performance.display import display_resource_usage
from performance.get_stuff_and_things import get_resource_usage
from performance.update import do_update, cpu_usage_data, memory_usage_data, disk_usage_data, time_data
from theme import apply_theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Dark theme flag
        self.dark_theme_enabled = False
        
        # Set window properties
        self.setWindowTitle("Chatbot UI")
        self.setGeometry(100, 100, 800, 600)
        
        # Create the main tab widget
        self.tab_widget = QTabWidget()
        
        # Create and add input tab
        self.input_tab = QWidget()
        self.tab_widget.addTab(self.input_tab, "Input")
        
        # Create and add performance tab
        self.performance_tab = QWidget()
        self.tab_widget.addTab(self.performance_tab, "Performance")
        
        # Create and add settings tab
        self.settings_tab = QWidget()
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        # Setup tabs
        self.setup_input_tab()
        self.setup_performance_tab()
        self.setup_settings_tab()
        
        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)
        
        # Connect tab change signal to toggle performance monitoring
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Start on the input tab
        self.tab_widget.setCurrentIndex(0)  

    def setup_input_tab(self):
        # Create layout for input tab
        layout = QVBoxLayout(self.input_tab)
        
        # Create splitter to divide the tab into output (top) and input (bottom) areas
        splitter = QSplitter(Qt.Vertical)
        
        # Create the output area (top)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Output will appear here...")
        splitter.addWidget(self.output_text)
        
        # Create container for input area (bottom)
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        
        # Create the text input
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter your text here...")
        self.input_text.setMaximumHeight(100)  # Limit height of input area
        
        # Create send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.process_input)
        
        # Add widgets to input layout
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.send_button)
        
        # Add input container to splitter
        splitter.addWidget(input_container)
        
        # Set initial sizes for splitter
        splitter.setSizes([400, 200])
        
        # Add splitter to main layout
        layout.addWidget(splitter)

    def setup_performance_tab(self):
        # Create layout for the performance tab
        layout = QVBoxLayout(self.performance_tab)
        
        # Create the matplotlib figure for plotting
        plt.ioff()  # Prevents seperate window
        self.figure, self.ax = plt.subplots(3, 1, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Control widget for the performance monitoring
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        
        # Mmonitoring label
        monitor_label = QLabel("Resource Monitoring:")
        control_layout.addWidget(monitor_label)
        
        # Create the monitoring toggle checkbox
        self.monitoring_toggle = QCheckBox()
        self.monitoring_toggle.setChecked(False)
        self.monitoring_toggle.stateChanged.connect(self.toggle_monitoring)
        control_layout.addWidget(self.monitoring_toggle)
        
        # Pushes controls to the left
        control_layout.addStretch()
        
        # Add the control widget to the main layout
        layout.addWidget(control_widget)
        
        # Initialize the plot with tight layout
        self.figure.tight_layout()

    def setup_settings_tab(self):
        # Create layout for the settings tab
        layout = QVBoxLayout(self.settings_tab)
        
        # Create theme section
        theme_widget = QWidget()
        theme_layout = QHBoxLayout(theme_widget)
        
        # Add dark theme toggle
        theme_label = QLabel("Dark Theme:")
        theme_layout.addWidget(theme_label)
        
        self.dark_theme_toggle = QCheckBox()
        self.dark_theme_toggle.setChecked(self.dark_theme_enabled)
        self.dark_theme_toggle.stateChanged.connect(self.toggle_theme)
        theme_layout.addWidget(self.dark_theme_toggle)
        
        # Add theme spacer
        theme_layout.addStretch()
        
        # Add to main layout
        layout.addWidget(theme_widget)
        
        # Add vertical spacing
        layout.addStretch()

    def toggle_monitoring(self, state):
        # Use the do_update function from update.py to toggle monitoring
        do_update(bool(state), self.ax, self.canvas)
    
        # Ensure the canvas is updated and events are processed
        if hasattr(self, 'canvas'):
            self.canvas.draw()
            self.canvas.flush_events()

    def on_tab_changed(self, index):
        # When leaving the performance tab, stop monitoring
        if index != 1 and hasattr(self, 'monitoring_toggle') and self.monitoring_toggle.isChecked():
            self.monitoring_toggle.setChecked(False)

    def process_input(self):
        # Get input text
        input_text = self.input_text.toPlainText().strip()
        if input_text:
            # Display input in the output area
            self.output_text.append(f"You: {input_text}")
            
            # Placeholder for AI response
            self.output_text.append("Jarvis: Sorry, AI integration is currently unavailable.")
            
            # Clear input field after sending
            self.input_text.clear()

    def toggle_theme(self, state):
        self.dark_theme_enabled = bool(state)
        # Use the external theme module
        apply_theme(self.dark_theme_enabled, self.canvas if hasattr(self, 'canvas') else None)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  

if __name__ == "__main__":
    main()