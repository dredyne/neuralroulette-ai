"""WebSocket Client for Pragmatic Play Live Casino
Handles real-time data connection to roulette tables
"""

import asyncio
import json
import websockets
import logging
from datetime import datetime

class RouletteWebSocketClient:
    """WebSocket client for connecting to live roulette data"""
    
    def __init__(self, ws_url, casino_id, table_id, currency="USD"):
        self.ws_url = ws_url
        self.casino_id = casino_id
        self.table_id = table_id
        self.currency = currency
        self.connected = False
        self.websocket = None
        self.callbacks = []
        self.logger = logging.getLogger("roulette_websocket")
        
    def register_callback(self, callback):
        """Register a callback function to receive roulette numbers"""
        self.callbacks.append(callback)
        
    async def connect(self):
        """Establish WebSocket connection"""
        try:
            self.websocket = await websockets.connect(self.ws_url)
            self.connected = True
            # self.logger.info(f"Connected to WebSocket at {self.ws_url}")
            
            # Send initial connection message
            await self.send_connection_message()
            
            # Start the ping loop in the background
            asyncio.create_task(self.start_ping())
            
            return True
        except Exception as e:
            self.logger.error(f"WebSocket connection error: {str(e)}")
            return False
    
    async def send_connection_message(self):
        """Send initial connection message to the server"""
        # Send the subscription message
        connection_msg = {
            "type": "subscribe",
            "isDeltaEnabled": True,
            "casinoId": self.casino_id,
            "key": [self.table_id],
            "currency": self.currency
        }
        # self.logger.info(f"Sending connection message: {connection_msg}")
        await self.websocket.send(json.dumps(connection_msg))
        
    async def start_ping(self):
        """Start sending ping messages every 5 minutes"""
        try:
            while self.connected:
                ping_msg = {
                    "type": "ping",
                    "pingTime": int(datetime.now().timestamp() * 1000)
                }
                await self.websocket.send(json.dumps(ping_msg))
                await asyncio.sleep(300)  # 5 minutes
        except Exception as e:
            self.logger.error(f"Error in ping loop: {str(e)}")
            self.connected = False
    
    async def listen(self):
        """Listen for incoming messages with automatic reconnection"""
        while True:  # Infinite loop for reconnection
            if not self.connected:
                # self.logger.error("WebSocket not connected - Attempting to connect...")
                if not await self.connect():
                    self.logger.error("Connection failed - Retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                
            try:
                self.logger.info("Listening for roulette spins...")
                while self.connected:
                    try:
                        message = await self.websocket.recv()
                        await self.process_message(message)
                    except websockets.exceptions.ConnectionClosed:
                        self.logger.error("Connection lost - Attempting to reconnect...")
                        self.connected = False
                        break
                    except Exception as e:
                        self.logger.error(f"Error processing message: {str(e)}")
            except Exception as e:
                self.logger.error(f"Fatal error in WebSocket listener: {str(e)}")
                self.connected = False
            
            # Wait before attempting to reconnect
            await asyncio.sleep(60)
    
    async def process_message(self, message):
        """Process incoming WebSocket messages"""
        try:
            # Log the raw message for debugging
            # self.logger.info(f"Received raw message: {message[:200]}..." if len(message) > 200 else f"Received raw message: {message}")
            
            data = json.loads(message)
            
            # Log the parsed data structure
            # self.logger.info(f"Message keys: {list(data.keys())}")
            
            # Check if this is a roulette result message in the format provided
            # Format: {"tableId":"236","last20Results":[{"time":"Aug 16, 2025 08:19:15 PM","result":"16","color":"red",...}]}
            if "tableId" in data and "last20Results" in data and len(data["last20Results"]) > 0:
                # Get the most recent result (first in the list)
                latest_result = data["last20Results"][0]
                # self.logger.info(f"Latest result: {latest_result}")
                
                if "result" in latest_result:
                    try:
                        roulette_number = int(latest_result["result"])
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # self.logger.info(f"Received roulette number: {roulette_number}")
                        
                        # Call all registered callbacks with the new number
                        for callback in self.callbacks:
                            await callback(roulette_number)
                            
                        # Log the number to file
                        # with open("roulette_log.txt", "a") as log_file:
                        #     log_file.write(f"{timestamp}: {roulette_number}\n")
                    except ValueError:
                        self.logger.error(f"Invalid roulette number format: {latest_result['result']}")
            # Fallback to the original format
            elif "result" in data and "number" in data["result"]:
                roulette_number = int(data["result"]["number"])
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # self.logger.info(f"Received roulette number: {roulette_number}")
                
                # Call all registered callbacks with the new number
                for callback in self.callbacks:
                    await callback(roulette_number)
                    
                # Log the number to file
                # with open("roulette_log.txt", "a") as log_file:
                #     log_file.write(f"{timestamp}: {roulette_number}\n")
            # else:
                # self.logger.info(f"Unrecognized message format, no roulette number found")
                    
        except json.JSONDecodeError:
            self.logger.error(f"Failed to decode JSON message: {message}")
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            self.logger.error(f"Message that caused error: {message[:200]}..." if len(message) > 200 else f"Message that caused error: {message}")
    
    async def disconnect(self):
        """Close the WebSocket connection"""
        if self.connected and self.websocket:
            await self.websocket.close()
            self.connected = False
            # self.logger.info("WebSocket connection closed")

    async def simulate_data(self):
        """Simulate roulette data for testing purposes"""
        import random
        
        self.connected = True
        self.logger.info("Starting roulette data simulation")
        
        try:
            while self.connected:
                # Generate random roulette number (0-36)
                roulette_number = random.randint(0, 36)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_time = datetime.now().strftime("%b %d, %Y %I:%M:%S %p")
                
                # Create a simulated message in the same format as the real WebSocket
                color = "red" if roulette_number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else \
                       "black" if roulette_number in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35] else "green"
                
                simulated_message = {
                    "tableId": str(self.table_id),
                    "last20Results": [
                        {
                            "time": formatted_time,
                            "result": str(roulette_number),
                            "color": color,
                            "gameId": f"sim{int(datetime.now().timestamp())}"
                        }
                    ]
                }
                
                self.logger.info(f"Simulated roulette number: {roulette_number}")
                
                # Process the simulated message
                await self.process_message(json.dumps(simulated_message))
                
                # Wait before generating next number (simulate real casino timing)
                await asyncio.sleep(5)  # 5 seconds between spins
                
        except Exception as e:
            self.logger.error(f"Error in simulation: {str(e)}")
            self.connected = False