from flask import Blueprint, render_template
from flask_login import login_required, current_user
from backend.decorators import role_required
from backend.models import Prediction, User, SharedReport, Consultation
from backend.database import db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    # Get user's prediction history
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).limit(5).all()
    
    if current_user.role == "admin":
        total_users = User.query.count()
        total_predictions = Prediction.query.count()
        return render_template("admin_dashboard.html", total_users=total_users, total_predictions=total_predictions)
    elif current_user.role == "doctor":
        # Get all predictions with risk analysis
        all_predictions = Prediction.query.order_by(Prediction.timestamp.desc()).all()
        
        # Calculate risk statistics
        high_risk_count = 0
        total_patients = len(set([p.user_id for p in all_predictions]))
        
        for pred in all_predictions:
            if pred.results_json:
                import json
                results = json.loads(pred.results_json)
                # Count as high risk if any cancer type >= 70%
                if any(isinstance(v, (int, float)) and v >= 70 for v in results.values()):
                    high_risk_count += 1
        
        return render_template("doctor_dashboard.html", 
                             predictions=all_predictions[:10], 
                             total_patients=total_patients,
                             high_risk_count=high_risk_count,
                             total_predictions=len(all_predictions))
    elif current_user.role == "researcher":
        return render_template("researcher_dashboard.html", user_predictions=user_predictions)
    else:
        return render_template("user_dashboard.html", user_predictions=user_predictions)

@dashboard_bp.route("/doctor/notes")
@login_required
@role_required('doctor')
def doctor_notes():
    return render_template("doctor_notes.html")

@dashboard_bp.route("/doctor/analytics")
@login_required
@role_required('doctor')
def doctor_analytics():
    return render_template("doctor_analytics.html")

@dashboard_bp.route("/research/biomarkers")
@login_required
@role_required('researcher')
def research_biomarkers():
    return render_template("research_biomarkers.html")

@dashboard_bp.route("/research/models")
@login_required
@role_required('researcher')
def research_models():
    return render_template("research_models.html")

@dashboard_bp.route("/research/cross-analysis")
@login_required
@role_required('researcher')
def research_cross_analysis():
    return render_template("research_cross_analysis.html")

@dashboard_bp.route("/collaboration")
@login_required
@role_required('doctor', 'researcher')
def collaboration():
    from backend.models import User, SharedReport, Consultation
    
    # Get doctors and researchers for sharing
    doctors = User.query.filter_by(role='doctor').all()
    researchers = User.query.filter_by(role='researcher').all()
    patients = User.query.filter_by(role='user').all()
    
    # Get user's predictions for dropdown
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).all()
    
    # Get shared reports
    shared_reports = SharedReport.query.filter(
        (SharedReport.from_user_id == current_user.id) | 
        (SharedReport.to_user_id == current_user.id)
    ).order_by(SharedReport.timestamp.desc()).all()
    
    return render_template("collaboration.html", 
                         doctors=doctors, 
                         researchers=researchers,
                         patients=patients,
                         user_predictions=user_predictions,
                         shared_reports=shared_reports)

@dashboard_bp.route("/patient/consult")
@login_required
@role_required('user')
def patient_consult():
    from backend.models import User
    
    # Get available doctors
    doctors = User.query.filter_by(role='doctor').all()
    
    # Get patient's predictions for consultation
    patient_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).all()
    
    return render_template("patient_consult.html", 
                         doctors=doctors,
                         patient_predictions=patient_predictions)

@dashboard_bp.route("/admin/users")
@login_required
@role_required('admin')
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)

@dashboard_bp.route("/admin/analytics")
@login_required
@role_required('admin')
def admin_analytics():
    total_users = User.query.count()
    total_predictions = Prediction.query.count()
    user_roles = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
    return render_template("admin_analytics.html", 
                         total_users=total_users,
                         total_predictions=total_predictions,
                         user_roles=user_roles)
