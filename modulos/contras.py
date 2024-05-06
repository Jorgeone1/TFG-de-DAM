import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QCheckBox, QFrame
import string
import random
import hashlib
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
        titulo = self.editline.text()
        hashn = self.nombrehash.text()
        if self.cantidad.text() == "":
            return
        if not titulo:
            titulo = "Contraseña"
        if not hashn:
            hashn = "Hash"
        Base = list(string.ascii_lowercase)
        
        list_password = [Base]
        lista = []
        hash = []
        passwords = {}
        # Array con todas las letras del abecedario en mayúscula
        if self.mayus.isChecked():
            uppercase_letters = list(string.ascii_uppercase)
            list_password.append(uppercase_letters)
        
        # Array con los números del 0 al 9
        if self.numeros.isChecked():
            numbers = list(string.digits)
            list_password.append(numbers)
        
        # Array con teclas especiales comunes
        if self.especial.isChecked():
            special_keys = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
            list_password.append(special_keys)
        
        for i in range(cantidad):
            text = ""
            for j in range(int(self.cantidad.text())):
                passs = random.choice(list_password)
                text = text + random.choice(passs)
            if self.hashchech.isChecked():
                hashh = self.__hash_password(text)
                hash.append(hashh)
            lista.append(text)
        passwords[titulo] = lista
        if self.hashchech.isChecked():
            passwords[hashn] = hash
        return passwords
    def __hash_password(self,password):
        # Convertir la contraseña a bytes
        password_bytes = password.encode('utf-8')

        # Crear un objeto hash usando SHA-256
        hash_object = hashlib.sha256()

        # Actualizar el objeto hash con la contraseña
        hash_object.update(password_bytes)

        # Obtener el hash resultante en formato hexadecimal
        hashed_password = hash_object.hexdigest()

        return hashed_password

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ContraWidget()
    mainWindow.show()
    sys.exit(app.exec())

