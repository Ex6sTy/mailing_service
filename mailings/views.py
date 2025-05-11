from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Mailing, Client, Message, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_count"] = Mailing.objects.count()
        context["active_count"] = Mailing.objects.filter(status="started").count()
        context["unique_clients_count"] = Client.objects.values("email").distinct().count()
        return context


class DenyManagersMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Менеджеры").exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailings/client_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(DenyManagersMixin, LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailings/client_form.html"
    success_url = reverse_lazy("mailings:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(DenyManagersMixin, LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailings/client_form.html"
    success_url = reverse_lazy("mailings:client_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(DenyManagersMixin, LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "mailings/client_confirm_delete.html"
    success_url = reverse_lazy("mailings:client_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all() if self.request.user.groups.filter(
                name="Менеджеры").exists() else Message.objects.filter(owner=self.request.user)
        return Client.objects.filter(owner=self.request.user)


class MessageCreateView(DenyManagersMixin, LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(DenyManagersMixin, LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all() if self.request.user.groups.filter(
                name="Менеджеры").exists() else Message.objects.filter(owner=self.request.user)
        return Client.objects.filter(owner=self.request.user)


class MessageDeleteView(DenyManagersMixin, LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all() if self.request.user.groups.filter(
                name="Менеджеры").exists() else Message.objects.filter(owner=self.request.user)
        return Client.objects.filter(owner=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all() if self.request.user.groups.filter(name="Менеджеры").exists() else Mailing.objects.filter(owner=self.request.user)
        return Client.objects.filter(owner=self.request.user)


class MailingCreateView(DenyManagersMixin, LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(DenyManagersMixin, LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all() if self.request.user.groups.filter(name="Менеджеры").exists() else Mailing.objects.filter(owner=self.request.user)
        return Client.objects.filter(owner=self.request.user)


class MailingDeleteView(DenyManagersMixin, LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all() if self.request.user.groups.filter(name="Менеджеры").exists() else Mailing.objects.filter(owner=self.request.user)
        return Client.objects.filter(owner=self.request.user)


@login_required
def send_mailing_now(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
    clients = mailing.clients.all()
    message = mailing.message

    for client in clients:
        try:
            result = send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status="success",
                server_response=f"Отправлено: {result}"
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status="failure",
                server_response=str(e)
            )

    mailing.status = "started"
    mailing.save()
    messages.success(request, f"Рассылка #{mailing.pk} отправлена.")
    return redirect("mailings:mailing_list")


class AttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailings/attempt_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return MailingAttempt.objects.filter(mailing__owner=self.request.user) if not self.request.user.groups.filter(name="Менеджеры").exists() else MailingAttempt.objects.all()
        return Client.objects.filter(owner=self.request.user)
