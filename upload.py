from __future__ import print_function
import drivetool.authen as authen
import drivetool.uploadrelated as Up
import os
import sys

folderid_flag = False
folder_id = ''

def count(args):
    
    number = 0
    for path in args.source:
        if os.path.isdir(path):
            number += 1 #root
            for r,d,files in os.walk(path):
                number+=(len(d)+len(files))
                for file in files:
                    if '.DS_Store' in file:
                        number -= 1
        elif os.path.isfile(path):
            if not '.DS_Store' in path:
                number += 1
    
    if args.newfolder is not None:
        number+=1
    
    return number

def upload_file(file_path: str,dest_id: str,new_folder_name: str,service):
    
    global folderid_flag,folder_id
    #upload files into drive
    if dest_id is None and new_folder_name is None:
    #No appointed destination folder, upload to MyDrive
        Up.create_file(file_path,service)
    elif dest_id is not None and new_folder_name is None:
    #directly upload to an appointed folder by folder id
        Up.create_file_in_folder(file_path,file_path,dest_id,service)
    elif new_folder_name is not None and dest_id is None:
    #create a new folder in Mydrive and upload files
        if folderid_flag is False:
            folder_id = Up.create_folder(new_folder_name,service)
            folderid_flag = True
        Up.create_file_in_folder(file_path,file_path,folder_id,service)
    else:
    #both new_folder_name and dest_id is not None
    #create a New folder in the dest_id folder and upload files
        if folderid_flag is False:
            folder_id = Up.create_folder_in_another_folder(new_folder_name,dest_id,service)
            folderid_flag = True
        Up.create_file_in_folder(file_path,file_path,folder_id,service)

def upload_dir(filepath: str,dest_id: str,new_folder_name: str,service):
    
    global folderid_flag,folder_id
    if dest_id is None and new_folder_name is None:
    #No appointed destination folder, upload to MyDrive
        Up.directory_upload_main(filepath,service)
    elif dest_id is not None and new_folder_name is None:
    #directly upload to an appointed folder by folder id
        Up.directory_upload_to_folder(filepath,dest_id,service)
    elif new_folder_name is not None and dest_id is None:
    #create a new folder in Mydrive and upload files
        if folderid_flag is False:
            folder_id = Up.create_folder(new_folder_name,service)
            folderid_flag = True
        Up.directory_upload_to_folder(filepath,folder_id,service)
    else:
    #both new_folder_name and dest_id is not None
    #create a New folder in the dest_id folder and upload files
        if folderid_flag == False:
            folder_id = Up.create_folder_in_another_folder(new_folder_name,dest_id,service)
            folderid_flag = True
        Up.directory_upload_to_folder(filepath,folder_id,service)

def verify_id(file_id: str,service):
    try:
        file = service.files().get(fileId=file_id).execute()
        if file['mimeType'] != "application/vnd.google-apps.folder":
            return False
        return True
    except:
        return False


def uploader(args):

    print("uploading......")

    new_folder_name = args.newfolder
    dest_id = args.destination
    cred_file = None
    service = authen.get_gdrive_service(cred_file)

    if dest_id is not None and 'folders' in dest_id:
    #if為檔案夾 用檔案夾切的方式切
        temp = dest_id.split('/')
        index = temp.index('folders')
        dest_id = temp[index+1]
        if '?usp=sharing' in dest_id:
            dest_id = dest_id.replace('?usp=sharing', '')

    #check id is pending
    if dest_id is not None:
        if not verify_id(dest_id,service):
            print("//error: destination ID [{}] refers to incorrect folder,".format(dest_id),"please input correct id")
            print("upload failed, please try again")
            sys.exit()
    
    #check path are all pending
    valid_path_flag = True
    for filepath in args.source:
        if not os.path.exists(filepath):
            print("//error: cannot find [{}],".format(filepath),"please input correct format")
            valid_path_flag = False
    if valid_path_flag is False:
        print("upload failed, please try again")
        sys.exit()

    total_count = count(args)
    print("Number of files: {}".format(total_count))

    Up.initialize_number(total_count)
    for file_path in args.source:
        if os.path.isfile(file_path):
            upload_file(file_path,dest_id,new_folder_name,service)
        elif os.path.isdir(file_path):
            upload_dir(file_path,dest_id,new_folder_name,service)

    print("upload completed")