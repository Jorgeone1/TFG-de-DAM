from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys, random,string
class ISBNWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.idioma = "EN"
        #creamos los elemento del widget
        self.label = QLabel("ISBN:", self)
        self.editline = QLineEdit(self)
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
        
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "ISBN"
    def generarISBN(self):
        codigopais = ""
        if self.idioma == "ES":
            codigopais = "84"
        if self.idioma =="EN":
            codigopais = random.choice(["00","01"])
        isb = random.choice(["978","979"]) + "-"+ codigopais +"-"+"".join(random.choices(string.digits,k = 5)) + "-" + "".join(random.choices(string.digits,k=2))
        isbn = isb.replace("-","")
        suma = 0
        for i in range(0,len(isbn)):
            if i % 2 == 0:
                suma += int(isbn[i])
            else:
                suma += int(isbn[i]) * 3
        isb +="-" + str(10-(suma%10))
        print(isb)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ISBNWidget()
    mainWindow.generarISBN()
    mainWindow.show()
    sys.exit(app.exec())