from pydantic import BaseModel, EmailStr, ValidationError

# Definición del modelo
class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    is_active: bool = True

# Creación y validación de una instancia del modelo
try:
    user = User(
        name="Alex",
        age=30,
        email="alex@example.com"
    )
    print(user)
except ValidationError as e:
    print(e.json())

# Intento de crear una instancia con datos inválidos
try:
    invalid_user = User(
        name="Laura",
        age="veinte",  # esto provocará un error porque no es un entero
        email="laura@example.com"
    )
except ValidationError as e:
    print(e.json())