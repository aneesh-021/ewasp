from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()   # read file as bytes

        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return {"error": "Unsupported file format"}

        preview = df.head().to_dict(orient="records")

        return {
            "filename": file.filename,
            "columns": list(df.columns),
            "preview": preview
        }

    except Exception as e:
        return {"error": str(e)}