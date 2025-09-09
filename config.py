# Root directory fallback
PROJECT_ROOT_FALLBACK = "../"

# Directory for storing contexts
CONTEXT_ROOT = "contexts"
MODULES_CONTEXTS_ROOT = "modules_contexts"  # НОВОЕ: Папка для хранения саммари директорий и модулей
EXT = "txt" # может быть md

# Model name
MODEL_NAME_CODE = "gemma3:4b"
MODEL_NAME_SUM = "gemma3:4b"  # НОВОЕ: Модель для создания саммари

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
            "1.1": {"name": "JIMCore", "paths": ["jim/JIM/JIMCore/src/main/java/su/jet/jim"], "model": MODEL_NAME_CODE},
            "1.2": {"name": "JIMDB", "paths": ["jim/JIM/JIMDB/src/main/java/su/jet/jim/db"], "model": MODEL_NAME_CODE},
            "1.3": {"name": "JIMFunctionality", "paths": ["jim/JIM/JIMFunctionality/src/main/java/su/jet/jim"], "model": MODEL_NAME_CODE},
            "1.4": {"name": "JIMAPIDTO", "paths": ["jim/JIM/JIMAPIDTO/src/main/java/su/jet/jim/rest"], "model": MODEL_NAME_CODE},
            "1.5": {"name": "JIMExtender", "paths": ["jim/JIM/JIMExtender/src/main/java/su/jet/jim/extender"], "model": MODEL_NAME_CODE},
            "1.6": {"name": "DBSchema", "paths": ["JetIdmJim/DBSchema/liquibase/sql", "jim/DBSchema"], "model": MODEL_NAME_CODE},
        }
    },
    "2": {
        "name": "mod_2_connectors",
        "subgroups": {
            "2.1": {"name": "AD Connector", "paths": ["jim/Connectors/AD/ActiveDirectoryConnector/src/main/java/su/jet/jim/ad"], "model": MODEL_NAME_CODE},
            "2.2": {"name": "AD Customization", "paths": ["JetIdmJim/Connectors/ADCustomization/ActiveDirectoryCustomization/src/main/java/su/jet/jim/ad/custom"], "model": MODEL_NAME_CODE},
            "2.3": {"name": "LDAP Connector", "paths": ["jim/Connectors/Ldap/"], "model": MODEL_NAME_CODE},
            "2.4": {"name": "JIMConnector", "paths": ["jim/JIM/JIMConnector/"], "model": MODEL_NAME_CODE},
        }
    },
    "3": {
        "name": "mod_3_bpmn_api",
        "subgroups": {
            "3.1": {"name": "Camunda BPMN Engine", "paths": ["jim/BPMNEngine/Camunda/JIMCamundaProcess/src/main/java/su/jet/jim/camunda"], "model": MODEL_NAME_CODE},
            "3.2": {"name": "Camunda API Client", "paths": ["jim/CamundaApi/openapi/src/main/java/org/camunda/community/rest/client"], "model": MODEL_NAME_CODE},
            "3.3": {"name": "OpenAPI", "paths": ["jim/CamundaApi/openapi"], "model": MODEL_NAME_CODE},
        }
    },
    "4": {
        "name": "mod_4_ui",
        "subgroups": {
            "4.1": {"name": "UI Admin Panel", "paths": ["jim/UI/admin/src/main/java/su/jet/idm/ui"], "model": MODEL_NAME_CODE},
        }
    },
    "5": {
        "name": "mod_5_other",
        "subgroups": {
            "5.1": {"name": "JIMGeneral", "paths": ["jim/JIM/JIMGeneral/src/main/java/su/jet/jim/general"], "model": MODEL_NAME_CODE},
            "5.2": {"name": "K8S", "paths": ["K8S"], "model": MODEL_NAME_CODE},
        }
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
    "ключевые системы и логику. Сделай описание очень подробным, развернутым и структурированным (заголовки, подразделы, списки, абзацы) "
    "для удобного чтения, без советов по улучшениям — только чистая логика и основные аспекты."
)

MODULE_PROMPT = ( 
    "Обобщи следующие контексты подгрупп и директорий модуля, "
    "чтобы создать связный контекст всего модуля: выдели основные моменты по каждому, "
    "опиши подробно взаимодействия между подгруппами и компонентами, "
    "ключевые системы и логику модуля в целом. Сделай описание очень подробным, развернутым и структурированным (заголовки, подразделы, списки, абзацы) "
    "для удобного чтения, без советов по улучшениям — только чистая логика и основные аспекты."
)