from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read file based on type
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
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