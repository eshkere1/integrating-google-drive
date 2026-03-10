from Google import Create_Service
import argparse

CLIENT_SECRET_FILE = 'credentials.json' 
API_NAME  = 'drive' 
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    parser = argparse.ArgumentParser(description="устанавливает файлы")
    parser.add_argument("-f", "--folder_id", help="Введите айди папки", type=str, default="1G6fzPmxfsxwpLdSeCW0yw37R-0kFQKMw")
    args = parser.parse_args()
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    results = service.files().list(
        pageSize=10,
        fields="files(id, name)",
        q=f"'{args.folder_id}' in parents"
    ).execute()
    existing_files = {item['name']: item['id'] for item in results.get('files', [])}
    for filename in existing_files:
        permission = {
            "type": "anyone",
            "role": "reader",
        }
        service.permissions().create(fileId=existing_files[filename], body=permission).execute()
        response_share_link = service.files().get(fileId =existing_files[filename], fields='webViewLink').execute()
        print(response_share_link['webViewLink'])


if __name__=="__main__":
    main()