from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,json
class OtrosWidget(QWidget):
    """
        Clase que genera un widget con sus componentes la cula el usuario subira un archivo csv y de este generara datos 
    Args:
        QWidget (QWidget): Extiende de la clase de QWidget
    """    
    def __init__(self,idiomas):
        """
            Inicia el widget y sus componentes mas las propiedades
        Args:
            idiomas (String): Recoge el idioma la cual el widget estara traducido
        """      
        super().__init__()
        #guardamos el idioma y abrimos el json
        self.idioma = idiomas
        with open('./idiomas/codigobarras.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        #creamos los elementos del widget
        self.label = QLabel("Otros:", self)
        self.editline = QLineEdit(self)
        self.check = QCheckBox()
        self.editline.setPlaceholderText("Nombre Proyecto")
        
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
        layout.addWidget(self.check,1,0)
        
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "Otros"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = OtrosWidget()
    mainWindow.show()
    sys.exit(app.exec())