from __future__ import print_function
from googleapiclient.http import MediaIoBaseDownload
from apiclient import errors
import io
import os
import sys
import shutil
from tqdm import tqdm
import progress_bar as progress

##不要下載某資料夾下之控制
ignore_flag = True
##覆蓋原資料夾時
cover_flag = False

total_count = 0

def inititial_total(count):
    global total_count
    total_count = count

def initialize_ignore_flag(i_flag: bool):
    """Let ignore_flag formatted as True
    """
    global ignore_flag
    ignore_flag = i_flag

def initialize_cover_flag(c_flag: bool):
    """Let cover_flag formatted as user's choice (True: cover all / False: do not cover)
    """
    global cover_flag
    cover_flag = c_flag

def download_file_by_id(file_id: str,file_name: str,location: str,service):
    """Download a file through the given id
    """
    global ignore_flag,cover_flag

    if ignore_flag == False:
        return
    
    if '.DS_Store' in file_name:
        return

    if cover_flag == False:#should ask#
        #asking query##cover_flag is False
        if os.path.isfile(str(location+'/'+file_name)):
        #if there is a file with the same name in the path
            choice = int(input("{} 的同名檔案已存在, 請輸入 1=兩者皆保留 ; 2=覆蓋 ; 3=不要下載\n".format(file_name)))
            if choice==1:
                temp_name = file_name
                temp_filename = temp_name.split('.')[0]
                temp_type = temp_name.split('.')[-1]
                temp_num = 1
                file_name = str(temp_filename+'('+str(temp_num)+')'+'.'+temp_type)
                while os.path.isfile(str(location+'/'+file_name)):
                    temp_num+=1
                    file_name = str(temp_filename+'('+str(temp_num)+')'+'.'+temp_type)
            elif choice == 2:
                file_name = file_name
            else:
                return

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(str(location+"/"+file_name), 'wb')
    downloader = MediaIoBaseDownload(fh, request,1024*1024)
    done = False
    ####
    last_update = 0
    now_count = progress.number_count()
    pbar = tqdm(total=100,leave=True,unit='Bytes',desc="({}/{}) {}".format(now_count,total_count,file_name))
    
    while done is False:
        try:
            status,done = downloader.next_chunk()
            if status:
                pg = status.progress() * 100
                updatepg = pg - last_update
                pbar.update(updatepg)
                last_update = pg
            else:
                pbar.update(100)
        except:
            fh.close()
            os.remove(str(location+"/"+file_name))
            print("Download failed at [{}], please try again".format(file_name))
            sys.exit(1)
        sys.stdout.flush()
    pbar.close()
    ###

def download_folder_by_id(folder_id: str, folder_name: str,location: str,service):
    """Download a folder through the given id
    """

    global ignore_flag,cover_flag,total_count

    if ignore_flag == False:
        return

    if not os.path.exists(str(location+"/"+folder_name)):
        os.makedirs(str(location+"/"+folder_name))
    else:
        if cover_flag == False:#should ask
            choice = int(input("{} 的同名資料夾已存在, 請輸入 1=兩者皆保留 ; 2=覆蓋 ; 3=不要下載\n".format(folder_name)))
            if choice == 1:
                temp_num = 1
                temp_foldername = folder_name
                folder_name = str(temp_foldername+'('+str(temp_num)+')')
                while os.path.isdir(str(location+'/'+folder_name)):
                    temp_num+=1
                    folder_name = str(temp_foldername+'('+str(temp_num)+')')
            
                os.makedirs(str(location+"/"+folder_name))
            elif choice ==2:
                folder_name = folder_name
                shutil.rmtree(str(location+"/"+folder_name))
                os.makedirs(str(location+"/"+folder_name))
                cover_flag = True
            else:
                ignore_flag = False
        else:#cover all
            shutil.rmtree(str(location+"/"+folder_name))
            os.makedirs(str(location+"/"+folder_name))
    
    location = str(location+"/"+folder_name)
    if not ignore_flag is False:
        progress.show_progress(folder_name,total_count)

    result = []
    page_token = None
    while True:
        files = service.files().list(
                q="trashed = false and '{}' in parents".format(folder_id),
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
                pageSize=1000).execute()
        result.extend(files['files'])
        page_token = files.get("nextPageToken")
        if not page_token:
            break

    result = sorted(result, key=lambda k: k['name'])
    ##print(len(result))

    for single_file in result:
        file_id = single_file['id']
        file_name = single_file['name']
        mime_type = single_file['mimeType']
        if mime_type == 'application/vnd.google-apps.folder':
            download_folder_by_id(file_id,file_name,location,service)
        else:
            download_file_by_id(file_id,file_name,location,service)


def get_file_data(fileid: str,service):
    """Retrieve file metadata through the given id
    """
    result = []
    try:
        file = service.files().get(fileId=fileid).execute()
        result.append(file['name'])
        result.append(file['mimeType'])
        return result
    except errors.HttpError as error:
        #print("error: %s" % error)
        print("//error: cannot find ID [{}],".format(fileid),"please input correct one")
        print("download failed, please try again")
        sys.exit()