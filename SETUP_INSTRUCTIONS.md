# GeneRisk AI - Setup Instructions

## Files Not Included in GitHub (Due to Size)

The following files are excluded from this repository due to GitHub's file size limitations:

### 1. **Machine Learning Models** (Required)
- `backend/models/*.pkl` files
- Download from: [Add your cloud storage link here]

### 2. **Training Data** (Optional - for research/training)
- `data/` folder with all datasets
- Download from: [Add your cloud storage link here]

### 3. **Database** (Auto-generated)
- `instance/data.db` - Will be created automatically on first run

## Quick Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd comb_disease_predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download required model files**
- Download the models folder from [cloud storage link]
- Place `.pkl` and `.json` files in `backend/models/`

4. **Run the application**
```bash
python run_app.py
```

5. **Access the application**
- Open browser: http://localhost:5000
- Use demo credentials from the console output

## File Structure (After Setup)

```
comb_disease_predictor/
├── backend/
│   ├── models/
│   │   ├── breast_balanced_model.pkl  (Download required)
│   │   ├── lung_balanced_model.pkl    (Download required)
│   │   ├── ovarian_balanced_model.pkl (Download required)
│   │   ├── breast_genes.json          (Included)
│   │   ├── lung_genes.json            (Included)
│   │   └── ovarian_genes.json         (Included)
│   └── ...
├── data/                               (Optional - for training)
├── instance/                           (Auto-generated)
└── ...
```

## Alternative: Use Pre-trained Models

If you don't have access to the original models, you can:
1. Train new models using the notebooks in `scripts/`
2. Use the training data from public sources (GEO datasets)

## Support

For issues or questions, please open a GitHub issue.
