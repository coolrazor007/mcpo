# MCPO Setup Guide

## Docker Configuration

### Container Setup

The MCPO server runs in a Docker container with the following security and configuration features:

1. **Non-Root User**
   ```dockerfile
   # Create dedicated user and group
   RUN groupadd -r mcpo && useradd -r -g mcpo mcpo
   
   # Set proper ownership
   RUN chown -R mcpo:mcpo /app
   
   # Switch to mcpo user
   USER mcpo
   ```

2. **Virtual Environment**
   ```dockerfile
   ENV VIRTUAL_ENV=/app/.venv
   RUN uv venv "$VIRTUAL_ENV" && chown -R mcpo:mcpo "$VIRTUAL_ENV"
   ENV PATH="$VIRTUAL_ENV/bin:$PATH"
   ```

3. **Cache Directory**
   ```dockerfile
   RUN mkdir -p /home/mcpo/.cache && chown -R mcpo:mcpo /home/mcpo
   ```

### Volume Mounts

The container uses two primary volume mounts:
```yaml
volumes:
  - ./config:/app/config:ro  # Read-only configuration
  - ./logs:/app/logs         # Read-write logs
```

### Network Configuration

1. **Port Mapping**
   ```yaml
   ports:
     - "${PORT}:${PORT}"  # Configurable through .env
   ```

2. **Network Isolation**
   ```yaml
   networks:
     - mcpo-net  # Dedicated bridge network
   ```

### Health Monitoring

The container includes a robust health check system:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:${PORT}/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

## Environment Configuration

### Required Variables

```env
# Server
PORT=8000              # Application port
API_KEY=top-secret    # Authentication key

# Paths
CONFIG_PATH=/app/config/config.json
LOG_PATH=/app/logs

# Container
CONTAINER_NAME=mcpo-server
CONTAINER_USER=mcpo
```

### Optional Settings

```env
# Development
DEBUG=false           # Enable debug mode
LOG_LEVEL=info       # Logging verbosity

# Docker Build
DOCKER_BUILDKIT=1
COMPOSE_DOCKER_CLI_BUILD=1
```

## Security Measures

1. **File Permissions**
   - Configuration files are mounted read-only
   - Log directory is the only writable volume
   - All files owned by non-root user

2. **Process Isolation**
   - Runs as unprivileged user
   - Limited filesystem access
   - Network isolation via Docker network

3. **API Security**
   - API key authentication
   - CORS configuration
   - SSL/TLS support (optional)

## Deployment Steps

1. **Build Container**
   ```bash
   docker-compose build
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Verify Deployment**
   ```bash
   # Check container status
   docker ps | grep mcpo
   
   # Test health endpoint
   curl http://localhost:8000/health
   
   # Access API documentation
   curl -I http://localhost:8000/docs
   ```

## Troubleshooting

1. **Permission Issues**
   - Verify file ownership: `ls -l config/ logs/`
   - Check container user: `docker exec mcpo-server whoami`

2. **Network Issues**
   - Confirm port mapping: `docker port mcpo-server`
   - Test network: `docker network inspect mcpo-net`

3. **Health Check Failures**
   - View logs: `docker logs mcpo-server`
   - Check endpoint: `curl http://localhost:8000/health`
