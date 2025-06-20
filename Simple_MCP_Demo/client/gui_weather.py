"""
Weather GUI Application
A simple GUI for the MCP weather tool that allows users to input a city and view weather information.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import asyncio
import threading
from datetime import datetime
from mcp_client import MCPClient
import os


class WeatherGUI:
    """Simple GUI for weather information using MCP client."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MCP Weather App")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # MCP Client
        server_host = os.environ.get("MCP_SERVER_HOST", "localhost")
        self.client = MCPClient(server_host=server_host)
        self.connected = False
        
        # Create GUI elements
        self.create_widgets()
        
        # Connect to server in background
        self.connect_to_server()
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🌤️ MCP Weather App", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Connection status
        self.status_label = ttk.Label(main_frame, text="Connecting to MCP Server...", 
                                     foreground='orange')
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # City input frame
        input_frame = ttk.LabelFrame(main_frame, text="Enter City Name", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)
        
        # City label and entry
        ttk.Label(input_frame, text="City:").grid(row=0, column=0, padx=(0, 10))
        self.city_entry = ttk.Entry(input_frame, width=30)
        self.city_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.city_entry.insert(0, "New York")  # Default city
        
        # Get weather button
        self.weather_button = ttk.Button(input_frame, text="Get Weather", 
                                        command=self.get_weather, state='disabled')
        self.weather_button.grid(row=0, column=2)
        
        # Bind Enter key to get weather
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        # Weather display frame
        weather_frame = ttk.LabelFrame(main_frame, text="Weather Information", padding="10")
        weather_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        weather_frame.columnconfigure(0, weight=1)
        weather_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Weather text area
        self.weather_text = tk.Text(weather_frame, height=15, width=60, 
                                   wrap=tk.WORD, state='disabled')
        weather_scrollbar = ttk.Scrollbar(weather_frame, orient='vertical', 
                                         command=self.weather_text.yview)
        self.weather_text.configure(yscrollcommand=weather_scrollbar.set)
        
        self.weather_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        weather_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Clear button
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_display)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_button = ttk.Button(button_frame, text="Refresh Connection", 
                                   command=self.refresh_connection)
        refresh_button.pack(side=tk.LEFT)
        
        # Example cities
        example_frame = ttk.LabelFrame(main_frame, text="Example Cities", padding="5")
        example_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        example_cities = ["New York", "London", "Tokyo", "Sydney", "Paris", "Berlin"]
        for i, city in enumerate(example_cities):
            btn = ttk.Button(example_frame, text=city, 
                           command=lambda c=city: self.set_city(c))
            btn.grid(row=0, column=i, padx=2)
    
    def connect_to_server(self):
        """Connect to MCP server in background thread."""
        def connect():
            try:
                # Run the async connection in the background
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                self.connected = loop.run_until_complete(self.client.connect())
                
                # Update GUI in main thread
                self.root.after(0, self.update_connection_status)
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Connection failed: {e}"))
        
        # Run connection in background thread
        thread = threading.Thread(target=connect, daemon=True)
        thread.start()
    
    def update_connection_status(self):
        """Update the connection status display."""
        if self.connected:
            self.status_label.config(text="✅ Connected to MCP Server", foreground='green')
            self.weather_button.config(state='normal')
        else:
            self.status_label.config(text="❌ Failed to connect to MCP Server", foreground='red')
            self.weather_button.config(state='disabled')
    
    def get_weather(self):
        """Get weather information for the entered city."""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        
        # Disable button during request
        self.weather_button.config(state='disabled')
        self.status_label.config(text="Fetching weather data...", foreground='blue')
        
        # Run weather request in background
        def fetch_weather():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                result = loop.run_until_complete(self.client.call_tool("weather.get_weather", {"city": city}))
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.display_weather(result))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Weather request failed: {e}"))
            finally:
                # Re-enable button
                self.root.after(0, lambda: self.weather_button.config(state='normal'))
                self.root.after(0, lambda: self.status_label.config(text="✅ Connected to MCP Server", foreground='green'))
        
        thread = threading.Thread(target=fetch_weather, daemon=True)
        thread.start()
    
    def display_weather(self, weather_data):
        """Display weather information in the text area."""
        self.weather_text.config(state='normal')
        self.weather_text.delete(1.0, tk.END)
        
        if not weather_data:
            self.weather_text.insert(tk.END, "No weather data received.")
            self.weather_text.config(state='disabled')
            return
        
        # Format weather data
        city = weather_data.get('city', 'Unknown')
        weather = weather_data.get('weather', {})
        timestamp = weather_data.get('timestamp', '')
        
        # Create formatted display
        display_text = f"""
🌍 WEATHER REPORT FOR {city.upper()}
{'=' * 50}

📅 Date/Time: {timestamp}

🌡️  Temperature: {weather.get('temperature', 'N/A')}°C
☁️  Condition: {weather.get('condition', 'N/A')}
💧 Humidity: {weather.get('humidity', 'N/A')}%

{'=' * 50}

📊 Raw Data:
{json.dumps(weather_data, indent=2)}

{'=' * 50}
Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.weather_text.insert(tk.END, display_text)
        self.weather_text.config(state='disabled')
        
        # Scroll to top
        self.weather_text.see(1.0)
    
    def set_city(self, city):
        """Set the city in the entry field."""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
    
    def clear_display(self):
        """Clear the weather display."""
        self.weather_text.config(state='normal')
        self.weather_text.delete(1.0, tk.END)
        self.weather_text.config(state='disabled')
    
    def refresh_connection(self):
        """Refresh the connection to the server."""
        self.status_label.config(text="Reconnecting to MCP Server...", foreground='orange')
        self.weather_button.config(state='disabled')
        self.connect_to_server()
    
    def show_error(self, message):
        """Show error message."""
        messagebox.showerror("Error", message)
        self.status_label.config(text="❌ Connection Error", foreground='red')
        self.weather_button.config(state='disabled')


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = WeatherGUI(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main() 