CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- =========================
-- Table patients
-- =========================
CREATE TABLE patients (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    external_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    gender CHAR(1)
) ENGINE=InnoDB;

-- =========================
-- Table device_types
-- =========================
CREATE TABLE device_types (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
) ENGINE=InnoDB;

-- =========================
-- Table monitors
-- =========================
CREATE TABLE monitors (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    monitor_id VARCHAR(50) UNIQUE NOT NULL,
    serial_number VARCHAR(100) UNIQUE,
    room VARCHAR(20),
    floor INT,
    status VARCHAR(20) DEFAULT 'available',
    patient_id INT UNSIGNED,
    device_type_id INT UNSIGNED,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (device_type_id) REFERENCES device_types(id)
) ENGINE=InnoDB;

-- =========================
-- Table exams
-- =========================
CREATE TABLE exams (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50),
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    patient_id INT UNSIGNED,
    monitor_id INT UNSIGNED,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (monitor_id) REFERENCES monitors(id)
) ENGINE=InnoDB;

-- =========================
-- Table observations
-- =========================
CREATE TABLE observations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    label VARCHAR(100),
    value FLOAT,
    unit VARCHAR(20),
    reference_range VARCHAR(50),
    interpretation VARCHAR(50),
    alert_threshold FLOAT,
    alert_level VARCHAR(20),
    exam_id INT UNSIGNED,
    monitor_id INT UNSIGNED,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (monitor_id) REFERENCES monitors(id)
) ENGINE=InnoDB;

-- =========================
-- Table alerts
-- =========================
CREATE TABLE alerts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    monitor_id INT UNSIGNED NOT NULL,
    patient_id INT UNSIGNED NOT NULL,
    exam_id INT UNSIGNED,
    type VARCHAR(50),
    value FLOAT,
    level VARCHAR(20),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('alert','resolved') DEFAULT 'alert',
    FOREIGN KEY (monitor_id) REFERENCES monitors(id),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id)
) ENGINE=InnoDB;