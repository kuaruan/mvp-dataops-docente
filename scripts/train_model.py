import os
import pandas as pd
import psycopg
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

load_dotenv()

def get_data():
    conn_params = {
        "host": os.getenv("SUPABASE_DB_HOST"),
        "port": os.getenv("SUPABASE_DB_PORT", "6543"),
        "dbname": os.getenv("SUPABASE_DB_NAME", "postgres"),
        "user": os.getenv("SUPABASE_DB_USER"),
        "password": os.getenv("SUPABASE_DB_PASSWORD"),
        "sslmode": "require",
    }
    
    print("Conectando a Supabase para extraer datos...")
    with psycopg.connect(**conn_params) as conn:
        query = "SELECT * FROM public.postulaciones_demo"
        df = pd.read_sql(query, conn)
    return df

def train():
    df = get_data()
    print(f"Datos cargados para entrenamiento: {len(df)} filas.")

    # Selección de características (Features) y objetivo (Target)
    # Usamos variables numéricas para el ejemplo simple
    features = ['puntaje', 'ptje_nem', 'psu_promlm', 'preferencia']
    target = 'matriculado'

    # Limpieza rápida: Convertir 'SI'/'NO' a 1/0 si es necesario
    df[target] = df[target].apply(lambda x: 1 if str(x).strip().upper() == 'SI' else 0)
    
    X = df[features].fillna(0)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Entrenando el modelo (Random Forest)...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluación
    y_pred = model.predict(X_test)
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred))

    # Guardar el modelo
    os.makedirs('artifacts', exist_ok=True)
    joblib.dump(model, 'artifacts/model.joblib')
    print("\n✅ Modelo guardado en artifacts/model.joblib")

if __name__ == "__main__":
    train()