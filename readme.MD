# Project Setup and Deployment

This document provides instructions for setting up and running the necessary services for the project. This includes the main server, processing server, and Redis server, all using Docker containers and a custom Docker network.

## Prerequisites

- Docker installed on your machine.
- Docker Compose (optional, for easier management).

## Services and Ports

1. **Main Server**

   - **Port**: 8000
   - **Command**: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

2. **Processing Server**

   - **Port**: 9000
   - **Command**: `uvicorn main:app --host 0.0.0.0 --port 9000 --reload`

3. **Redis Server**
   - **Port**: 6379
   - **Docker Command**: `docker run -d -p 6379:6379 --name redis-container redis`

## Setup Instructions

### 1. Create a Docker Network

First, create a custom Docker network to ensure that all containers can communicate with each other:

```bash
sudo docker network create chatbotnetwork
```

### 2. Run the Redis Server

Run the Redis server in a Docker container and connect it to the chatbotnetwork:

```bash
Copy code
sudo docker run --name redis-server --network chatbotnetwork -p 6379:6379 -d redis
```

### 3. Run the Main Server

Start the main server container, connecting it to the chatbotnetwork:

```bash
Copy code
sudo docker run --network chatbotnetwork -d -p 8000:8000 chatbotmain
```

### 4. Run the Processing Server

Start the processing server container, also connecting it to the chatbotnetwork:

```bash
Copy code
sudo docker run --network chatbotnetwork -d -p 9000:9000 chatbotprocess
```

### Notes

Ensure that Docker Daemon is running before executing the commands.
Replace chatbotmain and chatbotprocess with the actual Docker image names if they differ.
To use Docker Compose for managing these services, a docker-compose.yml file can be created for easier configuration and management.

### Troubleshooting

#### Ports Conflicts:

Ensure that no other services are using ports 8000, 9000, or 6379 on your host machine.

#### Network Issues:

If containers cannot communicate, verify that they are attached to the same Docker network using docker network inspect chatbotnetwork.
For further assistance, please refer to Docker's official documentation or consult with the development team.