from flask import Blueprint, request, redirect, render_template, flash
from flask_login import current_user, login_required
from backend.models import Prediction
from backend.database import db
from backend.prediction.run_predictions import run_predictions
from backend.prediction.preprocess import preprocess_data
from backend.decorators import role_required
import json

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
@login_required
@role_required('user', 'doctor', 'researcher')
def upload():
    if request.method == "POST":
        file = request.files["file"]
        
        if not file or file.filename == '':
            flash("Please select a file", "error")
            return render_template("index.html")

        try:
            processed = preprocess_data(file)
            results, shared = run_predictions(processed)

            p = Prediction(
                filename=file.filename,
                results_json=json.dumps(results),
                shared_json=json.dumps(shared),
                user_id=current_user.id
            )
            db.session.add(p)
            db.session.commit()
            
            flash("Prediction completed successfully!", "success")
            return render_template("result.html", results=results, shared_genes=shared, user_role=current_user.role)
        
        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return render_template("index.html")

    return render_template("index.html")
