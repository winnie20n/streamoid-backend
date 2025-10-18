from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import csv
import io

from database import SessionLocal, engine, Base
from models import Product
from utils import get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Streamoid Backend", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to Streamoid Backend 🚀"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        content = await file.read()
        decoded = content.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(decoded))
        count, skipped = 0, 0

        for row in csv_reader:
            sku = row["sku"].strip()

            
            existing = db.query(Product).filter(Product.sku == sku).first()
            if existing:
                skipped += 1
                continue

            product = Product(
                sku=sku,
                name=row["name"].strip(),
                brand=row["brand"].strip(),
                color=row["color"].strip(),
                size=row["size"].strip(),
                mrp=float(row["mrp"]) if row["mrp"] else 0.0,
                price=float(row["price"]) if row["price"] else 0.0,
                quantity=int(row["quantity"]) if row["quantity"] else 0,
            )
            db.add(product)
            count += 1

        db.commit()
        return {
            "message": f"✅ Uploaded {count} new products. ⏩ Skipped {skipped} duplicates."
        }

    except Exception as e:
        print("❌ Error uploading CSV:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@app.get("/products/search")
def search_products(
    brand: str | None = None,
    color: str | None = None,
    name: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    if color:
        query = query.filter(Product.color.ilike(f"%{color}%"))
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    return query.all()


@app.on_event("startup")
def startup_event():
    print("🚀 Starting backend... creating tables if not exist.")
    Base.metadata.create_all(bind=engine)
