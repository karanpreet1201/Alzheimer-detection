import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import logging

logger = logging.getLogger(__name__)

def load_data(file_path: str):
    """Loads dataset from CSV."""
    logger.info(f"Loading data from {file_path}")
    return pd.read_csv(file_path)

def get_preprocessor():
    """
    Creates and returns a scikit-learn ColumnTransformer for preprocessing.
    Handles missing values, scaling, and encoding.
    """
    numeric_features = ["Age", "EDUC", "SES", "MMSE", "CDR", "eTIV", "nWBV", "ASF"]
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_features = ["M/F"]
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )
    
    return preprocessor

def get_train_test_split(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """Splits dataframe into train and test sets."""
    # Convert 'Group' to binary target: Demented -> 1, Nondemented -> 0
    df = df[df['Group'].isin(['Demented', 'Nondemented'])].copy()
    df['Target'] = df['Group'].map({'Demented': 1, 'Nondemented': 0})
    
    X = df.drop(columns=["Target", "Subject ID", "MRI ID", "Group", "Hand", "Visit", "MR Delay"], errors="ignore")
    y = df["Target"]
    logger.info(f"Splitting data with test_size={test_size}")
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
