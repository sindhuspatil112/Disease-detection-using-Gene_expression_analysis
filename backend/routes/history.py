from flask import Blueprint, render_template
from backend.models import Prediction
from flask_login import login_required, current_user
import json

history_bp = Blueprint("history", __name__)

@history_bp.route("/history")
@login_required
def history():
    if current_user.role == 'doctor':
        # Doctors see all predictions from all users
        data = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    else:
        # Other roles see only their own predictions
        data = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).all()

    formatted = [
        {
            "filename": p.filename,
            "timestamp": p.timestamp,
            "results": json.loads(p.results_json) if p.results_json else {},
            "user_id": p.user_id
        }
        for p in data
    ]

    return render_template("history.html", items=formatted, user_role=current_user.role)
