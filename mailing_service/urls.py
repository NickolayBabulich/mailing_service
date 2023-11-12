from django.urls import path

from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import IndexView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    ClientDetailView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView, \
    MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, LogsListView

app_name = MailingServiceConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('clients/', ClientListView.as_view(), name='list_clients'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/view/<int:pk>', ClientDetailView.as_view(), name='view_client'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('messages/', MessageListView.as_view(), name='list_messages'),
    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/view/<int:pk>', MessageDetailView.as_view(), name='view_message'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('mailings/', MailingListView.as_view(), name='list_mailings'),
    path('mailing/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/view/<int:pk>', MailingDetailView.as_view(), name='view_mailing'),
    path('mailing/update/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailing/delete/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),

    path('logs/', LogsListView.as_view(), name='list_logs')

]
