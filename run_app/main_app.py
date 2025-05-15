import sys
import os
import threading

from PyQt6.QtWidgets import QApplication

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Flask and LLM
from Backend.app import app as flask_app
from llm.llm_local import ensure_ollama_ready

# GUI
from frontend.main import MainWindow

MODEL = "llama3.2"

def run_flask():
    flask_app.run(port=5000, debug=False, use_reloader=False)

def main():
    try:
        # Run LLM
        print(f"🔄 Initializing model '{MODEL}'...")
        ensure_ollama_ready(MODEL)
        print(f"✅ Model '{MODEL}' is ready.")

        # Run Backend
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Run Frontend
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec())

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()