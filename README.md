# social-network
hillel_python_pro
1. git clone
2. create+activate venv (python3 -m venv venv + source venv/bin/activate)
3. pip install -r requirements.txt
4. create directory for user's avatar saving (or it will be created automatically)
5. add .env (SECRET KEY, UPLOADED_PHOTOS_DEST, POSTGRESQL DATABASE INFO (USER, PASSWORD, HOST, DB_NAME)) (check example)
6. READY TO RUN (network.py)

* U can switch db from postresql to another in config by yourself.
* To create fake users $ flask fake users *amount*
* If FATAL:  password authentication failed for user - create postgres superuser named system user with system password
* If ImportError: cannot import name 'secure_filename' from 'werkzeug' - 
in venv/lib/site-packages/flask_uploads.py change 

*from werkzeug import secure_filename, FileStorage* 

to

*from werkzeug.utils import secure_filename*

*from werkzeug.datastructures import  FileStorage* 