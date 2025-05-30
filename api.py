from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
from main import process_input

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process-file/")
def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = process_input(file_path)
    return JSONResponse(content=result)

@app.post("/process-json/")
def process_json_input(json_data: dict):
    import json
    temp_path = os.path.join(UPLOAD_DIR, "temp.json")
    with open(temp_path, "w") as f:
        json.dump(json_data, f)
    result = process_input(temp_path)
    return JSONResponse(content=result)

@app.post("/process-email/")
def process_email_input(email_text: str = Form(...)):
    temp_path = os.path.join(UPLOAD_DIR, "temp_email.txt")
    with open(temp_path, "w") as f:
        f.write(email_text)
    result = process_input(temp_path)
    return JSONResponse(content=result) 