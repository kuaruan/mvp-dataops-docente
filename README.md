Actividad: DataOps - Predicción de matrícula estudiantil 
Objetivo del proyecto mínimo viable: Usando la técnica de DataOps de la mano de Machine Learning, se almacenaran y procesaran datos históricos de postulaciones, para predecir la probabilidad de que un estudiante se matricule

Tecnologías utilizadas: 
- Base de datos: Supabase (postgreSQL)
- Lenguaje: Python 3.12
- Framework API: FastAPI / Uvicorn
- IA: Scikit -learn (Random Forest)
- Gestión de versiones: Git / GitHub

Estructura del proyecto: 
app/ : contiene la lógica de la API y conexión a la base de datos
scripts/ : carga de datos (load_postulaciones_xlsx.py) y entrenamiento
artifacts/ : almacenamiento del modelo entrenado (model.joblib)
data/ : datos fuente en formato excel

Instalación y uso: 
1. Clonar el repositorio: 
   git clone "https://github.com/kuaruan/mvp-dataops-docente/"
   cd mvp-dataops-docente

2. Configurar entorno
   Crear archivo .env con credenciales de Supabase

3. Ejecución de Pipeline
   Carga de datos: python scripts/load_postulaciones_xlsx.py
   Entrenamiento: python scripts/train_model.py
   Iniciar API: uvicorn app.main:app --reload

Endpoints
- GET /db-health: verificará la conexión con Supabase
- GET /postulaciones-demo/stats: mostrará estadísticas generales del total de registros

  
  
