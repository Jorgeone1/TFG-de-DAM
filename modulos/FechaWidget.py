from PyQt6.QtWidgets import QWidget,QDateEdit,QToolTip,QCalendarWidget,QVBoxLayout,QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys, random, json,requests
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from datetime import *
from modulos import error
class FechaWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de fechas aleaotorias en un rango seleccionado por el usuario
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self,idioma):
        """
            Inicia el widget y sus componentes mas las propiedades
        Args:
            idiomas (String): Recoge el idioma la cual el widget estara traducido
        """  
        #guarda el idioma y abre el json    
        super().__init__()
        self.idioma = idioma
        with open('./idiomas/fechas.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[idioma]
        #creamos los elementos del widget
        self.label = QLabel(self.datas["Fecha"], self)
        self.editline = QLineEdit(self)
        self.largo = QCheckBox(self.datas["Largo"])
        self.fechainicio = QLineEdit()
        self.fechafinal = QLineEdit()
        self.separador = QLineEdit()
        self.fechainiciolabel = QLabel(self.datas["FechaInicio"])
        self.fechafinallabel = QLabel(self.datas["FechaFinal"])
        #Propiedades de los widget
        uncaracterregex = QRegularExpression(r'^.$')
        uncaracter = QRegularExpressionValidator(uncaracterregex)
        self.separador.setValidator(uncaracter)
        regexfecha = QRegularExpression(r'^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$')
        validatorfecha = QRegularExpressionValidator(regexfecha)
        self.fechainicio.setPlaceholderText(self.datas["Obligatorio"])
        self.fechafinal.setPlaceholderText(self.datas["Obligatorio"])
        self.fechainicio.setValidator(validatorfecha)
        self.fechafinal.setValidator(validatorfecha)
        self.separador.setPlaceholderText(self.datas["Separador"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.fechafinal.setValidator(validatorfecha)
        self.largo.enterEvent = self.showHelpLargo
        self.largo.leaveEvent = self.hideHelp
        
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
        layout.addWidget(self.largo,1,0)
        layout.addWidget(self.separador,1,2,1,2)
        layout.addWidget(self.fechainiciolabel,2,0)
        layout.addWidget(self.fechainicio,2,1)
        layout.addWidget(self.fechafinallabel,2,2)
        layout.addWidget(self.fechafinal,2,3)

        
        #establecemos layout
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)


    def traducir(self, nuevo_idioma):
        """
            Metodo que cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]
        self.label.setText(self.datas["Fecha"])
        self.largo.setText(self.datas["Largo"])
        self.fechainicio.setPlaceholderText(self.datas["Obligatorio"])
        self.fechafinal.setPlaceholderText(self.datas["Obligatorio"])
        self.separador.setPlaceholderText(self.datas["Separador"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.fechainiciolabel.setText(self.datas["FechaInicio"])
        self.fechafinallabel.setText(self.datas["FechaFinal"])

    def showHelpLargo(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.largo.mapToGlobal(self.largo.rect().center()), tooltip_text)

    def hideHelp(self, event):
        """
        Oculta el QToolTip
        Args:
            event (QEvent): El evento que activa la ocultación del tooltip.
        """
        QToolTip.hideText()
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        try:
            #Comprueba los editline si estan llenos o no
            barra = False
            titulo = self.editline.text() or self.datas["Fecha"]
            separador = self.separador.text() or " "
            fechainicio = self.fechainicio.text()
            fechafinal = self.fechafinal.text()
            if not fechainicio or not fechafinal:
                raise error.ErrorPrograma(self.datas["error3"])            #Comprueba que las fechas son validas sino lanzara un error
            date = datetime.strptime(fechainicio,r"%d-%m-%Y")
            date2 = datetime.strptime(fechafinal,r"%d-%m-%Y")
            #si la fecha final es menor que la inicial lanzara otro error
            if date > date2:
                raise error.ErrorPrograma(self.datas["error2"])
            #en las paginas web los simbolos se representan de otra forma
            if separador == "#":
                separador = "%23"
            elif separador == "?":
                separador = "%3F"
            #en este caso no funciona asi que decidi que sea el default para luego recogerlo en un bucle
            elif separador == "/":
                separador = " "
                barra = True
            #accede al REST API
            url = f"http://localhost:5000/fechas/{int(self.largo.isChecked())}/{fechainicio}/{fechafinal}/{separador}/{cantidad}/{self.idioma}"
            response = requests.get(url)
            data = response.json()
            #en caso que ponga la / sustituira todos los espacios por /
            if barra and not self.largo.isChecked():
                for i in range(len(data["fecha"])):
                    data["fecha"][i-1] = data["fecha"][i-1].replace(" ","/")
            return {titulo:data["fecha"]}
        except ValueError:
            raise error.ErrorPrograma(self.datas["error2"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FechaWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())
