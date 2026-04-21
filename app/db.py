import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    # Usamos el puerto 6543 para el Pooler de Supabase
    return psycopg.connect(
        host=os.getenv("SUPABASE_DB_HOST"),
        port=os.getenv("SUPABASE_DB_PORT", "6543"),
        dbname=os.getenv("SUPABASE_DB_NAME", "postgres"),
        user=os.getenv("SUPABASE_DB_USER"),
        password=os.getenv("SUPABASE_DB_PASSWORD"),
        row_factory=dict_row  # Esto hace que los resultados sean diccionarios fáciles de leer
    )

def test_connection():
    try:
        with get_conn() as conn:
            return {"status": "ok", "message": "Conexión exitosa a Supabase"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_postulaciones(limit=20):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.postulaciones_demo LIMIT %s", (limit,))
            return cur.fetchall()

def get_stats():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    count(*) as total,
                    count(CASE WHEN matriculado = 'SI' THEN 1 END) as matriculados,
                    avg(puntaje) as promedio_puntaje
                FROM public.postulaciones_demo
            """)
            return cur.fetchone()