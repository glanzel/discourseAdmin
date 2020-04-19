# discourseAdmin
a more fine grained way of administrate discourse (uses sso)

install

1. clone the git:  
2. install requirements: pip3 install -r requirements.txt -f .  (inside the clone directory)
3. create 2 files from the dsso/*.template files
4. create the database
4. populate the database: python3 manage.py migrate

start

python3 manage.py runserver 0.0.0.0:4911
-> should start on localhost:4911 
