# discourseAdmin
a more fine grained way of administrate discourse (uses sso)

A. install

0. sudo apt-get install libmysqlclient-dev (optional)
1. clone the git:  
2. install requirements: pip3 install -r requirements.txt -f .  (inside the clone directory)
3. create 2 files from the dsso/*.template files
4. create the database
5. populate the database: python3 manage.py migrate

B. development start

python3 manage.py runserver 0.0.0.0:4911
-> should start on localhost:4911 


C. Update
1. pull the git:  
2. update requirements: pip3 install -r requirements.txt -f .  (inside the clone directory)
4. update the database: python3 manage.py migrate


D. Production Setup
1. install ngnix
2. install gunicorn3
3. collect static files "python3 manage.py collectstatic"
4. create an ngnix server diretive inside your ngnix.conf file (use ngnix.conf.example as template)
5. create an service file (use dsso.service.example as template)
6. sudo systemctl start dsso
