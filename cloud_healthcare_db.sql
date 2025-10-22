-- Cloud-Based Healthcare System Database Script
-- Comprehensive SQL code for all modules: Users, Doctors, Patients, Appointments, Prescriptions, Billing, Medicines, Hospital Resources, Lab Tests, Feedback

-- Drop existing tables if they exist
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS lab_tests;
DROP TABLE IF EXISTS hospital_resources;
DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS medicines;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS users;

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'doctor', 'patient') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctors Table
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    availability_status ENUM('available','busy','off') DEFAULT 'available',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Patients Table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    dob DATE,
    gender ENUM('male','female','other'),
    phone VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Medicines Table
CREATE TABLE medicines (
    med_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    quantity INT DEFAULT 0,
    price DECIMAL(10,2),
    expiry_date DATE
);

-- Appointments Table
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    status ENUM('scheduled','completed','cancelled') DEFAULT 'scheduled',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- Prescriptions Table
CREATE TABLE prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    med_id INT NOT NULL,
    dosage VARCHAR(100),
    duration VARCHAR(50),
    instructions TEXT,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    FOREIGN KEY (med_id) REFERENCES medicines(med_id) ON DELETE CASCADE
);

-- Billing Table
CREATE TABLE billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    total_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    payment_status ENUM('pending','paid','partial') DEFAULT 'pending',
    payment_date DATETIME,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE
);

-- Hospital Resources Table
CREATE TABLE hospital_resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_name VARCHAR(100) NOT NULL,
    resource_type ENUM('room','bed','equipment') NOT NULL,
    quantity INT DEFAULT 0,
    status ENUM('available','occupied','maintenance') DEFAULT 'available'
);

-- Lab Tests Table
CREATE TABLE lab_tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    test_name VARCHAR(100),
    test_date DATETIME,
    result TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- Feedback Table
CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT,
    feedback_text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
);

-- Sample Data Insertion for Users
INSERT INTO users (username, password, role) VALUES
('admin1','adminpass','admin'),
('dr_smith','drpass','doctor'),
('john_doe','patientpass','patient');

-- Sample Doctors
INSERT INTO doctors (user_id, full_name, specialization, phone, email) VALUES
(2,'Dr. John Smith','Cardiology','9876543210','drsmith@example.com');

-- Sample Patients
INSERT INTO patients (user_id, full_name, dob, gender, phone, email, address) VALUES
(3,'John Doe','1985-07-12','male','9123456780','johndoe@example.com','123 Main Street, City');

-- Sample Medicines
INSERT INTO medicines (name, manufacturer, quantity, price, expiry_date) VALUES
('Paracetamol','PharmaInc',100,0.50,'2026-12-31'),
('Amoxicillin','Medico',50,1.20,'2025-11-30');

-- Sample Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes) VALUES
(1,1,'2025-11-01 10:00:00','scheduled','Routine checkup');

-- Sample Prescriptions
INSERT INTO prescriptions (appointment_id, med_id, dosage, duration, instructions) VALUES
(1,1,'500mg','5 days','Take after meals');

-- Sample Billing
INSERT INTO billing (appointment_id, total_amount, paid_amount, payment_status, payment_date) VALUES
(1,25.00,25.00,'paid','2025-11-01 11:00:00');

-- Sample Hospital Resources
INSERT INTO hospital_resources (resource_name, resource_type, quantity, status) VALUES
('ICU Bed','bed',10,'available'),
('X-Ray Machine','equipment',2,'available');

-- Sample Lab Tests
INSERT INTO lab_tests (patient_id, doctor_id, test_name, test_date, result) VALUES
(1,1,'Blood Test','2025-11-01 12:00:00','Normal');

-- Sample Feedback
INSERT INTO feedback (patient_id, doctor_id, feedback_text, rating) VALUES
(1,1,'Very satisfied with the consultation',5);

-- End of Script
