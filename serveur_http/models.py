from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(1))

    monitors = relationship("Monitor", back_populates="patient")
    exams = relationship("Exam", back_populates="patient")


class DeviceType(Base):
    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    monitors = relationship("Monitor", back_populates="device_type")


class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    monitor_id = Column(String(50), unique=True, nullable=False)
    serial_number = Column(String(100), unique=True)
    room = Column(String(20))
    floor = Column(Integer)
    status = Column(String(20), default="available")

    patient_id = Column(Integer, ForeignKey("patients.id"))
    device_type_id = Column(Integer, ForeignKey("device_types.id"))

    patient = relationship("Patient", back_populates="monitors")
    device_type = relationship("DeviceType", back_populates="monitors")
    exams = relationship("Exam", back_populates="monitor")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))
    performed_at = Column(TIMESTAMP)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    monitor_id = Column(Integer, ForeignKey("monitors.id"))

    patient = relationship("Patient", back_populates="exams")
    monitor = relationship("Monitor", back_populates="exams")
    observations = relationship("Observation", back_populates="exam")
    alerts = relationship("Alert", back_populates="exam")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(50))
    label = Column(String(100))
    value = Column(Float)
    unit = Column(String(20))
    reference_range = Column(String(50))
    interpretation = Column(String(50))
    alert_threshold = Column(Float)
    alert_level = Column(String(20))

    exam_id = Column(Integer, ForeignKey("exams.id"))
    monitor_id = Column(Integer, ForeignKey("monitors.id"))

    exam = relationship("Exam", back_populates="observations")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    monitor_id = Column(Integer, ForeignKey("monitors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"))

    type = Column(String(50))
    value = Column(Float)
    level = Column(String(20))
    status = Column(Enum("alert", "resolved"), default="alert")
    timestamp = Column(TIMESTAMP)

    exam = relationship("Exam", back_populates="alerts")
