from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys, random, json
from datetime import *
class FechaWidget(QWidget):
    def __init__(self,idioma):
        self.idioma = idioma
        super().__init__()
        with open('./idiomas/fechas.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.data = self.datos[idioma]
        #creamos los elementos del widget
        self.label = QLabel(self.data["Fecha"], self)
        self.editline = QLineEdit(self)
        self.largo = QCheckBox(self.data["Largo"])
        self.corto = QCheckBox(self.data["Corto"])
        self.fechainicio = QLineEdit()
        self.fechafinal = QLineEdit()
        self.separador = QLineEdit()
        self.obligatorio = QLabel(self.data["Obligatorio"])
        self.fechainicio.setPlaceholderText(self.data["FechaInicio"])
        self.fechafinal.setPlaceholderText(self.data["FechaFinal"])
        self.separador.setPlaceholderText(self.data["Separador"])
        self.editline.setPlaceholderText(self.data["NombreProyecto"])

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
        layout.addWidget(self.corto,1,1)
        layout.addWidget(self.separador,1,2,1,2)
        layout.addWidget(self.fechainicio,2,0,1,2)
        layout.addWidget(self.fechafinal,2,2,1,2)
        
        
        #establecemos layout
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
    def traducir(self, idioma):
        self.idioma = idioma
        self.data = self.datos[self.idioma]
        self.label.setText(self.data["Fecha"])
        self.largo.setText(self.data["Largo"])
        self.corto.setText(self.data["Corto"])
        self.obligatorio.setText(self.data["Obligatorio"])
        self.fechainicio.setPlaceholderText(self.data["FechaInicio"])
        self.fechafinal.setPlaceholderText(self.data["FechaFinal"])
        self.separador.setPlaceholderText(self.data["Separador"])
        self.editline.setPlaceholderText(self.data["NombreProyecto"])
    # Genera una fecha aleatoria entre dos fechas específicas
    def fechaaleatoria(self,fechainicio, fechafin):
        diferencia = fechafin - fechainicio
        dias = random.randint(0, diferencia.days)
        return fechainicio + timedelta(days=dias)
    
    def getdata(self,cantidad):
        
    
        titulo = self.editline.text() or self.data["Fecha"]
        separador = self.separador.text() or ""
        fechas = []
        dicts = {}
        for i in range(cantidad):
            fechas.append(self.fechaaleatoria(datetime.strptime(self.fechainicio.text(),"%d-%m-%Y"),datetime.strptime(self.fechafinal.text(),"%d-%m-%Y")))
        for i in range(len(fechas)):
            if self.largo.isChecked():
                fechas[i-1] = fechas[i-1].strftime(f"%d de {self.data["%m"]} %y")
            else:
                fechas[i-1] = fechas[i-1].strftime(f"%d{separador}%m{separador}%y")
        dicts[titulo] = fechas
        return dicts
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FechaWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())