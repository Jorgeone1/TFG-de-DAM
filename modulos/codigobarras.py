from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys
import random
class BarraWidget(QWidget):
    def __init__(self):
        super().__init__()
        #Creamos los elementos del widget
        self.label = QLabel("CodigoBarras:", self)
        self.editline = QLineEdit(self)
        self.UPC = QCheckBox("UPC")
        self.EAN = QCheckBox("EAN")
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.UPC.stateChanged.connect(self.__bloquearEAN)
        self.EAN.stateChanged.connect(self.__bloquearUPC)
        self.UPC.setChecked(True)
        self.EAN.setEnabled(False)
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos el layout al qframe
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #Agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.UPC,1,0)
        layout.addWidget(self.EAN,1,1)
        
        #Establecemos layout al widget
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
    
    def __bloquearEAN(self,state):
        if state == 2:
            self.EAN.setEnabled(False)
        else:
            self.EAN.setEnabled(True)
            
    def __bloquearUPC(self,state):
        if state == 2:
            self.UPC.setEnabled(False)
        else:
            self.UPC.setEnabled(True)
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "Codigo De Barras"
        lista = []
        codigos = {}
        for i in range(cantidad):
            lista.append(self.__generar_barrar())
        codigos[titulo] = lista
        return codigos


    def __generar_barrar(self):
        #creamos un codigo de barra
        barra = ""
        rango = 0
        #comprueba si esta checkeada o no
        rango = 11 if self.UPC.isChecked() else 12
        for i in range(rango):
            barra = barra + str(random.randint(0,9))
        
        #saca el codigo de verificacion
        barra = barra + str(self.__Calcular_ultimo_digito(barra))
        return barra
        
    def __Calcular_ultimo_digito(self,barra):
        pares = 0
        impares = 0
        #si es par suma el valor multiplicado por 2 y si es impar solo suma
        for i in range(0,len(barra)):
            if i % 2 == 0:
                pares += (int(barra[i]) * 2)
            else:
                impares += int(barra[i]) 
        #devuelve el valor sumado y restado por el resto entre 10 del resultado
        return 10 - ((pares + impares)%10)
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = BarraWidget()
    mainWindow.show()
    sys.exit(app.exec())