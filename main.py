import sys,json
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QLineEdit, QScrollArea, QComboBox,QSizePolicy, QFrame
from modulos import Salida,error,booleanos,ccc,coche,codigobarras,Color,contras,direccion, Dni,Empresa,FechaWidget,imagenes,instituciones,IP,ISBN,Matricula,nombres,Numero,Otros,Pais,SegSol,telefono,id
from functools import partial
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

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
        self.widgets_creados = []
        self.textolineas = []
        self.botones = []
        self.botons = []
        self.clave = []
        self.claves_espanol = [
            "nombre", "direccion", "contraseña", "dni", "telefonos", 
            "imagenes", "Matricula", "coches", "SeguridadSocial", "id",
            "CCC", "Empresa", "Numeros", "booleanos", "Fechas", "DireccionIP", 
            "Pais", "codigoBarra", "Color", "Instituciones", "ISBN"
        ]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.partePrincipal = QGridLayout()
        central_widget.setLayout(self.partePrincipal)
        with open('./idiomas/español.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datosesp = self.datos["ES"]

        # Widget central izquierdo
        self.widget_central_izquierdo = QWidget()
        self.izquierdo = QVBoxLayout()
        self.widget_central_izquierdo.setLayout(self.izquierdo)
        self.partePrincipal.addWidget(self.widget_central_izquierdo, 1, 0)

        # Ajuste de tamaño del QLineEdit
        self.buscadorBoton = QLineEdit()
        self.buscadorBoton.setFixedHeight(20)
        self.buscadorBoton.setPlaceholderText(self.datosesp["Buscador"])
        self.izquierdo.addWidget(self.buscadorBoton)
        self.textolineas.append(self.buscadorBoton)

        # Área de desplazamiento y QVBoxLayout
        self.scrollArea = QScrollArea()
        self.widgetCuerpoIzquierda = QWidget()
        self.VLayoutCuerpoIzq = QVBoxLayout()
        self.widgetCuerpoIzquierda.setLayout(self.VLayoutCuerpoIzq)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widgetCuerpoIzquierda)
        self.izquierdo.addWidget(self.scrollArea)

        # Establecer el estiramiento del QVBoxLayout del lado izquierdo
        self.partePrincipal.setColumnStretch(0, 1)

        # Widget derecho
        self.Widget_derecho = QWidget()
        self.layout_derecho = QVBoxLayout()
        self.Widget_derecho.setLayout(self.layout_derecho)
        self.partePrincipal.addWidget(self.Widget_derecho, 1, 1)

        # Botón de borrar, ComboBox de idioma, Área de desplazamiento, etc.
        self.arriba_derecha_widget = QWidget()
        self.layout_arriba_derecho = QGridLayout()
        self.arriba_derecha_widget.setLayout(self.layout_arriba_derecho)
        self.layout_derecho.addWidget(self.arriba_derecha_widget)

        
        # Widget de borrar y idiomas
        self.BotonBorrar = QPushButton(self.datosesp["Borrar"])
        self.BotonBorrar.clicked.connect(lambda: self.limpiar_cuerpo_derecho(self.cuerpoDerechoWidget))
        self.botons.append(self.BotonBorrar)
        self.layout_arriba_derecho.addWidget(self.BotonBorrar, 0, 0)

        self.comboboxIdiomas = QComboBox()
        self.layout_arriba_derecho.addWidget(self.comboboxIdiomas, 0, 2)
        comboIdiomas = ["ES", "EN"]
        self.comboboxIdiomas.addItems(comboIdiomas)

        # Área de desplazamiento para el cuerpo derecho
        self.scrollAreaL = QScrollArea()
        self.scrollAreaL.setWidgetResizable(True)
        self.layout_derecho.addWidget(self.scrollAreaL)

        # Widget para el cuerpo derecho
        self.cuerpoDerechoWidget = QWidget()
        self.Vderecho = QVBoxLayout()
        self.cuerpoDerechoWidget.setLayout(self.Vderecho)
        self.scrollAreaL.setWidget(self.cuerpoDerechoWidget)

        # Widget abajo de derecha
        self.abajo_derecha = QWidget()
        self.layout_abajo_derecha = QGridLayout()
        self.abajo_derecha.setLayout(self.layout_abajo_derecha)
        self.layout_derecho.addWidget(self.abajo_derecha)

        # Botón confirmar y combobox de formato de salida
        self.botonConfirmar = QPushButton(self.datosesp["Confirmar"])
        self.botonConfirmar.clicked.connect(lambda: self.Confirm(self.layout_derecho))
        self.botons.append(self.botonConfirmar)
        self.layout_abajo_derecha.addWidget(self.botonConfirmar, 0, 0)

        # Cuadro de texto para escribir la cantidad
        self.cantidad_numero = QLineEdit()

        #Regular expresion para limitar el cantidad_numero
        regex = QRegularExpression(r'^\d{0,3}$')
        validator = QRegularExpressionValidator(regex, self.cantidad_numero)
        self.cantidad_numero.setValidator(validator)
        #Mas propiedades
        self.layout_abajo_derecha.addWidget(self.cantidad_numero, 0, 1)
        self.cantidad_numero.setFixedHeight(20)
        self.cantidad_numero.setPlaceholderText(self.datosesp["Cantidad"])
        self.textolineas.append(self.cantidad_numero)

        #cuadro de texto para el nombre de la app
        self.nombretable = QLineEdit()
        self.layout_arriba_derecho.addWidget(self.nombretable,0,1)
        self.textolineas.append(self.nombretable)
        self.nombretable.setPlaceholderText(self.datosesp["Titulo"])

        # Combobox para elegir el formato de salida
        self.comboboxFormato = QComboBox()
        self.layout_abajo_derecha.addWidget(self.comboboxFormato, 0, 2)
        formatoarray = ["XML", "JSON", "CSV", "SQL", "XLSX"]
        self.comboboxFormato.addItems(formatoarray)
        
        # Conectar la señal textChanged del QLineEdit al método de filtro
        self.buscadorBoton.textChanged.connect(lambda text: self.filtrar_nombres(text, self.botones))
        #Boton Otros
        self.botonOtros = QPushButton(self.datosesp["Otros"])
        self.botonOtros.clicked.connect(partial(self.generar_boton, self.cuerpoDerechoWidget, "Otros"))
        self.partePrincipal.addWidget(self.botonOtros, 2, 0)
        self.botons.append(self.botonOtros)

        for i in range(len(self.claves_espanol)):
            boton = QPushButton(f"{self.datosesp[self.claves_espanol[i]]}")
            boton.setObjectName(f"Boton {i}")
            widgettipo = self.claves_espanol[i]
            boton.clicked.connect(partial(self.generar_boton, self.cuerpoDerechoWidget, widgettipo))
            self.botones.append(boton)
            self.VLayoutCuerpoIzq.addWidget(boton)

        # Establecer el ancho mínimo del Widget_derecho
        self.Widget_derecho.setMinimumWidth(self.widget_central_izquierdo.sizeHint().width())
        self.comboboxIdiomas.currentIndexChanged.connect(lambda index: self.traduci(index, self.botones, self.botons, self.textolineas))

        # Set the minimum width of the left and right columns and make them stretch equally
        self.partePrincipal.setColumnMinimumWidth(0, 200)
        self.partePrincipal.setColumnMinimumWidth(1, 200)
        self.partePrincipal.setColumnStretch(0, 1)
        self.partePrincipal.setColumnStretch(1, 1)
    def generar_widget(self, widgettipo):
        """
        Metodo que crea un objeto personalizado dependiendo del nombre del tipo

        Args:
            widgettipo (String): Nombre del boton

        Returns:
            QWidget: Devuelve un boton personalizado
        """        
        widget = None
        if widgettipo in self.claves_espanol or widgettipo == "Otros":
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
            return widget
    #prueba pa el futuro
    def comprobarRepetirWidget(self,widgettipo):
        """
        Comprueba que el widget este dentro de los que se puedan repetir o si no estan en el widget aun, si lo esta lo añade a un array
        y si no esta repetido lo deja pasar directamente

        Args:
            widgettipo (string): nombre del widget

        Returns:
            boolean: devuelve un booleano comprobando si esta bien o no
        """        
        if widgettipo =="booleanos" or widgettipo == "Numeros" or widgettipo =="Otros": 
            return False
        if widgettipo not in self.clave:
            self.clave.append(widgettipo)
            return False
        else:
            return True
        
    def generar_boton(self, widget, widgetnombre):
        """
        Metodo para generar un widget dependiendo del nombre y comprueba que no exista ya ademas de añadirle propiedades
        para que quepa en el layout
        Args:
            widget (QWidget): el widget donde insertar los modulos
            widgetnombre (String): nombre del widget 
        Raises:
            error.ErrorPrograma: recoge errores al crear los widget
        """        
        try:
            # Verificar si ya existe un widget del mismo tipo en el cuerpo derecho
            if  self.comprobarRepetirWidget(widgetnombre): 
                return
            
            #genera el widget
            widget_compuesto = self.generar_widget(widgetnombre)

            
            # Establecer la política de tamaño horizontal del widget compuesto como Expanding
            widget_compuesto.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

            # Agregar el widget compuesto al layout del widget pasado como argumento
            widget.layout().addWidget(widget_compuesto)
        except error.ErrorPrograma as e:
            QMessageBox.warning(self,"Error",e.mensaje)
        
    def limpiar_cuerpo_derecho(self, widget):
        """
        Limpia el cuerpo de los widgets introducidos

        Args:
            widget (QWidget):cuerpo que contiene los otros widget
        """        
        # Eliminar todos los widgets del layout del cuerpo derecho
        for i in reversed(range(widget.layout().count())):
            widget.layout().itemAt(i).widget().setParent(None)
        self.widgets_creados = []
        self.clave=[]
    #filtro simple
    def filtrar_nombres(self, textofiltro, botones):
        """
        Metodo que filtra los nombres dependiendo lo que escriba el usuario, se ira actualizando por palabra nueva

        Args:
            texto_filtro (String): texto a comprar
            botones (lista de botones): lista de botones
        """        
        for boton in botones:
            nombreboton = boton.text()#coje el nombre del texto
            #cada vez que se cambia comprueba si tiene el mismo nombre que del line edit
            if textofiltro.lower() in nombreboton.lower():
                boton.setVisible(True)
            else:
                boton.setVisible(False)
    def traduci(self, index, botones, botons, textlines):
        """
        Metodo que traduce cada vez que se cambia el idioma en el combobox

        Args:
            index (int): indice del combobox de idioma
            botones (array): lista de botones de seleccion
            botons (array): lista de botones especiales
            textlines (array): lista de cuadro de texto
        """            
        json = self.datos[self.comboboxIdiomas.currentText()]
        self.idioma = self.comboboxIdiomas.currentText()
            
        for i, boton in enumerate(botones):
            boton.setText(json[self.claves_espanol[i]])
            
        for i, boton in enumerate(botons):
            boton.setText(json[["Otros", "Borrar", "Confirmar"][i]])
            
        for i, text in enumerate(textlines):
            text.setPlaceholderText(json[["Buscador", "Cantidad","Titulo"][i]])
            
        for widget in self.widgets_creados:
            widget.traducir(self.idioma)
    def Confirm(self, widget):
        """
        Metodo que recoge la funcion getData de todos los widget en el cuerpo que los mantiene, la cual devolveran unos diccionarios
        y este los manejara en otra clase donde imprimiran el archivo dependiendo del formato
        Args:
            widget (_type_): cuerpo que contiene los widget

        Raises:
            error.ErrorPrograma: comprueba que el texto no este en blanco la de cantidad
            error.ErrorPrograma: comprueba que la descarga de datos esta en el limite permitido de cantidad
            error.ErrorPrograma: Comprueba que el widget del cuerpo mantenga mas de 1 widget para poder imprimir datos
        """        
        try:
            if not self.cantidad_numero.text():
                raise error.ErrorPrograma(self.datosesp["error1"])
            if 0<=int(self.cantidad_numero.text())>1000:
                raise error.ErrorPrograma(self.datosesp["error2"])
            if self.cuerpoDerechoWidget.layout().count()==0:
                raise error.ErrorPrograma(self.datosesp["error3"])
            titulo = self.nombretable.text() or self.datosesp["base"]
            if widget.count() > 0:
                lista = []
                for i in range(widget.count()):
                    layout_item = widget.itemAt(i).widget().findChild(QLabel)
                    
                    if isinstance(layout_item,QLabel):
                        for i in range(0,len(self.widgets_creados)):
                            dat = self.widgets_creados[i].getData(int(self.cantidad_numero.text()))

                            lista.append(dat)
                ruta = QFileDialog.getExistingDirectory(self, self.datosesp["seleccione"])
                programa = Salida.generarSalida(lista,self.comboboxFormato.currentText(),titulo,ruta,int(self.cantidad_numero.text()),self.comboboxIdiomas.currentText())
        except error.ErrorPrograma as e:
            QMessageBox.warning(self,"Error",e.mensaje)
       

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
