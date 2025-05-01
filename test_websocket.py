#!/usr/bin/env python3
import asyncio
import websockets
import sys


async def test_websocket():
    uri = "ws://localhost:8000/ws/deaths"
    try:
        print(f"Attempting to connect to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server!")
            print("Waiting for messages (press Ctrl+C to exit)...")

            async def heartbeat():
                while True:
                    try:
                        await websocket.ping()
                        await asyncio.sleep(5)
                    except:
                        break

            heartbeat_task = asyncio.create_task(heartbeat())

            # Receive and print messages
            try:
                while True:
                    message = await websocket.recv()
                    print(f"Received message: {message}")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")
            except KeyboardInterrupt:
                print("Exiting...")
            finally:
                heartbeat_task.cancel()

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Error: Invalid status code: {e}")
        print(f"The server returned status code: {e.status_code}")
        if e.status_code == 403:
            print(
                "This might be due to server-side authorization or CORS restrictions."
            )
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Error: Connection closed: {e}")
    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(test_websocket())
    except KeyboardInterrupt:
        print("Script interrupted by user")
        sys.exit(0)
