from __future__ import print_function
import os
from googleapiclient.http import MediaFileUpload
import progress_bar as progress
from tqdm import tqdm
from time import sleep

total_count = 0
def initialize_number(num):
    global total_count
    total_count = num

def create_folder(folder_name: str,service):
    """Create a new folder into MyDrive
    """
    folder_metadata = {
        "name" : folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    file = service.files().create(body=folder_metadata, fields="id").execute()
    ##
    progress.show_progress(folder_name,total_count)
    return file.get("id")


def create_file(file_name: str,service):
    """Upload a file into MyDrive
    """
    if not '.DS_Store' in file_name:
        file_uplname=os.path.basename(file_name)
        file_metadata = {
            "name": file_uplname
        }
        media = MediaFileUpload(file_name,
                                mimetype='application/octet-stream',
                                chunksize=1024 * 1024,
                                resumable=True)
        request = service.files().create(body=file_metadata, media_body=media, fields="id") #.execute()
        ####
        response = None
        last_update = 0
        now_count = progress.number_count()
        pbar = tqdm(total=100,unit='Bytes',leave=True,desc="({}/{}) {}".format(now_count,total_count,file_uplname),
                    #maxinterval=10,mininterval=0.01,ncols=80,smoothing=0.1,
                    #bar_format='{l_bar}|{bar}|{n_fmt}/{total_fmt}[{rate_fmt}]'
                    )
        while response is None:
            status,response = request.next_chunk()
            if status:
                pg = status.progress() * 100
                updatepg = pg - last_update
                pbar.update(updatepg)
                last_update = pg
            else:
                pbar.update(100)
        pbar.close()
        ####

def create_folder_in_another_folder(folder_name: str,parent_id: str,service):
    """Create a new folder into a specific folder by giving a folder id
    """
    folder_metadata = {
        "name" : folder_name,
        "parents" : [parent_id],
        "mimeType" : "application/vnd.google-apps.folder"
    }
    file = service.files().create(body=folder_metadata, fields="id").execute()
    progress.show_progress(folder_name,total_count)
    return file.get("id")

def create_file_in_folder(file_name: str,file_path: str,parent_id: str,service):
    """Upload a file into a specific folder by giving folder id
    """
    if not '.DS_Store' in file_name:
        file_uplname=os.path.basename(file_name)
        file_metadata = {
            "name": file_uplname,
            "parents": [parent_id]
        }
        media = MediaFileUpload(file_path,
                                mimetype='application/octet-stream',
                                chunksize= 1024 * 1024,
                                resumable=True)
        request = service.files().create(body=file_metadata, media_body=media, fields="id") #.execute()

        ####
        response = None
        last_update = 0
        now_count = progress.number_count()
        pbar = tqdm(total=100,unit='Bytes',leave=True,desc="({}/{}) {}".format(now_count,total_count,file_uplname))
        while response is None:
            status,response = request.next_chunk()
            if status:
                pg = status.progress() * 100
                updatepg = pg - last_update
                pbar.update(updatepg)
                last_update = pg
            else:
                pbar.update(100)
        pbar.close()
        ####

def upload_all_files(local_folder_path: str,parent_id: str,service):
    """Upload all files in the given directory
    """

    for root,d_names,f_names in os.walk(local_folder_path):
        for single_file in f_names:
            file_path = os.path.join(root,single_file)
            create_file_in_folder(single_file,file_path,parent_id,service)
        break

def recursive_upload(local_folder_path: str,parent_id: str,service):
    """Recursively upload all files in the given directory
    """
    upload_all_files(local_folder_path,parent_id,service)
    
    id_list = {} #key=directory's name value=direcotry's name
    for root,d_names,f_names in os.walk(local_folder_path):
        for dirs in d_names:
            dir_id = create_folder_in_another_folder(dirs,parent_id,service)
            id_list[dirs] = dir_id
        break
    for key,value in id_list.items():
        new_path = os.path.join(local_folder_path,key)
        recursive_upload(new_path,value,service)

def directory_upload_main(local_folder_path: str,service):
    """Upload a whole directory into MyDrive
    """
    root_name = local_folder_path.split('/')[-1]
    root_id = create_folder(root_name,service) #root folder id
    recursive_upload(local_folder_path,root_id,service)

def directory_upload_to_folder(local_folder_path: str,folder_id: str,service):
    """Upload a whole directory into the given destination id
    """
    root_name = local_folder_path.split('/')[-1]
    root_id = create_folder_in_another_folder(root_name,folder_id,service)
    recursive_upload(local_folder_path,root_id,service)
