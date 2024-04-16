from faker import Faker

# Crear una instancia de Faker
fake = Faker()

# Generar datos falsos
print("Nombre:", fake.name())
print("Dirección:", fake.address())
print("Email:", fake.email())
print("Texto:", fake.text())

# Puedes generar también datos específicos para una localidad
fake_es = Faker('es_ES') # para España, por ejemplo
print("Nombre Español:", fake_es.name())
print("Direccion Español:", fake_es.address())