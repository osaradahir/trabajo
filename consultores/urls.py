from django.urls import path
from . import views

urlpatterns = [
    path('miperfil', views.miProfile, name="miProfile"),
    path('principal', views.principal, name="principal"),
    path('detallesproyecto', views.detallesProyecto, name="detalles_proyecto"),
    path('upload', views.upload_file, name="upload"),
    path('updateprofileinformation', views.updateInformationProfile, name="updateInformationProfile"),
    path('updateconsultorinformation', views.updateInformationConsultor, name="updateInformationConsultor"),
    path('updateidiomaconsultor', views.updateIdiomaConsultor, name="updateIdiomaConsultor"),
    path('deleteidiomaconsultor', views.deleteIdiomaConsultor, name="deleteIdiomaConsultor"),
    path('updateModulosSAP', views.updateModulosSAP, name="updateModulosSAP"),
    path('updatecertificados', views.updateCertificados, name="updateCertificados"),
    path('updateexperiencia', views.updateExperiencia, name="updateExperiencia"),
    path('updateeducacion', views.updateEducacion, name="updateEducacion"),
    path('uploadImage', views.uploadImage, name="uploadImage"),
    path('deleteModuloSAP/<int:id>/', views.deleteModuloSAP, name="deleteModuloSAP"),
    #NOTIFICATIONS
    path("all_notifications/", views.all_notifications, name="all_notifications"),
    path("view_notification/<int:id>/", views.view_notification, name="view_notification"),
]
