from Google import Create_Service, MediaFileUpload, MediaIoBaseDownload
from os import walk, path
import os
import mimetypes
import io

CLIENT_SECRET_FILE = 'credentials.json' # путь до файла с данными клиента, которого создавали ранее в кратком руковдстве 
API_NAME  = 'drive' # название API системы
API_VERSION = 'v3' # версия API системы
SCOPES = ['https://www.googleapis.com/auth/drive'] # Доступ к командам и действиям

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


folder_id = '1G6fzPmxfsxwpLdSeCW0yw37R-0kFQKMw'
results = service.files().list(
    pageSize=10,
    fields="files(id, name)",
    q=f"'{folder_id}' in parents"
).execute()

existing_files = {item['name']: item['id'] for item in results.get('files', [])}

for root, dirs, files in walk('Google'):
    for filename in files:
        file_path = path.join(root, filename)
        print(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }

        if filename in existing_files:
            service.files().update(
                fileId=existing_files[filename],
                media_body=media
            ).execute()
            print(f"Обновлён: {filename}")
        else:
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"Загружен: {filename}")

print("Готово!")
for filename in existing_files:
    file_path = os.path.join("Download", filename)
    results = service.files().get_media(fileId=existing_files[filename])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, results)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    with open(file_path, "wb") as f:
        f.write(fh.read())
    print(f"Cкачан {filename}")
    permission = {
        "type": "anyone",
        "role": "reader",
    }
    service.permissions().create(fileId=existing_files[filename], body=permission).execute()
    response_share_link = service.files().get(fileId =existing_files[filename], fields='webViewLink').execute()
    print(response_share_link['webViewLink'])