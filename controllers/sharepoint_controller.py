from flask import jsonify
from requests_ntlm import HttpNtlmAuth

def authentication(dominio_usuario, contrasena):
    try:
        return HttpNtlmAuth(dominio_usuario, contrasena)
    except:
        return jsonify({ "status": False, "message": "Servicio no disponible"})