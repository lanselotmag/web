sudo rm -rf /etc/nginx/sites-enabled/*
sudo ln -sf ~/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
sudo ln -sf ~/web/etc/hello.py /etc/gunicorn.d/test
sudo /etc/init.d/gunicorn restart
