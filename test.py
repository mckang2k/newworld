import os


def print_files_in_current_directory():
    for name in sorted(os.listdir('.')):
        if os.path.isfile(name):
            print(name)


print_files_in_current_directory()
