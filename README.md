# Blog Platform API

A complete RESTful API for a blog platform with user authentication, post management, and analytics functionalities, built with Django REST Framework.

![Django](https://img.shields.io/badge/Django-4.x-green)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.14-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Celery](https://img.shields.io/badge/Celery-5.3-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## Features

- **User Management**
  - Registration and authentication with JWT tokens
  - User roles (Author, Reader)
  - Profile management

- **Blog Post Management**
  - Create, read, update, and delete blog posts
  - Categories for organizing content
  - Comments and likes functionality
  - Permission-based access control

- **Analytics**
  - Track post views, likes, and comments
  - Generate daily statistics
  - Basic analytics dashboard

- **Advanced API Features**
  - JWT Authentication
  - Role-based permissions
  - Rate limiting
  - Search and filtering
  - Pagination

## System Architecture

The API is built using a modern microservices architecture with Docker:

## Flowchart
![Flowchart](https://raw.githubusercontent.com/praddypawar/blog_platform/main/flowchart.jpeg)

## Data Model
![Data Model](https://github.com/praddypawar/blog_platform/blob/main/db.jpeg)

## Process Diagram
![Process Diagram](https://raw.githubusercontent.com/praddypawar/blog_platform/main/process.jpeg)



## Tech Stack

- **Backend Framework**: Django 4.x with Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT (JSON Web Tokens)
- **Asynchronous Tasks**: Celery with Redis
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker and Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blog-platform.git
   cd blog-platform
   ```

2. Make the helper script executable:
   ```bash
   chmod +x manage.sh
   ```

3. Start the Docker containers:
   ```bash
   ./manage.sh up
   ```

4. Create an admin user:
   ```bash
   ./manage.sh createsuperuser
   ```

5. Get a JWT token for the admin user:
   ```bash
   ./manage.sh token admin
   ```

6. Access the API documentation:
   - Swagger UI: http://localhost:8000/swagger/
   - ReDoc: http://localhost:8000/redoc/

### Usage Commands

The project includes a helper script `manage.sh` for common operations:

```bash
# Build Docker containers
./manage.sh build

# Start Docker containers
./manage.sh up

# Stop Docker containers
./manage.sh down

# Restart Docker containers
./manage.sh restart

# Show logs
./manage.sh logs

# Create a superuser
./manage.sh createsuperuser

# Open Django shell
./manage.sh shell

# Create database migrations
./manage.sh makemigrations

# Apply database migrations
./manage.sh migrate

# Get JWT token for a user
./manage.sh token <username>
```

## API Endpoints

### Authentication

```
POST /api/auth/register/     # Register a new user
POST /api/auth/login/        # Log in and get JWT token
POST /api/auth/refresh/      # Refresh JWT token
```

### Blog Posts

```
GET  /api/posts/             # List all posts
POST /api/posts/             # Create a new post (Author only)
GET  /api/posts/{id}/        # Get single post
PUT  /api/posts/{id}/        # Update post (Author only)
DELETE /api/posts/{id}/      # Delete post (Author only)
```

### Interactions

```
POST /api/posts/{id}/like/    # Like/unlike a post
POST /api/posts/{id}/comment/ # Add a comment to a post
GET  /api/posts/{id}/stats/   # Get post statistics
```

### Categories

```
GET  /api/categories/         # List all categories
POST /api/categories/         # Create a new category
GET  /api/categories/{id}/    # Get single category
PUT  /api/categories/{id}/    # Update category
DELETE /api/categories/{id}/  # Delete category
```

## Authentication

The API uses JWT (JSON Web Token) authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api/auth/login/` with username and password
2. Include the token in the Authorization header of your requests:
   ```
   Authorization: Bearer <your_token>
   ```

## Development

### Project Structure

```
blog_platform/
├── api/                    # Main API app
│   ├── migrations/         # Database migrations
│   ├── models.py           # Data models
│   ├── serializers.py      # REST framework serializers
│   ├── views.py            # API views and endpoints
│   ├── urls.py             # URL routing
│   ├── permissions.py      # Custom permissions
│   ├── tasks.py            # Celery tasks
│   ├── middleware.py       # Custom middleware
│   └── tests/              # Test suite
├── blog_platform/          # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL routing
│   └── celery.py           # Celery configuration
├── docker-compose.yml      # Docker services definition
├── Dockerfile              # Docker container definition
├── requirements.txt        # Python dependencies
└── manage.py               # Django command-line utility
```

## Testing

Run the test suite with:

```bash
./manage.sh test
```

## API Documentation

### Swagger UI
![Swagger UI](https://raw.githubusercontent.com/praddypawar/blog_platform/main/swagger_ui.jpeg)

### ReDoc
![ReDoc](https://raw.githubusercontent.com/praddypawar/blog_platform/main/redoc_ui.jpeg)

## Django Admin Panel
![Django Admin](https://raw.githubusercontent.com/praddypawar/blog_platform/main/django_admin.jpeg)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name <your.email@example.com>
```
