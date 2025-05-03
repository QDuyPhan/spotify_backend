import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SongPlayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to socket"}))

    async def disconnect(self, close_code):
        print(f"Disconnected: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received from client:", data)

        # Broadcast message to all (echo for now)
        await self.send(text_data=json.dumps({
            "message": f"You sent: {data.get('message')}"
        }))
