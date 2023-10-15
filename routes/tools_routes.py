from flask import Blueprint
from controllers.tools_controller import merge_pdf

tools_routes = Blueprint('tools_routes', __name__)

@tools_routes.route("/merge", methods=["POST"])
def merge():
    return merge_pdf()