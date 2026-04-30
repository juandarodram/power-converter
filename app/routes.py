from fastapi import APIRouter, Header, HTTPException
from jose import jwt, JWTError
from app.models import ConverterInput, UserLogin
from app.auth import create_token, SECRET_KEY, ALGORITHM

router = APIRouter()

# 🔐 LOGIN
@router.post("/login")
def login(user: UserLogin):
    if user.username == "admin" and user.password == "1234":
        token = create_token({"sub": user.username})
        return {"access_token": token}
    
    return {"error": "Credenciales incorrectas"}


# 🔒 VERIFICAR TOKEN
def verificar_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No autorizado")

    try:
        token = authorization.split(" ")[1]
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ⚡ TU SIMULADOR (PROTEGIDO)
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

