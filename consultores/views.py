from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor, NotificationConsultor, NotificationAdministrador, Proyectos, RequerimientosModulosProyecto, Empresas, EmpresaProyecto, PostulacionesProyecto, NotificationEmpresa, RequerimientosIdiomasProyecto, EntrevistasConsultoresProyecto, ProyectoConsultor, DatosBancarios, Bancos, Hijos, Documentacion, TipoDocumento, Contratos, Facturas, ReporteHoras, ReporteFinalActividades
import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from datetime import date
from datetime import datetime
import calendar
from django.contrib.auth import login, logout, authenticate
import os, json
from django.http import HttpResponseRedirect
from default import views
from django.core.paginator import Paginator
from pytz import timezone
import shutil
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
import os
from pathlib import Path
# CREATE PDFS
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
BASE_DIR = Path(__file__).resolve().parent.parent

@login_required
def miProfile(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        # print(request.session)
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        # # print(informationPersonalUser)
        edad = calcular_edad(informationPersonalUser.fecha_nacimiento)
        maneraPago2 = ManeraPago.objects.get(
            pk=informationConsultorUser.id_manera_pago_id)

        tipoMoneda = TipoMoneda.objects.get(
            pk=informationConsultorUser.id_tipo_moneda_id)
        codigo_moneda = tipoMoneda.tipo.split('(')[1].split(')')[0]

        experienciasConsultor2 = ExperienciasConsultor.objects.filter(id_consultor=informationConsultorUser)
        if experienciasConsultor2:
            myExperience = []
            a=0
            for experience in experienciasConsultor2:
                id = experience.id
                descripcion = experience.descripcion
                empresa = experience.empresa
                puesto = experience.puesto
                experienciaInicio = obtener_mes(experience.fecha_entrada)
                experienciaTermino = obtener_mes(experience.fecha_salida)
                if experience.tiempo_experiencia == 'Sigue Trabajando' or experience.tiempo_experiencia == '0':
                    experienciaTermino = 'En proceso'
                a=a+1
                myExperience.append([id, descripcion, empresa, puesto, experienciaInicio, experienciaTermino, a])
        else: 
            myExperience = []

        estudiosConsultor = Estudios.objects.filter(
            id_consultor=informationConsultorUser).order_by('-id').first()

        if estudiosConsultor:
            institucion = Instituciones.objects.get(pk=estudiosConsultor.id_institucion_id)
            educacionInicio = obtener_mes(estudiosConsultor.fecha_ingreso)

            if estudiosConsultor.fecha_termino == 'Sigue Estudiando':
                educacionTermino = 'En proceso'
            elif len(estudiosConsultor.fecha_termino) == 10 and estudiosConsultor.fecha_termino[4] == '-' and estudiosConsultor.fecha_termino[7] == '-':
                # 2021-12-17
                componentes = estudiosConsultor.fecha_termino.split('-')
                meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

                educacionTermino = meses[int(
                    componentes[1])-1] + ' ' + componentes[0]
            else:
                fecha = datetime.strptime(
                    estudiosConsultor.fecha_termino, '%Y-%m-%d %H:%M:%S.%f')
                educacionTermino = obtener_mes(fecha)
        else:
            institucion = ''
            educacionInicio = ''
            educacionTermino = ''

        ruta = 'media/PDF/' + informationPersonalUser.pais + '/' + \
            informationConsultorUser.rfc + '/' + informationConsultorUser.rfc
        cv = ruta+'_CV.pdf'
        ine = ruta+'_INE.pdf'
        actaNac = ruta+'_Acta_Nacimiento.pdf'
        pasaporte = ruta+'_Pasaporte.pdf'
        domicilio = ruta+'_Comprobante_Domicilio.pdf'
        recomendacion = ruta+'_Carta_Recomendacion.pdf'
        f3 = ruta+'_F3.pdf'
        monedaCobro = list(TipoMoneda.objects.values())
        maneraPago = list(ManeraPago.objects.values())
        listaIdiomas = list(Idiomas.objects.values())
        listaModulos = list(Modulos.objects.values())
        listaSubodulos = list(Submodulos.objects.values())
        listaNivelesConocimiento = list(NivelesConocimiento.objects.values())
        # misIdiomas = list(IdiomasConsultor.objects.filter(id_consultor_id=informationConsultorUser.id))

        misIdiomas = IdiomasConsultor.objects.filter(
            id_consultor_id=informationConsultorUser.id)
        myLenguajes = []
    
        misModulos = ConocimientosConsultor.objects.filter(id_consultor_id=informationConsultorUser.id)
        myModuls = []


        myCourses = []
        c=0  
        cursosConsultor = CursosConsultor.objects.filter(id_consultor=informationConsultorUser)
        if cursosConsultor:
            for cursos in cursosConsultor:
                id = cursos.id
                nombre_curso = cursos.nombre_curso
                enlace_certificado = cursos.enlace_certificado
                descripcion = cursos.descripcion
                fecha_termino = obtener_mes(cursos.fecha_termino)
                institucionCurso = Instituciones.objects.get(pk=cursos.id_institucion_curso_id)
                institucionNombre = institucionCurso.nombre
                c=c+1
                myCourses.append([id, nombre_curso, enlace_certificado, descripcion, fecha_termino, institucionNombre,  c]) 
        else:
            myCourses = []

        if misIdiomas:
            for idioma in misIdiomas:
                id = idioma.id
                nombre_idioma = Idiomas.objects.get(pk=idioma.id_idioma_id)
                nivel = idioma.nivel.split()[1]
                myLenguajes.append([id, nombre_idioma, nivel])
        else:
            myLenguajes = []
        
        c = 0
        if misModulos:
            for moduloConsulta in misModulos:
                id = moduloConsulta.id
                modulo = Modulos.objects.get(pk=moduloConsulta.id_modulo_id)
                submodulo = Submodulos.objects.get(pk=moduloConsulta.id_submodulo_id)
                nivel = NivelesConocimiento.objects.get(pk=moduloConsulta.id_nivel_id)
                c = c+1
                myModuls.append([id, modulo, submodulo, nivel, c])
        else:
            myModuls = []



        notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
        pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')[:4]

        context = {
            'titulo': 'Mi perfil',
            'indice': 'Perfil',
            'image':user.image,
            'informationPersonalUser': informationPersonalUser,
            'correo': request.session.get('username'),
            'edad': edad,
            'maneraPago2': maneraPago2,
            'informationConsultorUser': informationConsultorUser,
            'maneraPago': maneraPago,
            'tipoMoneda': codigo_moneda,
            'myExperience':myExperience,
            'estudiosConsultor': estudiosConsultor,
            'cursosConsultor': cursosConsultor,
            'institucion': institucion,
            'myCourses':myCourses,
            'educacionInicio': educacionInicio,
            'educacionTermino': educacionTermino,
            'monedaCobro': monedaCobro,
            'maneraPago': maneraPago,
            'listaIdiomas': listaIdiomas,
            'misIdiomas': myLenguajes,
            'listaModulos':listaModulos,
            'listaSubodulos':listaSubodulos,
            'listaNivelesConocimiento':listaNivelesConocimiento,
            'misModulos':myModuls,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
            'files': [
                searchFile(cv), searchFile(ine), searchFile(actaNac), searchFile(
                    pasaporte), searchFile(domicilio), searchFile(recomendacion), searchFile(f3),
            ]
        }
        # # print(context)
        return render(request, 'miProfile.html', context)

    
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year
    if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    return edad


def obtener_mes(fecha):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    mes = fecha.month
    mes = int(mes)
    mesNumber = mes-1
    return meses[mesNumber] + ' ' + str(fecha.year)



@login_required
def upload_file(request):
    user = Usuarios.objects.get(correo=request.session.get('username'))
    informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
    informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        nameFile = request.POST.get('name', '')
        rfc = request.POST.get('rfc', '')

        directory = 'media/PDF/' + informationPersonalUser.pais + '/' + rfc

        # Verificar si el directorio existe, si no, crearlo
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Validar la extensión del archivo
        if not file.name.endswith('.pdf'):
            return render(request, 'miProfile.html', {
                'status': 'El archivo debe ser un PDF',
            })

        # Especificar el nombre del archivo
        new_filename = rfc + '_' + nameFile+'.pdf'

        # Combinar el directorio y el nuevo nombre de archivo
        new_filepath = os.path.join(directory, new_filename)

        # Guardar el archivo en el directorio "archivos" con el nuevo nombre
        with open(new_filepath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Buscar o crear el objeto TipoDocumento
        documento, created = TipoDocumento.objects.get_or_create(nombre=nameFile)

        # Buscar o crear el objeto Documentacion
        query, created = Documentacion.objects.get_or_create(
            id_consultor=informationConsultorUser,
            id_tipo_documento=documento,
            ruta=directory,
            nombre=new_filename,
            fecha_creacion=date.today()
        )


        return redirect('miProfile')
    else:
        return render(request, 'miProfile.html', {
            'status': 'No se proporciono ningun archivo',
        })

@login_required
def uploadImage(request):
    user = Usuarios.objects.get(correo=request.session.get('username'))
    informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
    informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

    if request.method == 'POST' and request.FILES.get('imagen'):
        imagen = request.FILES['imagen']
        ruta_destino = 'media/IMAGES/' + informationPersonalUser.pais + '/' + informationConsultorUser.rfc

        # Verificar si el directorio existe, si no, crearlo
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        nombre_archivo = informationConsultorUser.rfc +'.jpg'  # Puedes generar un nombre único si lo deseas
        ruta_archivo = os.path.join(ruta_destino, nombre_archivo)

        with open(ruta_archivo, 'wb') as f:
            for chunk in imagen.chunks():
                f.write(chunk)

        user.image = 'media/IMAGES/' + informationPersonalUser.pais + '/' + informationConsultorUser.rfc + '/' + nombre_archivo
        user.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})




