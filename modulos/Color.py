from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
from PIL import ImageColor
import random

class ColorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #Creamos los elementos del widget
        self.label = QLabel("Color:", self)
        self.editline = QLineEdit(self)
        self.Hex = QCheckBox("Sin Hex")
        self.rgb = QCheckBox("RGB")
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.rgbline = QLineEdit()
        self.rgbline.setPlaceholderText("Nombre RGB")
        self.Hex.setEnabled(False)
        self.rgbline.setEnabled(False)

        self.rgb.stateChanged.connect(self.__bloquearHex)
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al QFrame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,2)
        layout.addWidget(self.Hex,1,1)
        layout.addWidget(self.rgb,1,0)
        layout.addWidget(self.rgbline,2,0,1,2)
        
        #establecemos un layout al Principal
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
    def __bloquearHex(self,state):
        if state == 2:
            self.Hex.setEnabled(True)
            self.rgbline.setEnabled(True)
        else:
            self.Hex.setEnabled(False)
            self.Hex.setChecked(False)
            self.rgbline.setEnabled(False)

    def getData(self,cantidad):
        titulo = self.editline.text() or "Color"
        rgb = self.rgbline.text() or "RGB"
        listaHex = []
        listaRGB = []
        colores = {}
        for i in range(cantidad):
            colo = self.__CrearHex()
            listaHex.append(colo)
            listaRGB.append(self.__hex_to_rgb(colo))
        #comprueba si esta checkeado o no
        if self.rgb.isChecked():
            colores[rgb] = listaRGB
            if not self.Hex.isChecked():
                colores[titulo] = listaHex
        else:
            colores[titulo] = listaHex
        return colores

    def __hex_to_rgb(self,hex_color):
        #calcula el rgba del hex
        rgba_tuple = ImageColor.getcolor(hex_color, "RGBA")
        return rgba_tuple[:3]  # Tomamos los primeros tres valores (RGB)
    
    def __CrearHex(self):
        hex = "#"
        lista = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","F"] #Posibles numeros
        for i in range(6):
            hex = hex + random.choice(lista)
        return hex

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ColorWidget()
    mainWindow.show()
    sys.exit(app.exec())