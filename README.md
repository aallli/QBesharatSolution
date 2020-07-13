# QBesharatSolution

1- apt-get update && apt-get -y upgrade
2- apt-get install python3 && apt-get install python3-pip && apt-get install libpq-dev
3- Install nginx:

    sudo apt-get update
    sudo apt-get install nginx

4- pip3 install virtualenv
5- Create virtual environment: virtualenv venv
6- Clone source: git clone https://github.com/aallli/QBesharatSolution.git
7- Activate virtualenv: source venv/bin/activate
8- pip install -r requirements.txt
9- Install postgresql:

    sudo apt-get install postgresql postgresql-contrib
    sudo usermod -aG sudo postgres

10- Switch over to the postgres account on your server by typing:
    
    sudo -i -u postgres

11- Create database named sadesa: sudo -u postgres createdb

    sudo -u postgres createdb qbesharat

12- Set postgres password: 
    
    sudo -u postgres psql postgres
    \password postgres
    \q
    exit 

13- Caution: Allow remote access to postgres:
    
    Add to /etc/postgresql/9.5/main/postgresql.conf : #listen_addresses = '*'
    Add to /etc/postgresql/9.5/main/pg_hba.conf : host all all 0.0.0.0/0 trust
    systemctl restart postgresql

NOTE: Set environment variable for database access: 

    export DATABASES_PASSWORD='[Database password]'

14- python manage.py migrate

NOTE: Set environment variable for database access: 

    export ALLOWED_HOSTS='[Server IP]'
    
15- test if gunicorn can serve application: gunicorn --bind 0.0.0.0:8000 QBesharatSolution.wsgi
16- sudo groupadd --system www-data
17- sudo useradd --system --gid www-data --shell /bin/bash --home-dir /home/[user]/qbesharat/QBesharatSolution qbesharat
18- sudo usermod -aG sudo qbesharat
19- sudo chown -R qbesharat:www-data /home/[user]/qbesharat/QBesharatSolution
20- sudo chmod -R g+w /home/[user]/qbesharat/QBesharatSolution
21- sudo chmod 777 /home/[user]/qbesharat/QBesharatSolution/media/

Configure Gunicorn:
22- sudo nano /etc/systemd/system/gunicorn-qbesharat.service
23- add:
    
    [Unit]
    Description=gunicorn daemon
    After=network.target
    
    [Service]
    User=qbesharat
    Group=www-data
    WorkingDirectory=/home/[user]/qbesharat/QBesharatSolution
    EnvironmentFile=/etc/gunicorn-qbesharat.env
    ExecStart=/home/[user]/qbesharat/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/[user]/qbesharat/QBesharatSolution/QBesharatSolution.sock QBesharatSolution.wsgi:application
    
    [Install]
    WantedBy=multi-user.target
        
24- sudo nano /etc/gunicorn-qbesharat.env
24- Add followings:
    
    DEBUG=0
    DEPLOY=1
    DATABASES_PASSWORD='[database password]'
    ALLOWED_HOSTS='[server ip]'
    ADMIN_TEL='[admin tel]'
    ADMIN_EMAIL='[admin email]'
    LIST_PER_PAGE=[list per page in admin pages]
    CHAT_SERVER_URL='[Chat server url]'
    CHAT_SUPPORT_GROUP='[The name of chat support group]'
    CHAT_SUPPORT_REFRESH_INTERVAL=[interval in seconds]
    
25- sudo systemctl start gunicorn-qbesharat
26- sudo systemctl enable gunicorn-qbesharat
27- Check if 'QBesharatSolution.sock' file exists: ls /home/[user]/qbesharat/QBesharatSolution
28- sudo nano /etc/nginx/conf.d/proxy_params
29- Add followings:

    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

29- If gunicorn.service file is changed, run:

    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn-qbesharat

30- Install gettext:

    deactivate
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install
    sudo apt-get install gettext

31- Compile messages for i18N:
    
    source env/bin/activate
    django-admin compilemessages -f (if translation is needed)

32- Collect static files: (Create static and uploads directory if needed)
 
    python manage.py collectstatic

Configure Nginx:
33- create keys and keep them in /root/certs/qbesharat/:
    
    openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out /root/certs/qbesharat/qbesharat.crt -keyout /root/certs/qbesharat/qbesharat.key

34- Restrict the key’s permissions so that only root can access it:
    
    chmod 400 /root/certs/qbesharat/qbesharat.key


36- Run nginx:

    sudo systemctl daemon-reload
    sudo systemctl start nginx.service
    sudo systemctl enable nginx.service
    
37- Configure nginx:

    sudo nano /etc/nginx/conf.d/qbesharat.conf

38- Add:
    
    server {
        listen       80;
        server_name  qbesharat.irib.ir;
    
        error_page 404 /404.html;
        location /404.html {
            root /home/[user]/qbesharat/QBesharatSolution/static/errors;
            internal;
        }
    
        location /static/ {
            if ($request_method = 'GET') {
                add_header 'Access-Control-Allow-Origin' 'http://qbesharat.irib.ir:8000';
                add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
                add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
                add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
            }
    
            root /home/[user]/qbesharat/QBesharatSolution;
        }
    
        location   / {
            return 301 http://qbesharat.irib.ir:8000;
        }
    }
    
    server {
        listen 8000;
        server_name  qbesharat.irib.ir;
    
        location = /favicon.ico { access_log off; log_not_found off; }
    
        error_page 502 /502.html;
        location /502.html {
            root /home/[user]/qbesharat/QBesharatSolution/static/errors;
            internal;
        }
    
        error_page 503 504 507 508 /50x.html;
        location /50x.html {
            root /home/[user]/qbesharat/QBesharatSolution/static/errors;
            internal;
        }
    
        location /static/ {
            root /home/[user]/qbesharat/QBesharatSolution;
        }
    
        location /media/ {
            root /home/[user]/qbesharat/QBesharatSolution;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/[user]/qbesharat/QBesharatSolution/QBesharatSolution.sock;
        }
    }

39- Test your Nginx configuration for syntax errors by typing: 

    sudo /usr/sbin/nginx -t

40- Restart nginx:

    sudo systemctl restart nginx.service
    sudo systemctl status nginx.service

41- Get more admin themes:
    
    python manage.py loaddata admin_interface_theme_django.json
    python manage.py loaddata admin_interface_theme_bootstrap.json
    python manage.py loaddata admin_interface_theme_foundation.json
    python manage.py loaddata admin_interface_theme_uswds.json