from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
from PyQt6.QtGui import QIntValidator
import sys, requests
from modulos import error
class idWidget(QWidget):
    def __init__(self,idiomas):
        super().__init__()
        self.idioma = idiomas
        #creamos los elementos del widget        
        self.label = QLabel("ID:", self)
        self.editline = QLineEdit(self)

        self.editline.setPlaceholderText("Nombre Proyecto")
        self.labelempezar = QLabel("Inicio Num: ")
        self.empezar = QLineEdit()
        self.empezar.setPlaceholderText("Opcional")
        self.empezar.setValidator(QIntValidator(0, 100000, self))
        self.formatolabel = QLabel("Formato: ")
        self.formato = QLineEdit()
        self.formato.setPlaceholderText("opcional")
        self.incrementar = QLineEdit()
        self.incrementar.setValidator(QIntValidator(0, 100, self))
        self.labelincrementar = QLabel("Incrementar:")
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
        layout.addWidget(self.labelempezar,1,0)  
        layout.addWidget(self.empezar,1,1)
        layout.addWidget(self.labelincrementar,1,2)
        layout.addWidget(self.incrementar,1,3)
        layout.addWidget(self.formatolabel,2,0)
        layout.addWidget(self.formato,2,1,1,3)

        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        try:
            idname = self.editline.text() or "ID"
            numero = self.empezar.text() or 0
            formato = self.formato.text() or "null"
            increment = self.incrementar.text() or 1
            if "+" in str(numero):
                numero = numero.replace("+","0")
            if "+" in str(increment):
                if len(increment)== 1:
                    increment = 1
                else:
                    increment = increment.replace("+","")
            if formato != "null":
                formato.format("hola")
                if r"{{}}" in formato:
                    raise error.ErrorPrograma("No puede haber {{}}")
                if r"{}" not in formato:
                    formato = "null"
            url = r"http://localhost:5000/id/"+str(numero)+"/"+formato+"/"+str(increment)+"/"+str(cantidad)
            response = requests.get(url)
            data = response.json()
            dicts = {idname : data["id"]}
            return dicts
        
        except KeyError:
            raise error.ErrorPrograma("Debe estar limpio el {}")
        except IndexError:
            raise error.ErrorPrograma("No puede haber mas de un {}")
        except ValueError:
            raise error.ErrorPrograma("No puede haber {} sin cerrar")    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = idWidget("ES")
    mainWindow.getData(5)
    mainWindow.show()
    sys.exit(app.exec())