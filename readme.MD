# Project Setup and Deployment

This document provides instructions for setting up and running the necessary services for the project. This includes the main server, processing server, and Redis server, all using Docker containers and a custom Docker network.

## Prerequisites

- Docker installed on your machine.
- Docker Compose (optional, for easier management).

### 1. Install Mysql and set the root user at password 12345678

### 2. Run the Redis Server

Run the Redis server in a Docker container and connect it to the chatbotnetwork:

```bash
Copy code
sudo docker run --network chatbotnetwork --name redis-server -d redis:latest
```

### 3. Run the RabbitMQ Server

```bash
Copy code
sudo docker run --network chatbotnetwork --name rabbitmq -it --rm --name rabbitmq -d -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

### 4. Run the Qdrant Server

```bash
Copy code
sudo docker run --network chatbotnetwork --name qdrant -d -p 6333:6333 -p 6334:6334 \
-v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### 6. Run the Main Server after building the latest image

```bash
 sudo docker run --network chatbotnetwork  -e MYSQL_URI='mysql+pymysql://<user>:<password>@<your Ip>:3306/chatbotserver' -e OPENAI_API_KEY='' -e LANGCHAIN_API_KEY='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' -e DEEP_INFRA_API_KEY='' -e REDIS_URL='redis://redis-server:6379/0' -p 8000:8000 chatbotmain

```

### 7. Run the Processing Server after building the latest image

```bash
sudo docker run --network chatbotnetwork  -e MYSQL_URI='mysql+pymysql://<user>:<password>@<your Ip>:3306/chatbotserver' -e OPENAI_API_KEY='' -e MAILJET_API_KEY='b206a37878213791ca36f654de1a5ee4' -e MAILJET_SECRET_KEY='0186662647f8ca1a38953139ce28ff3a' -e SENDER='shivam.pandey@jellyfishtechnologies.com' -p 9000:9000 chatbotprocess

```

### Troubleshooting

#### Ports Conflicts:

Ensure that no other services are using ports 8000, 9000, or 6379 on your host machine.

if issue presist stop the local redis with

```bash
cd processing_server
sudo snap stop redis

```

#### Network Issues:

If containers cannot communicate, verify that they are attached to the same Docker network using docker network inspect chatbotnetwork.
For further assistance, please refer to Docker's official documentation or consult with the development team.
