

import json
import os
import hashlib
import datetime
from typing import Dict, List, Optional

class HealthcareSystem:
    def __init__(self, data_file: str = "healthcare_data.json"):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file or create new structure"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Initialize with empty data structure
        return {
            "users": {},
            "patients": {},
            "doctors": {},
            "beds": {},
            "medicines": {},
            "next_ids": {"user": 1, "patient": 1, "doctor": 1, "bed": 1, "medicine": 1}
        }
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    def get_next_id(self, entity_type: str) -> int:
        """Get next available ID for entity type"""
        next_id = self.data["next_ids"][entity_type]
        self.data["next_ids"][entity_type] += 1
        return next_id
    
    # User Management
    def register_user(self, username: str, password: str, role: str, first_name: str, last_name: str, email: str = "", phone: str = "") -> Dict:
        """Register a new user"""
        if username in self.data["users"]:
            return {"success": False, "message": "Username already exists"}
        
        user_id = self.get_next_id("user")
        user = {
            "id": user_id,
            "username": username,
            "password_hash": self.hash_password(password),
            "role": role,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "is_active": True,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        self.data["users"][username] = user
        self.save_data()
        return {"success": True, "message": "User registered successfully", "user_id": user_id}
    
    def login_user(self, username: str, password: str) -> Dict:
        """Login user"""
        if username not in self.data["users"]:
            return {"success": False, "message": "User not found"}
        
        user = self.data["users"][username]
        if not self.verify_password(password, user["password_hash"]):
            return {"success": False, "message": "Invalid password"}
        
        if not user["is_active"]:
            return {"success": False, "message": "Account deactivated"}
        
        return {"success": True, "message": "Login successful", "user": user}
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        return self.data["users"].get(username)
    
    # Patient Management
    def add_patient(self, first_name: str, last_name: str, age: int, gender: str, phone: str = "", email: str = "", medical_history: str = "", allergies: str = "") -> Dict:
        """Add a new patient"""
        patient_id = self.get_next_id("patient")
        patient = {
            "id": patient_id,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "gender": gender,
            "phone": phone,
            "email": email,
            "medical_history": medical_history,
            "allergies": allergies,
            "is_active": True,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        self.data["patients"][patient_id] = patient
        self.save_data()
        return {"success": True, "message": "Patient added successfully", "patient": patient}
    
    def get_patient(self, patient_id: int) -> Optional[Dict]:
        """Get patient by ID"""
        return self.data["patients"].get(patient_id)
    
    def get_all_patients(self) -> List[Dict]:
        """Get all active patients"""
        return [p for p in self.data["patients"].values() if p["is_active"]]
    
    def update_patient(self, patient_id: int, **kwargs) -> Dict:
        """Update patient information"""
        if patient_id not in self.data["patients"]:
            return {"success": False, "message": "Patient not found"}
        
        patient = self.data["patients"][patient_id]
        for key, value in kwargs.items():
            if key in patient and key not in ["id", "created_at"]:
                patient[key] = value
        
        self.save_data()
        return {"success": True, "message": "Patient updated successfully", "patient": patient}
    
    def delete_patient(self, patient_id: int) -> Dict:
        """Soft delete patient"""
        if patient_id not in self.data["patients"]:
            return {"success": False, "message": "Patient not found"}
        
        self.data["patients"][patient_id]["is_active"] = False
        self.save_data()
        return {"success": True, "message": "Patient deleted successfully"}
    
    # Doctor Management
    def add_doctor(self, first_name: str, last_name: str, specialization: str, phone: str = "", email: str = "", shift: str = "", license_number: str = "") -> Dict:
        """Add a new doctor"""
        doctor_id = self.get_next_id("doctor")
        doctor = {
            "id": doctor_id,
            "first_name": first_name,
            "last_name": last_name,
            "specialization": specialization,
            "phone": phone,
            "email": email,
            "shift": shift,
            "license_number": license_number,
            "is_available": True,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        self.data["doctors"][doctor_id] = doctor
        self.save_data()
        return {"success": True, "message": "Doctor added successfully", "doctor": doctor}
    
    def get_doctor(self, doctor_id: int) -> Optional[Dict]:
        """Get doctor by ID"""
        return self.data["doctors"].get(doctor_id)
    
    def get_all_doctors(self) -> List[Dict]:
        """Get all doctors"""
        return list(self.data["doctors"].values())
    
    def update_doctor(self, doctor_id: int, **kwargs) -> Dict:
        """Update doctor information"""
        if doctor_id not in self.data["doctors"]:
            return {"success": False, "message": "Doctor not found"}
        
        doctor = self.data["doctors"][doctor_id]
        for key, value in kwargs.items():
            if key in doctor and key not in ["id", "created_at"]:
                doctor[key] = value
        
        self.save_data()
        return {"success": True, "message": "Doctor updated successfully", "doctor": doctor}
    
    # Bed Management
    def add_bed(self, bed_number: str, bed_type: str, ward: str = "") -> Dict:
        """Add a new bed"""
        bed_id = self.get_next_id("bed")
        bed = {
            "id": bed_id,
            "bed_number": bed_number,
            "bed_type": bed_type,
            "status": "available",
            "ward": ward,
            "patient_id": None,
            "assigned_at": None,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        self.data["beds"][bed_id] = bed
        self.save_data()
        return {"success": True, "message": "Bed added successfully", "bed": bed}
    
    def get_bed(self, bed_id: int) -> Optional[Dict]:
        """Get bed by ID"""
        return self.data["beds"].get(bed_id)
    
    def get_all_beds(self) -> List[Dict]:
        """Get all beds"""
        return list(self.data["beds"].values())
    
    def assign_bed(self, bed_id: int, patient_id: int) -> Dict:
        """Assign bed to patient"""
        if bed_id not in self.data["beds"]:
            return {"success": False, "message": "Bed not found"}
        
        if patient_id not in self.data["patients"]:
            return {"success": False, "message": "Patient not found"}
        
        bed = self.data["beds"][bed_id]
        if bed["status"] != "available":
            return {"success": False, "message": "Bed is not available"}
        
        bed["status"] = "occupied"
        bed["patient_id"] = patient_id
        bed["assigned_at"] = datetime.datetime.now().isoformat()
        
        self.save_data()
        return {"success": True, "message": "Bed assigned successfully", "bed": bed}
    
    def release_bed(self, bed_id: int) -> Dict:
        """Release bed"""
        if bed_id not in self.data["beds"]:
            return {"success": False, "message": "Bed not found"}
        
        bed = self.data["beds"][bed_id]
        if bed["status"] != "occupied":
            return {"success": False, "message": "Bed is not occupied"}
        
        bed["status"] = "available"
        bed["patient_id"] = None
        bed["assigned_at"] = None
        
        self.save_data()
        return {"success": True, "message": "Bed released successfully", "bed": bed}
    
    # Medicine Management
    def add_medicine(self, name: str, expiry_date: str, quantity: int, unit_price: float, category: str = "", minimum_stock_level: int = 10) -> Dict:
        """Add a new medicine"""
        medicine_id = self.get_next_id("medicine")
        medicine = {
            "id": medicine_id,
            "name": name,
            "expiry_date": expiry_date,
            "quantity": quantity,
            "unit_price": unit_price,
            "category": category,
            "minimum_stock_level": minimum_stock_level,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        self.data["medicines"][medicine_id] = medicine
        self.save_data()
        return {"success": True, "message": "Medicine added successfully", "medicine": medicine}
    
    def get_medicine(self, medicine_id: int) -> Optional[Dict]:
        """Get medicine by ID"""
        return self.data["medicines"].get(medicine_id)
    
    def get_all_medicines(self) -> List[Dict]:
        """Get all medicines"""
        return list(self.data["medicines"].values())
    
    def get_low_stock_medicines(self) -> List[Dict]:
        """Get medicines with low stock"""
        return [m for m in self.data["medicines"].values() if m["quantity"] <= m["minimum_stock_level"]]
    
    def get_expired_medicines(self) -> List[Dict]:
        """Get expired medicines"""
        today = datetime.date.today().isoformat()
        return [m for m in self.data["medicines"].values() if m["expiry_date"] <= today]
    
    def update_medicine_stock(self, medicine_id: int, new_quantity: int) -> Dict:
        """Update medicine stock"""
        if medicine_id not in self.data["medicines"]:
            return {"success": False, "message": "Medicine not found"}
        
        self.data["medicines"][medicine_id]["quantity"] = new_quantity
        self.save_data()
        return {"success": True, "message": "Medicine stock updated successfully"}
    
    # Analytics
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        stats = {
            "total_patients": len([p for p in self.data["patients"].values() if p["is_active"]]),
            "total_doctors": len(self.data["doctors"]),
            "total_beds": len(self.data["beds"]),
            "available_beds": len([b for b in self.data["beds"].values() if b["status"] == "available"]),
            "occupied_beds": len([b for b in self.data["beds"].values() if b["status"] == "occupied"]),
            "total_medicines": len(self.data["medicines"]),
            "low_stock_medicines": len(self.get_low_stock_medicines()),
            "expired_medicines": len(self.get_expired_medicines())
        }
        return stats
    
    # Sample Data
    def seed_sample_data(self):
        """Create sample data for testing"""
        print("🌱 Seeding sample data...")
        
        # Create users
        self.register_user("admin", "admin123", "admin", "Admin", "User", "admin@hospital.com")
        self.register_user("doctor", "doctor123", "doctor", "Dr. John", "Smith", "doctor@hospital.com")
        self.register_user("patient", "patient123", "patient", "Jane", "Doe", "patient@hospital.com")
        
        # Create patients
        self.add_patient("Alice", "Johnson", 35, "Female", "123-456-7890", "alice@email.com", "Diabetes", "Penicillin")
        self.add_patient("Bob", "Wilson", 42, "Male", "123-456-7891", "bob@email.com", "Asthma", "None")
        
        # Create doctors
        self.add_doctor("Dr. Sarah", "Brown", "Cardiology", "123-456-7801", "sarah@hospital.com", "Morning", "DOC001")
        self.add_doctor("Dr. Michael", "Davis", "Neurology", "123-456-7802", "michael@hospital.com", "Evening", "DOC002")
        
        # Create beds
        self.add_bed("G001", "general", "Ward A")
        self.add_bed("ICU001", "icu", "ICU")
        self.add_bed("ER001", "emergency", "Emergency")
        
        # Create medicines
        self.add_medicine("Paracetamol", "2025-12-31", 100, 5.50, "Painkiller", 20)
        self.add_medicine("Amoxicillin", "2024-06-30", 5, 15.75, "Antibiotic", 10)
        
        print("✅ Sample data seeded successfully!")
        print("🔑 Test Credentials:")
        print("   Admin: username='admin', password='admin123'")
        print("   Doctor: username='doctor', password='doctor123'")
        print("   Patient: username='patient', password='patient123'")

# Simple CLI Interface
def main():
    """Simple command-line interface"""
    system = HealthcareSystem()
    
    # Seed data if empty
    if not system.data["users"]:
        system.seed_sample_data()
    
    print("\n🏥 Healthcare Management System")
    print("=" * 40)
    
    while True:
        print("\n📋 Main Menu:")
        print("1. Login")
        print("2. View Dashboard")
        print("3. Manage Patients")
        print("4. Manage Doctors")
        print("5. Manage Beds")
        print("6. Manage Medicines")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            result = system.login_user(username, password)
            print(f"✅ {result['message']}" if result['success'] else f"❌ {result['message']}")
            
        elif choice == "2":
            stats = system.get_dashboard_stats()
            print("\n📊 Dashboard Statistics:")
            print(f"   Patients: {stats['total_patients']}")
            print(f"   Doctors: {stats['total_doctors']}")
            print(f"   Beds: {stats['total_beds']} (Available: {stats['available_beds']}, Occupied: {stats['occupied_beds']})")
            print(f"   Medicines: {stats['total_medicines']} (Low Stock: {stats['low_stock_medicines']}, Expired: {stats['expired_medicines']})")
            
        elif choice == "3":
            print("\n👥 Patient Management:")
            print("1. Add Patient")
            print("2. View All Patients")
            print("3. View Patient Details")
            
            sub_choice = input("Enter choice (1-3): ").strip()
            
            if sub_choice == "1":
                first_name = input("First Name: ").strip()
                last_name = input("Last Name: ").strip()
                age = int(input("Age: ").strip())
                gender = input("Gender: ").strip()
                phone = input("Phone (optional): ").strip()
                email = input("Email (optional): ").strip()
                medical_history = input("Medical History (optional): ").strip()
                allergies = input("Allergies (optional): ").strip()
                
                result = system.add_patient(first_name, last_name, age, gender, phone, email, medical_history, allergies)
                print(f"✅ {result['message']}")
                
            elif sub_choice == "2":
                patients = system.get_all_patients()
                print(f"\n👥 All Patients ({len(patients)}):")
                for patient in patients:
                    print(f"   {patient['id']}: {patient['first_name']} {patient['last_name']} ({patient['age']}, {patient['gender']})")
                    
            elif sub_choice == "3":
                patient_id = int(input("Patient ID: ").strip())
                patient = system.get_patient(patient_id)
                if patient:
                    print(f"\n Patient Details:")
                    print(f"   Name: {patient['first_name']} {patient['last_name']}")
                    print(f"   Age: {patient['age']}, Gender: {patient['gender']}")
                    print(f"   Phone: {patient['phone']}")
                    print(f"   Email: {patient['email']}")
                    print(f"   Medical History: {patient['medical_history']}")
                    print(f"   Allergies: {patient['allergies']}")
                else:
                    print("❌ Patient not found")
                    
        elif choice == "4":
            print("\n👨‍⚕️ Doctor Management:")
            print("1. Add Doctor")
            print("2. View All Doctors")
            
            sub_choice = input("Enter choice (1-2): ").strip()
            
            if sub_choice == "1":
                first_name = input("First Name: ").strip()
                last_name = input("Last Name: ").strip()
                specialization = input("Specialization: ").strip()
                phone = input("Phone (optional): ").strip()
                email = input("Email (optional): ").strip()
                shift = input("Shift (optional): ").strip()
                license_number = input("License Number (optional): ").strip()
                
                result = system.add_doctor(first_name, last_name, specialization, phone, email, shift, license_number)
                print(f"✅ {result['message']}")
                
            elif sub_choice == "2":
                doctors = system.get_all_doctors()
                print(f"\n👨‍⚕️ All Doctors ({len(doctors)}):")
                for doctor in doctors:
                    print(f"   {doctor['id']}: {doctor['first_name']} {doctor['last_name']} - {doctor['specialization']}")
                    
        elif choice == "5":
            print("\n🛏️ Bed Management:")
            print("1. Add Bed")
            print("2. View All Beds")
            print("3. Assign Bed")
            print("4. Release Bed")
            
            sub_choice = input("Enter choice (1-4): ").strip()
            
            if sub_choice == "1":
                bed_number = input("Bed Number: ").strip()
                bed_type = input("Bed Type (general/icu/emergency): ").strip()
                ward = input("Ward (optional): ").strip()
                
                result = system.add_bed(bed_number, bed_type, ward)
                print(f"✅ {result['message']}")
                
            elif sub_choice == "2":
                beds = system.get_all_beds()
                print(f"\n🛏️ All Beds ({len(beds)}):")
                for bed in beds:
                    status = "🟢 Available" if bed['status'] == 'available' else "🔴 Occupied"
                    print(f"   {bed['id']}: {bed['bed_number']} ({bed['bed_type']}) - {status}")
                    
            elif sub_choice == "3":
                bed_id = int(input("Bed ID: ").strip())
                patient_id = int(input("Patient ID: ").strip())
                result = system.assign_bed(bed_id, patient_id)
                print(f"✅ {result['message']}" if result['success'] else f"❌ {result['message']}")
                
            elif sub_choice == "4":
                bed_id = int(input("Bed ID: ").strip())
                result = system.release_bed(bed_id)
                print(f"✅ {result['message']}" if result['success'] else f"❌ {result['message']}")
                
        elif choice == "6":
            print("\n💊 Medicine Management:")
            print("1. Add Medicine")
            print("2. View All Medicines")
            print("3. View Low Stock Medicines")
            print("4. View Expired Medicines")
            
            sub_choice = input("Enter choice (1-4): ").strip()
            
            if sub_choice == "1":
                name = input("Medicine Name: ").strip()
                expiry_date = input("Expiry Date (YYYY-MM-DD): ").strip()
                quantity = int(input("Quantity: ").strip())
                unit_price = float(input("Unit Price: ").strip())
                category = input("Category (optional): ").strip()
                minimum_stock_level = int(input("Minimum Stock Level (default 10): ").strip() or "10")
                
                result = system.add_medicine(name, expiry_date, quantity, unit_price, category, minimum_stock_level)
                print(f"✅ {result['message']}")
                
            elif sub_choice == "2":
                medicines = system.get_all_medicines()
                print(f"\n💊 All Medicines ({len(medicines)}):")
                for medicine in medicines:
                    print(f"   {medicine['id']}: {medicine['name']} - Qty: {medicine['quantity']}, Price: ${medicine['unit_price']}")
                    
            elif sub_choice == "3":
                low_stock = system.get_low_stock_medicines()
                print(f"\n⚠️ Low Stock Medicines ({len(low_stock)}):")
                for medicine in low_stock:
                    print(f"   {medicine['name']}: {medicine['quantity']} (Min: {medicine['minimum_stock_level']})")
                    
            elif sub_choice == "4":
                expired = system.get_expired_medicines()
                print(f"\n🚨 Expired Medicines ({len(expired)}):")
                for medicine in expired:
                    print(f"   {medicine['name']}: Expired on {medicine['expiry_date']}")
                    
        elif choice == "7":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
