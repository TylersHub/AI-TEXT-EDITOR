import sys
import os
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.llm_worker import LLMStreamWorker

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

        self.response_output.clear()
        self.send_button.setEnabled(False)

        self.worker = LLMStreamWorker(prompt=prompt)
        self.worker.token_received.connect(self.append_token)
        self.worker.finished.connect(self.stream_finished)
        self.worker.start()

    def append_token(self, token: str):
        self.response_output.moveCursor(QTextCursor.MoveOperation.End)
        self.response_output.insertPlainText(token)
        self.response_output.ensureCursorVisible()

    def stream_finished(self):
        self.send_button.setEnabled(True)
