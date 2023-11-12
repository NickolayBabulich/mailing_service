from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from mailing_service.models import Client, Message, Mailing, Logs
from mailing_service.forms import ClientForm, MessageForm, MailingForm


class IndexView(TemplateView):
    template_name = 'mailing_service/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['total_mailings'] = Mailing.objects.all().count()
        context_data['total_activity_mailings'] = Mailing.objects.filter(status=2).count()
        context_data['total_clients'] = Client.objects.all().count()

        return context_data


class ClientListView(ListView):
    model = Client
    template_name = 'mailing_service/clients/clients.html'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('index:list_clients')
    template_name = 'mailing_service/clients/client_form.html'

    def form_valid(self, form):
        obj: Client = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('index:list_clients')
    template_name = 'mailing_service/clients/client_update_form.html'

    def test_func(self):
        return not self.request.user.is_staff


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('index:list_clients')
    template_name = 'mailing_service/clients/client_confirm_delete.html'

    def test_func(self):
        return not self.request.user.is_staff


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing_service/clients/client_detail.html'


class MessageListView(ListView):
    model = Message
    template_name = 'mailing_service/message/messages.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('index:list_messages')
    template_name = 'mailing_service/message/message_form.html'

    def form_valid(self, form):
        obj: Message = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('index:list_messages')
    template_name = 'mailing_service/message/message_form.html'

    def test_func(self):
        return not self.request.user.is_staff


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing_service/message/message_detail.html'


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('index:list_messages')
    template_name = 'mailing_service/message/message_confirm_delete.html'

    def test_func(self):
        return not self.request.user.is_staff


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_service/mailing/mailings.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('index:list_mailings')
    template_name = 'mailing_service/mailing/mailing_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def form_valid(self, form):
        obj: Mailing = form.save()
        obj.owner = self.request.user
        obj.next_try = obj.time_to_start
        if obj.time_to_finish <= obj.next_try:
            obj.status = 0
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing/mailing_detail.html'


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('index:list_mailings')
    template_name = 'mailing_service/mailing/mailing_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def test_func(self):
        return not self.request.user.is_staff


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('index:list_mailings')
    template_name = 'mailing_service/mailing/mailing_confirm_delete.html'

    def test_func(self):
        return not self.request.user.is_staff


class LogsListView(ListView):
    model = Logs
    template_name = 'mailing_service/logs/logs.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Logs.objects.all()
        return Logs.objects.filter(owner=self.request.user)
