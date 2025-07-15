
print("DEBUG: app/main.py load!")
import sqlite3
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from flask import Flask, request, jsonify
from app.config import Config
from app.models import QueryRequest, AnswerResponse
from api.endpoints import api_blueprint
from api.swagger import swagger_spec
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from rag.chain import warmup_model

import os


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "AI RAG Agent API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.add_url_rule(API_URL, 'swagger_spec', swagger_spec)

app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "AI RAG Agent is running!"})

if __name__ == '__main__':
    warmup_model()
    app.run(host='0.0.0.0', port=5000, debug=True)