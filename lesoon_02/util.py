import os
from dotenv import load_dotenv

# Load secret authorization key
def get_authorization_key() -> str:
    """
    Get authorization key from environment variables.
    :return: authorization key
    """
    load_dotenv()

    AUTH_TOKEN = os.getenv('AUTH_TOKEN')

    if not AUTH_TOKEN:
        raise EnvironmentError("AUTH_TOKEN is not set")
    return AUTH_TOKEN


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
