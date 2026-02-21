from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
from schemas import IngestBase
from fastapi.middleware.cors import CORSMiddleware

# Crée les tables dans la base de données si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini DPI FastAPI",
    description="Interface d'ingestion de données d'hospitalisation (HL7-like JSON)",
    version="1.0.0"
)

# -------------------- Configuration CORS --------------------
# Indispensable si tu as un front-end (React, Vue, etc.) qui communique avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Dépendance DB --------------------
def get_db():
    """Gère l'ouverture et la fermeture de la session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Routes --------------------

@app.get("/")
def read_root():
    return {"status": "online", "message": "Mini DPI API is running"}

@app.post("/ingest", status_code=201)
def ingest_data(payload: IngestBase, db: Session = Depends(get_db)):
    """
    Point d'entrée principal pour l'ingestion des données.
    
    Cette route :
    1. Reçoit le JSON validé par Pydantic (IngestBase).
    2. Crée/Récupère le Patient, le Type d'appareil et le Moniteur.
    3. Enregistre l'Examen et les Observations.
    4. Génère des alertes automatiques si les valeurs sont hors normes.
    """
    try:
        # On passe directement 'payload' qui est un objet Pydantic.
        # crud.py pourra ainsi faire payload.patient.externalId sans erreur.
        exam = crud.create_exam_from_message(db, payload)

        return {
            "status": "success",
            "message": "Data ingested successfully",
            "details": {
                "patient_id": exam.patient_id,
                "monitor_id": exam.monitor_id,
                "exam_id": exam.id
            }
        }
    except Exception as e:
        # En cas d'erreur interne (DB, logique métier), on renvoie une 500 propre
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# -------------------- Lancement --------------------
# Pour lancer : uvicorn main:app --reload