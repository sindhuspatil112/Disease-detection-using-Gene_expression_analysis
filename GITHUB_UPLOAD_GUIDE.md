# GitHub Upload Summary

## ✅ FILES TO KEEP (Will be uploaded to GitHub)

### Application Code
- `backend/*.py` - All Python application files
- `backend/routes/*.py` - Route handlers
- `backend/prediction/*.py` - ML prediction logic
- `backend/templates/*.html` - All HTML templates
- `backend/static/css/*.css` - Stylesheets
- `backend/static/images/logo.jpg` - Logo (if small)

### Configuration & Setup
- `requirements.txt` - Python dependencies
- `run_app.py` - Application launcher
- `create_admin.py` - Admin user creation
- `create_user.py` - User creation utility
- `demo_setup.py` - Demo setup script
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation
- `README_ROLES.md` - Role documentation
- `SETUP_INSTRUCTIONS.md` - Setup guide
- `system_architecture_flowchart.md` - Architecture docs

### Small Reference Files
- `backend/models/*.json` - Gene lists (small files)
- `scripts/*.ipynb` - Training notebooks (code only)

### Scripts
- `remove_large_files.bat` - Git cleanup script

---

## ❌ FILES EXCLUDED (Too large for GitHub)

### Data Files (~100+ MB)
- `data/labeled/*.csv` - Labeled datasets
- `data/mapped/*.csv` - Mapped datasets
- `data/preprocessed/*.csv` - Preprocessed data
- `data/*.txt` - Series matrix files
- `data/*.annot` - Annotation files

### Model Files (~50+ MB each)
- `backend/models/breast_balanced_model.pkl`
- `backend/models/breast_model.pkl`
- `backend/models/lung_balanced_model.pkl`
- `backend/models/lung_model.pkl`
- `backend/models/ovarian_balanced_model.pkl`
- `backend/models/ovarian_model.pkl`
- `backend/models/cross_cancer_union_model.pkl`
- `backend/models/cross_overlap_pairwise_overlap_model.pkl`
- `backend/models/biomarkers/` - Biomarker data

### Database Files (Generated)
- `instance/data.db`
- `backend/instance/data.db`

### Output Files (Generated)
- `outputs/metrics/*.csv` - Metric files
- `outputs/metrics/*.png` - Confusion matrices

### Cache & Temporary Files
- `__pycache__/` - Python cache
- `.ipynb_checkpoints/` - Notebook checkpoints
- `*.pyc` - Compiled Python files

---

## 📊 Size Comparison

**Before cleanup**: ~500+ MB (Cannot upload to GitHub)
**After cleanup**: ~5-10 MB (Ready for GitHub)

---

## 🚀 Upload Steps

1. **Run the cleanup script**:
   ```bash
   remove_large_files.bat
   ```

2. **Stage all files**:
   ```bash
   git add .
   ```

3. **Commit changes**:
   ```bash
   git commit -m "Initial commit - Remove large files"
   ```

4. **Push to GitHub**:
   ```bash
   git push origin main
   ```

---

## 📦 Hosting Large Files

Consider hosting excluded files on:
- **Google Drive** - Free up to 15GB
- **Dropbox** - Free up to 2GB
- **AWS S3** - Pay as you go
- **Kaggle Datasets** - Free for public datasets
- **Hugging Face** - Free for ML models

Update the download links in `SETUP_INSTRUCTIONS.md` after uploading.
