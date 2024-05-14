import random
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class TelefonoWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creamos elementos del widget
        self.label = QLabel("Telfono:", self)
        self.editline = QLineEdit(self)
        self.fijo = QCheckBox("Fijo")
        self.mobil = QCheckBox("Mobil")
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
        layout.addWidget(self.fijo,1,0)
        layout.addWidget(self.mobil,1,1)
        
        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "Telefono"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = TelefonoWidget()
    mainWindow.show()
    sys.exit(app.exec())

def crearTelefono(idioma,tipo):
    telefono = ""

    if idioma == "ES":
        if tipo:
            telefono = "9"
            for i in range(8):
                telefono = telefono +str(round(random.uniform(0,9)))
            return telefono
        else:
            rand = round(random.uniform(0,1))
            if rand == 0:
                telefono = "6"
            else:
                telefono="7"
            for i in range(8):
                telefono = telefono +str(round(random.uniform(0,9)))
            return telefono
    elif idioma == "EN":
        telefono = ""
        if tipo:
            telefono = "01"
            for i in range(9):
                telefono = telefono + str(round(random.uniform(0,9)))
            return telefono
        else:
            telefono = "07"
            for i in range(9):
                telefono = telefono + str(round(random.uniform(0,9)))
            return telefono
        