from PyQt6.QtWidgets import QWidget, QToolTip,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests, json
class DireccionWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, ademas genera direcciones falsas con sus nombre de calles, ciudades y provincia. 
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
        with open('./idiomas/direccion.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["direccion"], self)
        self.editline = QLineEdit(self)
        self.COP = QCheckBox(self.datas["codpop"], self)
        self.ciudad = QCheckBox(self.datas["Comunidad"], self)
        self.Provincia = QCheckBox(self.datas["Provincia"], self)
        self.COPtext = QLineEdit()
        self.ciudadtext = QLineEdit()
        self.proviniciatext = QLineEdit()
        self.sindireccion = QCheckBox(self.datas["nodirec"])
        #Propiedades de los widgets
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.COPtext.setPlaceholderText(self.datas["NombreCOP"])
        self.ciudadtext.setPlaceholderText(self.datas["NombreCiudad"])
        self.proviniciatext.setPlaceholderText(self.datas["NombreProv"])
        self.sindireccion.setEnabled(False)
        self.COPtext.setEnabled(False)
        self.proviniciatext.setEnabled(False)
        self.ciudadtext.setEnabled(False)

        # Asignar eventos para mostrar y ocultar tooltips
        self.COP.enterEvent = self.showHelpCOP
        self.COP.leaveEvent = self.hideHelp
        self.ciudad.enterEvent = self.showHelpCiudad
        self.ciudad.leaveEvent = self.hideHelp
        self.Provincia.enterEvent = self.showHelpProvincia
        self.Provincia.leaveEvent = self.hideHelp
        self.COP.stateChanged.connect(self.bloquearSin)
        self.ciudad.stateChanged.connect(self.bloquearSin)
        self.Provincia.stateChanged.connect(self.bloquearSin)
        self.sindireccion.enterEvent = self.showHelpSin
        self.sindireccion.leaveEvent = self.hideHelp
        self.COP.stateChanged.connect(lambda state: self.bloquearLine(state,self.COPtext))
        self.ciudad.stateChanged.connect(lambda state: self.bloquearLine(state,self.ciudadtext))
        self.Provincia.stateChanged.connect(lambda state: self.bloquearLine(state,self.proviniciatext))
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Añadimos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)
        layout.addWidget(self.sindireccion,0,2)
        layout.addWidget(self.COP, 1, 0)
        layout.addWidget(self.COPtext,1,1,1,2)
        layout.addWidget(self.Provincia, 2, 0)
        layout.addWidget(self.proviniciatext,2,1,1,2)
        layout.addWidget(self.ciudad, 3, 0)
        layout.addWidget(self.ciudadtext,3,1,1,2)
        
        # Establecemos layout al principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
    def bloquearLine(self,state,editline):
        """
        Bloquea o activa los cuadro de texto correspondiente a su checkbox

        Args:
            state (_type_): _description_
            editline (_type_): _description_
        """        
        if state== 2:
            editline.setEnabled(True)
        else:
            editline.setEnabled(False)
    def bloquearSin(self,state):
        """
            Método que comprueba que los 3 botones si estan activados o desactivados
            para que el sin direccion imprima o no imprima texto
        Args:
            state (_type_): _description_
        """        
        if self.COP.isChecked() or self.ciudad.isChecked() or self.Provincia.isChecked():
            self.sindireccion.setEnabled(True)
        elif not self.COP.isChecked() and not self.ciudad.isChecked() and not self.Provincia.isChecked():
            self.sindireccion.setEnabled(False)
            self.sindireccion.setChecked(False)
    def showHelpSin(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda4"]
        QToolTip.showText(self.sindireccion.mapToGlobal(self.sindireccion.rect().center()), tooltip_text)

    def showHelpCOP(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.COP.mapToGlobal(self.COP.rect().center()), tooltip_text)

    def showHelpCiudad(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.ciudad.mapToGlobal(self.ciudad.rect().center()), tooltip_text)

    def showHelpProvincia(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.Provincia.mapToGlobal(self.Provincia.rect().center()), tooltip_text)

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
        self.label.setText(self.datas["direccion"])
        self.COP.setText(self.datas["codpop"])
        self.ciudad.setText(self.datas["Comunidad"])
        self.Provincia.setText(self.datas["Provincia"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        
        # Actualizar los tooltips
        self.COP.setToolTip(self.datas["ayuda1"])
        self.ciudad.setToolTip(self.datas["ayuda2"])
        self.Provincia.setToolTip(self.datas["ayuda3"])
        self.COPtext.setPlaceholderText(self.datas["NombreCOP"])
        self.ciudadtext.setPlaceholderText(self.datas["NombreCiudad"])
        self.proviniciatext.setPlaceholderText(self.datas["NombreProv"])
        self.sindireccion.setText(self.datas["nodirec"])    
        #bloquea la provincia porque no existe comunidades autonomas en Inglaterra
        if self.idioma =="ES":
            self.Provincia.setEnabled(True)
        elif self.idioma == "EN":
            self.Provincia.setEnabled(False)
            self.Provincia.setChecked(False)
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #comprueba que este escrito en el y si no pone uno default
        titulo = self.editline.text() or self.datas["direccion"]
        codpos = self.COPtext.text() or self.datas["codpop"]
        ciudad = self.ciudadtext.text() or self.datas["Comunidad"]
        prov = self.proviniciatext.text() or self.datas["Provincia"]
        #accede a la rest API
        url = f'http://127.0.0.1:5000/direccion/{self.idioma}/{cantidad}'
        response = requests.get(url)
        data = response.json()
        direcci = {}
        #Filtra los datos que hay que enviar
        if not self.sindireccion.isChecked():
            direcci[titulo] = data["direccion"]
        if self.COP.isChecked():
            direcci[codpos] = data["Codigo"]
        if self.ciudad.isChecked():
            direcci[prov] = data["Provincia"]
        if self.Provincia.isChecked():
            direcci[ciudad] = data["ciudad"]
        return direcci
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DireccionWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())
