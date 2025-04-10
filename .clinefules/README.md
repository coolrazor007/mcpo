# MCPO Documentation

## Overview

MCPO (Model Context Protocol OpenAPI) is a server that provides a bridge between MCP (Model Context Protocol) servers and OpenAPI. It enables seamless integration of various MCP tools and resources through a RESTful API interface.

## Key Features

- **MCP Server Integration**: Supports multiple MCP servers (memory, time, etc.)
- **OpenAPI Interface**: Auto-generates OpenAPI documentation for all endpoints
- **Security**: Runs with non-root user and supports API key authentication
- **Health Monitoring**: Built-in health check system
- **Docker Support**: Containerized deployment with proper security practices

## Documentation Index

1. [Setup Guide](setup.md)
   - Docker configuration
   - Environment variables
   - Security settings
   - Network configuration

2. [Testing Documentation](testing.md)
   - Test coverage
   - Test results
   - Endpoint verification
   - Health check status

## Quick Links

- Main API Documentation: http://localhost:8000/docs
- Memory Server: http://localhost:8000/memory/docs
- Time Server: http://localhost:8000/time/docs
- Health Check: http://localhost:8000/health

## Environment Variables

```env
# Server configuration
PORT=8000
API_KEY=top-secret

# Application paths
CONFIG_PATH=/app/config/config.json
LOG_PATH=/app/logs

# Development settings
DEBUG=false
LOG_LEVEL=info

# Docker container settings
CONTAINER_NAME=mcpo-server
CONTAINER_USER=mcpo
```

## Project Structure

```
mcpo/
├── config/          # Configuration files
├── logs/           # Application logs
├── src/            # Source code
│   └── mcpo/       # Main package
└── tests/          # Test suite
