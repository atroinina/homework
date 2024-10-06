"""
Module for fetching and saving sales data from an API.

This module is responsible for:
1. Loading sales data from a specified API
    using a secret authorization token.
2. Saving the fetched data to a raw directory in JSON format, ensuring
   the files are structured within subdirectories based on date.
3. Ensuring idempotence by clearing the target directory
   before saving new files.
4. Handling multiple pages of data from the API
   and saving them into separate files.

Functions:
- clear_directory(path): Removes all files from the specified directory
  to ensure idempotent behavior.
- fetch_sales_data(raw_dir): Fetches sales data from the API and saves it
  in JSON format within a date-specific directory.

The main entry point sets the raw directory for saving sales data
and initiates the process of fetching the data from the API.

Environment Variables:
- AUTH_TOKEN: API token for authorization.
  Must be set in an environment variable.

Usage:
- Run the script to fetch and store sales data from the API.
- Ensure the 'AUTH_TOKEN' environment variable is set before execution.
"""

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
def clear_directory(path:str) -> None:
    """
    Remove all files from the specified directory.

    This function ensures idempotence by clearing the contents
    of the given directory before new data is saved.

    Parameters:
    path (str): The path of the directory to be cleared.
    """
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Load data from API
def fetch_sales_data(raw_dir:str) -> None:
    """Fetch sales data from an API.

    The function retrieves data from the API, clears the raw directory,
    and saves each page of the response as a JSON file. If the API returns a
    404 response, it indicates the end of the available data.

    Parameters:
    raw_dir (str): The root directory where the sales data will be saved.

    Raises:
    Exception: If there is an error while fetching data from the API.
    EnvironmentError: If the 'AUTH_TOKEN' environment variable is not set.
    """
    headers = {'Authorization': AUTH_TOKEN}
    url = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'
    current_page = 1
    while True:
        response = requests.get(
            url,
            headers=headers,
            params={'date': '2022-08-09', 'page': current_page}
        )

        if response.status_code == 404:
            response = requests.get(
                url,
                headers=headers,
                params={'date': '2022-08-09', 'page': current_page-1}
            )
            if response.status_code != 404:
                print("The end of a file reached.")
                break

        if response.status_code != 200 and response.status_code != 404:
            raise Exception(f"Error fetching data: {response.status_code}.")

        data = response.json()

        # Format data for the filepath
        today = '2022-08-09'
        sales_dir = os.path.join(raw_dir, 'sales', today)

        # Make directory to save a file and make sure that it is empty
        os.makedirs(sales_dir, exist_ok=True)
        clear_directory(sales_dir)

        # Give a name to a file
        file_name = f"sales-{today}_{current_page}.json"
        file_path = os.path.join(sales_dir, file_name)

        # Save the file as JSON
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        current_page += 1  # Increment page counter
        print(f"Sales data saved to {file_path}")


if __name__ == "__main__":
    # Define path to raw directory
    raw_dir = '/path/to/my_dir/raw'
    os.makedirs(raw_dir, exist_ok=True)
    fetch_sales_data(raw_dir)
