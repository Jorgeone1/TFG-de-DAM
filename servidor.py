from flask import Flask, jsonify
import pymongo,json,hashlib,random,string
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
def generarDni(idioma,dni):
        letras= "TRWAGMYFPDXBNJZSQVHLCKE" #lista en orden de los codigos
        letnum={"X":"0","Y":"1","Z":"2"} #diccionario para sustituirlas letras en el dni
        letnum2={0:"X",1:"Y",2:"Z"}
        if(not dni):#Comprueba si el codigo que inserto el 
            if idioma == "ES":
                dninuevo= ""
                dninuevo = dninuevo + "".join(random.choices(string.digits,k=8))
                numeros = int(dninuevo[:8])-int((int(dninuevo[:8])/23))*23
                dninuevo = dninuevo + letras[numeros]
                return dninuevo
            elif idioma =="EN":
                dninuevo = "".join(random.choices(string.digits,k=9))
                return dninuevo
        else:#Comprueba si es un NIE
            if idioma == "ES":
                nie = letnum2[round(random.uniform(0,2))]
                nie = nie + "".join(random.choices(string.digits,k=7))
                
                numeros=int(letnum[nie[0].upper()]+nie[1:8])-(int(int(letnum[nie[0].upper()]+nie[1:8])/23)*23)
                return nie + letras[numeros]
            else:
                nie = "".join(random.choices(string.ascii_uppercase,k=2)) + random.choice(string.digits + "X")+"".join(random.choices(string.digits,k=6))
                return nie        
@app.route("/dni/<int:cantidad>/<int:dni>/<idioma>")
def generaDNI(cantidad,dni,idioma):
    dnis = []
    for i in range(cantidad):
        dnis.append(generarDni(idioma,bool(dni)))
    dicts = {"dni":dnis}
    return jsonify(dicts)
if __name__ == '__main__':

    app.run(debug=True)