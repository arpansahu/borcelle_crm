# check_service_health/management/commands/test_all_services.py

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from io import StringIO


class Command(BaseCommand):
    help = 'Run all service health checks for the Borcelle CRM application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed output for each service'
        )
        parser.add_argument(
            '--skip',
            nargs='+',
            type=str,
            metavar='SERVICE',
            help='Skip specific services (e.g., --skip celery storage)'
        )
        parser.add_argument(
            '--only',
            nargs='+',
            type=str,
            metavar='SERVICE',
            help='Only check specific services (e.g., --only db cache)'
        )

    def handle(self, *args, **options):
        verbose = options.get('detailed', False)
        skip_services = options.get('skip') or []
        only_services = options.get('only')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(
            '   🏥 BORCELLE CRM - SERVICE HEALTH CHECK'
        ))
        self.stdout.write('='*70 + '\n')
        
        # Define all available services
        all_services = [
            ('db', 'test_db', 'Database (PostgreSQL)', True),
            ('cache', 'test_cache', 'Cache (Redis)', True),
            ('channels', 'test_channels', 'Django Channels (WebSockets)', True),
            ('celery', 'test_celery', 'Celery Workers', True),
            ('storage', 'test_storage', 'Storage (MinIO)', True),
            ('rabbitmq', 'test_rabbitmq', 'RabbitMQ', self._is_rabbitmq_configured()),
            ('email', 'test_email', 'Email Service (MailJet)', self._is_email_configured()),
        ]
        
        # Filter services based on arguments
        services_to_check = []
        for key, command, name, is_configured in all_services:
            if only_services:
                if key in only_services:
                    services_to_check.append((key, command, name, is_configured))
            elif key not in skip_services:
                services_to_check.append((key, command, name, is_configured))
        
        results = {}
        
        for key, command, service_name, is_configured in services_to_check:
            self.stdout.write(f'{"-"*70}')
            
            if not is_configured:
                self.stdout.write(self.style.WARNING(f'⏭️  {service_name}: SKIPPED (not configured)'))
                results[service_name] = '⏭️  SKIPPED'
                continue
            
            self.stdout.write(self.style.HTTP_INFO(f'🔍 Testing: {service_name}'))
            self.stdout.write(f'{"-"*70}')
            
            out = StringIO()
            err = StringIO()
            
            try:
                # Build command arguments
                cmd_kwargs = {'stdout': out, 'stderr': err}
                if verbose:
                    cmd_kwargs['verbosity'] = 2
                
                call_command(command, **cmd_kwargs)
                output = out.getvalue()
                error = err.getvalue()
                
                if error:
                    self.stdout.write(self.style.ERROR(error))
                    results[service_name] = '❌ FAILED'
                elif 'ERROR' in output.upper() or 'FAILED' in output.upper() or '❌' in output:
                    self.stdout.write(output)
                    results[service_name] = '❌ FAILED'
                elif '⚠️' in output or 'WARNING' in output.upper():
                    self.stdout.write(output)
                    results[service_name] = '⚠️  WARNING'
                else:
                    if verbose:
                        self.stdout.write(output)
                    self.stdout.write(self.style.SUCCESS(f'✅ {service_name}: PASSED'))
                    results[service_name] = '✅ PASSED'
                    
            except CommandError as e:
                self.stdout.write(self.style.ERROR(f'❌ {service_name}: FAILED ({str(e)})'))
                results[service_name] = '❌ FAILED'
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ {service_name}: ERROR ({str(e)})'))
                results[service_name] = '❌ ERROR'
        
        # Summary
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('   📊 HEALTH CHECK SUMMARY'))
        self.stdout.write('='*70)
        
        passed = sum(1 for v in results.values() if '✅' in v)
        warnings = sum(1 for v in results.values() if '⚠️' in v)
        failed = sum(1 for v in results.values() if '❌' in v)
        skipped = sum(1 for v in results.values() if '⏭️' in v)
        
        for service_name, result in results.items():
            self.stdout.write(f'{result} {service_name}')
        
        self.stdout.write(f'\n' + '-'*70)
        self.stdout.write(f'Total: {len(results)} | Passed: {passed} | Warnings: {warnings} | Failed: {failed} | Skipped: {skipped}')
        self.stdout.write('='*70 + '\n')
        
        if failed > 0:
            raise CommandError(f'{failed} service(s) failed health check')
    
    def _is_rabbitmq_configured(self):
        """Check if RabbitMQ is configured"""
        return hasattr(settings, 'RABBITMQ_HOST') and settings.RABBITMQ_HOST
    
    def _is_email_configured(self):
        """Check if email service is configured"""
        return hasattr(settings, 'MAIL_JET_API_KEY') and settings.MAIL_JET_API_KEY
