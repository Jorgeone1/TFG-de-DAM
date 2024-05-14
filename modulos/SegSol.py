import random, string
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class SegSolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.idioma = "EN"
        #creamos elementos de widget
        self.label = QLabel("Seguridad Social:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox()
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
        layout.addWidget(self.check,1,0)
        
        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "Seguridad Social"
        lista = []
        seg = {}
        for i in range(cantidad):
            if self.idioma == "ES":
                lista.append(self.comprobarNaf())
            if self.idioma =="EN":
                lista.append(self.generarEnSeg())
        seg[titulo]= lista
        return seg
    def comprobarNaf(self):
        
        naf = "28"
        naf += ''.join(random.choices(string.digits, k=8))
        if(int(naf[2:10])<10000000):#comprueba si los numeros del medio supera los 
            numeros=((int(naf[:1])+int(naf[2:10]))*10000000)%97       
        else:
            numeros=int((int(naf[:10]))%97)#sino realizara otro tipo de operación
        naf = naf +str(numeros)       
        return naf
    def generarEnSeg(self):
        seg = self.generar_prefijo()
        seg += "".join(random.choices(string.digits, k=6))
        seg += random.choice(["A","B","C","D"])
        return seg
    def generar_prefijo(self):
        while True:
            #genera lista sin las letras prohibidas
            letrasvalidas = []
            for letra in string.ascii_uppercase:
                if letra not in 'DFIQUV':
                    letrasvalidas.append(letra)
            primerletra = random.choice(letrasvalidas)
            #lo mismo pero añadiendo la o
            letraval= []
            for letra in letrasvalidas:
                if letra != 'O':
                    letraval.append(letra)
            segundaletra = random.choice(letraval)
            # Comrpueba que la primera letra y segunda no hagan un combo que este prohibido
            prefijo = primerletra + segundaletra
            if not prefijo in ('BG', 'GB', 'KN', 'NK', 'NT', 'TN', 'ZZ'):
                return prefijo
            else:
                print("error")
            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = SegSolWidget()
    print(mainWindow.generarEnSeg())
    mainWindow.show()
    sys.exit(app.exec())
