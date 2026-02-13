# check_service_health/management/commands/test_channels.py

import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
import time
import uuid

class Command(BaseCommand):
    help = 'Test if Django Channels is working properly'

    def handle(self, *args, **kwargs):
        # Check if Channels is configured
        if not hasattr(settings, 'CHANNEL_LAYERS'):
            self.stdout.write(self.style.ERROR('❌ Channels is not configured in this application'))
            return
        
        # Display channel layer configuration
        channel_config = settings.CHANNEL_LAYERS.get('default', {})
        self.stdout.write(f'Channel Layer Backend: {channel_config.get("BACKEND", "Unknown")}')
        
        # Run the async test function
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.test_channels())
        except RuntimeError:
            # If loop is already running, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.test_channels())

    async def test_channels(self):
        try:
            from channels.layers import get_channel_layer
        except ImportError:
            self.stdout.write(self.style.ERROR('❌ Django Channels is not installed'))
            return

        channel_layer = get_channel_layer()
        if not channel_layer:
            self.stdout.write(self.style.ERROR('❌ Channels layer is not configured properly'))
            return

        test_channel = f'test_channel_{uuid.uuid4().hex[:8]}'
        test_message = {
            'type': 'test.message',
            'text': 'Hello, Channels!',
            'timestamp': time.time()
        }

        try:
            # Test 1: Send and Receive
            self.stdout.write(f'Testing channel: {test_channel}')
            
            # Send a message to the channel
            await channel_layer.send(test_channel, test_message)
            self.stdout.write(self.style.SUCCESS('✅ Message sent to channel'))

            # Receive the message from the channel
            received_message = await channel_layer.receive(test_channel)
            self.stdout.write(self.style.SUCCESS(f'✅ Message received from channel'))

            # Verify the message content
            if received_message['text'] == 'Hello, Channels!':
                self.stdout.write(self.style.SUCCESS('✅ Message content verified'))
            else:
                self.stdout.write(self.style.ERROR('❌ Message content mismatch'))
                return
            
            # Test 2: Group Send
            group_name = f'test_group_{uuid.uuid4().hex[:8]}'
            test_channel2 = f'test_channel_2_{uuid.uuid4().hex[:8]}'
            
            # Add channel to group
            await channel_layer.group_add(group_name, test_channel2)
            self.stdout.write(f'Channel added to group: {group_name}')
            
            # Send message to group
            await channel_layer.group_send(
                group_name,
                {
                    'type': 'test.broadcast',
                    'message': 'Group broadcast message'
                }
            )
            self.stdout.write(self.style.SUCCESS('✅ Group message sent'))
            
            # Receive group message
            group_message = await channel_layer.receive(test_channel2)
            if group_message and 'message' in group_message:
                self.stdout.write(self.style.SUCCESS('✅ Group message received'))
            
            # Remove from group
            await channel_layer.group_discard(group_name, test_channel2)
            self.stdout.write(self.style.SUCCESS('✅ Channel removed from group'))
            
            self.stdout.write(self.style.SUCCESS('\n✅ Django Channels test completed successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ An error occurred: {e}'))