# JET-AI-AGENT

## Стратегия анализа

Для документирования системы IDM кодовая база разделяется на логические группы и подгруппы. Каждая группа анализируется итеративно с учетом контекста для создания точной документации. Процесс включает:

1. Разделение файлов на модули (например, mod_1, mod_2 и т.д.) и подгруппы (например, mod_1.1, mod_1.2).
2. Первичный анализ подгрупп для создания начального контекста (КОНТЕКСТ_1).
3. Переход на уровень выше для создания КОНТЕКСТ_ГРУППЫ основываясь на КОНТЕКСТ_1, КОНТЕКСТ_2 ( контексты подгрупп )
4. Объединение всех контекстов для создания полной документации.

---

## Структура модулей

### mod_1: Основные и связанные модули

Содержит основную бизнес-логику, структуру базы данных и расширяемые компоненты.

- **mod_1.1: JIMCore**
    - Путь: GITHUB/jim/JIM/JIMCore/src/main/java/su/jet/jim
    - Описание: Основная бизнес-логика, контроллеры, обработчики событий и базовые компоненты.
- **mod_1.2: JIMDB**
    - Путь: GITHUB/jim/JIM/JIMDB/src/main/java/su/jet/jim/db
    - Описание: Определения таблиц и записей базы данных, сгенерированные с помощью JOOQ.
- **mod_1.3: JIMFunctionality**
    - Путь: GITHUB/jim/JIM/JIMFunctionality/src/main/java/su/jet/jim
    - Описание: Функциональные компоненты, включая коннекторы, обработчики событий, сервисы и генераторы.
- **mod_1.4: JIMAPIDTO**
    - Путь: GITHUB/jim/JIM/JIMAPIDTO/src/main/java/su/jet/jim/rest
    - Описание: Объекты DTO для REST API, помогающие документировать форматы запросов и ответов.
- **mod_1.5: JIMExtender**
    - Путь: GITHUB/jim/JIM/JIMExtender/src/main/java/su/jet/jim/extender
    - Описание: Расширяемая функциональность системы.
- **mod_1.6: DBSchema**
    - Путь: GITHUB/JetIdmJim/DBSchema/liquibase/sql, GITHUB/jim/DBSchema
    - Описание: Файлы Liquibase для управления схемой базы данных.

### mod_2: Модули коннекторов

Отвечает за интеграцию с внешними системами.

- **mod_2.1: Коннектор Active Directory (AD)**
    - Путь: GITHUB/jim/Connectors/AD/ActiveDirectoryConnector/src/main/java/su/jet/jim/ad
    - Описание: Логика взаимодействия с Active Directory.
- **mod_2.2: Кастомизация AD**
    - Путь: GITHUB/JetIdmJim/Connectors/ADCustomization/ActiveDirectoryCustomization/src/main/java/su/jet/jim/ad/custom
    - Описание: Кастомная логика для коннектора Active Directory.
- **mod_2.3: Коннектор LDAP**
    - Путь: GITHUB/jim/Connectors/Ldap/
    - Описание: Коннектор для интеграции с LDAP.
- **mod_2.4: JIMConnector**
    - Путь: GITHUB/jim/JIM/JIMConnector/
    - Описание: Общий модуль для управления коннекторами.

### mod_3: Модули BPMN и API

Управление рабочими процессами и взаимодействием с API.

- **mod_3.1: Движок Camunda BPMN**
    - Путь: GITHUB/jim/BPMNEngine/Camunda/JIMCamundaProcess/src/main/java/su/jet/jim/camunda
    - Описание: Делегаты для процессов Camunda BPMN.
- **mod_3.2: Клиент Camunda API**
    - Путь: GITHUB/jim/CamundaApi/openapi/src/main/java/org/camunda/community/rest/client
    - Описание: Java-клиент для REST API Camunda.
- **mod_3.3: OpenAPI**
    - Путь: GITHUB/jim/CamundaApi/openapi
    - Описание: Определения OpenAPI для API Camunda.

### mod_4: Модуль интерфейса

Управление пользовательским интерфейсом.

- **mod_4.1: Панель администрирования UI**
    - Путь: GITHUB/jim/UI/admin/src/main/java/su/jet/idm/ui
    - Описание: Логика фронтенда для административной панели.

### mod_5: Прочие модули

Вспомогательные и дополнительные модули.

- **mod_5.1: JIMGeneral**
    - Путь: GITHUB/jim/JIM/JIMGeneral/src/main/java/su/jet/jim/general
    - Описание: Общие компоненты, используемые в проекте.
- **mod_5.2: K8S**
    - Путь: GITHUB/K8S
    - Описание: Файлы конфигурации для развертывания в Kubernetes.
    

---

## Порядок анализа

1. **Анализ mod_1**: Загрузка и анализ файлов из JIMCore, JIMDB, JIMFunctionality, JIMAPIDTO, JIMExtender и DBSchema для создания **КОНТЕКСТ_1**.
2. **Анализ mod_2**: Анализ файлов из AD Connector, AD Customization, Ldap Connector и JIMConnector с использованием **КОНТЕКСТ_1** для создания **КОНТЕКСТ_2**.
3. **Анализ mod_3**: Анализ файлов из Camunda BPMN Engine, Camunda API Client и OpenAPI с использованием **КОНТЕКСТ_1** и **КОНТЕКСТ_2** для создания **КОНТЕКСТ_3**.
4. **Анализ mod_4**: Анализ файлов из UI Administration Panel с использованием **КОНТЕКСТ_1**, **КОНТЕКСТ_2** и **КОНТЕКСТ_3**.
5. **Анализ mod_5**: Анализ файлов из JIMGeneral и K8S для создания **КОНТЕКСТ_4**.
6. **Финальный анализ**: Объединение всех контекстов (**КОНТЕКСТ_1**, **КОНТЕКСТ_2**, **КОНТЕКСТ_3**, **КОНТЕКСТ_4**) для создания полной документации.

---

## Технологии

| Ollama Model | Reason | Requirements |
| --- | --- | --- |
| Gpt-oss 20B ( or 120B ) | DeepSeek-R1 32B ( or 70B ) | Ревью кода построчно  | от 20 ГБ до 65 ГБ памяти |
| Llama 3.2 3B | Легкая для написания заключения | 2GB |

---

## Запуск

1. Скачать ollama - https://ollama.com/


```bash
ollama pull gemma3:4b
```

```bash
ollama serve
```

2. Установить Python and Libraries

```bash
pip install requests
```

1. Запуск скрипта

```bash
python interactive_service.py
```