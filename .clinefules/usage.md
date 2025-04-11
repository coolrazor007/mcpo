# MCPO Usage Guide

This guide demonstrates how to interact with the MCPO server using various clients and programming languages.

## Authentication

All examples use the following API key:
```
API_KEY=top-secret
```

## 1. cURL Examples

### Get Current Time (Time Server)
```bash
curl -X POST http://localhost:8000/time/get_current_time \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer top-secret" \
  -d '{"timezone": "America/Los_Angeles"}'
```

### Create Memory Entity
```bash
curl -X POST http://localhost:8000/memory/create_entities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer top-secret" \
  -d '{
    "entities": [
      {
        "name": "test_entity",
        "entityType": "test",
        "observations": ["This is a test observation"]
      }
    ]
  }'
```

## 2. Python Examples

### Using requests Library
```python
import requests

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": "Bearer top-secret",
    "Content-Type": "application/json"
}

# Get current time
def get_current_time(timezone="America/Los_Angeles"):
    response = requests.post(
        f"{BASE_URL}/time/get_current_time",
        headers=HEADERS,
        json={"timezone": timezone}
    )
    return response.json()

# Create memory entity
def create_memory_entity(name, entity_type, observations):
    response = requests.post(
        f"{BASE_URL}/memory/create_entities",
        headers=HEADERS,
        json={
            "entities": [
                {
                    "name": name,
                    "entityType": entity_type,
                    "observations": observations
                }
            ]
        }
    )
    return response.json()

# Example usage:
if __name__ == "__main__":
    # Get current time
    time_result = get_current_time()
    print("Current time:", time_result)

    # Create memory entity
    memory_result = create_memory_entity(
        "test_entity",
        "test",
        ["This is a test observation"]
    )
    print("Memory entity:", memory_result)
```

## 3. JavaScript/Node.js Examples

### Using fetch API
```javascript
const BASE_URL = 'http://localhost:8000';
const HEADERS = {
  'Authorization': 'Bearer top-secret',
  'Content-Type': 'application/json'
};

// Get current time
async function getCurrentTime(timezone = 'America/Los_Angeles') {
  const response = await fetch(`${BASE_URL}/time/get_current_time`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify({ timezone })
  });
  return await response.json();
}

// Create memory entity
async function createMemoryEntity(name, entityType, observations) {
  const response = await fetch(`${BASE_URL}/memory/create_entities`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify({
      entities: [
        {
          name,
          entityType,
          observations
        }
      ]
    })
  });
  return await response.json();
}

// Example usage:
async function main() {
  try {
    // Get current time
    const timeResult = await getCurrentTime();
    console.log('Current time:', timeResult);

    // Create memory entity
    const memoryResult = await createMemoryEntity(
      'test_entity',
      'test',
      ['This is a test observation']
    );
    console.log('Memory entity:', memoryResult);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

## 4. Fetch MCP Server Examples

### Using fetch tool
```javascript
// Example using fetch MCP server
async function fetchExample() {
  const response = await fetch('http://example.com/api/data', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  return await response.json();
}
```

## Testing Examples

Let's verify these examples work:

### 1. Test Time Server
```bash
# Test command
curl -X POST http://localhost:8000/time/get_current_time \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer top-secret" \
  -d '{"timezone": "America/Los_Angeles"}'
```

### 2. Test Memory Server
```bash
# Test command
curl -X POST http://localhost:8000/memory/create_entities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer top-secret" \
  -d '{
    "entities": [
      {
        "name": "test_entity",
        "entityType": "test",
        "observations": ["This is a test observation"]
      }
    ]
  }'
```

Let's test these examples to ensure they work correctly.
