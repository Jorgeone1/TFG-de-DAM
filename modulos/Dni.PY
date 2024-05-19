from PyQt6.QtWidgets import QWidget, QToolTip, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests, json
class DNIWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, ademas genera una lista de dni o nie falsos verificados 
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self, idioma):
        super().__init__()
        """
        Inicia el widget y sus componentes más las propiedades
        Args:
            idioma (str): Recoge el idioma en el cual el widget estará traducido
        """
        # Guardamos el idioma y abrimos el json
        self.idioma = idioma
        with open('./idiomas/dni.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del Widget
        self.label = QLabel(self.datas["Dni"], self)
        self.editline = QLineEdit(self)
        self.Nie = QCheckBox(self.datas["NIE"], self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])

        # Asignar eventos para mostrar y ocultar tooltips
        self.Nie.enterEvent = self.showHelpNIE
        self.Nie.leaveEvent = self.hideHelp

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Agregamos el layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)
        layout.addWidget(self.Nie, 1, 0)

        # Agregamos layout al widget principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)

    def showHelpNIE(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.Nie.mapToGlobal(self.Nie.rect().center()), tooltip_text)

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

        # Actualizar los textos de los elementos del widget
        self.label.setText(self.datas["Dni"])
        self.Nie.setText(self.datas["NIE"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])

        # Actualizar los tooltips
        self.Nie.setToolTip(self.datas["ayuda1"])
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que editline tiene texto sino, lo sustituye por uno default
        titulo = self.editline.text() or "DNI" 
        if self.Nie.isChecked() and titulo == "DNI":
            titulo = "NIE"
        #conecta con el servidor REST API
        url = f"http://127.0.0.1:5000/dni/{cantidad}/{int(self.Nie.isChecked())}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        dnis = {}        
        #Envia el diccionario
        dnis[titulo] = data["dni"]
        return dnis

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DNIWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())


