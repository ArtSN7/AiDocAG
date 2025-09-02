# analyzer_service.py
import requests
import os
from config import OLLAMA_API_URL, MAX_FILE_SIZE_KB, TEMPERATURE, NUM_PREDICT


def analyze_code_block(file_paths, previous_context, prompt_instruction, model_name):
    print(f"Использую модель: {model_name}")
    print("Собираю содержимое файлов...")
    
    file_contents = ""
    
    for path in file_paths:
        try:
            if os.path.exists(path):
                file_size_kb = os.path.getsize(path) / 1024
                print(f"Файл {path}: размер {file_size_kb:.2f} KB")
                if file_size_kb < MAX_FILE_SIZE_KB:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        file_contents += f"\n--- Файл: {path} ---\n{content}\n"
                        print(f"  - Успешно прочитан: {path} (длина: {len(content)} символов)")
                else:
                    print(f"Пропускаю файл (слишком большой: {file_size_kb:.2f} KB > {MAX_FILE_SIZE_KB} KB): {path}")
            else:
                print(f"Пропускаю файл (не найден): {path}")
        except Exception as e:
            print(f"Ошибка при чтении файла {path}: {e}")
            continue

    if not file_contents and not previous_context:
        print("Ошибка: Не удалось найти или прочитать ни один файл для анализа.")
        return None
    
    full_prompt = (
        f"{prompt_instruction}\n\n"
        f"Учти следующий предыдущий контекст: {previous_context}\n\n"
        f"Код для анализа предоставлен ниже. Проанализируй его полностью:\n{file_contents}"
    )

    print(f"Длина полного промпта: {len(full_prompt)} символов")

    data = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": NUM_PREDICT,
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