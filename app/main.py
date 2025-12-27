from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.ocr_logic import extract_structured_data

app = FastAPI(title="Garment OCR API")

class GarmentOCRResponse(BaseModel):
    branch: str
    bill_no: str
    garment_type: str
    category: str
    date: str
    customer_name: str
    customer_address: str


@app.post("/extract-garment-data", response_model=GarmentOCRResponse)
async def extract_garment_data(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return extract_structured_data(image_bytes)
