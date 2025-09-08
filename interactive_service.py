# interactive_service.py
import os
import sys
from analyzer_service import analyze_code_block
from config import PROJECT_ROOT_FALLBACK, CONTEXT_ROOT, FINAL_PROMPT, FILE_PROMPT, DIR_PROMPT, TEMPERATURE, NUM_PREDICT, MODEL_NAME_CODE, MODEL_NAME_SUM, SUPPORTED_EXTENSIONS, MODULES, EXT


if len(sys.argv) > 1:
    PROJECT_ROOT = sys.argv[1]
    if not os.path.isdir(PROJECT_ROOT):
        print(f"Ошибка: '{PROJECT_ROOT}' не является директорией.")
        sys.exit(1)
else:
    PROJECT_ROOT = PROJECT_ROOT_FALLBACK


print(f"Используемый PROJECT_ROOT: {os.path.abspath(PROJECT_ROOT)}")
os.makedirs(CONTEXT_ROOT, exist_ok=True)


def get_all_files_in_dir(base_dir, extensions=SUPPORTED_EXTENSIONS):
    """
    Рекурсивно находит все файлы с указанными расширениями в директории.
    """
    all_files = []
    if os.path.exists(base_dir):
        for dirpath, _, filenames in os.walk(base_dir):
            for f in filenames:
                if any(f.lower().endswith(ext) for ext in extensions):
                    full_path = os.path.join(dirpath, f)
                    all_files.append(full_path)
    else:
        print(f"Директория не найдена: {base_dir}")
    if not all_files:
        print("Внимание: Не найдено ни одного подходящего файла в директории!")
    return all_files


