import sys 
sys.path.insert(0, '/projekt/back')
activate_this = 
with open(activate_this) as file_:
    exec(file.read(), dict(__file__=activate_this))
from base_file import app as application