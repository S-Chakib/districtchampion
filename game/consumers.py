from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .game import game
import json

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f"game_{self.match_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received data: {data}")  # Debugging line

        card_id         = data.get("card_id")
        team            = data.get("team")
        target_players  = data.get("targets", [])

        # Ensure card_id and team are valid
        if not card_id or not team:
            print("❌ Invalid data received: Missing card_id or team")
            return

        # Process the game logic asynchronously
        process = await sync_to_async(game)(card_id, target_players)

        if process:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "remove_points_effect", 
                    "points": 10,
                }
            )

    async def remove_points_effect(self, event):
        await super().send(text_data=json.dumps({
            "action": "remove_points",
            "points": event["points"]
        }))
