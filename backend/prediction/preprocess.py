import pandas as pd
import io
import os
import json
import logging
from pathlib import Path
from werkzeug.utils import secure_filename

# Base directories
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"

# ------------------------------
# Load ordered gene lists
# ------------------------------
def load_genes_file(fname):
    # Secure filename to prevent path traversal
    secure_fname = secure_filename(fname)
    path = MODELS_DIR / secure_fname
    
    try:
        with open(path, "r") as f:
            genes = json.load(f)
        return [g.strip() for g in genes if isinstance(g, str) and g.strip()]
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to load gene file {fname}: {str(e)}")

BREAST_GENES = load_genes_file("breast_genes.json")
LUNG_GENES = load_genes_file("lung_genes.json")
OVARIAN_GENES = load_genes_file("ovarian_genes.json")

# Build unified list
model_concat = BREAST_GENES + LUNG_GENES + OVARIAN_GENES
MODEL_GENES = list(dict.fromkeys([g.upper() for g in model_concat]))


# ============================================================
# Preprocessing function
# ============================================================
def preprocess_data(file=None, manual_input=None):

    # ------------- FILE INPUT -----------------
    if file is not None:

        filename = getattr(file, "filename", "").lower()

        # Allow .csv, .txt, .tsv, .gz
        if filename.endswith(".csv"):
            df = pd.read_csv(file)

        elif filename.endswith(".txt") or filename.endswith(".tsv"):
            content = file.read().decode("utf-8", errors="ignore")
            df = pd.read_csv(io.StringIO(content), sep=None, engine="python")

        elif filename.endswith(".gz"):
            import gzip
            with gzip.open(file, "rt") as f:
                df = pd.read_csv(f, sep=None, engine="python")

        else:
            raise ValueError("Allowed formats: .csv, .txt, .tsv, .gz")

        if df.empty:
            raise ValueError("Uploaded file contains no data.")

        df.columns = [c.strip().lower() for c in df.columns]

        # Case A — One row
        if df.shape[0] == 1:
            return _filter_to_model_genes(df)

        # Case B — Row-based
        possible_gene_cols = ["gene", "gene_name", "genesymbol", "symbol"]
        possible_value_cols = ["value", "expression", "tpm", "fpkm", "rpkm", "raw_count", "intensity"]

        gene_col = next((c for c in df.columns if c in possible_gene_cols), None)
        val_col = next((c for c in df.columns if c in possible_value_cols), None)

        if gene_col and val_col:
            df_row = df[[gene_col, val_col]].dropna()
            df_row = df_row.set_index(gene_col).T
            df_row.index = ["sample"]
            return _filter_to_model_genes(df_row)

        # Case C — Microarray
        possible_probe = ["probe_id", "probe", "id"]
        if any(col in df.columns for col in possible_probe) and "genesymbol" in df.columns:

            expr_col = next((c for c in possible_value_cols if c in df.columns), None)
            if expr_col is None:
                raise ValueError("Microarray detected but intensity column missing.")

            df_m = df[["genesymbol", expr_col]].groupby("genesymbol").mean()
            df_m = df_m.T
            df_m.index = ["sample"]
            return _filter_to_model_genes(df_m)

        raise ValueError("Unrecognized file format.")

    # ------------ MANUAL INPUT -----------------
    if manual_input and manual_input.strip():
        lines = manual_input.strip().split("\n")
        genes, vals = [], []
        for line in lines:
            parts = line.strip().replace(",", " ").split()
            if len(parts) == 2:
                g, v = parts
                try:
                    vals.append(float(v))
                    genes.append(g)
                except (ValueError, TypeError):
                    pass

        df_manual = pd.DataFrame([vals], columns=[g.upper() for g in genes])
        return _filter_to_model_genes(df_manual)

    raise ValueError("No input provided.")


# ============================================================
# Gene filtering
# ============================================================
def _filter_to_model_genes(df):
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None")
    
    df.columns = [c.upper() for c in df.columns]
    
    usable = [g for g in MODEL_GENES if g in df.columns]
    
    if not usable:
        raise ValueError(f"No matching genes found. Available: {len(df.columns)}, Required: {len(MODEL_GENES)}")
    
    # Remove duplicate columns first, then fill missing genes with 0
    df = df.loc[:, ~df.columns.duplicated()]
    df_final = df.reindex(columns=MODEL_GENES, fill_value=0)
    
    logging.info(f"Gene matching: {len(usable)}/{len(MODEL_GENES)} genes found")
    logging.info(f"Input data shape: {df_final.shape}")
    logging.info(f"Non-zero values in input: {(df_final != 0).sum().sum()}")
    logging.info(f"Sample input values: {df_final.iloc[0, :5].values}")
    
    return df_final
