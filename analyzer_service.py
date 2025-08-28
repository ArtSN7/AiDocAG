# analyzer_service.py
import requests
import os

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def analyze_code_block(file_paths, previous_context, prompt_instruction, model_name):
    """
    Отправляет код на анализ в Ollama с указанной моделью и инструкциями.

    Args:
        file_paths (list): Список путей к файлам для анализа.
        previous_context (str): Текст предыдущего контекста.
        prompt_instruction (str): Инструкция для LLM.
        model_name (str): Имя модели Ollama (например, 'deepseek-coder').

    Returns:
        str: Сгенерированный LLM контекст или None в случае ошибки.
    """

    print(f"Использую модель: {model_name}")
    print("Собираю содержимое файлов...")
    
    file_contents = ""
    MAX_FILE_SIZE_KB = 1024 

    for path in file_paths:
        try:
            if os.path.exists(path) and os.path.getsize(path) < MAX_FILE_SIZE_KB * 1024:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_contents += f"\n--- Файл: {path} ---\n{f.read()}\n"
            else:
                print(f"Пропускаю файл (не найден или слишком большой): {path}")
        except Exception as e:
            print(f"Ошибка при чтении файла {path}: {e}")
            continue

    if not file_contents and not previous_context:
        return "Не удалось найти или прочитать файлы для анализа."
    
    full_prompt = (
        f"{prompt_instruction}\n\n"
        f"Учти следующий предыдущий контекст: {previous_context}\n\n"
        f"Код для анализа:\n{file_contents}"
    )

    data = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 4096,
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        result = response.json()
        return result['response']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при вызове Ollama API: {e}")
        return None