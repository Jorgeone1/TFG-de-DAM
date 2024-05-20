from flask import Flask, jsonify
import pymongo,json,hashlib,random,string,requests
from PIL import ImageColor
import sqlite3 as sq
from bs4 import BeautifulSoup
from faker import Faker
from datetime import *
app = Flask(__name__)

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["GeneradorDeDatos"]

# Cargar datos de nombres una sola vez
@app.route("/nombres/<genero>/<idioma>/<int:cantidad>/<dominio>")
def generarNombre(genero, idioma, cantidad,dominio):
    """
    Método que genera nombres y apellidos y los imprime en la ruta de arriba /nombres/<genero>/<idioma>/<int:cantidad>/<dominio>
    

    Args:
        genero (string): valor que puede ser - M F representa un tipo de datos la cual se quiere sacar
        idioma (string): idioma en la que se salga debido a que los ingleses tienen un apellido
        cantidad (int): cantidad de datos a imprimir
        dominio (_type_): _description_

    Returns:
        _type_: _description_
    """    
    cursor = db["NombreEng"]
    cursor2 = db["Apellidos"]
    noms = []
    gen = []
    ape = []

    # Obtener todos los apellidos necesarios de una sola vez
    apellidos = list(cursor2.aggregate([{ "$sample": { "size": cantidad * 2 }}]))
    apellidos = [ap["name"] for ap in apellidos]

    # Obtener todos los nombres necesarios de una sola vez
    if genero == "-":
        nombres = cursor.aggregate([{ "$sample": { "size": cantidad }}])
    else:
        nombres = cursor.aggregate([
            { "$match": { "gender": genero }},
            { "$sample": { "size": cantidad }}
        ])

    nombres = list(nombres)

    # Organizar los nombres y apellidos en la respuesta
    for i in range(cantidad):
        #como es el doble de grande los apellidos, ap cogera los pares, y el ap2 impares
        ap = apellidos[i*2]
        ap2 = apellidos[i*2 + 1] if idioma == "ES" else ""
        apellido = f"{ap} {ap2}".strip()
        ape.append(apellido)
        
        nom = nombres[i]
        noms.append(nom["name"])
        gen.append(nom["gender"])
    correo = []
    for i in range(0,len(noms)):
        correo.append(noms[i]+ape[i].replace(" ","")+f"@{dominio}.com")
    dicts = {"names": noms, "Apellido": ape, "Genero": gen,"correo":correo}
    return jsonify(dicts)

@app.route("/direccion/<idioma>/<int:cantidad>")
def getDirecciones(idioma,cantidad):
    if idioma == "ES":
        faker = Faker("es_ES")
    if idioma== "EN":
        faker = Faker("en_GB")

    direccion = []
    codigoPostal = []
    ciudad = []
    provincias = []
    for i in range(cantidad):
        direccion.append(faker.address())
        codigoPostal.append(faker.postcode())
        ciudad.append(faker.region()) if idioma == "ES" else ""
        provincias.append(faker.city())
    dicts = {"direccion":direccion,"Codigo": codigoPostal,"ciudad":ciudad,"Provincia":provincias}
    return jsonify(dicts)

def hash_password(password):
        # Convertir la contraseña a bytes
        password_bytes = password.encode('utf-8')

        # Crear un objeto hash usando SHA-256
        hash_object = hashlib.sha256()

        # Actualizar el objeto hash con la contraseña
        hash_object.update(password_bytes)

        # Obtener el hash resultante en formato hexadecimal
        hashed_password = hash_object.hexdigest()

        return hashed_password

@app.route("/contra/<int:cantidad>/<int:tamano>/<int:mayus>/<int:numer>/<int:espe>")
def generararContrasena(cantidad,tamano,mayus,numer,espe):
    Base = list(string.ascii_lowercase)
    list_password = [Base]
    lista = []
    hash = []
    passwords = {}
    # Array con todas las letras del abecedario en mayúscula
    if mayus:
        uppercase_letters = list(string.ascii_uppercase)
        list_password.append(uppercase_letters)
        
    # Array con los números del 0 al 9
    if numer:
        numbers = list(string.digits)
        list_password.append(numbers)
        
    # Array con teclas especiales comunes
    if espe:
        special_keys = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
        list_password.append(special_keys)
        
    for i in range(cantidad):
        text = ""
        for j in range(tamano):
            passs = random.choice(list_password)
            text = text + random.choice(passs)
            hashh = hash_password(text)
            hash.append(hashh)
        lista.append(text)
    passwords["Contra"] = lista
    passwords["hash"] = hash
    return jsonify(passwords)
                
