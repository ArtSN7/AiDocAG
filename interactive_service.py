# interactive_orchestrator.py
import os
import sys
from analyzer_service import analyze_code_block

# путь где лежит наш файл со всеми папками ( ну с нашим IDM проектом - у меня это папка GITHUB )
PROJECT_ROOT = "./GITHUB/"

MODEL_NAME_CODE = "deepseek-r1:70b"
MODEL_NAME_SUM = "llama3.2:3b"


def get_all_files_in_dir(base_dirs):
    """Собирает пути ко всем файлам из списка директорий."""
    all_files = []
    for base_dir in base_dirs:
        if os.path.exists(base_dir):
            for dirpath, _, filenames in os.walk(base_dir):
                for f in filenames:
                    if f.endswith('.java') or f.endswith('.sql'):
                        all_files.append(os.path.join(dirpath, f))
    return all_files


# --- Определение структуры модулей с подгруппами и моделями ---
modules = {
    "1": {
        "name": "mod_1_core",
        "subgroups": {
            "1.1": {"name": "JIMCore", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMCore/src/main/java/su/jet/jim")], "context_file": "context_1_1_jimcore.txt", "model": MODEL_NAME_CODE},
            "1.2": {"name": "JIMDB", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMDB/src/main/java/su/jet/jim/db")], "context_file": "context_1_2_jimdb.txt", "model": MODEL_NAME_CODE},
            "1.3": {"name": "JIMFunctionality", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMFunctionality/src/main/java/su/jet/jim")], "context_file": "context_1_3_jimfunc.txt", "model": MODEL_NAME_CODE},
            "1.4": {"name": "JIMAPIDTO", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMAPIDTO/src/main/java/su/jet/jim/rest")], "context_file": "context_1_4_apidto.txt", "model": MODEL_NAME_CODE},
            "1.5": {"name": "JIMExtender", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMExtender/src/main/java/su/jet/jim/extender")], "context_file": "context_1_5_jimextender.txt", "model": MODEL_NAME_CODE},
            "1.6": {"name": "DBSchema", "paths": [os.path.join(PROJECT_ROOT, "JetIdmJim/DBSchema/liquibase/sql"), os.path.join(PROJECT_ROOT, "GITHUB/jim/DBSchema")], "context_file": "context_1_6_dbschema.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "context_mod_1_core_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "2": {
        "name": "mod_2_connectors",
        "subgroups": {
            "2.1": {"name": "AD Connector", "paths": [os.path.join(PROJECT_ROOT, "jim/Connectors/AD/ActiveDirectoryConnector/src/main/java/su/jet/jim/ad")], "context_file": "context_2_1_ad.txt", "model": MODEL_NAME_CODE},
            "2.2": {"name": "AD Customization", "paths": [os.path.join(PROJECT_ROOT, "JetIdmJim/Connectors/ADCustomization/ActiveDirectoryCustomization/src/main/java/su/jet/jim/ad/custom")], "context_file": "context_2_2_ad_custom.txt", "model": MODEL_NAME_CODE},
            "2.3": {"name": "LDAP Connector", "paths": [os.path.join(PROJECT_ROOT, "jim/Connectors/Ldap/")], "context_file": "context_2_3_ldap.txt", "model": MODEL_NAME_CODE},
            "2.4": {"name": "JIMConnector", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMConnector/")], "context_file": "context_2_4_jimconnector.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "context_mod_2_connectors_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "3": {
        "name": "mod_3_bpmn_api",
        "subgroups": {
            "3.1": {"name": "Camunda BPMN Engine", "paths": [os.path.join(PROJECT_ROOT, "jim/BPMNEngine/Camunda/JIMCamundaProcess/src/main/java/su/jet/jim/camunda")], "context_file": "context_3_1_camunda_bpmn.txt", "model": MODEL_NAME_CODE},
            "3.2": {"name": "Camunda API Client", "paths": [os.path.join(PROJECT_ROOT, "jim/CamundaApi/openapi/src/main/java/org/camunda/community/rest/client")], "context_file": "context_3_2_camunda_api.txt", "model": MODEL_NAME_CODE},
            "3.3": {"name": "OpenAPI", "paths": [os.path.join(PROJECT_ROOT, "jim/CamundaApi/openapi")], "context_file": "context_3_3_openapi.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "context_mod_3_bpmn_api_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "4": {
        "name": "mod_4_ui",
        "subgroups": {
            "4.1": {"name": "UI Admin Panel", "paths": [os.path.join(PROJECT_ROOT, "jim/UI/admin/src/main/java/su/jet/idm/ui")], "context_file": "context_4_1_ui_admin.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "context_mod_4_ui_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "5": {
        "name": "mod_5_other",
        "subgroups": {
            "5.1": {"name": "JIMGeneral", "paths": [os.path.join(PROJECT_ROOT, "jim/JIM/JIMGeneral/src/main/java/su/jet/jim/general")], "context_file": "context_5_1_general.txt", "model": MODEL_NAME_CODE},
            "5.2": {"name": "K8S", "paths": [os.path.join(PROJECT_ROOT, "K8S")], "context_file": "context_5_2_k8s.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "context_mod_5_other_group.txt",
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

    """Отображает меню и обрабатыет выбор пользователя."""

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

    subgroup_context = ""

    for sub_key, sub_group in group["subgroups"].items():

        if os.path.exists(sub_group["context_file"]):

            print(f"  - Контекст для подгруппы {sub_group['name']} уже существует. Использую его.")

            with open(sub_group["context_file"], 'r', encoding='utf-8') as f:
                subgroup_context += f.read() + "\n\n"

            continue

        print(f"  - Анализирую подгруппу: {sub_group['name']}...")
        file_list = get_all_files_in_dir(sub_group["paths"])
        
        current_subgroup_context = subgroup_context if subgroup_context else "Нет предыдущего контекста."
        prompt_for_subgroup = f"Проанализируй следующий код из подгруппы {sub_group['name']}. Сфокусируйся на функциональности, зависимостях и end-points."
        new_context = analyze_code_block(file_list, current_subgroup_context, prompt_for_subgroup, sub_group['model'])
        
        if new_context:

            with open(sub_group["context_file"], "w", encoding="utf-8") as f:
                f.write(new_context)

            subgroup_context += new_context + "\n\n"
            print(f"  - Контекст для {sub_group['name']} сохранен в {sub_group['context_file']}.")

        else:

            print(f"  - Анализ подгруппы {sub_group['name']} не удался. Прерываю анализ группы.")
            return False


    print(f"\n--- Объединяю контексты подгрупп для {group['name']} ---")
    previous_group_context = load_previous_group_context(group_key)

    if previous_group_context is None:

        print("Не удалось загрузить контекст предыдущих групп. Анализ прерван.")
        return False

    prompt_for_group = f"Скомпонуй и обобщи следующие контексты подгрупп для создания связного КОНТЕКСТА ГРУППЫ для модуля {group['name']}."
    
    group_context = analyze_code_block([], subgroup_context + previous_group_context, prompt_for_group, group['model_for_group'])

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
    
    final_documentation = analyze_code_block([], final_prompt, "Создай итоговый документ.", MODEL_NAME_SUM)
    
    if final_documentation:

        with open("final_documentation.txt", "w", encoding="utf-8") as f:
            f.write(final_documentation)

        print("\n--- Итоговая документация сохранена в final_documentation.txt ---")

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