from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LiveCountsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('live_feed', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('live_feed', self.channel_name)

    async def counts_update(self, event):
        data = event['data']
        await self.send_json(data)
