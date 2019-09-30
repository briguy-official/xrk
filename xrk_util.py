# Utilities and helper functions for reading aim xrk files
# Brian Acosta 
# May 16th, 2018
#
#
# Distributed under creative commons beerware license:
# Free, but if you use it and we ever meet you buy me a beer.

from ctypes import *
import os

def c_char2Str(c_char_str):
    return str(c_char_str.value).strip('b').strip('\'')
    
try:
    aimXRK = cdll.LoadLibrary('MatLabXRK-2017-64-ReleaseU.dll')
except:
    print('Could not find AIM XRK access application extension. \nPlease ensure \'MatLabXRK-32-ReleaseU.dll\' is in the path of this program. Goodbye.')
    quit()
    
    
def file_pointer(filename):
    try:
        # open_file requires an absolute file path
        full_file_path = os.path.abspath(('%s' %filename)) 
    except ValueError:
        print('name passed to file_pointer must be a python string')
    except IOerror:
        print('XRK file not found. \nPlease place all target XRK files in the xrk_files folder in the project path')
    except:
        print('An error occured locating the specified file.')
    
    # generate a C char pointer to represent the full file path       
    fileptr = c_char_p(full_file_path.encode()) 
    
    return fileptr