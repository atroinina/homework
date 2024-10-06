import os
import json
import fastavro
from fastavro.schema import load_schema
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from util import clear_directory
app = Flask(__name__)

def convert_json_to_avro(raw_dir: str, stg_dir: str) -> None:
    """
    Converts JSON files from the raw directory to Avro format
    and saves them to the staging directory.

    Parameters:
    raw_dir (str): The directory containing JSON files.
    stg_dir (str): The directory where Avro files will be saved.
    """
    today = '2022-08-09'
    stg_sales_dir = os.path.join(stg_dir, 'sales', today)

    # Make directory to save a file and ensure it's clean
    os.makedirs(stg_sales_dir, exist_ok=True)
    clear_directory(stg_sales_dir)

    schema = load_schema('sales_schema.avsc')  # Define Avro schema

    for json_file_name in os.listdir(raw_dir):
        if json_file_name.endswith('.json'):
            json_file_path = os.path.join(raw_dir, json_file_name)

            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            avro_file_name = json_file_name.replace('.json', '.avro')
            avro_file_path = os.path.join(stg_sales_dir, avro_file_name)

            # Convert to Avro and save
            with open(avro_file_path, 'wb') as avro_file:
                fastavro.writer(avro_file, schema, data)

            print(f"Converted {json_file_name} to Avro and saved to {avro_file_path}")


@app.route('/convert', methods=['POST'])
def handle_convert_request():
    """
    Endpoint to handle the conversion job.

    This function takes a POST request with two parameters: raw_dir and stg_dir,
    reads the JSON files from raw_dir, converts them to Avro, and saves them in stg_dir.
    """
    req_data = request.get_json()

    raw_dir = req_data.get('raw_dir')
    stg_dir = req_data.get('stg_dir')

    if not raw_dir or not stg_dir:
        return jsonify({'error': 'Both raw_dir and stg_dir are required.'}), 400

    convert_json_to_avro(raw_dir, stg_dir)

    return jsonify({'message': 'JSON files successfully converted to Avro.'}), 200


if __name__ == "__main__":
    app.run(host='localhost', port=8082)
