# interactive_service.py
import os
import sys
from analyzer_service import analyze_code_block
from config import PROJECT_ROOT_FALLBACK, CONTEXT_ROOT, MODULES, FINAL_PROMT, GROUP_PROMT, SUB_GROUP_PROMT, FILE_PROMT


if len(sys.argv) > 1:
    PROJECT_ROOT = sys.argv[1]
    if not os.path.isdir(PROJECT_ROOT):
        print(f"Ошибка: '{PROJECT_ROOT}' не является директорией.")
        sys.exit(1)
else:
    PROJECT_ROOT = PROJECT_ROOT_FALLBACK


print(f"Используемый PROJECT_ROOT: {os.path.abspath(PROJECT_ROOT)}")
os.makedirs(CONTEXT_ROOT, exist_ok=True)


def get_all_files_in_dir(base_dirs):
    
    all_files = []
    for base_dir in base_dirs:
        base_dir = os.path.join(PROJECT_ROOT, base_dir) if not os.path.isabs(base_dir) else base_dir
        if os.path.exists(base_dir):
            for dirpath, _, filenames in os.walk(base_dir):
                for f in filenames:
                    if f.endswith('.java') or f.endswith('.sql'):
                        full_path = os.path.join(dirpath, f)
                        all_files.append(full_path)
        else:
            print(f"Директория не найдена: {base_dir}")
    if not all_files:
        print("Внимание: Не найдено ни одного .java или .sql файла в указанных директориях!")
    return all_files


def load_previous_group_context(group_key):
    """Загружает объединенный контекст всех предыдущих групп."""
    context = ""
    for i in range(1, int(group_key)):
        group_context_file = os.path.join(CONTEXT_ROOT, MODULES[str(i)]["group_context_file"])
        if os.path.exists(group_context_file):
            with open(group_context_file, 'r', encoding='utf-8') as f:
                context += f.read() + "\n\n"
        else:
            print(f"Внимание: Не найден объединенный контекст для группы {MODULES[str(i)]['name']}.")
            return None
    return context


def main_menu():
    """Отображает меню и обрабатывает выбор пользователя."""
    print("\n--- Меню анализа проекта ---")
    print("Выберите действие:")
    for key, group in MODULES.items():
        status = " (ГОТОВ)" if os.path.exists(os.path.join(CONTEXT_ROOT, group["group_context_file"])) else ""
        print(f"  [{key}] Анализ группы: {group['name']}{status}")
    print("  [F] Сгенерировать финальную документацию")
    print("  [E] Выход")
    choice = input("Ваш выбор: ").upper()
    return choice