@app.route("/dni/<int:cantidad>/<int:dni>/<idioma>")
def generaDNI(cantidad,dni,idioma):
    dnis = []
    for i in range(cantidad):
        letras= "TRWAGMYFPDXBNJZSQVHLCKE" #lista en orden de los codigos
        letnum={"X":"0","Y":"1","Z":"2"} #diccionario para sustituirlas letras en el dni
        letnum2={0:"X",1:"Y",2:"Z"}
        if(not dni):#Comprueba si el codigo que inserto el 
            if idioma == "ES":
                dninuevo= ""
                dninuevo = dninuevo + "".join(random.choices(string.digits,k=8))
                numeros = int(dninuevo[:8])-int((int(dninuevo[:8])/23))*23
                dninuevo = dninuevo + letras[numeros]
                dnis.append(dninuevo)
            elif idioma =="EN":
                dninuevo = "".join(random.choices(string.digits,k=9))
                dnis.append(dninuevo)
        else:#Comprueba si es un NIE
            if idioma == "ES":
                nie = letnum2[round(random.uniform(0,2))]
                nie = nie + "".join(random.choices(string.digits,k=7))
                
                numeros=int(letnum[nie[0].upper()]+nie[1:8])-(int(int(letnum[nie[0].upper()]+nie[1:8])/23)*23)
                dnis.append(nie + letras[numeros])
            elif idioma == "EN":
                nie = "".join(random.choices(string.ascii_uppercase,k=2)) + random.choice(string.digits + "X")+"".join(random.choices(string.digits,k=6))
                dnis.append(nie)
    dicts = {"dni":dnis}
    return jsonify(dicts)

@app.route("/telefono/<int:cantidad>/<idioma>")
def generarTelefono(cantidad,idioma):
    telefono = ""
    listat = []
    listam = []
    for i in range(cantidad):
        if idioma == "ES":
            telefono = "9"
            for i in range(8):
                telefono = telefono +str(round(random.uniform(0,9)))
            listat.append(telefono)
            rand = round(random.uniform(0,1))
            if rand == 0:
                telefono = "6"
            else:
                telefono="7"
            for i in range(8):
                telefono = telefono +str(round(random.uniform(0,9)))
            listam.append(telefono)
        elif idioma == "EN":
            telefono = ""
            telefono = "01"
            for i in range(9):
                telefono = telefono + str(round(random.uniform(0,9)))
            listat.append(telefono)
            telefono = "07"
            for i in range(9):
                telefono = telefono + str(round(random.uniform(0,9)))
            listam.append(telefono)
    return jsonify({"fijo":listat, "mobil":listam})
@app.route("/imagenes/<buscar>")
def getImagenes(buscar):
    urls = [f'https://unsplash.com/es/s/fotos/{buscar}',f"https://stock.adobe.com/es/search?k={buscar}&search_type=usertyped"
               ]
    lista = []
    for url in urls:
        # Realiza una solicitud HTTP para obtener el contenido de la página
        response = requests.get(url)
        
        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            # Parsea el contenido HTML de la página
            soup = BeautifulSoup(response.text, 'html.parser')
                
            # Encuentra todas las etiquetas "img" en la página
            img_tags = soup.find_all('img')
            hola = ""
            # Itera a través de las etiquetas "img" y obtén el atributo "src"
            for img_tag in img_tags:
                src = img_tag.get('src')
                if src:
                    if "secure" not in src and "betrad" not in src:
                        lista.append(src)     
        else:
            print("No se pudo acceder a la página",url)
    return jsonify({"imagenes":lista})
