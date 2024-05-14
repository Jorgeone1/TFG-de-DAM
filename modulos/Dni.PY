import re
import random
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,string
class DNIWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        lista = []
        dnis = {}
        for i in range(cantidad):
            lista.append(self.__generarDni(not self.Nie.isChecked()))
        dnis[titulo] = lista
        return dnis
     
    def __generarDni(self,dni):
        letras= "TRWAGMYFPDXBNJZSQVHLCKE" #lista en orden de los codigos
        letnum={"X":"0","Y":"1","Z":"2"} #diccionario para sustituirlas letras en el dni
        letnum2={0:"X",1:"Y",2:"Z"}
        if(dni):#Comprueba si el codigo que inserto el 
            dninuevo= ""
            dninuevo = dninuevo + "".join(random.choices(string.digits,k=8))
            numeros = int(dninuevo[:8])-int((int(dninuevo[:8])/23))*23
            dninuevo = dninuevo + letras[numeros]
            return dninuevo
        else:#Comprueba si es un NIE
            nie = letnum2[round(random.uniform(0,2))]
            nie = nie + "".join(random.choices(string.digits,k=7))
            
            numeros=int(letnum[nie[0].upper()]+nie[1:8])-(int(int(letnum[nie[0].upper()]+nie[1:8])/23)*23)
            return nie + letras[numeros]

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DNIWidget()
    mainWindow.show()
    sys.exit(app.exec())


