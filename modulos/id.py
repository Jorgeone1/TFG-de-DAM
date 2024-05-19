from PyQt6.QtWidgets import QWidget, QLabel,QToolTip, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
import sys, requests,json
from modulos import error
class idWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una secuencia de numeros. 
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
        with open('./idiomas/id.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["id"], self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.labelempezar = QLabel(self.datas["inicio"], self)
        self.empezar = QLineEdit()
        self.empezar.setPlaceholderText(self.datas["opcional"])
        regexempezar = QRegularExpression(r'^[0-9]{1,6}$')
        validatorempezar = QRegularExpressionValidator(regexempezar, self.empezar)
        self.empezar.setValidator(validatorempezar)
        self.formatolabel = QLabel(self.datas["formato"], self)
        self.formato = QLineEdit()
        self.formato.setPlaceholderText(self.datas["opcional"])
        self.incrementar = QLineEdit()
        regexincrementar = QRegularExpression(r'^([1-9][0-9]?|100)$')
        validatorincrementar = QRegularExpressionValidator(regexincrementar, self.incrementar)
        self.incrementar.setValidator(validatorincrementar)
        self.incrementar.setPlaceholderText(self.datas["opcional"])
        self.labelincrementar = QLabel(self.datas["incrementar:"], self)

        # Asignar tooltips
        self.labelempezar.enterEvent = self.showHelpEmpezar
        self.labelempezar.leaveEvent = self.hideHelp
        self.labelincrementar.enterEvent = self.showHelpIncrementar
        self.labelincrementar.leaveEvent = self.hideHelp
        self.formatolabel.enterEvent = self.showHelpFormato
        self.formatolabel.leaveEvent = self.hideHelp

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1, 1, 3)
        layout.addWidget(self.labelempezar, 1, 0)  
        layout.addWidget(self.empezar, 1, 1)
        layout.addWidget(self.labelincrementar, 1, 2)
        layout.addWidget(self.incrementar, 1, 3)
        layout.addWidget(self.formatolabel, 2, 0)
        layout.addWidget(self.formato, 2, 1, 1, 3)

        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
    def showHelpEmpezar(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.labelempezar.mapToGlobal(self.labelempezar.rect().center()), tooltip_text)

    def showHelpIncrementar(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.labelincrementar.mapToGlobal(self.labelincrementar.rect().center()), tooltip_text)

    def showHelpFormato(self, event):
        """
        Muestra un QToolTip en la posición del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        tooltip_text = self.datas["ayuda3"]
        QToolTip.showText(self.formatolabel.mapToGlobal(self.formatolabel.rect().center()), tooltip_text)

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
        self.label.setText(self.datas["id"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.labelempezar.setText(self.datas["inicio"])
        self.empezar.setPlaceholderText(self.datas["opcional"])
        self.formatolabel.setText(self.datas["formato"])
        self.formato.setPlaceholderText(self.datas["opcional"])
        self.labelincrementar.setText(self.datas["incrementar:"])
        self.incrementar.setPlaceholderText(self.datas["opcional"])

        # Actualizar los tooltips
        self.label.setToolTip(self.datas["ayuda1"])
        self.labelempezar.setToolTip(self.datas["ayuda1"])
        self.formatolabel.setToolTip(self.datas["ayuda3"])
        self.labelincrementar.setToolTip(self.datas["ayuda2"])
        
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        try:
            idname = self.editline.text() or self.datas["id"]
            numero = self.empezar.text() or 0
            formato = self.formato.text() or "null"
            increment = self.incrementar.text() or 1
            if formato != "null":
                formato.format("hola")
                if r"{{}}" in formato:
                    raise error.ErrorPrograma(self.datas["error5"])
                if r"{}" not in formato:
                    formato = "null"
            url = f"http://localhost:5000/id/{str(numero)}/{formato}/{str(increment)}/{str(cantidad)}"
            response = requests.get(url)
            data = response.json()
            dicts = {idname : data["id"]}
            return dicts
        
        except KeyError:
            raise error.ErrorPrograma(self.datas["error1"])
        except IndexError:
            raise error.ErrorPrograma(self.datas["error2"])
        except ValueError:
            raise error.ErrorPrograma(self.datas["error3"])    
        except Exception:
            raise error.ErrorPrograma(self.datas["error4"])
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = idWidget("ES")
    mainWindow.getData(5)
    mainWindow.show()
    sys.exit(app.exec())