from Google import Create_Service, MediaFileUpload
from os import walk, path
import mimetypes
import argparse



CLIENT_SECRET_FILE = 'credentials.json' # путь до файла с данными клиента, которого создавали ранее в кратком руковдстве 
API_NAME  = 'drive' # название API системы
API_VERSION = 'v3' # версия API системы
SCOPES = ['https://www.googleapis.com/auth/drive'] # Доступ к командам и действиям




def main():
    parser = argparse.ArgumentParser(description="загружает файлы в из папки Google")
    parser.add_argument("-f", "--folder_id", help="Введите айди папки", required=True)
    args = parser.parse_args()
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    #folder_id = '1G6fzPmxfsxwpLdSeCW0yw37R-0kFQKMw'
    results = service.files().list(
        pageSize=10,
        fields="files(id, name)",
        q=f"'{args.folder_id}' in parents"
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
                'parents': [args.folder_id]
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


if __name__=="__main__":
    main()