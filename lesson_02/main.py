from flask import Flask, request, jsonify
from job_1 import fetch_sales_data
app = Flask(__name__)

@app.route('/', methods=['POST'])
def extract_sales_data():

    # Get data from request
    data = request.get_json()
    raw_dir = data.get('raw_dir')

    try:
        fetch_sales_data(raw_dir)
        return jsonify({"message": "Sales data extracted successfully!"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8081)  # For get
    app.run(port=8082)  # For convert