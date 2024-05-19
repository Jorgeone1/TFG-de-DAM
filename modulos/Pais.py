from PyQt6.QtWidgets import QWidget,QToolTip, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame, QComboBox
import sys,pymongo, json,requests,random
class PaisWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, y devolvera el nombre de un pais aleatorio, con su capital y continente. 
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
        with open('./idiomas/pais.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget        
        self.label = QLabel(self.datas["pais"], self)
        self.editline = QLineEdit(self)
        self.continentes = QComboBox()
        self.capital = QCheckBox(self.datas["capital"], self)
        self.continent = QCheckBox(self.datas["continente"], self)
        self.continentetext= QLineEdit()
        self.capitaltext = QLineEdit()
        self.sinpais = QCheckBox(self.datas["sinpais"])
        #Propiedades de los widget
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.continentetext.setPlaceholderText(self.datas["NombreContinente"])
        self.capitaltext.setPlaceholderText(self.datas["NombreContinente"])
        self.continentetext.setEnabled(False)
        self.capitaltext.setEnabled(False)
        self.sinpais.setEnabled(False)
        # Asignar eventos para mostrar y ocultar tooltips
        self.capital.enterEvent = self.showHelpCapital
        self.capital.leaveEvent = self.hideHelp
        self.continent.enterEvent = self.showHelpContinente
        self.continent.leaveEvent = self.hideHelp
        self.capital.stateChanged.connect(self.bloquearsin)
        self.continent.stateChanged.connect(self.bloquearsin)
        self.capital.stateChanged.connect(lambda state: self.bloquearLine(state,self.capitaltext))
        self.continent.stateChanged.connect(lambda state: self.bloquearLine(state,self.continentetext))
        self.sinpais.enterEvent = self.showHelpsin
        self.sinpais.leaveEvent = self.hideHelp
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Rellenar los datos del QComboBox
        self.rellenarDatos()

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)  
        layout.addWidget(self.continentes, 1, 1)
        layout.addWidget(self.sinpais,1,0)
        layout.addWidget(self.capital, 2, 0)
        layout.addWidget(self.capitaltext,2,1)
        layout.addWidget(self.continent, 3, 0)
        layout.addWidget(self.continentetext,3,1)

        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
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

    def bloquearsin(self,state):
        """
            Bloquea el sin pais o desbloquea dependiendo del texto
        Args:
            state (_type_): _description_
        """        
        if self.capital.isChecked() or self.continent.isChecked():
            self.sinpais.setEnabled(True)
        if not self.capital.isChecked() and not self.continent.isChecked():
            self.sinpais.setEnabled(False)
            self.sinpais.setChecked(False)
    def showHelpsin(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.sinpais.mapToGlobal(self.sinpais.rect().center()), tooltip_text)
    def showHelpCapital(self, event):

        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.capital.mapToGlobal(self.capital.rect().center()), tooltip_text)

    def showHelpContinente(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.continent.mapToGlobal(self.continent.rect().center()), tooltip_text)

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
        self.label.setText(self.datas["pais"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.capital.setText(self.datas["capital"])
        self.continent.setText(self.datas["continente"])
        self.continentetext.setPlaceholderText(self.datas["NombreContinente"])
        self.capitaltext.setPlaceholderText(self.datas["NombreContinente"])
        self.sinpais.setText(self.datas["sinpais"])
        # Actualizar los tooltips
        self.rellenarDatos()
    def rellenarDatos(self):
        """
        Método que rellena el combobox de continentes a traves de mongodb
        """        
        self.continentes.clear()
        self.continentes.addItem("-")
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["GeneradorDeDatos"][f"Pais{self.idioma}"]
        datos = db.aggregate([
            { "$group": { "_id": "$continente", "conti": { "$addToSet": "$continente" } } }
        ])
        for dato in datos:
            self.continentes.addItem(dato["conti"][0])
            
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba si el texto esta rellenado si no pone uno default
        titulo = self.editline.text() or self.datas["pais"]
        capital = self.capital.text() or self.datas["capital"]
        continente = self.continent.text() or self.datas["continente"]
        #Accede al rest api 
        paises = {}
        url = f"http://localhost:5000/pais/{self.continentes.currentText()}/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        lista = []
        #guarda los datos en un diccionario y compruebe si esta pulsado los checks
        if not self.sinpais.isChecked():
            paises[titulo] = data["pais"]
            lista = paises[titulo]
        if self.continent.isChecked():
            paises[continente]=data["continente"]
            lista = paises[continente]
        if self.capital.isChecked():
            paises[capital] = data["capital"]
            lista = paises[capital]
        #si la lista no llena la cantidad, duplica aleatorimaente el contenido del diccionario
        
        if len(lista) < cantidad:
            for i in range(cantidad - len(lista)):
                num = random.randint(0,len(lista))
                if not self.sinpais.isChecked():
                    paises[titulo].append(paises[titulo][num-1])
                if self.continent.isChecked():
                    paises[continente].append(data[continente][num-1])
                if self.capital.isChecked():
                    paises[capital].append(data[capital][num-1])
        return paises
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = PaisWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())