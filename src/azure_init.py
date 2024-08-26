import os
from dotenv import load_dotenv
from dnalib.azfile import azure_init
from dnalib.azfile import AzFile


load_dotenv()

azureml_name = os.getenv("AZUREML_NAME")
azureml_subscription_id = os.getenv("AZUREML_SUBSCRIPTION_ID")
azureml_resource_group = os.getenv("AZUREML_RESOURCE_GROUP")
contrainer_url = os.getenv("SECRET_AZURE_INPUT_SAS_URL")
working_dir = os.getenv("DSDEV_WORK_DIR")
train_data= os.getenv("AZFILE_TRAIN_INPUT_DATA")

azure_init(azure_storage_secrets={
    "dsdev": { "container_url": contrainer_url },  # SAS URL for a Container
})

azf = AzFile.from_string(train_data)
azf.download(local_dest=working_dir, )

