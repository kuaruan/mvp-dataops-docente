from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
# Importamos tus funciones de db.py
from app.db import test_connection, get_stats, get_postulaciones

app = FastAPI()

# --- RUTA INICIAL ---
@app.get("/")
def read_root():
    return {"message": "API de Postulaciones Operativa", "version": "1.0.0"}

# --- ETAPA J: RUTAS DESCRIPTIVAS (SupaBase) ---
@app.get("/db-health")
def db_health():
    if test_connection():
        return {"status": "ok", "message": "Conexión exitosa a Supabase"}
    raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

@app.get("/postulaciones-demo/stats")
def fetch_stats():
    stats = get_stats()
    if stats:
        return stats
    raise HTTPException(status_code=404, detail="No se pudieron obtener estadísticas")

# --- ETAPA K: RUTA PREDICTIVA (Machine Learning) ---
MODEL_PATH = "artifacts/model.joblib"

@app.get("/predict")
def predict(puntaje_lenguaje: float, puntaje_matematica: float):
    try:
        # Cargamos el cerebro de nuestra IA
        model = joblib.load(MODEL_PATH)
        
        # Preparamos los datos tal como el modelo los espera
        input_data = pd.DataFrame(
            [[puntaje_lenguaje, puntaje_matematica]], 
            columns=['puntaje_lenguaje', 'puntaje_matematica']
        )
        
        # Realizamos la predicción
        prediction = model.predict(input_data)[0]
        probabilidad = model.predict_proba(input_data)[0][1]
        
        return {
            "puntajes_recibidos": {
                "lenguaje": puntaje_lenguaje,
                "matematica": puntaje_matematica
            },
            "se_matricula": bool(prediction),
            "probabilidad_exito": round(float(probabilidad), 2),
            "mensaje": "Predicción generada exitosamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")