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
    MAX_FILE_SIZE_KB = 2048  # Увеличил до 2MB, чтобы реже пропускать файлы

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
        return None  # Возвращаем None вместо строки, чтобы избежать пустого контекста
    
    full_prompt = (
        f"{prompt_instruction}\n\n"
        f"Учти следующий предыдущий контекст: {previous_context}\n\n"
        f"Код для анализа предоставлен ниже. Проанализируй его полностью:\n{file_contents}"
    )  # Явно указываем, что код предоставлен, чтобы избежать недоразумений с моделью

    print(f"Длина полного промпта: {len(full_prompt)} символов")  # Для дебага

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