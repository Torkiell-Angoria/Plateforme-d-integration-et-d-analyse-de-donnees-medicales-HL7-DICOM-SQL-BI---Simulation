from database import Base, engine, SessionLocal
from models import DeviceType, Monitor

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Exemples de types d'appareils
types = ["cardio_monitor", "spirometer", "ecg_portable"]
for t in types:
    db.add(DeviceType(name=t, description=f"Device type {t}"))

db.commit()

# Exemples de moniteurs
db.add(Monitor(monitor_id="M01", serial_number="SN01", room="101", floor=1, device_type_id=1))
db.add(Monitor(monitor_id="M02", serial_number="SN02", room="102", floor=1, device_type_id=2))

db.commit()
db.close()

print("✅ Tables créées et données de test insérées")