def run_group_analysis(group_key):
    """Анализирует все подгруппы и объединяет их контексты."""
    group = MODULES[group_key]
    print(f"\n--- Начинаю пошаговый анализ группы: {group['name']} ---")
    all_subgroup_context = ""

    for sub_key, sub_group in group["subgroups"].items():
        subgroup_context_dir = os.path.join(CONTEXT_ROOT, sub_group["context_dir"])
        os.makedirs(subgroup_context_dir, exist_ok=True)
        subgroup_context_file = os.path.join(CONTEXT_ROOT, sub_group["group_context_file"])

        if os.path.exists(subgroup_context_file):
            print(f"  - Контекст для подгруппы {sub_group['name']} уже существует. Использую его.")
            with open(subgroup_context_file, 'r', encoding='utf-8') as f:
                all_subgroup_context += f.read() + "\n\n"
            continue

        print(f"  - Анализирую подгруппу: {sub_group['name']}...")
        file_list = get_all_files_in_dir(sub_group["paths"])
        
        if not file_list:
            print(f"  - Нет файлов для анализа в подгруппе {sub_group['name']}. Прерываю.")
            return False
        
        current_subgroup_context = ""
        
        # Анализ каждого файла по отдельности с сохранением в отдельный файл
        for file_path in file_list:
            relative_path = os.path.relpath(file_path, PROJECT_ROOT)
            context_file_name = os.path.basename(file_path).replace('.java', '_context.txt').replace('.sql', '_context.txt')
            context_file_path = os.path.join(subgroup_context_dir, context_file_name)
            
            if os.path.exists(context_file_path):
                print(f"    - Контекст для файла {os.path.basename(file_path)} уже существует. Использую его.")
                with open(context_file_path, 'r', encoding='utf-8') as f:
                    current_subgroup_context += f.read() + "\n\n"
                continue
            
            print(f"    - Анализирую файл: {file_path}")
            prompt_for_file = f"{FILE_PROMT} {os.path.basename(file_path)} в подгруппе {sub_group['name']}."
            
            file_context = analyze_code_block([file_path], "", prompt_for_file, sub_group['model'])
            
            if file_context:
                with open(context_file_path, "w", encoding="utf-8") as f:
                    f.write(file_context)
                current_subgroup_context += file_context + "\n\n"
                print(f"    - Контекст для {os.path.basename(file_path)} сохранен в {context_file_path}.")
            else:
                print(f"    - Анализ файла {file_path} не удался.")
        
        # Обобщение контекстов файлов в контекст подгруппы
        if current_subgroup_context:
            prompt_for_subgroup = f"{SUB_GROUP_PROMT} {sub_group['name']}"
            
            final_subgroup_context = analyze_code_block([], current_subgroup_context, prompt_for_subgroup, sub_group['model'])
            
            if final_subgroup_context:
                with open(subgroup_context_file, "w", encoding="utf-8") as f:
                    f.write(final_subgroup_context)
                all_subgroup_context += final_subgroup_context + "\n\n"
                print(f"  - Обобщенный контекст для {sub_group['name']} сохранен в {subgroup_context_file}.")
            else:
                print(f"  - Не удалось обобщить контекст для подгруппы {sub_group['name']}.")
                return False
        else:
            print(f"  - Не удалось получить контекст ни по одному файлу в подгруппе {sub_group['name']}. Прерываю.")
            return False

    print(f"\n--- Объединяю контексты подгрупп для {group['name']} ---")
    previous_group_context = load_previous_group_context(group_key)

    if previous_group_context is None:
        print("Не удалось загрузить контекст предыдущих групп. Анализ прерван.")
        return False

    prompt_for_group = f"{GROUP_PROMT} {group['name']}."
    
    group_context = analyze_code_block([], all_subgroup_context + previous_group_context, prompt_for_group, group['model_for_group'])

    if group_context:
        with open(os.path.join(CONTEXT_ROOT, group["group_context_file"]), "w", encoding="utf-8") as f:
            f.write(group_context)
        print(f"Объединенный контекст для группы {group['name']} сохранен в {os.path.join(CONTEXT_ROOT, group['group_context_file'])}.")
        return True
    
    else:
        print(f"Не удалось создать объединенный контекст для группы {group['name']}.")
        return False


def generate_final_documentation():
    
    print("\n--- Запускаю финальную генерацию документации ---")
    final_context = ""

    for group_info in MODULES.values():
        context_path = os.path.join(CONTEXT_ROOT, group_info["group_context_file"])
        if os.path.exists(context_path):
            with open(context_path, "r", encoding="utf-8") as f:
                final_context += f.read() + "\n\n"
    
    if not final_context:
        print("Ошибка: Отсутствуют файлы контекста. Проанализируйте модули сначала.")
        return

    final_prompt = FINAL_PROMT + final_context
    
    final_documentation = analyze_code_block([], "", final_prompt, MODULES["1"]["model_for_group"])
    
    if final_documentation:
        final_doc_path = os.path.join(CONTEXT_ROOT, "final_documentation.txt")
        with open(final_doc_path, "w", encoding="utf-8") as f:
            f.write(final_documentation)
        print(f"\n--- Итоговая документация сохранена в {final_doc_path} ---")
    else:
        print("Не удалось сгенерировать финальную документацию.")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        
        if choice == "E":
            print("Выход.")
            sys.exit(0)
        
        elif choice == "F":
            generate_final_documentation()
        
        elif choice in MODULES:
            run_group_analysis(choice)
        
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")