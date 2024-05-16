from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys, requests,random
from bs4 import BeautifulSoup
class ImagenesWidget(QWidget):
    def __init__(self,idiomas):
        super().__init__()
        self.idioma = idiomas
        #creamos los elementos del widget
        self.label = QLabel("Imagenes:", self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.obligatorio = QLabel("Obligatorio:")
        self.Buscador = QLineEdit()
        self.Buscador.setPlaceholderText("Buscador")
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos elementos al layout
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.obligatorio,1,0)
        layout.addWidget(self.Buscador,2,0,1,2)
        #establecemos layout
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "Imagenes"
        url = f"http://localhost:5000/imagenes/{self.Buscador.text()}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        img = data["imagenes"]
        print(len(img))
        dicts = {}
        lis = random.choices(img,k=cantidad)
        dicts[titulo] = lis
        return dicts
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ImagenesWidget()
    mainWindow.show()
    sys.exit(app.exec())