def build_context_tree(root_dir=PROJECT_ROOT, context_root=CONTEXT_ROOT):
    """
    Рекурсивно строит дерево контекстов: сначала анализирует файлы в листовых директориях,
    затем агрегирует контексты поддиректорий вверх по дереву.
    Возвращает путь к финальному контексту корневой директории.
    """
    relative_root = os.path.relpath(root_dir, PROJECT_ROOT)
    context_dir = os.path.join(context_root, relative_root) if relative_root != '.' else context_root
    os.makedirs(context_dir, exist_ok=True)
    context_file = os.path.join(context_dir, "dir_context." + EXT)

    if os.path.exists(context_file):
        print(f"Контекст для директории {root_dir} уже существует: {context_file}. Использую его.")
        return context_file

    print(f"\n--- Анализирую директорию: {root_dir} ---")

    # Шаг 1: Собрать все поддиректории и файлы, исключая директорию контекстов
    subdirs = []
    files = []
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path) and entry != os.path.basename(CONTEXT_ROOT):
            subdirs.append(full_path)
        elif any(entry.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            files.append(full_path)

    # Шаг 2: Рекурсивно обработать поддиректории и собрать их контексты
    subdir_contexts = ""
    for subdir in subdirs:
        sub_context_file = build_context_tree(subdir, context_root)
        if sub_context_file and os.path.exists(sub_context_file):
            with open(sub_context_file, 'r', encoding='utf-8') as f:
                subdir_contexts += f"\n--- Контекст поддиректории {os.path.basename(subdir)} ---\n{f.read()}\n\n"
        else:
            print(f"Внимание: Не удалось получить контекст для поддиректории {subdir}.")

    # Шаг 3: Анализировать файлы в текущей директории
    file_contexts = ""
    if files:
        print(f"  - Найдено {len(files)} файлов для анализа в {root_dir}.")
        for file_path in files:
            relative_path = os.path.relpath(file_path, PROJECT_ROOT)
            context_file_name = os.path.basename(file_path).replace('.', '_') + '_context.' + EXT
            context_file_path = os.path.join(context_dir, context_file_name)

            if os.path.exists(context_file_path):
                print(f"    - Контекст для файла {os.path.basename(file_path)} уже существует. Использую его.")
                with open(context_file_path, 'r', encoding='utf-8') as f:
                    file_contexts += f.read() + "\n\n"
                continue

            print(f"    - Анализирую файл: {file_path}")
            prompt_for_file = f"{FILE_PROMPT} {os.path.basename(file_path)} в директории {os.path.basename(root_dir)}."

            file_context = analyze_code_block([file_path], "", prompt_for_file, MODEL_NAME_CODE)

            if file_context:
                with open(context_file_path, "w", encoding="utf-8") as f:
                    f.write(file_context)
                file_contexts += file_context + "\n\n"
                print(f"    - Контекст для {os.path.basename(file_path)} сохранен в {context_file_path}.")
            else:
                print(f"    - Анализ файла {file_path} не удался.")

    # Шаг 4: Агрегировать контексты файлов и поддиректорий в контекст текущей директории
    all_context = file_contexts + subdir_contexts
    if all_context:
        print(f"  - Агрегирую контексты для директории {root_dir}...")
        prompt_for_dir = f"{DIR_PROMPT} {os.path.basename(root_dir)}."

        dir_context = analyze_code_block([], all_context, prompt_for_dir, MODEL_NAME_SUM)

        if dir_context:
            with open(context_file, "w", encoding="utf-8") as f:
                f.write(dir_context)
            print(f"  - Контекст для директории {root_dir} сохранен в {context_file}.")
            return context_file
        else:
            print(f"  - Не удалось агрегировать контекст для директории {root_dir}.")
            return None
    else:
        print(f"  - Нет контекстов для агрегации в директории {root_dir}.")
        return None


def generate_final_documentation():
    print("\n--- Запускаю финальную генерацию документации ---")
    
    # Собираем все групповые контексты модулей вместо корневого контекста
    all_context = ""
    for module_key, module in MODULES.items():
        group_context_file = os.path.join(CONTEXT_ROOT, module["group_context_file"])
        if os.path.exists(group_context_file):
            with open(group_context_file, 'r', encoding='utf-8') as f:
                all_context += f"\n--- Контекст модуля {module['name']} ---\n{f.read()}\n\n"
        else:
            print(f"Внимание: Контекст для модуля {module['name']} не найден: {group_context_file}")

    if not all_context:
        print("Ошибка: Нет доступных контекстов модулей для генерации документации.")
        return

    final_prompt = FINAL_PROMPT + all_context

    final_documentation = analyze_code_block([], "", final_prompt, MODEL_NAME_SUM)

    if final_documentation:
        final_doc_path = os.path.join(CONTEXT_ROOT, "final_documentation." + EXT)
        with open(final_doc_path, "w", encoding="utf-8") as f:
            f.write(final_documentation)
        print(f"\n--- Итоговая документация сохранена в {final_doc_path} ---")
    else:
        print("Не удалось сгенерировать финальную документацию.")


def run_specific_dir_analysis(specific_path):
    """Анализирует указанную директорию рекурсивно."""
    full_path = os.path.join(PROJECT_ROOT, specific_path)
    if not os.path.isdir(full_path):
        print(f"Ошибка: '{specific_path}' не является директорией в PROJECT_ROOT.")
        return
    build_context_tree(root_dir=full_path)


def run_module_analysis(module_key):
    """Анализирует модуль по предопределенной структуре из config.MODULES."""
    if module_key not in MODULES:
        print(f"Ошибка: Модуль '{module_key}' не найден в конфигурации.")
        return

    module = MODULES[module_key]
    print(f"\n--- Анализирую модуль: {module['name']} ---")

    all_subgroup_context = ""
    for sub_key, sub_group in module["subgroups"].items():
        # Берем все пути подгруппы и анализируем каждый
        for path in sub_group["paths"]:
            sub_dir = os.path.join(PROJECT_ROOT, path)
            if os.path.exists(sub_dir):
                print(f"  - Анализирую подгруппу: {sub_group['name']} в {sub_dir}")
                sub_context_file = build_context_tree(root_dir=sub_dir)
                if sub_context_file:
                    with open(sub_context_file, 'r', encoding='utf-8') as f:
                        all_subgroup_context += f"\n--- Контекст подгруппы {sub_group['name']} (путь: {path}) ---\n{f.read()}\n\n"
            else:
                print(f"Внимание: Путь не существует: {sub_dir}")

    # Агрегировать для группы модуля
    group_context_file = os.path.join(CONTEXT_ROOT, module["group_context_file"])
    if all_subgroup_context:
        prompt_for_group = f"{DIR_PROMPT} для модуля {module['name']}."
        group_context = analyze_code_block([], all_subgroup_context, prompt_for_group, module['model_for_group'])
        if group_context:
            with open(group_context_file, "w", encoding="utf-8") as f:
                f.write(group_context)
            print(f"Контекст для модуля {module['name']} сохранен в {group_context_file}.")


def main_menu():
    """Отображает меню и обрабатывает выбор пользователя."""
    print("\n--- Меню анализа проекта ---")
    print("Выберите действие:")
    print("  [A] Проанализировать весь проект (имитация прогона по всем модулям автоматически)")
    print("  [S] Проанализировать конкретную директорию (введите относительный путь, напр. jim/JIM/JIMCore/src/main/java/su/jet/jim)")
    for key, mod in MODULES.items():
        status = " (ГОТОВ)" if os.path.exists(os.path.join(CONTEXT_ROOT, mod["group_context_file"])) else ""
        print(f"  [{key}] Проанализировать модуль: {mod['name']}{status}")
    print("  [F] Сгенерировать финальную документацию")
    print("  [E] Выход")
    choice = input("Ваш выбор: ").upper()
    return choice


if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == "E":
            print("Выход.")
            sys.exit(0)

        elif choice == "F":
            generate_final_documentation()

        elif choice == "A":
            print("\n--- Имитация полного анализа: прогон по всем модулям автоматически ---")
            for module_key in MODULES:
                run_module_analysis(module_key)

        elif choice == "S":
            specific_path = input("Введите относительный путь к директории: ").strip()
            run_specific_dir_analysis(specific_path)

        elif choice in MODULES:
            run_module_analysis(choice)

        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")