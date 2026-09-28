from django.conf import settings

def clinic_info(request):
    return {
        'CLINIC': settings.CLINIC_METADATA,
    }