@app.route("/matricula/<int:cantidad>/<idioma>")
def getMatricula(cantidad,idioma):
    
    opciones = ['AA', 'AN', 'AD', 'UK', 'AO', 'AU', 'AO', 'UK', 'AV', 'AY', 'AV', 'UK', 'BA', 'BY', 'CA', 'CO', 'CK', 'GB', 'CP', 'CV', 'CT', 'GB', 'CW', 'CY', 'DA', 'DK', 'DI', 'GB', 'DL', 'DY', 'DX', 'GB', 'EA', 'EY', 'EJ', 'GB', 'FA', 'FP', 'FG', 'GB', 'FR', 'FY', 'FY', 'GB', 'GA', 'GO', 'GL', 'GP', 'GY', 'GV', 'HA', 'HJ', 'HF', 'HK', 'HY', 'KA', 'KL', 'KM', 'KM', 'KY', 'KR', 'LA', 'LJ', 'LK', 'LT', 'LR', 'GB', 'LU', 'LY', 'LX', 'GB', 'MA', 'MY', 'MW', 'GB', 'NA', 'NO', 'NP', 'NY', 'OA', 'OY', 'PA', 'PT', 'PU', 'PY', 'RA', 'RY', 'SA', 'SJ', 'SK', 'SO', 'SP', 'ST', 'SU', 'SW', 'SX', 'SY', 'VA', 'VY', 'WA', 'WJ', 'WK', 'WL', 'WL', 'WM', 'WY', 'YA', 'YK', 'YL', 'YU', 'YV', 'YY']
    matriculas = []
    for i in range(cantidad):
        mat = ""
        if idioma == "ES":
            mat = "".join(random.choices(string.digits,k=4)) + "".join(random.choices([digit for digit in string.ascii_uppercase if digit != "Q"],k=3))
            matriculas.append(mat)
        elif idioma=="EN":
            mat = "".join(random.choice(opciones)) + "".join(random.choices(string.digits,k=2)) + "".join(random.choices(string.ascii_uppercase,k=3))
            matriculas.append(mat)
    return jsonify({"matricula":matriculas})

@app.route("/coches/<tipo>/<int:cantidad>/<idioma>")
def generarCoches(tipo,cantidad,idioma):
    # Selecciona la base de datos según el idioma
    db_path = f"./datos/Sqlite/Coches{idioma}.db" 

    # Conecta a la base de datos
    conectar = sq.connect(db_path)
    cursor = conectar.cursor()
    if tipo == "-":
        # Genera una lista de números aleatorios
        numeros_aleatorios = [random.randint(1, 12539) for i in range(cantidad)]
        placeholders = ', '.join('?' for i in numeros_aleatorios)

        # Ejecuta una sola consulta para obtener los 1000 coches
        query = f"""
        SELECT Coches.modelo, Coches.tipo, Marca.nombre
        FROM Coches
        INNER JOIN Marca ON Coches.id_coche = Marca.id
        WHERE Coches.id IN ({placeholders})
        """
        cursor.execute(query, numeros_aleatorios)
    else:
        query = f"""
        SELECT Coches.modelo, Coches.tipo, Marca.nombre
        FROM Coches
        INNER JOIN Marca ON Coches.id_coche = Marca.id
        WHERE Marca.nombre = ?
        ORDER BY RANDOM()
        LIMIT ?
        """
        cursor.execute(query, (tipo, cantidad))

    dicts  = {"modelo":[],"tipo":[],"marca":[]}
    # Obtiene todos los datos de una sola vez
    datos = cursor.fetchall()
    for dato in datos:
        dicts["modelo"].append(dato[0])
        dicts["tipo"].append(dato[1])
        dicts['marca'].append(dato[2])
    
    conectar.close()
    return jsonify(dicts)

def generar_prefijo():
    while True:
        #genera lista sin las letras prohibidas
        letrasvalidas = [letra for letra in string.ascii_uppercase]
        primerletra = random.choice(letrasvalidas)
        #lo mismo pero añadiendo la o
        letraval= [ letra for letra in letrasvalidas if letra != 'O']
        segundaletra = random.choice(letraval)
        # Comrpueba que la primera letra y segunda no hagan un combo que este prohibido
        prefijo = primerletra + segundaletra
        if not prefijo in ('BG', 'GB', 'KN', 'NK', 'NT', 'TN', 'ZZ'):
            return prefijo
        else:
            print("error")
