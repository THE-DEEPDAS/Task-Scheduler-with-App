import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main_logic import TaskManager
from src.ui.main_window import MainWindow

def main():
    """
    Initialize and start the task management application with GUI.
    """
    task_manager = TaskManager()
    app = MainWindow(task_manager)
    app.mainloop()

if __name__ == "__main__":
    main()
