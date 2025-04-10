from flask import Blueprint
import pandas
import flask
from io import BytesIO
import os
from werkzeug.utils import secure_filename
import openpyxl
import xlrd


upload_excel_bp = Blueprint('upload_excel_bp', __name__)


ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
UPLOAD_FOLDER = './uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_excel_bp.route("/upload-excel", methods=["POST"])
def handle_upload_excel():
    # breakpoint()
    prompt = flask.request.form.get("prompt")
    file = flask.request.files.get("excelFile")

    if not file or file.filename == '':
        return flask.jsonify({"success": False, "message": "No file uploaded"}), 400

    if not prompt:
        return flask.jsonify({"success": False, "message": "Prompt is required"}), 400
    

    filename = secure_filename(file.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file_stream = BytesIO(file.read())

    if filename.endswith('.xlsx'):
        df = pandas.read_excel(file_stream, engine='openpyxl')
    elif filename.endswith('.xls'):
        df = pandas.read_excel(file_stream, engine='xlrd')
    elif filename.endswith('.csv'):
        df = pandas.read_csv(file_stream)
    else:
        return flask.jsonify({"success": False, "message": "Unsupported file format"}), 400
    

    processed_data = df.to_dict()

    # breakpoint()
    return chatbot_handle_excel_file(processed_data, prompt)

    
def chatbot_handle_excel_file(data, prompt):
    return