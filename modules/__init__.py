import importlib
import os
from main import app  # Impor 'app' dari 'main.py' agar tersedia di semua modul

# Inisialisasi semua modul yang ada di direktori 'modules'
module_directory = os.path.dirname(__file__)

for filename in os.listdir(module_directory):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"modules.{filename[:-3]}"
        importlib.import_module(module_name)
