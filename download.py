import os
import sys
import drivetool.downloadrelated as download
import drivetool.authen as authen
import list as li

def count(args,service):

    file_count = 0
    for file_id in args.source:
        file_count += 1
        file_id = li.retrieve_id_from_url(file_id)
        file = download.get_file_data(file_id,service)
        file_name = file[0]
        file_mimetype = file[1]
        list_count = 0
        if file_mimetype == "application/vnd.google-apps.folder":
            value = li.list_by_folderid(file_id)
            list_count = len(value)
            file_count+=list_count
            #print(list_count)
        if '.DS_Store' in file_name:
            file_count -=1
    
    return file_count

def downloader(args):

    print("downloading......")

    if args.cover:
        cover_flag = True
    else:
        cover_flag = False
    
    ignore_flag = True
    
    cred_file = None
    service = authen.get_gdrive_service(cred_file)

    location = args.destination
    #check location is pending
    if not os.path.exists(location) or not os.path.isdir(location):
        print("//error: destination [{}] refers to incorrect path,".format(location),"please input correct one")
        print("download failed, please try again")
        sys.exit()
    
    file_count = count(args,service)
    download.inititial_total(file_count)
    print("Number of files: {}".format(file_count))

    for file_id in args.source:

        if 'folders' in file_id:
            temp = file_id.split('/')
            index = temp.index('folders')
            file_id = temp[index+1]
            if '?usp=sharing' in file_id:
                file_id = file_id.replace('?usp=sharing', '')

        elif 'file' in file_id:
            temp = file_id.split('/')
            index = temp.index('d')
            file_id = temp[index+1]
            if '?usp=sharing' in file_id:
                file_id = file_id.replace('?usp=sharing', '')
        
        filedata = download.get_file_data(file_id,service)
    
        file_name = filedata[0]
        file_mimetype = filedata[1]

        download.initialize_ignore_flag(ignore_flag)
        download.initialize_cover_flag(cover_flag)

        if file_mimetype == "application/vnd.google-apps.folder":
            download.download_folder_by_id(file_id,file_name,location,service)
        else:
            download.download_file_by_id(file_id,file_name,location,service)
    
    print("download completed")
