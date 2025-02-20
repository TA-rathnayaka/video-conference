import asyncio
import websockets
import json

connected_clients = set()

async def signaling_server(websocket, path):
    # Register client
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received message: {data}")

            # Broadcast the message to all connected clients except the sender
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(signaling_server, "0.0.0.0", 8765):
        print("Signaling server listening on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())