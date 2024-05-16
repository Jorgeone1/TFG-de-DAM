import random
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests
class TelefonoWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma 
        #creamos elementos del widget
        self.label = QLabel("Telefono:", self)
        self.editline = QLineEdit(self)
        self.tele = QCheckBox("Telefono")
        self.tele.stateChanged.connect(self.bloquearMobil)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.teleName = QLineEdit()
        self.teleName.setPlaceholderText("Nombre telefono")
        self.sinmobil = QCheckBox("Sin mobil")
        self.sinmobil.setEnabled(False)
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,2)
        layout.addWidget(self.tele,1,0)
        layout.addWidget(self.teleName,1,1)
        layout.addWidget(self.sinmobil,1,2)
        
        widgetcreados = QGridLayout(self)
        widgetcreados.addWidget(self.frame)
    
    def bloquearMobil(self,state):
        if state == 2:
            self.sinmobil.setEnabled(True)
        else:
            self.sinmobil.setEnabled(False)
            self.sinmobil.setChecked(False)
    
    def getData(self,cantidad):
        fijo = self.editline.text() or "Fijo"
        mobil = self.teleName.text() or "Mobil"
        url = f"http://localhost:5000/telefono/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        dicts ={}
        if self.tele.isChecked():
            if self.sinmobil.isChecked():
                dicts[fijo] = data["fijo"]
            else:
                dicts[fijo] = data["fijo"]
                dicts[mobil]=data["mobil"]
        else:
            dicts[mobil]=data["mobil"]
        return dicts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = TelefonoWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())


        