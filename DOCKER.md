# 🐳 Docker Setup Guide

Complete Docker configuration for StockWatcher application with all services (PostgreSQL, Redis, Backend, Frontend, Nginx).

## 📦 Services

- **PostgreSQL 15**: Database server
- **Redis 7**: Cache server
- **Backend**: Flask Python application with Gunicorn
- **Frontend**: React application
- **Nginx**: Reverse proxy and load balancer

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
bash docker-setup.sh
```

### Option 2: Manual Start

```bash
docker-compose up -d
```

## 🌐 Access URLs

| Service | URL | Port |
|---------|-----|------|
| Frontend | http://localhost:3000 | 3000 |
| Backend API | http://localhost:8000 | 8000 |
| Nginx | http://localhost:80 | 80 |
| PostgreSQL | localhost:5432 | 5432 |
| Redis | localhost:6379 | 6379 |

## 📝 Database Credentials

```
Username: stockwatcher
Password: stockwatcher_password
Database: stockwatcher
Host: postgres
Port: 5432
```

## 📊 Useful Docker Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Container Management

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Restart containers
docker-compose restart

# Rebuild images
docker-compose build --no-cache

# Full rebuild and restart
docker-compose down --remove-orphans
docker-compose up -d --build
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U stockwatcher -d stockwatcher

# Redis CLI
docker-compose exec redis redis-cli
```

### Service Health Check

```bash
# Check all services
docker-compose ps

# Inspect specific container
docker inspect stockwatcher-backend
docker inspect stockwatcher-frontend
```

## 🔧 Configuration

### Environment Variables

Environment variables are defined in `docker-compose.yml`:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `FLASK_ENV`: Flask environment (production/development)
- `REACT_APP_API_URL`: Frontend API URL

### Volume Management

Persistent volumes for data:

- `postgres_data`: PostgreSQL database files
- `redis_data`: Redis data files

Local development volumes:

- `./backend:/app`: Backend source code (live reload)
- `./frontend:/app`: Frontend source code (live reload)

## 🐛 Troubleshooting

### Containers won't start

```bash
# Check Docker daemon
docker info

# View error logs
docker-compose logs

# Rebuild everything
docker-compose build --no-cache
docker-compose up -d
```

### Port already in use

```bash
# Find process using port
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Kill process
kill -9 <PID>
```

### Database connection error

```bash
# Wait for database to be ready
docker-compose exec backend bash

# Test connection
psql -U stockwatcher -h postgres -d stockwatcher -c "SELECT 1"
```

### Redis connection error

```bash
# Check Redis
docker-compose exec redis redis-cli ping
```

## 📈 Production Deployment

For production, consider:

1. Use `.env` file for sensitive data
2. Enable HTTPS/SSL in Nginx
3. Use environment-specific configurations
4. Set up proper logging and monitoring
5. Configure database backups
6. Use dedicated volumes for data persistence
7. Set resource limits for containers

Example production updates:

```yaml
# In docker-compose.yml
services:
  postgres:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
```

## 🔐 Security Notes

⚠️ **Warning**: Default credentials in this setup are for development only.

For production:
- Change database password in `docker-compose.yml`
- Use environment variables for sensitive data
- Enable SSL/TLS for all connections
- Implement proper authentication
- Use secrets management system
- Regular security updates

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

## ❓ FAQ

**Q: How do I reset the database?**
```bash
docker-compose down -v
docker-compose up -d
```

**Q: How do I backup the database?**
```bash
docker-compose exec postgres pg_dump -U stockwatcher stockwatcher > backup.sql
```

**Q: Can I use this in production?**
Not as-is. You'll need to make security modifications and use proper secrets management.

**Q: How do I modify services?**
Edit `docker-compose.yml` and run `docker-compose up -d --build`