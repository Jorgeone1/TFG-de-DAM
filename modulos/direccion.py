from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests
class DireccionWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma
        #creamos los elementos de widget
        self.label = QLabel("Direccion:", self)
        self.editline = QLineEdit(self)
        self.COP = QCheckBox("Codigo Postal")
        self.ciudad = QCheckBox("Comunidad Autonoma")
        self.Provincia = QCheckBox("Provincia")
        self.editline.setPlaceholderText("Nombre Proyecto")

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos in layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #añadimos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,3)
        layout.addWidget(self.ciudad,1,2)
        layout.addWidget(self.COP,1,0)
        layout.addWidget(self.Provincia,1,1)
        
        #establecemos layout al principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)

    def getData(self,cantidad):
        titulo = self.editline.text() or "Direccion"
        url = f'http://127.0.0.1:5000/direccion/{self.idioma}/{cantidad}'
        response = requests.get(url)
        data = response.json()
        direcci = {}
        direcci[titulo] = data["direccion"]
        if self.COP.isChecked():
            direcci["Codigo Postal"] = data["Codigo"]
        if self.ciudad.isChecked():
            direcci["Ciudad"] = data["Provincia"]
        if self.Provincia.isChecked():
            direcci["Provincia"] = data["ciudad"]
        return direcci
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DireccionWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())
