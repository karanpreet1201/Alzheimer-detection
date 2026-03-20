import os
import joblib
import pandas as pd
import logging
from typing import Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
import jwt

# Import DB and Models
from src.database import engine, Base, get_db, User, Patient, get_password_hash, verify_password

# Initialize Tables (SQLite/MySQL/PostgreSQL)
Base.metadata.create_all(bind=engine)

# Security Constants
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Alzheimer's Early Detection API", description="API for predicting early signs of Alzheimer's")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model globally to avoid loading on each request
# Assuming uvicorn is run from the root directory
MODEL_PATH = "models/best_alzheimers_model.joblib"

# Load the model directly at startup
try:
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading model from {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
    else:
        logger.warning(f"Model not found at {MODEL_PATH}. Make sure to run train.py first.")
        model = None
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: Optional[str] = None
    email: Optional[str] = None

class PatientData(BaseModel):
    # Registration Fields
    fullName: str
    gender: str
    address: str
    mobile: str
    email: EmailStr
    
    # Medical Fields
    Age: float = Field(..., description="Age of the patient", ge=40, le=120)
    EDUC: float = Field(..., description="Years of education")
    SES: float = Field(..., description="Socioeconomic Status")
    MMSE: Optional[float] = Field(None, description="Mini-Mental State Examination score (0-30)", ge=0, le=30)
    CDR: float = Field(..., description="Clinical Dementia Rating")
    eTIV: float = Field(..., description="Estimated Total Intracranial Volume (cm3)")
    nWBV: float = Field(..., description="Normalize Whole Brain Volume")
    ASF: float = Field(..., description="Atlas Scaling Factor")
    
    class Config:
        schema_extra = {
            "example": {
                "fullName": "John Doe",
                "gender": "M",
                "address": "123 Main St",
                "mobile": "555-0100",
                "email": "john@example.com",
                "Age": 75.5,
                "EDUC": 14,
                "SES": 2,
                "MMSE": 26.0,
                "CDR": 0.5,
                "eTIV": 1500.0,
                "nWBV": 0.72,
                "ASF": 1.15
            }
        }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email
    }

@app.post("/predict")
def predict(patient: PatientData, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Accepts patient data, returns ML prediction, and stores in database.
    Requires authentication.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. The server cannot serve predictions at this time.")
    
    try:
        # Convert request for ML inference
        ml_data = {
            "Age": patient.Age,
            "EDUC": patient.EDUC,
            "SES": patient.SES,
            "MMSE": patient.MMSE,
            "CDR": patient.CDR,
            "eTIV": patient.eTIV,
            "nWBV": patient.nWBV,
            "ASF": patient.ASF,
            "M/F": patient.gender
        }
        input_df = pd.DataFrame([ml_data])
        
        # Inference
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1] # Probability of class 1 (Early signs)
        
        # Translate to human-readable response
        result_text = "Early signs detected" if prediction == 1 else "No signs detected"
        confidence = float(probability) if prediction == 1 else 1.0 - float(probability)
        
        # Store to DB
        new_patient = Patient(
            full_name=patient.fullName,
            age=patient.Age,
            gender=patient.gender,
            address=patient.address,
            mobile=patient.mobile,
            email=patient.email,
            educ=patient.EDUC,
            ses=patient.SES,
            mmse=patient.MMSE,
            cdr=patient.CDR,
            etiv=patient.eTIV,
            nwbv=patient.nWBV,
            asf=patient.ASF,
            prediction=result_text,
            confidence_score=confidence,
            probability_early_signs=float(probability),
            doctor_id=current_user.id
        )
        db.add(new_patient)
        db.commit()
        
        logger.info(f"Prediction made & DB saved: {result_text} with confidence {confidence:.2f}")
        
        return {
            "prediction": result_text,
            "confidence_score": round(confidence, 4),
            "probability_early_signs": round(float(probability), 4)
        }
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Mount the frontend directory to the root path
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
os.makedirs(frontend_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")