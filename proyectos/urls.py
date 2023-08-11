from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("misProyectos", views.my_projects, name="my_projectsCreateds"),
    path("crearProyecto", views.create_new_project, name="create_new_project"),
    path("requerimientosProyecto", views.requirements_project, name="requirements_project"),
    path("requerimientosEducacionProyecto", views.requirements_education_project,name="requerimientosEducationProyecto"),
    path("proyectoCreado", views.project_created, name="project_created"),
    path("detallesProyecto", views.details_project, name="details_project"),
    path("updateDetallesProyecto", views.updateDetails_project, name="update_details_project"),
    path("updateRequerimientosProyecto", views.updateRequerimientos_project, name="update_requerimientos_project"),
    path("updateRequerimientosIdiomaProyecto", views.updateRequerimientosIdioma_project, name="update_requerimientos_idioma_project"),
    path("updateDetallesCertificacionesProyecto", views.updateDetailsCertificaciones_project, name="update_details_certificaciones_project"),
    path("deleteRequerimientosProyecto/<int:id>", views.deleteRequerimientos_project, name="delete_requerimientos_project"),
    path("deleteRequerimientosProyectoIdiomas/<int:id>", views.deleteRequerimientosIdiomas_project, name="delete_requerimientos_idiomas_project"),
    path("addRequerimientosProyecto/<int:id>", views.addRequerimientos_project, name="add_requerimientos_project"),
    path("addRequerimientosIdiomaProyecto/<int:id>", views.addRequerimientos_idiomas_project, name="add_requerimientos_idiomas_project"),
    path("addNewProject", views.addNewProject, name="addNewProject"),
    path('deletePostulacionProyecto', views.deletePostulacionProyecto, name="deletePostulacionProyectos"),
    path('solictar/entrevista', views.solicitarEntrevista, name="solicitarEntrevista"),
    path('entrevistaAgendada', views.entrevistaAgendada, name="entrevistaAgendada"),
    path("ver/consultor/<int:id>/mapa", views.mapa, name="mapa"),
    path("ver/all/<int:id>/consultor/mapa", views.allMapa, name="allMapa"),
    path("ver/allGnosis/<int:id>/consultor/mapa", views.allMapaGnosis, name="allMapaGnosis"),
    path('validarEntrevistaGnosis', views.validarEntrevistaGnosis, name="validarEntrevistaGnosis"),
    path('nuevaEntrevista', views.nuevaEntrevista, name="nuevaEntrevista"),
    path('eliminarEntrevista', views.eliminarEntrevista, name="eliminarEntrevista"),
    path('solicitarReporteHoras', views.solicitarReporteHoras, name="solicitarReporteHoras"),
    path('solicitarContrato', views.solicitarContrato, name="solicitarContrato"),
    path('solicitarContratoRenovacion', views.solicitarContratoRenovacion, name="solicitarContratoRenovacion"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)