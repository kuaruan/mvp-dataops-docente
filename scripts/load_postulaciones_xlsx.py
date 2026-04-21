import os
import pandas as pd
import psycopg
from dotenv import load_dotenv

# Cargamos variables de entorno (.env)
load_dotenv()

def get_connection_params():
    return {
        "host": os.getenv("SUPABASE_DB_HOST"),
        "port": os.getenv("SUPABASE_DB_PORT", "6543"),
        "dbname": os.getenv("SUPABASE_DB_NAME", "postgres"),
        "user": os.getenv("SUPABASE_DB_USER"),
        "password": os.getenv("SUPABASE_DB_PASSWORD"),
        "sslmode": "require",
    }

def load_dataframe():
    path = "data/postulaciones.xlsx"
    print(f"Leyendo archivo: {path}...")
    df = pd.read_excel(path, sheet_name="Postulaciones")
    # Limpiamos nombres de columnas por si acaso
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

def insert_rows(conn, df):
    sql = '''
    INSERT INTO public.postulaciones_demo (
        cedula, periodo, sexo, preferencia, carrera, matriculado, facultad,
        puntaje, grupo_depen, region, latitud, longitud, ptje_nem,
        psu_promlm, pace, gratuidad
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    '''
    rows = []
    print(f"Preparando {len(df)} registros...")
    for _, row in df.iterrows():
        rows.append((
            str(row["CEDULA"]), int(row["PERIODO"]), str(row["SEXO"]),
            int(row["PREFERENCIA"]), str(row["CARRERA"]), str(row["MATRICULADO"]),
            str(row["FACULTAD"]), float(row["PUNTAJE"]), str(row["GRUPO_DEPEN"]),
            str(row["REGION"]), float(row["LATITUD"]), float(row["LONGITUD"]),
            float(row["PTJE_NEM"]), float(row["PSU_PROMLM"]), str(row["PACE"]),
            str(row["GRATUIDAD"])
        ))

    with conn.cursor() as cur:
        print("Enviando datos a Supabase... (esto será rápido)")
        cur.executemany(sql, rows)
        conn.commit()

def main():
    try:
        params = get_connection_params()
        df = load_dataframe()
        
        with psycopg.connect(**params) as conn:
            # Limpiamos la tabla antes de cargar
            with conn.cursor() as cur:
                print("Limpiando tabla previa...")
                cur.execute("TRUNCATE TABLE public.postulaciones_demo RESTART IDENTITY;")
            
            insert_rows(conn, df)
            
        print("✅ ¡ÉXITO! Datos cargados correctamente.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()