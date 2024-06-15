from django.utils.translation import activate

from emission.models import GlobalSettings

class ActivateLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Aquí puedes implementar la lógica para activar el idioma según la solicitud
        settings = GlobalSettings.objects.first()
        language = settings.language if settings else 'en'
        activate(language)
        response = self.get_response(request)
        return response