from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication
import sys
class DireccionWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.label = QLabel("Direccion:", self)
        self.editline = QLineEdit(self)
        self.button = QPushButton("Click Me", self)
        self.editline.setPlaceholderText("Nombre Proyecto")
        layout = QGridLayout()
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.button,1,0,2,0)
        
        self.setLayout(layout)
        
        self.button.clicked.connect(self.on_button_clicked)
        
        
    def on_button_clicked(self):
        nombre = self.editline.text()
        print("Nombre ingresado:", nombre)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = NombreWidget()
    mainWindow.show()
    sys.exit(app.exec())
