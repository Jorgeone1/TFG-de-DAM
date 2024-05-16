from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys, random,requests
import sqlite3 as sq
class CocheWidget(QWidget):
    def __init__(self,idiomas):
        super().__init__()
        self.idioma =idiomas
        #Creamos los elementos del Widget
        self.label = QLabel("Coche:", self)
        self.editline = QLineEdit(self)
        self.Marca = QCheckBox("Marca")
        self.Tipo = QCheckBox("Tipo")
        self.Marca.stateChanged.connect(self.bloquearMarca)
        self.Tipo.stateChanged.connect(self.bloquearTipo)
        self.marcno = QLineEdit()
        self.tipono = QLineEdit()
        self.marcno.setPlaceholderText("Marca nombre")
        self.tipono.setPlaceholderText("Tipo Nombre")
        self.marcno.setEnabled(False)
        self.tipono.setEnabled(False)
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
        frame_layout.addWidget(self.marcno,1,1)
        frame_layout.addWidget(self.Tipo,2,0)
        frame_layout.addWidget(self.tipono,2,1)
        
        #Establecemos un layout al widget y añadimos el frame
        widget_lat = QGridLayout(self)
        widget_lat.addWidget(self.frame)
        
    def bloquearMarca(self,state):
        if state == 2:
            self.marcno.setEnabled(True)
        else:
            self.marcno.setEnabled(False)
    def bloquearTipo(self,state):
        if state == 2:
            self.tipono.setEnabled(True)
        else:
            self.tipono.setEnabled(False)
    def getData(self,cantidad):
        titulo = self.editline.text() or "Coches"
        mar = self.marcno.text() or "Marca"
        ti = self.tipono.text() or "Tipo"
        dicts = {}
        url = f"http://localhost:5000/coches/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        dicts[titulo] = data["modelo"]
        if self.Tipo.isChecked():
            dicts[ti] = data["tipo"]
        if self.Marca.isChecked():
            dicts[mar] = data["marca"]
        return dicts
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CocheWidget()
    mainWindow.generarCoches()
    mainWindow.show()
    sys.exit(app.exec())