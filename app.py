from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
from mangum import Mangum
import os

# Load optimized trained model from current directory
model = joblib.load('optimized_rank_predictor_model.pkl')

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class PredictionRequest(BaseModel):
    marks: float
    category: str

class PredictionResponse(BaseModel):
    rank_range: List[int]
    category_rank_range: Optional[List[int]] = None

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: PredictionRequest):
    try:
        # Predict rank using the ML model
        predicted_rank = model.predict(np.array([[data.marks]]))[0]
        predicted_rank = int(round(predicted_rank))
        lower_bound = int(round(predicted_rank * 0.9))
        upper_bound = int(round(predicted_rank * 1.1))

        response = {
            "rank_range": [lower_bound, upper_bound],
            "category_rank_range": None
        }

        # Calculate category rank range if applicable
        if data.category != "General":
            if data.category == "OBC-NCL":
                cat_rank = int(round(0.25 * (predicted_rank ** 1.01)))
            elif data.category == "SC":
                cat_rank = int(round(0.01716 * (predicted_rank ** 1.02338)))
            elif data.category == "ST":
                cat_rank = int(round(0.007465 * (predicted_rank ** 1.04465)))
            else:
                raise HTTPException(status_code=400, detail="Invalid category")

            cat_lb = int(round(cat_rank * 0.9))
            cat_ub = int(round(cat_rank * 1.1))
            response["category_rank_range"] = [cat_lb, cat_ub]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handler for AWS Lambda
handler = Mangum(app)

if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
