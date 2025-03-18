# Blog Platform API - Technical Documentation

This document provides detailed technical information about the Blog Platform API implementation.

## Architecture

The Blog Platform API follows a modern microservices architecture using Docker containers:

1. **Web API Container**: Django + Django REST Framework application
2. **Database Container**: PostgreSQL database
3. **Cache/Message Broker Container**: Redis
4. **Worker Containers**: Celery workers for asynchronous tasks
5. **Scheduler Container**: Celery Beat for scheduled tasks

## Technology Stack

### Core Technologies

- **Python 3.10**: Base programming language
- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: REST API framework
- **PostgreSQL 15**: Relational database
- **Redis 7**: Cache and Celery message broker
- **Celery 5.3.4**: Distributed task queue
- **Docker & Docker Compose**: Containerization
- **JWT Authentication**: Token-based authentication via SimpleJWT

### Additional Libraries

- **django-filter**: Filtering support for DRF
- **drf-yasg**: Swagger/OpenAPI documentation
- **psycopg2-binary**: PostgreSQL adapter
- **python-dotenv**: Environment variable management

## Database Schema

### Core Models

1. **User** (Django's built-in User model)
   - Standard Django user fields (username, email, password, etc.)

2. **UserProfile**
   - `user`: OneToOne relationship with User
   - `role`: Choice field ('author' or 'reader')
   - `bio`: Text field for user information
   - Timestamps (created_at, updated_at)

3. **Category**
   - `name`: String
   - `slug`: String (URL-friendly name)
   - `description`: Text
   - `created_at`: DateTime

4. **Post**
   - `title`: String
   - `content`: Text
   - `author`: ForeignKey to User
   - `categories`: ManyToMany relationship with Category
   - `is_published`: Boolean
   - Timestamps (created_at, updated_at)

5. **Comment**
   - `post`: ForeignKey to Post
   - `author`: ForeignKey to User
   - `content`: Text
   - Timestamps (created_at, updated_at)

6. **Like**
   - `post`: ForeignKey to Post
   - `user`: ForeignKey to User
   - `created_at`: DateTime
   - Unique constraint on (post, user)

7. **PostView**
   - `post`: ForeignKey to Post
   - `user`: ForeignKey to User (nullable for anonymous views)
   - `ip_address`: IP address
   - `timestamp`: DateTime

8. **PostStatistics**
   - `post`: ForeignKey to Post
   - `date`: Date
   - `view_count`: Integer
   - `like_count`: Integer
   - `comment_count`: Integer
   - Unique constraint on (post, date)

## API Security

### Authentication

The API uses JWT (JSON Web Tokens) for authentication:

- Tokens are obtained by sending credentials to `/api/auth/login/`
- Access tokens expire after 1 day (configurable)
- Refresh tokens expire after 7 days (configurable)
- Token must be included in the `Authorization` header of requests: `Bearer <token>`

### Permissions

The API implements several custom permission classes:

1. **IsAuthorOrReadOnly**
   - Allows read-only access to anyone
   - Only allows write operations to the author of the content

2. **IsAuthor**
   - Only allows users with the 'author' role

3. **IsReader**
   - Only allows users with the 'reader' role

4. **IsCommentAuthorOrReadOnly**
   - Only allows modification of comments by their authors

### Rate Limiting

The API implements rate limiting to prevent abuse:

- Anonymous users: 5 requests/minute
- Authenticated users: 30 requests/minute

## Asynchronous Tasks

The API uses Celery for asynchronous and scheduled tasks:

### Tasks

1. **send_welcome_email**
   - Triggered when a new user registers
   - Sends a welcome email asynchronously

2. **generate_daily_post_statistics**
   - Scheduled to run daily at midnight
   - Aggregates and stores statistics for all posts

3. **clean_old_view_data**
   - Periodically cleans old view records to prevent database bloat

## Advanced Features

### Search and Filtering

The API supports comprehensive search and filtering options:

- Search posts by title or content
- Filter posts by author, date, or category
- Sort posts by date or popularity (view count)

### Pagination

- Default page size: 10 items
- Configurable via query parameters (`?page=2&page_size=20`)

### Custom Middleware

The API includes a custom middleware for request logging:

- `RequestLoggingMiddleware`: Logs details about requests and responses
- Records processing time, status codes, and user information

## Docker Configuration

### Services

1. **web**
   - Django application
   - Exposes port 8000
   - Depends on db and redis

2. **db**
   - PostgreSQL database
   - Persists data via a Docker volume

3. **redis**
   - Redis instance for caching and message broker

4. **celery**
   - Celery worker for processing asynchronous tasks
   - Connected to the same codebase as the web service

5. **celery-beat**
   - Scheduler for periodic tasks
   - Uses the same codebase as the web service

### Data Persistence

- Database data is persisted using a Docker volume (`postgres_data`)
- Configuration is done via environment variables

## Deployment Considerations

### Production Settings

For production deployment, consider:

1. **Environment Variables**
   - Set `DEBUG=0`
   - Use a strong, unique `SECRET_KEY`
   - Configure database credentials securely

2. **Security Settings**
   - Set appropriate `ALLOWED_HOSTS`
   - Enable HTTPS
   - Configure CORS settings if needed

3. **Performance Optimizations**
   - Add caching (Redis or similar)
   - Consider database read replicas for high traffic
   - Use a production-grade web server (Nginx, etc.)

### Scaling

The application can be scaled in various ways:

1. **Horizontal Scaling**
   - Multiple web containers behind a load balancer
   - Multiple Celery workers

2. **Database Scaling**
   - Master-slave replication
   - Connection pooling

3. **Caching**
   - Implement Redis caching for frequently accessed data
   - Consider a CDN for static assets

## Testing

The project includes unit tests for the API endpoints:

- Authentication tests
- CRUD operation tests for posts, comments, likes
- Permission tests
- Rate limiting tests

Run tests using:
```bash
docker-compose exec web python manage.py test
```

## Monitoring

For production deployments, consider adding:

1. **Application Monitoring**
   - Django Debug Toolbar (development)
   - Application Performance Monitoring (APM) tools
   - Prometheus and Grafana

2. **Log Management**
   - Centralized logging (ELK stack, Graylog, etc.)
   - Error tracking (Sentry)

## API Documentation

The API documentation is available through Swagger and ReDoc:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Troubleshooting

Common issues and solutions:

1. **Database Connection Issues**
   - Check if PostgreSQL container is running
   - Verify database credentials
   - Check network connectivity between containers

2. **Authentication Problems**
   - Ensure token format is correct: `Bearer <token>`
   - Check if token is expired
   - Verify user exists and is active

3. **Celery Task Issues**
   - Check if Redis is running
   - Verify Celery worker logs
   - Ensure tasks are properly registered