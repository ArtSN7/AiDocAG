# interactive_service.py
import os
import sys
from analyzer_service import analyze_code_block
from config import PROJECT_ROOT_FALLBACK, CONTEXT_ROOT, MODULES_CONTEXTS_ROOT, FILE_PROMPT, DIR_PROMPT, MODULE_PROMPT, MODEL_NAME_CODE, MODEL_NAME_SUM, SUPPORTED_EXTENSIONS, MODULES, EXT 


if len(sys.argv) > 1:
    PROJECT_ROOT = sys.argv[1]
    if not os.path.isdir(PROJECT_ROOT):
        print(f"Ошибка: '{PROJECT_ROOT}' не является директорией.")
        sys.exit(1)
else:
    PROJECT_ROOT = PROJECT_ROOT_FALLBACK


print(f"Используемый PROJECT_ROOT: {os.path.abspath(PROJECT_ROOT)}")
os.makedirs(CONTEXT_ROOT, exist_ok=True)
os.makedirs(MODULES_CONTEXTS_ROOT, exist_ok=True)


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


def analyze_files_in_dir(root_dir, context_root=CONTEXT_ROOT):
    """
    Анализирует все одиночные файлы в директории рекурсивно, создавая контексты только для файлов.
    """
    relative_root = os.path.relpath(root_dir, PROJECT_ROOT)
    context_dir = os.path.join(context_root, relative_root) if relative_root != '.' else context_root
    os.makedirs(context_dir, exist_ok=True)

    print(f"\n--- Анализирую файлы в директории: {root_dir} ---")

    files = get_all_files_in_dir(root_dir)

    if files:
        print(f"  - Найдено {len(files)} файлов для анализа в {root_dir}.")
        for file_path in files:
            relative_path = os.path.relpath(file_path, PROJECT_ROOT)
            context_file_name = os.path.basename(file_path).replace('.', '_') + '_context.' + EXT
            context_file_path = os.path.join(context_dir, context_file_name)

            if os.path.exists(context_file_path):
                print(f"    - Контекст для файла {os.path.basename(file_path)} уже существует. Использую его.")
                continue

            print(f"    - Анализирую файл: {file_path}")
            prompt_for_file = f"{FILE_PROMPT} {os.path.basename(file_path)} в директории {os.path.basename(root_dir)}."

            file_context = analyze_code_block([file_path], "", prompt_for_file, MODEL_NAME_CODE)

            if file_context:
                with open(context_file_path, "w", encoding="utf-8") as f:
                    f.write(file_context)
                print(f"    - Контекст для {os.path.basename(file_path)} сохранен в {context_file_path}.")
            else:
                print(f"    - Анализ файла {file_path} не удался.")
    else:
        print(f"  - Нет файлов для анализа в директории {root_dir}.")


def build_dir_summary_tree(context_dir, modules_contexts_root=MODULES_CONTEXTS_ROOT): 
    """
    Рекурсивно строит дерево саммари для директорий на основе существующих контекстов файлов в CONTEXT_ROOT.
    Возвращает путь к файлу саммари текущей директории.
    """
    relative_context = os.path.relpath(context_dir, CONTEXT_ROOT)
    summary_dir = os.path.join(modules_contexts_root, relative_context) if relative_context != '.' else modules_contexts_root
    os.makedirs(summary_dir, exist_ok=True)
    summary_file = os.path.join(summary_dir, "dir_summary." + EXT)

    if os.path.exists(summary_file):
        print(f"Саммари для директории {context_dir} уже существует: {summary_file}. Использую его.")
        return summary_file

    print(f"\n--- Создаю саммари для директории: {context_dir} ---")

    # Шаг 1: Собрать поддиректории и файлы контекстов (игнорируя другие файлы)
    subdirs = []
    file_contexts = ""

    for entry in os.listdir(context_dir):
        full_path = os.path.join(context_dir, entry)

        if os.path.isdir(full_path):
            subdirs.append(full_path)

        elif entry.endswith('_context.' + EXT):

            with open(full_path, 'r', encoding='utf-8') as f:
                file_contexts += f"\n--- Контекст файла {entry} ---\n{f.read()}\n\n"

    # Шаг 2: Рекурсивно обработать поддиректории и собрать их саммари
    subdir_summaries = ""

    for subdir in subdirs:
        sub_summary_file = build_dir_summary_tree(subdir, modules_contexts_root)

        if sub_summary_file and os.path.exists(sub_summary_file):

            with open(sub_summary_file, 'r', encoding='utf-8') as f:
                subdir_summaries += f"\n--- Саммари поддиректории {os.path.basename(subdir)} ---\n{f.read()}\n\n"

        else:
            print(f"Внимание: Не удалось получить саммари для поддиректории {subdir}.")

    # Шаг 3: Агрегировать контексты файлов и саммари поддиректорий
    all_context = file_contexts + subdir_summaries

    if all_context:

        print(f"  - Агрегирую контексты для директории {context_dir}...")
        prompt_for_dir = f"{DIR_PROMPT} для директории {os.path.basename(context_dir)}."

        dir_summary = analyze_code_block([], all_context, prompt_for_dir, MODEL_NAME_SUM)

        if dir_summary:

            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(dir_summary)

            print(f"  - Саммари для директории {context_dir} сохранено в {summary_file}.")

            return summary_file
        
        else:

            print(f"  - Не удалось создать саммари для директории {context_dir}.")
            return None
        
    else:
        print(f"  - Нет контекстов для агрегации в директории {context_dir}.")
        return None


