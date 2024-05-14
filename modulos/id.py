from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class idWidget(QWidget):
    def __init__(self):
        super().__init__()

        #creamos los elementos del widget        
        self.label = QLabel("ID:", self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.empezar = QLineEdit(self)
        self.empezar.setPlaceholderText("Opcional")
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
        layout.addWidget(self.empezar,1,0,1,2)
        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "ID"
        numero = self.empezar.text() or 0
        numero = int(numero)
        lista = []
        ids = {}
        for i in range(0,cantidad):
            numero = numero + i
            lista.append(numero)
        ids[titulo] = lista
        return ids
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = idWidget()
    mainWindow.show()
    sys.exit(app.exec())