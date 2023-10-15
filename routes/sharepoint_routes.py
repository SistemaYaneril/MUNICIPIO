
import re
from urllib.parse import unquote
from flask import Blueprint, request, jsonify
from controllers.sharepoint_controller import authentication, authentication_sites, upload_file_site, add_metadata

sharepoint_routes = Blueprint('sharepoint_routes', __name__)

@sharepoint_routes.route("/upload", methods=['POST'])
def upload_file():
    json_data = request.json

    if not json_data or 'dominio' not in json_data:
        return jsonify({"status": False, "message": "La propiedad 'dominio' es requerida"}), 400

    if not json_data or 'usuario' not in json_data:
        return jsonify({"status": False, "message": "La propiedad 'usuario' es requerida"}), 400

    if not json_data or 'contrasena' not in json_data:
        return jsonify({"status": False, "message": "La propiedad 'contrasena' es requerida"}), 400

    if not json_data or 'url_domain' not in json_data:
        return jsonify({"status": False, "message": "La propiedad 'url_domain' es requerida"}), 400

    if not json_data or 'metadata' not in json_data:
        return jsonify({"status": False, "message": "La propiedad 'metadata' es requerida"}), 400

    if not json_data or 'url_documents' not in json_data:
        return jsonify({"status": False, "message": "La propiedad 'url_documents' es requerida"}), 400
    
    dominio = request.json['dominio']
    usuario = request.json['usuario']
    contrasena = request.json['contrasena']
    url_domain = request.json["url_domain"]
    metadata = request.json['metadata']
    name_file = request.json['name_file']
    url_file = unquote(request.json['url_documents'])

    dominio_usuario = dominio+"\\"+usuario
    
    url_decodificado = unquote(url_domain)

    ubicacion = url_decodificado.split("?")

    resultado = re.search(r'RootFolder=([^&]+)', ubicacion[1])
  
    lista = resultado.group(1).split("/")

    lista_filtrada = [elemento for elemento in lista if elemento]

    biblioteca = f"{lista_filtrada[-2]}"

    resultado = re.search(r"(http://[^/]+/sites/[^/]+)", ubicacion[0])

    url_domain = resultado.group(1)
    
    auth = authentication(dominio_usuario, contrasena)

    if auth['status'] == False:
        return jsonify(auth)

    digest_value = authentication_sites(auth['message'], url_domain)

    if digest_value['status'] == False:
        return jsonify(digest_value)

    result_uploading = upload_file_site(auth['message'], digest_value['message'], url_domain, url_file, name_file, f"{lista_filtrada[-2]}/{lista_filtrada[-1]}")

    if result_uploading['status'] == False:
        return jsonify(result_uploading)
    
    return jsonify(add_metadata(auth['message'], digest_value['message'], metadata, biblioteca, url_domain, result_uploading['message']))