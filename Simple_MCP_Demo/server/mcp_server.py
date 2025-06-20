"""
MCP Server Implementation
A simple Model Context Protocol server that provides various tools to clients.
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from tools import TOOL_REGISTRY, CalculatorTool, WeatherTool, FileTool, SystemTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServer:
    """Simple MCP Server implementation."""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.clients = []
        self.tools = self._register_tools()
        self.server_info = {
            "name": "Simple MCP Server",
            "version": "1.0.0",
            "description": "A demonstration MCP server with various tools",
            "capabilities": ["tools", "resources"]
        }
    
    def _register_tools(self) -> Dict[str, Dict[str, Any]]:
        """Register available tools with their metadata."""
        return {
            "calculator.add": {
                "name": "calculator.add",
                "description": "Add two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                },
                "tool": CalculatorTool.add
            },
            "calculator.subtract": {
                "name": "calculator.subtract",
                "description": "Subtract two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                },
                "tool": CalculatorTool.subtract
            },
            "calculator.multiply": {
                "name": "calculator.multiply",
                "description": "Multiply two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                },
                "tool": CalculatorTool.multiply
            },
            "calculator.divide": {
                "name": "calculator.divide",
                "description": "Divide two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                },
                "tool": CalculatorTool.divide
            },
            "weather.get_weather": {
                "name": "weather.get_weather",
                "description": "Get weather information for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"}
                    },
                    "required": ["city"]
                },
                "tool": WeatherTool.get_weather
            },
            "file.read_file": {
                "name": "file.read_file",
                "description": "Read contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Path to the file"}
                    },
                    "required": ["filepath"]
                },
                "tool": FileTool.read_file
            },
            "file.write_file": {
                "name": "file.write_file",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Path to the file"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["filepath", "content"]
                },
                "tool": FileTool.write_file
            },
            "file.list_files": {
                "name": "file.list_files",
                "description": "List files in a directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {"type": "string", "description": "Directory path", "default": "."}
                    }
                },
                "tool": FileTool.list_files
            },
            "system.get_system_info": {
                "name": "system.get_system_info",
                "description": "Get basic system information",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "tool": SystemTool.get_system_info
            },
            "system.echo": {
                "name": "system.echo",
                "description": "Echo a message back",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Message to echo"}
                    },
                    "required": ["message"]
                },
                "tool": SystemTool.echo
            }
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC requests."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        logger.info(f"Received request: {method}")
        
        try:
            if method == "initialize":
                response = await self._handle_initialize(params)
            elif method == "tools/list":
                response = await self._handle_list_tools(params)
            elif method == "tools/call":
                response = await self._handle_call_tool(params)
            elif method == "ping":
                response = {"pong": True}
            else:
                response = {"error": f"Unknown method: {method}"}
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": response
            }
            
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        logger.info("Client initialized")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": self.server_info
        }
    
    async def _handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools listing request."""
        tools_list = []
        for tool_name, tool_info in self.tools.items():
            tools_list.append({
                "name": tool_info["name"],
                "description": tool_info["description"],
                "inputSchema": tool_info["parameters"]
            })
        
        return {"tools": tools_list}
    
    async def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        
        tool_info = self.tools[tool_name]
        tool_func = tool_info["tool"]
        
        # Execute the tool
        if tool_name == "file.list_files":
            result = tool_func(arguments.get("directory", "."))
        else:
            result = tool_func(**arguments)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }
    
    async def start_server(self):
        """Start the MCP server."""
        logger.info(f"Starting MCP Server on {self.host}:{self.port}")
        
        # For demonstration, we'll create a simple server that accepts connections
        # In a real implementation, you might use asyncio.start_server or similar
        
        print("=" * 50)
        print("MCP Server Started Successfully!")
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        print("Available Tools:")
        for tool_name in self.tools.keys():
            print(f"  - {tool_name}")
        print("=" * 50)
        print("Server is ready to accept connections...")
        print("Press Ctrl+C to stop the server")
        
        try:
            # Keep the server running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
    
    def get_tools_info(self) -> Dict[str, Any]:
        """Get information about available tools."""
        return {
            "total_tools": len(self.tools),
            "tools": list(self.tools.keys()),
            "categories": {
                "calculator": ["add", "subtract", "multiply", "divide"],
                "weather": ["get_weather"],
                "file": ["read_file", "write_file", "list_files"],
                "system": ["get_system_info", "echo"]
            }
        }


async def main():
    """Main function to run the MCP server."""
    server = MCPServer()
    await server.start_server()


if __name__ == "__main__":
    asyncio.run(main()) 