@login_required
def updateInformationProfile(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '')
            apepa = request.POST.get('apellido_paterno', '')
            apema = request.POST.get('apellido_materno', '')
            fechaNacimiento = request.POST.get('fechaNacimiento', '')
            genero = request.POST.get('genero', '')

            telefono = request.POST.get('telefono', '')
            correoSend = request.POST.get('correo', '')
            codigoPostal = request.POST.get('codigoPostal', '')
            pais = request.POST.get('pais', '')
            estado = request.POST.get('estado', '')
            ciudad = request.POST.get('ciudad', '')
            municipio = request.POST.get('municipio', '')
            colonia = request.POST.get('colonia', '')

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)

            if nombre:
                informationPersonalUser.nombre = nombre

            if apepa:
                informationPersonalUser.ape_pat = apepa

            if apema:
                informationPersonalUser.ape_mat = apema

            if fechaNacimiento:
                informationPersonalUser.fecha_nacimiento = fechaNacimiento

            if genero:
                informationPersonalUser.sexo = genero

            if codigoPostal:
                informationPersonalUser.cod_post = codigoPostal

            if telefono:
                informationPersonalUser.telefono = telefono

            if pais:
                informationPersonalUser.pais = pais

            if estado:
                informationPersonalUser.estado = estado

            if ciudad:
                informationPersonalUser.ciudad = ciudad

            if municipio:
                informationPersonalUser.municipio = municipio

            if colonia:
                informationPersonalUser.colonia = colonia

            if correoSend:
                try:
                    Usuarios.objects.get(correo=correoSend)
                    return HttpResponse(status=400)
                except Usuarios.DoesNotExist:
                    user.correo = correoSend
                    user.save()
                    logout(request)
                    return redirect('logout')

            informationPersonalUser.save()

            return HttpResponse(status=200)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


@login_required
def updateInformationConsultor(request):
    if request.method == 'POST':
        try:
            nombreMoneda = request.POST.get('tipo_moneda', '')
            hora = request.POST.get('updateHora', '')

            rfc = request.POST.get('RFC', '')
            honorarios = request.POST.get('honorarios', '')

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)

            if nombreMoneda:
                tipoMoneda = TipoMoneda.objects.get(pk=int(nombreMoneda))
                informationConsultorUser.id_tipo_moneda_id = tipoMoneda

            if honorarios:
                maneraPago = ManeraPago.objects.get(pk=int(honorarios))
                # print(maneraPago)
                informationConsultorUser.id_manera_pago = maneraPago
                # print(informationConsultorUser.id)

            if hora:
                informationConsultorUser.tarifa_hora = int(hora)

            if rfc:

                carpeta_a_eliminar = 'PDF/' + informationPersonalUser.pais + '/' + informationConsultorUser.rfc

                # Comprobar si la carpeta existe
                if os.path.exists(carpeta_a_eliminar):
                    try:
                        # Eliminar la carpeta con su contenido
                        shutil.rmtree(carpeta_a_eliminar)
                        # print("La carpeta se ha eliminado correctamente.")
                    except OSError as e:
                        print("Error al eliminar la carpeta:", e)
                else:
                    print("La carpeta no existe.")

                informationConsultorUser.rfc = rfc

            informationConsultorUser.save()

            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


@login_required
def updateIdiomaConsultor(request):
    if request.method == 'POST':
        try:
            idioma = request.POST.get('idioma', '')
            nivel = request.POST.get('nivel', '')

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)
            idiomaModel = Idiomas.objects.get(pk=int(idioma))

            if idioma and nivel:
                consulta = IdiomasConsultor.objects.filter(
                    Q(id_consultor=informationConsultorUser) & Q(id_idioma=idiomaModel))

                if consulta.exists():
                    objeto_consulta = consulta.first()
                    objeto_consulta.nivel = nivel
                    objeto_consulta.save()
                else:
                    idiomaConsultor = IdiomasConsultor(
                        id_consultor=informationConsultorUser, id_idioma=idiomaModel, nivel=nivel)
                    # print("no hay")
                    idiomaConsultor.save()

            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


@login_required
def deleteIdiomaConsultor(request):
    if request.method == 'POST':
        try:
            idioma_id = request.POST.get('elemento')
            if idioma_id:
                idioma = IdiomasConsultor.objects.get(pk=int(idioma_id))
                idioma.delete()
            # print(idioma_id)
            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


