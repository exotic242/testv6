
from flask import Flask
from routes.public import public_bp
from routes.student import student_bp
from routes.admin import admin_bp

app = Flask(name)
app.secret_key = "your-secret-key"


app.register_blueprint(public_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)

if name == "main":
    app.run(debug=True)