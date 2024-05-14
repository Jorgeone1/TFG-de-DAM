import re

texto = """
AA-AN AD UK Norwich AO-AU AO UK Ipswich AV-AY AV UK B Birmingham Birmingham BA-BY matrícula britanica de Birmingham actual amarilla C Cymru Cardiff CA-CO CK GB Swansea CP-CV CT GB Bangor CW-CY D Deeside to Shrewsbury Chester DA-DK DI GB Shrewsbury DL-DY DX GB E Essex Chelmsford EA-EY EJ GB F Forest and Fens Nottingham FA-FP FG GB Fens Lincoln FR-FY FY GB G Garden of England Maidstone GA-GO GL Brighton GP-GY GV H Hampshire and Dorset Bournemouth HA-HJ HF Portsmouth HK-HY Matricula de Portsmouth, sur de Gran Bretaña K Luton KA-KL KM Northampton KM-KY KR L London Wimbledon LA-LJ Matricula de Londres Wimbeldon Stanmore LK-LT LR GB Sidcup LU-LY LX GB M Manchester and Merseyside Manchester MA-MY MW GB N North Newcastle NA-NO Matricula de Newcastle, Gran Bretaña Stockton NP-NY Matricula de Stockton, United Kingdom O Oxford Oxford OA-OY Matricula de Oxford en Gran Bretaña P Preston Preston PA-PT Matricula de Preston reino unido Carlisle PU-PY R Reading Reading RA-RY Matricula de Reading S Scotland Glasgow SA-SJ Matricula de Glasgow Edimburgo SK-SO Matricula de Edimburgo, Escocia Dundee SP-ST Matricula de Escocia, Dundee Aberdeen SU-SW Inverness SX, SY V Severn Valley Worcester VA-VY Matricula de Worcester en Severn Valley W West of England Exeter WA-WJ Matricula de Exeter en West England Truro WK, WL Matricula de Truro con letras WL Bristol WM-WY Matricula del Oeste, Bristol Y Yorkshire Leeds YA-YK Matricula de Leeds Sheffield YL-YU Matricula de Sheddield en Yorkshire, Reino Unido Beverley YV-YY
"""

# Expresión regular para buscar letras en mayúsculas
regex = r"\b[A-Z]{2}\b"

# Buscar todas las coincidencias en el texto
matches = re.findall(regex, texto)
print(matches)
