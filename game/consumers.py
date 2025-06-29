from channels.generic.websocket import AsyncWebsocketConsumer
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
        card = data.get("card")
        team = data.get("team")

        # Ensure card is a dict, not None
        if not isinstance(card, dict) or not team:
            return

        process = game(card, team)  # Your game logic function

        if process:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "remove_points_effect",  # triggers method below
                    "points": 10,
                }
            )


    async def remove_points_effect(self, event):
        await super().send(text_data=json.dumps({
            "action": "remove_points",
            "points": event["points"]
        }))
