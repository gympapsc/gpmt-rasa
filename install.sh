mkdir nginx-config-files 
wget -qO nginx-config-files/nginx.conf https://storage.googleapis.com/rasa-x-releases/0.42.0/nginx-config-files/nginx.conf 
wget -qO nginx-config-files/ssl.conf.template https://storage.googleapis.com/rasa-x-releases/0.42.0/nginx-config-files/ssl.conf.template 
wget -qO nginx-config-files/rasax.nginx.template https://storage.googleapis.com/rasa-x-releases/0.42.0/nginx-config-files/rasax.nginx.template 
sudo mkdir ./db && sudo chown -R 1001 ./db && sudo chmod -R 750 ./db
sudo docker-compose -f docker-compose.yml up -d