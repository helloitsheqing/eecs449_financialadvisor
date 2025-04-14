from flask import Blueprint
import pandas
import flask
from io import BytesIO
from chatbot import get_chatbot_response
import os
import json
from werkzeug.utils import secure_filename
import openpyxl
import xlrd

# hey everyone

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
    

    processed_data = json.dumps(df.to_dict())

    # breakpoint()
    data = chatbot_handle_excel_file(processed_data, prompt)
    return flask.jsonify({"response": "Success", "data": data}), 200


SPREADSHEET_PROMPT = """OK, so you are about to receive a spreadsheet that was translated to a
                        JSON dictionary as well as prompt that was given by the user, indicating why they
                        gave you this spreadsheet and what they want you to do with it. Your job is to follow
                        the user's instructions and produce a (potentially) updated spreadsheet or provide feedback on it.
                        So basically you have to do one of two things: either edit the spreadsheet data in the JSON as you
                        see fit or just give feedback on it. If you decide to change the JSON data, make sure to return a JSON string with two 
                        keys: one being 'data' and the value is a JSON string of the new spredsheet, and the other being 'response' with the 
                        value being whatever feedback/information you want to give the user. If you decide to just give feedback on it 
                        for whatever reason, indicate it to use using the string 'FEEDBACK' followed by your actual feedback. This way,
                        we will know that you only decided to provide feedback on it and we can handle it differently. 
                        Here is the user prompt, followed by the jsonified data:\n
                    """

    
def chatbot_handle_excel_file(data, prompt):
    prompt = SPREADSHEET_PROMPT + prompt + "\nData:\n" + data
    response = get_chatbot_response(prompt, 0)

    if "FEEDBACK" in response:
        response = response.replace("FEEDBACK", "")
        if response.startswith(":"):
            response = response.replace(":", "")
        return response
    
    # breakpoint()

    # response should be a stringified json
    response = json.loads(response)

    return response

# these returns may (probably will be) flawed af but fuck it we ball for now