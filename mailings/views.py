from django.views.generic import TemplateView
from .models import Mailing, Client

class HomeView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_count"] = Mailing.objects.count()
        context["active_count"] = Mailing.objects.filter(status="started").count()
        context["unique_clients_count"] = Client.objects.values("email").distinct().count()
        return context

