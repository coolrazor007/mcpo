# MCPO Testing Documentation

## Test Coverage

### 1. Unit Tests

The test suite includes 12 unit tests covering various aspects of schema processing:

```bash
✓ test_process_simple_string_required
✓ test_process_simple_integer_optional
✓ test_process_simple_boolean_optional_no_default
✓ test_process_simple_number
✓ test_process_unknown_type
✓ test_process_array_of_strings
✓ test_process_array_of_any_missing_items
✓ test_process_simple_object
✓ test_process_nested_object
✓ test_process_array_of_objects
✓ test_process_empty_object
✓ test_model_caching
```

**Last Run Results:**
```bash
======================================================================= test session starts ========================================================================
platform linux -- Python 3.12.3 pytest-8.3.5 pluggy-1.5.0
collected 12 items

tests/test_main.py ............                                                                                                                             [100%]

======================================================================== 12 passed in 0.50s ========================================================================
```

### 2. Integration Tests

#### Core Server Endpoints

1. **Health Check**
   ```bash
   $ curl http://localhost:8000/health
   {"status":"healthy"}
   ```

2. **Main API Documentation**
   ```bash
   $ curl -I http://localhost:8000/docs
   HTTP/1.1 200 OK
   content-type: text/html; charset=utf-8
   ```

#### MCP Server Integration

1. **Memory Server**
   ```bash
   $ curl -I http://localhost:8000/memory/docs
   HTTP/1.1 200 OK
   content-type: text/html; charset=utf-8
   ```

2. **Time Server**
   ```bash
   $ curl -I http://localhost:8000/time/docs
   HTTP/1.1 200 OK
   content-type: text/html; charset=utf-8
   ```

### 3. Container Health

**Container Status:**
```bash
$ docker ps | grep mcpo
856109e46ed2   mcpo-mcpo   "mcpo --port 8000 --…"   Up (healthy)   0.0.0.0:8000->8000/tcp   mcpo-server
```

## Test Verification Points

### Core Functionality
✅ FastAPI server starts successfully  
✅ Health check endpoint responds correctly  
✅ API documentation is accessible  
✅ All unit tests pass  

### Security
✅ Container runs as non-root user  
✅ Configuration mounted read-only  
✅ API key authentication works  

### MCP Integration
✅ Memory server accessible  
✅ Time server accessible  
✅ Server documentation available  

### Container Health
✅ Container reports healthy status  
✅ Port 8000 properly exposed  
✅ Volume mounts working  

## Running Tests

### Unit Tests
```bash
# Install test dependencies
uv pip install ".[dev]"

# Run tests
python -m pytest tests/ -v
```

### Integration Tests
```bash
# Health check
curl http://localhost:8000/health

# API documentation
curl -I http://localhost:8000/docs

# MCP servers
curl -I http://localhost:8000/memory/docs
curl -I http://localhost:8000/time/docs
```

### Container Tests
```bash
# Check status
docker ps | grep mcpo

# View logs
docker logs mcpo-server

# Test health
docker inspect --format='{{.State.Health.Status}}' mcpo-server
```

## Test Environment

- Python: 3.12.3
- pytest: 8.3.5
- Docker: Latest
- OS: Linux 5.15
- FastAPI: 0.115.12
- uvicorn: 0.34.0
