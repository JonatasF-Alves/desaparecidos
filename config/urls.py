from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import Http404, HttpResponse
from allauth.core.internal.httpkit import get_client_ip


def debug_ip(request):
    # TEMPORARIO: só superusuário; apagar depois do teste
    if not request.user.is_superuser:
        raise Http404
    linhas = [
        f"allauth le: {get_client_ip(request)}",
        f"CF-Connecting-IP: {request.headers.get('CF-Connecting-IP')}",
        f"True-Client-IP: {request.headers.get('True-Client-IP')}",
        f"X-Forwarded-For: {request.headers.get('X-Forwarded-For')}",
        f"REMOTE_ADDR: {request.META.get('REMOTE_ADDR')}",
        f"HEADER configurado: {settings.ALLAUTH_TRUSTED_CLIENT_IP_HEADER}",
        f"PROXY_COUNT: {settings.ALLAUTH_TRUSTED_PROXY_COUNT}",
    ]
    return HttpResponse("\n".join(linhas), content_type="text/plain")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("painel/", include("analises.urls")),
#    path("contas/", include("contas.urls")),
    path("accounts/", include("allauth.urls")),
    path("debug-ip/", debug_ip),
    path("", include("casos.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
