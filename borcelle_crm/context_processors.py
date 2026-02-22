"""
Custom context processors for borcelle_crm
"""
from django.conf import settings


def testing_context(request):
    """
    Add TESTING flag to template context
    This is used to conditionally load external resources during testing
    """
    return {
        'testing': getattr(settings, 'TESTING', False)
    }
