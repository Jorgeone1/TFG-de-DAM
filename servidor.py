from flask import Flask, jsonify
import pymongo,json,hashlib,random,string,requests
import sqlite3 as sq
from bs4 import BeautifulSoup
from faker import Faker
app = Flask(__name__)

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["GeneradorDeDatos"]

# Cargar datos de nombres una sola vez
@app.route("/nombres/<genero>/<idioma>/<int:cantidad>")
def generarNombre(genero, idioma, cantidad):
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

    dicts = {"names": noms, "Apellido": ape, "Genero": gen}
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
        ciudad.append(faker.region())
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
            else:
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
@app.route("/imagenes/<buscar>/<idioma>")
def getImagenes(buscar,idioma):
    urls = [f'https://unsplash.com/es/s/fotos/{buscar}',f"https://stock.adobe.com/es/search?k={buscar}&search_type=usertyped"
               ,f"https://depositphotos.com/es/photos/{buscar}.html?filter=all"
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

@app.route("/coches/<int:cantidad>/<idioma>")
def generarCoches(cantidad,idioma):
    # Selecciona la base de datos según el idioma
    db_path = f"./datos/Sqlite/Coches{idioma}.db" 

    # Conecta a la base de datos
    conectar = sq.connect(db_path)
    cursor = conectar.cursor()

    # Genera una lista de 1000 números aleatorios
    numeros_aleatorios = [random.randint(1, 12539) for i in range(cantidad)]
    placeholders = ', '.join('?' for i in numeros_aleatorios)
    print(len(numeros_aleatorios))
    # Ejecuta una sola consulta para obtener los 1000 coches
    query = f"""
    SELECT Coches.modelo, Coches.tipo, Marca.nombre
    FROM Coches
    INNER JOIN Marca ON Coches.id_coche = Marca.id
    WHERE Coches.id IN ({placeholders})
    """
    cursor.execute(query, numeros_aleatorios)
    dicts  = {"modelo":[],"tipo":[],"marca":[]}
    # Obtiene todos los datos de una sola vez
    datos = cursor.fetchall()
    print(datos)
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
if __name__ == '__main__':
    app.run(debug=True)