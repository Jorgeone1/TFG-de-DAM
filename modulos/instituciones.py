from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame,QComboBox
import sys,json, pymongo
class InstitucionesWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma
        with open('./idiomas/instituciones.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.data = self.datos[self.idioma]
        #creamos los elementos del widget 
        self.label = QLabel(self.data["Instituciones"], self)
        self.editline = QLineEdit(self)
        self.zona = QCheckBox(self.data["Zona"])
        self.direccion = QCheckBox(self.data["direccion"])
        self.editline.setPlaceholderText(self.data["NombreProyecto"])
        self.Colegio = QComboBox()
        self.Colegio.addItems([self.data["Colegio"],self.data["Universidad"]])
        self.Colegio.currentIndexChanged.connect(self.cambiarIndice)
        self.Comunidad = QComboBox()
        self.rellenarDatos()
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
        layout.addWidget(self.zona,1,2)
        layout.addWidget(self.direccion,1,3)
        
        #establecemois laoyut
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
    
    def traducir(self, idioma):
        self.idioma = idioma
        self.data = self.datos[self.idioma]
        self.label.setText(self.data["Instituciones"])
        self.editline.setPlaceholderText(self.data["NombreProyecto"])
        self.zona.setText(self.data["Zona"])
        self.direccion.setText(self.data["direccion"])
        self.Colegio.setItemText(0, self.data["Colegio"])
        self.Colegio.setItemText(1, self.data["Universidad"])
        if self.idioma != "EN":
            self.direccion.setEnabled(True)
        else:
            if self.Colegio.currentIndex() == 1:
                self.direccion.setEnabled(False)
        self.rellenarDatos()  # Método para rellenar los datos de Comunidad si es necesario

    def cambiarIndice(self):
        self.rellenarDatos()
        if self.Colegio.currentIndex() ==0 :
            self.direccion.setEnabled(True)
        else:
            if self.idioma == "EN":
                self.direccion.setEnabled(False)
                self.direccion.setChecked(False)
    def rellenarDatos(self):
        self.Comunidad.clear()
        self.Comunidad.addItem("-")
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["Instituciones"]
        if self.Colegio.currentIndex()== 0:
            print(self.data["Colegio"])
            dd = db[self.data["Colegio"]]
        else:
            print(self.data["Universidad"])
            dd = db[self.data["Universidad"]]
        datos = dd.aggregate([
            { "$group": { "_id": "$TOWN", "town": { "$addToSet": "$TOWN" } } }
        ])
        for dato in datos:
            if not type(dato["town"][0])== float:
                self.Comunidad.addItem(dato["town"][0])

    def getData(self,cantidad):
        titulo = self.editline.text() or self.data["Instituciones"]
        nom = []
        comun = []
        direc = []
        dicts = {}
        for i in range(cantidad):
            data = self.getInstitution()
            nom.append(data["name"])
            if self.direccion.isChecked():
                direc.append(data["Street"])
            if self.zona.isChecked():
                comun.append(data["TOWN"])
        dicts[titulo] = nom
        if self.direccion.isChecked():
            dicts[self.data["direccion"]] = direc
        if self.zona.isChecked():
            dicts[self.data["Zona"]]=comun
        return dicts
    def getInstitution(self):
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["Instituciones"]
        if self.Colegio.currentIndex()==0:
            dd = db[self.data["Colegio"]]
        else:
            dd = db[self.data["Universidad"]]
        if self.Comunidad.currentText() == "-":
            data = dd.aggregate([{ "$sample": { "size": 1 }}]).next()
        else:
            datos = dd.aggregate([
                { "$match": { "TOWN": self.Comunidad.currentText()} },  # Filtrar por género "M"
                { "$sample": { "size": 1 } }       # Seleccionar un documento aleatorio
                ])
            data = {}
            for dat in datos:
                data = dat
        return data
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = InstitucionesWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())