-vm kurduktan sonra ssh ile baglanip nifi ve kafka olusturmak icin asagidaki kodlari kopyalayip terminalde calistiriyoruz

sudo apt update
wget https://archive.apache.org/dist/nifi/1.13.2/nifi-1.13.2-bin.tar.gz
tar -xzvf nifi-1.13.2-bin.tar.gz
sudo apt-get install openjdk-8-jdk -y


-nifi.properties dosyasina girip f6 ile arama cubuguna 127 yazip 127 ile baslayan ip yi siliyoruz
nano nifi-1.13.2/conf/nifi.properties

- nifi yı baslatıyoruz sonra kafkayı kurup baslatıyoruz
cd nifi-1.13.2/bin
./nifi.sh start
cd
wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.3.1.tgz
tar -xzvf kafka_2.12-3.3.1.tgz
cd kafka_2.12-3.3.1/
sudo nohup bin/zookeeper-server-start.sh config/zookeeper.properties &
sudo nohup bin/kafka-server-start.sh config/server.properties &
sudo apt install python3-pip
pip install kafka-python



-topic oluşturma
sudo bin/kafka-topics.sh --create --topic topic_name --bootstrap-server localhost:9092

-topic silme
sudo bin/kafka-topics.sh --delete --topic topic_name --bootstrap-server localhost:9092

-topic e gönderme
sudo bin/kafka-console-producer.sh --topic topic_name --bootstrap-server localhost:9092

-topic den alma
sudo bin/kafka-console-consumer.sh --topic topic_name --from-beginning --bootstrap-server localhost:9092

-topic'leri listele
bin/kafka-topics.sh --list --bootstrap-server localhost:9092


