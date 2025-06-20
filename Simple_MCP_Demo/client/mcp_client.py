"""
MCP Client Implementation
A simple Model Context Protocol client that connects to MCP servers.
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPClient:
    """Simple MCP Client implementation."""
    
    def __init__(self, server_host: str = None, server_port: int = 8080):
        # Allow overriding server_host with an environment variable for Docker
        self.server_host = server_host or os.environ.get("MCP_SERVER_HOST", "localhost")
        self.server_port = server_port
        self.request_id = 0
        self.connected = False
        self.available_tools = []
        self.server_info = {}
    
    def _get_next_request_id(self) -> int:
        """Get the next request ID."""
        self.request_id += 1
        return self.request_id
    
    def _create_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a JSON-RPC request."""
        return {
            "jsonrpc": "2.0",
            "id": self._get_next_request_id(),
            "method": method,
            "params": params or {}
        }
    
    async def connect(self) -> bool:
        """Connect to the MCP server."""
        try:
            print(f"{Fore.CYAN}Connecting to MCP Server at {self.server_host}:{self.server_port}...{Style.RESET_ALL}")
            
            # For demonstration, we'll simulate a connection
            # In a real implementation, you would establish a WebSocket or TCP connection
            
            # Simulate connection delay
            await asyncio.sleep(1)
            
            # Initialize the connection
            init_request = self._create_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "Simple MCP Client",
                    "version": "1.0.0"
                }
            })
            
            # Simulate server response
            init_response = await self._simulate_server_request(init_request)
            
            if "error" in init_response:
                print(f"{Fore.RED}Failed to initialize connection: {init_response['error']}{Style.RESET_ALL}")
                return False
            
            self.server_info = init_response.get("result", {}).get("serverInfo", {})
            self.connected = True
            
            print(f"{Fore.GREEN}✓ Successfully connected to MCP Server{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Server: {self.server_info.get('name', 'Unknown')} v{self.server_info.get('version', 'Unknown')}{Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Connection failed: {e}{Style.RESET_ALL}")
            return False
    
    async def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from the server."""
        if not self.connected:
            print(f"{Fore.RED}Not connected to server{Style.RESET_ALL}")
            return []
        
        try:
            print(f"{Fore.CYAN}Discovering available tools...{Style.RESET_ALL}")
            
            request = self._create_request("tools/list")
            response = await self._simulate_server_request(request)
            
            if "error" in response:
                print(f"{Fore.RED}Failed to discover tools: {response['error']}{Style.RESET_ALL}")
                return []
            
            tools = response.get("result", {}).get("tools", [])
            self.available_tools = tools
            
            print(f"{Fore.GREEN}✓ Found {len(tools)} available tools{Style.RESET_ALL}")
            
            return tools
            
        except Exception as e:
            print(f"{Fore.RED}Tool discovery failed: {e}{Style.RESET_ALL}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the server."""
        if not self.connected:
            print(f"{Fore.RED}Not connected to server{Style.RESET_ALL}")
            return {}
        
        try:
            print(f"{Fore.CYAN}Calling tool: {tool_name}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Arguments: {json.dumps(arguments, indent=2)}{Style.RESET_ALL}")
            
            request = self._create_request("tools/call", {
                "name": tool_name,
                "arguments": arguments
            })
            
            response = await self._simulate_server_request(request)
            
            if "error" in response:
                print(f"{Fore.RED}Tool call failed: {response['error']}{Style.RESET_ALL}")
                return {}
            
            result = response.get("result", {})
            content = result.get("content", [])
            
            if content:
                tool_result = json.loads(content[0].get("text", "{}"))
                print(f"{Fore.GREEN}✓ Tool executed successfully{Style.RESET_ALL}")
                return tool_result
            else:
                print(f"{Fore.YELLOW}No content returned from tool{Style.RESET_ALL}")
                return {}
                
        except Exception as e:
            print(f"{Fore.RED}Tool call failed: {e}{Style.RESET_ALL}")
            return {}
    
    async def _simulate_server_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a server request (for demonstration purposes)."""
        # In a real implementation, this would send the request over WebSocket or TCP
        # For now, we'll simulate the server processing
        
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        # Simulate server responses based on method
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "Simple MCP Server",
                        "version": "1.0.0",
                        "description": "A demonstration MCP server with various tools"
                    }
                }
            }
        
        elif method == "tools/list":
            # Return mock tool list
            tools = [
                {
                    "name": "calculator.add",
                    "description": "Add two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "weather.get_weather",
                    "description": "Get weather information for a city",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string"}
                        },
                        "required": ["city"]
                    }
                },
                {
                    "name": "system.echo",
                    "description": "Echo a message back",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"}
                        },
                        "required": ["message"]
                    }
                }
            ]
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": tools}
            }
        
        elif method == "tools/call":
            # Simulate tool execution
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            # Mock tool results
            if tool_name == "calculator.add":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = {
                    "operation": "addition",
                    "operands": [a, b],
                    "result": a + b,
                    "timestamp": datetime.now().isoformat()
                }
            elif tool_name == "weather.get_weather":
                city = arguments.get("city", "Unknown")
                result = {
                    "city": city,
                    "weather": {
                        "temperature": 22,
                        "condition": "Sunny",
                        "humidity": 65
                    },
                    "timestamp": datetime.now().isoformat(),
                    "source": "mock_data"
                }
            elif tool_name == "system.echo":
                message = arguments.get("message", "")
                result = {
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "status": "echoed"
                }
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def display_tools(self):
        """Display available tools in a formatted way."""
        if not self.available_tools:
            print(f"{Fore.YELLOW}No tools available. Run discover_tools() first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Available Tools:{Style.RESET_ALL}")
        print("=" * 50)
        
        for i, tool in enumerate(self.available_tools, 1):
            print(f"{Fore.GREEN}{i}. {tool['name']}{Style.RESET_ALL}")
            print(f"   Description: {tool['description']}")
            
            # Display parameters if available
            schema = tool.get('inputSchema', {})
            properties = schema.get('properties', {})
            required = schema.get('required', [])
            
            if properties:
                print(f"   Parameters:")
                for param_name, param_info in properties.items():
                    param_type = param_info.get('type', 'unknown')
                    required_mark = " *" if param_name in required else ""
                    print(f"     - {param_name} ({param_type}){required_mark}")
            
            print()
    
    def disconnect(self):
        """Disconnect from the server."""
        self.connected = False
        print(f"{Fore.YELLOW}Disconnected from MCP Server{Style.RESET_ALL}")


async def main():
    """Main function to run the MCP client."""
    client = MCPClient()
    
    # Connect to server
    if await client.connect():
        # Discover tools
        await client.discover_tools()
        
        # Display tools
        client.display_tools()
        
        # Example tool calls
        print(f"{Fore.CYAN}Running example tool calls...{Style.RESET_ALL}")
        
        # Calculator example
        result = await client.call_tool("calculator.add", {"a": 10, "b": 5})
        print(f"{Fore.GREEN}Calculator Result:{Style.RESET_ALL}")
        print(json.dumps(result, indent=2))
        
        # Weather example
        result = await client.call_tool("weather.get_weather", {"city": "New York"})
        print(f"\n{Fore.GREEN}Weather Result:{Style.RESET_ALL}")
        print(json.dumps(result, indent=2))
        
        # Echo example
        result = await client.call_tool("system.echo", {"message": "Hello MCP!"})
        print(f"\n{Fore.GREEN}Echo Result:{Style.RESET_ALL}")
        print(json.dumps(result, indent=2))
        
        # Disconnect
        client.disconnect()


if __name__ == "__main__":
    asyncio.run(main()) 