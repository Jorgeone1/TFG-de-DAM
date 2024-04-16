import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QScrollArea, QGridLayout,QLineEdit

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
        partePrincipal = QGridLayout()
        central_widget.setLayout(partePrincipal)

        # Campo de texto (TextField)
        textField = QLineEdit()
        partePrincipal.addWidget(textField, 0, 0, 1, 2)  # Se extiende a través de dos columnas
        partePrincipal.setRowStretch(0, 0)  # No estirar la fila del TextField

        # Parte central con área de desplazamiento
        scrollAreaWidgetContents = QWidget()
        scrollAreaLayout = QVBoxLayout(scrollAreaWidgetContents)

        for i in range(20):
            scrollAreaLayout.addWidget(QPushButton(f"Botón {i+1}"))

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollAreaWidgetContents)

        partePrincipal.addWidget(scrollArea, 1, 0, 1, 2)  # Se extiende a través de dos columnas
        partePrincipal.setRowStretch(1, 1)  # Estirar la fila para llenar el espacio restante

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()