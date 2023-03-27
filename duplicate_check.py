import os



def find_duplicate_files(folder):
    # create a dictionary to store file names and their paths
    duplicate_files = []
    files_dict = {}
    for subdir, dirs, files in os.walk(folder):
        print(len(files))
        for file in files:
            if file.endswith(".txt"):
                # check if file already exists in the dictionary
                if file in files_dict:
                    # if file already exists, print its path and the path of the duplicate file
                    print(f"Duplicate file: {file}")
                    print(f"{os.path.join(subdir, file)} and {files_dict[file]}")
                    duplicate_files.append(file)
                else:
                    # if file does not exist, add it to the dictionary with its path
                    files_dict[file] = os.path.join(subdir, file)
    
    if (len(duplicate_files)==0):
        print(f"no duplicates in folder: {folder}")
    else:
        print(duplicate_files)      

# call the function and pass the path to the folder you want to check for duplicates
find_duplicate_files("/Users/duncanoregan/Desktop/untitled folder")