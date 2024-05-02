import random
#Comprobación y operaciones del ccc
def comprobarIBAN():
    entidad = ""
    codigocuenta = ""
    for i in range(8):
        entidad = entidad + str(round(random.uniform(0,9)))

    for i in range(10):
        codigocuenta =codigocuenta+ str(round(random.uniform(0,9)))

    num1=[4,8,5,10,9,7,3,6] #Guarda las operaciones para el primer digito en orden
    num2=[1,2,4,8,5,10,9,7,3,6] #Guarda las operaciones del segundo digito en orden
    
    digito1=primerDigito(entidad,num1) #Realiza las operaciones del digito 1
    digito2=segundoDigito(codigocuenta,num2) #Realiza las operaciones del digito 2
    total= f"{digito1}{digito2}" #los junta
    return entidad + total + codigocuenta   #devuelve un booleano si coinciden o no

#operaciones del primer digito
def primerDigito(entidad,num1):
    numeros=0
    for po in range(0,8): #for que realiza las operaciones
        numeros= numeros + (int(entidad[po])*num1[po])
    resto=numeros%11
    
    if(resto==1):
        return 1
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
    else:
        return resto2
    
def CreadorIBAN(cuenta):
    total=cuenta+"142800" 
    numerosiban=98-(int(total)%97) #realiza la operación para calcular los numeros de despues del ES
    if(len(str(numerosiban))==1):
        numerosiban="0" + str(numerosiban) #Crea un iban pero con los numeros creados por las operaciones 
    iban="ES"+str(numerosiban)+cuenta
    return iban


print(CreadorIBAN(comprobarIBAN()))