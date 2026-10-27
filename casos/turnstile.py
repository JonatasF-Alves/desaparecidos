from django import forms
from django.utils.html import format_html
import json
import urllib.parse
import urllib.request

from django.conf import settings

URL_VERIFICACAO = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verificar_turnstile(token, ip=None, secret=None):
    """Devolve True só se a Cloudflare confirmar que o token é válido."""
    if not token:
        return False

    dados = {"secret": secret or settings.TURNSTILE_SECRET_KEY, "response": token}
    if ip:
        dados["remoteip"] = ip

    corpo = urllib.parse.urlencode(dados).encode()
    try:
        with urllib.request.urlopen(URL_VERIFICACAO, data=corpo, timeout=5) as resp:
            resultado = json.load(resp)
    except Exception:
        return False

    return resultado.get("success") is True

class TurnstileWidget(forms.Widget):
    """Desenha a caixinha do Turnstile no lugar do campo."""

    def render(self, name, value, attrs=None, renderer=None):
        return format_html(
            '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'
            '<div class="cf-turnstile" data-sitekey="{}"></div>',
            settings.TURNSTILE_SITE_KEY,
        )


class TurnstileField(forms.Field):
    widget = TurnstileWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", "")
        kwargs.setdefault("error_messages", {"required": "Confirme que você não é um robô."})
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if not verificar_turnstile(value):
            raise forms.ValidationError("Não foi possível confirmar que você não é um robô. Tente de novo.")


class CadastroComTurnstileForm(forms.Form):
    """Campo extra que o allauth junta ao formulário de cadastro."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O nome tem hífen, então não dá para declarar como atributo da classe.
        # É o nome que o Cloudflare usa no campo escondido que ele cria sozinho.
        self.fields["cf-turnstile-response"] = TurnstileField()

    def signup(self, request, user):
        pass  # o allauth exige este método, mas não temos nada a fazer aqui