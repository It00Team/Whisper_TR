from google.cloud import storage
from google.oauth2 import service_account
from django.core.files.storage import default_storage
from google.cloud import speech


def upload_file_to_bucket(bucket_name: str, local_file_path: str, destination_blob_name: str) -> None:
   
    client_file =r'C:\\tr_2\\main\\new.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = storage.Client(credentials=credentials)

    bucket = client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    print(f"File uploaded to {bucket_name}/{destination_blob_name} successfully.")


# def upload_file_to_bucket(bucket_name: str, uploaded_file, destination_blob_name: str) -> None:
#     # Get the local file path where the uploaded file is temporarily stored
#     local_file_path = default_storage.save(uploaded_file.name, uploaded_file)

#     client_file = r'C:\Users\Admin\Downloads\Transcription_tool\project\main\khushi.json'
#     credentials = service_account.Credentials.from_service_account_file(client_file)
#     client = storage.Client(credentials=credentials)

#     bucket = client.bucket(bucket_name)

#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_filename(local_file_path)

#     # Delete the temporarily stored file
#     default_storage.delete(local_file_path)

#     print(f"File {uploaded_file.name} uploaded to {bucket_name}/{destination_blob_name} successfully.")


    # print(f"File {local_file_path} uploaded to {bucket_name}/{destination_blob_name} successfully.")
