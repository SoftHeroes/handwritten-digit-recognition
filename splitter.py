import os
import shutil
import zipfile

# Source and destination directories
dataset_dir = 'dataset'
source_dir = dataset_dir + '/' + 'train-set'
destination_dir = dataset_dir + '/' + 'test-set'

if os.path.exists(dataset_dir):
    shutil.rmtree(dataset_dir)

with zipfile.ZipFile('archive.zip', 'r') as zip_ref:
    zip_ref.extractall('')

# Ensure both directories exist
if not os.path.exists(source_dir):
    print("Source directory does not exist.Creating now... with moving all digit subdirectories into it")
    os.mkdir(source_dir)

    # Looping through all digits in the source directory
    for i in range(0, 10):
        shutil.move(dataset_dir+'/'+str(i)+'/'+str(i), source_dir+'/'+str(i))
        os.rmdir(dataset_dir+'/'+str(i))

if not os.path.exists(destination_dir):
    print("Destination directory does not exist. Creating now... with all digit subdirectories")
    os.mkdir(destination_dir)
    # Looping through all digits in the source directory
    for i in range(0, 10):
        os.mkdir(destination_dir+'/'+str(i))

# Looping through all digits in the source directory
for i in range(0,10):
    # Get list of files in source directory
    files = os.listdir(source_dir+'/'+str(i))

    # Iterate through files and move those with names greater than '8000.png'
    for file in files:
        if file.endswith('.png') and int(file.split('.')[0]) > 8000:
            source_file_path = os.path.join(source_dir+ "/" + str(i), file)
            destination_file_path = os.path.join(destination_dir+ "/" + str(i), file)
            # Move file
            shutil.move(source_file_path, destination_file_path)
            print(f"Moved {file} to {destination_dir}")