def generate_module_summary(module_key):
    """Генерирует саммари для всего модуля на основе саммари подгрупп."""

    if module_key not in MODULES:
        print(f"Ошибка: Модуль '{module_key}' не найден в конфигурации.")
        return

    module = MODULES[module_key]

    print(f"\n--- Генерирую саммари для модуля: {module['name']} ---")

    all_subgroup_summaries = ""

    for sub_key, sub_group in module["subgroups"].items():
        for path in sub_group["paths"]:

            sub_context_dir = os.path.join(CONTEXT_ROOT, path)

            if os.path.exists(sub_context_dir):

                print(f"  - Обрабатываю подгруппу: {sub_group['name']} в {sub_context_dir}")

                # Строим дерево саммари для этой подгруппы
                sub_summary_file = build_dir_summary_tree(sub_context_dir)

                if sub_summary_file:

                    with open(sub_summary_file, 'r', encoding='utf-8') as f:
                        all_subgroup_summaries += f"\n--- Саммари подгруппы {sub_group['name']} (путь: {path}) ---\n{f.read()}\n\n"

            else:
                print(f"Внимание: Директория контекстов не существует: {sub_context_dir}")

    module_summary_dir = os.path.join(MODULES_CONTEXTS_ROOT, module['name'])
    os.makedirs(module_summary_dir, exist_ok=True)
    module_summary_file = os.path.join(module_summary_dir, "module_summary." + EXT)

    if all_subgroup_summaries:

        prompt_for_module = f"{MODULE_PROMPT} для модуля {module['name']}."

        module_summary = analyze_code_block([], all_subgroup_summaries, prompt_for_module, MODEL_NAME_SUM)

        if module_summary:

            with open(module_summary_file, "w", encoding="utf-8") as f:
                f.write(module_summary)

            print(f"Саммари для модуля {module['name']} сохранено в {module_summary_file}.")

    else:
        print(f"Нет саммари подгрупп для модуля {module['name']}.")


def run_module_analysis(module_key):
    """Анализирует модуль по предопределенной структуре из config.MODULES, обрабатывая только одиночные файлы в подгруппах."""

    if module_key not in MODULES:
        print(f"Ошибка: Модуль '{module_key}' не найден в конфигурации.")
        return

    module = MODULES[module_key]
    print(f"\n--- Анализирую модуль: {module['name']} ---")

    for sub_key, sub_group in module["subgroups"].items():

        for path in sub_group["paths"]:

            sub_dir = os.path.join(PROJECT_ROOT, path)

            if os.path.exists(sub_dir):

                print(f"  - Анализирую подгруппу: {sub_group['name']} в {sub_dir}")
                analyze_files_in_dir(root_dir=sub_dir)

            else:
                print(f"Внимание: Путь не существует: {sub_dir}")


def run_all_modules_analysis():
    """Имитирует полный анализ, прогоняя все модули из config.MODULES автоматически."""
    print("\n--- Имитация полного анализа: прогон по всем модулям автоматически ---")
    for module_key in MODULES:
        run_module_analysis(module_key)


def main_menu():

    print("\n--- Меню анализа проекта ---")
    print("Выберите действие:")
    print("  [A] Проанализировать все модули и сделать для них базовые контексты и саммари")
    print("  [G] Сгенерировать саммари для всех модулей ( нужно сделать анализ на базовом уровне сначала )")

    for key, mod in MODULES.items():
        print(f"  [{key}] Проанализировать модуль: {mod['name']} (файлы)")
        print(f"  [{key}G] Сгенерировать саммари для модуля: {mod['name']}")

    print("  [E] Выход")

    choice = input("Ваш выбор: ").upper()
    return choice


if __name__ == "__main__":

    while True:
        choice = main_menu()

        if choice == "E":
            print("Выход.")
            sys.exit(0)

        elif choice == "A":
            run_all_modules_analysis()

            print("\n--- Генерация саммари для всех модулей ---")
            for module_key in MODULES:
                generate_module_summary(module_key)

        elif choice.endswith("G") and choice[:-1] in MODULES: 
            generate_module_summary(choice[:-1])


        elif choice in MODULES:
            run_module_analysis(choice)

        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")