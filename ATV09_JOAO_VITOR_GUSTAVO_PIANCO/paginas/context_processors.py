from .views import obter_menu


def menu(request):
    """Coloca 'itens_menu' em todos os templates (menu dinâmico)."""
    return {"itens_menu": obter_menu()}
