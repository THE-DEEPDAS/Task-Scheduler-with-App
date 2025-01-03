import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Data storage settings
DATA_DIR = os.path.join(BASE_DIR, 'data')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.csv')
DEPENDENCIES_FILE = os.path.join(DATA_DIR, 'dependencies.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
