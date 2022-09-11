from django.conf import settings


def get_available_providers():
    return [(key, value.get('name')) for key, value in settings.COURIER_PROVIDERS.items()]
