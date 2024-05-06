from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication, QCheckBox, QFrame
import sys
import random
import pymongo
class NombreWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creamos los elementos del widget
        self.label = QLabel("Nombre:", self)
        self.editline = QLineEdit(self)
        self.checkbox = QCheckBox("Mi CheckBox")
        self.editline.setPlaceholderText("Nombre Proyecto")
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.checkbox,1,0)
        
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
        


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


