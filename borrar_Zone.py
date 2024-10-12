import os

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Eliminado: {file_path}")
            except Exception as e:
                print(f"No se pudo eliminar {file_path}: {e}")