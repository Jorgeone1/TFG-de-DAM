from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys, requests,json
class SegSolWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, devuelve una lista de codigos de la seguridad social verificadas falsas
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self, idiomas):
        super().__init__()
        """
        Inicia el widget y sus componentes más las propiedades
        Args:
            idiomas (str): Recoge el idioma en el cual el widget estará traducido
        """      
        # Guardamos el idioma y abrimos el json
        self.idioma = idiomas
        with open('./idiomas/segsol.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["segsol"], self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])

        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)

        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)

    def traducir(self, nuevo_idioma):
        """
        Método para traducir el contenido del widget al nuevo idioma
        Args:
            nuevo_idioma (str): Nuevo idioma al cual se traducirá el contenido del widget
        """
        self.idioma = nuevo_idioma
        self.datas = self.datos[self.idioma]

        # Actualizar los textos de los elementos del widget
        self.label.setText(self.datas["segsol"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        
    
    def getData(self,cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        titulo = self.editline.text() or "Seguridad Social"
        seg = {}
        url = f"http://localhost:5000/segsol/{cantidad}/{self.idioma}"
        response = requests.get(url)
        data = response.json()
        seg[titulo]= data["seguridad"]
        return seg
    
        

            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = SegSolWidget()
    print(mainWindow.generarEnSeg())
    mainWindow.show()
    sys.exit(app.exec())
