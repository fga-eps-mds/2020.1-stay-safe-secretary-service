"""
Utils functions to create and remove folders and files at system.
"""
import os


def __get_folder_path(folder_name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, folder_name)
    return path


def create_folder(folder_name):
    """
    Create a folder to save the excel files.
    """
    path = __get_folder_path(folder_name)

    os.mkdir(path)


def delete_folder(folder_name):
    """
    Delete a folder after using all the files.
    """
    path = __get_folder_path(folder_name)

    os.rmdir(path)


def delete_file(directory, filename):
    """
    Delete the excel files after extracting the datas.
    """
    parent_dir = os.getcwd()
    location = os.path.join(parent_dir, directory)
    path = os.path.join(location, filename)

    os.remove(path)
