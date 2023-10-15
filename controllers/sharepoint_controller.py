import requests
import os
from flask import jsonify, request
from requests_ntlm import HttpNtlmAuth

def authentication(dominio_usuario, contrasena):
    try:
        result_loggin = HttpNtlmAuth(dominio_usuario, contrasena)

        return { "status": True, "message": result_loggin}
    except:
        return { "status": False, "message": "Usuario - contraseña incorrecto"}
    
def authentication_sites(auth, url_domain):
    try:
        url_ctx = f"{url_domain}/_api/contextinfo"

        headers_session = {
            'Accept': 'application/json;odata=verbose',
        }

        response = requests.post(url_ctx, headers=headers_session, auth=auth)

        digest_value = response.json().get('d').get('GetContextWebInformation').get('FormDigestValue')

        return { "status": True, "message": digest_value}
    except:
        return { "status": False, "message": f"Sitio '{url_domain}' no disponible"}

def upload_file_site(auth, value, url_site, url_file, file_name, librery):
    try:
        upload_url = f"{url_site}/_api/web/GetFolderByServerRelativeUrl('{librery}')/Files/add(url='{file_name}',overwrite=true)"
        
        headers_file = {
            'Accept': 'application/json;odata=verbose',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-RequestDigest': value
        }
        
        response_file = requests.get(url_file); 

        with open(file_name, "wb") as f:
                f.write(response_file.content)

        with open(file_name, 'rb') as file:
            files = {'file':  file}
            response = requests.post(upload_url, headers=headers_file, files=files, auth=auth)

        if os.path.exists(file_name):
            os.remove(file_name)

        if response.status_code in [200, 201]:
            
            file_link = response.json()['d']['ServerRelativeUrl']

            return {'status': True, 'message': file_link}
                
        return {'status': False, 'message': 'Archivo no se pudo ser subido'}
    except:        
        return { "status": False, "message": f"Error al subir archivo"}
    
def add_metadata(auth, value, metadata, library, url_site, repository):
    try:
        update_url = f"{url_site}/_api/web/GetFileByServerRelativeUrl('{repository}')/ListItemAllFields"
        
        headers = {
            'Accept': 'application/json;odata=verbose',
            'Content-Type': 'application/json;odata=verbose',
            'X-RequestDigest': value,
            'X-HTTP-Method': 'MERGE',
            'IF-MATCH': '*',
            "prefer": "return=representation"
        }

        data = {
            '__metadata': {'type': f"SP.Data.{library}Item"}
        }

        data.update(metadata)

        response = requests.post(update_url, headers=headers, json=data, auth=auth)
        
        if response.status_code in [204, 200, 201]:
            return {'status': True, 'message': 'Metadata adjuntado con éxito'}
                
        return {'status': False, 'message': 'Error al adjuntar metadata'}

    except:
        return { "status": False, "message": f"Error al adjuntar metadata"}