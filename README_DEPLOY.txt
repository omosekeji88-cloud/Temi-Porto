PythonAnywhere deployment notes

1. Upload this project folder to PythonAnywhere, for example:
   /home/YOUR_USERNAME/Web_server

2. Create a new Web app on PythonAnywhere.
   Choose: Manual configuration
   Choose a Python version available on your account.

3. In the Web tab, set Source code to:
   /home/YOUR_USERNAME/Web_server

4. Open the WSGI configuration file and replace its contents with:

import sys
path = '/home/YOUR_USERNAME/Web_server'
if path not in sys.path:
    sys.path.append(path)

from server import app as application

5. In a PythonAnywhere Bash console, run:
   cd ~/Web_server
   pip3 install --user -r requirements.txt

6. Go back to the Web tab and click Reload.

7. Visit:
   https://YOUR_USERNAME.pythonanywhere.com

Remember to replace YOUR_USERNAME with your actual PythonAnywhere username.
