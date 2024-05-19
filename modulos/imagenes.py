from PyQt6.QtWidgets import QWidget, QToolTip, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys, requests,random, json
from modulos import error
class ImagenesWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, ademas devuelve con scrapping links de imagenes 
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self, idiomas):
        super().__init__()
        """
        Inicia el widget y sus componentes más las propiedades
        Args:
            idiomas (String): Recoge el idioma en el cual el widget estará traducido
        """
        # Guardamos el idioma y abrimos el json
        self.idioma = idiomas
        with open('./idiomas/imagenes.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        
        # Creamos los elementos del widget
        self.label = QLabel(self.datas["img"] + ":", self)
        self.editline = QLineEdit(self)
        self.obligatorio = QLabel(self.datas["buscador"], self)
        self.Buscador = QLineEdit()
        
        #propiedades de los widget
        self.Buscador.setPlaceholderText(self.datas["Obligatorio"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.obligatorio.enterEvent = self.showHelpBuscador
        self.obligatorio.leaveEvent= self.hideHelp
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos elementos al layout
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)
        layout.addWidget(self.obligatorio, 1, 0)
        layout.addWidget(self.Buscador, 1, 1)
        
        # Establecemos layout
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
    def showHelpBuscador(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.obligatorio.mapToGlobal(self.obligatorio.rect().center()), tooltip_text)

    def hideHelp(self, event):
        """
        Oculta el QToolTip
        Args:
            event (QEvent): El evento que activa la ocultación del tooltip.
        """
        QToolTip.hideText() 

    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]
        self.label.setText(self.datas["img"] + ":")
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.obligatorio.setText(self.datas["buscador"])
        self.Buscador.setPlaceholderText(self.datas["Obligatorio"])
    
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que el texto tengo algo y si no pone uno default
        titulo = self.editline.text() or self.datas["img"]
        if not self.Buscador.text().strip():
            raise error.ErrorPrograma(self.datas["error1"])
        #Accedemos a la restApi
        url = f"http://localhost:5000/imagenes/{self.Buscador.text()}"
        response = requests.get(url)
        data = response.json()
        img = data["imagenes"]
        #Comprueba que haya mas de 3 busquedas sino lanzara un error
        if len(img) < 3:
            raise error.ErrorPrograma(self.datas["error2"] + self.Buscador.text())
        #envia el diccionario con datos duplicados 
        dicts = {}
        lis = random.choices(img,k=cantidad)
        dicts[titulo] = lis
        return dicts
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ImagenesWidget()
    mainWindow.show()
    sys.exit(app.exec())