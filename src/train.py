import os
import joblib
import logging
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from preprocessing import load_data, get_preprocessor, get_train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def evaluate_model(y_true, y_pred, y_proba, model_name="Model"):
    """Evaluates the model and logs metrics."""
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_proba)
    
    logger.info(f"--- Evaluation for {model_name} ---")
    logger.info(f"Accuracy:  {acc:.4f}")
    logger.info(f"Precision: {prec:.4f}")
    logger.info(f"Recall:    {rec:.4f}")
    logger.info(f"F1-score:  {f1:.4f}")
    logger.info(f"ROC-AUC:   {roc_auc:.4f}")
    
    return roc_auc

def main():
    data_path = "data/adni_oasis_dataset.csv"
    model_dir = "models"
    
    if not os.path.exists(data_path):
        logger.error(f"Data not found at {data_path}. Please generate it first.")
        return
    
    # Load and split
    df = load_data(data_path)
    X_train, X_test, y_train, y_test = get_train_test_split(df)
    
    # Get preprocessor
    preprocessor = get_preprocessor()
    
    # Define models
    models = {
        "LogisticRegression": LogisticRegression(random_state=42, max_iter=1000),
        "RandomForest": RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    best_roc_auc = 0
    best_model = None
    best_model_name = ""
    
    # Train and evaluate models
    for name, classifier in models.items():
        logger.info(f"Training {name}...")
        
        # Create pipeline
        clf_pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ])
        
        # Train
        clf_pipeline.fit(X_train, y_train)
        
        # Predict
        y_pred = clf_pipeline.predict(X_test)
        
        # Determine how to get probabilities depending on model
        if hasattr(clf_pipeline, "predict_proba"):
            y_proba = clf_pipeline.predict_proba(X_test)[:, 1]
        else:
            y_proba = y_pred # Fallback
            
        # Evaluate
        roc_auc = evaluate_model(y_test, y_pred, y_proba, model_name=name)
        
        # Keep track of the best model based on ROC-AUC
        if roc_auc > best_roc_auc:
            best_roc_auc = roc_auc
            best_model = clf_pipeline
            best_model_name = name
            
    # Save the best model
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "best_alzheimers_model.joblib")
    joblib.dump(best_model, model_path)
    logger.info(f"Best model ({best_model_name}) saved to {model_path}")

if __name__ == "__main__":
    # make sure cwd is at the root since we run data path from here
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root_dir)
    main()
