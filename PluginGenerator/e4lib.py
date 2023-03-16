import os

def getExtensionName(path):
    return os.path.splitext(path)[1]