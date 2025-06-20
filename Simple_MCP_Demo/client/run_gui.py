#!/usr/bin/env python3
"""
GUI Launcher Script
Simple script to launch the MCP Weather GUI application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui_weather import main
    
    print("Starting MCP Weather GUI...")
    print("Make sure the MCP server is running first!")
    print("To start the server: cd ../server && python mcp_server.py")
    print("-" * 50)
    
    main()
    
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you have installed all requirements:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"Error starting GUI: {e}")
    print("Please check that the MCP server is running.") 