from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asyncio


class LiveCountsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'live_feed'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.heartbeat_task = asyncio.create_task(self.send_heartbeat())

    async def disconnect(self, code):
        if hasattr(self, 'heartbeat_task') and self.heartbeat_task:
            self.heartbeat_task.cancel()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def counts_update(self, event):
        data = event['data']
        await self.send_json(data)

    async def send_heartbeat(self):
        """
        Sends a ping message every 45 seconds to keep the connection alive.
        """
        while True:
            await asyncio.sleep(45)
            await self.send_json({'type': 'heartbeat', 'message': 'ping'})
