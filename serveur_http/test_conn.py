from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Encode le mot de passe pour les caractères spéciaux
password = quote_plus("barjackolo99@")  # ici ton vrai mot de passe

# URL de connexion MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/hospital_db"

# Création de l'engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Test de connexion
try:
    conn = engine.connect()
    print("✅ Connexion MySQL réussie !")
    conn.close()
except Exception as e:
    print("❌ Erreur de connexion :", e)
