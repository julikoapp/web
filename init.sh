sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

sudo ln -s /home/box/web/hello.py   /etc/gunicorn.d/test
sudo /etc/init.d/gunicorn restart

cd /home/box/web/

#sudo gunicorn -c /home/box/web/hello.py hello:wsgi_application
#sudo nano /usr/sbin/gunicorn-debian
sudo nano /usr/bin/gunicorn
sudo nano /usr/bin/gunicorn_django
sudo nano /usr/bin/gunicorn_paster
sudo ln -sf /home/box/web/etc/django_conf.py /etc/gunicorn.d/django_conf.py

sudo gunicorn -c /etc/gunicorn.d/django_conf.py ask.wsgi:application
