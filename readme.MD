CHROMA COMMAND
chroma run --host localhost --port 5000 --path ~/companydb

processing server port : 9000  
command for processing server : uvicorn main:app --host 0.0.0.0 --port 9000 --reload

main server port :8000
command for main server : uvicorn main:app --host 0.0.0.0 --port 8000 --reload

redis server port :5672
command to run redis docker image with localhost : docker run -d -p 6379:6379 --name redis-container redis


command to create the network:
sudo docker network create chatbotnetwork



commands to run on a same network :
sudo docker run --network chatbotnetwork  -d -p 8000:8000 chatbotmain
sudo docker run --network chatbotnetwork  -d -p 9000:9000 chatbotprocess
sudo docker run --name redis-server --network chatbotnetwork -p 6379:6379 -d redis



