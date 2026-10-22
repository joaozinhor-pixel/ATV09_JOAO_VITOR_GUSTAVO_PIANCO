from pathlib import Path

from django.core.management.base import BaseCommand

from paginas.models import Conteudo, Menu

PASTA = Path(__file__).resolve().parent.parent.parent / "conteudos_iniciais"

# (slug, título) - o HTML de cada um está em paginas/conteudos_iniciais/<slug>.html
CONTEUDOS = [
    ("inicio", "Página Inicial"),
    ("curriculo-joao-vitor", "Currículo - João Vitor"),
    ("curriculo-gustavo-pianco", "Currículo - Gustavo Piancó"),
    ("jogos-e-musicas", "Tema: Jogos e Músicas"),
    ("brawl-stars", "Tema: Brawl Stars"),
    ("contato", "Contato / Ouvidoria"),
]

# (título, slug do conteúdo ou None, URL externa)
MENU = [
    ("Página Inicial", "inicio", ""),
    ("Currículo - João Vitor", "curriculo-joao-vitor", ""),
    ("Currículo - Gustavo Piancó", "curriculo-gustavo-pianco", ""),
    ("Tema: Jogos e Músicas", "jogos-e-musicas", ""),
    ("Tema: Brawl Stars", "brawl-stars", ""),
    ("Contato / Ouvidoria", "contato", ""),
    ("Playstation Store", None, "https://store.playstation.com/pt-br/"),
    ("Spotify", None, "https://open.spotify.com/intl-pt"),
    ("Brawl Stars", None, "https://store.supercell.com/pt/brawlstars"),
]


class Command(BaseCommand):
    help = "Cadastra no banco os conteúdos e o menu iniciais do portal (atalho para o Admin)."

    def handle(self, *args, **options):
        objetos = {}
        for slug, titulo in CONTEUDOS:
            html = (PASTA / f"{slug}.html").read_text(encoding="utf-8")
            obj, _ = Conteudo.objects.update_or_create(
                slug=slug,
                defaults={"titulo": titulo, "conteudo_html": html, "ativo": True},
            )
            objetos[slug] = obj

        for ordem, (titulo, slug, url) in enumerate(MENU, start=1):
            if slug:
                Menu.objects.update_or_create(
                    titulo=titulo,
                    defaults={
                        "tipo_destino": Menu.INTERNO,
                        "conteudo": objetos[slug],
                        "url_externa": "",
                        "ordem": ordem,
                        "ativo": True,
                    },
                )
            else:
                Menu.objects.update_or_create(
                    titulo=titulo,
                    defaults={
                        "tipo_destino": Menu.EXTERNO,
                        "conteudo": None,
                        "url_externa": url,
                        "ordem": ordem,
                        "ativo": True,
                    },
                )

        self.stdout.write(self.style.SUCCESS(
            f"{len(CONTEUDOS)} conteúdos e {len(MENU)} itens de menu cadastrados."
        ))
