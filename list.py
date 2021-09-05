import sys
import drivetool.authen as au
import json
import progress_bar as progress

dict = []

def retrieve_id_from_url(id):
    if 'folders' in id:
        temp = id.split('/')
        index = temp.index('folders')
        id = temp[index+1]
        if '?usp=sharing' in id:
            id = id.replace('?usp=sharing', '')
    elif 'file' in id:
        temp = id.split('/')
        index = temp.index('d')
        id = temp[index+1]
        if '?usp=sharing' in id:
            id = id.replace('?usp=sharing', '')
    
    return id


def list_by_folderid(folder_id):
    """Get listing data
    """
    #dict = []
    cred_file = None
    service = au.get_gdrive_service(cred_file)
    if 'folders' in folder_id:
        folder_id = retrieve_id_from_url(folder_id)

    page_token = None
    
    while True:
        try:
            response = service.files().list(q= "trashed = false and '{}' in parents".format(folder_id),
                                            fields="nextPageToken, files(id, name, mimeType)",
                                            pageToken=page_token,
                                            pageSize = 1000).execute()
        except:
            print("//error: this is incorrect source [{}]".format(folder_id))
            print("list failed, please try again")
            sys.exit()

        for file in response.get("files", []):
            value = [
                {\
                'name':file['name'],\
                'id':file['id'],\
                'mimeType':file['mimeType'],\
                }
            ]
            dict.append(value)
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                list_by_folderid(file['id'])
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    
    return dict

def print_json():
    fileadd = 'list.json'
    with open(fileadd,'r') as jsonfile:
        parsed = json.load(jsonfile)
    print(json.dumps(parsed,indent=4))

    print('List could be also viewed on list.json')

def list_into_json(args):
    """Put listing data into list.json
    """
    folder_id = args.source
    total_data = list_by_folderid(folder_id)
    name = "Listing"

    with open('list.json','w+',encoding='utf-8') as file:
        file.write(json.dumps(total_data,ensure_ascii=False,indent=4))
        progress.show_progress(name,1)
    
    #print("Done, please check in list.json")
    print_json()