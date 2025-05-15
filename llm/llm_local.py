import subprocess, socket, time, os, sys, shutil

def _ollama_path():
    """
    Determine the path to the Ollama binary.
    Checks for a bundled binary inside /ollama/, or falls back to system path.
    """
    folder = os.path.join(
        os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__),
        "..", "ollama"
    )
    bundled = os.path.join(folder, "ollama.exe" if os.name == "nt" else "ollama")

    if os.path.exists(bundled):
        return bundled

    # Fallback to system-installed Ollama
    return shutil.which("ollama")

def ensure_ollama_ready(model="llama3:8b"):
    """
    Ensures the Ollama daemon is running and the specified model is pulled.
    - Starts Ollama if not already running.
    - Pulls the model if it's not already downloaded.
    """
    ollama = _ollama_path()

    if not ollama:
        print("❌ Ollama not found! Please install it from https://ollama.com/download")
        sys.exit(1)

    print("✔ Using Ollama at:", ollama)

    # Check if Ollama daemon is already running
    try:
        socket.create_connection(("127.0.0.1", 11434), timeout=1).close()
        print("✔ Ollama daemon is already running.")
    except OSError:
        print("⏳ Starting Ollama daemon...")
        subprocess.Popen([ollama, "serve"])
        time.sleep(3)

    # Pull the model if it's not already downloaded
    try:
        models = subprocess.check_output([ollama, "list"], stderr=subprocess.STDOUT).decode()
        print("📦 Available models:", models)
        if model not in models:
            print(f"⬇ Pulling model '{model}'...")
            subprocess.run([ollama, "pull", model])
        else:
            print(f"✔ Model '{model}' is already available.")
    except subprocess.CalledProcessError as e:
        print("❌ Error running Ollama:", e.output.decode())
        sys.exit(1)

# Debug log (optional)
if __name__ == "__main__":
    print("Using Ollama at:", _ollama_path())
    print("Exists:", os.path.exists(_ollama_path()))
