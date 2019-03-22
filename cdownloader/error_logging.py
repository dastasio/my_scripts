import sys
from os import removedirs

def exitWithError(error = str):
    #removedirs('temp')
    sys.exit('Error: ' + error)