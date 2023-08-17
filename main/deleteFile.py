from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import speech

def delete_file(bucket_name, file_name):
    client_file = r'C:\\tr_2\\main\\new.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = storage.Client(credentials=credentials)

    bucket = client.bucket(bucket_name)

    file_blob = bucket.blob(file_name)

    file_blob.delete()

    print(f"File {file_name} deleted from bucket {bucket_name}.")
