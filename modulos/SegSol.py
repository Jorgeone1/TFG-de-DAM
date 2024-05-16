from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys, requests
class SegSolWidget(QWidget):
    def __init__(self,idiomas):
        super().__init__()
        self.idioma = "ES"
        #creamos elementos de widget
        self.label = QLabel("Seguridad Social:", self)
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
        
        widget_creados = QGridLayout(self)
        widget_creados.addWidget(self.frame)
        
    
    def getData(self,cantidad):
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
