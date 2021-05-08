sudo apt-get update
sudo apt-get install docker.io

#eigen docker pullen
sudo docker pull dockertomhub/endboss
sudo docker pull redis
sudo docker pull mongo

#onderdelen van de docker laden
sudo docker run -d --network="host" redis
sudo docker run -d --network="host" mongo
sudo docker run --network="host" dockertomhub/endboss
