import sys,json
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QLineEdit, QScrollArea, QComboBox,QSizePolicy, QFrame
from modulos import error,booleanos,ccc,coche,codigobarras,Color,contras,direccion, Dni,Empresa,FechaWidget,imagenes,instituciones,IP,ISBN,Matricula,nombres,Numero,Otros,Pais,SegSol,telefono,id
from functools import partial
with open('./idiomas/español.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)
colorcuenta = 0
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.idioma = "ES"
        self.setWindowTitle("Generador de datos")
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle("Generador de datos") 
        self.initUI()
        

    def initUI(self):
        # Crear un widget central y establecer el diseño en él
        self.widgets_creados = [] 
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
        self.clave= []
        self.claves_espanol = [
        "nombre", "direccion", "contraseña", "dni", "telefonos", 
        "imagenes", "Matricula", "coches", "SeguridadSocial", "id",
        "CCC", "Empresa", "Numeros", "booleanos", "Fechas", "DireccionIP", 
        "Pais", "codigoBarra", "Color", "Instituciones","ISBN"]
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
        BotonBorrar.clicked.connect(lambda: self.limpiar_cuerpo_derecho(cuerpoDerechoWidget))
        botons.append(BotonBorrar)
        layout_arriba_derecho.addWidget(BotonBorrar,0,0)
        
        self.comboboxIdiomas= QComboBox()
        layout_arriba_derecho.addWidget(self.comboboxIdiomas,0,1)
        comboIdiomas = ["ES","EN"]
        self.comboboxIdiomas.addItems(comboIdiomas)
        
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
        botonConfirmar.clicked.connect(lambda: self.Confirm(layout_derecho))
        botons.append(botonConfirmar)


        botonOtros.clicked.connect(partial(self.generar_boton,cuerpoDerechoWidget,"Otros"))
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
        # y una línea horizontal entre los widgets para separarlos
        cuerpoDerechoLayout = cuerpoDerechoWidget.layout()
        cuerpoDerechoLayout.setContentsMargins(5, 5, 5, 5)  # Márgenes del layout

        # Agregar un borde al layout del cuerpo derecho
        cuerpoDerechoWidget.setStyleSheet("QVBoxLayout {border: 1px solid black;}")
        buscadorBoton.textChanged.connect(lambda text: self.filtrar_nombres(text, botones))
        for i in range(len(self.claves_espanol)):
            boton = QPushButton(f"{datosesp[self.claves_espanol[i]]}")
            boton.setObjectName(f"Boton {i}")  # Establecer un nombre único para cada botón
            widgettipo = self.claves_espanol[i]
            boton.clicked.connect(partial(self.generar_boton, cuerpoDerechoWidget, widgettipo))
            botones.append(boton)
            VLayoutCuerpoIzq.addWidget(boton)

        
        # Establecer el ancho mínimo del Widget_derecho
        Widget_derecho.setMinimumWidth(widget_central_izquierdo.sizeHint().width())
        self.comboboxIdiomas.currentIndexChanged.connect(lambda index:self.traduci(index,botones,botons,textolineas,datos))
        # Set the minimum width of the left and right columns and make them stretch equally
        partePrincipal.setColumnMinimumWidth(0, 200)
        partePrincipal.setColumnMinimumWidth(1, 200)
        partePrincipal.setColumnStretch(0, 1)
        partePrincipal.setColumnStretch(1, 1)
    
    def generar_widget(self, widgettipo):
        widget = None
        if widgettipo in self.claves_espanol:
            if widgettipo == "nombre":
                widget = nombres.NombreWidget(self.idioma)
            elif widgettipo == "direccion":
                widget = direccion.DireccionWidget(self.idioma)
            elif widgettipo == "id":
                widget = id.idWidget(self.idioma)
                
            elif widgettipo == "contraseña":
                widget = contras.ContraWidget(self.idioma)
                
            elif widgettipo == "dni":
                widget = Dni.DNIWidget(self.idioma)
                
            elif widgettipo == "telefonos":
                widget = telefono.TelefonoWidget(self.idioma)
                
            elif widgettipo == "imagenes":
                widget = imagenes.ImagenesWidget(self.idioma)
            elif widgettipo == "Matricula":
                widget = Matricula.MatriculaWidget(self.idioma)
            elif widgettipo == "coches":
                widget = coche.CocheWidget(self.idioma)
                
            elif widgettipo == "SeguridadSocial":
                widget = SegSol.SegSolWidget(self.idioma)
                
            elif widgettipo == "CCC":
                widget = ccc.CCCWidget(self.idioma)
                
            elif widgettipo == "Empresa":
                widget =Empresa.EmpresaWidget(self.idioma)
                
            elif widgettipo == "Numeros":
                widget = Numero.NumeroWidget(self.idioma)
            elif widgettipo == "booleanos":
                widget = booleanos.BoolWidget(self.idioma)
            elif widgettipo == "Fechas":
                widget = FechaWidget.FechaWidget(self.idioma)
                
            elif widgettipo == "DireccionIP":
                widget = IP.IPWidget(self.idioma)
                
            elif widgettipo == "Pais":
                widget = Pais.PaisWidget(self.idioma)
                
            elif widgettipo == "codigoBarra":
                widget = codigobarras.BarraWidget(self.idioma)
                
            elif widgettipo == "Color":
                widget = Color.ColorWidget(self.idioma)
                
            elif widgettipo == "Instituciones":
                widget = instituciones.InstitucionesWidget(self.idioma)
                
            elif widgettipo == "ISBN":
                widget = ISBN.ISBNWidget(self.idioma)
                
            elif widgettipo == "Otros":
                widget = Otros.OtrosWidget(self.idioma)
        if widget:
            self.widgets_creados.append(widget)
            print(self.widgets_creados)
            return widget
    #prueba pa el futuro
    def comprobarWidget(self,widgettipo):
        if widgettipo =="booleanos" or widgettipo == "Numeros": 
            return False
        if widgettipo not in self.clave:
            self.clave.append(widgettipo)
            return False
        else:
            return True
    def generar_boton(self, widget, widgetnombre):
        # Verificar si ya existe un widget del mismo tipo en el cuerpo derecho
        if  self.comprobarWidget(widgetnombre): 
            return
        widget_compuesto = self.generar_widget(widgetnombre)
        if widgetnombre != "booleanos" and widgetnombre !="Numeros":
            for i in range(widget.layout().count()):
                existing_widget = widget.layout().itemAt(i).widget().findChild(QLabel)
                label2 = widget_compuesto.findChild(QLabel)
                if existing_widget.text() == label2.text() and existing_widget.text() :
                    # Si ya existe un widget del mismo tipo, no hacer nada
                    return
                else:
                    print("False")

        
        # Establecer la política de tamaño horizontal del widget compuesto como Expanding
        widget_compuesto.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        # Agregar el widget compuesto al layout del widget pasado como argumento
        widget.layout().addWidget(widget_compuesto)
        
        
    def limpiar_cuerpo_derecho(self, widget):
        # Eliminar todos los widgets del layout del cuerpo derecho
        for i in reversed(range(widget.layout().count())):
            widget.layout().itemAt(i).widget().setParent(None)
        self.widgets_creados = []
        self.clave=[]
    #filtro simple
    def filtrar_nombres(self, texto_filtro, botones):
        for boton in botones:
            nombre_boton = boton.text()#coje el nombre del texto
            #cada vez que se cambia comprueba si tiene el mismo nombre que del line edit
            if texto_filtro.lower() in nombre_boton.lower():
                boton.setVisible(True)
            else:
                boton.setVisible(False)
    def traduci(self,index,botones,botons,textlines,json):
            i = 0
            
            botonss = ["Otros","Borrar","Confirmar"]
            textos = ["Buscador","Cantidad"]
            if  index == 0:
                json = json["Español"]
            elif index == 1:
                json = json["English"]
            self.idioma = self.comboboxIdiomas.currentText()
            
            for boton in botones:
                boton.setText(json[self.claves_espanol[i]])
                i+=1
            i= 0
            for boton in botons:
                boton.setText(json[botonss[i]])
                i+=1
            i=0
            for text in textlines:
                text.setPlaceholderText(json[textos[i]])
                i+=1
            for widget in  self.widgets_creados:
                widget.traducir(self.idioma)
    def Confirm(self, widget):
        try:
            if widget.count() > 0:
                lista = []
                for i in range(widget.count()):
                    layout_item = widget.itemAt(i).widget().findChild(QLabel)
                    
                    if isinstance(layout_item,QLabel):
                        for i in range(0,len(self.widgets_creados)):
                            dat = self.widgets_creados[i].getData(1000)

                            lista.append(dat)
                                    
                print(lista)
        except error.ErrorPrograma as e:
            QMessageBox.warning(self,"Error",e.mensaje)
       

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