@app.route("/segsol/<int:cantidad>/<idioma>")
def comprobarNaf(cantidad,idioma):
    lista = []
    for i in range(cantidad):
        if idioma == "ES":
            naf = "28"
            naf += ''.join(random.choices(string.digits, k=8))
            if(int(naf[2:10])<10000000):#comprueba si los numeros del medio supera los 
                numeros=((int(naf[:1])+int(naf[2:10]))*10000000)%97       
            else:
                numeros=int((int(naf[:10]))%97)#sino realizara otro tipo de operación
            cero = ""
            if numeros < 10:
                cero = "0"
             
            naf = naf +cero + str(numeros)       
            lista.append(naf)
        elif idioma =="EN":
            seg = generar_prefijo()
            seg += "".join(random.choices(string.digits, k=6))
            seg += random.choice(["A","B","C","D"])
            lista.append(seg)
    return jsonify({"seguridad":lista})

@app.route("/id/<int:comenzar>/<formato>/<int:incrementar>/<int:cantidad>")
def generarID(comenzar,formato,incrementar,cantidad):
    lista = []
    hola = ""
    for i in range(0,cantidad):
        if formato == "null":            
            lista.append(comenzar)
        else:
            lista.append(formato.format(str(comenzar)))
        comenzar += incrementar
    return jsonify({"id":lista})



    #operaciones del primer digito
def primerDigito(entidad,num1):
    numeros=0
    for po in range(0,8): #for que realiza las operaciones
        numeros= numeros + (int(entidad[po])*num1[po])
    resto=numeros%11
    if(resto == 1 ):
        return 1
    elif resto == 0:
        return 0
    else:
        return int(11- resto)
        
    #Operaciones con el segundo digito
def segundoDigito(codigocuenta,num2):
    numeros2=0
    for pi in range(0,len(num2)): # for que realiza las operaciones
        numeros2= numeros2 + (int(codigocuenta[pi])*num2[pi])
    resto2=11-(numeros2%11)
    if(resto2==10):
        return 1
    elif resto2 == 11:
        return 0
    else:
        return resto2
        
def CreadorIBAN(cuenta):
    total=cuenta+"142800" 
    numerosiban=98-(int(total)%97) #realiza la operación para calcular los numeros de despues del ES
    if(len(str(numerosiban))==1):
        numerosiban="0" + str(numerosiban) #Crea un iban pero con los numeros creados por las operaciones 
    iban="ES"+str(numerosiban)+cuenta
    return iban
@app.route("/IBAN/<int:cantidad>")
def comprobarIBAN(cantidad):
    ccclista = []
    ibanlista =[]
    for i in range(cantidad):
        entidad = ""
        codigocuenta = ""
        entidad = entidad + "".join(random.choices(string.digits,k=8))
        codigocuenta =codigocuenta+ "".join(random.choices(string.digits,k=10))

        num1=[4,8,5,10,9,7,3,6] #Guarda las operaciones para el primer digito en orden
        num2=[1,2,4,8,5,10,9,7,3,6] #Guarda las operaciones del segundo digito en orden
            
        digito1=primerDigito(entidad,num1) #Realiza las operaciones del digito 1
        digito2=segundoDigito(codigocuenta,num2) #Realiza las operaciones del digito 2
        total= f"{digito1}{digito2}" #los junta
        ccc =  entidad + total + codigocuenta   #devuelve un booleano si coinciden o no
        ccclista.append(ccc)
        ibanlista.append(CreadorIBAN(ccc))
    return jsonify({"ccc":ccclista,"iban":ibanlista})
