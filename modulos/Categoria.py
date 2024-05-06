from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QFrame, QCheckBox
import sys

class CategoriaWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Creamos los elementos del widget
        self.label = QLabel("Categoria:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox("En pruebas")

        # Creamos un QFrame
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        
        # Establecemos el layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        # Agregamos los elementos al layout del QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1)
        frame_layout.addWidget(self.check, 1, 0)

        # Establecemos el layout principal del widget
        layout = QGridLayout(self)
        layout.addWidget(self.frame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CategoriaWidget()
    mainWindow.show()
    sys.exit(app.exec())
