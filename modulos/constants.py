# Packages
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from RPA.PDF import PDF
from RPA.Tables import Tables
import os

# Setuping RPA Framework
browser_lib = Selenium()
fileSystem_lib = FileSystem()
pdf_lib = PDF()
tables_lib = Tables()

# Constants
OUTPUT_PATH = os.getcwd() + '\output'
DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'), 'downloads')
AGENCY = 'National Science Foundation'

print('OUTPUT_PATH:',OUTPUT_PATH)
print('DOWNLOAD_PATH:',DOWNLOAD_PATH)
print('AGENCY:',AGENCY)

try:
    os.mkdir(OUTPUT_PATH)
except:
    print('Output path already exist.')

browser_lib.set_download_directory(OUTPUT_PATH)
