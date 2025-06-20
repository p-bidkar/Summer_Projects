"""
MCP Tools Implementation
Contains various tools that the MCP server can provide to clients.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional


class CalculatorTool:
    """Simple calculator tool for basic arithmetic operations."""
    
    @staticmethod
    def add(a: float, b: float) -> Dict[str, Any]:
        """Add two numbers."""
        result = a + b
        return {
            "operation": "addition",
            "operands": [a, b],
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def subtract(a: float, b: float) -> Dict[str, Any]:
        """Subtract two numbers."""
        result = a - b
        return {
            "operation": "subtraction",
            "operands": [a, b],
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def multiply(a: float, b: float) -> Dict[str, Any]:
        """Multiply two numbers."""
        result = a * b
        return {
            "operation": "multiplication",
            "operands": [a, b],
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def divide(a: float, b: float) -> Dict[str, Any]:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        return {
            "operation": "division",
            "operands": [a, b],
            "result": result,
            "timestamp": datetime.now().isoformat()
        }


class WeatherTool:
    """Mock weather tool for demonstration purposes."""
    
    @staticmethod
    def get_weather(city: str) -> Dict[str, Any]:
        """Get weather information for a city (mock data)."""
        # Mock weather data
        weather_data = {
            "New York": {"temperature": 22, "condition": "Sunny", "humidity": 65},
            "London": {"temperature": 15, "condition": "Cloudy", "humidity": 80},
            "Tokyo": {"temperature": 25, "condition": "Rainy", "humidity": 75},
            "Sydney": {"temperature": 28, "condition": "Clear", "humidity": 60}
        }
        
        if city in weather_data:
            return {
                "city": city,
                "weather": weather_data[city],
                "timestamp": datetime.now().isoformat(),
                "source": "mock_data"
            }
        else:
            return {
                "city": city,
                "weather": {"temperature": 20, "condition": "Unknown", "humidity": 50},
                "timestamp": datetime.now().isoformat(),
                "source": "mock_data",
                "note": "City not found, returning default data"
            }


class FileTool:
    """File operations tool."""
    
    @staticmethod
    def read_file(filepath: str) -> Dict[str, Any]:
        """Read contents of a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                return {
                    "filepath": filepath,
                    "content": content,
                    "size": len(content),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                }
        except FileNotFoundError:
            return {
                "filepath": filepath,
                "error": "File not found",
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
        except Exception as e:
            return {
                "filepath": filepath,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    @staticmethod
    def write_file(filepath: str, content: str) -> Dict[str, Any]:
        """Write content to a file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
                return {
                    "filepath": filepath,
                    "content_length": len(content),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                }
        except Exception as e:
            return {
                "filepath": filepath,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    @staticmethod
    def list_files(directory: str = ".") -> Dict[str, Any]:
        """List files in a directory."""
        try:
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                files.append({
                    "name": item,
                    "is_directory": os.path.isdir(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None
                })
            
            return {
                "directory": directory,
                "files": files,
                "count": len(files),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "directory": directory,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }


class SystemTool:
    """System information tool."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get basic system information."""
        return {
            "platform": os.name,
            "current_directory": os.getcwd(),
            "timestamp": datetime.now().isoformat(),
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
        }
    
    @staticmethod
    def echo(message: str) -> Dict[str, Any]:
        """Echo a message back."""
        return {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "status": "echoed"
        }


# Tool registry
TOOL_REGISTRY = {
    "calculator": CalculatorTool,
    "weather": WeatherTool,
    "file": FileTool,
    "system": SystemTool
} 