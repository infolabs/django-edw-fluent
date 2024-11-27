from django.conf import settings


DOMAIN_WITH_PROTOCOL = getattr(settings, 'CURRENT_DOMAIN_WITH_PROTOCOL', None)
