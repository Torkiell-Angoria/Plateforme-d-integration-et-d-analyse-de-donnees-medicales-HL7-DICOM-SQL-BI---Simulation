from pydantic import BaseModel
from typing import List, Optional

# -------------------- Metadata --------------------
class MetadataSchema(BaseModel):
    messageControlId: str
    messageType: str
    triggerEvent: str
    sourceSystem: str
    messageTimestamp: str

# -------------------- Patient --------------------
class PatientSchema(BaseModel):
    externalId: str
    firstName: str
    lastName: str
    birthDate: str
    gender: str

# -------------------- Visit --------------------
class VisitSchema(BaseModel):
    location: str
    department: str
    visitType: str

# -------------------- Observation --------------------
class ObservationSchema(BaseModel):
    code: str
    label: str
    value: float
    unit: str
    referenceRange: Optional[str]
    interpretation: Optional[str]
    abnormalFlag: Optional[str]

# -------------------- HL7 Message --------------------
class IngestBase(BaseModel):
    metadata: MetadataSchema
    patient: PatientSchema
    visit: VisitSchema
    observations: List[ObservationSchema]

# -------------------- Alias pour compatibilité main.py --------------------
