from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame, QComboBox
import sys,pymongo, json,random
class PaisWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma
        #creamos los elementos del widget        
        self.label = QLabel("Pais:", self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.continentes = QComboBox()
        self.capital = QCheckBox("Capital")
        self.continent = QCheckBox("Continente")
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        self.rellenarDatos()
        #establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1,1,2)  
        layout.addWidget(self.continentes,1,0)
        layout.addWidget(self.capital,1,1)
        layout.addWidget(self.continent,1,2)
        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)

    def rellenarDatos(self):
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
        titulo = self.editline.text() or "Pais"
        lista = []
        capital = []
        continente = []
        paises = {}
        for i in range(cantidad):
            data = self.getPais()
            lista.append(data["pais"])
            if self.continent.isChecked():
                continente.append(data["continente"])
            if self.capital.isChecked():
                capital.append(data["capital"])
        paises[titulo] = lista
        if self.continent.isChecked:
            paises["continente"]=continente
        if self.capital.isChecked():
            paises["capital"] = capital
        return paises
    
    def getPais(self):
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["GeneradorDeDatos"][f"Pais{self.idioma}"]
        if self.continentes.currentText() == "-":
            data = db.aggregate([{ "$sample": { "size": 1 }}]).next()
            return data
        else:
            data = db.aggregate([
                { "$match": { "continente": self.continentes.currentText()} },  # Filtrar por género "M"
                { "$sample": { "size": 1 } }       # Seleccionar un documento aleatorio
                ])
            dato = {}
            for dat in data:
                dato = dat
            return dato


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = PaisWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())