# Streamoid Product CSV Parser (FastAPI + SQLite)

## Features
- Upload product data using CSV file  
- Automatically skip duplicate SKUs  
- Validate data before saving (e.g., price ≤ mrp)  
- Store data in SQLite database  
- Fetch all products  
- Search by brand, color, or name  

---

## Tech Stack
- **Backend:** FastAPI  
- **Database:** SQLite (via SQLAlchemy ORM)  
- **Language:** Python 3  
- **Server:** Uvicorn  

---

##  Project Structure
```
streamoid-backend/
├── main.py
├── database.py
├── models.py
├── utils.py
├── products.csv
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### nstall Dependencies
```bash
pip install fastapi uvicorn sqlalchemy python-multipart pydantic
```

---

## Run the Backend Server
```bash
uvicorn main:app --reload
```

or  
```bash
python -m uvicorn main:app --reload
```

Then open docs here 👇  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

You should see:
```json
{"message": "Welcome to Streamoid Backend 🚀"}
```

---

## Upload CSV Endpoint

### **POST /upload**
Upload your CSV file to add products.

**Body (form-data):**
- Key: `file`
- Value: select your `products.csv` file

**Example CSV Format:**
```csv
sku,name,brand,color,size,mrp,price,quantity
TSHIRT-RED-001,Classic Cotton T-Shirt,StreamThreads,Red,M,799,499,20
POLO-GRN-003,Heritage Polo,StreamThreads,Green,XL,1299,999,8
```

**Example cURL Command:**
```bash
curl -X POST -F "file=@products.csv" http://localhost:8000/upload
```

**Example Response:**
```json
{
  "message": "✅ Uploaded 18 new products. ⏩ Skipped 2 duplicates."
}
```

---

## Get All Products

### **GET /products**
Returns all stored products.  
**Example:**  
```
http://localhost:8000/products
```

---

## Search Products

### **GET /products/search**
Search using brand, color, or name.

**Query Examples:**
```
/products/search?brand=StreamThreads
/products/search?color=Red
/products/search?name=T-Shirt
```

**Response Example:**
```json
[
  {
    "sku": "TSHIRT-RED-001",
    "name": "Classic Cotton T-Shirt",
    "brand": "StreamThreads",
    "color": "Red",
    "size": "M",
    "mrp": 799,
    "price": 499,
    "quantity": 20
  }
]
```

---

## Notes
- Duplicate SKUs are automatically skipped  
- You can view and test all endpoints at `/docs`  
- Works fully offline (no external DB needed)

---


