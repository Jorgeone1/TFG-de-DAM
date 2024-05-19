from PyQt6.QtWidgets import QWidget,QToolTip ,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame,QComboBox
import sys,json, pymongo, requests,random
class EmpresaWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, Ademas devuelve una lista de empresas con sus datos de direccion, nombre o telefono/web 
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
        with open('./idiomas/empresa.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del Widget
        self.label = QLabel(self.datas["empresa"], self)
        self.editline = QLineEdit(self)
        self.direccion = QCheckBox(self.datas["direccion"], self)
        self.modificable = QCheckBox(self.datas["web"], self)
        self.mostrarProvincia = QCheckBox(self.datas["Zona"], self)
        self.provincia = QComboBox(self)
        self.direciontext = QLineEdit()
        self.modificabletext = QLineEdit()
        self.provinciatext = QLineEdit()
        #Propiedades de los widget
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        
        self.rellenarDatos()
        self.direciontext.setPlaceholderText(self.datas["nombredireccion"])
        self.modificabletext.setPlaceholderText(self.datas["nombreweb"])
        self.provinciatext.setPlaceholderText(self.datas["nombreprovincia"])
        self.direciontext.setEnabled(False)
        self.modificabletext.setEnabled(False)
        self.provinciatext.setEnabled(False)
        # Asignar eventos para mostrar y ocultar tooltips
        self.direccion.enterEvent = self.showHelpDireccion
        self.direccion.leaveEvent = self.hideHelp
        self.modificable.enterEvent = self.showHelpWeb
        self.modificable.leaveEvent = self.hideHelp
        self.mostrarProvincia.enterEvent = self.showHelpZona
        self.mostrarProvincia.leaveEvent = self.hideHelp
        self.direccion.stateChanged.connect(lambda state: self.bloquearLine(state,self.direciontext))
        self.modificable.stateChanged.connect(lambda state: self.bloquearLine(state,self.modificabletext))
        self.mostrarProvincia.stateChanged.connect(lambda state: self.bloquearLine(state,self.provinciatext))
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
        layout.addWidget(self.direccion, 2, 0)
        layout.addWidget(self.direciontext,2,1,1,2)
        layout.addWidget(self.modificable, 3, 0)
        layout.addWidget(self.modificabletext,3,1,1,2)
        layout.addWidget(self.mostrarProvincia, 1, 0)
        layout.addWidget(self.provinciatext,1,1)
        layout.addWidget(self.provincia, 1, 2)

        # Establecemos layout al widget principal
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
    def showHelpDireccion(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.direccion.mapToGlobal(self.direccion.rect().center()), tooltip_text)

    def showHelpWeb(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.modificable.mapToGlobal(self.modificable.rect().center()), tooltip_text)

    def showHelpZona(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.mostrarProvincia.mapToGlobal(self.mostrarProvincia.rect().center()), tooltip_text)

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
        self.label.setText(self.datas["empresa"])
        self.direccion.setText(self.datas["direccion"])
        self.modificable.setText(self.datas["web"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.mostrarProvincia.setText(self.datas["Zona"])
        self.direciontext.setPlaceholderText(self.datas["nombredireccion"])
        self.modificabletext.setPlaceholderText(self.datas["nombreweb"])
        self.provinciatext.setPlaceholderText(self.datas["nombreprovincia"])
        # Actualizar los tooltips
        self.rellenarDatos()
    def rellenarDatos(self):
        self.provincia.clear()
        self.provincia.addItem("-")
        # Establecer conexión con el servidor de MongoDB
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        # Seleccionar la base de datos
        db = cliente["Empresas"][f"Empresas{self.idioma}"]

        datos = db.aggregate([
            { "$group": { "_id": "$provincia", "prov": { "$addToSet": "$provincia" } } }
        ])
        for dato in datos:
            if type(dato["prov"][0]) != float:
                self.provincia.addItem(dato["prov"][0])
            
                
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba los editline y si no pone uno default
        titulo = self.editline.text() or self.datas["empresa"]
        direccion = self.direciontext.text() or self.datas["direccion"]
        mods = self.modificabletext.text() or self.datas["web"]
        Zona = self.provinciatext.text() or self.datas["Zona"]
        
        dicts = {titulo:[]}
        #accede al Rest api
        url = f"http://localhost:5000/Empresa/{self.provincia.currentText()}/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        dicts[titulo] = data["nombre"]
        #Comprueba los checkbox y va añadiendo los datos
        if self.direccion.isChecked():
            dicts[direccion]=data["direccion"]
        if self.modificable.isChecked():
            dicts[mods] = data["contacto"]
        if self.mostrarProvincia.isChecked():
            dicts[Zona] = data["provincia"]
        #si los datos son menores a la cantidad pedida por el usuario se elimina
        if len(dicts[titulo])< cantidad:
            for i in range(cantidad - len(dicts[titulo])):
                num = random.randint(0,len(dicts[titulo])-1)
                dicts[titulo].append(dicts[titulo][num])
                if self.direccion.isChecked():
                    dicts[direccion].append(dicts[direccion][num])
                if self.modificable.isChecked():
                    dicts[mods].append(dicts[mods][num])
                if self.mostrarProvincia.isChecked():
                    dicts[Zona].append(Zona[num])
        return dicts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = EmpresaWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())