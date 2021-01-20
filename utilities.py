import os


def file_path_exists(path: str):
    return os.path.exists(path)


def clean_string(string: str):
    return string.strip().replace('\\', '/')


def play_song(file_path: str):
    if file_path and file_path_exists(file_path):
        os.startfile(file_path)


def is_empty(itemList: list):
    return len(itemList) == 0
