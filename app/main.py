import sys
from PyQt6.QtWidgets import QApplication
from demo import MainWindow
from llm.llm_local import ensure_ollama_ready

MODEL = "llama3"

def main():
    try:
        print(f"🔄 Initializing model '{MODEL}'...")
        ensure_ollama_ready(MODEL)
        print(f"✅ Model '{MODEL}' is ready.")

        app = QApplication(sys.argv)
        window = MainWindow()
        window.showMaximized()
        sys.exit(app.exec())

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
