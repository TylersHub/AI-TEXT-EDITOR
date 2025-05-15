## HungryText

A group project based on an LLM-powered text editor, for CCNY's Spring 2025 Software Engineering course.

Intended Instructions when the App is finished:
1. Double-click HungryText.exe to start.
2. The app will automatically:
   - Prompt user to download Ollama
   - Pull the model (e.g., llama3:8b)
   - Continue to the HungryText Application

No Python installation or command line required.



Pyinstaller Build/Packaging Command:

pyinstaller --onefile --windowed --paths=./ --name=HungryText run_app/main_app.py
