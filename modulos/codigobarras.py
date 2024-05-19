from PyQt6.QtWidgets import QToolTip, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys, requests,json

class BarraWidget(QWidget):
    """
        Clase que crea un widget con los atributos especiales y genera
        codigo de barras UPC o EAN
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self,idioma):
        super().__init__()
        """
            Inicia el widget y sus componentes mas las propiedades
        Args:
            idiomas (String): Recoge el idioma la cual el widget estara traducido
        """      
        #Selecciona el idioma del JSON y el widget
        self.idioma = idioma
        with open('./idiomas/codigobarras.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        #Creamos los elementos del widget
        self.label = QLabel(self.datas["CodigoBarras"], self)
        self.editline = QLineEdit(self)
        self.UPC = QCheckBox("UPC")

        #propiedades de los componentes
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.UPC.setChecked(True)
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos el layout al qframe
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #Agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        layout.addWidget(self.UPC,1,0)
        
        #Establecemos layout al widget
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
        self.UPC.enterEvent = self.showHelpUPC
        self.UPC.leaveEvent = self.HideHelpUPC
    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        # Cambia el idioma del parámetro
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]

        # Cambia los valores del widget
        self.label.setText(self.datas["CodigoBarras"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
    def showHelpUPC(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Mostrar un widget emergente personalizado cuando el mouse entra en el checkbox
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.UPC.mapToGlobal(self.UPC.rect().center()), tooltip_text)

    def HideHelpUPC(self, event):
        """
            Esconde el QToolTip al salir del widget con el raton
        Args:
            event (QEvent): El evento que activa la escondida del tooltip.
        """
        # Ocultar el widget emergente cuando el mouse sale del checkbox
        QToolTip.hideText()

    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """        
        #comprueba que el usuario a rellenado el editline sino pongo uno default
        titulo = self.editline.text() or self.datas["CodigoBarras"]
        codigos = {}
        #conecta a la rest api
        url = f"http://localhost:5000/codigobarras/{int(self.UPC.isChecked())}/{cantidad}"
        response = requests.get(url)
        data = response.json()
        #devuelve el diccionario
        codigos[titulo] = data["barra"]
        return codigos



if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = BarraWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())