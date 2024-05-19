from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests,json
class MatriculaWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de matriculas de coches
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self,idioma):
        super().__init__()
        """
            Inicia el widget y sus componentes mas las propiedades
        Args:
            idiomas (String): Recoge el idioma la cual el widget estara traducido
        """      
        #guardamos el idioma y abrimos el json
        self.idioma = idioma
        with open('./idiomas/matricula.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        #creamos los elementos del widget
        self.label = QLabel(self.datas["Matricula"], self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        #establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        #agregamos los elementos al frame
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.editline,0,1)
        
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
    def traducir(self,nuevo_idioma):
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]
        self.label.setText(self.datas["Matricula"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        #Comprueba que haya texto en el editline
        titulo = self.editline.text() or "Matricula"
        #Accedemos al Rest API
        url = f"http://localhost:5000/matricula/{cantidad}/{self.idioma}"
        dicts = {}
        response = requests.get(url)
        data = response.json()
        dicts[titulo]  = data["matricula"]
        return dicts

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MatriculaWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())