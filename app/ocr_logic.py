import cv2
import numpy as np
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

AREA_KEYWORDS = ["vihar", "nagar", "bagh", "colony", "sector", "city"]

def clean(line: str) -> str:
    return re.sub(r"[^A-Za-z0-9\s.-]", "", line).strip()


def extract_structured_data(image_bytes: bytes) -> dict:
    # -------- OCR --------
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return {}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    raw_text = pytesseract.image_to_string(
        gray, lang="eng", config="--psm 6"
    )

    lines = [clean(l) for l in raw_text.splitlines() if l.strip()]

    data = {
        "branch": "",
        "bill_no": "",
        "garment_type": "",
        "category": "",
        "date": "",
        "customer_name": "",
        "customer_address": ""
    }

    bill_index = -1
    date_index = -1

    # ---------- PASS 1: STRONG PATTERNS ----------
    for i, line in enumerate(lines):
        l = line.lower()

        # Bill No
        bill = re.search(r"h\d{4}-\d-\d", l)
        if bill:
            data["bill_no"] = bill.group().upper()
            bill_index = i

        # Date
        date = re.search(r"\d{2}\s[a-z]{3}\s\d{2}\s[a-z]{3}", l)
        if date:
            data["date"] = date.group().title()
            date_index = i

        # Branch (location-like text)
        if any(k in l for k in AREA_KEYWORDS):
            if not data["branch"]:
                data["branch"] = line

    # ---------- PASS 2: RELATIVE POSITION ----------
    for i, line in enumerate(lines):
        # Garment Type → immediately after bill line
        if bill_index != -1 and i == bill_index + 1:
            if re.fullmatch(r"[A-Za-z]{3,}\s?\d*", line):
                data["garment_type"] = line.split()[0].title()

        # Category → line containing 2-letter code near garment
        if (
            data["garment_type"]
            and re.search(r"\b[A-Z]{2}\b", line)
            and not data["category"]
        ):
            data["category"] = re.search(
                r"\b[A-Z]{2}\b", line
            ).group()

        # Customer Name → line after date
        if date_index != -1 and i == date_index + 1:
            if line.istitle() and len(line.split()) == 1:
                data["customer_name"] = line

        # Address → line after name
        if (
            data["customer_name"]
            and i > date_index + 1
            and re.match(r"[A-Z]{1,3}\d+", line)
        ):
            data["customer_address"] = line
            break

    return data
