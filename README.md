# Google Drive Api Tool

***This is an usage of Google Drive Api to let you easily upload and download files***

**Cooperator:Joe Huang**

## Feature

***The following shows what this tool could fulfill......***

+ Upload:
  + Upload into MyDrive
  + Upload into a newly-created directory in MyDrive
  + Upload into an existing directory with designated id
  + Upload into a newly-created directory in an existing directory with designated id
+ Download:
  + Download files and directories into a designated local path

> *Note: Both upload and download support working with several files and directories at one time*

+ List: 
  + Display metadata of files under a designated directory and stored into `list.json`

## Instruction

### 1. Prerequisite:

+ Python 3 or above
+ pip or pip3 is installed

### 2. Create credentials:

Please follow the direction : [建立憑證](./建立Google Drive API憑證.pdf)

Visit [Google Developers Console](https://console.developers.google.com/) and apply for the credentials. 

After set up successfully, choose option to download it as JSON format and save it into your local space.

### 3. Install required modules:

Please install with the command: 

```python
$ pip install -r requirements.txt
or 
$ pip3 install -r requirements.txt
```

( Depends on your version `pip` or `pip3` )

### 4. How to use the tool:

**Typically follow the following structure to get started:**

```python
$ python -m gdrivetool [function] {[arg1] [arg2]...}
```

You can follow the direction : [使用手冊](./Google Drive Api小工具使用手冊.pdf) or read the following simple instructions.

#### (1) Authenticate / Update content of API:

For the first time, please authenticate gdrive API and a new file named `token.pickle ` will automatically be created with the following command.

```python
$ python -m gdrivetool auth -cred '{/path/to/yourcredentials.json}'
```

+ Introduction to argument:

  `-cred` [Required] : personal OAuth 2.0 credential file with format of JSON

( If you want to change different account to download or uplaod, just execute above command again. )

#### (2) Upload:

```python
$ python -m gdrivetool upload '{corresponding sets of arguments...}'
```

+ Introduction to arguments:

  + `upload` : choose upload function

    Options:
    
    1. + `-src` [Required] : full path or relative path to source file or directory to upload

       	( Input more than one path at one time is permitted and _remember to separate different path by "whitespace_" )

       + `-new` [Optional] : new folder name you wanna create into gdrive

       + `-dest` [Optional] : destination directory id/url in gdrive where you wanna upload into
    
    
		> For example:
	
		```python
		$ python -m gdrivetool upload -src '{/path/to/file}' '{/path/to/folder}' -new '{foldername}' -dest '{directoryid/url}'
		```

#### (3) Download:

```python
$ python -m gdrivetool download '{corresponding sets of arguments...}'
```

+ Introduction to arguments:

  + `download` : choose download function

    Options:

    1. + `-src`[Required] : multiple gdrive ids/urls

       *( Allowed to add more than one id or url at one time and remember to separate different ones by "whiteapce" )*

       + `-dest`[Required] : path/to/local/directory as download destination
		   + `-c` [Optional]: Update all files and folders with the same name without more request
		
		> For example:
		
		```python
		$ python -m gdrivetool download -src '{fileid}' '{directoryurl}'... -dest '{/path/to/localdirectory}' -c
		```

#### (4) List: to retrieve all metadata under the given directory id

```python
$ python -m gdrivetool list -src '{gdrive folder url/id}'
```

+ Introduction to argument:

  + `-src` : directory id/url ( input one at one time )

#### NOTE: 

+ If you execute on `zsh` with urls, to quote your url will be necessary. 
