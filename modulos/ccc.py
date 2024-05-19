import random
#Comprobación y operaciones del ccc
from PyQt6.QtWidgets import QWidget, QToolTip,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame 
import sys,requests, json
class CCCWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, ademas envia un diccionario con CCC y sus respectivos IBAN
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self,idiomas):
        super().__init__()
        """
            Inicia el widget y sus componentes mas las propiedades
        Args:
            idiomas (String): Recoge el idioma la cual el widget estara traducido
        """      
        #Se abre el archivo JSON
        self.idioma= idiomas
        with open('./idiomas/ccc.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        #crear los elementos del widget
        self.label = QLabel("CCC:", self)
        self.editline = QLineEdit(self)
        self.IBAN = QCheckBox("IBAN")
        self.noCC = QCheckBox("Sin CCC")
        self.ibanline = QLineEdit()

        #Propiedades del Widget
        self.noCC.setEnabled(False)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.IBAN.stateChanged.connect(self.bloquearCCC)
        self.ibanline.setPlaceholderText("Nombre IBAN")
        self.ibanline.setEnabled(False)
        self.IBAN.enterEvent = self.showHelpIBAN
        self.IBAN.leaveEvent = self.HideHelp
        self.noCC.enterEvent = self.showHelpCCC
        self.noCC.leaveEvent = self.HideHelp
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #Establecer layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        #Agregar los elementos al QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1,1,2)
        frame_layout.addWidget(self.IBAN, 1, 0)
        frame_layout.addWidget(self.noCC, 1, 2)
        frame_layout.addWidget(self.ibanline,2,0,1,3)
        
        #Establecer el layout principal del widget
        widget_layout = QGridLayout(self)
        widget_layout.addWidget(self.frame)
    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        #Cambia el idioma del parametro
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]
        
        #cambia los valores del widget
        self.label.setText(self.datas["noCCC"])
        self.noCC.setText(self.datas["noCCC"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.ibanline.setPlaceholderText(self.datas["Nombre IBAN"])

    def showHelpCCC(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de ayuda
        tooltip_text = self.datas["ayuda1"]
        # Calcular la posición central del QCheckBox
        QToolTip.showText(self.noCC.mapToGlobal(self.noCC.rect().center()), tooltip_text)

    def showHelpIBAN(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de ayuda
        tooltip_text = self.datas["ayuda2"]
        # Calcular la posición central del QCheckBox
        QToolTip.showText(self.IBAN.mapToGlobal(self.IBAN.rect().center()), tooltip_text)
    
    def HideHelp(self, event):
        """
            Esconde el QToolTip al salir del widget con el raton
        Args:
            event (QEvent): El evento que activa la escondida del tooltip.
        """
        # La ventana se esconde para que no este todo el rato activo
        QToolTip.hideText()

    #Evitar errores de logica bloqueando los botones necesarios
    def bloquearCCC(self,state):
        """
            Metodo que bloquea el o desbloque el checkbox no CC
        Args:
            state (int): comprueba el estado del checkbox
        """        
        if state == 2:  
            self.noCC.setEnabled(True)
            self.ibanline.setEnabled(True)
        else:
            self.noCC.setEnabled(False)
            self.noCC.setChecked(False)
            self.ibanline.setEnabled(False)

    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que tenga texto los lineEdit sino sera uno predeterminado
        title = self.editline.text() or "CCC"
        iban_name = self.ibanline.text() or "IBAN"

        #Recoge los datos del REST API
        url = f"http://localhost:5000/IBAN/{str(cantidad)}"
        response = requests.get(url)
        data = response.json()
        datosBancarios  = {}
        #Comprueba los checkbox pulsados
        if self.IBAN.isChecked():
            datosBancarios[iban_name] = data["iban"]
            if not self.noCC.isChecked():
                datosBancarios[title] = data["ccc"]
        else:
            datosBancarios[title] = data["ccc"]
        return datosBancarios



    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CCCWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())
