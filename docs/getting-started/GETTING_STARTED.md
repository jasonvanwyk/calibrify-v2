# Getting Started with Calibrify

This guide will help you set up Calibrify for development or production use.

## Prerequisites

- Docker Engine 24.0+
- Docker Compose V2
- Git
- A text editor (VS Code recommended)

## Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/calibrify-v2.git
   cd calibrify-v2
   ```

2. **Environment Configuration**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your settings
   nano .env
   ```

3. **Build and Start Services**
   ```bash
   # Start development environment
   docker-compose -f docker/development/docker-compose.dev.yml up --build
   
   # In a new terminal, run migrations
   docker-compose -f docker/development/docker-compose.dev.yml exec backend python manage.py migrate
   
   # Create a superuser
   docker-compose -f docker/development/docker-compose.dev.yml exec backend python manage.py createsuperuser
   ```

4. **Access the Application**
   - Backend API: http://localhost:8000/api/
   - Admin Interface: http://localhost:8000/admin/
   - Frontend: http://localhost:8080/

## Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Run Tests**
   ```bash
   docker-compose -f docker/development/docker-compose.dev.yml exec backend python manage.py test
   ```

3. **Check Code Style**
   ```bash
   # Backend
   docker-compose -f docker/development/docker-compose.dev.yml exec backend flake8
   
   # Frontend
   npm run lint
   ```

4. **Make a Pull Request**
   - Push your changes
   - Create a PR against the main branch
   - Wait for CI checks and review

## Production Deployment

See our [Deployment Guide](../deployment/DEPLOYMENT.md) for production setup instructions.

## Common Issues

### Database Migrations
If you see database errors, try:
```bash
docker-compose -f docker/development/docker-compose.dev.yml down -v
docker-compose -f docker/development/docker-compose.dev.yml up --build
```

### Port Conflicts
If you see port conflicts, check if you have other services running on ports 8000 or 8080.

## Next Steps

- Read the [Architecture Overview](../development/ARCHITECTURE.md)
- Review our [Coding Standards](../development/CODING_STANDARDS.md)
- Check out the [API Documentation](../development/API.md) 