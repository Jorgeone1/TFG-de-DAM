import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QLineEdit, QScrollArea, QComboBox,QSizePolicy
from modulos import nombres, direccion
with open('./idiomas/español.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

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
        textolineas= []
        datosesp = datos["Español"]
        # Widget central izquierdo
        widget_central_izquierdo = QWidget()
        izquierdo = QVBoxLayout()
        widget_central_izquierdo.setLayout(izquierdo)
        partePrincipal.addWidget(widget_central_izquierdo, 1, 0)

        # Ajuste de tamaño del QLineEdit
        buscadorBoton = QLineEdit()
        buscadorBoton.setFixedHeight(20)  # Establecer la altura fija del QLineEdit
        buscadorBoton.setPlaceholderText(datosesp["Buscador"])
        izquierdo.addWidget(buscadorBoton)
        textolineas.append(buscadorBoton)
        # Área de desplazamiento y QVBoxLayout
        scrollArea = QScrollArea()
        widgetCuerpoIzquierda = QWidget()
        VLayoutCuerpoIzq = QVBoxLayout()
        widgetCuerpoIzquierda.setLayout(VLayoutCuerpoIzq)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widgetCuerpoIzquierda)
        izquierdo.addWidget(scrollArea)
        
        claves_espanol = [
        "nombre", "direccion", "contraseña", "dni", "telefonos", "correos", 
        "imagenes", "Matricula", "coches", "SeguridadSocial", "deportes", 
        "IBAN", "CCC", "Numeros", "booleanos", "Fechas", "DireccionIP", 
        "Pais", "Precio", "producto", "codigoBarra", "equipos", "Color", 
        "Marca", "materiales", "Instituciones", "CodigoPostal", "Libros", 
        "ISBN", "Categoria"
        ]
        # Botones en el QVBoxLayout(Pruebas, luego recoradar cambiarlo)
        botones = []
        botons = []
        
        

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
        botonOtros = QPushButton("Otros Datos")
        partePrincipal.addWidget(botonOtros,2,0)
        botons.append(botonOtros)
        #Widget de borrar y idiomas
        BotonBorrar = QPushButton(datosesp["Borrar"])
        botons.append(BotonBorrar)
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
        botonConfirmar = QPushButton(datosesp["Confirmar"])
        botons.append(botonConfirmar)
        widgetnombre = nombres.NombreWidget()
        widgetdireccion = direccion.DireccionWidget()
        botonConfirmar.clicked.connect(lambda: self.generar_boton(cuerpoDerechoWidget,widgetdireccion))
        layout_abajo_derecha.addWidget(botonConfirmar,0,0)  # Agregar el botón al layout derecho
        cantidad_numero = QLineEdit()
        layout_abajo_derecha.addWidget(cantidad_numero,0,1)
        cantidad_numero.setFixedHeight(20)
        cantidad_numero.setPlaceholderText(datosesp["Cantidad"])
        textolineas.append(cantidad_numero)
        comboboxFormato = QComboBox()
        layout_abajo_derecha.addWidget(comboboxFormato,0,2)
        formatoarray = ["XML","JSON","CSV","SQL","PDF","TXT"]
        comboboxFormato.addItems(formatoarray)
        # Conectar la señal textChanged del QLineEdit al método de filtro
        
        buscadorBoton.textChanged.connect(lambda text: self.filtrar_nombres(text, botones))
        for i in range(0, 29):
            boton = QPushButton(f"{datosesp[claves_espanol[i]]}")
            boton.setObjectName(f"Boton {i}")  # Establecer un nombre único para cada botón
            boton.clicked.connect(lambda: self.generar_boton(cuerpoDerechoWidget,widgetnombre))
            botones.append(boton)
            VLayoutCuerpoIzq.addWidget(boton)
        
        # Establecer el ancho mínimo del Widget_derecho
        Widget_derecho.setMinimumWidth(widget_central_izquierdo.sizeHint().width())
        comboboxIdiomas.currentIndexChanged.connect(lambda index:self.traducir(index,botones,botons,textolineas,datos,claves_espanol))
        # Set the minimum width of the left and right columns and make them stretch equally
        partePrincipal.setColumnMinimumWidth(0, 200)
        partePrincipal.setColumnMinimumWidth(1, 200)
        partePrincipal.setColumnStretch(0, 1)
        partePrincipal.setColumnStretch(1, 1)
        
    #prueba pa el futuro
    def generar_boton(self, widget,widget_compuesto):
        for i in range(widget.layout().count()):
            existing_widget = widget.layout().itemAt(i).widget()
            if isinstance(existing_widget, type(widget_compuesto)):
                # Si ya existe un widget del mismo tipo, no hacer nada
                return
        # Establecer un borde al widget compuesto
        widget_compuesto.setStyleSheet("border: 1px solid gray;")

        # Establecer la política de tamaño horizontal del widget compuesto como Expanding
        widget_compuesto.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        # Agregar el widget compuesto al layout del widget pasado como argumento
        widget.layout().addWidget(widget_compuesto)
    
    def limpiar_cuerpo_derecho(self, widget):
        # Eliminar todos los widgets del layout del cuerpo derecho
        for i in reversed(range(widget.layout().count())):
            widget.layout().itemAt(i).widget().setParent(None)
    #filtro simple
    def filtrar_nombres(self, texto_filtro, botones):
        for boton in botones:
            nombre_boton = boton.text()#coje el nombre del texto
            #cada vez que se cambia comprueba si tiene el mismo nombre que del line edit
            if texto_filtro.lower() in nombre_boton.lower():
                boton.setVisible(True)
            else:
                boton.setVisible(False)
    def traducir(self,index,botones,botons,textlines,json,array):
            i = 0
            botonss = ["Otros","Borrar","Confirmar"]
            textos = ["Buscador","Cantidad"]
            if index == 0:
                json = json["Español"]
            elif index == 1:
                json = json["English"]

            for boton in botones:
                boton.setText(json[array[i]])
                i+=1
            i= 0
            for boton in botons:
                boton.setText(json[botonss[i]])
                i+=1
            i=0
            for text in textlines:
                text.setPlaceholderText(json[textos[i]])
                i+=1
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
