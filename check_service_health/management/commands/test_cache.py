# check_service_health/management/commands/test_cache.py

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.conf import settings
import time
import uuid

class Command(BaseCommand):
    help = 'Test if Redis cache is working properly'

    def handle(self, *args, **kwargs):
        try:
            # Display cache configuration
            self.stdout.write(f'Cache Backend: {settings.CACHES["default"]["BACKEND"]}')
            self.stdout.write(f'Cache Location: {settings.CACHES["default"]["LOCATION"][:50]}...')
            
            # Test 1: Set and Get
            test_key = f'health_check_{uuid.uuid4().hex[:8]}'
            test_value = f'test_value_{time.time()}'
            
            cache.set(test_key, test_value, timeout=30)
            value = cache.get(test_key)
            
            if value == test_value:
                self.stdout.write(self.style.SUCCESS(f'✅ Cache set/get test passed'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Cache set/get test failed'))
                return
            
            # Test 2: Delete
            cache.delete(test_key)
            value = cache.get(test_key)
            
            if value is None:
                self.stdout.write(self.style.SUCCESS(f'✅ Cache delete test passed'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Cache delete test failed'))
                return
            
            # Test 3: Expiration
            expire_key = f'expire_check_{uuid.uuid4().hex[:8]}'
            cache.set(expire_key, 'expire_value', timeout=2)
            
            value_before = cache.get(expire_key)
            if value_before:
                self.stdout .write(f'Value set with 2 second expiration')
                
                # Wait for expiration
                time.sleep(3)
                
                value_after = cache.get(expire_key)
                if value_after is None:
                    self.stdout.write(self.style.SUCCESS(f'✅ Cache expiration test passed'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Cache still available after expiration'))
                    return
            
            # Test 4: Increment/Decrement
            counter_key = f'counter_{uuid.uuid4().hex[:8]}'
            cache.set(counter_key, 0)
            cache.incr(counter_key)
            cache.incr(counter_key)
            
            counter_value = cache.get(counter_key)
            if counter_value == 2:
                self.stdout.write(self.style.SUCCESS(f'✅ Cache increment test passed'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Cache increment test returned {counter_value}'))
            
            cache.delete(counter_key)
            
            self.stdout.write(self.style.SUCCESS('\n✅ Redis cache test completed successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error occurred: {e}'))