from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class ColorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #Creamos los elementos del widget
        self.label = QLabel("Color:", self)
        self.editline = QLineEdit(self)
        self.Hex = QCheckBox("HEX")
        self.rgb = QCheckBox("RGB")
        self.rgba = QCheckBox("RGBA")
        self.editline.setPlaceholderText("Nombre Proyecto")

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al QFrame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,2)
        layout.addWidget(self.Hex,1,0)
        layout.addWidget(self.rgb,1,1)
        layout.addWidget(self.rgba,1,2)
        
        #establecemos un layout al Principal
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ColorWidget()
    mainWindow.show()
    sys.exit(app.exec())