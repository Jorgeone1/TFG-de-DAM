import re
import random
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests
class DNIWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma
        #creamos los elementos del Widget
        self.label = QLabel("DNI:", self)
        self.editline = QLineEdit(self)
        self.Nie = QCheckBox("NIE")
        self.editline.setPlaceholderText("Nombre Proyecto")
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #agregamos el layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.Nie,1,0)
        
        #agregamos layout al widget principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "DNI" 
        if self.Nie.isChecked() and titulo == "DNI":
            titulo = "NIE"
        url = f"http://127.0.0.1:5000/dni/{cantidad}/{int(self.Nie.isChecked())}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        dnis = {}        
        dnis[titulo] = data["dni"]
        return dnis
     
    

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DNIWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())


