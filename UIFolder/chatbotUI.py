import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QTextEdit, QTabWidget, QSplitter)
from PyQt6.QtCore import Qt
import google.generativeai as genai


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize Gemini API
        genai.configure(api_key="")  # API key will need to be set
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.chat = self.model.start_chat(history=[])
        
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
        self.setup_settings_tab()
        
        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

    def setup_input_tab(self):
        # Create layout for input tab
        layout = QVBoxLayout(self.input_tab)
        
        # Create a splitter to divide the tab into output (top) and input (bottom) areas
        splitter = QSplitter(Qt.Orientation.Vertical)
        
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
        
        # Set initial sizes for splitter (70% output, 30% input)
        splitter.setSizes([400, 200])
        
        # Add splitter to main layout
        layout.addWidget(splitter)

    def setup_settings_tab(self):
        # Create layout for the settings tab
        layout = QVBoxLayout(self.settings_tab)
        # This is left empty as in the original

    def get_ai_response(self, prompt):
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            print(f"Error getting response from Gemini: {e}")
            return "Sorry, I encountered an error processing your request."

    def process_input(self):
        # Get input text
        input_text = self.input_text.toPlainText().strip()
        if input_text:
            # Display input in the output area
            self.output_text.append(f"You: {input_text}")
            
            # Get AI response
            ai_response = self.get_ai_response(input_text)
            
            # Display AI response
            self.output_text.append(f"AI: {ai_response}")
            
            # Clear the input field after sending
            self.input_text.clear()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()