@login_required
def updateModulosSAP(request):
    if request.method == 'POST':
        try:
            moduloEnviado = request.POST.get('modulo', '')
            submoduloEnviado = request.POST.get('submodulo', '')
            nivelEnviado = request.POST.get('nivel', '')

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)
            moduloModel = Modulos.objects.get(pk=int(moduloEnviado))
            subModuloModel = Submodulos.objects.get(pk=int(submoduloEnviado))
            nivelesConocimiento = NivelesConocimiento.objects.get(pk=int(nivelEnviado))

            if moduloEnviado and submoduloEnviado and nivelEnviado:
                consulta = ConocimientosConsultor.objects.filter(
                    Q(id_consultor=informationConsultorUser) & Q(id_modulo=moduloModel))

                if consulta.exists():
                    # print(consulta)
                    objeto_consulta = consulta.first()
                    objeto_consulta.id_nivel = nivelesConocimiento
                    objeto_consulta.id_submodulo = subModuloModel
                    objeto_consulta.save()
                else:
                    conocimientoConsultor = ConocimientosConsultor(
                        id_consultor=informationConsultorUser, id_modulo=moduloModel,id_nivel=nivelesConocimiento, id_submodulo = subModuloModel)
                    # print("no hay")
                    conocimientoConsultor.save()
                nombre = informationPersonalUser.nombre + " " + informationPersonalUser.ape_pat + " " + informationPersonalUser.ape_mat
                newNotificacion = NotificationAdministrador(name=nombre, email=user.correo, subject='Tengo nueva experiencia SAP', message='Recientemente agregue nuevos modulos a mi conocimiento en SAP', status='Pending', id_persona_destinatary_id=1)
            
                newNotificacion.save()

            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


@login_required
def updateCertificados(request):
    if request.method == 'POST':
        try:
            certificado = request.POST.get('nameCertificate', '')
            institute = request.POST.get('institute', '')
            enlace = request.POST.get('linkCertificate', '')
            descripcion = request.POST.get('descripcion', '')
            termino = request.POST.get('termino', '')
            id_certificadoQuery = request.POST.get('id_certificadoQuery', '')

            # print(id_certificadoQuery)
            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)

            if certificado and institute and termino:
                if Instituciones.objects.filter(nombre=institute).exists():
                        # Se encontró la institución
                    institucion = Instituciones.objects.get(nombre=institute)
                else:
                        # No se encontró la institución
                    institucion = Instituciones(nombre=institute)
                    institucion.save()

                if id_certificadoQuery:
                    cursos = CursosConsultor.objects.get(pk=id_certificadoQuery)
                    cursos.nombre_curso=certificado
                    cursos.enlace_certificado=enlace
                    cursos.descripcion=descripcion
                    cursos.fecha_termino=termino
                    cursos.id_institucion_curso=institucion
                    cursos.save()
                else:
                    cursos = CursosConsultor(nombre_curso=certificado, enlace_certificado=enlace, descripcion=descripcion, fecha_termino=termino, id_consultor=informationConsultorUser, id_institucion_curso=institucion)
                    cursos.save()

            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


@login_required
def updateExperiencia(request):
    if request.method == 'POST':
        try:
            puesto = request.POST.get('puesto', '')
            empresa = request.POST.get('empresa', '')
            ageInit = request.POST.get('ageInit', '')
            ageFinish = request.POST.get('ageFinish', '')
            actividades = request.POST.get('actividades', '')
            id_experiencia = request.POST.get('experiencia-saber', '')
            
            
            
            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)

            if not id_experiencia and puesto and ageInit:
                fecha_entrada_str = ageInit
                fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d')
                fecha_salida = date.today()
                if 'check' in request.POST:
                    tiempoExperiencia = 'Sigue Trabajando'
                else:
                    fecha_salida_str = ageFinish
                    if fecha_salida_str:
                        fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d')
                        diferencia = fecha_salida - fecha_entrada
                        tiempoExperiencia = diferencia.days

                experienciaRegistrada = Experiencias(nombre=puesto)
                experienciaRegistrada.save()
                experiencia = ExperienciasConsultor(descripcion = actividades, empresa = empresa, puesto = puesto, id_experiencia = experienciaRegistrada, tiempo_experiencia=tiempoExperiencia, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, id_consultor=informationConsultorUser)
                experiencia.save()




            if id_experiencia and puesto and empresa and ageInit:
                
                fecha_entrada_str = ageInit
                fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d')
                fecha_salida = date.today()
                if 'check' in request.POST:
                    tiempoExperiencia = 'Sigue Trabajando'
                else:
                    fecha_salida_str = ageFinish
                    if fecha_salida_str:
                        fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d')
                        diferencia = fecha_salida - fecha_entrada
                        tiempoExperiencia = diferencia.days
                experiencia = ExperienciasConsultor.objects.get(pk=id_experiencia)

                experienciaRegistrada = Experiencias.objects.get(pk=experiencia.id_experiencia_id)
                experienciaRegistrada.nombre = puesto
                experienciaRegistrada.save()    
                # print(experienciaRegistrada.id)
                experiencia.descripcion = actividades
                experiencia.empresa = empresa
                experiencia.puesto = puesto
                experiencia.id_experiencia = experienciaRegistrada
                experiencia.tiempo_experiencia=tiempoExperiencia
                experiencia.fecha_entrada=fecha_entrada
                experiencia.fecha_salida=fecha_salida
                # print(experiencia.id)
                experiencia.save()
                # print(experiencia.id)


            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)

@login_required
def updateEducacion(request):
    if request.method == 'POST':
        try:
            nivelEducacion = request.POST.get('nivelEducacion', '')
            instituteEducacion = request.POST.get('instituteEducacion', '')
            tituloEducacion = request.POST.get('tituloEducacion', '')
            ageInitEducacion = request.POST.get('ageInitEducacion', '')
            ageFinish = request.POST.get('ageFinish', '')
            check = request.POST.get('check', '')
            id_education_saber = request.POST.get('education-saber', '')
            

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)

            if nivelEducacion and instituteEducacion and tituloEducacion and ageInitEducacion and not id_education_saber:
                if Instituciones.objects.filter(nombre=instituteEducacion).exists():
                    # Se encontró la institución
                    institucion = Instituciones.objects.get(
                        nombre=instituteEducacion)
                else:
                    # No se encontró la institución
                    institucion = Instituciones(
                        nombre=instituteEducacion)
                    institucion.save()

                if check:
                    estudios = Estudios(id_institucion = institucion,titulo_registrado = tituloEducacion,fecha_ingreso = ageInitEducacion,fecha_termino = 'Sigue Estudiando',educacion = nivelEducacion, id_consultor=informationConsultorUser)

                else:
                    estudios = Estudios(id_institucion = institucion,titulo_registrado = tituloEducacion,fecha_ingreso = ageInitEducacion,fecha_termino = ageFinish,educacion = nivelEducacion, id_consultor=informationConsultorUser)

                estudios.save()

            if nivelEducacion and instituteEducacion and tituloEducacion and ageInitEducacion and id_education_saber:
                if Instituciones.objects.filter(nombre=instituteEducacion).exists():
                    # Se encontró la institución
                    institucion = Instituciones.objects.get(
                        nombre=instituteEducacion)
                else:
                    # No se encontró la institución
                    institucion = Instituciones(
                        nombre=instituteEducacion)
                    institucion.save()

                if check:
                    estudios = Estudios.objects.get(pk=id_education_saber)
                    estudios.id_institucion = institucion
                    estudios.titulo_registrado = tituloEducacion
                    estudios.fecha_ingreso = ageInitEducacion
                    estudios.fecha_termino = 'Sigue Estudiando'
                    estudios.educacion = nivelEducacion
                else:
                    estudios = Estudios.objects.get(pk=id_education_saber)
                    estudios.id_institucion = institucion
                    estudios.titulo_registrado = tituloEducacion
                    estudios.fecha_ingreso = ageInitEducacion
                    estudios.fecha_termino = ageFinish
                    estudios.educacion = nivelEducacion

                estudios.save()
            
            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=404)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=404)
        except Personas.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            print(e)
            return HttpResponse(status=404)


