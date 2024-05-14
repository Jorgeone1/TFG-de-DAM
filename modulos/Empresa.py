from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox,QFrame,QComboBox
import sys,json, pymongo, math
class EmpresaWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma
        #creamos los elementos del widget
        self.label = QLabel("Empresa:", self)
        self.editline = QLineEdit(self)
        self.direccion = QCheckBox("Direccion")
        self.modificable = QCheckBox("web")
        self.provincia = QComboBox()
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.mostrarProvincia = QCheckBox("Zona")
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
        layout.addWidget(self.editline,0,1,1,2)
        layout.addWidget(self.direccion,1,0)
        layout.addWidget(self.modificable,1,1)
        layout.addWidget(self.mostrarProvincia,1,2)
        layout.addWidget(self.provincia,1,3)
        
        
        #establecemos layout
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
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
            if type(dato["prov"][0]) == float:
                print("Error")
            else:
                print(dato["prov"][0])
                self.provincia.addItem(dato["prov"][0])
    def getData(self,cantidad):
        titulo = self.editline.text() or "Empresa"
        lista = []
        direcc = []
        mod = []
        zona = []
        dicts = {}
        for i in range(cantidad):
            data = self.generarEmpresa()
            lista.append(data["nombre"])
            if self.direccion.isChecked():
                direcc.append(data["direccion"])
            if self.modificable.isChecked():
                if self.idioma=="ES":
                    mods = "web"
                elif self.idioma=="EN":
                    mods = "telefono"
                mod.append(data[mods])
            if self.mostrarProvincia.isChecked():
                zona.append(data["provincia"])
        dicts[titulo] = lista
        if self.direccion.isChecked():
            dicts["direccion"]=direcc
        if self.modificable.isChecked():
            if self.idioma=="ES":
                mods = "web"
            elif self.idioma=="EN":
                mods = "phone"
            dicts[mods] = mod
        if self.mostrarProvincia.isChecked():
            dicts["Zona"] = zona
        return dicts

    def generarEmpresa(self):
        # Establecer conexión con el servidor de MongoDB
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        # Seleccionar la base de datos
        db = cliente["Empresas"][f"Empresas{self.idioma}"]
        if self.provincia.currentText() == "-":
            datos = db.aggregate([{ "$sample": { "size": 1 }}]).next()
        else:
            data = db.aggregate([
                { "$match": { "provincia": self.provincia.currentText()} },  # Filtrar por género "M"
                { "$sample": { "size": 1 } }       # Seleccionar un documento aleatorio
                ])
            datos = {}
            for datas in data:
                datos = datas
        return datos
        # Obtener la colección en la que deseas insertar datos

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = EmpresaWidget("EN")
    mainWindow.show()
    sys.exit(app.exec())