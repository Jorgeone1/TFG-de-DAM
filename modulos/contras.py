import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QCheckBox, QFrame
import requests

class ContraWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Creamps los elementos del widget
        self.label = QLabel("Contrase:", self)
        self.editline = QLineEdit(self)
        self.numeros = QCheckBox("Numeros")
        self.especial = QCheckBox("Teclas Especiales")
        self.mayus = QCheckBox("Mayusculas")
        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText("longitud contraseña")
        self.hashchech = QCheckBox("Hash")
        self.nombrehash = QLineEdit()
        self.nombrehash.setPlaceholderText("Nombre de la columna del hash")
        self.nombrehash.setEnabled(False)
        self.hashchech.stateChanged.connect(self.bloquearHash)
        
        # Crear un QFrame
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        
        # Establecemos el layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        # Agregamos los elementos al layout del QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1, 1, 2)
        frame_layout.addWidget(self.numeros, 1, 0)
        frame_layout.addWidget(self.especial, 1, 1)
        frame_layout.addWidget(self.cantidad, 2, 0, 1, 3)
        frame_layout.addWidget(self.mayus, 1, 2)
        frame_layout.addWidget(self.hashchech,3,0)
        frame_layout.addWidget(self.nombrehash,3,1,1,2)
        
        # Establecemos el layout principal del widget
        layout = QGridLayout(self)
        layout.addWidget(self.frame)
    def bloquearHash(self,state):
        if state == 2:  # 2 significa que el CheckBox está marcado
            self.nombrehash.setEnabled(True)
        else:
            self.nombrehash.setEnabled(False)

    def getData(self, cantidad):
        # Array con todas las letras del abecedario en minúscula
        titulo = self.editline.text() or "Contraseña"
        hashn = self.nombrehash.text() or "Hash"
        url = f"http://127.0.0.1:5000/contra/{cantidad}/{self.cantidad.text()}/{int(self.mayus.isChecked())}/{int(self.numeros.isChecked())}/{int(self.especial.isChecked())}"
        response = requests.get(url)
        data = response.json()
        dicts ={}
        dicts[titulo] = data["Contra"]
        if self.hashchech.isChecked():
            dicts[hashn] = data["hash"]
        return dicts

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ContraWidget()
    mainWindow.show()
    sys.exit(app.exec())

