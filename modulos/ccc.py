import random
#Comprobación y operaciones del ccc
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame 
import sys,string
class CCCWidget(QWidget):
    def __init__(self):
        super().__init__()
        #crear los elementos del widget
        self.label = QLabel("CCC:", self)
        self.editline = QLineEdit(self)
        self.IBAN = QCheckBox("IBAN")
        self.noCC = QCheckBox("Sin CCC")
        self.noCC.setEnabled(False)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.IBAN.stateChanged.connect(self.bloquearCCC)
        self.ibanline = QLineEdit()
        self.ibanline.setPlaceholderText("Nombre IBAN")
        self.ibanline.setEnabled(False)
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #Establecer layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        #Agregar los elementos al QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1)
        frame_layout.addWidget(self.IBAN, 1, 0)
        frame_layout.addWidget(self.noCC, 1, 1)
        frame_layout.addWidget(self.ibanline,2,0,1,2)
        
        #Establecer el layout principal del widget
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)

    def bloquearCCC(self,state):
        if state == 2:  # 2 significa que el CheckBox está marcado
            self.noCC.setEnabled(True)
            self.ibanline.setEnabled(True)
        else:
            self.noCC.setEnabled(False)
            self.noCC.setChecked(False)
            self.ibanline.setEnabled(False)

    def getData(self,cantidad):
        #Comprueba que tenga texto los lineEdit sino sera uno predeterminado
        title = self.editline.text() or "CCC"
        iban_name = self.ibanline.text() or "IBAN"
        #Creacion de lista para guardar datos
        listaCCC = []
        listaIBAN = []
        datosBancarios  = {}
        for i in range(cantidad):
            cc = self.__comprobarIBAN()
            iba =self.__CreadorIBAN(cc)
            listaCCC.append(cc)
            listaIBAN.append(iba)
        #depende de los check del checkbox
        if self.IBAN.isChecked():
            datosBancarios[iban_name] = listaIBAN
            if not self.noCC.isChecked():
                datosBancarios[title] = listaCCC
        else:
            datosBancarios[title] = listaCCC
        return datosBancarios



    def __comprobarIBAN(self):
        entidad = ""
        codigocuenta = ""
        entidad = entidad + "".join(random.choices(string.digits,k=8))
        codigocuenta =codigocuenta+ "".join(random.choices(string.digits,k=10))

        num1=[4,8,5,10,9,7,3,6] #Guarda las operaciones para el primer digito en orden
        num2=[1,2,4,8,5,10,9,7,3,6] #Guarda las operaciones del segundo digito en orden
        
        digito1=self.__primerDigito(entidad,num1) #Realiza las operaciones del digito 1
        digito2=self.__segundoDigito(codigocuenta,num2) #Realiza las operaciones del digito 2
        total= f"{digito1}{digito2}" #los junta
        return entidad + total + codigocuenta   #devuelve un booleano si coinciden o no

    #operaciones del primer digito
    def __primerDigito(self,entidad,num1):
        numeros=0
        for po in range(0,8): #for que realiza las operaciones
            numeros= numeros + (int(entidad[po])*num1[po])
        resto=numeros%11
        
        if(resto==1):
            return 1
        else:
            return int(11- resto)
        
    #Operaciones con el segundo digito
    def __segundoDigito(self,codigocuenta,num2):
        numeros2=0
        for pi in range(0,len(num2)): # for que realiza las operaciones
            numeros2= numeros2 + (int(codigocuenta[pi])*num2[pi])
        resto2=11-(numeros2%11)
        if(resto2==10):
            return 1
        else:
            return resto2
        
    def __CreadorIBAN(self,cuenta):
        total=cuenta+"142800" 
        numerosiban=98-(int(total)%97) #realiza la operación para calcular los numeros de despues del ES
        if(len(str(numerosiban))==1):
            numerosiban="0" + str(numerosiban) #Crea un iban pero con los numeros creados por las operaciones 
        iban="ES"+str(numerosiban)+cuenta
        return iban

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CCCWidget()
    mainWindow.show()
    sys.exit(app.exec())
