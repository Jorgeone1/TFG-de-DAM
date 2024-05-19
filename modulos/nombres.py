from PyQt6.QtWidgets import QWidget, QToolTip, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication, QCheckBox, QFrame, QComboBox
import sys,random,pymongo,json,requests

class NombreWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de nombre y sus apellidos, ademas de tambien generar Correos
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
        with open('./idiomas/nombres.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["Nombre"], self)
        self.editline = QLineEdit(self)
        self.apellido = QCheckBox(self.datas["Apellido"], self)
        self.separado = QCheckBox(self.datas["separar"], self)
        self.apellidonom = QLineEdit()
        self.generobox = QCheckBox(self.datas["Genero"], self)
        self.genero = QComboBox()
        self.correo = QCheckBox(self.datas["correo"], self)
        self.correolabel = QLabel(self.datas["Dominio"], self)
        self.dominio = QLineEdit()
        
        #Propiedades de los widget
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.apellidonom.setPlaceholderText(self.datas["NombreApellido"])
        self.dominio.setPlaceholderText(self.datas["DominioName"])
        self.genero.addItems(["-", "M", "F"])
        self.apellido.stateChanged.connect(self.bloquearApe)
        self.separado.stateChanged.connect(self.bloquearLine)
        self.separado.setEnabled(False)
        self.apellidonom.setEnabled(False)
        self.dominio.setEnabled(False)
        # Asignar eventos para mostrar y ocultar tooltips
        self.apellido.enterEvent = self.showHelpApellido
        self.apellido.leaveEvent = self.hideHelp
        self.separado.enterEvent = self.showHelpSeparar
        self.separado.leaveEvent = self.hideHelp
        self.correo.enterEvent = self.showHelpCorreo
        self.correo.leaveEvent = self.hideHelp
        self.generobox.enterEvent = self.showHelpGenero
        self.generobox.leaveEvent = self.hideHelp
        self.correo.stateChanged.connect(lambda state: self.bloquearLines(state, self.dominio))
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
        layout.addWidget(self.apellido, 1, 0)
        layout.addWidget(self.generobox, 1, 1)
        layout.addWidget(self.genero, 1, 2)
        layout.addWidget(self.separado, 2, 0)
        layout.addWidget(self.apellidonom, 2, 1, 1, 2)
        layout.addWidget(self.correo, 3, 0)
        layout.addWidget(self.correolabel, 3, 1)
        layout.addWidget(self.dominio, 3, 2)

        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
    def bloquearLines(self,state,editline):
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
    def showHelpGenero(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda4"]
        QToolTip.showText(self.generobox.mapToGlobal(self.generobox.rect().center()), tooltip_text)
    def showHelpApellido(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.apellido.mapToGlobal(self.apellido.rect().center()), tooltip_text)

    def showHelpSeparar(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.separado.mapToGlobal(self.separado.rect().center()), tooltip_text)

    def showHelpCorreo(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.correo.mapToGlobal(self.correo.rect().center()), tooltip_text)

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
        self.label.setText(self.datas["Nombre"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.apellido.setText(self.datas["Apellido"])
        self.separado.setText(self.datas["separar"])
        self.apellidonom.setPlaceholderText(self.datas["NombreApellido"])
        self.generobox.setText(self.datas["Genero"])
        self.correo.setText(self.datas["correo"])
        self.correolabel.setText(self.datas["Dominio"])
        self.dominio.setPlaceholderText(self.datas["Dominio"])
        self.dominio.setPlaceholderText(self.datas["DominioName"])
        # Actualizar los tooltips
        
        self.correo.setToolTip(self.datas["ayuda3"])
    
    def bloquearApe(self,state):
        if state ==2:
            self.separado.setEnabled(True)  
        else:
            self.apellidonom.setEnabled(False)
            self.separado.setEnabled(False)
            self.separado.setChecked(False)
    def bloquearLine(self,state):
        if state==2:
            self.apellidonom.setEnabled(True)
        else:
            self.apellidonom.setEnabled(False)    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #comprueba que los editline tienen un nombre o sino pondra uno por defecto
        titulo = self.editline.text() or self.datas["Nombre"]
        dominio = self.dominio or "Gmail"
        apellid = self.apellidonom.text() or self.datas["Apellido"]
        #accede a la rest api
        url = f'http://127.0.0.1:5000/nombres/{self.genero.currentText()}/{self.idioma}/{cantidad}/{dominio}'
        response = requests.get(url)
        data = response.json()  # Convertir la respuesta a JSON
        dicts  = {}

        dicts[titulo] = data["names"]
        if self.apellido.isChecked():
            if self.separado.isChecked():
                dicts[apellid] = data["Apellido"]
            else:
                for i in range(len(dicts[titulo])):
                    dicts[titulo][i-1] = dicts[titulo][i-1] + " "+ data["Apellido"][i-1]
        if self.correo.isChecked():
            dicts[self.data["correo"]] = data["correo"]
        if self.generobox.isChecked():
            dicts[self.datas["Genero"]]= data["Genero"]
        
        return dicts
    def generarApellido(self,mongo):
        ap = mongo.aggregate([{ "$sample": { "size": 1 }}]).next()
        ap2 = mongo.aggregate([{ "$sample": { "size": 1 }}]).next()["name"] if self.idioma == "ES" else "" 
        return ap["name"] + " " + ap2
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = NombreWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())


