from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QFrame
import sys
import random
class BoolWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Creamos los elementos del widget
        self.label = QLabel("Booleanos:", self)
        self.editline = QLineEdit(self)
        self.truelab = QLabel("True:")
        self.falselab = QLabel("False:")
        self.opcional = QLabel("Opcional:")
        self.edittrue = QLineEdit()
        self.edittrue.setPlaceholderText("Nombre True")
        self.editfalse = QLineEdit()
        self.editfalse.setPlaceholderText("Nombre False")
        self.editline.setPlaceholderText("Nombre Proyecto")

        # Creamos un QFrame
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        
        # Establecemos el layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        # Agregamos los elementos al layout del QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1, 1, 3)
        frame_layout.addWidget(self.opcional, 1, 0)
        frame_layout.addWidget(self.truelab, 2, 0)
        frame_layout.addWidget(self.edittrue, 2, 1)
        frame_layout.addWidget(self.falselab, 2, 2)
        frame_layout.addWidget(self.editfalse, 2, 3)

        # Establecemos el layout principal del widget
        layout = QGridLayout(self)
        layout.addWidget(self.frame)
    def getData(self,cantidad):
        truename = self.edittrue.text()
        falsename = self.editfalse.text()
        titulo = self.editline.text()
        if not truename:
            truename = "True"
        if not falsename:
            falsename = "False"
        if not titulo:
            titulo = "Booleanos"
        booleanos = {}
        lista = []
        for i in range(cantidad):
            sel = random.choice([True,False])
            if sel:
                lista.append(truename)
            else:
                lista.append(falsename)
        booleanos[titulo] = lista
        return lista
                
                    
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = BoolWidget()
    mainWindow.show()
    sys.exit(app.exec())