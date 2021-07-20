# maker
import os
try:
    dirPath = './data'
    if not(os.path.isfile(dirPath)):
        os.mkdir(dirPath)
        print("Created ", dirPath)

    dirPath = './Extracts'
    if not(os.path.isfile(dirPath)):
        os.mkdir(dirPath)
        print("Created ", dirPath)

    dirPath = './Transcripts'
    if not(os.path.isfile(dirPath)):
        os.mkdir(dirPath)
        print("Created ", dirPath)

    dirPath = './Summary'
    if not(os.path.isfile(dirPath)):
        os.mkdir(dirPath)
        print("Created ", dirPath)


except:
    print('Error while Creating directory', dirPath)
