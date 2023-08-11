from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('miperfil', views.miProfile, name="miProfile"), # Documentado
    path('principal', views.principal, name="principal"), # Documentado
    path('misproyectos', views.miProjects, name="miProjects"), # Documentado
    path('proyecto/<int:id>/detalles', views.detallesProyecto, name="detalles_proyecto"), # Documentado
    path('miProyecto/<int:id>/detalles', views.miProyecto, name="miProyecto"), # Documentado
    path('upload', views.upload_file, name="upload"),
    path('upload_all_files', views.upload_all_files_rp, name="upload_all_files"),
    path('updateprofileinformation', views.updateInformationProfile, name="updateInformationProfile"),
    path('updateconsultorinformation', views.updateInformationConsultor, name="updateInformationConsultor"),
    path('updateidiomaconsultor', views.updateIdiomaConsultor, name="updateIdiomaConsultor"),
    path('deleteidiomaconsultor', views.deleteIdiomaConsultor, name="deleteIdiomaConsultor"),
    path('updateModulosSAP', views.updateModulosSAP, name="updateModulosSAP"),
    path('updatecertificados', views.updateCertificados, name="updateCertificados"),
    path('updateexperiencia', views.updateExperiencia, name="updateExperiencia"),
    path('addDescriptionConsultor', views.addDescriptionConsultor, name="addDescriptionConsultor"),
    path('updateeducacion', views.updateEducacion, name="updateEducacion"),
    path('uploadImage', views.uploadImage, name="uploadImage"),
    path('deleteModuloSAP/<int:id>/', views.deleteModuloSAP, name="deleteModuloSAP"),
    path('postulaciones', views.postularse, name="postulaciones"),
    path('addInfoExtra', views.addInfoExtra, name="addInfoExtra"),
    path('deletePostulacion', views.deletePostulacion, name="deletePostulacion"),
    path('confirm/<int:id>/entrevista', views.confirmarEntrevistaConsultor, name="confirmarEntrevistaConsultor"),
    path('confirm/<int:id>/proyecto', views.confirmarProyectoConsultor, name="confirmarProyectoConsultor"),
    path('test', views.test, name="test"),
    path('bancos/<int:id>/Datos', views.bancosDatos, name="bancosDatos"),
    path('curriculum_consultor', views.curriculum_vitae, name="curriculum_consultor"),
    #NOTIFICATIONS
    path("all_notifications/", views.all_notifications, name="all_notifications"),
    path("view_notification/<int:id>/", views.view_notification, name="view_notification"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)