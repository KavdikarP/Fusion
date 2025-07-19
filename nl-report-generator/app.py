from flask import Flask, request, jsonify
import os
from vertex_ai_utils import generate_sql_from_nl
from db_utils import run_sql_and_fetch
from report_generator import generate_excel, generate_pdf, generate_ppt
from google.cloud import storage

app = Flask(__name__)

def upload_to_gcs(file_path, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    return blob.public_url

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    nl_query = data.get('query')
    output_format = data.get('format', 'excel').lower()

    sql_query = generate_sql_from_nl(nl_query)
    df = run_sql_and_fetch(sql_query)

    temp_file = f"/tmp/output.{output_format}"
    if output_format == 'excel':
        generate_excel(df, temp_file)
    elif output_format == 'pdf':
        generate_pdf(df, temp_file)
    elif output_format == 'ppt':
        generate_ppt(df, temp_file)
    else:
        return jsonify({'error': 'Unsupported file format'}), 400

    bucket_name = "cxo-prism"
    public_url = upload_to_gcs(temp_file, bucket_name, os.path.basename(temp_file))

    return jsonify({'file_url': public_url, 'sql_used': sql_query})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
