import os
import sys

def print_directory_structure(startpath, indent=''):
    
    """
    Рекурсивно печатает структуру директорий проекта в tree-like формате, включая только папки.
    
    Args:
    startpath (str): Путь к корневой директории проекта.
    indent (str): Текущий отступ для уровня вложенности (используется рекурсивно).
    """

    items = sorted([item for item in os.listdir(startpath) if os.path.isdir(os.path.join(startpath, item))])
    for i, item in enumerate(items):
        path = os.path.join(startpath, item)
        is_last = (i == len(items) - 1)
        prefix = '└── ' if is_last else '├── '
        print(f"{indent}{prefix}{item}/")
        
        new_indent = indent + ('    ' if is_last else '│   ')
        print_directory_structure(path, new_indent)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py /path/to/your/project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    if not os.path.isdir(project_path):
        print(f"Ошибка: '{project_path}' не является директорией.")
        sys.exit(1)
    
    print(os.path.basename(project_path) + '/')
    print_directory_structure(project_path)