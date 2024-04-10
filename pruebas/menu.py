import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menú Emergente")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Haz clic derecho aquí", self)
        self.label.setGeometry(50, 50, 200, 50)

        self.initUI()

    def initUI(self):
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos: QPoint):
        context_menu = QMenu(self)

        option1_action = context_menu.addAction("Opción 1")
        option1_action.triggered.connect(self.option1Selected)

        option2_menu = context_menu.addMenu("Opción 2")
        option2_submenu1 = option2_menu.addAction("Subopción 1")
        option2_submenu1.triggered.connect(lambda: self.option2Selected("Subopción 1"))
        
        option2_submenu2 = option2_menu.addMenu("Submenú 2")
        option2_submenu2_submenu1 = option2_submenu2.addAction("Subsubopción 1")
        option2_submenu2_submenu1.triggered.connect(lambda: self.option2SubSelected("Submenú 2 - Subsubopción 1"))
        option2_submenu2_submenu2 = option2_submenu2.addAction("Subsubopción 2")
        option2_submenu2_submenu2.triggered.connect(lambda: self.option2SubSelected("Submenú 2 - Subsubopción 2"))

        option3_action = context_menu.addAction("Opción 3")
        option3_action.triggered.connect(self.option3Selected)

        context_menu.exec(self.label.mapToGlobal(pos))

    def option1Selected(self):
        self.optionSelected("Opción 1")

    def option2Selected(self, suboption):
        self.optionSelected(f"Opción 2 - {suboption}")

    def option2SubSelected(self, suboption):
        self.optionSelected(suboption)

    def option3Selected(self):
        self.optionSelected("Opción 3")

    def optionSelected(self, option):
        print(f"Seleccionaste la opción: {option}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()