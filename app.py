import os
from flask import Flask
from routes.tools_routes import tools_routes
from routes.sharepoint_routes import sharepoint_routes

app = Flask(__name__)

app.register_blueprint(tools_routes, url_prefix="/v1/api/tools")
app.register_blueprint(sharepoint_routes, url_prefix="/v1/api/sharepoint")

valor_variable = os.environ.get('debug') or True

if __name__ == '__main__':
    app.run(debug=valor_variable, host="0.0.0.0")