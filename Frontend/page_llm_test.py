import sys
import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.llm_api import generate_with_ollama

class LLMTestPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter a prompt for the model...")

        self.send_button = QPushButton("Send to LLM")
        self.send_button.clicked.connect(self.query_llm)

        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)

        layout.addWidget(self.prompt_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.response_output)

    def query_llm(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.response_output.setText("⚠️ Please enter a prompt.")
            return

        try:
            response = generate_with_ollama(prompt)
            self.response_output.setText(response)
        except Exception as e:
            self.response_output.setText(f"❌ Error: {e}")
