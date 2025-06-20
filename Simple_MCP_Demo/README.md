# Simple MCP Demo Project

This project demonstrates the Model Context Protocol (MCP) with a simple server, client, and workflow.

## Project Structure

```
Simple_MCP_Demo/
├── assets/                 # Contains application assets
│   └── gui_screenshot.png # Screenshot of the GUI
├── server/                 # MCP Server implementation
│   ├── mcp_server.py      # Main server with tools
│   ├── tools.py           # Tool implementations
│   └── requirements.txt   # Server dependencies
├── client/                # MCP Client implementation
│   ├── mcp_client.py     # Main client
│   ├── gui_weather.py    # GUI weather application
│   ├── run_gui.py        # GUI launcher script
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

### 2. Setup Client (Command Line)
```bash
cd client
pip install -r requirements.txt
python mcp_client.py
```

### 3. Setup Client (GUI)
```bash
cd client
pip install -r requirements.txt
python run_gui.py
```

## Features

- **Simple Calculator Tool**: Basic arithmetic operations
- **Weather Tool**: Mock weather data retrieval
- **File Operations**: Read/write file operations
- **System Information**: System details and echo functionality
- **GUI Weather App**: User-friendly interface for weather queries
- **Workflow Demo**: Step-by-step MCP communication demonstration

## GUI Weather Application

The GUI application provides a user-friendly interface for weather queries:

### Screenshot
![MCP Weather App Screenshot](assets/gui_screenshot.png)

### Features:
- **City Input**: Enter any city name to get weather information
- **Quick City Buttons**: Pre-defined buttons for popular cities
- **Real-time Connection Status**: Shows connection to MCP server
- **Formatted Weather Display**: Beautiful presentation of weather data
- **Error Handling**: Graceful error messages and recovery

### How to Use:
1. Start the MCP server first
2. Run the GUI application: `python run_gui.py`
3. Enter a city name or click on example city buttons
4. Click "Get Weather" or press Enter
5. View the formatted weather information

### GUI Components:
- **Connection Status**: Shows if connected to MCP server
- **City Input Field**: Type city name here
- **Get Weather Button**: Fetch weather data
- **Weather Display**: Shows formatted weather information
- **Example Cities**: Quick buttons for popular cities
- **Control Buttons**: Clear display and refresh connection

## Workflow

1. Server starts and registers tools
2. Client connects to server (CLI or GUI)
3. Client discovers available tools
4. Client executes tools and processes results
5. Results are displayed with clear formatting

## Requirements

- Python 3.8+
- asyncio
- json-rpc
- websockets (for future WebSocket support)
- tkinter (included with Python standard library)
- colorama (for colored terminal output) 