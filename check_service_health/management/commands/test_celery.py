# check_service_health/management/commands/test_celery.py

from django.core.management.base import BaseCommand
from celery import Celery
from django.conf import settings
from celery.result import AsyncResult
import time


class Command(BaseCommand):
    help = 'Test if Celery is working properly'

    def handle(self, *args, **kwargs):
        try:
            # Create Celery app instance
            app = Celery('borcelle_crm')
            app.config_from_object('django.conf:settings', namespace='CELERY')
            
            # Check if Celery is configured
            self.stdout.write(f'Celery Broker URL: {settings.CELERY_BROKER_URL[:30]}...')
            self.stdout.write(f'Celery Result Backend: {settings.CELERY_RESULT_BACKEND[:30]}...')
            
            # Try to inspect Celery workers
            inspect = app.control.inspect()
            
            # Check active workers
            active_workers = inspect.active()
            if active_workers:
                self.stdout.write(self.style.SUCCESS(f'✅ Active Celery workers found: {list(active_workers.keys())}'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  No active Celery workers found'))
            
            # Check registered tasks
            registered_tasks = inspect.registered()
            if registered_tasks:
                task_count = len(sum(registered_tasks.values(), []))
                self.stdout.write(self.style.SUCCESS(f'✅ Registered tasks: {task_count} tasks'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  No registered tasks found'))
            
            # Check stats
            try:
                stats = inspect.stats()
                if stats:
                    self.stdout.write(self.style.SUCCESS(f'✅ Worker stats retrieved successfully'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️  Could not retrieve worker stats: {e}'))
            
            self.stdout.write(self.style.SUCCESS('✅ Celery connectivity test completed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error occurred: {e}'))
