from django.urls import path
from . import views

urlpatterns = [
    path("valdarEntrevista", views.valdarEntrevista, name="valdarEntrevista"),
    # NOTIFICATIONS
    path("all_notifications/", views.all_notifications, name="all_notificationsEmpresa"),
    path("view_notification/<int:id>/", views.view_notification, name="view_notificationEmpresa"),
]
