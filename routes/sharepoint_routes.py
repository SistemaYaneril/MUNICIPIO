from flask import Blueprint

sharepoint_routes = Blueprint('sharepoint_routes', __name__)

@sharepoint_routes.route("/upload", methods=['POST'])
def upload_file():
    return "uploading_pdf"