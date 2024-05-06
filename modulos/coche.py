from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys
class CocheWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #Creamos los elementos del Widget
        self.label = QLabel("Coche:", self)
        self.editline = QLineEdit(self)
        self.Marca = QCheckBox("Marca")
        self.Tipo = QCheckBox("Tipo")
        self.editline.setPlaceholderText("Nombre Proyecto")

        # Creamos un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        #Establecemos un layout al QFrame
        frame_layout = QGridLayout()

        #Agregamos los elementos al QFrame
        self.frame.setLayout(frame_layout)
        frame_layout.addWidget(self.label,0,0)
        frame_layout.addWidget(self.editline,0,1,1,1)
        frame_layout.addWidget(self.Marca,1,0)
        frame_layout.addWidget(self.Tipo,1,1)
        
        #Establecemos un layout al widget y añadimos el frame
        widget_lat = QGridLayout(self)
        widget_lat.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CocheWidget()
    mainWindow.show()
    sys.exit(app.exec())