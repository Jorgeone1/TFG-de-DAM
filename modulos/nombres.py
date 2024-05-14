from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication, QCheckBox, QFrame, QComboBox
import sys,random,pymongo,json

class NombreWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.idioma ="ES"
        with open('./idiomas/fechas.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        #creamos los elementos del widget
        self.label = QLabel("Nombre:", self)
        self.editline = QLineEdit(self)
        self.apellido = QCheckBox("Apellidos")
        self.separado = QCheckBox("Separar apellidos")
        self.apellidonom = QLineEdit()
        self.generobox = QCheckBox("Genero")
        self.genero = QComboBox()
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.apellidonom.setPlaceholderText("Nombre del apellido (Opcional)")
        self.genero.addItems(["-","M","F"])
        self.apellido.stateChanged.connect(self.bloquearApe)
        self.separado.stateChanged.connect(self.bloquearLine)
        self.separado.setEnabled(False)
        self.apellidonom.setEnabled(False)
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
        layout.addWidget(self.apellido,1,0)
        layout.addWidget(self.generobox,1,1)
        layout.addWidget(self.genero,1,2)
        layout.addWidget(self.separado,2,0)
        layout.addWidget(self.apellidonom,2,1,1,2)
        
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)

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
        titulo = self.editline.text() or "Nombre"
        apellid = self.apellidonom.text() or "Apellidos"
        lis = []
        ape = []
        generoo = []
        dicts = {}
        # Establecer conexión con el servidor de MongoDB
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        # Seleccionar la base de datos
        db = cliente["GeneradorDeDatos"]
        # Obtener la colección en la que deseas insertar datos
        
        if self.genero.currentText()=="-":
            
            cursor = db["NombreEng"]
            cursor2 = db["Apellidos"]
            for i in range(cantidad):
                nom = cursor.aggregate([{ "$sample": { "size": 1 }}]).next()
                lis.append(nom["name"])
                if self.generobox.isChecked():
                    generoo.append(nom["gender"])
            if self.apellido.isChecked():
                if self.separado.isChecked():      
                    for i in range(cantidad): 
                        ape.append(self.generarApellido(cursor2))
                else:
                    for i in range(0,cantidad):
                        lis[i] = lis[i] + " "+ self.generarApellido(cursor2)
            else:
               nom = cursor.aggregate([{ "$sample": { "size": 1 }}]).next()
               lis.append(nom["name"])
            dicts[titulo] = lis
            if self.apellido.isChecked() & self.separado.isChecked():
                dicts[apellid] = ape
            if self.generobox.isChecked():
                dicts["genero"]= generoo
        else:
            cursor = db["NombreEng"]
            cursor2 = db["Apellidos"]
            
            
            for i in range(cantidad):
                dato = cursor.aggregate([
                { "$match": { "gender": self.genero.currentText() } },  # Filtrar por género "M"
                { "$sample": { "size": 1 } }       # Seleccionar un documento aleatorio
                ])
                for documento in dato:
                    lis.append(documento["name"])
                    if self.generobox.isChecked():
                        generoo.append(documento["gender"]) 
            if self.apellido.isChecked():
                if self.separado.isChecked():
                    for i in range(cantidad):
                        ape.append(self.generarApellido(cursor2))
                    dicts[apellid] = ape
                else:
                    for i in range(cantidad):
                        lis[i] = lis[i] + " " + self.generarApellido(cursor2)
            dicts[titulo] = lis
            if self.generobox.isChecked():
               dicts["genero"] = generoo
        return dicts
    def generarApellido(self,mongo):
        ap = mongo.aggregate([{ "$sample": { "size": 1 }}]).next()
        ap2 = mongo.aggregate([{ "$sample": { "size": 1 }}]).next()["name"] if self.idioma == "ES" else "" 
        return ap["name"] + " " + ap2
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = NombreWidget()
    mainWindow.show()
    sys.exit(app.exec())


