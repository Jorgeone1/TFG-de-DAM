import random
from PyQt6.QtWidgets import QWidget, QToolTip,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests, json
class TelefonoWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de telefonos falsos mobiles o fijos
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
        with open('./idiomas/telefono.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["telefono"], self)
        self.editline = QLineEdit(self)
        self.tele = QCheckBox(self.datas["fijo"], self)
        self.teleName = QLineEdit()
        self.sinmobil = QCheckBox(self.datas["sinmobil"], self)
        
        #Propiedades de los widget
        self.sinmobil.setEnabled(False)
        self.teleName.setEnabled(False)
        self.tele.stateChanged.connect(self.bloquearMobil)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.teleName.setPlaceholderText(self.datas["NombreTelefono"])
        # Asignar eventos para mostrar y ocultar tooltips
        self.tele.enterEvent = self.showHelpFijo
        self.tele.leaveEvent = self.hideHelp
        self.sinmobil.enterEvent = self.showHelpSinMobil
        self.sinmobil.leaveEvent = self.hideHelp
        self.tele.stateChanged.connect(lambda state:self.bloquearLine(state,self.teleName))
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1, 1, 2)
        layout.addWidget(self.tele, 1, 0)
        layout.addWidget(self.teleName, 1, 1)
        layout.addWidget(self.sinmobil, 1, 2)

        widgetcreados = QGridLayout(self)
        widgetcreados.addWidget(self.frame)
    def bloquearLine(self,state,editline):
        """
        Bloquea o activa los cuadro de texto correspondiente a su checkbox

        Args:
            state (int):comprueba el estado del checbox
            editline (QEditLine): cuadro de texto a bloquear o desbloquear
        """        
        if state== 2:
            editline.setEnabled(True)
        else:
            editline.setEnabled(False)
    def bloquearMobil(self, state):
        """
        Método para habilitar o deshabilitar el checkbox de sin móvil.
        Args:
            state (int): Estado del checkbox de fijo.
        """
        if state == 2:  # Checkbox checked
            self.sinmobil.setEnabled(True)
        else:
            self.sinmobil.setEnabled(False)

    def showHelpFijo(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.tele.mapToGlobal(self.tele.rect().center()), tooltip_text)

    def showHelpSinMobil(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.sinmobil.mapToGlobal(self.sinmobil.rect().center()), tooltip_text)

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
        self.label.setText(self.datas["telefono"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.tele.setText(self.datas["fijo"])
        self.teleName.setPlaceholderText(self.datas["NombreTelefono"])
        self.sinmobil.setText(self.datas["sinmobil"])

        # Actualizar los tooltips
        self.tele.setToolTip(self.datas["ayuda1"])
        self.sinmobil.setToolTip(self.datas["ayuda2"])
    
    def bloquearMobil(self,state):
        if state == 2:
            self.sinmobil.setEnabled(True)
        else:
            self.sinmobil.setEnabled(False)
            self.sinmobil.setChecked(False)
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #mira si esta rellenado los cuadro de texto sino
        fijo = self.editline.text() or "Fijo"
        mobil = self.teleName.text() or "Mobil"
        #accede al rest API
        url = f"http://localhost:5000/telefono/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        dicts ={}
        #Comprueba que datos estan checkeados y devuelve el diccionario
        if self.tele.isChecked():
            if self.sinmobil.isChecked():
                dicts[fijo] = data["fijo"]
            else:
                dicts[fijo] = data["fijo"]
                dicts[mobil]=data["mobil"]
        else:
            dicts[mobil]=data["mobil"]
        return dicts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = TelefonoWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())


        