import urllib.request
import os
import zipfile
from tools import download_progress
from tools import zip_extract_perc
from flattener import go

zip_file="ipl_json.zip"

def zip_extract(extracted_size,url,retries,zip_file):
    if retries > 3:
        print("Exceeded maximum number of retries.")
        return

    try:
        # Extract the JSON files from the downloaded zip file
        with zipfile.ZipFile(os.path.join(os.getcwd(), zip_file), "r") as zip_ref:

            total_size = sum(file_info.file_size for file_info in zip_ref.infolist())

            for file_info in zip_ref.infolist():
                extracted_size += int(file_info.file_size)
                zip_extract_perc(zip_file,extracted_size, total_size)    
                zip_ref.extract(file_info.filename, all_json_directory)

    except zipfile.BadZipFile:

        urllib.request.urlretrieve(url, os.path.join(os.getcwd(), zip_file), reporthook=download_progress)
        zip_extract(extracted_size,url,retries+1,zip_file=zip_file)       
        
    # Print a message indicating that the update has been downloaded and extracted
    print("\nALL JSON files have been extracted successfully!")    

all_json_directory = os.path.join(os.getcwd(), zip_file.split('.')[0])

try:
    os.mkdir(all_json_directory)
    print("Folder created successfully!")
except FileExistsError:
    print("Folder already exists!")
except Exception as e:
    print("An error occurred:", str(e))

url = "https://cricsheet.org/"

if os.path.exists(all_json_directory+"\""+zip_file) == True:
    print("The file "+ os.getcwd()+"\\"+zip_file+" exists in the directory.")
else:
    urllib.request.urlretrieve(url+"downloads/"+zip_file, os.path.join(os.getcwd(), zip_file), reporthook=download_progress)
    print(f"\nDownloaded  {zip_file} successfully!")

extracted_size = 0

zip_extract(extracted_size,url,retries=0,zip_file=zip_file)

go()