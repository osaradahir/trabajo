from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.signin, name="login"), # documentado

    # Registro consultor
    path('registro', views.register, name="registre"), # documentado
    path('add/contacto', views.addContacto, name="contacto"), # documentado
    path('add/profesion', views.addProfesion, name="profesion"), # documentado
    path('add/experiencia', views.addExperiencia, name="experiencia"), # documentado
    path('add/educacion', views.addEducation, name="educacion"), # documentado
    path('add/confirmacion', views.addConfirmacion, name="emailConfimacion"), # documentado
    path('felicitaciones', views.countCreated, name="countCreated"),
    path('consultor/', include('consultores.urls')),
    path('logout/', views.signout, name='logout'),
    path('administrador/', include('administradores.urls')),
    path('proyectos/', include('proyectos.urls')),
    path('empresas/', include('empresas.urls')),


    # Registro Administrador
    path('registroAdministrador', views.registerAdministrador, name="registroAdministrador"),
    path('add/contactoAdministrador', views.addContactoAdministrador, name="contactoAdministrador"),


    # Registro Empresa
    path('registroEmpresa', views.registerEmpresa, name="registroEmpresa"),
    path('add/detallesEmpresa', views.addDetallesEmpresa, name="detallesEmpresa"),
]
