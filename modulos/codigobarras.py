from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys
class BarraWidget(QWidget):
    def __init__(self):
        super().__init__()
        #Creamos los elementos del widget
        self.label = QLabel("CodigoBarras:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox("En proceso")
        self.editline.setPlaceholderText("Nombre Proyecto")
        
        
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
        layout.addWidget(self.check,1,0)
        
        #Establecemos layout al widget
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = BarraWidget()
    mainWindow.show()
    sys.exit(app.exec())