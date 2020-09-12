import os

def create_folder(folder_name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, folder_name)

    os.mkdir(path) 


def delete_folder(folder_name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, folder_name)

    os.rmdir(path)


def delete_file(directory, filename):
    parent_dir = os.getcwd()
    location = os.path.join(parent_dir, directory)
    path = os.path.join(location, filename)

    os.remove(path)