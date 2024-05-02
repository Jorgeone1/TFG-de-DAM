import re
import random

def comprobarDni(dni):
    letras= "TRWAGMYFPDXBNJZSQVHLCKE" #lista en orden de los codigos
    letnum={"X":"0","Y":"1","Z":"2"} #diccionario para sustituirlas letras en el dni
    letnum2={0:"X",1:"Y",2:"Z"}
    if(dni):#Comprueba si el codigo que inserto el 
        dninuevo= ""
        for i in range(8):
            dninuevo = dninuevo + str(round(random.uniform(0,9)))
        numeros = int(dninuevo[:8])-int((int(dninuevo[:8])/23))*23
        dninuevo = dninuevo + letras[numeros]
        return dninuevo
    else:#Comprueba si es un NIE
        nie = letnum2[round(random.uniform(0,2))]
        for i in range(7):
            nie = nie + str(round(random.uniform(0,9)))
        
        numeros=int(letnum[nie[0].upper()]+nie[1:8])-(int(int(letnum[nie[0].upper()]+nie[1:8])/23)*23)
        return nie + letras[numeros]
print(comprobarDni(False))
