# cloud_aws


### file structure 

/home/ubuntu/flaskapp/
    ├── flaskapp.py
    ├── flaskapp.wsgi
    ├── users.db
    ├── uploads
    └── templates/
         ├── index.html
         ├── register.html
         ├── display.html
         └── relogin.html

### bash

- sudo chown ubuntu:www-data users.db
- sudo chmod 664 users.db
- sudo chmod 775 uploads
- sudo chown ubuntu:www-data /home/ubuntu/flaskapp
- sudo chmod 775 /home/ubuntu/flaskapp
- sudo chown ubuntu:www-data /home/ubuntu/flaskapp/uploads
- sudo chmod 775 /home/ubuntu/flaskapp/uploads

- sudo systemctl restart apache2
- sudo tail -n 50 /var/log/apache2/error.log
