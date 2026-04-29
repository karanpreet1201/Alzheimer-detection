# Authors

## Karanpreet Singh -  2210990482
## Karishma Dhawan -   2210990483
## Kanishk Kharbanda - 2210990472
## Jasmine Rathor -    2210990450

# Early Diagnosis of Alzheimer’s Disease Using Machine Learning

This repository contains a complete backend pipeline to generate synthetic data, train an ML model, and serve inferences via a REST API.

## Requirements

1. Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `src/data_generator.py`: Generates the synthetic dataset (`data/alzheimers_data.csv`).
- `src/preprocessing.py`: Defines the sklearn preprocessing pipeline (handling missing values, scaling, encoding).
- `src/train.py`: Trains Logistic Regression and Random Forest models, evaluates them, and saves the best pipeline using `joblib`.
- `src/app.py`: Contains the FastAPI application and REST endpoint `/predict`.

## How to Run

1. **Train Model**
   Run the training script to generate data and train the ML models:
   ```bash
   python src/train.py
   ```
   *This saves the best model artifacts to `models/best_alzheimers_model.joblib`.*

2. **Start the API server**
   Use `uvicorn` to start the FastAPI server:
   ```bash
   uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Make a Prediction**
   You can go to `http://localhost:8000/docs` to use the Swagger UI, or run a `curl` request:
   
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/predict' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
     "Age": 75.5,
     "MMSE": 22.0,
     "APOE4_Alleles": 1,
     "BrainVolume_cm3": 1150.0,
     "MemoryTestScore": 60.0
   }'
   ```
   
   **Response:**
   ```json
   {
     "prediction": "Early signs detected",
     "confidence_score": 0.8245,
     "probability_early_signs": 0.8245
   }
   ```
