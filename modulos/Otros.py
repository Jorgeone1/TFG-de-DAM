from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QCheckBox, QFrame, QFileDialog, QMessageBox
import json,random,sys
import pandas as pd
from modulos import error
class OtrosWidget(QWidget):
    """
    Clase que genera un widget con sus componentes en el cual el usuario subirá un archivo CSV o Excel y de este generará datos.
    """
    def __init__(self, idiomas):
        """
        Inicia el widget y sus componentes más las propiedades.
        Args:
            idiomas (String): Recoge el idioma en el cual el widget estará traducido.
        """
        super().__init__()
        # Guardamos el idioma y abrimos el JSON
        self.idioma = idiomas
        with open('./idiomas/otros.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]

        # Crear elementos del widget
        self.label = QLabel(self.datas["otros"], self)
        self.editline = QLineEdit(self)
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
        self.editline.setEnabled(False)
        # Crear un QFrame sin un padre específico
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)  # Establecer la forma del marco
        self.frame.setLineWidth(2)  # Establecer el ancho del borde

        # Establecemos un layout al frame
        layout = QGridLayout()
        self.frame.setLayout(layout)

        # Agregamos los elementos al frame
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.editline, 0, 1)

        # Crear el layout principal
        widget_creado = QGridLayout(self)
        widget_creado.addWidget(self.frame, 0, 0)

        # Almacenar los datos del archivo
        self.datadict = {}
        archivo, _ = QFileDialog.getOpenFileName(self, self.datas["Abrir"], "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)")
        self.lineas = []
        self.boxes = []
        if archivo:
            try:
                if archivo.endswith('.csv'):
                    df = self.load_csv(archivo)
                else:
                    df = pd.read_excel(archivo)

                self.llenarfilas(df)
            except Exception as e:
                raise error.ErrorPrograma(self.datas["error1"])
    def traducir(self,nuevoidioma):
        """
        Método para traducir el contenido del widget al nuevo idioma
        Args:
            nuevo_idioma (str): Nuevo idioma al cual se traducirá el contenido del widget
        """
        self.idioma= nuevoidioma
        self.datas = self.datos[self.idioma]
        self.label.setText(self.datas["otros"])
        self.editline.setPlaceholderText(self.datas["NombreProyecto"])
    def load_csv(self, file_path):
        """
        Metodo que comprueba el estado del csv, debido a que puede tener diferenten encodificacion,
        y el dato que los delimita de cada columna o fila es distinta

        Args:
            file_path (string): path completo del archivo

        Raises:
            error.ErrorPrograma: devuelve un error en caso de que no haya podido posible abrirlo

        Returns:
            panda: devuelve el archivo abierto con sus tablas y columnas
        """        
        delimiters = [',', ';', '\t']
        encodings = ['utf-8', 'ISO-8859-1']

        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
                except pd.errors.ParserError:
                    continue
                except UnicodeDecodeError:
                    break
        raise error.ErrorPrograma(self.datas["error2"])
    def llenarfilas(self, df):
        """
        Metodo que rellena el widget con un checkbox y un editline para que el usuario pueda seleccionar
        que datos quiere imprimir y cuales no

        Args:
            df (panda): archivo abierto con las columnas y sus datos
        """        
        #coje la cantidad de filas
        layout = self.frame.layout()
        startrow = layout.rowCount()

        for col in df.columns:
            #crea un checkbox y lineedit
            checkbox = QCheckBox(col)
            editline = QLineEdit()

            #los añade a un array para lueg ocomrpobarlo
            self.boxes.append((checkbox,editline,col))
            editline.setPlaceholderText(self.datas["NombreProyecto"])

            #los añade al widget
            layout.addWidget(checkbox, startrow, 0)
            layout.addWidget(editline, startrow, 1)

            #guarda los datos en diccionario y pasa a la siguiente fila
            self.datadict[col] = df[col].tolist()
            startrow += 1

    def getData(self, cantidad):
        """
            Devuelve una lista de datos recogida en el RESTAPI
        Args:
            cantidad (int): Cantidad de datos que quiere devolver

        Returns:
            dict: devuelve un diccionario con los datos elegidos
        """
        dicts = {}
        # Aquí puedes procesar self.datadict según lo que necesites hacer
        for checkbox,editline,col in self.boxes:
            dato = editline.text() or col
            if checkbox.isChecked():
                dicts[dato] = random.choices(self.datadict[col],k=cantidad)
        return dicts

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = OtrosWidget("ES")
    mainWindow.show()
    sys.exit(app.exec())