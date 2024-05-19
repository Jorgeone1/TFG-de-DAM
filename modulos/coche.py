from PyQt6.QtWidgets import QWidget,QToolTip, QComboBox,QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame
import sys, random,requests,json
import sqlite3 as sq
import json
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox, QComboBox, QGridLayout, QFrame, QApplication
import sys

class CocheWidget(QWidget):
    """
        Clase que crea un widget con sus componentes, y permite generar una lista de Coches aleatoria
    Args:
        QWidget (QWidget): Extendiende de la clase de QWidget
    """    
    def __init__(self, idioma):
        super().__init__()
        """
            Inicia el widget y sus componentes mas las propiedades
        Args:
            idiomas (String): Recoge el idioma la cual el widget estara traducido
        """      
        # Abrimos el archivo JSON con el idioma
        self.idioma = idioma
        with open('./idiomas/coche.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del Widget
        self.label = QLabel(self.datas["Coche"], self)
        self.editline = QLineEdit(self)
        self.Marca = QCheckBox(self.datas["Marca"])
        self.Tipo = QCheckBox(self.datas["Tipo"])
        self.comlab = QLabel(self.datas["Seleccionar"])
        self.comobo = QComboBox()
        self.marcno = QLineEdit()
        self.tipono = QLineEdit()

        # Propiedades de los widget creados
        self.Marca.enterEvent = self.showHelpMarca
        self.Tipo.enterEvent = self.showHelpTipo
        self.comlab.enterEvent = self.showHelpSeleccionar
        self.Marca.stateChanged.connect(self.bloquearMarca)
        self.Tipo.stateChanged.connect(self.bloquearTipo)
        self.marcno.setPlaceholderText(self.datas["MarcaNom"])
        self.tipono.setPlaceholderText(self.datas["TipoNom"])
        self.marcno.setEnabled(False)
        self.tipono.setEnabled(False)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.rellenarDatos()

        # Creamos un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al QFrame
        frame_layout = QGridLayout()

        # Agregamos los elementos al QFrame
        self.frame.setLayout(frame_layout)
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1, 1, 1)
        frame_layout.addWidget(self.Marca, 1, 0)
        frame_layout.addWidget(self.marcno, 1, 1)
        frame_layout.addWidget(self.Tipo, 2, 0)
        frame_layout.addWidget(self.tipono, 2, 1)
        frame_layout.addWidget(self.comlab, 3, 0)
        frame_layout.addWidget(self.comobo, 3, 1)

        # Establecemos un layout al widget y añadimos el frame
        widget_lat = QGridLayout(self)
        widget_lat.addWidget(self.frame)

    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        # Cambia el idioma del parámetro
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]

        # Cambia los valores del widget
        self.label.setText(self.datas["Coche"])
        self.Marca.setText(self.datas["Marca"])
        self.Tipo.setText(self.datas["Tipo"])
        self.comlab.setText(self.datas["Seleccionar"])
        self.marcno.setPlaceholderText(self.datas["MarcaNom"])
        self.tipono.setPlaceholderText(self.datas["TipoNom"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
    
    #rellena los datos
    def rellenarDatos(self):
        """ Metodo que rellena los datos del combobox de las marcas del coche
        """
        base = sq.connect(r"datos\Sqlite\CochesES.db")
        cursor = base.cursor()
        cursor.execute("Select nombre from Marca")
        datos = cursor.fetchall()
        self.comobo.addItem("-")
        for dato in datos:
            self.comobo.addItem(dato[0])
    def bloquearMarca(self,state):
        """bloquea el editline o desbloquea dependiendo si esta activo o no

        Args:
            state (int): indica el estado del checkbox
        """
        if state == 2:
            self.marcno.setEnabled(True)
        else:
            self.marcno.setEnabled(False)
    def bloquearTipo(self,state):
        """bloquea el editline o desbloquea dependiendo si esta activo o no

        Args:
            state (int): indica el estado del checkbox
        """

        if state == 2:
            self.tipono.setEnabled(True)
        else:
            self.tipono.setEnabled(False)
    
    def showHelpTipo(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de abajo, es decir una ayuda
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.Tipo.mapToGlobal(self.Tipo.rect().center()), tooltip_text)
    
    def showHelpMarca(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de abajo, es decir una ayuda
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.Marca.mapToGlobal(self.Marca.rect().center()), tooltip_text)
    
    def showHelpSeleccionar(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de abajo, es decir una ayuda
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.comlab.mapToGlobal(self.comlab.rect().center()), tooltip_text)
    
    def HideHelp(self, event):
        """
            Esconde el QToolTip al salir del widget con el raton
        Args:
            event (QEvent): El evento que activa la escondida del tooltip.
        """
        # La ventana se esconde para que no este todo el rato activo
        QToolTip.hideText()

    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que este rellenado los texto sino devuelve uno
        titulo = self.editline.text() or self.datas["Coche"]
        mar = self.marcno.text() or self.datas["Marca"]
        ti = self.tipono.text() or self.datas["Tipo"]
        dicts = {}

        #Accede al Rest API y recoge los datos
        url = f"http://localhost:5000/coches/{self.comobo.currentText()}/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()

        #Guarda los datos deseados, dependiendo los checkbox
        dicts[titulo] = data["modelo"]
        if self.Tipo.isChecked():
            dicts[ti] = data["tipo"]
        if self.Marca.isChecked():
            dicts[mar] = data["marca"]
        #si la cantidad de datos no es la adecuada, copia aleatoriamente datos dentro del diccionario
        if len(dicts[titulo])<cantidad:
            for i in range(cantidad-len(dicts[titulo])):
                num = random.randint(0,len(dicts[titulo])-1)
                dicts[titulo].append(dicts[titulo][num])
                if self.Tipo.isChecked():
                    dicts[ti].append(dicts[ti][num])
                if self.Marca.isChecked():
                    dicts[mar].append(dicts[mar][num])
        return dicts
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CocheWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())