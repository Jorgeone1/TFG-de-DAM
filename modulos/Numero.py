from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,QApplication,QCheckBox, QToolTip,QFrame
import sys
class NumeroWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #creamos los elementos del widget
        self.label = QLabel("Numeros:", self)
        self.editline = QLineEdit(self)
        self.entero = QCheckBox("Entero")
        self.editline.setPlaceholderText("Nombre Proyecto")
        self.minimoe = QLineEdit()
        self.maximoe = QLineEdit()
        self.minimol = QLabel("Minimo:")
        self.maximol = QLabel("Maximo:")
        
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
        layout.addWidget(self.entero,0,3)
        layout.addWidget(self.minimol,1,0)
        layout.addWidget(self.minimoe,1,1)
        layout.addWidget(self.maximol,1,2)
        layout.addWidget(self.maximoe,1,3)
        
        self.entero.enterEvent  = self.show_tooltip
        self.entero.leaveEvent = self.hide_tooltip
        
        widget_Creados = QGridLayout(self)
        widget_Creados.addWidget(self.frame)

    def show_tooltip(self, event):
        # Mostrar un widget emergente personalizado cuando el mouse entra en el checkbox
        tooltip_text = "Selecciona solo enteros dentro de ese rango\n si hay decimales se redondea"
        QToolTip.showText(self.entero.mapToGlobal(self.entero.rect().center()), tooltip_text)

    def hide_tooltip(self, event):
        # Ocultar el widget emergente cuando el mouse sale del checkbox
        QToolTip.hideText()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = NumeroWidget()
    mainWindow.show()
    sys.exit(app.exec())