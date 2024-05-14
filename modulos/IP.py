from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
import random
class IPWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creacion de los elementos del widget
        self.label = QLabel("IP:", self)
        self.editline = QLineEdit(self)
        self.ip6 = QCheckBox("IPV6")
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
        layout.addWidget(self.ip6,1,1)
        
        #establecemos layout
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "IP"
        lista = []
        ips = {}
        for i in range(cantidad):
            if self.ip6.isChecked():
                lista.append(self.__crearIPV6())
            else:
                lista.append(self.__crearIPV4())
        ips[titulo] = lista
        return ips

    def __crearIPV4(self):
        ipv4 = []
        for i in range(4):
            ipv4.append(str(random.randint(0,255)))
        return ".".join(ipv4)
    
    def __crearIPV6(self):
        ipv6 = []
        lista = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","F"]
        for i in range(8):
            digito = ""
            for k in range(4):
                digito = digito + random.choice(lista)
            ipv6.append(digito)
        return ":".join(ipv6)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = IPWidget()
    mainWindow.show()
    sys.exit(app.exec())