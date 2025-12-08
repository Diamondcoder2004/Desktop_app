# src/utils/ai_helper.py
import requests
import json
from typing import List, Dict

def query_ollama(prompt: str, model: str = "llama3.2", timeout: int = 60) -> str:
    """
    Отправляет запрос к локальному Ollama и возвращает ответ.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Ответ от модели пуст.")
        else:
            return f"Ошибка Ollama: {response.status_code} – {response.text}"
    except Exception as e:
        return f"Не удалось подключиться к Ollama: {str(e)}\n\nУбедитесь, что Ollama запущен: `ollama serve`"