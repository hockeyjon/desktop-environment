import os
import shutil

new_directory = "allFiles"
file_type = "jpg"

for root, directories, filenames in os.walk('.'):
    if filenames:
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        for filename in filenames:
            if filename.endswith(file_type):
                src = os.path.join(root, filename)
                shutil.copy2(src, new_directory)
            else:
                print filename + " is not of type " + file_type
    else:
        print "Could not find any files."