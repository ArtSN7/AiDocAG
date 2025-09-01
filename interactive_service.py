# interactive_orchestrator.py
import os
import sys
from analyzer_service import analyze_code_block

# путь где лежит наш файл со всеми папками ( ну с нашим IDM проектом )
# Теперь PROJECT_ROOT берётся из аргумента командной строки
if len(sys.argv) > 1:
    PROJECT_ROOT = sys.argv[1]
    if not os.path.isdir(PROJECT_ROOT):
        print(f"Ошибка: '{PROJECT_ROOT}' не является директорией.")
        sys.exit(1)
else:
    PROJECT_ROOT = "../../../../GITHUB/"  # Фоллбек на старый путь

print(f"Используемый PROJECT_ROOT: {os.path.abspath(PROJECT_ROOT)}")

MODEL_NAME_CODE = "gemma3:4b"
MODEL_NAME_SUM = "gemma3:4b"

# Директория для хранения контекстов
CONTEXT_ROOT = "contexts"
os.makedirs(CONTEXT_ROOT, exist_ok=True)


def get_all_files_in_dir(base_dirs):
    """Собирает пути ко всем файлам из списка директорий."""
    all_files = []
    for base_dir in base_dirs:
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


# --- Определение структуры модулей с подгруппами и моделями ---
modules = {
    "1": {
        "name": "mod_1_core",
        "subgroups": {
            "1.1": {"name": "JIMCore", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMCore/src/main/java/su/jet/jim")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_1_core/JIMCore"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_1_1_jimcore.txt"), "model": MODEL_NAME_CODE},
            "1.2": {"name": "JIMDB", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMDB/src/main/java/su/jet/jim/db")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_1_core/JIMDB"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_1_2_jimdb.txt"), "model": MODEL_NAME_CODE},
            "1.3": {"name": "JIMFunctionality", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMFunctionality/src/main/java/su/jet/jim")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_1_core/JIMFunctionality"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_1_3_jimfunc.txt"), "model": MODEL_NAME_CODE},
            "1.4": {"name": "JIMAPIDTO", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMAPIDTO/src/main/java/su/jet/jim/rest")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_1_core/JIMAPIDTO"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_1_4_apidto.txt"), "model": MODEL_NAME_CODE},
            "1.5": {"name": "JIMExtender", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMExtender/src/main/java/su/jet/jim/extender")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_1_core/JIMExtender"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_1_5_jimextender.txt"), "model": MODEL_NAME_CODE},
            "1.6": {"name": "DBSchema", "paths": [os.path.join(PROJECT_ROOT, "JetIdmJim/DBSchema/liquibase/sql"), os.path.join(PROJECT_ROOT, "jim/DBSchema")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_1_core/DBSchema"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_1_6_dbschema.txt"), "model": MODEL_NAME_CODE},
        },
        "group_context_file": os.path.join(CONTEXT_ROOT, "mod_1_core/context_mod_1_core_group.txt"),
        "model_for_group": MODEL_NAME_SUM
    },
    "2": {
        "name": "mod_2_connectors",
        "subgroups": {
            "2.1": {"name": "AD Connector", "paths": [os.path.join(PROJECT_ROOT, "jim/Connectors/AD/ActiveDirectoryConnector/src/main/java/su/jet/jim/ad")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_2_connectors/AD_Connector"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_2_connectors/context_2_1_ad.txt"), "model": MODEL_NAME_CODE},
            "2.2": {"name": "AD Customization", "paths": [os.path.join(PROJECT_ROOT, "JetIdmJim/Connectors/ADCustomization/ActiveDirectoryCustomization/src/main/java/su/jet/jim/ad/custom")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_2_connectors/AD_Customization"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_2_connectors/context_2_2_ad_custom.txt"), "model": MODEL_NAME_CODE},
            "2.3": {"name": "LDAP Connector", "paths": [os.path.join(PROJECT_ROOT, "jim/Connectors/Ldap/")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_2_connectors/LDAP_Connector"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_2_connectors/context_2_3_ldap.txt"), "model": MODEL_NAME_CODE},
            "2.4": {"name": "JIMConnector", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMConnector/")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_2_connectors/JIMConnector"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_2_connectors/context_2_4_jimconnector.txt"), "model": MODEL_NAME_CODE},
        },
        "group_context_file": os.path.join(CONTEXT_ROOT, "mod_2_connectors/context_mod_2_connectors_group.txt"),
        "model_for_group": MODEL_NAME_SUM
    },
    "3": {
        "name": "mod_3_bpmn_api",
        "subgroups": {
            "3.1": {"name": "Camunda BPMN Engine", "paths": [os.path.join(PROJECT_ROOT, "jim/BPMNEngine/Camunda/JIMCamundaProcess/src/main/java/su/jet/jim/camunda")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/Camunda_BPMN_Engine"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/context_3_1_camunda_bpmn.txt"), "model": MODEL_NAME_CODE},
            "3.2": {"name": "Camunda API Client", "paths": [os.path.join(PROJECT_ROOT, "jim/CamundaApi/openapi/src/main/java/org/camunda/community/rest/client")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/Camunda_API_Client"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/context_3_2_camunda_api.txt"), "model": MODEL_NAME_CODE},
            "3.3": {"name": "OpenAPI", "paths": [os.path.join(PROJECT_ROOT, "jim/CamundaApi/openapi")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/OpenAPI"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/context_3_3_openapi.txt"), "model": MODEL_NAME_CODE},
        },
        "group_context_file": os.path.join(CONTEXT_ROOT, "mod_3_bpmn_api/context_mod_3_bpmn_api_group.txt"),
        "model_for_group": MODEL_NAME_SUM
    },
    "4": {
        "name": "mod_4_ui",
        "subgroups": {
            "4.1": {"name": "UI Admin Panel", "paths": [os.path.join(PROJECT_ROOT, "jim/UI/admin/src/main/java/su/jet/idm/ui")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_4_ui/UI_Admin_Panel"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_4_ui/context_4_1_ui_admin.txt"), "model": MODEL_NAME_CODE},
        },
        "group_context_file": os.path.join(CONTEXT_ROOT, "mod_4_ui/context_mod_4_ui_group.txt"),
        "model_for_group": MODEL_NAME_SUM
    },
    "5": {
        "name": "mod_5_other",
        "subgroups": {
            "5.1": {"name": "JIMGeneral", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMGeneral/src/main/java/su/jet/jim/general")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_5_other/JIMGeneral"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_5_other/context_5_1_general.txt"), "model": MODEL_NAME_CODE},
            "5.2": {"name": "K8S", "paths": [os.path.join(PROJECT_ROOT, "K8S")], "context_dir": os.path.join(CONTEXT_ROOT, "mod_5_other/K8S"), "group_context_file": os.path.join(CONTEXT_ROOT, "mod_5_other/context_5_2_k8s.txt"), "model": MODEL_NAME_CODE},
        },
        "group_context_file": os.path.join(CONTEXT_ROOT, "mod_5_other/context_mod_5_other_group.txt"),
        "model_for_group": MODEL_NAME_SUM
    }
}


def load_previous_group_context(group_key):
    """Загружает объединенный контекст всех предыдущих групп."""
    context = ""
    for i in range(1, int(group_key)):
        group_context_file = modules[str(i)]["group_context_file"]
        if os.path.exists(group_context_file):
            with open(group_context_file, 'r', encoding='utf-8') as f:
                context += f.read() + "\n\n"
        else:
            print(f"Внимание: Не найден объединенный контекст для группы {modules[str(i)]['name']}.")
            return None
    return context


def main_menu():
    """Отображает меню и обрабатывает выбор пользователя."""
    print("\n--- Меню анализа проекта ---")
    print("Выберите действие:")
    for key, group in modules.items():
        status = " (ГОТОВ)" if os.path.exists(group["group_context_file"]) else ""
        print(f"  [{key}] Анализ группы: {group['name']}{status}")
    print("  [F] Сгенерировать финальную документацию")
    print("  [E] Выход")
    choice = input("Ваш выбор: ").upper()
    return choice


def run_group_analysis(group_key):
    """Анализирует все подгруппы и объединяет их контексты."""
    group = modules[group_key]
    print(f"\n--- Начинаю пошаговый анализ группы: {group['name']} ---")
    all_subgroup_context = ""

    for sub_key, sub_group in group["subgroups"].items():
        subgroup_context_dir = sub_group["context_dir"]
        os.makedirs(subgroup_context_dir, exist_ok=True)
        subgroup_context_file = sub_group["group_context_file"]  # Это файл обобщенного контекста подгруппы

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
            prompt_for_file = f"Проанализируй следующий код из файла {os.path.basename(file_path)} в подгруппе {sub_group['name']}. Сфокусируйся на функциональности и назначении этого файла."
            
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
            prompt_for_subgroup = f"Скомпонуй и обобщи следующие контексты отдельных файлов, чтобы создать связный КОНТЕКСТ для подгруппы {sub_group['name']}. Сфокусируйся на взаимодействии файлов и общей функциональности подгруппы."
            
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

    prompt_for_group = f"Скомпонуй и обобщи следующие контексты подгрупп для создания связного КОНТЕКСТА ГРУППЫ для модуля {group['name']}."
    
    group_context = analyze_code_block([], all_subgroup_context + previous_group_context, prompt_for_group, group['model_for_group'])

    if group_context:
        with open(group["group_context_file"], "w", encoding="utf-8") as f:
            f.write(group_context)
        print(f"Объединенный контекст для группы {group['name']} сохранен в {group['group_context_file']}.")
        return True
    
    else:
        print(f"Не удалось создать объединенный контекст для группы {group['name']}.")
        return False


def generate_final_documentation():
    """Собирает все контексты групп и генерирует финальный документ."""
    print("\n--- Запускаю финальную генерацию документации ---")
    final_context = ""

    for group_info in modules.values():
        context_path = group_info["group_context_file"]
        if os.path.exists(context_path):
            with open(context_path, "r", encoding="utf-8") as f:
                final_context += f.read() + "\n\n"
    
    if not final_context:
        print("Ошибка: Отсутствуют файлы контекста. Проанализируйте модули сначала.")
        return

    final_prompt = (
        "Используй следующий контекст, чтобы создать полную, связную и подробную документацию "
        "для проекта IDM. Объедини все контексты в единый документ.\n"
        "Собранный контекст:\n" + final_context
    )
    
    final_documentation = analyze_code_block([], "", final_prompt, MODEL_NAME_SUM)
    
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
        
        elif choice in modules:
            run_group_analysis(choice)
        
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")