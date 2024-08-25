# Task Manager

## Objective

To develop a secure, high-performance, and scalable backend for a task management application, utilizing modern methodologies and technologies to ensure quality and maintainability.

## Technology Stack

- Django
- Django Rest Framework
- Elasticsearch
- Docker
- PostgreSQL
- Pytest

## Features

- User Management:
  - Register
  - Login
  - List, Retrieve, or Delete a User

- Task Management:
  - Create Task
  - Update Task
  - Retrieve Task
  - Delete Task

- Search Functionality:
  - Search tasks using Elasticsearch based on `title` and `description`

## Setup

### Create a `.env` File

In the root directory of the project, create a `.env` file with the following values:

```js
POSTGRES_DB="task_db"
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
POSTGRES_HOST="localhost"
POSTGRES_PORT=5432

ELASTICSEARCH_HOST="http://localhost:9200"
```

## Running the Application Without Docker

1. **Clone the Repository:**
    
    ```bash
    git clone https://github.com/Tomdieu/task-manager.git
    ```

2. **Install the Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Docker Compose:**

   Open `docker-compose.yaml` and comment out the following section:

    ```yaml
    web:
        build: .
        command: gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000
        volumes:
          - .:/app
        ports:
          - "8000:8000"
        depends_on:
          - db
          - elasticsearch
        environment:
          - DATABASE_URL=postgres://user:password@db:5432/task_db
          - POSTGRES_DB=task_db
          - POSTGRES_USER=user
          - POSTGRES_PASSWORD=password
          - ELASTICSEARCH_HOST=http://elasticsearch:9200
    ```

4. **Run Docker Compose:**

    ```bash
    docker compose up
    ```

5. **Run Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Start the Django Server:**

    ```bash
    python manage.py runserver
    ```

7. **Build the Search Index:**

   Ensure the Elasticsearch container is running before executing:

    ```bash
    python manage.py search_index --rebuild
    ```

   Or:

    ```bash
    python manage.py search_index --create
    ```

8. **Access the Swagger API:**

   The API documentation is available at [Swagger API](http://127.0.0.1:8000/swagger/).

9. **Run Tests:**

   Ensure both Elasticsearch and the test database are running, then execute:

    ```bash
    pytest
    ```

## Running the Application with Docker

1. **Clone the Repository:**
    
    ```bash
    git clone https://github.com/Tomdieu/task-manager.git
    ```

2. **Install the Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Execute Docker Compose:**

    ```bash
    docker compose up
    ```

4. **Access the Swagger API:**

   The API documentation is available at [Swagger API](http://127.0.0.1:8000/swagger/).

### Running Tests

Ensure both Elasticsearch and the test database are running, then execute:

```bash
pytest
```