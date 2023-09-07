-once docker-compose dosyasını cm e aktar sonra
sudo apt update
sudo apt-get install docker.io -y
sudo apt-get install docker-compose -y
echo -e "AIRFLOW_UID=$(id -u)" > .env
sudo docker-compose up airflow-init
sudo docker-compose up -d