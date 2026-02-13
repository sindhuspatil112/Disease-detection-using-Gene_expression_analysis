import os
import json
import pickle
import pandas as pd
import joblib
import logging
from pathlib import Path
from werkzeug.utils import secure_filename

# Define base directories
BASE_DIR = Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "models"



# -------------------------------------------------------
# Helper: Load model + CLEAN gene list
# -------------------------------------------------------
def load_model_and_genes(model_name, gene_file):
    # Secure filenames to prevent path traversal
    secure_model = secure_filename(model_name)
    secure_gene = secure_filename(gene_file)
    
    model_path = MODEL_DIR / secure_model
    gene_path = MODEL_DIR / secure_gene

    try:
        # Load model
        model = joblib.load(model_path)
        
        # Load gene list
        with open(gene_path, "r") as f:
            genes = json.load(f)
    except (FileNotFoundError, PermissionError) as e:
        raise ValueError(f"Failed to load model files: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error loading model or genes: {str(e)}")

    # --------- CLEAN GENE LIST ---------
    cleaned = []
    for g in genes:
        if not isinstance(g, str):
            continue

        g = g.strip().upper()

        # Expand merged genes like ABC1///ABC2///ABC3
        if "///" in g:
            parts = [p.strip().upper() for p in g.split("///") if p.strip()]
            cleaned.extend(parts)
        else:
            cleaned.append(g)

    # Remove duplicates (preserve order)
    cleaned = list(dict.fromkeys(cleaned))

    return model, cleaned


# -------------------------------------------------------
# Load models + genes
# -------------------------------------------------------
breast_model, breast_genes = load_model_and_genes("breast_balanced_model.pkl", "breast_genes.json")
ovarian_model, ovarian_genes = load_model_and_genes("ovarian_balanced_model.pkl", "ovarian_genes.json")
lung_model, lung_genes = load_model_and_genes("lung_balanced_model.pkl", "lung_genes.json")


# -------------------------------------------------------
# Main prediction function
# -------------------------------------------------------
def run_predictions(sample_df):
    """
    sample_df must be:
    - DataFrame of 1 row
    - gene names as columns
    """
    # Input validation
    if not isinstance(sample_df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    if sample_df.empty or len(sample_df) == 0:
        raise ValueError("Input DataFrame is empty")
    
    results = {}

    # Normalize uploaded gene column names
    sample_df.columns = [c.upper() for c in sample_df.columns]

    # REMOVE duplicate columns from sample
    sample_df = sample_df.loc[:, ~sample_df.columns.duplicated(keep='first')]

    shared_genes = {}   # NEW — to track overlaps

    # ---------------------------------------------------
    # Inner function for each cancer type
    # ---------------------------------------------------
    def predict_for(model, disease_name):
        # Use exact order used during training
        expected_genes = list(model.feature_names_in_)

        logging.info(f"Checking {disease_name} gene list - Expected: {len(expected_genes)} genes")
        logging.info(f"Duplicates found: {pd.Index(expected_genes).duplicated().sum()}")

        # Find usable genes
        matched = [g for g in expected_genes if g in sample_df.columns]

        shared_genes[disease_name] = matched   # SAVE OVERLAP

        if not matched:
            results[disease_name] = "Insufficient gene overlap"
            logging.warning(f"No gene overlap found for {disease_name}")
            return

        # Build input vector in model's expected order
        X = sample_df.reindex(columns=expected_genes, fill_value=0)
        
        # Log input data for debugging
        logging.info(f"{disease_name} - Input shape: {X.shape}")
        logging.info(f"{disease_name} - Non-zero values: {(X != 0).sum().sum()}")
        logging.info(f"{disease_name} - Sample values: {X.iloc[0, :5].values}")

        # Convert to numpy row
        values = X.values.reshape(1, -1)

        # Run prediction
        try:
            prob = float(model.predict_proba(values)[0][1] * 100)
        except Exception as e:
            results[disease_name] = f"Error: {str(e)}"
            return

        results[disease_name] = round(prob, 2)

    # ---------------------------------------------------
    # Run predictions for all 3 cancers
    # ---------------------------------------------------
    predict_for(breast_model, "breast")
    predict_for(ovarian_model, "ovarian")
    predict_for(lung_model, "lung")

    logging.info(f"Prediction results: {results}")

    # Return BOTH for template
    return results, shared_genes
