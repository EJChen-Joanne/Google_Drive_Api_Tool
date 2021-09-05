import download as down
import upload as up
import drivetool.authen as au
import list as li
from argparse import ArgumentParser

# sub-command functions
def auth(args):
    au.init_auth(args)

def download(args):
    down.downloader(args)

def upload(args):
    up.uploader(args)

def list(args):
    li.list_into_json(args)

# create the top-level parser
parser = ArgumentParser()
subparsers = parser.add_subparsers()

# create the parser for the "auth" command
parser_upload = subparsers.add_parser('auth')
parser_upload.add_argument("-cred","--credentials",type=str,required=True,help="path/to/credentials.json")
parser_upload.set_defaults(func=auth)

# create the parser for the "upload" command
parser_upload = subparsers.add_parser('upload')
parser_upload.add_argument("-src","--source",required=True,type=str,help="path/to/multiple/files or directories",nargs='+')
parser_upload.add_argument("-dest","--destination",type=str,help="gdrive directory id/url as upload destination",default=None)
parser_upload.add_argument("-new","--newfolder",type=str,help="new directory name to be created onto gdrive",default=None)
parser_upload.set_defaults(func=upload)

# create the parser for the "download" command
parser_download = subparsers.add_parser('download')
parser_download.add_argument("-src","--source",type=str,required=True,help="multiple gdrive ids/urls",nargs='+')
parser_download.add_argument("-dest","--destination",type=str,required=True,help="path/to/directory as download destination")
parser_download.add_argument("-c","--cover",action="store_true",help="enable to update all existing files")
parser_download.set_defaults(func=download)

# create the parser for the "list" command
parser_list = subparsers.add_parser('list')
parser_list.add_argument("-src","--source",type=str,required=True,help="directory id/url")
parser_list.set_defaults(func=list)

# parse the args and call whatever function was selected
args = parser.parse_args()
args.func(args)