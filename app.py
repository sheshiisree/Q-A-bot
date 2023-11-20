# main.py
import logging

from flask import Flask, request
from flask_cors import CORS
from datetime import timedelta

# Importing blueprints for different routes
from routes.bot import bot as bot_router

from flask_jwt_extended import JWTManager

# Importing database configuration
from database import Base, engine

# Initializing Flask app
app = Flask(__name__)

# JWT configurations
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# Apply CORS to the app (uncomment if needed)
# CORS(app, resources={r"*": {"origins": "*"}})

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Registering the blueprints for different parts of the application
app.register_blueprint(bot_router, url_prefix="/bot")

# Function to log request details before processing
@app.before_request
def before_request():
    print("Request Received:")
    print("URL:", request.url)
    print("Method:", request.method)
    print("Query Params:", request.args)
    if request.method == "POST":
        if request.content_type.startswith("application/json"):
            request_body = request.get_json()
            if 'base64' in request_body:
                print("Request has base64 data so skipping print")
            else:
                print("Body (JSON):", request_body)
        elif request.content_type.startswith("multipart/form-data"):
            print("Form Data:")
            for key, value in request.form.items():
                print(f"{key}: {value}")
    else:
        print("Body: No request body")


# Function to log response details and handle CORS headers
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST")

    print("Response Sent:")
    print("Status Code:", response.status_code)
    print("Content Type:", response.content_type)

    if response.content_type == "application/json":
        print("Data:", response.get_json())
    elif response.content_type.startswith("image/") or response.content_type.startswith(
        "application/"
    ):
        print("File Response: Not Printing Binary Data")
    else:
        print("Data:", response.get_data(as_text=True))
    return response



if __name__ == "__main__":
    from models.chat import Chat

    Base.metadata.create_all(engine)

    app.run(host="0.0.0.0", debug=True, port=5000)
