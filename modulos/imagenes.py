from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys, requests,random
from bs4 import BeautifulSoup
class ImagenesWidget(QWidget):
    def __init__(self):
        super().__init__()
        
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
        img = self.getImagenes()
        dicts = {}
        lis = random.choices(img,k=cantidad)
        dicts[titulo] = lis
        return dicts
    def getImagenes(self):

        urls = [f'https://unsplash.com/es/s/fotos/{self.Buscador.text()}',f"https://stock.adobe.com/es/search?k={self.Buscador.text()}&search_type=usertyped"
               ,f"https://depositphotos.com/es/photos/{self.Buscador.text()}.html?filter=all"
               ]
        lista = []
        for url in urls:
            # Realiza una solicitud HTTP para obtener el contenido de la página
            response = requests.get(url)
            
            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Parsea el contenido HTML de la página
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Encuentra todas las etiquetas "img" en la página
                img_tags = soup.find_all('img')
                hola = ""
                
                # Itera a través de las etiquetas "img" y obtén el atributo "src"
                for img_tag in img_tags:
                    src = img_tag.get('src')
                    if src:
                        if "secure" not in src and "betrad" not in src:
                            print(src)
                            lista.append(src)
                        
            else:
                print("No se pudo acceder a la página")
        return lista
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ImagenesWidget()
    mainWindow.show()
    sys.exit(app.exec())