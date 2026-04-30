from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI()

# Permitir conexión desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Rutas de la API (tu /calculate)
app.include_router(router)

# 🌐 Servir archivos estáticos (tu página web)
app.mount("/", StaticFiles(directory="public", html=True), name="static")
