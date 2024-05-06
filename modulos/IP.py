from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys
class IPWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creacion de los elementos del widget
        self.label = QLabel("IP:", self)
        self.editline = QLineEdit(self)
        self.ip4 = QCheckBox("IPV4")
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
        layout.addWidget(self.ip4,1,0)
        layout.addWidget(self.ip6,1,1)
        
        #establecemos layout
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = IPWidget()
    mainWindow.show()
    sys.exit(app.exec())