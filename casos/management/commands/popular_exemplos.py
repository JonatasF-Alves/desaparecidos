import random
from datetime import date, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from casos.models import Caso

NOMES = ["Ana Souza", "Bruno Lima", "Carla Mendes", "Diego Rocha", "Elisa Martins", "Felipe Santos",
         "Gabriela Alves", "Henrique Costa", "Isabela Ramos", "João Pereira", "Kátia Nunes", "Lucas Barros"]
CIDADES = ["Rio de Janeiro", "São João de Meriti", "Duque de Caxias", "Niterói",
           "Nova Iguaçu", "Belford Roxo", "São Gonçalo"]
CORES = ["#C9D3DE", "#D9CFC1", "#CBD8CF", "#D6CBD9", "#D3D3C0"]


def silhueta(cor):
    img = Image.new("RGB", (400, 500), cor)
    d = ImageDraw.Draw(img)
    d.ellipse((140, 90, 260, 210), fill="#7A8794")
    d.ellipse((70, 250, 330, 620), fill="#7A8794")
    buf = BytesIO()
    img.save(buf, "JPEG", quality=85)
    return buf.getvalue()


class Command(BaseCommand):
    help = "Cria casos FICTÍCIOS para testar o site (use --limpar para apagá-los)."

    def add_arguments(self, parser):
        parser.add_argument("--limpar", action="store_true")

    def handle(self, *args, **opts):
        if opts["limpar"]:
            n, _ = Caso.objects.filter(numero_bo__startswith="TESTE-").delete()
            self.stdout.write(f"{n} caso(s) de exemplo apagado(s).")
            return
        random.seed(7)
        for i, nome in enumerate(NOMES, 1):
            desde = date.today() - timedelta(days=random.randint(5, 240))
            achado = i % 4 == 0
            caso = Caso(
                nome=nome, idade=random.choice([8, 14, 16, 23, 31, 45, 52, 67, 74]),
                cidade=random.choice(CIDADES), estado="RJ", data_desaparecimento=desde,
                descricao="Caso fictício criado apenas para testar o site.",
                contato="(21) 90000-0000", numero_bo=f"TESTE-{i:03d}", aprovado=True,
                status="encontrado" if achado else "desaparecido",
                data_encontrado=desde + timedelta(days=random.randint(2, 30)) if achado else None,
            )
            caso.foto.save(f"exemplo{i}.jpg", ContentFile(silhueta(random.choice(CORES))), save=False)
            caso.save()
        self.stdout.write("12 casos fictícios criados.")
