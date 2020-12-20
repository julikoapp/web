sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -sf /home/box/web/hello.py /etc/gunicorn.d/hello.py


sudo /etc/init.d/gunicorn restart

gunicorn --bind='0.0.0.0:8080' hello:wsgi_application
