# check_service_health/management/commands/test_email.py

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Test if MailJet email service is configured properly'

    def handle(self, *args, **kwargs):
        try:
            from mailjet_rest import Client
            
            # Get MailJet credentials
            api_key = getattr(settings, 'MAIL_JET_API_KEY', '')
            api_secret = getattr(settings, 'MAIL_JET_API_SECRET', '')
            email_address = getattr(settings, 'MAIL_JET_EMAIL_ADDRESS', '')
            
            if not api_key or not api_secret:
                self.stdout.write(self.style.ERROR(
                    '❌ MailJet credentials not configured'
                ))
                return
            
            self.stdout.write(f'MailJet Email Address: {email_address}')
            
            # Initialize MailJet client
            mailjet = Client(auth=(api_key, api_secret), version='v3')
            
            # Test 1: Get account information
            self.stdout.write('Testing MailJet API connection...')
            result = mailjet.sender.get()
            
            if result.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f'✅ API connection successful'))
                
                data = result.json()
                if 'Data' in data:
                    senders = data['Data']
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Found {len(senders)} verified sender(s)'
                    ))
                    
                    for sender in senders[:3]:  # Show first 3
                        status = sender.get('Status', 'Unknown')
                        email = sender.get('Email', 'Unknown')
                        self.stdout.write(f'   - {email}: {status}')
            else:
                self.stdout.write(self.style.ERROR(
                    f'❌ API request failed: {result.status_code}'
                ))
                return
            
            # Test 2: Check if sender is verified
            if email_address:
                verified = False
                for sender in senders:
                    if sender.get('Email') == email_address:
                        if sender.get('Status') == 'Active':
                            verified = True
                            self.stdout.write(self.style.SUCCESS(
                                f'✅ Email address {email_address} is verified and active'
                            ))
                        break
                
                if not verified:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️  Email address {email_address} is not verified'
                    ))
            
            self.stdout.write(self.style.SUCCESS('\n✅ MailJet test completed successfully'))
            
        except ImportError:
            self.stdout.write(self.style.ERROR(
                '❌ mailjet_rest package not installed. Run: pip install mailjet-rest'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error occurred: {e}'))
