from sqlalchemy.orm import Session
from models import Patient, Monitor, DeviceType, Exam, Observation, Alert
from datetime import datetime


def is_out_of_range(value, reference_range):
    if not reference_range:
        return False
    try:
        min_val, max_val = reference_range.split("-")
        return value < float(min_val) or value > float(max_val)
    except:
        return False


from datetime import datetime # Assure-toi d'avoir cet import

def get_or_create_patient(db: Session, message):
    # 1. Conversion de la date (format AAAAMMJJ vers objet date)
    b_date = None
    if message.patient.birthDate:
        try:
            # On transforme '19890130' en objet date
            b_date = datetime.strptime(message.patient.birthDate, "%Y%m%d").date()
        except ValueError:
            b_date = None # Ou gestion d'erreur si le format est différent

    # 2. Recherche du patient
    patient = db.query(Patient).filter_by(
        external_id=message.patient.externalId
    ).first()

    if not patient:
        patient = Patient(
            external_id=message.patient.externalId,
            first_name=message.patient.firstName,
            last_name=message.patient.lastName,
            birth_date=b_date, # Utilisation de l'objet date converti
            gender=message.patient.gender
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

    return patient


def get_or_create_device_type(db: Session, message):
    device_type = db.query(DeviceType).filter_by(
        name=message.metadata.sourceSystem
    ).first()

    if not device_type:
        device_type = DeviceType(
            name=message.metadata.sourceSystem,
            description="Auto-created device type"
        )
        db.add(device_type)
        db.commit()
        db.refresh(device_type)
    return device_type

def get_or_create_monitor(db: Session, message, patient, device_type):
    monitor = db.query(Monitor).filter_by(
        monitor_id=message.metadata.sourceSystem
    ).first()

    # Sécurité pour l'étage (floor)
    try:
        # On essaie de convertir, sinon on met 0 par défaut
        floor_val = int(message.visit.department) if message.visit.department else 0
    except (ValueError, TypeError):
        floor_val = 0

    if not monitor:
        monitor = Monitor(
            monitor_id=message.metadata.sourceSystem,
            room=message.visit.location,
            floor=floor_val,
            status="available",
            patient_id=patient.id,
            device_type_id=device_type.id
        )
        db.add(monitor)
    else:
        # Mise à jour du patient et de l'emplacement si le moniteur existe déjà
        monitor.patient_id = patient.id
        monitor.room = message.visit.location
        monitor.floor = floor_val
    
    db.commit()
    db.refresh(monitor)
    return monitor  # <--- C'était ici l'erreur !


def create_exam_from_message(db: Session, message):

    patient = get_or_create_patient(db, message)
    device_type = get_or_create_device_type(db, message)
    monitor = get_or_create_monitor(db, message, patient, device_type)

    exam = Exam(
        type=message.metadata.messageType,
        patient_id=patient.id,
        monitor_id=monitor.id
    )

    db.add(exam)
    db.commit()
    db.refresh(exam)

    for obs in message.observations:

        observation = Observation(
            code=obs.code,
            label=obs.label,
            value=obs.value,
            unit=obs.unit,
            reference_range=obs.referenceRange,
            interpretation=obs.interpretation,
            exam_id=exam.id,
            monitor_id=monitor.id,
            alert_level=None
        )

        db.add(observation)
        db.commit()

        trigger_alert = False

        if obs.interpretation == "H":
            trigger_alert = True

        elif is_out_of_range(obs.value, obs.referenceRange):
            trigger_alert = True

        if trigger_alert:
            alert = Alert(
                monitor_id=monitor.id,
                patient_id=patient.id,
                exam_id=exam.id,
                type=obs.code,
                value=obs.value,
                level="alert",
                status="alert",
                timestamp=datetime.utcnow()
            )
            db.add(alert)
            db.commit()

    return exam



