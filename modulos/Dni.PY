import re
import random
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class DNIWidget(QWidget):
    def __init__(self):
        super().__init__()
        #creamos los elementos del Widget
        self.label = QLabel("DNI:", self)
        self.editline = QLineEdit(self)
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
        
        #agregamos layout al widget principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DNIWidget()
    mainWindow.show()
    sys.exit(app.exec())

def comprobarDni(dni):
    letras= "TRWAGMYFPDXBNJZSQVHLCKE" #lista en orden de los codigos
    letnum={"X":"0","Y":"1","Z":"2"} #diccionario para sustituirlas letras en el dni
    letnum2={0:"X",1:"Y",2:"Z"}
    if(dni):#Comprueba si el codigo que inserto el 
        dninuevo= ""
        for i in range(8):
            dninuevo = dninuevo + str(round(random.uniform(0,9)))
        numeros = int(dninuevo[:8])-int((int(dninuevo[:8])/23))*23
        dninuevo = dninuevo + letras[numeros]
        return dninuevo
    else:#Comprueba si es un NIE
        nie = letnum2[round(random.uniform(0,2))]
        for i in range(7):
            nie = nie + str(round(random.uniform(0,9)))
        
        numeros=int(letnum[nie[0].upper()]+nie[1:8])-(int(int(letnum[nie[0].upper()]+nie[1:8])/23)*23)
        return nie + letras[numeros]

