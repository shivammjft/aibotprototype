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
sudo docker run -d -p 6379:6379 redis:latest
```

### 3. Run the RabbitMQ Server

```bash
Copy code
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

### 4. Run the Qdrant Server

```bash
Copy code
docker run -p 6333:6333 -p 6334:6334 \
-v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### 6. Run the Main Server with the env

```bash
cd main_server
uvicorn main:app --port 8000 --reload

```

### 7. Run the Processing Server with the env

```bash
cd processing_server
uvicorn main:app --port 9000 --reload

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
