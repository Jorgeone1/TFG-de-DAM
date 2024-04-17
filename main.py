import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QLineEdit, QScrollArea, QComboBox,QSizePolicy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de datos")
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle("Generador de datos") 
        self.initUI()

    def initUI(self):
        # Crear un widget central y establecer el diseño en él
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        partePrincipal = QGridLayout()
        central_widget.setLayout(partePrincipal)

        # Widget central izquierdo
        widget_central_izquierdo = QWidget()
        izquierdo = QVBoxLayout()
        widget_central_izquierdo.setLayout(izquierdo)
        partePrincipal.addWidget(widget_central_izquierdo, 1, 0)

        # Ajuste de tamaño del QLineEdit
        buscadorBoton = QLineEdit()
        buscadorBoton.setFixedHeight(15)  # Establecer la altura fija del QLineEdit
        izquierdo.addWidget(buscadorBoton)

        # Área de desplazamiento y QVBoxLayout
        scrollArea = QScrollArea()
        widgetCuerpoIzquierda = QWidget()
        VLayoutCuerpoIzq = QVBoxLayout()
        widgetCuerpoIzquierda.setLayout(VLayoutCuerpoIzq)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widgetCuerpoIzquierda)
        izquierdo.addWidget(scrollArea)
        botonesNombre = ["NombreApellidos"]
        # Botones en el QVBoxLayout(Pruebas, luego recoradar cambiarlo)
        botones = []
        for i in range(1, 50):
            boton = QPushButton(f"Boton {i}")
            boton.setObjectName(f"Boton {i}")  # Establecer un nombre único para cada botón
            botones.append(boton)
            VLayoutCuerpoIzq.addWidget(boton)

        # Establecer el estiramiento del QVBoxLayout del lado izquierdo
        partePrincipal.setColumnStretch(0, 1)  # La primera columna se estira para ocupar el espacio restante

        # Widget derecho
        Widget_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        Widget_derecho.setLayout(layout_derecho)
        partePrincipal.addWidget(Widget_derecho, 1, 1)
        
        # Botón de borrar, ComboBox de idioma, Área de desplazamiento, etc.
        arriba_derecha_widget = QWidget()
        layout_arriba_derecho = QGridLayout()
        arriba_derecha_widget.setLayout(layout_arriba_derecho)
        layout_derecho.addWidget(arriba_derecha_widget)

        #Widget de borrar y idiomas
        BotonBorrar = QPushButton("Borrar")
        layout_arriba_derecho.addWidget(BotonBorrar,0,0)
        comboboxIdiomas= QComboBox()
        layout_arriba_derecho.addWidget(comboboxIdiomas,0,1)
        comboIdiomas = ["ES","EN"]
        comboboxIdiomas.addItems(comboIdiomas)

        # Área de desplazamiento para el cuerpo derecho
        scrollAreaL = QScrollArea()
        scrollAreaL.setWidgetResizable(True)
        layout_derecho.addWidget(scrollAreaL)  # Agregar el área de desplazamiento en lugar del cuerpo derecho

        # Widget para el cuerpo derecho
        cuerpoDerechoWidget = QWidget()
        Vderecho = QVBoxLayout()
        cuerpoDerechoWidget.setLayout(Vderecho)
        scrollAreaL.setWidget(cuerpoDerechoWidget)  

        #Widget Abajo de recha
        abajo_derecha = QWidget()
        layout_abajo_derecha = QGridLayout()
        abajo_derecha.setLayout(layout_abajo_derecha)
        layout_derecho.addWidget(abajo_derecha)

        #boton confirmar y combobox de formato de salida
        botonConfirmar = QPushButton("Confirmar")
        botonConfirmar.clicked.connect(lambda: self.generar_boton(cuerpoDerechoWidget))
        layout_abajo_derecha.addWidget(botonConfirmar,0,0)  # Agregar el botón al layout derecho
        comboboxFormato = QComboBox()
        layout_abajo_derecha.addWidget(comboboxFormato,0,1)
        formatoarray = ["XML","JSON","CSV","SQL","PDF","TXT"]
        comboboxFormato.addItems(formatoarray)
        # Conectar la señal textChanged del QLineEdit al método de filtro
        buscadorBoton.textChanged.connect(lambda text: self.filtrar_nombres(text, botones))

        # Establecer el ancho mínimo del Widget_derecho
        Widget_derecho.setMinimumWidth(widget_central_izquierdo.sizeHint().width())

        # Set the minimum width of the left and right columns and make them stretch equally
        partePrincipal.setColumnMinimumWidth(0, 200)
        partePrincipal.setColumnMinimumWidth(1, 200)
        partePrincipal.setColumnStretch(0, 1)
        partePrincipal.setColumnStretch(1, 1)
    #prueba pa el futuro
    def generar_boton(self, widget):
        # Crear un nuevo widget compuesto con un QLineEdit y un QPushButton
        widget_compuesto = QWidget()
        layout_compuesto = QVBoxLayout()
        widget_compuesto.setLayout(layout_compuesto)

        # Agregar un QLineEdit al layout compuesto
        linea_texto = QLineEdit()
        layout_compuesto.addWidget(linea_texto)

        # Agregar un QPushButton al layout compuesto
        boton_agregar = QPushButton("Agregar")
        layout_compuesto.addWidget(boton_agregar)

        # Establecer un borde al widget compuesto
        widget_compuesto.setStyleSheet("border: 1px solid gray;")

        # Establecer la política de tamaño horizontal del widget compuesto como Expanding
        widget_compuesto.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        # Agregar el widget compuesto al layout del widget pasado como argumento
        widget.layout().addWidget(widget_compuesto)
    #filtro simple
    def filtrar_nombres(self, texto_filtro, botones):
        for boton in botones:
            nombre_boton = boton.text()#coje el nombre del texto
            #cada vez que se cambia comprueba si tiene el mismo nombre que del line edit
            if texto_filtro.lower() in nombre_boton.lower():
                boton.setVisible(True)
            else:
                boton.setVisible(False)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
