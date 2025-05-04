import logging
import azure.functions as func
import csv
import io
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get('file')

        if not file:
            return func.HttpResponse("Aucun fichier envoyé.", status_code=400)

        content = file.stream.read().decode('cp1252')
        csv_reader = csv.DictReader(io.StringIO(content))
        data = [row for row in csv_reader]

        return func.HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=4),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.exception("Erreur lors de la conversion")
        return func.HttpResponse(f"Erreur : {str(e)}", status_code=500)