@app.route("/Empresa/<provincia>/<int:cantidad>/<idioma>")
def generarEmpresa(provincia,cantidad,idioma):
    # Establecer conexión con el servidor de MongoDB
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    # Seleccionar la base de datos
    db = cliente["Empresas"][f"Empresas{idioma}"]
    if provincia == "-":
        data = list(db.aggregate([{ "$sample": { "size": cantidad }}]))
    else:
            data = list(db.aggregate([
            { "$match": { "provincia": provincia} },  # Filtrar por género "M"
            { "$sample": { "size": cantidad } }       # Seleccionar un documento aleatorio
            ]))
    datos = {"nombre":[],"direccion":[],"provincia":[],"contacto":[]}
    var = "telefono" if idioma == "EN" else "web"
    for datas in data:
        datos["nombre"].append(datas["nombre"])
        datos["direccion"].append(datas["direccion"])
        datos['provincia'].append(datas["provincia"])
        datos["contacto"].append(datas[var])
    return jsonify(datos)

@app.route("/numeros/<int:entero>/<int:minimo>/<int:maximo>/<int:decimales>/<int:cantidad>")
def getNum(entero,minimo,maximo,decimales,cantidad):
    lista = []
    for i in range(cantidad):
        num = 0
        if entero:
            num = round(random.uniform(float(minimo),float(maximo)))
        else:
            num = round(random.uniform(float(minimo), float(maximo)), decimales)
        lista.append(num)
    return jsonify({"numeros":lista})

@app.route("/booleanos/<nomtrue>/<nomfalse>/<int:cantidad>")
def generarBooleanos(nomtrue,nomfalse,cantidad):
    lista = []
    for i in range(cantidad):
        sel = random.choice([True,False])
        if sel:
            lista.append(nomtrue)
        else:
            lista.append(nomfalse)
    return jsonify({"booleanos": lista})

def fechaaleatoria(fechainicio, fechafin):
        diferencia = fechafin - fechainicio
        dias = random.randint(0, diferencia.days)
        return fechainicio + timedelta(days=dias)