def searchFile(ruta):
    if os.path.exists(ruta):
        return '1'
    else:
        return '0'

@login_required
def principal(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        
        consulta = request.GET.get('consulta')
        estado = request.GET.get('estado')
        ciudad = request.GET.get('ciudad')

        experiencia = request.GET.get('experiencia')
        tipo = request.GET.get('tipo')

        registros = Proyectos.objects.all().order_by('-id')

        if consulta:
            registros = registros.filter(proyecto_nombre__icontains=consulta)

        if estado:
            empresas = Empresas.objects.filter(estado__icontains=estado)
            empresaProyecto = EmpresaProyecto.objects.filter(id_empresa__in=empresas)
            registros = registros.filter(id_empresa_proyecto__in=empresaProyecto)

        if ciudad:
            empresas = Empresas.objects.filter(ciudad__icontains=ciudad)
            empresaProyecto = EmpresaProyecto.objects.filter(id_empresa__in=empresas)
            registros = registros.filter(id_empresa_proyecto__in=empresaProyecto)

        if tipo:
            registros = registros.filter(tipo__exact=tipo)

        if estado and ciudad:
            empresas = Empresas.objects.filter(estado__icontains=estado, ciudad__icontains=ciudad)
            empresaProyecto = EmpresaProyecto.objects.filter(id_empresa__in=empresas)
            registros = registros.filter(id_empresa_proyecto__in=empresaProyecto)        
        
        requerimientos = RequerimientosModulosProyecto.objects.all()
        
        if experiencia:
            nivelesConocimiento = NivelesConocimiento.objects.filter(nombre__exact=experiencia)
            requerimientos_ids = RequerimientosModulosProyecto.objects.filter(id_experiencia_requerida__in=nivelesConocimiento).values_list('id_proyecto', flat=True)

            # print(requerimientos_ids)
            registros = registros.filter(id__in=requerimientos_ids)


        paginator = Paginator(registros, 8)
        page_number = request.GET.get('page')
        proyectos = paginator.get_page(page_number)
        cantidad_proyectos = paginator.count
        num_paginas = paginator.num_pages
        proyectos_con_requerimientos = {}

        for proyecto in proyectos:
            proyectos_con_requerimientos[proyecto] = []
            requerimientos_proyecto = requerimientos.filter(id_proyecto=proyecto)
            proyectos_con_requerimientos[proyecto] = requerimientos_proyecto

        
        # print(proyectos)
        notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)

        # // ONLY 4 PENDING 
        pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)[:4]
        
        return render(request, "principal.html", {
            'indice':'Principal',
            'image':user.image,
            'proyectos_con_requerimientos': proyectos_con_requerimientos,
            'num_paginas':num_paginas,
            'informationPersonalUser': informationPersonalUser,
            'cantidad_proyectos':cantidad_proyectos,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
        
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def detallesProyecto(request, id=int):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        
        proyecto = Proyectos.objects.get(pk=id)
        empresaProyecto = EmpresaProyecto.objects.filter(id_proyecto=proyecto).first()
        if empresaProyecto is not None:
            empresa = Empresas.objects.get(pk=empresaProyecto.id_empresa_id)
        else:
            empresa = ''
        requerimientosModulosProyecto = RequerimientosModulosProyecto.objects.filter(id_proyecto=proyecto).order_by('-id')

        requerimientosIdiomasProyecto = RequerimientosIdiomasProyecto.objects.filter(id_proyecto=proyecto).order_by('-id')


        fecha_actual = datetime.now().date()
        # Fecha de publicación del staffing (ejemplo)
        fecha_publicacion = proyecto.fecha_publicacion

        # Calcula la diferencia de días
        diferencia = fecha_actual - fecha_publicacion
        dias_pasados = diferencia.days

        if dias_pasados > 30:
            diasStaffing = 'Hace mas de un mes'
        elif dias_pasados == 0:
            diasStaffing = 'Hoy'
        else:
            diasStaffing = 'Hace ' + str(dias_pasados) + ' días'


        postulacion = PostulacionesProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)

        if not postulacion:
            postulacion = ProyectoConsultor.objects.filter(id_proyecto=proyecto, id_consultor=informationConsultorUser)
            if postulacion:
                aceptado = True
            else:
                aceptado = False
        else:
            aceptado = False

        notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
        pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')[:4]

        return render(request, "detalles_proyecto.html", {
            'indice':'Principal',
            'image':user.image,
            'filter':2,
            'proyecto':proyecto,
            'empresa':empresa,
            'aceptado':aceptado,
            'postulacion':postulacion,
            'requerimientosModulosProyecto':requerimientosModulosProyecto,
            'diasStaffing':diasStaffing,
            'informationPersonalUser': informationPersonalUser,
            'requerimientosIdiomasProyecto':requerimientosIdiomasProyecto,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
        
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')

# //  VIEW ALL NOTIFICATIONS
@login_required
def all_notifications(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        # // NOTIFICATIONS DATA
        notification_list = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')
        # //Pagination

        # //Cantidad de notificaciones que apareceran antes de crear otra page
        if notification_list.exists():
            paginator = Paginator(notification_list, 16)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationConsultor.objects.filter(status='Pending',id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
            pending = NotificationConsultor.objects.filter(status='Pending',id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')[:4]
        else:
            notification = []
            pending = []
            pending_total = 0
            

        context = {
            'indice': 'Principal',
            'filter':1,
            'image':user.image,
            'informationPersonalUser': informationPersonalUser,
            'notification':notification,
            'notification_pending': pending,
            'pending':pending,
            'pending_total':pending_total,
        }
        return render(request, 'notifications/all_notifications.html', context)


    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


# //  VIEW 1 NOTIFICATION
@login_required
def view_notification(request, id= None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        # // DATA DE LA NOTIFICACION ELEGIDA
        notification = NotificationConsultor.objects.get(pk=id, id_consultor_destinatary=informationConsultorUser.id)

        if notification.data:
            data = notification.data
            pares = data.split(',')
            datos = {}
            for par in pares:
                clave, valor = par.split(':')
                datos[clave] = valor

            entrevista = datos.get('id_entrevista', '')
            proyectoConsultor = datos.get('id_proyectoConsultor', '')
        else:
            entrevista = ''
            proyectoConsultor = ''


        # // EL STATUS CAMBIA A 'READ' Y GUARDA
        notification.status = 'Read'
        notification.save()
        # // NOTIFICATIONS DATA
        notification_data = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
        pending = NotificationConsultor.objects.filter(status='Pending',id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')[:4]


        context = {
            'indice': 'Principal',
            'image':user.image,
            'filter':2,
            'informationPersonalUser': informationPersonalUser,
            'entrevista':entrevista,
            'proyectoConsultor':proyectoConsultor,
            'notification':notification,
            'notifications':notification_data,
            'pending':pending,
            'pending_total':pending_total,
        }
        return render(request, "notifications/view_notification.html", context)

    except NotificationConsultor.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


@login_required
@require_http_methods(['DELETE'])
def deleteModuloSAP(request, id):
    
    try:
        # print(id)
        conocimiento = ConocimientosConsultor(pk=int(id))
        # print(conocimiento)
        conocimiento.delete()
        # print("se eliminado")
        # print(conocimiento)
        return JsonResponse({'message': 'El objeto se ha eliminado correctamente.'}, status=200)
    except ConocimientoConsultor.DoesNotExist:
        return JsonResponse({'message': 'El objeto no existe.'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'message': f'Error al eliminar el objeto: {str(e)}'}, status=404)



@login_required
def postularse(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

        data = json.loads(request.body)
        id = data['id']

        proyecto = Proyectos.objects.get(pk=int(id))
        empresa = proyecto.id_empresa_proyecto.id_empresa

        postulacion = PostulacionesProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)

        if postulacion:
            pass
        else:
            postulacion = PostulacionesProyecto(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)
            postulacion.save()
            
            message = 'Me acabo de postular a su proyecto ' + str(proyecto.proyecto_nombre)
            name = 'Consultor'
            
            if informationPersonalUser.sexo == 'M':
                titulo = '¡¡Estoy interesado!!'
            else:
                titulo = '¡¡Estoy interesada!!'

            notificacion = NotificationEmpresa(name=name, email='consultor@gnosis.com.mx', subject=titulo, message=message, status='Pending', id_empresa_destinatary=empresa)
            notificacion.save()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)


@login_required
def deletePostulacion(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

        data = json.loads(request.body)
        id = data['id']

        proyecto = Proyectos.objects.get(pk=int(id))
        empresa = proyecto.id_empresa_proyecto.id_empresa

        postulacion = PostulacionesProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)

        if postulacion:
            postulacion.delete()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=404)



@login_required
def confirmarEntrevistaConsultor(request, id:int):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

        entrevistasConsultoresProyecto = EntrevistasConsultoresProyecto.objects.get(pk=int(id), id_consultor=informationConsultorUser)
        if entrevistasConsultoresProyecto:
            entrevistasConsultoresProyecto.estatus = 'Confirmada'
            entrevistasConsultoresProyecto.save()

            message = 'He aceptado la entrevista para el proyecto: ' + str(entrevistasConsultoresProyecto.id_proyecto.proyecto_nombre) + ' de la empresa: ' + str(entrevistasConsultoresProyecto.id_empresa.empresa)
            adminNotificacion = NotificationAdministrador(name=informationPersonalUser.nombre, email=user.correo, subject="¡¡Tengo una entrevista!!", message=message, status='Pending', id_persona_destinatary_id=1)
            adminNotificacion.save()


            messageEmpresa = 'He aceptado la entrevista para el proyecto: ' + str(entrevistasConsultoresProyecto.id_proyecto.proyecto_nombre) + '. Gracias por la oportunidad.'

            empresaNotificacion = NotificationEmpresa(name='Consultor', email='consultor@gnosis.com.mx', subject='Entrevista confirmada', message=messageEmpresa, status='Pending', id_empresa_destinatary=entrevistasConsultoresProyecto.id_empresa)
            empresaNotificacion.save()

        return render(request, "confirmation.html")
        

    except Exception as error:
        print(f"Error: {str(error)}")
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('miProfile')



@login_required
def confirmarProyectoConsultor(request, id:int):
    try:    
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        proyectoConsultor = ProyectoConsultor.objects.get(pk=int(id))
        proyectoConsultor.status = 'Aceptada'
        proyectoConsultor.save()

        informationPersonalUser.disponible = False
        informationPersonalUser.save()

        return render(request, "entrevistaConfirmada.html")
    
    except Exception as error:
        print(f"Error: {str(error)}")
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('miProfile')


@login_required
def test(request):
    try:
        return render(request, "emails/reporte_email.html")
    except Exception as error:
        print(f"Error: {str(error)}")
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def bancosDatos(request, id):
    try:
        if request.method == 'GET':
            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
            
            notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id)
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)
            # // ONLY 4 PENDING 
            pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)[:4]

            return render(request, "data_bancos.html", {
                'indice':'Principal',
                'image':user.image,
                'filter':2,
                'informationConsultorUser':informationConsultorUser.id,
                'informationPersonalUser': informationPersonalUser,
                'correo': request.session.get('username'),
                'notifications':notification,
                'pending':pending,
                'pending_total':pending_total,
            })
        else:
            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

            cuentambiente = request.POST.get('cuentambiente')
            banco = request.POST.get('banco')
            tipoCuenta = request.POST.get('tipoCuenta')
            no_cuenta = request.POST.get('no_cuenta')
            ejecutivo_cuenta = request.POST.get('ejecutivo_cuenta')
            telefono_ejecutivo = request.POST.get('telefono_ejecutivo')
            sucursal = request.POST.get('sucursal')
            correo_ejecutivo= request.POST.get('correo_ejecutivo')
            clave= request.POST.get('clave')
            dia_corte = request.POST.get('dia_corte')
            chec = request.POST.get('chec')
            descripcion = request.POST.get('descripcion')
        

            if not chec:
                chec = False
            else:
                chec = True

            bancoNew = Bancos.objects.filter(nombre__icontains=banco).first()
            if not bancoNew:
                bancoNew = Bancos(nombre=banco)
                bancoNew.save()

            try:
                queryData = DatosBancarios.objects.get(id_usuario=user)
                queryData.id_banco=bancoNew
                queryData.sucursal=sucursal
                queryData.cuentambiente=cuentambiente
                queryData.tipo_cuenta=tipoCuenta
                queryData.no_cuenta_clabe=no_cuenta
                queryData.ejecutivo_cuenta=ejecutivo_cuenta
                queryData.telefono_ejecutivo=telefono_ejecutivo
                queryData.correo_ejecutivo=correo_ejecutivo
                queryData.dia_corte=dia_corte
                queryData.descripcion=descripcion
                queryData.activo=chec
                queryData.id_usuario=user
                queryData.save()

            except DatosBancarios.DoesNotExist:
                data = DatosBancarios(id_banco=bancoNew, sucursal=sucursal,cuentambiente=cuentambiente, tipo_cuenta=tipoCuenta, no_cuenta_clabe=no_cuenta, ejecutivo_cuenta=ejecutivo_cuenta, telefono_ejecutivo=telefono_ejecutivo,correo_ejecutivo=correo_ejecutivo,rfc_clave=clave, dia_corte=dia_corte, descripcion=descripcion,activo=chec, id_usuario=user)

                data.save()

            return redirect('miProfile')

    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def addInfoExtra(request):
    try:
        if request.method == 'POST':

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

            CURP = request.POST.get('CURP') 
            licencia = request.POST.get('licencia') 
            visa = request.POST.get('visa') 
            pasaporte = request.POST.get('pasaporte') 
            estadoCivil = request.POST.get('estadoCivil') 
            cHijos = request.POST.get('cHijos')
            viajar = request.POST.get('viajar') 
            comprobante_domicilio = request.POST.get('comprobante_domicilio') 
            

            informationConsultorUser.curp = CURP
            informationConsultorUser.licencia_conducir = licencia
            informationConsultorUser.visa = visa
            informationConsultorUser.pasaporte = pasaporte
            informationConsultorUser.estadoCivil = estadoCivil
            informationConsultorUser.cantidad_hijos = int(cHijos)
            informationConsultorUser.comprobante_domicilio = comprobante_domicilio

            if viajar == 'True':
                informationConsultorUser.viajar = True
            else:
                informationConsultorUser.viajar = False

            informationConsultorUser.save()

            gnroHijo1 = request.POST.get('gnroHijo1') 
            edadHijo1 = request.POST.get('edadHijo1') 
 
            if gnroHijo1 and edadHijo1:
                query = Hijos.objects.filter(id_persona=informationPersonalUser, nHjo=1)
                if query:
                    query.genero = gnroHijo1
                    query.edad = edadHijo1
                    query.save()
                else:
                    hjo1 = Hijos(genero=gnroHijo1, edad=edadHijo1, id_persona=informationPersonalUser, nHjo=1)
                    hjo1.save()


            gnroHijo2 = request.POST.get('gnroHijo2') 
            edadHijo2 = request.POST.get('edadHijo2') 
 
            if gnroHijo2 and edadHijo2:
                query = Hijos.objects.filter(id_persona=informationPersonalUser, nHjo=2)
                if query:
                    query.genero = gnroHijo2
                    query.edad = edadHijo2
                    query.save()
                else:
                    hjo2 = Hijos(genero=gnroHijo2, edad=edadHijo2, id_persona=informationPersonalUser, nHjo=2)
                    hjo2.save()


            gnroHijo3 = request.POST.get('gnroHijo3') 
            edadHijo3 = request.POST.get('edadHijo3') 
 
            if gnroHijo3 and edadHijo3:
                query = Hijos.objects.filter(id_persona=informationPersonalUser, nHjo=3)
                if query:
                    query.genero = gnroHijo3
                    query.edad = edadHijo3
                    query.save()
                else:
                    hjo3 = Hijos(genero=gnroHijo3, edad=edadHijo3, id_persona=informationPersonalUser, nHjo=3)
                    hjo3.save()
            
            return redirect('miProfile')

    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def miProjects(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        
        proyectoConsultor = ProyectoConsultor.objects.filter(id_consultor=informationConsultorUser, status='Aceptada')
        # Obtener el número de objetos devueltos por la consulta
        cantidad_proyectos = proyectoConsultor.count()

        notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)

        # // ONLY 4 PENDING 
        pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)[:4]

        return render(request, "misProyectos.html", {
            'indice':'Proyectos',
            'image':user.image,
            'informationPersonalUser': informationPersonalUser,
            'proyectoConsultor':proyectoConsultor,
            'cantidad_proyectos':cantidad_proyectos,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
        
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def miProyecto(request, id=int):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona.id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        
        proyecto = Proyectos.objects.get(pk=id)

        empresaProyecto = EmpresaProyecto.objects.filter(id_proyecto=proyecto).first()
        if empresaProyecto is not None:
            empresa = Empresas.objects.get(pk=empresaProyecto.id_empresa.id)
        else:
            empresa = ''

        colaborador = ProyectoConsultor.objects.filter(id_proyecto=proyecto,id_consultor=informationConsultorUser)

        if colaborador:
            id_proyecto_consultor_list = colaborador.values_list('id', flat=True)

            # Obtener todos los contratos asociados a los id_proyecto_consultor
            try:
                contratos = Contratos.objects.get(id_proyecto_consultor__in=id_proyecto_consultor_list)
            except Contratos.DoesNotExist as error:
                contratos = None
            facturas = Facturas.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)
            
            
            regitrosFacturas = []
            for f in facturas:
                periodo = f.periodo
                fecha = f.id_documentacion.fecha_creacion
                directory = str(f.id_documentacion.ruta) + '/' + str(f.id_documentacion.nombre)
                entregado = searchFile(directory)
                validacionGnosis = f.validacionGnosis
                validacionEmpresa = f.validacionEmpresa

                regitrosFacturas.append([periodo, entregado, validacionGnosis, validacionEmpresa, fecha])


            reportesHoras = ReporteHoras.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)

            regitrosReportesHoras = []
            for f in reportesHoras:
                periodo = f.periodo
                fecha = f.id_documentacion.fecha_creacion
                directory = str(f.id_documentacion.ruta) + '/' + str(f.id_documentacion.nombre)
                entregado = searchFile(directory)
                validacionGnosis = f.validacionGnosis
                validacionEmpresa = f.validacionEmpresa

                regitrosReportesHoras.append([periodo, entregado, validacionGnosis, validacionEmpresa, fecha])

            
            reportesFinales = ReporteFinalActividades.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)

            regitrosReportesFinales = []
            for f in reportesFinales:
                periodo = f.periodo
                fecha = f.id_documentacion.fecha_creacion
                directory = str(f.id_documentacion.ruta) + '/' + str(f.id_documentacion.nombre)
                entregado = searchFile(directory)
                validacionGnosis = f.validacionGnosis
                validacionEmpresa = f.validacionEmpresa

                regitrosReportesFinales.append([periodo, entregado, validacionGnosis, validacionEmpresa, fecha])

            # print(regitrosReportesFinales)

            fecha_actual = datetime.now().date()
            # Fecha de publicación del staffing (ejemplo)
            fecha_publicacion = proyecto.fecha_publicacion

            # Calcula la diferencia de días
            diferencia = fecha_actual - fecha_publicacion
            dias_pasados = diferencia.days

            if dias_pasados > 30:
                diasStaffing = 'Hace mas de un mes'
            elif dias_pasados == 0:
                diasStaffing = 'Hoy'
            else:
                diasStaffing = 'Hace ' + str(dias_pasados) + ' días'


            
            
            
            notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')

            # // ONLY 4 PENDING 
            pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')[:4]

            return render(request, "miProyecto.html", {
                'indice':'Proyectos',
                'image':user.image,
                'filter':2,
                'proyecto':proyecto,
                'empresa':empresa,
                'diasStaffing':diasStaffing,
                'informationPersonalUser': informationPersonalUser,
                'informationConsultorUser':informationConsultorUser,
                'facturas':regitrosFacturas,
                'reporteHoras':regitrosReportesHoras,
                'reportesFinales':regitrosReportesFinales,
                'contrato':contratos,
                'cambioHoyMXN':tipoCambioMXN(),
                'cambioHoyUSD':tipoCambioUSD(),
                'notifications':notification,
                'pending':pending,
                'pending_total':pending_total,
            })
        else:
            return redirect('miProjects')
        
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('miProjects')
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('miProjects')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('miProjects')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')





@login_required
def upload_all_files_rp(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        if request.method == 'POST' and request.FILES['file']:
            file = request.FILES['file']
            original_filename = file.name
            nameFile = request.POST.get('name', '')
            rfc = request.POST.get('rfc', '')
            proyecto = request.POST.get('proyecto', '')
            mes = request.POST.get('mes', '')

            cobranza = request.POST.get('cobranza', '')
            pago = request.POST.get('pago', '')

            directory = 'media/PDF/' + informationPersonalUser.pais + '/' + rfc + '/RP/PRJ' + proyecto
            # Verificar si el directorio existe, si no, crearlo
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Combinar el directorio y el nuevo nombre de archivo usando el nombre original

            if nameFile == 'FACTURA':
                fecha_actual = datetime.now()
                # Obtener el año de la fecha actual
                ano_actual = fecha_actual.year
                if mes:
                    nameFile = 'FACTURA-' + str(mes) + '-'+str(ano_actual)

            elif nameFile == 'RHORAS':
                fecha_actual = datetime.now()
                # Obtener el año de la fecha actual
                ano_actual = fecha_actual.year
                if mes:
                    nameFile = 'RHORAS-' + str(mes) + '-'+str(ano_actual)

            else:
                pass

            new_filename = rfc + '_' + nameFile + os.path.splitext(original_filename)[1]
            new_filepath = os.path.join(directory, new_filename)

            # Guardar el archivo en el directorio con el nuevo nombre
            with open(new_filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Buscar o crear el objeto TipoDocumento
            documento, created = TipoDocumento.objects.get_or_create(nombre=nameFile)
            # Buscar o crear el objeto Documentacion
            query, created = Documentacion.objects.get_or_create(
                id_consultor=informationConsultorUser,
                id_tipo_documento=documento,
                ruta=directory,
                nombre=new_filename,
                fecha_creacion=date.today()
            )
            # Actualizar la fecha de creación
            query.fecha_creacion = date.today()
            query.save()


            nameConsultor = str(informationPersonalUser.nombre) + ' ' + str(informationPersonalUser.ape_pat) + ' ' + str(informationPersonalUser.ape_mat)
            proyectoNa = Proyectos.objects.get(pk=int(proyecto))
            proyectoName = str(proyectoNa.proyecto_nombre)
            empresa = Empresas.objects.get(pk=proyectoNa.id_empresa_proyecto.id_empresa.id)
            empresaName = str(empresa.empresa)
            correoEmpresa = str(empresa.id_usuario.correo)

            proyectoConsultor = ProyectoConsultor.objects.get(id_proyecto=proyectoNa, id_consultor=informationConsultorUser)

            if nameFile.startswith('FACTURA'):
                manual = request.POST.get('manual-terceros')
                tipoCambio = request.POST.get('cambio-terceros')

                if manual == '1':
                    # print("manual")
                    cambio = request.POST.get('tipoCambioHoy-Manual-terceros')
                    
                else:
                    # print("api")
                    cambio = request.POST.get('tipoCambioHoy-Auto-terceros')

                # print(cambio)
                # print(tipoCambio)
                try:
                    
                    factura = Facturas.objects.get(
                        id_proyecto_consultor=proyectoConsultor,
                        periodo=mes,
                        id_documentacion=query
                    )
                    factura.fecha_cobranza = cobranza
                    factura.fecha_pago = pago
                    activo = request.POST.get('cambio-activo')

                    if activo == '1':
                        factura.tipoCambioMXN = tipoCambio
                        factura.tipoCambioUSD = cambio
                    else:
                        factura.tipoCambioMXN = 0.00
                        factura.tipoCambioUSD = 0.00
                    factura.save()
                except Facturas.DoesNotExist:
                    facturas = Facturas.objects.filter(id_proyecto_consultor=proyectoConsultor)
                    numero_de_facturas = facturas.count()
                    numero_de_facturas = numero_de_facturas + 1
                    activo = request.POST.get('cambio-activo')
                    if activo == '1':
                        factura = Facturas(
                            id_proyecto_consultor=proyectoConsultor,
                            periodo=mes,
                            id_documentacion=query,
                            fecha_cobranza = cobranza,
                            fecha_pago = pago,
                            num_mes_declarado=numero_de_facturas,
                            tipoCambioMXN = tipoCambio,
                            tipoCambioUSD = cambio
                        )
                    else:
                        factura = Facturas(
                            id_proyecto_consultor=proyectoConsultor,
                            periodo=mes,
                            id_documentacion=query,
                            fecha_cobranza = cobranza,
                            fecha_pago = pago,
                            num_mes_declarado=numero_de_facturas,
                        )

                    factura.save()


            elif nameFile.startswith('RHORAS'):
                reporteHoras = ReporteHoras.objects.get_or_create(
                    id_proyecto_consultor=proyectoConsultor,
                    periodo=mes,
                    id_documentacion=query
                ) 
            else:
                reporteFinal = ReporteFinalActividades.objects.get_or_create(
                    id_proyecto_consultor=proyectoConsultor,
                    periodo=mes,
                    id_documentacion=query
                ) 


            if nameFile.startswith('FACTURA'):
                nombre = str(informationPersonalUser.nombre) + " " + str(informationPersonalUser.ape_pat) + " " + str(informationPersonalUser.ape_mat)

                message='Acabo de entregar mi Factura correspondiente al mes de ' + str(mes) + ' para el proyecto ' + str(proyectoName)
                newNotificacion = NotificationAdministrador(name=nombre, email=user.correo, subject=nameFile, message=message, status='Pending', id_persona_destinatary_id=1)
            
                newNotificacion.save()


                # sendemail(str(empresa.id_usuario.correo), empresaName, str(new_filepath), nameConsultor, proyectoName, 'FACTURA', new_filename)
                
            elif nameFile.startswith('RHORAS'):
                
                nombre = str(informationPersonalUser.nombre) + " " + str(informationPersonalUser.ape_pat) + " " + str(informationPersonalUser.ape_mat)

                message='Acabo de entregar mi Reporte de horas correspondiente al mes de ' + str(mes) + ' para el proyecto ' + str(proyectoName)
                newNotificacion = NotificationAdministrador(name=nombre, email=user.correo, subject=nameFile, message=message, status='Pending', id_persona_destinatary_id=1)
            
                newNotificacion.save()

                # sendemail(correoEmpresa, empresaName, str(new_filepath), nameConsultor, proyectoName)
                
                
            else:

                nombre = str(informationPersonalUser.nombre) + " " + str(informationPersonalUser.ape_pat) + " " + str(informationPersonalUser.ape_mat)

                message='Acabo de entregar mi Reporte final de actividades de el proyecto ' + str(proyectoName)
                newNotificacion = NotificationAdministrador(name=nombre, email=user.correo, subject=nameFile, message=message, status='Pending', id_persona_destinatary_id=1)
            
                newNotificacion.save()

                # sendemail(correoEmpresa, empresaName, str(new_filepath), nameConsultor, proyectoName)
           

            return redirect('miProjects')
        else:
            return redirect('miProjects')

    except Exception as e:
        print(e)
        return redirect('miProjects')


def sendemail(email, nameEmpresa, ruta, nameConsultor, proyecto, RP, assunt):
    try:
        to = email
        name = nameEmpresa
        # se envian los datos al email template
        if RP == 'RHORAS':
            html_content = render_to_string(
                "emails/reporte_email.html", {"nameEmpresa":nameEmpresa, "nameConsultor":nameConsultor, "proyecto":proyecto, "RP":"REPORTE DE HORAS"}
            )
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                # nombre que tendra el correo
                "Gnosis [REPORTE DE HORAS]",
                # texto contenido
                text_content,
                # conexion con settings y el host user
                settings.EMAIL_HOST_USER,
                # rec list
                [to],
            )
            assunt = '5TY3HJ4HJBHZ_RHORAS.xlsx'
        
        elif RP == 'FACTURA':
            html_content = render_to_string(
                "emails/reporte_email.html", {"nameEmpresa":nameEmpresa, "nameConsultor":nameConsultor, "proyecto":proyecto, "RP":"FACTURA"}
            )
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                # nombre que tendra el correo
                "Gnosis [FACTURA]",
                # texto contenido
                text_content,
                # conexion con settings y el host user
                settings.EMAIL_HOST_USER,
                # rec list
                [to],
            )
            assunt = '5TY3HJ4HJBHZ_FACTURA.xlsx'
        else:
            html_content = render_to_string(
                "emails/reporte_email.html", {"nameEmpresa":nameEmpresa, "nameConsultor":nameConsultor, "proyecto":proyecto, "RP":"REPORTE FINAL DE ACTIVIDADES"}
            )
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                # nombre que tendra el correo
                "Gnosis [REPORTE FINAL DE ACTIVIDADES]",
                # texto contenido
                text_content,
                # conexion con settings y el host user
                settings.EMAIL_HOST_USER,
                # rec list
                [to],
            )
        

        # Se adjunta el archivo XLSX al correo
        # xlsx_file_path = os.path.join(BASE_DIR, "media", "PDF", "México", "5TY3HJ4HJBHZ", "RP", "PRJ37", "5TY3HJ4HJBHZ_RHORAS.xlsx")

        xlsx_file_path = ruta
        if os.path.exists(xlsx_file_path):
            with open(xlsx_file_path, "rb") as xlsx_file:
                email.attach(assunt, xlsx_file.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # se indica que se convierta como html
        email.attach_alternative(html_content, "text/html")
        # se envia el correo
        email.send()
        return "Correo enviado"
    
    except Exception as e:
        print(e)
        return "Correo fallido"


@login_required
def addDescriptionConsultor(request):
    try:
        if request.method == 'POST':
            persona = request.POST['persona']
            descripcion = request.POST['descripcion']

            personaQuery = Personas.objects.get(pk=int(persona))
            personaQuery.descripcion = descripcion
            personaQuery.save()
            # Redirigir a la URL construida
            return redirect('curriculum_consultor')
            
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def curriculum_vitae(request):
    try:
        # descripcion = request.POST.get('descripcion') #perfil descripcion
        
        try:
            # OBTENER ID DEL CONSULTOR QUE INICIO SESION

            user = Usuarios.objects.get(correo=request.session.get('username'))
            informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

            #SE PIDEN LOS DATOS A LOS MODELOS
            estudios = Estudios.objects.filter (id_consultor = informationConsultorUser ) #educacion
            curso = CursosConsultor.objects.filter  (id_consultor = informationConsultorUser  ) #certificaciones
            modulos = ConocimientosConsultor.objects.filter( id_consultor = informationConsultorUser  )
            idiomas = IdiomasConsultor.objects.filter( id_consultor = informationConsultorUser)
            proyectoConsultor = ProyectoConsultor.objects.filter(id_consultor = informationConsultorUser  )

            # Pasar los datos al HTML que servirá como plantilla para el PDF
            template_path = "CV/curriculum.html"
            context = {
                "usuarios":user,
                "personas":informationPersonalUser,
                "estudios":estudios,
                "curso":curso,
                "consultores":informationConsultorUser,
                "modulos":modulos,
                "idiomas":idiomas,
                "proyectoConsultor":proyectoConsultor,
            }
            # print(context)
            # print("---")
            if modulos:
                # print("pipi")
                pass
            else:
                # print("popop")
                pass
            template = get_template(template_path)
            html = template.render(context)
            
            # Crear un objeto de respuesta Django y especificar content_type como PDF
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'filename="CURRICULUM-VITAE.pdf"'
            pdf_bytes = BytesIO()
            
            # Generar el PDF en memoria usando pisa
            pisa_status = pisa.CreatePDF(html, dest=pdf_bytes, encoding='UTF-8', page_size='letter')

            # Verificar si hubo errores al generar el PDF
            if pisa_status.err:
                raise Exception("Error al generar el PDF")


            # Crear el PDF a partir del HTML usando pisa
            pisa_status = pisa.CreatePDF(html, dest=response, encoding='UTF-8', page_size='letter')

            # Si hay errores al generar el PDF, mostrar un mensaje
            if pisa_status.err:
                return HttpResponse("Error al generar el PDF")

            return response
            #return HttpResponse(status=200)
        except IdiomasConsultor.DoesNotExist as error:
            print(f"Error: {str(error)}")
            return redirect('miProfile')

        except ProyectoConsultor.DoesNotExist as error:
            print(f"Error: {str(error)}")
            return redirect('miProfile')
    
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return redirect('miProfile')
    except Exception as e:
        print(e)
        return redirect('miProfile')



def tipoCambioUSD():
    api_key = "2783819ab9795ebb65cf80f8"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/MXN"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        exchange_rates = data["conversion_rates"]
        for currency, rate in exchange_rates.items():
            if currency == 'USD':
                # print(f"1 USD = {round(float(rate),2)} {currency}")
                st = str(rate)
                return st[0:6]
    else:
        print("Error:", response.status_code)
        return None


def tipoCambioMXN():
    api_key = "2783819ab9795ebb65cf80f8"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        exchange_rates = data["conversion_rates"]
        for currency, rate in exchange_rates.items():
            if currency == 'MXN':
                # print(f"1 USD = {round(float(rate),2)} {currency}")
                st = str(rate)
                return st[0:6]
    else:
        print("Error:", response.status_code)
        return None