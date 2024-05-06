from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        # Crear un QFrame
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        frame.setLineWidth(2)  # Establecer el ancho del borde

        # Crear y agregar elementos al QFrame
        label = QLabel("Label")
        edit_line = QLineEdit()
        button = QPushButton("Button")

        frame_layout = QVBoxLayout()  # Layout vertical para el QFrame
        frame_layout.addWidget(label)
        frame_layout.addWidget(edit_line)
        frame_layout.addWidget(button)

        frame.setLayout(frame_layout)  # Establecer el layout en el QFrame

        # Agregar el QFrame al QGridLayout
        grid_layout.addWidget(frame, 0, 0)

        self.setWindowTitle("Ejemplo de QFrame recubriendo elementos en QGridLayout")

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
