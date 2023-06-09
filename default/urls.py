from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.signin, name="login"),
    path('registro', views.register, name="registre"),
    path('add/contacto', views.addContacto, name="contacto"),
    path('add/profesion', views.addProfesion, name="profesion"),
    path('add/experiencia', views.addExperiencia, name="experiencia"),
    path('add/educacion', views.addEducation, name="educacion"),
    path('add/confirmacion', views.addConfirmacion, name="emailConfimacion"),
    path('felicitaciones', views.countCreated, name="countCreated"),
    path('consultor/', include('consultores.urls')),
    path('logout/', views.signout, name='logout'),
]
