# Below is code which allows text to display as it streams from llm output

from PyQt6.QtCore import QThread, pyqtSignal # Allows LLM output stream to run in a separate thread
import requests
import json

class LLMStreamWorker(QThread):
    token_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, prompt: str, model: str = "llama3.2"):
        super().__init__()
        self.prompt = prompt
        self.model = model

    def run(self):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": self.prompt,
            "stream": True
        }

        try:
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            self.token_received.emit(token)
                    except json.JSONDecodeError:
                        self.token_received.emit("\n[Error parsing stream chunk]")
        except Exception as e:
            self.token_received.emit(f"\n❌ Error: {str(e)}")
        finally:
            self.finished.emit()
