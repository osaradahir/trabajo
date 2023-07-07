from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('consultorperfil/<int:id>/', views.miConsultorProfile, name="miConsultorProfile"),
    path('updateModulosSAPAdmin', views.updateModulosSAPAdmin, name="updateModulosSAPAdmin"),
    path('principal', views.principal, name="principalAdmin"),
    # NOTIFICATIONS
    path("all_notifications/", views.all_notifications, name="all_notificationsAdministrador"),
    path("view_notification/<int:id>/", views.view_notification, name="view_notificationAdministrador"),
    path("queryforname", views.queryForName, name="queryForName"),
    path("getconsultoresdisponibles", views.getConsultoresDisponibles, name="getConsultoresDisponibles"),
    path("getconsultoresdisponibleswithfilters", views.getConsultoresDisponiblesWithFilters, name="getConsultoresDisponiblesWithFilters"),
    path("consultor/documentacion", views.consultorDocumentacion, name="consultorDocumentacion"),
    path('consultor/PDF/<str:pais>/<str:rfc>/<str:nombre_pdf>/', views.servir_pdf, name='servir_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)