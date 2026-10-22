from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Conteudo(models.Model):
    """Página do portal. O HTML interno fica salvo no banco de dados."""

    titulo = models.CharField("título", max_length=150)
    slug = models.SlugField(
        "slug",
        unique=True,
        help_text="Parte da URL: /conteudo/<slug>/ (ex.: meu-tema).",
    )
    conteudo_html = models.TextField(
        "conteúdo HTML",
        help_text=(
            "Somente o HTML interno da página (section, article, h1, p...). "
            "NÃO coloque html, head, body, header, nav ou footer aqui."
        ),
    )
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "conteúdo"
        verbose_name_plural = "conteúdos"
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        # A página inicial (slug "inicio") também responde em "/"
        if self.slug == "inicio":
            return reverse("home")
        return reverse("conteudo", args=[self.slug])


class Menu(models.Model):
    """Item da navegação. Aponta para um Conteudo (interno) ou para uma URL (externo)."""

    INTERNO = "interno"
    EXTERNO = "externo"
    TIPOS_DESTINO = [
        (INTERNO, "Conteúdo interno"),
        (EXTERNO, "Link externo"),
    ]

    titulo = models.CharField("título", max_length=100)
    tipo_destino = models.CharField(
        "tipo de destino", max_length=10, choices=TIPOS_DESTINO, default=INTERNO
    )
    ordem = models.PositiveIntegerField(
        "ordem", default=0, help_text="Menor número aparece primeiro."
    )
    ativo = models.BooleanField("ativo", default=True)
    conteudo = models.ForeignKey(
        Conteudo,
        verbose_name="conteúdo relacionado",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="itens_menu",
        help_text="Obrigatório quando o destino for 'Conteúdo interno'.",
    )
    url_externa = models.URLField(
        "URL externa",
        blank=True,
        help_text="Obrigatória quando o destino for 'Link externo' (ex.: https://github.com).",
    )

    class Meta:
        verbose_name = "item do menu"
        verbose_name_plural = "itens do menu"
        ordering = ["ordem", "titulo"]

    def __str__(self):
        return f"{self.ordem} - {self.titulo}"

    def clean(self):
        """Garante que cada item tenha o destino correto para o seu tipo."""
        if self.tipo_destino == self.INTERNO:
            if not self.conteudo:
                raise ValidationError(
                    {"conteudo": "Escolha o conteúdo para um item de destino interno."}
                )
            self.url_externa = ""
        elif self.tipo_destino == self.EXTERNO:
            if not self.url_externa:
                raise ValidationError(
                    {"url_externa": "Informe a URL para um item de destino externo."}
                )
            self.conteudo = None

    @property
    def url(self):
        """URL final do item: rota do Django (interno) ou link cadastrado (externo)."""
        if self.tipo_destino == self.INTERNO and self.conteudo:
            return self.conteudo.get_absolute_url()
        return self.url_externa

    @property
    def eh_externo(self):
        return self.tipo_destino == self.EXTERNO
