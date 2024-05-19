from PyQt6.QtWidgets import QWidget, QToolTip,QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QFrame
import sys, requests,json
class BoolWidget(QWidget):
    """
        Clase que genera un widget con sus componentes, y devuelve si es true o false, permitiendo modificar sus nombres 
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
        #abrimos archivo JSON de idiomas
        self.idioma= idiomas
        with open('./idiomas/booleanos.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Creamos los elementos del widget
        self.label = QLabel(self.datas["Booleanos"])
        self.editline = QLineEdit(self)
        self.truelab = QLabel(self.datas["NombreTrue"])
        self.falselab = QLabel(self.datas["NombreFalse"])
        self.edittrue = QLineEdit()
        self.editfalse = QLineEdit()
        
        #Propiedades de los widget
        self.edittrue.setPlaceholderText(self.datas["Opcional"])
        self.editfalse.setPlaceholderText(self.datas["Opcional"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])

        # Creamos un QFrame
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde
        
        # Establecemos el layout del QFrame
        frame_layout = QGridLayout()
        self.frame.setLayout(frame_layout)

        # Agregamos los elementos al layout del QFrame
        frame_layout.addWidget(self.label, 0, 0)
        frame_layout.addWidget(self.editline, 0, 1, 1, 3)
        frame_layout.addWidget(self.truelab, 1, 0)
        frame_layout.addWidget(self.edittrue, 1, 1)
        frame_layout.addWidget(self.falselab, 1, 2)
        frame_layout.addWidget(self.editfalse, 1, 3)
        
        #Creamos eventos que muestre la ayuda
        self.truelab.enterEvent = self.showHelpTrue
        self.truelab.leaveEvent = self.HideHelp
        self.falselab.enterEvent = self.showHelpFalse
        self.truelab.leaveEvent = self.HideHelp
        
        # Establecemos el layout principal del widget
        layout = QGridLayout(self)
        layout.addWidget(self.frame)
    
    def showHelpTrue(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de abajo, es decir una ayuda
        tooltip_text = self.datas["ayuda1"]
        QToolTip.showText(self.truelab.mapToGlobal(self.truelab.rect().center()), tooltip_text)
    
    def showHelpFalse(self, event):
        """
            Muestra un QToolTip en la posicion del Widget
        Args:
            event (QEvent): El evento que activa la muestra del tooltip.
        """
        # Muestra un bocadillo o una mini ventana que pone el mensaje de abajo, es decir una ayuda
        tooltip_text = self.datas["ayuda2"]
        QToolTip.showText(self.falselab.mapToGlobal(self.falselab.rect().center()), tooltip_text)
    
    def HideHelp(self, event):
        """
            Esconde el QToolTip al salir del widget con el raton
        Args:
            event (QEvent): El evento que activa la escondida del tooltip.
        """
        # La ventana se esconde para que no este todo el rato activo
        QToolTip.hideText()

    def traducir(self, idioma_nuevo):
        """
            Cambia el idioma de todo el widget
        Args:
            nuevo_idioma (String): idioma nuevo a cambiar
        """        
        #cambia el idioma
        self.idioma = idioma_nuevo
        self.datas = self.datos[self.idioma]
        #sustituye todos los valores
        self.label.setText(self.datas["Booleanos"])
        self.truelab.setText(self.datas["NombreTrue"])
        self.falselab.setText(self.datas["NombreFalse"])
        self.edittrue.setPlaceholderText(self.datas["Opcional"])
        self.editfalse.setPlaceholderText(self.datas["Opcional"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])

    def getData(self,cantidad):
        """
            Recoge los datos del Rest API y recoge los deseados
        Args:
            cantidad (int): Cantidad de datos a recoger

        Returns:
            dict: devuelve un diccionario con los datos deseados
        """        
        #Nombre de los editline
        truename = self.edittrue.text() or "True"
        falsename = self.editfalse.text() or "False"
        titulo = self.editline.text() or self.datas["Booleanos"]
        #Conectar a base
        url = f"http://localhost:5000/booleanos/{truename}/{falsename}/{cantidad}"
        response = requests.get(url)
        data = response.json()
        #creacion y devolucion del diccionario
        dicts = {titulo:data["booleanos"]}
        return dicts
                
                    
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = BoolWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())