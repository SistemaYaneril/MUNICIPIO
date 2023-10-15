import io
from flask import request, jsonify, send_file
from PyPDF4 import PdfFileMerger

def merge_pdf():
    try:
        pdf_merger = PdfFileMerger()

        if 'pdfs' not in request.files:
            return jsonify({"status": False, "message": "No se enviaron archivos PDF"}), 400

        pdf_files = request.files.getlist('pdfs')
        pdf_name = request.form.get('name_pdf', 'merged_1.pdf')

        for pdf_file in pdf_files:
            if pdf_file.filename != '':
                pdf_merger.append(pdf_file)

        output_pdf = io.BytesIO()
        pdf_merger.write(output_pdf)
        pdf_merger.close()

        output_pdf.seek(0)

        return send_file(output_pdf, as_attachment=True, download_name=pdf_name, mimetype='application/pdf')
    except Exception as e:
            return jsonify({"error": str(e)}), 500