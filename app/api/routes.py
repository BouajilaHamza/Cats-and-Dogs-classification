from fastapi import APIRouter, UploadFile, File
from app.data.data_loader import DataLoader

router = APIRouter()

@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict whether an uploaded image is a cat or dog
    """
    # Add prediction logic here
    return {"filename": file.filename, "prediction": "cat"}

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

@router.post("/update_data")
async def update_data():
    """
    Update data endpoint
    """
    data_loader = DataLoader()
    cat_bytes, dog_bytes = await data_loader.fetch_data()
    data_loader.save_data(cat_bytes, dog_bytes)
    return {"status": "data updated"}
