from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class CorreoWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creamos los elementos del widget
        self.label = QLabel("Correo:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox("Conectar Nombre")
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.dominioe = QLineEdit()
        self.dominiol = QLabel("Dominio")
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #Establecemos el layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,2)
        layout.addWidget(self.dominiol,1,0)
        layout.addWidget(self.dominioe,1,1)
        layout.addWidget(self.check,1,2)

        #establecemos el layout principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CorreoWidget()
    mainWindow.show()
    sys.exit(app.exec())
