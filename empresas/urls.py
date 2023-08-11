from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("valdarEntrevista", views.valdarEntrevista, name="valdarEntrevista"),
    path("formComentarios/<int:id>/Evaluacion/<int:prj>/", views.formComentariosEvaluacion, name="formComentariosEvaluacion"),
    path("formComentarios", views.formComentarios, name="formComentarios"),
    path('consultorEmpresa/<int:id>/prj/<int:prj>/', views.consultorEmpresa, name="consultorEmpresa"),
    # NOTIFICATIONS
    path("all_notifications/", views.all_notifications, name="all_notificationsEmpresa"),
    path("view_notification/<int:id>/", views.view_notification, name="view_notificationEmpresa"),
    path('addDatos/bancarios', views.datosBancarios, name="datosBancarios"),
    
    path('consultor/<int:id>/Facturas/<int:prj>/', views.consultorFacturas, name="consultorFacturas"),
    path('consultor/<int:id>/Reportes/<int:prj>/', views.consultorReportes, name="consultorReportes"),
    path('validarFacturas', views.validarFacturas, name="validarFacturas"),
    path('validarHoras', views.validarHoras, name="validarHoras"),
    path('validarReporteFinal', views.validarReporteFinal, name="validarReporteFinal"),
    path('curriculum/<int:id>/consultor', views.curriculum_vitaeEmpresa, name="curriculum_consultor_Empresa"),
    path("consultor/documentos", views.consultorDocumentosShowXML, name="consultorDocumentosShowXML"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)