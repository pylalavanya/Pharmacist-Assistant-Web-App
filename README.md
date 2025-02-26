## **📖 README for Pharmacy Assistant Web App**  

### **🚀 Pharmacy Assistant - Flask Web Application**  
A Flask-based **Pharmacist’s Assistant** that processes **handwritten prescriptions**, extracts patient details and medicines using **OCR**, performs **fuzzy matching** for medicine names, and generates **patient orders**.  

---

## **📌 Features**
 **Upload Handwritten Prescription** (OCR Processing)  
 **Extract and Match Medicines from Database**  
 **Admin Panel** (Add, Edit, Delete Medicines)  
 **Manage Orders** (Update Status, Delete)  
 **Generate Detailed PDF Receipts**  
 **"Back to Home" Button for Easy Navigation**  

---

## **🛠️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/pharmacy-assistant.git
cd pharmacy-assistant
```

### **2️⃣ Create a Virtual Environment** (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **⚙️ Configuration**
### **🔹 Database Setup**
The app uses **SQLite** as the database. If `pharmacy.db` does not exist, create it with:
```bash
python setup_db.py
```
This will create the required tables:  
- `orders` → Stores patient prescriptions & matched medicines  
- `medicines` → Stores medicine details  

---

## **▶️ Running the Application**
```bash
python app.py
```
- The app will be available at **`http://127.0.0.1:5000/`**  
- Navigate to **`/admin`** to manage medicines  
- Navigate to **`/orders`** to view and manage orders  

---

## **📂 Project Structure**
```
📦 pharmacy-assistant
│-- 📂 static          # CSS & frontend assets
│-- 📂 templates       # HTML templates
│-- 📂 uploads         # Uploaded prescriptions & generated PDFs
│-- app.py            # Main Flask app
│-- ocr.py            # OCR processing logic
│-- setup_db.py       # Database initialization script
│-- requirements.txt  # Required Python packages
│-- README.md         # Project documentation
```

---

## **📝 API Routes**
| Route                 | Method | Description |
|-----------------------|--------|-------------|
| `/`                   | GET, POST | Upload prescription and extract text |
| `/orders`             | GET    | View all orders |
| `/update_status/<id>` | POST   | Update order status |
| `/generate_receipt/<id>` | GET | Download receipt as PDF |
| `/admin`              | GET    | Manage medicines |
| `/add_medicine`       | POST   | Add new medicine |
| `/edit_medicine/<id>` | POST   | Edit existing medicine |
| `/delete_medicine/<id>` | POST | Delete medicine |

---

## **🛠️ Dependencies**
The project uses the following Python libraries:
```txt
Flask
SQLite3
Pytesseract (OCR)
ReportLab (PDF Generation)
Pillow (Image Processing)
FuzzyWuzzy (Fuzzy Matching)
```

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## **🔹 Contribution**
Feel free to **fork** this repository, submit **issues**, or open a **pull request**. 🚀  

---

## **💡 Future Improvements**
🔹 Implement **User Authentication**  
🔹 Enhance **OCR Accuracy** using Deep Learning  
🔹 Integrate **Medicine Inventory Management**  

---

## **📜 License**
This project is **MIT Licensed**. Feel free to use and modify.  

---

## **📬 Contact**
🔹 **Author:** Pyla Lavanya  
🔹 **Email:** lavanyapyla6543@gmail.com  
🔹 **GitHub:** https://github.com/pylalavanya  

---
  
