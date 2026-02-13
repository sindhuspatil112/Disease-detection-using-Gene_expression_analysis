from flask import render_template
from flask import Flask
from flask_login import LoginManager
from backend.database import db
from backend.models import User
from flask import redirect, url_for

from backend.routes.dashboard import dashboard_bp
from backend.routes.history import history_bp
from backend.routes.uploads import upload_bp
from backend.auth import auth_bp
# app.register_blueprint(auth_bp)

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret123"

    # DB settings
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    db.init_app(app)

    login = LoginManager()
    login.login_view = "auth.login"
    login.init_app(app)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def home():
        return render_template("landing.html")
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html', 
                             error_code=403, 
                             error_message="Access Denied: You don't have permission to access this resource."), 403
    
    @app.errorhandler(401)
    def unauthorized(error):
        return redirect(url_for('auth.login'))



    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
