from fastapi import APIRouter, Header, HTTPException, Depends
from jose import jwt, JWTError
from app.models import ConverterInput, UserLogin
from app.auth import create_token, SECRET_KEY, ALGORITHM
from app.dynamo import table

router = APIRouter()


# 🔒 VERIFICAR TOKEN (PRIMERO)
def verificar_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No autorizado")

    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# 🔐 LOGIN
@router.post("/login")
def login(user: UserLogin):
    response = table.get_item(Key={"username": user.username})

    # ❌ usuario no existe
    if "Item" not in response:
        raise HTTPException(status_code=401, detail="Usuario no existe")

    db_user = response["Item"]

    # ❌ contraseña incorrecta
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # ✅ generar token
    token = create_token({"sub": user.username})

    return {"access_token": token}

# 👤 PERFIL
@router.get("/perfil")
def perfil(payload: dict = Depends(verificar_token)):
    return {"usuario": payload["sub"]}

# REGISTRAR

@router.post("/register")
def register(user: UserLogin):
    # Verificar si ya existe
    response = table.get_item(Key={"username": user.username})

    if "Item" in response:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    # Crear usuario
    table.put_item(Item={
        "username": user.username,
        "password": user.password
    })

    return {"msg": "Usuario creado"}

# ⚡ SIMULADOR (PROTEGIDO)
@router.post("/calculate")
def calculate(data: ConverterInput, authorization: str = Header(None)):
    verificar_token(authorization)

    vin = data.vin
    duty = data.duty

    if duty >= 1:
        return {"error": "Duty inválido"}

    vout = vin / (1 - duty)

    if vout < 10:
        estado = "baja eficiencia"
    elif vout < 20:
        estado = "normal"
    else:
        estado = "alta eficiencia"

    return {
        "vin": vin,
        "duty": duty,
        "vout": round(vout, 2),
        "estado": estado
    }
