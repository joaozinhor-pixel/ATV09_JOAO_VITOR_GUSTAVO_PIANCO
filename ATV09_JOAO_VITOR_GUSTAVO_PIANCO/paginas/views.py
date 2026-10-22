from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Conteudo, Menu


def obter_menu():
    """Itens ativos do menu, na ordem definida no Admin.

    Itens internos só aparecem se o Conteudo relacionado também estiver ativo.
    """
    return (
        Menu.objects.filter(ativo=True)
        .filter(
            Q(tipo_destino=Menu.EXTERNO)
            | Q(tipo_destino=Menu.INTERNO, conteudo__ativo=True)
        )
        .select_related("conteudo")
        .order_by("ordem", "titulo")
    )


def home(request):
    """Página inicial: exibe o Conteudo de slug 'inicio'."""
    conteudo = get_object_or_404(Conteudo, slug="inicio", ativo=True)
    return render(request, "paginas/conteudo.html", {"conteudo": conteudo})


def conteudo_detalhe(request, slug):
    """Exibe um Conteudo específico a partir do slug da URL."""
    conteudo = get_object_or_404(Conteudo, slug=slug, ativo=True)
    return render(request, "paginas/conteudo.html", {"conteudo": conteudo})
