from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('consultorperfil/<int:id>/', views.miConsultorProfile, name="miConsultorProfile"), # documentado
    path('updateModulosSAPAdmin', views.updateModulosSAPAdmin, name="updateModulosSAPAdmin"),
    path('principal', views.principal, name="principalAdmin"), # documentado
    # NOTIFICATIONS
    path("all_notifications/", views.all_notifications, name="all_notificationsAdministrador"),
    path("view_notification/<int:id>/", views.view_notification, name="view_notificationAdministrador"),
    path("queryforname", views.queryForName, name="queryForName"),
    path("getconsultoresdisponibles", views.getConsultoresDisponibles, name="getConsultoresDisponibles"), # documentado
    path("getconsultoresdisponibleswithfilters", views.getConsultoresDisponiblesWithFilters, name="getConsultoresDisponiblesWithFilters"), # documentado
    path("consultor/documentacion", views.consultorDocumentacion, name="consultorDocumentacion"),
    path('consultor/PDF/<str:pais>/<str:rfc>/<str:nombre_pdf>/', views.servir_pdf, name='servir_pdf'),
    path('addConsultorProyecto', views.addConsultorProyecto, name="addConsultorProyecto"),
    path("validar/consultor/<int:id>/entrevista/<int:proyecto>", views.validarEntrevista, name="validarEntrevista"),
    path('addCategoriaConsultor', views.addCategoriaConsultor, name="addCategoriaConsultor"),
    path("contrato/consultor/<int:id>/proyecto/<int:proyecto>", views.contratoConsultor, name="contratoConsultor"),
    path('contratoBase', views.contratoMachote, name="contratoMachote"),
    path('contratoMarco', views.contratoMarco, name="contratoMarco"),
    path('contratoAnexo', views.contratoAnexo, name="contratoAnexo"),
    path('contratoFinal', views.contratoFinal, name="contratoFinal"),
    path('contratoTerceros', views.contratoTerceros, name="contratoTerceros"),
    path('facturas/<int:id>/Consultor/<int:prj>/', views.facturasConsultor, name="facturasConsultorForAdmin"),
    path('validarFacturas', views.validarFacturas, name="validarFacturasForAdmin"),
    path('updateNotaConsultor', views.updateNotaConsultor, name="updateNotaConsultor"),
    path('curriculum/<int:id>/consultor', views.curriculum_vitaeAdmin, name="curriculum_consultor_admin"),
    path('consultor/<int:id>/Reportes/<int:prj>/', views.consultorReportes, name="consultorReportesForAdmin"),
    path('validarHoras', views.validarHoras, name="validarHorasForAdmin"),
    path('validarReporteFinal', views.validarReporteFinal, name="validarReporteFinalForAdmin"),
    path('controlDePagosProyectoConsultor', views.excel, name="controlDePagosProyectoConsultor"),
    # ADMIN
    path('agregarAdministrador', views.agergarAdministrador, name="agergarAdministrador"), # documentado
    path('profesionConsultorAdmin', views.profesionConsultorAdmin, name="profesionConsultorAdmin"), # documentado
    path('educationConsultorAdmin', views.educationConsultorAdmin, name="educationConsultorAdmin"), # documentado
    path('experienceConsultorAdmin', views.experienceConsultorAdmin, name="experienceConsultorAdmin"), # documentado
    path('agregadoConsultorAdmin', views.agregadoConsultorAdmin, name="AgregadoConsultorAdmin"), # documentado

    path('proyectosForAdmin', views.proyectosForAdmin, name="proyectosForAdmin"), # documentado
    path('proyecto/<int:id>/Adetalles', views.detallesProyectoAdmin, name="detalles_proyecto_admin"), # documentado
    path('postulacionesByAdmin', views.postularByAdministrador, name="postularByAdministrador"),
    path("updatePuntuacion/<int:id>/Evaluacion/<int:prj>/", views.updatePuntuacion, name="updatePuntuacion"),
    path("formComentariosUpdateAdmin", views.formComentariosUpdateAdmin, name="formComentariosUpdateAdmin"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)