import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from scripts.editor import DialogueEditor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set global font for better readability
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = DialogueEditor()

    window.show()
    
    sys.exit(app.exec())
