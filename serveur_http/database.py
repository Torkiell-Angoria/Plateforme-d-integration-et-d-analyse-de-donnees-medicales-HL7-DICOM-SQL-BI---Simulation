from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#DATABASE_URL = "sqlite:///./mini_dpi.db"
# Si MySQL :
DATABASE_URL = "mysql+pymysql://root:barjackolo99%40@localhost/hospital_db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
