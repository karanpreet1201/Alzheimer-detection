from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from datetime import datetime

# MySQL Database URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:karanhunny8168@localhost/patientDB"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Password Hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Relationship to patients assessed by this user (e.g. if the user is a doctor)
    patients = relationship("Patient", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Float, nullable=False)
    gender = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    
    # Medical details
    educ = Column(Float, nullable=False)
    ses = Column(Float, nullable=False)
    mmse = Column(Float, nullable=True) # or False
    cdr = Column(Float, nullable=False)
    etiv = Column(Float, nullable=False)
    nwbv = Column(Float, nullable=False)
    asf = Column(Float, nullable=False)
    
    # Analysis Result
    prediction = Column(String(50), nullable=True)
    confidence_score = Column(Float, nullable=True)
    probability_early_signs = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Who performed the assessment
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    doctor = relationship("User", back_populates="patients")

def get_db():
    """Dependency to get the DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Depending on passlib/bcrypt version, we may need to handle strings
    return pwd_context.hash(password)
