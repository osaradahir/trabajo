from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, UsuariosManager, Empresas, NivelesConocimiento
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from urllib.parse import urlencode
from .config import cipher_suite
from cryptography.fernet import Fernet
from datetime import datetime
from datetime import date
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    return render(request, 'index.html')


def signin(request):
    try:
        if request.method == 'GET':
            return render(request, 'login/login.html')
        else:
            user = authenticate(
                request, correo=request.POST['correo'], password=request.POST['password'])

            if user is None:
                return render(request, 'login/login.html', {
                    'error': 'Usuario o Contraseña incorrectos'
                })
            else:
                if user.validacion:
                    login(request, user)
                    # Guardar el nombre de usuario en la sesión
                    request.session['username'] = user.correo
                    if 'remind_user' in request.POST:
                        # Duración de sesión más larga (por ejemplo, 30 días)
                        request.session.set_expiry(30 * 24 * 60 * 60)
                    else:
                        # Duración de sesión más corta (por ejemplo, 1 día)
                        request.session.set_expiry(24 * 60 * 60)
                    
                    if user.is_superuser:
                        return redirect('administrador/principal')
                    else:
                        if user.rol == 'Consultor':
                            # print("consultor")
                            return redirect('consultor/principal')
                        else:
                            # print("empresa")
                            return redirect('proyectos/misProyectos')
                else:
                    return render(request, 'login/login.html', {
                        'error': 'El nombre de usuario no esta registrado en Gnosis'
                    })

    except Exception as e:
            print(e)
            messages.error(
                request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
            return redirect('login')

def register(request):
    if request.method == 'GET':
        return render(request, 'login/registry.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = Usuarios.objects.get(correo=request.POST['correo'])
                return render(request, 'login/registry.html', {
                    'error': 'Username Already Exists'
                })
            except Usuarios.DoesNotExist:
                if 'accepted' in request.POST:
                    if request.POST.get('nombre') != '' and request.POST.get('ape_pat') != '' and request.POST.get('correo') != '' and request.POST.get('password1') != '' and request.POST.get('password2') != '':
                        name_value = request.POST['nombre']
                        apepa_value = request.POST['ape_pat']
                        apema_value = request.POST['ape_mat']
                        correo_value = request.POST['correo']
                        password_value = request.POST['password1']
                        # for key, value in request.POST.items():
                            # print(f"{key}: {value}")
                        # También puedes imprimir todo el diccionario completo
                        # print(request.POST)
                        params = {
                            'name':  cipher_suite.encrypt(name_value.encode('utf-8')).decode('utf-8'),
                            'apepa': cipher_suite.encrypt(apepa_value.encode('utf-8')).decode('utf-8'),
                            'apema': cipher_suite.encrypt(apema_value.encode('utf-8')).decode('utf-8'),
                            'email': cipher_suite.encrypt(correo_value.encode('utf-8')).decode('utf-8'),
                            'password': cipher_suite.encrypt(password_value.encode('utf-8')).decode('utf-8'),
                        }
                        query_string = urlencode(params)
                        url = reverse('contacto') + '?' + query_string
                        return HttpResponseRedirect(url)
                    else:
                        return render(request, 'login/registry.html', {
                            'error': 'Necesitas llenar todos los campos requeridos'
                        })
                else:
                    return render(request, 'login/registry.html', {
                        'error': 'Debes aceptar los Terminos y Condiciones primero'
                    })
        else:
            return render(request, 'login/registry.html', {
                'error': 'Las contraseñas no coinciden'
            })


def addContacto(request):
    try:
        if request.method == 'GET':
            return render(request, 'login/contact.html')
        else:
            if request.POST.get('telefono') != '' and request.POST.get('pais') != '' and request.POST.get('cod_post') != '' and request.POST.get('estado') != '' and request.POST.get('fecha_nacimiento') != '' and request.POST.get('genero') != '' and request.POST.get('disponibilidad') != '':
                # print(request.POST['telefono'])

                params = {
                    'telefono':  cipher_suite.encrypt(request.POST.get('telefono').encode('utf-8')).decode('utf-8'),
                    'pais': cipher_suite.encrypt(request.POST.get('pais').encode('utf-8')).decode('utf-8'),
                    'cod_post': cipher_suite.encrypt(request.POST.get('cod_post').encode('utf-8')).decode('utf-8'),
                    'estado': cipher_suite.encrypt(request.POST.get('estado').encode('utf-8')).decode('utf-8'),
                    'ciudad': cipher_suite.encrypt(request.POST.get('ciudad').encode('utf-8')).decode('utf-8'),
                    'municipio': cipher_suite.encrypt(request.POST.get('municipio').encode('utf-8')).decode('utf-8'),
                    'colonia': cipher_suite.encrypt(request.POST.get('colonia').encode('utf-8')).decode('utf-8'),
                    'fecha_nacimiento': cipher_suite.encrypt(request.POST.get('fecha_nacimiento').encode('utf-8')).decode('utf-8'),
                    'genero': cipher_suite.encrypt(request.POST.get('genero').encode('utf-8')).decode('utf-8'),
                    'disponibilidad': cipher_suite.encrypt(request.POST.get('disponibilidad').encode('utf-8')).decode('utf-8'),
                }
                # for key, value in request.POST.items():
                    # print(f"{key}: {value}")
                    # También puedes imprimir todo el diccionario completo
                # print(request.POST)
                query_string = urlencode(params)
                url = reverse('profesion') + '?' + request.GET.urlencode() + '&' + query_string
                return redirect(url)

            else:
                return render(request, 'login/contact.html', {
                    'error': 'Necesitas llenar todos los campos requeridos'
                })

    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


def addProfesion(request):
    try:
        encrypted_name = request.GET.get('name').encode('utf-8')
        encrypted_apepa = request.GET.get('apepa').encode('utf-8')
        encrypted_apema = request.GET.get('apema').encode('utf-8')
        encrypted_correo = request.GET.get('email').encode('utf-8')
        encrypted_contrasena = request.GET.get('password').encode('utf-8')
        decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
        decrypted_apepa = cipher_suite.decrypt(encrypted_apepa).decode('utf-8')
        decrypted_apema = cipher_suite.decrypt(encrypted_apema).decode('utf-8')
        decrypted_correo = cipher_suite.decrypt(
            encrypted_correo).decode('utf-8')
        decrypted_password = cipher_suite.decrypt(
            encrypted_contrasena).decode('utf-8')

        encrypted_telefono = request.GET.get('telefono').encode('utf-8')
        decrypted_telefono = cipher_suite.decrypt(encrypted_telefono).decode('utf-8')
        encrypted_pais = request.GET.get('pais').encode('utf-8')
        decrypted_pais = cipher_suite.decrypt(encrypted_pais).decode('utf-8')
        encrypted_cod_post = request.GET.get('cod_post').encode('utf-8')
        decrypted_cod_post = cipher_suite.decrypt(encrypted_cod_post).decode('utf-8')
        encrypted_estado = request.GET.get('estado').encode('utf-8')
        decrypted_estado= cipher_suite.decrypt(encrypted_estado).decode('utf-8')
        encrypted_ciudad = request.GET.get('ciudad').encode('utf-8')
        decrypted_ciudad = cipher_suite.decrypt(encrypted_ciudad).decode('utf-8')
        encrypted_municipio = request.GET.get('municipio').encode('utf-8')
        decrypted_municipio = cipher_suite.decrypt(encrypted_municipio).decode('utf-8')
        encrypted_colonia = request.GET.get('colonia').encode('utf-8')
        decrypted_colonia = cipher_suite.decrypt(encrypted_colonia).decode('utf-8')
        encrypted_fecha_nacimiento = request.GET.get('fecha_nacimiento').encode('utf-8')
        decrypted_fecha_nacimiento = cipher_suite.decrypt(encrypted_fecha_nacimiento).decode('utf-8')
        encrypted_genero = request.GET.get('genero').encode('utf-8')
        decrypted_genero = cipher_suite.decrypt(encrypted_genero).decode('utf-8')
        encrypted_disponibilidad = request.GET.get('disponibilidad').encode('utf-8')
        decrypted_disponibilidad = cipher_suite.decrypt(encrypted_disponibilidad).decode('utf-8')


        if request.method == 'GET':
            # print(decrypted_name)
            monedaCobro = list(TipoMoneda.objects.values())
            maneraPago = list(ManeraPago.objects.values())
            niveles = list(NivelesConocimiento.objects.values())
            return render(request, 'login/profession.html', {
                'monedaCobro': monedaCobro,
                'maneraPago': maneraPago,
                'niveles':niveles
            })
        else:
            if request.POST.get('puesto') != '' and request.POST.get('tipo_moneda') != '' and request.POST.get('Tarifa') != '' and request.POST.get('forma_cobro') != '' and request.POST.get('RFC') != '' and 'accepted_emails' in request.POST and request.POST.get('tipo_moneda') != '' and request.POST.get('SAP') != '' and request.POST.get('experiencia') != '':

                persona = Personas(nombre=decrypted_name, ape_pat=decrypted_apepa, ape_mat=decrypted_apema, fecha_nacimiento=decrypted_fecha_nacimiento, ciudad=decrypted_ciudad, cod_post=decrypted_cod_post, estado=decrypted_estado, pais=decrypted_pais, telefono=decrypted_telefono, sexo=decrypted_genero, municipio=decrypted_municipio, colonia=decrypted_colonia, disponible=int(decrypted_disponibilidad))
                persona.save()
                user = Usuarios.objects.create_user(
                    correo=decrypted_correo, password=decrypted_password, id_persona=persona, rol='Consultor')
                user.save()


                user = Usuarios.objects.get(correo=decrypted_correo)
                persona = Personas.objects.get(pk=user.id_persona_id)
                pago = ManeraPago.objects.get(pk=request.POST['forma_cobro'])
                moneda = TipoMoneda.objects.get(pk=request.POST['tipo_moneda'])
                nivel = NivelesConocimiento.objects.get(pk=request.POST['experiencia'])

                consultores = Consultores(
                    tipo_persona='Fisica', rfc=request.POST['RFC'], tarifa_hora=int(request.POST['Tarifa']), id_persona=persona, id_manera_pago=pago, id_tipo_moneda=moneda, especialidad=request.POST.get('SAP'), id_nivel=nivel)
                consultores.save()

                params = {
                    'name':  cipher_suite.encrypt(decrypted_name.encode('utf-8')).decode('utf-8'),
                    'apepa': cipher_suite.encrypt(decrypted_apepa.encode('utf-8')).decode('utf-8'),
                    'apema': cipher_suite.encrypt(decrypted_apema.encode('utf-8')).decode('utf-8'),
                    'email': cipher_suite.encrypt(decrypted_correo.encode('utf-8')).decode('utf-8'),
                    'password': cipher_suite.encrypt(decrypted_password.encode('utf-8')).decode('utf-8'),
                }
                # for key, value in request.POST.items():
                    # print(f"{key}: {value}")
                    # También puedes imprimir todo el diccionario completo
                # print(request.POST)
                query_string = urlencode(params)
                url = reverse('experiencia') + '?' + query_string
                return HttpResponseRedirect(url)
            else:
                return render(request, 'login/profession.html', {
                    'error': 'Necesitas llenar todos los campos requeridos'
                })
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


def addExperiencia(request):
    try:
        encrypted_name = request.GET.get('name').encode('utf-8')
        encrypted_apepa = request.GET.get('apepa').encode('utf-8')
        encrypted_apema = request.GET.get('apema').encode('utf-8')
        encrypted_correo = request.GET.get('email').encode('utf-8')
        encrypted_contrasena = request.GET.get('password').encode('utf-8')

        decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
        decrypted_apepa = cipher_suite.decrypt(encrypted_apepa).decode('utf-8')
        decrypted_apema = cipher_suite.decrypt(encrypted_apema).decode('utf-8')
        decrypted_correo = cipher_suite.decrypt(
            encrypted_correo).decode('utf-8')
        decrypted_password = cipher_suite.decrypt(
            encrypted_contrasena).decode('utf-8')

        if request.method == 'GET':
            # print(decrypted_name)
            user = Usuarios.objects.get(correo=decrypted_correo)
            idUser = user.id_persona
            # print(idUser)

            consultor = Consultores.objects.get(id_persona=idUser)
            # print()
            # print(consultor)
            persona = Personas.objects.get(pk=user.id_persona_id)
            return render(request, 'login/experience.html', {
                'fechaNacimiento': persona.fecha_nacimiento
            })
        else:
            if request.POST.get('puesto') != '' and request.POST.get('empresa') != '' and request.POST.get('fecha_entrada') != '' and request.POST.get('activities') != '':
                experiencia = Experiencias(nombre=request.POST['puesto'])
                experiencia.save()

                user = Usuarios.objects.get(correo=decrypted_correo)
                idUser = user.id_persona
                # print(idUser)

                consultor = Consultores.objects.get(id_persona=idUser)
                # print()
                # print(consultor)
                persona = Personas.objects.get(pk=user.id_persona_id)

                fecha_entrada_str = request.POST['fecha_entrada']
                fecha_entrada = datetime.strptime(
                    fecha_entrada_str, '%Y-%m-%d')
                fecha_salida = date.today()
                if 'chec' in request.POST:
                    tiempoExperiencia = 'Sigue Trabajando'
                else:
                    fecha_salida_str = request.POST['fecha_salida']
                    if fecha_salida_str:
                        fecha_salida = datetime.strptime(
                            fecha_salida_str, '%Y-%m-%d')
                        diferencia = fecha_salida - fecha_entrada
                        tiempoExperiencia = diferencia.days
                    else:
                        return render(request, 'login/experience.html', {
                            'error': 'Proporcione la fecha de salida'
                        })

                experienciaConsultor = ExperienciasConsultor(id_experiencia_id=experiencia.id, empresa=request.POST['empresa'], puesto=request.POST['puesto'], descripcion=request.POST[
                                                             'activities'], tiempo_experiencia=tiempoExperiencia, id_consultor_id=consultor.id, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida)
                experienciaConsultor.save()

                params = {
                    'name':  cipher_suite.encrypt(decrypted_name.encode('utf-8')).decode('utf-8'),
                    'apepa': cipher_suite.encrypt(decrypted_apepa.encode('utf-8')).decode('utf-8'),
                    'apema': cipher_suite.encrypt(decrypted_apema.encode('utf-8')).decode('utf-8'),
                    'email': cipher_suite.encrypt(decrypted_correo.encode('utf-8')).decode('utf-8'),
                    'password': cipher_suite.encrypt(decrypted_password.encode('utf-8')).decode('utf-8'),
                }
                # for key, value in request.POST.items():
                    # print(f"{key}: {value}")
                    # También puedes imprimir todo el diccionario completo
                # print(request.POST)
                query_string = urlencode(params)
                if 'save' in request.POST:
                    url = reverse('educacion') + '?' + query_string
                    return HttpResponseRedirect(url)
                else:
                    url = reverse('experiencia') + '?' + query_string
                    return HttpResponseRedirect(url)
            else:
                return render(request, 'login/experience.html', {
                    'error': 'Debes llenar todos los campos primero'
                })

    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


def addEducation(request):
    try:
        encrypted_name = request.GET.get('name').encode('utf-8')
        encrypted_apepa = request.GET.get('apepa').encode('utf-8')
        encrypted_apema = request.GET.get('apema').encode('utf-8')
        encrypted_correo = request.GET.get('email').encode('utf-8')
        encrypted_contrasena = request.GET.get('password').encode('utf-8')

        decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
        decrypted_apepa = cipher_suite.decrypt(encrypted_apepa).decode('utf-8')
        decrypted_apema = cipher_suite.decrypt(encrypted_apema).decode('utf-8')
        decrypted_correo = cipher_suite.decrypt(
            encrypted_correo).decode('utf-8')
        decrypted_password = cipher_suite.decrypt(
            encrypted_contrasena).decode('utf-8')

        if request.method == 'GET':
            user = Usuarios.objects.get(correo=decrypted_correo)
            idUser = user.id_persona
            # print(idUser)

            consultor = Consultores.objects.get(id_persona=idUser)
            # print()
            # print(consultor)
            persona = Personas.objects.get(pk=user.id_persona_id)
            return render(request, 'login/education.html', {
                'fechaNacimiento': persona.fecha_nacimiento
            })
        else:
            if request.POST.get('nivel') != '' and request.POST.get('institucion') != '' and request.POST.get('titulo') != '' and request.POST.get('ano_inicio') != '':

                if Instituciones.objects.filter(nombre=request.POST['institucion']).exists():
                    # Se encontró la institución
                    institucion = Instituciones.objects.get(
                        nombre=request.POST['institucion'])
                else:
                    # No se encontró la institución
                    institucion = Instituciones(
                        nombre=request.POST['institucion'])
                    institucion.save()

                user = Usuarios.objects.get(correo=decrypted_correo)
                idUser = user.id_persona
                # print(idUser)
                consultor = Consultores.objects.get(id_persona=idUser)

                if 'chec' in request.POST:
                    estudios = Estudios(id_institucion=institucion,
                                        titulo_registrado=request.POST['titulo'], id_consultor=consultor, fecha_ingreso=request.POST['ano_inicio'], fecha_termino='Estudiando', educacion=request.POST['nivel'])
                else:
                    estudios = Estudios(id_institucion=institucion,
                                        titulo_registrado=request.POST['titulo'], id_consultor=consultor, fecha_ingreso=request.POST['ano_inicio'], fecha_termino=request.POST['ano_termino'], educacion=request.POST['nivel'])

                estudios.save()

                params = {
                    'name':  cipher_suite.encrypt(decrypted_name.encode('utf-8')).decode('utf-8'),
                    'apepa': cipher_suite.encrypt(decrypted_apepa.encode('utf-8')).decode('utf-8'),
                    'apema': cipher_suite.encrypt(decrypted_apema.encode('utf-8')).decode('utf-8'),
                    'email': cipher_suite.encrypt(decrypted_correo.encode('utf-8')).decode('utf-8'),
                    'password': cipher_suite.encrypt(decrypted_password.encode('utf-8')).decode('utf-8'),
                }
                # for key, value in request.POST.items():
                    # print(f"{key}: {value}")
                    # También puedes imprimir todo el diccionario completo
                # print(request.POST)
                query_string = urlencode(params)
                url = reverse('emailConfimacion') + '?' + query_string
                # enviar email de confirmacion
                sendemail(decrypted_correo, decrypted_name)
                return HttpResponseRedirect(url)
            else:
                return render(request, 'login/education.html', {
                    'error': 'Debes llenar todos los campos primero'
                })

    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


def addConfirmacion(request):
    try:
        encrypted_name = request.GET.get('name').encode('utf-8')
        encrypted_apepa = request.GET.get('apepa').encode('utf-8')
        encrypted_apema = request.GET.get('apema').encode('utf-8')
        encrypted_correo = request.GET.get('email').encode('utf-8')
        encrypted_contrasena = request.GET.get('password').encode('utf-8')

        decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
        decrypted_apepa = cipher_suite.decrypt(encrypted_apepa).decode('utf-8')
        decrypted_apema = cipher_suite.decrypt(encrypted_apema).decode('utf-8')
        decrypted_correo = cipher_suite.decrypt(
            encrypted_correo).decode('utf-8')
        decrypted_password = cipher_suite.decrypt(
            encrypted_contrasena).decode('utf-8')

        return render(request, 'login/hotmail_conffirm.html', {
            'correo': decrypted_correo
        })
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


def countCreated(request):
    return render(request, 'login/count_created.html')


def sendemail(email, name):
    to = email
    name = name
    # se envian los datos al email template
    html_content = render_to_string(
        "emails/email_template.html", {"name": name}
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        # nombre que tendra el correo
        "Gnosis [Autenticación de Correo]",
        # texto contenido
        text_content,
        # conexion con settings y el host user
        settings.EMAIL_HOST_USER,
        # rec list
        [to],
    )
    
    # se indica que se convierta como html
    email.attach_alternative(html_content, "text/html")
    # se envia el correo
    email.send()
    return "Correo enviado"



def decrypt_value(cipher_suite, encrypted_value):
    decrypted_value = cipher_suite.decrypt(
        encrypted_value.encode('utf-8')).decode('utf-8')
    return decrypted_value


@login_required
def signout(request):
    logout(request)
    return redirect('login')





def registerAdministrador(request):
    if request.method == 'GET':
        return render(request, 'login/registryAdmin.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = Usuarios.objects.get(correo=request.POST['correo'])
                return render(request, 'login/registryAdmin.html', {
                    'error': 'Username Already Exists'
                })
            except Usuarios.DoesNotExist:
                if 'accepted' in request.POST:
                    if request.POST.get('nombre') != '' and request.POST.get('ape_pat') != '' and request.POST.get('correo') != '' and request.POST.get('password1') != '' and request.POST.get('password2') != '':
                        name_value = request.POST['nombre']
                        apepa_value = request.POST['ape_pat']
                        apema_value = request.POST['ape_mat']
                        correo_value = request.POST['correo']
                        password_value = request.POST['password1']

                        params = {
                            'name':  cipher_suite.encrypt(name_value.encode('utf-8')).decode('utf-8'),
                            'apepa': cipher_suite.encrypt(apepa_value.encode('utf-8')).decode('utf-8'),
                            'apema': cipher_suite.encrypt(apema_value.encode('utf-8')).decode('utf-8'),
                            'email': cipher_suite.encrypt(correo_value.encode('utf-8')).decode('utf-8'),
                            'password': cipher_suite.encrypt(password_value.encode('utf-8')).decode('utf-8'),
                        }
                        query_string = urlencode(params)
                        url = reverse('contactoAdministrador') + '?' + query_string
                        return HttpResponseRedirect(url)
                    else:
                        return render(request, 'login/registryAdmin.html', {
                            'error': 'Necesitas llenar todos los campos requeridos'
                        })
                else:
                    return render(request, 'login/registryAdmin.html', {
                        'error': 'Debes aceptar los Terminos y Condiciones primero'
                    })
        else:
            return render(request, 'login/registryAdmin.html', {
                'error': 'Las contraseñas no coinciden'
            })


def addContactoAdministrador(request):
    try:

        if request.method == 'GET':
            return render(request, 'login/contact.html')
        else:
            if request.POST.get('telefono') != '' and request.POST.get('pais') != '' and request.POST.get('cod_post') != '' and request.POST.get('estado') != '' and request.POST.get('fecha_nacimiento') != '' and request.POST.get('genero') != '' and request.POST.get('disponibilidad') != '':
                # print(request.POST['telefono'])

                encrypted_name = request.GET.get('name').encode('utf-8')
                encrypted_apepa = request.GET.get('apepa').encode('utf-8')
                encrypted_apema = request.GET.get('apema').encode('utf-8')
                encrypted_correo = request.GET.get('email').encode('utf-8')
                encrypted_contrasena = request.GET.get('password').encode('utf-8')

                decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
                decrypted_apepa = cipher_suite.decrypt(encrypted_apepa).decode('utf-8')
                decrypted_apema = cipher_suite.decrypt(encrypted_apema).decode('utf-8')
                decrypted_correo = cipher_suite.decrypt(
                    encrypted_correo).decode('utf-8')
                decrypted_password = cipher_suite.decrypt(
                    encrypted_contrasena).decode('utf-8')

                persona = Personas(nombre=decrypted_name, ape_pat=decrypted_apepa, ape_mat=decrypted_apema, fecha_nacimiento=request.POST.get('fecha_nacimiento'), ciudad=request.POST.get('ciudad'), cod_post=request.POST.get('cod_post'), estado=request.POST.get('estado'), pais=request.POST.get('pais'), telefono=request.POST.get('telefono'), sexo=request.POST.get('genero'), municipio=request.POST.get('municipio'), colonia=request.POST.get('colonia'), disponible=int(request.POST.get('disponibilidad')))
                persona.save()


                # Crea un nuevo superusuario
                superusuario = Usuarios.objects.create_superuser(correo=decrypted_correo, password=decrypted_password, image='', rol='Administrador', id_persona=persona)

                # Guarda el superusuario en la base de datos
                superusuario.save()
                url = reverse('login')
                return redirect(url)
            else:
                return render(request, 'login/contact.html', {
                    'error': 'Necesitas llenar todos los campos requeridos'
                })

    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')




def registerEmpresa(request):
    if request.method == 'GET':
        return render(request, 'login/registryEmpresa.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = Usuarios.objects.get(correo=request.POST['correo'])
                return render(request, 'login/registryEmpresa.html', {
                    'error': 'Username Already Exists'
                })
            except Usuarios.DoesNotExist:
                if 'accepted' in request.POST:
                    if request.POST.get('nombre') != '' and request.POST.get('ape_pat') != '' and request.POST.get('correo') != '' and request.POST.get('password1') != '' and request.POST.get('password2') != '':
                        name_value = request.POST['nombre']
                        apepa_value = request.POST['ape_pat']
                        apema_value = request.POST['ape_mat']
                        correo_value = request.POST['correo']
                        password_value = request.POST['password1']

                        params = {
                            'name':  cipher_suite.encrypt(name_value.encode('utf-8')).decode('utf-8'),
                            'apepa': cipher_suite.encrypt(apepa_value.encode('utf-8')).decode('utf-8'),
                            'apema': cipher_suite.encrypt(apema_value.encode('utf-8')).decode('utf-8'),
                            'email': cipher_suite.encrypt(correo_value.encode('utf-8')).decode('utf-8'),
                            'password': cipher_suite.encrypt(password_value.encode('utf-8')).decode('utf-8'),
                        }
                        query_string = urlencode(params)
                        url = reverse('detallesEmpresa') + '?' + query_string
                        return HttpResponseRedirect(url)
                    else:
                        return render(request, 'login/registryEmpresa.html', {
                            'error': 'Necesitas llenar todos los campos requeridos'
                        })
                else:
                    return render(request, 'login/registryEmpresa.html', {
                        'error': 'Debes aceptar los Terminos y Condiciones primero'
                    })
        else:
            return render(request, 'login/registryEmpresa.html', {
                'error': 'Las contraseñas no coinciden'
            })



def addDetallesEmpresa(request):
    try:
        encrypted_name = request.GET.get('name').encode('utf-8')
        encrypted_apepa = request.GET.get('apepa').encode('utf-8')
        encrypted_apema = request.GET.get('apema').encode('utf-8')
        encrypted_correo = request.GET.get('email').encode('utf-8')
        encrypted_contrasena = request.GET.get('password').encode('utf-8')

        decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
        decrypted_apepa = cipher_suite.decrypt(encrypted_apepa).decode('utf-8')
        decrypted_apema = cipher_suite.decrypt(encrypted_apema).decode('utf-8')
        decrypted_correo = cipher_suite.decrypt(
                    encrypted_correo).decode('utf-8')
        decrypted_password = cipher_suite.decrypt(
                    encrypted_contrasena).decode('utf-8')


        if request.method == 'GET':
            return render(request, 'login/detallesEmpresa.html')
        else:
            if request.POST.get('nombreEmpresa') != '' and request.POST.get('nivel') != '' and request.POST.get('industria') != '' and request.POST.get('sapVersion') != '' and request.POST.get('telefono') != '' and request.POST.get('tamano') != '' and request.POST.get('pais') != '' and request.POST.get('cod_post') != '' and request.POST.get('estado') != '':

                usuario = Usuarios.objects.create_user(correo=decrypted_correo, password=decrypted_password, image='', rol='Empresa')
                usuario.save()

                empresa = Empresas(empresa=request.POST.get('nombreEmpresa'), nivel=request.POST.get('nivel'), nombre=decrypted_name, ape_pat=decrypted_apepa, ape_mat=decrypted_apema, telefono=request.POST.get('telefono'), tamano=request.POST.get('tamano'), industria=request.POST.get('industria'), versionSAP=request.POST.get('sapVersion'), id_usuario=usuario, pais=request.POST.get('pais'), estado=request.POST.get('estado'), cod_post=request.POST.get('cod_post'), ciudad=request.POST.get('ciudad'), municipio=request.POST.get('municipio'), colonia=request.POST.get('colonia'), calle=request.POST.get('calle'),n_exterior=request.POST.get('nExterior'), fax=request.POST.get('fax'))
                empresa.save()
                url = reverse('login')
                return redirect(url)
            else:
                return render(request, 'login/detallesEmpresa.html', {
                    'error': 'Necesitas llenar todos los campos requeridos'
                })

    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')