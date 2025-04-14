# Fetch MCP Server

## Overview
The Fetch MCP server provides HTTP request functionality through a standardized interface. It is implemented using the official MCP fetch server from the modelcontextprotocol/servers repository.

## Implementation Details
- Source: https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
- Uses Docker-in-Docker (dind) to run the official MCP fetch server container
- Container is pulled automatically when needed

## Configuration
```json
{
  "mcpServers": {
    "fetch": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/fetch"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

The configuration uses Docker to run the fetch server:
- `run`: Creates a new container
- `-i`: Keeps STDIN open for interactive use
- `--rm`: Automatically removes the container when it exits
- `mcp/fetch`: The official MCP fetch server image

## Testing
To test the fetch MCP server functionality:

```bash
# Test basic GET request
curl -X POST http://localhost:8000/fetch/fetch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer top-secret" \
  -d '{
    "url": "https://api.example.com/data",
    "method": "GET",
    "headers": {
      "Accept": "application/json"
    }
  }'
```

## Status
- [x] Added Docker-based configuration to config.json
- [x] Ready for use (will auto-pull image when needed)
