import requests
import json

def generate_with_ollama(prompt: str, model: str = "llama3:8b", stream: bool = True):
    """
    Sends a prompt to the local Ollama LLM and prints the response (streamed if enabled).

    Args:
        prompt (str): The input text to send to the LLM.
        model (str): The model name (e.g. "llama3:8b", "mistral:instruct", etc.)
        stream (bool): Whether to stream the response.

    Returns:
        str: The full generated response.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    try:
        response = requests.post(url, json=payload, stream=stream)
        response.raise_for_status()

        full_output = ""

        if stream:
            print("Streaming response:\n")
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            print(data["response"], end="", flush=True)
                            full_output += data["response"]
                    except json.JSONDecodeError:
                        print(f"\n[Error parsing line: {line}]")
        else:
            data = response.json()
            full_output = data.get("response", "")
            print(full_output)

        return full_output

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return ""