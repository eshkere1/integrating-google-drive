from Google import MediaIoBaseDownload, Create_Service
import os
import io
import argparse

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME  = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    parser = argparse.ArgumentParser(description="устанавливает файлы")
    parser.add_argument("-f", "--folder_id", help="Введите айди папки", type=str, default="1G6fzPmxfsxwpLdSeCW0yw37R-0kFQKMw")
    args = parser.parse_args()
    results = service.files().list(
        pageSize=10,
        fields="files(id, name)",
        q=f"'{args.folder_id}' in parents"
    ).execute()
    existing_files = {item['name']: item['id'] for item in results.get('files', [])}
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


if __name__=="__main__":
    main()
