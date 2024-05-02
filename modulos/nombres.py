from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication, QCheckBox
import sys
import random
import pymongo
class NombreWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.label = QLabel("Nombre:", self)
        self.editline = QLineEdit(self)
        self.button = QPushButton("Click Me", self)
        self.checkbox = QCheckBox("Mi CheckBox")
        self.editline.setPlaceholderText("Nombre Proyecto")
        layout = QGridLayout()
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.button,1,0,2,0)
        layout.addWidget(self.checkbox,1,2)
        
        self.setLayout(layout)
        
        self.button.clicked.connect(self.on_button_clicked)
        
        
    def on_button_clicked(self):
        nombre = self.editline.text()
        print(random.uniform(0,9))
        print("Nombre ingresado:", nombre)

    def getData(self,cantidad):
        titulo = self.editline.text()
        # Establecer conexión con el servidor de MongoDB
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        print(self.checkbox.isChecked())
        # Seleccionar la base de datos
        db = cliente["GeneradorDeDatos"]
        # Obtener la colección en la que deseas insertar datos
        lis = [titulo]
        for i in range(cantidad):
            num = round(random.uniform(0,96529))
            print(num)
            cursor = db.NombreEng.find({"id": num})
            for documento in cursor:
                lis.append(documento["name"])
        return lis
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = NombreWidget()
    mainWindow.show()
    sys.exit(app.exec())


