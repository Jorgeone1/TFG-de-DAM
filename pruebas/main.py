import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de datos")
        self.setGeometry(100, 100, 1000, 500)

        self.initUI()

    def initUI(self):
        # Crear un widget central y establecer el diseño en él
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        partePrincipal =  QGridLayout()
        central_widget.setLayout(partePrincipal)

        # Título
        titulo = QLabel("Generador de Datos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el título
        partePrincipal.addWidget(titulo, 0, 0, 1, 2)  # Se extiende a través de dos columnas
        partePrincipal.setRowStretch(0, 0)  # No estirar la fila del título

        # Parte central
        parteMedio = QWidget()
        parteMedioLayout = QGridLayout()  # Usar un QGridLayout para los botones
        parteMedio.setLayout(parteMedioLayout)
        partePrincipal.addWidget(parteMedio, 1, 0, 1, 2)  # Se extiende a través de dos columnas
        partePrincipal.setRowStretch(1, 1)  # Estirar la fila para llenar el espacio restante

        botonprueba = QPushButton("boton izquierdo")
        parteMedioLayout.addWidget(botonprueba, 0, 0)

        botonprueba2 = QPushButton("boton derecho")
        parteMedioLayout.addWidget(botonprueba2, 0, 1)
        
        creditos = QLabel("Jorge Wang Wang Copyright")
        creditos.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el título
        partePrincipal.addWidget(creditos, 2, 0, 1, 2)  # Se extiende a través de dos columnas
        partePrincipal.setRowStretch(0, 0)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
