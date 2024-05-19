import sys
from PyQt6.QtWidgets import QToolTip, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QCheckBox, QFrame
import requests,json
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from modulos import error
class ContraWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, ademas envia una lista de contraseña con los simbolos saleccionados y en hash 
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
        # Guarda el idioma y abre el json   
        self.idioma = idioma
        with open('./idiomas/contra.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        
        # Creamos los elementos del widget
        self.label = QLabel(self.datas["contra"], self)
        self.editline = QLineEdit(self)
        self.numeros = QCheckBox(self.datas["numeros"], self)
        self.especial = QCheckBox(self.datas["TeclasEs"], self)
        self.mayus = QCheckBox(self.datas["mayus"], self)
        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText(self.datas["longitud"])
        self.hashchech = QCheckBox("Hash")
        self.nombrehash = QLineEdit()
        regex = QRegularExpression(r'^\d{0,2}$')
        validator = QRegularExpressionValidator(regex)
        self.nombrehash.setPlaceholderText(self.datas["nombrehash"])
        self.nombrehash.setEnabled(False)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.hashchech.stateChanged.connect(self.bloquearHash)
        self.numeros.enterEvent = self.showHelpNumeros
        self.numeros.leaveEvent = self.hideHelp
        self.especial.enterEvent = self.showHelpTeclasEs
        self.especial.leaveEvent = self.hideHelp
        self.mayus.enterEvent = self.showHelpMayus
        self.mayus.leaveEvent = self.hideHelp
        self.hashchech.enterEvent = self.showHelpHash
        self.hashchech.leaveEvent = self.hideHelp
        self.cantidad.setValidator(validator)
        # Crear un QFrame
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        
        # Establecemos el layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        # Agregamos los elementos al layout del QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1, 1, 2)
        frame_layout.addWidget(self.numeros, 1, 0)
        frame_layout.addWidget(self.especial, 1, 1)
        frame_layout.addWidget(self.cantidad, 2, 0, 1, 3)
        frame_layout.addWidget(self.mayus, 1, 2)
        frame_layout.addWidget(self.hashchech, 3, 0)
        frame_layout.addWidget(self.nombrehash, 3, 1, 1, 2)
        
        # Establecemos el layout principal del widget
        layout = QGridLayout(self)
        layout.addWidget(self.frame)
    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]
        
        # Actualizar los textos de los elementos del widget
        self.label.setText(self.datas["contra"])
        self.numeros.setText(self.datas["numeros"])
        self.especial.setText(self.datas["TeclasEs"])
        self.mayus.setText(self.datas["mayus"])
        self.cantidad.setPlaceholderText(self.datas["longitud"])
        self.nombrehash.setPlaceholderText(self.datas["nombrehash"])
        
        # Actualizar los tooltips
        self.numeros.setToolTip(self.datas["ayuda1"])
        self.especial.setToolTip(self.datas["ayuda3"])
        self.mayus.setToolTip(self.datas["ayuda2"])
        self.hashchech.setToolTip(self.datas["ayuda4"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
    def bloquearHash(self,state):
        """
            Método que bloquea el CheckBox de hash
        Args:
            state (int): el estado del checkbox
        """        
        if state == 2:  # 2 significa que el CheckBox está marcado
            self.nombrehash.setEnabled(True)
        else:
            self.nombrehash.setEnabled(False)
    def showHelpNumeros(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.numeros.mapToGlobal(self.numeros.rect().center()), tooltip_text)

    def showHelpTeclasEs(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.especial.mapToGlobal(self.especial.rect().center()), tooltip_text)

    def showHelpMayus(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.mayus.mapToGlobal(self.mayus.rect().center()), tooltip_text)

    def showHelpHash(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda4"]
        QToolTip.showText(self.hashchech.mapToGlobal(self.hashchech.rect().center()), tooltip_text)

    def hideHelp(self, event):
        """
        Oculta el QToolTip
        Args:
            event (QEvent): El evento que activa la escondida del tooltip.
        """
        QToolTip.hideText()
    def getData(self, cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        # Array con todas las letras del abecedario en minúscula
        titulo = self.editline.text() or self.datas["contra"]
        hashn = self.nombrehash.text() or "Hash"
        if not self.cantidad.text():
            raise error.ErrorPrograma("Tienes que poner una cantidad en las contraseña")
        #accede al rest Api
        url = f"http://127.0.0.1:5000/contra/{cantidad}/{self.cantidad.text()}/{int(self.mayus.isChecked())}/{int(self.numeros.isChecked())}/{int(self.especial.isChecked())}"
        response = requests.get(url)
        data = response.json()
        dicts ={}
        dicts[titulo] = data["Contra"]
        if self.hashchech.isChecked():
            dicts[hashn] = data["hash"]
        return dicts

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ContraWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())

