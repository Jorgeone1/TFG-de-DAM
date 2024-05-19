from PyQt6.QtWidgets import QWidget, QToolTip,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests,json
class IPWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de IP, del protocolo IPv4 o IPv6  
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
        with open('./idiomas/ip.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creación de los elementos del widget
        self.label = QLabel("IP:", self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.ip6 = QCheckBox("IPv6", self)

        # Asignar eventos para mostrar y ocultar tooltips
        self.ip6.enterEvent = self.showHelpIPV6
        self.ip6.leaveEvent = self.hideHelp

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)
        layout.addWidget(self.ip6, 1, 0)
        
        # Establecemos layout
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)

    def showHelpIPV6(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.ip6.mapToGlobal(self.ip6.rect().center()), tooltip_text)

    def hideHelp(self, event):
        """
        Oculta el QToolTip
        Args:
            event (QEvent): El evento que activa la ocultación del tooltip.
        """
        QToolTip.hideText()

    def traducir(self, nuevo_idioma):
        """
        Método para traducir el contenido del widget al nuevo idioma
        Args:
            nuevo_idioma (str): Nuevo idioma al cual se traducirá el contenido del widget
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]

        # Actualizar los textos de los elementos del widget
        self.label.setText("IP:")
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.ip6.setText("IPv6")

        # Actualizar los tooltips
        self.ip6.setToolTip(self.datas["ayuda1"])
        
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que este el editline tenga texto sino pone uno default
        titulo = self.editline.text() or "IP"
        #Accede con un protocolo GET al Rest API
        url = f"http://localhost:5000/IP/{int(self.ip6.isChecked())}/{cantidad}"
        response = requests.get(url)
        data = response.json()
        #devuelve los datos
        return {titulo:data["ip"]}
if __name__ == "__main__":  
    app = QApplication(sys.argv)
    mainWindow = IPWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())