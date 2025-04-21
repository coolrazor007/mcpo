# MCP Memory Tool

## Building the Docker Image

Build the memory tool Docker image with:

```bash
docker build -t mcp-memory ./src/mcpo/mcp_servers/memory --no-cache
```

This will create a fresh `mcp-memory` image for use in your MCP system.

## Usage

This tool is now a one-shot CLI utility. It is intended to be run by the MCP orchestrator, which will pass the appropriate arguments for saving or retrieving memories.

Environment variables for Weaviate and Ollama configuration must be set as shown in your system's configuration.
