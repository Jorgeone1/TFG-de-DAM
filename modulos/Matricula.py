from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,requests
class MatriculaWidget(QWidget):
    def __init__(self,idioma):
        super().__init__()
        self.idioma = idioma
        #creamos los elementos del widget
        self.label = QLabel("Matricula:", self)
        self.editline = QLineEdit(self)
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
        
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame)
        
    
    def getData(self,cantidad):
        titulo = self.editline.text() or "Matricula"
        url = f"http://localhost:5000/matricula/{cantidad}/{self.idioma}"
        dicts = {}
        response = requests.get(url)
        data = response.json()
        dicts[titulo]  = data["matricula"]
        return dicts

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MatriculaWidget("ES")
    print(mainWindow.getMatricula())
    mainWindow.show()
    sys.exit(app.exec())