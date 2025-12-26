# from fastapi import FastAPI, UploadFile, File
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse

# from app.ocr_logic import extract_text_from_image

# app = FastAPI(
#     title="Image to Text OCR API",
#     version="1.0.0",
#     description="Upload any image and get extracted text"
# )

# # ✅ Response schema
# class OCRResponse(BaseModel):
#     status: bool
#     extracted_text: str


# @app.post(
#     "/image-to-text",
#     response_model=OCRResponse,
#     summary="Image to Text",
#     description="Upload any image file and extract readable text using OCR"
# )
# async def image_to_text(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     text = extract_text_from_image(image_bytes)

#     if not text:
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": False,
#                 "extracted_text": ""
#             }
#         )

#     return {
#         "status": True,
#         "extracted_text": text
#     }




# from fastapi import FastAPI, UploadFile, File
# from pydantic import BaseModel

# from app.ocr_logic import extract_structured_data

# app = FastAPI(
#     title="Garment OCR Structured API",
#     version="1.0.0"
# )

# class GarmentOCRResponse(BaseModel):
#     branch: str
#     bill_no: str
#     garment_type: str
#     category: str
#     date: str
#     customer_name: str
#     customer_address: str


# @app.post("/extract-garment-data", response_model=GarmentOCRResponse)
# async def extract_garment_data(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     data = extract_structured_data(image_bytes)

#     return {
#         "branch": data.get("branch", ""),
#         "bill_no": data.get("bill_no", ""),
#         "garment_type": data.get("garment_type", ""),
#         "category": data.get("category", ""),
#         "date": data.get("date", ""),
#         "customer_name": data.get("customer_name", ""),
#         "customer_address": data.get("customer_address", "")
#     }



from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.ocr_logic import extract_structured_data

app = FastAPI(
    title="Garment OCR Structured API",
    version="1.0.0"
)

# ✅ ROOT ROUTE (IMPORTANT)
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Garment OCR Structured API is running 🚀",
        "docs": "/docs"
    }


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
    data = extract_structured_data(image_bytes)

    return {
        "branch": data.get("branch", ""),
        "bill_no": data.get("bill_no", ""),
        "garment_type": data.get("garment_type", ""),
        "category": data.get("category", ""),
        "date": data.get("date", ""),
        "customer_name": data.get("customer_name", ""),
        "customer_address": data.get("customer_address", "")
    }