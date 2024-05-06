from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys
class ProductoWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creamos los elementos del widget
        self.label = QLabel("Producto:", self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.check = QCheckBox("En creacion")
        
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
        
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ProductoWidget()
    mainWindow.show()
    sys.exit(app.exec())