# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/core/06_archive.ipynb.

# %% auto 0
__all__ = ['upload_zip_to_s3']

# %% ../../nbs/core/06_archive.ipynb 4
import pubcrawler as proj
from .. import const, log, utils, tools
import adu_proj.utils as adutils

# %% ../../nbs/core/06_archive.ipynb 5
import shutil
import boto3
import os

# %% ../../nbs/core/06_archive.ipynb 7
if shutil.make_archive(f'{const.data_path}/{const.directory_name}', 'zip', f'{const.pre_output_path}'):
    print(f"All files saved to {const.data_path}/{const.directory_name}")

# %% ../../nbs/core/06_archive.ipynb 8
def upload_zip_to_s3(file_path, bucket_name, s3_file_name):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Open the file and upload to S3
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, bucket_name, s3_file_name)

# %% ../../nbs/core/06_archive.ipynb 9
if const.s3_bucket:
    upload_zip_to_s3(f"{const.data_path}/{const.directory_name}.zip", const.s3_bucket, f"{const.directory_name}.zip")
