# Rank Predictor API

FastAPI application that predicts rank ranges based on marks and category.

## Deployment on Render

### Option 1: Deploy through Render Dashboard

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" and select "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - Name: rank-predictor-api (or your preferred name)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

### Option 2: Deploy using render.yaml

1. Push your code with the render.yaml to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the render.yaml and set up the service

## Local Development

```
pip install -r requirements.txt
uvicorn app:app --reload
```

Access the API at http://localhost:8000/docs

## API Endpoints

### Predict Rank

**Endpoint**: `/predict`
**Method**: POST
**Request Body**:
```json
{
    "marks": 650,
    "category": "General"
}
```

Category options: "General", "OBC-NCL", "SC", "ST"

**Response**:
```json
{
    "rank_range": [90000, 110000],
    "category_rank_range": null
}
```

## Documentation

FastAPI automatically generates API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 