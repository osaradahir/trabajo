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
]
