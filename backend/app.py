# backend/app.py
from flask import Flask
from flask_cors import CORS
from routes.analyze import analyze

app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend

# Register blueprints
app.register_blueprint(analyze)

if __name__ == '__main__':
    app.run(debug=True)
