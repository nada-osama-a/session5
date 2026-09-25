import sys
from PySide6.QtWidgets import QApplication
from console.gui.window import Window  

def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
