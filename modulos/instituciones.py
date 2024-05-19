from PyQt6.QtWidgets import QWidget, QToolTip, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame,QComboBox
import sys,json, pymongo, requests,random
class InstitucionesWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, además devuelve una lista de colegios o universidades del pais seleccionado 
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
        #guardamos el idioma y abrimos el json
        self.idioma = idioma
        with open('./idiomas/instituciones.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        #creamos los elementos del widget 
        self.label = QLabel(self.datas["Instituciones"], self)
        self.editline = QLineEdit(self)
        self.zona = QCheckBox(self.datas["Zona"])
        self.direccion = QCheckBox(self.datas["direccion"])
        self.Colegio = QComboBox()
        self.Comunidad = QComboBox()
        self.zonatext = QLineEdit()
        self.direcciontext = QLineEdit()
        #Propiedades de los widgets
        self.zonatext.setPlaceholderText(self.datas["NombreZona"])
        self.direcciontext.setPlaceholderText(self.datas["NombreDireccion"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.Colegio.addItems([self.datas["Colegio"],self.datas["Universidad"]])
        self.Colegio.currentIndexChanged.connect(self.cambiarIndice)
        self.zonatext.setEnabled(False)
        self.direcciontext.setEnabled(False)
        #eventos
        self.zona.enterEvent = self.showHelpZona
        self.zona.leaveEvent = self.hideHelp
        self.direccion.enterEvent = self.showHelpArea
        self.direccion.leaveEvent = self.hideHelp
        self.rellenarDatos()
        self.zona.stateChanged.connect(lambda state:self.bloquearLine(state,self.zonatext))
        self.direccion.stateChanged.connect(lambda state:self.bloquearLine(state,self.direcciontext))
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,3)
        layout.addWidget(self.Colegio,1,0)
        layout.addWidget(self.Comunidad,1,1)
        layout.addWidget(self.zona,2,0)
        layout.addWidget(self.zonatext,2,1)
        layout.addWidget(self.direccion,3,0)
        layout.addWidget(self.direcciontext,3,1)

        #establecemois laoyut
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
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
    def showHelpZona(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.zona.mapToGlobal(self.zona.rect().center()), tooltip_text)
    def showHelpArea(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.direccion.mapToGlobal(self.direccion.rect().center()), tooltip_text)
    def hideHelp(self, event):
        """
        Oculta el QToolTip
        Args:
            event (QEvent): El evento que activa la ocultación del tooltip.
        """
        QToolTip.hideText() 
    def traducir(self, idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        self.idioma = idioma
        self.datas = self.datos[self.idioma]
        self.label.setText(self.datas["Instituciones"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.zona.setText(self.datas["Zona"])
        self.direccion.setText(self.datas["direccion"])
        self.Colegio.setItemText(0, self.datas["Colegio"])
        self.Colegio.setItemText(1, self.datas["Universidad"])
        self.zonatext.setPlaceholderText(self.datas["NombreZona"])
        self.direcciontext.setPlaceholderText(self.datas["NombreDireccion"])
        #Bloquea direcciones de empresa en ingles debido a que faltan esos datos
        if self.idioma != "EN":
            self.direccion.setEnabled(True)
        else:
            if self.Colegio.currentIndex() == 1:
                self.direccion.setEnabled(False)
                self.direccion.setChecked(False)
        self.rellenarDatos()  

    def cambiarIndice(self):
        """
            Bloquea direccion debido a la falta de informacion.
        """        
        self.rellenarDatos()
        if self.Colegio.currentIndex() ==0 :
            self.direccion.setEnabled(True)
        else:
            if self.idioma == "EN":
                self.direccion.setEnabled(False)
                self.direccion.setChecked(False)
    def rellenarDatos(self):
        """
            Metodo que Accede a MongoDB y recoge las zonas, lo agrupara para que no se repita en el combobox
            y rellene el combobox
        """        
        self.Comunidad.clear()
        self.Comunidad.addItem("-")
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["Instituciones"]
        #Comprueba el index
        if self.Colegio.currentIndex()== 0:
            dd = db[self.datas["Colegio"]]
        else:
            dd = db[self.datas["Universidad"]]
        datos = dd.aggregate([
            { "$group": { "_id": "$TOWN", "town": { "$addToSet": "$TOWN" } } }
        ])
        #rellena los datos en el combobox
        for dato in datos:
            if not type(dato["town"][0])== float:
                self.Comunidad.addItem(dato["town"][0])

    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que el editline esta con texto y sino pone uno default
        titulo = self.editline.text() or self.datas["Instituciones"]
        direccion = self.direcciontext.text() or self.datas["direccion"]
        zona = self.zonatext.text() or self.datas["Zona"]
        dicts = {}
        #Accede al REST API
        url = f"http://localhost:5000/instituciones/{self.Colegio.currentIndex()}/{self.Comunidad.currentText()}/{cantidad}/{self.idioma}"
        response = requests.get(url)
        dataset = response.json()
        #Comprueba los datos y que checkbox estan checkeados
        dicts[titulo] = dataset["name"]
        if self.direccion.isChecked():
            dicts[direccion] = dataset["address"]
        if self.zona.isChecked():
            dicts[zona]=dataset["area"]
        #comprueba si la cantidad de datos es igual al pedido sino lo duplica aleatoriamente
        if len(dicts[titulo]) <cantidad:
            for i in range(cantidad - len(dicts[titulo])):
                num = random.randint(0,len(dicts[titulo]))
                dicts[titulo].append(dicts[titulo][num-1])
                if self.direccion.isChecked():
                    dicts[direccion].append(dicts[direccion][num-1])
                if self.zona.isChecked():
                    dicts[zona].append(dicts[zona][num-1])
        return dicts
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = InstitucionesWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())