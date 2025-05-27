from flask import Flask
from routes.public import public_bp
from routes.student import student_bp
from routes.admin import admin_bp
app = Flask(__name__)
app.secret_key = "your-secret-key"
# Register blueprints
app.register_blueprint(public_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)
if __name__ == "__main__":
    app.run(debug=True)
# Main app entry point