#!/bin/bash

# Helper script for common commands

case "$1" in
  "build")
    echo "Building Docker containers..."
    sudo docker-compose build
    ;;
  "up")
    echo "Starting Docker containers..."
    sudo docker-compose up -d
    ;;
  "down")
    echo "Stopping Docker containers..."
    sudo docker-compose down
    ;;
  "restart")
    echo "Restarting Docker containers..."
    sudo docker-compose down
    sudo docker-compose up -d
    ;;
  "logs")
    echo "Showing logs..."
    sudo docker-compose logs -f
    ;;
  "createsuperuser")
    echo "Creating superuser..."
    sudo docker-compose exec web python create_admin.py
    ;;
  "shell")
    echo "Opening Django shell..."
    sudo docker-compose exec web python manage.py shell
    ;;
  "test")
    echo "Opening Django shell..."
    sudo docker-compose exec web python manage.py test api.tests.test_api
    ;;
  "makemigrations")
    echo "Making migrations..."
    sudo docker-compose exec web python manage.py makemigrations
    ;;
  "migrate")
    echo "Applying migrations..."
    sudo docker-compose exec web python manage.py migrate
    ;;
  *)
    echo "Usage: ./manage.sh [command]"
    echo "Available commands:"
    echo "  build            - Build Docker containers"
    echo "  up               - Start Docker containers"
    echo "  down             - Stop Docker containers"
    echo "  restart          - Restart Docker containers"
    echo "  logs             - Show logs"
    echo "  createsuperuser  - Create a superuser"
    echo "  shell            - Open Django shell"
    echo "  makemigrations   - Create database migrations"
    echo "  migrate          - Apply database migrations"
    ;;
esac