import random
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class SegSolWidget(QWidget):
    def __init__(self):
        super().__init__()
        
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
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = SegSolWidget()
    mainWindow.show()
    sys.exit(app.exec())

def comprobarNaf():
    
    naf = "28"
    for i in range(8):
        naf= naf + str(round(random.uniform(0,9)))
    if(int(naf[2:10])<10000000):#comprueba si los numeros del medio supera los 
        numeros=((int(naf[:1])+int(naf[2:10]))*10000000)%97       
    else:
        numeros=int((int(naf[:10]))%97)#sino realizara otro tipo de operación
    naf = naf +str(numeros)       
    return naf