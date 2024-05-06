from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class DeporteWidget(QWidget):
    def __init__(self):
        super().__init__()
        #creamos los elementos del widget
        self.label = QLabel("Deporte:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox("EN CONSTRUCCION")
        self.editline.setPlaceholderText("Nombre Proyecto")

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #Establecemos layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #Agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.check,1,0)
        
        #establecemos el layout del widget
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DeporteWidget()
    mainWindow.show()
    sys.exit(app.exec())