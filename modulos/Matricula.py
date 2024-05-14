from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QFrame
import sys,json,random,string
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
        lista = []
        dicts = {}
        for i in range(cantidad):
            lista.append(self.getMatricula())
        dicts[titulo]  = lista
        return dicts
    def getMatricula(self):
        mat = ""
        opciones = ['AA', 'AN', 'AD', 'UK', 'AO', 'AU', 'AO', 'UK', 'AV', 'AY', 'AV', 'UK', 'BA', 'BY', 'CA', 'CO', 'CK', 'GB', 'CP', 'CV', 'CT', 'GB', 'CW', 'CY', 'DA', 'DK', 'DI', 'GB', 'DL', 'DY', 'DX', 'GB', 'EA', 'EY', 'EJ', 'GB', 'FA', 'FP', 'FG', 'GB', 'FR', 'FY', 'FY', 'GB', 'GA', 'GO', 'GL', 'GP', 'GY', 'GV', 'HA', 'HJ', 'HF', 'HK', 'HY', 'KA', 'KL', 'KM', 'KM', 'KY', 'KR', 'LA', 'LJ', 'LK', 'LT', 'LR', 'GB', 'LU', 'LY', 'LX', 'GB', 'MA', 'MY', 'MW', 'GB', 'NA', 'NO', 'NP', 'NY', 'OA', 'OY', 'PA', 'PT', 'PU', 'PY', 'RA', 'RY', 'SA', 'SJ', 'SK', 'SO', 'SP', 'ST', 'SU', 'SW', 'SX', 'SY', 'VA', 'VY', 'WA', 'WJ', 'WK', 'WL', 'WL', 'WM', 'WY', 'YA', 'YK', 'YL', 'YU', 'YV', 'YY']
        if self.idioma == "ES":
            mat = "".join(random.choices(string.digits,k=4)) + "".join(random.choices([digit for digit in string.ascii_uppercase if digit != "Q"],k=3))
        elif self.idioma=="EN":
            mat = "".join(random.choice(opciones)) + "".join(random.choices(string.digits,k=2)) + "".join(random.choices(string.ascii_uppercase,k=3))
        return mat

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MatriculaWidget("ES")
    print(mainWindow.getMatricula())
    mainWindow.show()
    sys.exit(app.exec())