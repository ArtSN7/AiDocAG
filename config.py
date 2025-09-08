# Root directory fallback
PROJECT_ROOT_FALLBACK = "../"

# Directory for storing contexts
CONTEXT_ROOT = "contexts"
EXT = "txt" # может быть md

# Model names
MODEL_NAME_CODE = "gemma3:4b"
MODEL_NAME_SUM = "gemma3:4b"

# Ollama API settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MAX_FILE_SIZE_KB = 2048  # Maximum file size in KB for analysis
TEMPERATURE = 0.1  # Temperature for LLM
NUM_PREDICT = 8192  # Number of tokens to predict

# Supported file extensions 
SUPPORTED_EXTENSIONS = [
    '.java', '.sql', '.xml', '.yaml', '.yml', '.properties', '.json', 
    '.kt', '.groovy', '.sh', '.bat', '.md', '.txt' ]

# Module structure
MODULES = {
    "1": {
        "name": "mod_1_core",
        "subgroups": {
            "1.1": {"name": "JIMCore", "paths": ["jim/JIM/JIMCore/src/main/java/su/jet/jim"], "context_dir": "mod_1_core/JIMCore", "group_context_file": "mod_1_core/context_1_1_jimcore.txt", "model": MODEL_NAME_CODE},
            "1.2": {"name": "JIMDB", "paths": ["jim/JIM/JIMDB/src/main/java/su/jet/jim/db"], "context_dir": "mod_1_core/JIMDB", "group_context_file": "mod_1_core/context_1_2_jimdb.txt", "model": MODEL_NAME_CODE},
            "1.3": {"name": "JIMFunctionality", "paths": ["jim/JIM/JIMFunctionality/src/main/java/su/jet/jim"], "context_dir": "mod_1_core/JIMFunctionality", "group_context_file": "mod_1_core/context_1_3_jimfunc.txt", "model": MODEL_NAME_CODE},
            "1.4": {"name": "JIMAPIDTO", "paths": ["jim/JIM/JIMAPIDTO/src/main/java/su/jet/jim/rest"], "context_dir": "mod_1_core/JIMAPIDTO", "group_context_file": "mod_1_core/context_1_4_apidto.txt", "model": MODEL_NAME_CODE},
            "1.5": {"name": "JIMExtender", "paths": ["jim/JIM/JIMExtender/src/main/java/su/jet/jim/extender"], "context_dir": "mod_1_core/JIMExtender", "group_context_file": "mod_1_core/context_1_5_jimextender.txt", "model": MODEL_NAME_CODE},
            "1.6": {"name": "DBSchema", "paths": ["JetIdmJim/DBSchema/liquibase/sql", "jim/DBSchema"], "context_dir": "mod_1_core/DBSchema", "group_context_file": "mod_1_core/context_1_6_dbschema.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "mod_1_core/context_mod_1_core_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "2": {
        "name": "mod_2_connectors",
        "subgroups": {
            "2.1": {"name": "AD Connector", "paths": ["jim/Connectors/AD/ActiveDirectoryConnector/src/main/java/su/jet/jim/ad"], "context_dir": "mod_2_connectors/AD_Connector", "group_context_file": "mod_2_connectors/context_2_1_ad.txt", "model": MODEL_NAME_CODE},
            "2.2": {"name": "AD Customization", "paths": ["JetIdmJim/Connectors/ADCustomization/ActiveDirectoryCustomization/src/main/java/su/jet/jim/ad/custom"], "context_dir": "mod_2_connectors/AD_Customization", "group_context_file": "mod_2_connectors/context_2_2_ad_custom.txt", "model": MODEL_NAME_CODE},
            "2.3": {"name": "LDAP Connector", "paths": ["jim/Connectors/Ldap/"], "context_dir": "mod_2_connectors/LDAP_Connector", "group_context_file": "mod_2_connectors/context_2_3_ldap.txt", "model": MODEL_NAME_CODE},
            "2.4": {"name": "JIMConnector", "paths": ["jim/JIM/JIMConnector/"], "context_dir": "mod_2_connectors/JIMConnector", "group_context_file": "mod_2_connectors/context_2_4_jimconnector.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "mod_2_connectors/context_mod_2_connectors_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "3": {
        "name": "mod_3_bpmn_api",
        "subgroups": {
            "3.1": {"name": "Camunda BPMN Engine", "paths": ["jim/BPMNEngine/Camunda/JIMCamundaProcess/src/main/java/su/jet/jim/camunda"], "context_dir": "mod_3_bpmn_api/Camunda_BPMN_Engine", "group_context_file": "mod_3_bpmn_api/context_3_1_camunda_bpmn.txt", "model": MODEL_NAME_CODE},
            "3.2": {"name": "Camunda API Client", "paths": ["jim/CamundaApi/openapi/src/main/java/org/camunda/community/rest/client"], "context_dir": "mod_3_bpmn_api/Camunda_API_Client", "group_context_file": "mod_3_bpmn_api/context_3_2_camunda_api.txt", "model": MODEL_NAME_CODE},
            "3.3": {"name": "OpenAPI", "paths": ["jim/CamundaApi/openapi"], "context_dir": "mod_3_bpmn_api/OpenAPI", "group_context_file": "mod_3_bpmn_api/context_3_3_openapi.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "mod_3_bpmn_api/context_mod_3_bpmn_api_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "4": {
        "name": "mod_4_ui",
        "subgroups": {
            "4.1": {"name": "UI Admin Panel", "paths": ["jim/UI/admin/src/main/java/su/jet/idm/ui"], "context_dir": "mod_4_ui/UI_Admin_Panel", "group_context_file": "mod_4_ui/context_4_1_ui_admin.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "mod_4_ui/context_mod_4_ui_group.txt",
        "model_for_group": MODEL_NAME_SUM
    },
    "5": {
        "name": "mod_5_other",
        "subgroups": {
            "5.1": {"name": "JIMGeneral", "paths": ["jim/JIM/JIMGeneral/src/main/java/su/jet/jim/general"], "context_dir": "mod_5_other/JIMGeneral", "group_context_file": "mod_5_other/context_5_1_general.txt", "model": MODEL_NAME_CODE},
            "5.2": {"name": "K8S", "paths": ["K8S"], "context_dir": "mod_5_other/K8S", "group_context_file": "mod_5_other/context_5_2_k8s.txt", "model": MODEL_NAME_CODE},
        },
        "group_context_file": "mod_5_other/context_mod_5_other_group.txt",
        "model_for_group": MODEL_NAME_SUM
    }
}

# Prompts
FILE_PROMPT = (
    "Проанализируй следующий код из файла, фокусируясь исключительно на логике: "
    "опиши подробно, что делают ключевые функции и системы, как компоненты взаимодействуют между собой, "
    "основные моменты и потоки данных. Исключи детали импортов, вызовов функций, потенциальных ошибок или улучшений. "
    "Сделай описание подробным, но структурированным для удобного чтения (используй заголовки, списки, абзацы)."
)

DIR_PROMPT = (
    "Скомпонуй и обобщи следующие контексты файлов и поддиректорий в этой директории, "
    "чтобы создать связный контекст директории: выдели основные моменты по каждому, "
    "опиши подробно взаимодействия между компонентами/файлами/поддиректориями, "
    "ключевые системы и логику. Сделай описание подробным, структурированным (заголовки, списки, абзацы) "
    "для удобного чтения, без советов по улучшениям — только чистая логика и основные аспекты."
)

FINAL_PROMPT = (
    "Используй следующий агрегированный контекст всего проекта, чтобы создать полную, связную и подробную документацию "
    "для проекта. Объедини все в единый документ с четкой структурой: введение, разделы по директориям/модулям, "
    "описания взаимодействий, ключевых систем и логики. Сделай текст удобным для чтения с заголовками, подразделами, "
    "списками и абзацами.\n"
    "Собранный контекст:\n"
)