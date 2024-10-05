import os
import requests
import json
from dotenv import load_dotenv

# Load secret variables
load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN')



if not AUTH_TOKEN:
    raise EnvironmentError("AUTH_TOKEN is not set")


# Clear directory for idempotence
def clear_directory(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Load data from API
def fetch_sales_data(raw_dir):
    headers={'Authorization': AUTH_TOKEN}
    url = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'

    response = requests.get(url, headers=headers, params={'date': '2022-08-09', 'page': 1})

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")

    data = response.json()

    # Format data for the filepath
    today = '2022-08-09'
    sales_dir = os.path.join(raw_dir, 'sales', today)

    # Make directory to save a file and make sure that it is empty
    os.makedirs(sales_dir, exist_ok=True)
    clear_directory(sales_dir)

    # Give a name to a file
    file_name = f"sales-{today}.json"
    file_path = os.path.join(sales_dir, file_name)

    # Save the file as JSON
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Sales data saved to {file_path}")


if __name__ == "__main__":
    # Define path to raw directory
    raw_dir = '/path/to/my_dir/raw/sales'
    os.makedirs(raw_dir, exist_ok=True)

    fetch_sales_data(raw_dir)
