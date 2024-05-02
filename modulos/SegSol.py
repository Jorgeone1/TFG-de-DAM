import random
def comprobarNaf():
    
    naf = "28"
    for i in range(8):
        naf= naf + str(round(random.uniform(0,9)))
    if(int(naf[2:10])<10000000):#comprueba si los numeros del medio supera los 
        numeros=((int(naf[:1])+int(naf[2:10]))*10000000)%97       
    else:
        numeros=int((int(naf[:10]))%97)#sino realizara otro tipo de operación
    naf = naf +str(numeros)       
    print(naf)   
comprobarNaf()