@app.route("/fechas/<int:largo>/<fechainicio>/<fechafinal>/<separador>/<int:cantidad>/<idioma>")
def generarFechas(largo,fechainicio,fechafinal,separador,cantidad,idioma):
    fechas = []
    dicts = {}
    with open('./idiomas/fechas.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    data = datos[idioma]
    for i in range(cantidad):
        fechas.append(fechaaleatoria(datetime.strptime(fechainicio,"%d-%m-%Y"),datetime.strptime(fechafinal,"%d-%m-%Y")))
    for i in range(len(fechas)):
        if largo:
            mes = fechas[i-1].strftime(f"%m")
            fechas[i-1] = fechas[i-1].strftime(f"%d de {data[mes]} %Y")
        else:
            fechas[i-1] = fechas[i-1].strftime(f"%d{separador}%m{separador}%Y")
    dicts["fecha"] = fechas
    return jsonify(dicts)

def crearIPV4():
    ipv4 = []
    for i in range(4):
        ipv4.append(str(random.randint(0,255)))
    return ".".join(ipv4)
    
def crearIPV6():
    ipv6 = []
    lista = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","F"]
    for i in range(8):
        digito = ""
        for k in range(4):
            digito = digito + random.choice(lista)
        ipv6.append(digito)
    return ":".join(ipv6)
@app.route("/IP/<int:ip6>/<int:cantidad>")
def getIp(ip6,cantidad):
    lista = []
    for i in range(cantidad):
        if ip6:
            lista.append(crearIPV6())
        else:
            lista.append(crearIPV4())
    
    return jsonify({"ip":lista})

@app.route("/pais/<continentes>/<int:cantidad>/<idioma>")
def getPais(continentes,cantidad,idioma):
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["GeneradorDeDatos"][f"Pais{idioma}"]
    if continentes == "-":
        data = list(db.aggregate([{ "$sample": { "size": cantidad }}]))
    else:
        data = db.aggregate([
            { "$match": { "continente": continentes} },  # Filtrar por género "M"
            { "$sample": { "size": cantidad } }       # Seleccionar un documento aleatorio
            ])
    dato = {"pais":[],"continente":[],"capital":[]}
    for dat in data:
        dato["pais"].append(dat["pais"])
        dato["continente"].append(dat["continente"])
        dato["capital"].append(dat["capital"])
    
    return jsonify(dato)

        
def Calcular_ultimo_digito(barra):
    pares = 0
    impares = 0
    #si es par suma el valor multiplicado por 2 y si es impar solo suma
    for i in range(0,len(barra)):
        if i % 2 == 0:
            pares += (int(barra[i]) * 2)
        else:
            impares += int(barra[i]) 
    #devuelve el valor sumado y restado por el resto entre 10 del resultado
    num = 10 - ((pares + impares)%10)
    if num == 10: 
        return 0
    else:
        return num
@app.route("/codigobarras/<int:UPC>/<int:cantidad>")
def generar_barrar(UPC,cantidad):
    barras = []
    #creamos un codigo de barra
    for i in range(cantidad):
        barra = ""
        rango = 0
        #comprueba si esta checkeada o no
        rango = 11 if UPC else 12
        for i in range(rango):
            barra = barra + str(random.randint(0,9))
        
        #saca el codigo de verificacion
        barra = barra + str(Calcular_ultimo_digito(barra))
        barras.append(barra)
    return jsonify({"barra":barras})

def hex_to_rgb(hex_color):
    #calcula el rgba del hex
    rgba_tuple = ImageColor.getcolor(hex_color, "RGBA")
    return rgba_tuple[:3]  # Tomamos los primeros tres valores (RGB)
    
def CrearHex():
    hex = "#"
    lista = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","F"] #Posibles numeros
    for i in range(6):
        hex = hex + random.choice(lista)
    return hex
@app.route("/color/<int:cantidad>")
def generarColor(cantidad):
    listaHex = []
    listaRGB = []
    for i in range(cantidad):
        colo = CrearHex()
        listaHex.append(colo)
        listaRGB.append(hex_to_rgb(colo))
    return jsonify({"hex":listaHex,"rgb":listaRGB})

@app.route("/instituciones/<int:Colegio>/<Comunidad>/<int:cantidad>/<idioma>")
def getInstitution(Colegio,Comunidad,cantidad,idioma):
    with open('./idiomas/instituciones.json', 'r', encoding='utf-8') as archivo:
        datosInstitucion = json.load(archivo)
    data = datosInstitucion[idioma]
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["Instituciones"]
    if Colegio==0:
        dd = db[data["Colegio"]]
    else:
        dd = db[data["Universidad"]]
    if Comunidad == "-":
        datoss = list(dd.aggregate([{ "$sample": { "size": cantidad }}]))
    else:
        datoss = list(dd.aggregate([
            { "$match": { "TOWN": Comunidad} },  # Filtrar por género "M"
            { "$sample": { "size": cantidad } }       # Seleccionar un documento aleatorio
            ]))
    dataa = {"name":[],"area":[],"address":[]}
    for dat in datoss:
        dataa["name"].append(dat["name"])
        dataa["area"].append(dat["TOWN"])
        if Colegio != 1 or idioma != "EN":  
            dataa["address"].append(dat["Street"])
    return jsonify(dataa)
def isbnCodigoControl(isbn):
    suma = 0
    for i in range(0,len(isbn)):
        if i % 2 == 0:
            suma += int(isbn[i])
        else:
            suma += int(isbn[i]) * 3
    num = 10-(suma%10)
    if num == 10:
        return 0
    else:    
        return num
@app.route("/ISBN/<int:cantidad>/<idioma>")
def generarISBN(cantidad,idioma):
    lista =[]
    for i in range(cantidad):
        codigopais = ""
        if idioma == "ES":
            codigopais = "84"
        if idioma =="EN":
            codigopais = random.choice(["00","01"])
        isb = random.choice(["978","979"]) + "-"+ codigopais +"-"+"".join(random.choices(string.digits,k = 5)) + "-" + "".join(random.choices(string.digits,k=2))
        isbn = isb.replace("-","")
        isb +="-" + str(isbnCodigoControl(isbn))
        lista.append(isb)
    return jsonify({"isbn":lista})

if __name__ == '__main__':
    app.run(debug=True)