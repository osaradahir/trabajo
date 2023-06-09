from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
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


def index(request):
    title = "Gnosis"
    return render(request, 'index.html')


def signin(request):
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
            login(request, user)
            # Guardar el nombre de usuario en la sesión
            request.session['username'] = user.correo
            if 'remind_user' in request.POST:
                # Duración de sesión más larga (por ejemplo, 30 días)
                request.session.set_expiry(30 * 24 * 60 * 60)
            else:
                # Duración de sesión más corta (por ejemplo, 1 día)
                request.session.set_expiry(24 * 60 * 60)
            return redirect('consultor/miperfil')


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
            return render(request, 'login/contact.html')
        else:
            if request.POST.get('telefono') != '' and request.POST.get('pais') != '' and request.POST.get('cod_post') != '' and request.POST.get('estado') != '' and request.POST.get('fecha_nacimiento') != '' and request.POST.get('genero') != '' and request.POST.get('disponibilidad') != '':
                # print(request.POST['telefono'])
                persona = Personas(nombre=decrypted_name, ape_pat=decrypted_apepa, ape_mat=decrypted_apema, fecha_nacimiento=request.POST['fecha_nacimiento'], ciudad=request.POST[
                    'ciudad'], cod_post=request.POST['cod_post'], estado=request.POST['estado'], pais=request.POST['pais'], telefono=request.POST['telefono'], sexo=request.POST['genero'], municipio=request.POST['municipio'], colonia=request.POST['colonia'])
                persona.save()
                user = Usuarios.objects.create_user(
                    correo=decrypted_correo, password=decrypted_password, id_persona=persona)
                user.save()

                params = {
                    'name':  cipher_suite.encrypt(decrypted_name.encode('utf-8')).decode('utf-8'),
                    'apepa': cipher_suite.encrypt(decrypted_apepa.encode('utf-8')).decode('utf-8'),
                    'apema': cipher_suite.encrypt(decrypted_apema.encode('utf-8')).decode('utf-8'),
                    'email': cipher_suite.encrypt(decrypted_correo.encode('utf-8')).decode('utf-8'),
                    'password': cipher_suite.encrypt(decrypted_password.encode('utf-8')).decode('utf-8'),
                }
                query_string = urlencode(params)
                url = reverse('profesion') + '?' + query_string
                return HttpResponseRedirect(url)
            else:
                return render(request, 'login/contact.html', {
                    'error': 'Necesitas llenar todos los campos requeridos'
                })

    except Exception as e:
        print(e)
        return render(request, 'login/registry.html', {
            'error': 'Algo salio mal a la hora de procesar'
        })


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

        if request.method == 'GET':
            # print(decrypted_name)
            monedaCobro = list(TipoMoneda.objects.values())
            maneraPago = list(ManeraPago.objects.values())
            return render(request, 'login/profession.html', {
                'monedaCobro': monedaCobro,
                'maneraPago': maneraPago
            })
        else:
            if request.POST.get('puesto') != '' and request.POST.get('tipo_moneda') != '' and request.POST.get('Tarifa') != '' and request.POST.get('forma_cobro') != '' and request.POST.get('RFC') != '' and request.POST.get('SAP') != '' and 'accepted_emails' in request.POST and request.POST.get('tipo_moneda') != '':
                user = Usuarios.objects.get(correo=decrypted_correo)
                persona = Personas.objects.get(pk=user.id_persona_id)
                pago = ManeraPago.objects.get(pk=request.POST['forma_cobro'])
                moneda = TipoMoneda.objects.get(pk=request.POST['tipo_moneda'])
                """
                Pendientes
                    - submodulo de especialidad SAP
                """
                consultores = Consultores(
                    tipo_persona='Fisica', rfc=request.POST['RFC'], tarifa_hora=request.POST['Tarifa'], id_persona=persona, id_manera_pago=pago, id_tipo_moneda=moneda)
                consultores.save()

                params = {
                    'name':  cipher_suite.encrypt(decrypted_name.encode('utf-8')).decode('utf-8'),
                    'apepa': cipher_suite.encrypt(decrypted_apepa.encode('utf-8')).decode('utf-8'),
                    'apema': cipher_suite.encrypt(decrypted_apema.encode('utf-8')).decode('utf-8'),
                    'email': cipher_suite.encrypt(decrypted_correo.encode('utf-8')).decode('utf-8'),
                    'password': cipher_suite.encrypt(decrypted_password.encode('utf-8')).decode('utf-8'),
                }
                query_string = urlencode(params)
                url = reverse('experiencia') + '?' + query_string
                return HttpResponseRedirect(url)
            else:
                return render(request, 'login/profession.html', {
                    'error': 'Necesitas llenar todos los campos requeridos'
                })
    except Exception as e:
        print(e)
        return render(request, 'login/profession.html', {
            'error': 'Algo salio mal a la hora de procesar'
        })


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
        return render(request, 'login/experience.html', {
            'error': 'Algo salio mal al procesar'
        })


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

                """
                    Pendientes
                        - Consultar Institucion
                        - Consultar Carrera
                        - Consultar nivel

                        - Relacionar modelo.Niveles y modelo.Conocimientos y modelo.conocimientosConsultores
                """

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
                query_string = urlencode(params)
                url = reverse('emailConfimacion') + '?' + query_string
                # enviar email de confirmacion
                # sendemail(decrypted_correo, decrypted_name)
                return HttpResponseRedirect(url)
            else:
                return render(request, 'login/education.html', {
                    'error': 'Debes llenar todos los campos primero'
                })

    except Exception as e:
        print(e)
        return render(request, 'login/education.html', {
            'error': 'Algo salio mal al procesar'
        })


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
        return render(request, 'login/education.html', {
            'error': 'Algo salio mal al procesar'
        })


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

# Función para descifrar los valores cifrados


def decrypt_value(cipher_suite, encrypted_value):
    decrypted_value = cipher_suite.decrypt(
        encrypted_value.encode('utf-8')).decode('utf-8')
    return decrypted_value


@login_required
def signout(request):
    logout(request)
    return redirect('login')
