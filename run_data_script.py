module_path = ('/home/amitj/praat/')
import sys
sys.path.append(module_path)
from calculate_data import calculate_data

if __name__=='__main__':
    print calculate_data('sample','/tmp/some_tmp')
