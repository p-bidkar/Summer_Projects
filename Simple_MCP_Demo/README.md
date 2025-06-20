# Simple MCP Demo Project

This project demonstrates the Model Context Protocol (MCP) with a simple server, client, and workflow.

## Project Structure

```
Simple_MCP_Demo/
├── server/                 # MCP Server implementation
│   ├── mcp_server.py      # Main server with tools
│   ├── tools.py           # Tool implementations
│   └── requirements.txt   # Server dependencies
├── client/                # MCP Client implementation
│   ├── mcp_client.py     # Main client
│   ├── workflow_demo.py  # Demo workflow
│   └── requirements.txt  # Client dependencies
├── config/               # Configuration files
│   └── server_config.json
├── examples/             # Example usage
│   └── demo_workflow.py
└── README.md            # This file
```

## What is MCP?

The Model Context Protocol (MCP) is a protocol that allows AI assistants to connect to external data sources and tools. It enables:
- Secure access to external data
- Tool execution capabilities
- Structured communication between AI and external systems

## Quick Start

### 1. Setup Server
```bash
cd server
pip install -r requirements.txt
python mcp_server.py
```

### 2. Setup Client
```bash
cd client
pip install -r requirements.txt
python workflow_demo.py
```

## Features

- **Simple Calculator Tool**: Basic arithmetic operations
- **Weather Tool**: Mock weather data retrieval
- **File Operations**: Read/write file operations
- **Workflow Demo**: Step-by-step MCP communication demonstration

## Workflow

1. Server starts and registers tools
2. Client connects to server
3. Client discovers available tools
4. Client executes tools and processes results
5. Results are displayed with clear formatting

## Requirements

- Python 3.8+
- asyncio
- json-rpc
- websockets (for future WebSocket support) 