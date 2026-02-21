USE hospital_db;

-- Patients
INSERT INTO patients (external_id, first_name, last_name, birth_date, gender)
VALUES 
('P001', 'John', 'Doe', '1996-01-01', 'M'),
('P002', 'Jane', 'Smith', '1988-05-12', 'F'),
('P003', 'Alice', 'Johnson', '1990-11-03', 'F'),
('P004', 'Bob', 'Williams', '1975-07-21', 'M');

-- Device types
INSERT INTO device_types (name, description)
VALUES
('cardio_monitor', 'Moniteur cardiaque pour patients'),
('spirometer', 'Appareil pour mesurer la fonction respiratoire'),
('blood_pressure_monitor', 'Moniteur de tension artérielle'),
('oximeter', 'Appareil pour mesurer la saturation en oxygène'),
('temperature_sensor', 'Capteur de température corporelle');

-- Monitors
INSERT INTO monitors (monitor_id, serial_number, room, floor, status, patient_id, device_type_id)
VALUES
('M01', 'SN001', '101', 1, 'active', 1, 1),
('M02', 'SN002', '102', 1, 'available', NULL, 1),
('M03', 'SN003', '103', 1, 'active', 2, 2),
('M04', 'SN004', '104', 1, 'available', NULL, 3),
('M05', 'SN005', '105', 1, 'active', 1, 4),
('M06', 'SN006', '106', 2, 'available', NULL, 5),
('M07', 'SN007', '201', 2, 'available', NULL, 1),
('M08', 'SN008', '202', 2, 'active', 2, 3);

-- Exams
INSERT INTO exams (type, patient_id, monitor_id)
VALUES
('ECG', 1, 1),
('Spirometry', 1, 2),
('ECG', 2, 3),
('Spirometry', 2, 3),
('ContinuousCardio', 2, 3),
('BloodPressure', 1, 4),
('Oximetry', 1, 5),
('Temperature', 3, 6),
('ECG', 3, 7),
('BloodPressure', 4, 8);

-- Observations
INSERT INTO observations (code, label, value, unit, reference_range, interpretation, alert_threshold, alert_level, exam_id, monitor_id)
VALUES
('HR', 'Heart Rate', 85, 'bpm', '60-100', 'N', 120, 'warning', 1, 1),
('FEV1', 'Forced Expiratory Volume', 2.9, 'L', '2.5-3.5', 'N', 1.5, 'critical', 2, 2),
('HR', 'Heart Rate', 135, 'bpm', '60-100', 'H', 120, 'critical', 5, 3),
('BP_SYS', 'Systolic Blood Pressure', 145, 'mmHg', '90-120', 'H', 140, 'critical', 6, 4),
('BP_DIA', 'Diastolic Blood Pressure', 95, 'mmHg', '60-80', 'H', 90, 'critical', 6, 4),
('SpO2', 'Oxygen Saturation', 92, '%', '95-100', 'L', 90, 'warning', 7, 5),
('TEMP', 'Body Temperature', 38.5, '°C', '36.5-37.5', 'H', 38, 'warning', 8, 6),
('HR', 'Heart Rate', 78, 'bpm', '60-100', 'N', 120, 'normal', 9, 7),
('BP_SYS', 'Systolic Blood Pressure', 130, 'mmHg', '90-120', 'H', 140, 'warning', 10, 8);

-- Alerts
INSERT INTO alerts (monitor_id, patient_id, exam_id, type, value, level, status)
VALUES
(3, 2, 5, 'HR', 135.0, 'critical', 'alert'),
(5, 2, 7, 'SpO2', 88.0, 'critical', 'alert');