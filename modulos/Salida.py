import csv,json
from PyQt6.QtWidgets import QMessageBox
from modulos import error
import xml.etree.ElementTree as ET
from xml.dom import minidom
from openpyxl import Workbook
class generarSalida:
    def __init__(self,dicts,salida,titulo,ruta,cantidad,idioma):
        self.dicts = dicts
        self.salida = salida
        self.titulo = titulo.replace(" ","_")
        self.ruta = ruta
        self.idioma = idioma
        with open('./idiomas/salida.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)
        self.datas = self.datos[self.idioma]
        self.diccionario = {}
        self.cantidad = cantidad
        print("entre")
        for dicc in self.dicts:
            for indice,valor in dicc.items():
                self.diccionario[indice] = valor

        
        if self.ruta:
            
            if self.salida == "CSV":
                self.subir_csv()

            elif self.salida =="JSON":
                self.subir_json()
            elif self.salida =="XML":
                self.subir_xml()
            elif self.salida == "SQL":
                self.subir_sql()
            elif self.salida =="XLSX":
                self.subir_excel()
        else:
            raise error.ErrorPrograma(self.datas["error"])
        
    def subir_csv(self):
        """
        Metodo que convierte en un diccionario a un csv
        Raises:
            error.ErrorPrograma: recoge en caso que haya un error al crear el archivo
        """        
        try:
            
            self.rutacompleta = f"{self.ruta}/{self.titulo}.csv"
            encabezado = self.diccionario.keys()
            with open(self.rutacompleta, mode='w', newline='') as carpeta:
                writer = csv.writer(carpeta)
                writer.writerow(encabezado)  # Escribir encabezados

                # Escribir las filas
                for i in range(self.cantidad):
                    fila = [self.diccionario[key][i] for key in encabezado]
                    writer.writerow(fila)
            QMessageBox.information(None, self.datas["Subido"], f"{self.datas["Archivo"]}{self.rutacompleta}")
        except Exception as e:
            raise error.ErrorPrograma(f"{self.datas["crear"]}csv")
        
    def subir_json(self):
        """
        Metodo que convierte en un diccionario a un json
        Raises:
            error.ErrorPrograma: recoge en caso que haya un error al crear el archivo
        """      
        try:
            self.rutacompleta = f"{self.ruta}/{self.titulo}.json"
            listadicts = []

            # Obtener la longitud de las listas

            # Crear una lista de diccionarios
            for i in range(self.cantidad):
                filadict = {key: self.diccionario[key][i] for key in self.diccionario}
                listadicts.append(filadict)

            with open(self.rutacompleta, mode='w') as carpeta:
                json.dump(listadicts, carpeta, indent=4)
            QMessageBox.information(None, self.datas["Subido"], f"{self.datas["Archivo"]}{self.rutacompleta}")
        except Exception:
            raise error.ErrorPrograma(f"{self.datas["crear"]}JSON")
    def subir_xml(self):
        """
        Metodo que convierte en un diccionario a un xml
        Raises:
            error.ErrorPrograma: recoge en caso que haya un error al crear el archivo
        """      
        try:
            # Ruta completa del archivo XML
            self.rutacompleta = f"{self.ruta}/{self.titulo}.xml"
            
            # Crear el elemento raíz
            root = ET.Element(self.titulo)

            # Crear un elemento XML para cada fila
            for i in range(self.cantidad):
                item = ET.SubElement(root, "Columna")
                for indice in self.diccionario:
                    # Crear subelementos con llave y su valor, con el replace es para evitar los espacios
                    subelement = ET.SubElement(item, indice.replace(" ","_"))
                    subelement.text = str(self.diccionario[indice][i])
            
            # Convertir el xml en un string
            xmlbyte = ET.tostring(root, encoding='utf-8', xml_declaration=True)
            
            # Usar minidom que sirve para mejorar la visualizacion del xml en los archivos
            xmlstr = minidom.parseString(xmlbyte).toprettyxml(indent="  ")

            # Crea el xml con el string modificado
            with open(self.rutacompleta, 'w', encoding='utf-8') as f:
                f.write(xmlstr)
            QMessageBox.information(None, self.datas["Subido"], f"{self.datas["Archivo"]}{self.rutacompleta}")
        except Exception as e:
            raise error.ErrorPrograma(f"{self.datas["crear"]}XML: {e}")
    
    def subir_sql(self):
        """
        Metodo que convierte en un diccionario a un sql
        Raises:
            error.ErrorPrograma: recoge en caso que haya un error al crear el archivo
        """      
        try:
            # Ruta completa del archivo SQL
            self.rutacompleta = f"{self.ruta}/{self.titulo}.sql"
            
            # Crear el contenido del archivo SQL
            with open(self.rutacompleta, 'w', encoding='utf-8') as f:
                llaves = ",".join(self.diccionario.keys())
                # Insertar los datos
                for i in range(self.cantidad):
                    values = ", ".join([f"'{self.diccionario[key][i]}'" for key in self.diccionario.keys()])
                    insert = f"INSERT INTO {self.titulo}({llaves}) VALUES ({values});\n"
                    f.write(insert)
            
            QMessageBox.information(None, self.datas["Subido"], f"{self.datas["Archivo"]}{self.rutacompleta}")
        except Exception as e:
            raise error.ErrorPrograma(f"{self.datas["crear"]}SQL: {e}")
    
    def subir_excel(self):
        """
        Metodo que convierte en un diccionario a un sql
        Raises:
            error.ErrorPrograma: recoge en caso que haya un error al crear el archivo
        """      
        try:
            # Ruta completa del archivo Excel
            self.rutacompleta = f"{self.ruta}/{self.titulo}.xlsx"
            
            # Crear un libro de trabajo y una hoja
            workbook = Workbook()
            hoja = workbook.active
            hoja.title = self.titulo

            # Escribir encabezados
            encabezados = list(self.diccionario.keys())
            hoja.append(encabezados)

            # Escribir los datos
            for i in range(self.cantidad):
                fila = [self.diccionario[llave][i] for llave in self.diccionario]
                hoja.append(fila)
            
            # Guardar el archivo Excel
            workbook.save(self.rutacompleta)
            
            QMessageBox.information(None, self.datas["Subido"], f"{self.datas["Archivo"]}{self.rutacompleta}")
        except Exception as e:
            raise error.ErrorPrograma(f"{self.datas["crear"]}Excel: {e}")