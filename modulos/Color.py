from PyQt6.QtWidgets import QWidget, QToolTip,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests,json
from PIL import ImageColor

class ColorWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, Clase que genera colores aleatorios en modo HEX o en RGB 
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
        #Guarda el idioma y abre el json   
        self.idioma = idioma
        with open('./idiomas/color.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        #Creamos los elementos del widget
        self.label = QLabel(self.datas["color"], self)
        self.editline = QLineEdit(self)
        self.Hex = QCheckBox(self.datas["nohex"])
        self.rgb = QCheckBox("RGB")
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.rgbline = QLineEdit()
        self.rgbline.setPlaceholderText(self.datas["nombrergb"])
        self.Hex.setEnabled(False)
        self.rgbline.setEnabled(False)

        self.rgb.stateChanged.connect(self.__bloquearHex)
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        self.Hex.enterEvent = self.showHelpNoHEX
        self.rgb.enterEvent = self.showHelpRGB
        self.Hex.leaveEvent = self.HideHelp
        self.rgb.leaveEvent = self.HideHelp
        #Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al QFrame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,2)
        layout.addWidget(self.Hex,1,1)
        layout.addWidget(self.rgb,1,0)
        layout.addWidget(self.rgbline,2,0,1,2)
        
        #establecemos un layout al Principal
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]
        
        # Actualizar los textos de los elementos del widget
        self.label.setText(self.datas["color"])
        self.Hex.setText(self.datas["nohex"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.rgbline.setPlaceholderText(self.datas["nombrergb"])

    def __bloquearHex(self,state):
        """
            Bloquea el boton de no Hex para evitar errores
        Args:
            state (int): Comprueba el estado del checkbox
        """        
        if state == 2:
            self.Hex.setEnabled(True)
            self.rgbline.setEnabled(True)
        else:
            #deja en false por si estaba checkeado antes de despulsar el checkbox de rgb
            self.Hex.setEnabled(False)
            self.Hex.setChecked(False)
            self.rgbline.setEnabled(False)
    def showHelpRGB(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Mostrar un widget emergente personalizado cuando el mouse entra en el checkbox
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.rgb.mapToGlobal(self.rgb.rect().center()), tooltip_text)
    def showHelpNoHEX(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Mostrar un widget emergente personalizado cuando el mouse entra en el checkbox
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.Hex.mapToGlobal(self.Hex.rect().center()), tooltip_text)
    def HideHelp(self, event):
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
        titulo = self.editline.text() or self.datas["color"]
        rgb = self.rgbline.text() or "RGB"
        colores = {}
        url = f"http://localhost:5000/color/{cantidad}"
        response = requests.get(url)
        data = response.json()
        #comprueba si esta checkeado o no
        if self.rgb.isChecked():
            colores[rgb] = data["rgb"]
            if not self.Hex.isChecked():
                colores[titulo] = data["hex"]
        else:
            colores[titulo] = data["hex"]
        return colores



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ColorWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())