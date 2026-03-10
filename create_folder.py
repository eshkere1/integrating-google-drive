from Google import Create_Service
import argparse

CLIENT_SECRET_FILE = 'credentials.json' 
API_NAME  = 'drive' 
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


def create_folder(folder_name, service):
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')


def main():
    parser = argparse.ArgumentParser(description="Создает папку")
    parser.add_argument("-f", "--folder_name", help="Введите имя папки", required=True)
    args = parser.parse_args()
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    create_folder(args.folder_name, service)


if __name__ == "__main__":
    main()