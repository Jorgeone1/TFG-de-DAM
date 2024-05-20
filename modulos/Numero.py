from PyQt6.QtWidgets import QWidget, QComboBox, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QToolTip,QFrame
import sys,random,json, requests
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from modulos import error
class NumeroWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de numeros aleatorios, con o sin decimales
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self, idiomas):
        """
        Inicia el widget y sus componentes más las propiedades
        Args:
            idiomas (str): Recoge el idioma en el cual el widget estará traducido
        """      
        super().__init__()
        # Guardamos el idioma y abrimos el json
        self.idioma = idiomas
        with open('./idiomas/numero.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["numeros"], self)
        self.editline = QLineEdit(self)
        self.entero = QCheckBox(self.datas["Entero"], self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.minimoe = QLineEdit()
        # Crear un QRegularExpressionValidator
        regex = QRegularExpression(r'^-?\d{0,7}(\.\d{0,2})?$')
        regexvalidator = QRegularExpressionValidator(regex)
        self.minimoe.setValidator(regexvalidator)
        self.maximoe = QLineEdit()
        self.maximoe.setValidator(regexvalidator)
        self.minimoe.setPlaceholderText(self.datas["obligatorio"])
        self.maximoe.setPlaceholderText(self.datas["obligatorio"])
        
        self.minimol = QLabel(self.datas["minimo"], self)
        self.maximol = QLabel(self.datas["maximo"], self)
        self.labeldecimal = QLabel(self.datas["decimales"], self)
        self.decimales = QComboBox()
        self.decimales.addItems(["1", "2", "3", "4", "5"])

        # Asignar eventos para mostrar y ocultar tooltips
        self.entero.enterEvent = self.showHelpEntero
        self.entero.leaveEvent = self.hideHelp
        self.labeldecimal.enterEvent = self.showHelpDecimales
        self.labeldecimal.leaveEvent = self.hideHelp

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1, 1, 4)
        layout.addWidget(self.minimol, 2, 0)
        layout.addWidget(self.minimoe, 2, 1)
        layout.addWidget(self.maximol, 2, 2)
        layout.addWidget(self.maximoe, 2, 3)
        layout.addWidget(self.entero, 1, 0)
        layout.addWidget(self.labeldecimal, 1, 2)
        layout.addWidget(self.decimales, 1, 3)

        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)

    def getData(self, cantidad):
        """
        Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        try:
            titulo = self.editline.text() or "Número"
            dicts = {}
            if self.minimoe.text() == "" or self.maximoe.text() == "" or self.minimoe.text() == "-" or self.maximoe.text() == "-" or self.minimoe.text() == "." or self.maximoe.text() == ".":
                raise ValueError(self.datas["error1"])
            
            url = f"http://localhost:5000/numeros/{int(self.entero.isChecked())}/{self.minimoe.text()}/{self.maximoe.text()}/{self.decimales.currentText()}/{cantidad}"
            response = requests.get(url)
            data = response.json()
            print(data)
            if len(data["numeros"]) != cantidad:
                raise ValueError(self.datas["error1"])
            dicts[titulo] = data["numeros"]
            return dicts
        except ValueError:
            raise ValueError(self.datas["error1"])

    def showHelpEntero(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.entero.mapToGlobal(self.entero.rect().center()), tooltip_text)

    def hideHelp(self, event):
        """
        Oculta el QToolTip
        Args:
            event (QEvent): El evento que activa la ocultación del tooltip.
        """
        QToolTip.hideText()

    def showHelpDecimales(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.labeldecimal.mapToGlobal(self.labeldecimal.rect().center()), tooltip_text)

    def traducir(self, nuevo_idioma):
        """
        Método para traducir el contenido del widget al nuevo idioma
        Args:
            nuevo_idioma (str): Nuevo idioma al cual se traducirá el contenido del widget
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]

        # Actualizar los textos de los elementos del widget
        self.label.setText(self.datas["numeros"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.entero.setText(self.datas["Entero"])
        self.minimoe.setPlaceholderText(self.datas["obligatorio"])
        self.maximoe.setPlaceholderText(self.datas["obligatorio"])
        self.minimol.setText(self.datas["minimo"])
        self.maximol.setText(self.datas["maximo"])
        self.labeldecimal.setText(self.datas["decimales"])

        # Actualizar los tooltips
        self.entero.setToolTip(self.datas["ayuda1"])
        self.labeldecimal.setToolTip(self.datas["ayuda2"])
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        try:
            titulo = self.editline.text() or "Número"
            dicts = {}
            if self.minimoe.text() == "" or self.maximoe.text()==""  or self.minimoe.text() == "-" or self.maximoe.text()=="-" or self.minimoe.text() == "." or self.maximoe.text()==".":
                raise error.ErrorPrograma("Hay que poner datos validos")
            
            url = f"http://localhost:5000/numeros/{int(self.entero.isChecked())}/{self.minimoe.text()}/{self.maximoe.text()}/{self.decimales.currentText()}/{cantidad}"
            response = requests.get(url)
            data = response.json()
            if len(data["numeros"]) != cantidad:
                raise error.ErrorPrograma("Error en los datos introducidos")
            dicts[titulo] = data["numeros"]
            return dicts
        except ValueError:
            error.ErrorPrograma("Tiene que ser un Numero Valido")
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = NumeroWidget()
    mainWindow.show()
    sys.exit(app.exec())