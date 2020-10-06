#This is deprecated use the Azure CLI 
#Blobstorage creation in Azure
#For use in conjuction with Azure DevLa
#Jeff Schmitz 2020

from azure.storage.blob import BlobService
from os import listdir
from os.path import isfile, join

# Set parameters here
ACCOUNT_NAME = "<your_account_name>"
ACCOUNT_KEY = "<your_account_key>"
CONTAINER_NAME = "<your_container_name>"
LOCAL_DIRECT = "<your_local_directory>"        

blob_service = BlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
# find all files in the LOCAL_DIRECT (excluding directory)
local_file_list = [f for f in listdir(LOCAL_DIRECT) if isfile(join(LOCAL_DIRECT, f))]

file_num = len(local_file_list)
for i in range(file_num):
    local_file = join(LOCAL_DIRECT, local_file_list[i])
    blob_name = local_file_list[i]
    try:
        blob_service.put_block_blob_from_path(CONTAINER_NAME, blob_name, local_file)
    except:
        print "something wrong happened when uploading the data %s"%blob_name
