# check_service_health/management/commands/test_rabbitmq.py

from django.core.management.base import BaseCommand
from django.conf import settings
import time
import uuid


class Command(BaseCommand):
    help = 'Test if RabbitMQ is working properly'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed output'
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=10,
            help='Connection timeout in seconds (default: 10)'
        )

    def handle(self, *args, **options):
        verbose = options.get('detailed', False)
        timeout = options.get('timeout', 10)
        
        self.stdout.write('Testing RabbitMQ connection...')
        
        try:
            import pika
        except ImportError:
            self.stdout.write(self.style.ERROR(
                '❌ pika package not installed. Run: pip install pika'
            ))
            return
        
        # Get RabbitMQ settings
        rabbitmq_host = getattr(settings, 'RABBITMQ_HOST', 'localhost')
        rabbitmq_port = getattr(settings, 'RABBITMQ_PORT', 5672)
        rabbitmq_user = getattr(settings, 'RABBITMQ_USER', 'guest')
        rabbitmq_pass = getattr(settings, 'RABBITMQ_PASSWORD', 'guest')
        rabbitmq_vhost = getattr(settings, 'RABBITMQ_VHOST', '/')
        
        test_queue = f'django_health_check_test_{uuid.uuid4().hex[:8]}'
        test_exchange = f'health_check_exchange_{uuid.uuid4().hex[:8]}'
        test_message = f'health_check_{time.time()}'
        
        connection = None
        
        try:
            # 1. Test Connection
            self.stdout.write('Connecting to RabbitMQ...')
            
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
            parameters = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                virtual_host=rabbitmq_vhost,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=1,
                socket_timeout=timeout,
                blocked_connection_timeout=timeout
            )
            
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Connected to RabbitMQ'))
            
            if verbose:
                self.stdout.write(f'   Host: {rabbitmq_host}:{rabbitmq_port}')
                self.stdout.write(f'   Virtual Host: {rabbitmq_vhost}')
                self.stdout.write(f'   User: {rabbitmq_user}')
            
            # 2. Declare Exchange
            self.stdout.write('Creating test exchange...')
            channel.exchange_declare(
                exchange=test_exchange,
                exchange_type='direct',
                durable=False
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Exchange created: {test_exchange}'))
            
            # 3. Declare Queue
            self.stdout.write('Creating test queue...')
            channel.queue_declare(queue=test_queue, durable=False)
            self.stdout.write(self.style.SUCCESS(f'✅ Queue created: {test_queue}'))
            
            # 4. Bind Queue to Exchange
            channel.queue_bind(
                exchange=test_exchange,
                queue=test_queue,
                routing_key='health.check'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Queue bound to exchange'))
            
            # 5. Publish Message
            channel.basic_publish(
                exchange=test_exchange,
                routing_key='health.check',
                body=test_message.encode()
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Message published'))
            
            # 6. Consume Message
            method_frame, header_frame, body = channel.basic_get(queue=test_queue)
            
            if method_frame:
                received_message = body.decode()
                if received_message == test_message:
                    self.stdout.write(self.style.SUCCESS(f'✅ Message received and verified'))
                    channel.basic_ack(method_frame.delivery_tag)
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Message mismatch'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ No message received'))
            
            # 7. Cleanup
            channel.queue_delete(queue=test_queue)
            channel.exchange_delete(exchange=test_exchange)
            self.stdout.write(self.style.SUCCESS(f'✅ Test resources cleaned up'))
            
            self.stdout.write(self.style.SUCCESS('\n✅ RabbitMQ test completed successfully'))
            
        except pika.exceptions.AMQPConnectionError as e:
            self.stdout.write(self.style.ERROR(f'❌ Connection failed: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error occurred: {e}'))
        finally:
            if connection and connection.is_open:
                connection.close()
                if verbose:
                    self.stdout.write('Connection closed')
