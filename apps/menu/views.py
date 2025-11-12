from django.views.generic import TemplateView
from .models import MenuItem

class MenuTreeView(TemplateView):
    template_name = 'menu/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.filter(parent__isnull=True).prefetch_related('children')
        return context

