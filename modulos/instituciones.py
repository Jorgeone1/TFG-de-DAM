from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class InstitucionesWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creamos los elementos del widget 
        self.label = QLabel("Instituciones:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox("En proceso")
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
        
        #establecemois laoyut
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = InstitucionesWidget()
    mainWindow.show()
    sys.exit(app.exec())