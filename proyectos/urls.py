from django.urls import path, include
from . import views

urlpatterns = [
    path("misProyectos", views.my_projects, name="my_projectsCreateds"),
    path("crearProyecto", views.create_new_project, name="create_new_project"),
    path("requerimientosProyecto", views.requirements_project, name="requirements_project"),
    path("requerimientosEducacionProyecto", views.requirements_education_project,name="requerimientosEducationProyecto"),
    path("proyectoCreado", views.project_created, name="project_created"),
    path("detallesProyecto", views.details_project, name="details_project"),
    path("mapa", views.mapa, name="mapa"),
    path("addNewProject", views.addNewProject, name="addNewProject"),
]
