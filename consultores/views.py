from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor, NotificationConsultor, NotificationAdministrador
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from datetime import date
from datetime import datetime
import calendar
from django.contrib.auth import login, logout, authenticate
import os
from django.http import HttpResponseRedirect
from default import views
from django.core.paginator import Paginator
from pytz import timezone
import shutil

@login_required
def miProfile(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)
        # print(informationPersonalUser)
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


        return render(request, 'miProfile.html', {
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
        ruta_destino = 'consultores/static/images/profile/' + informationPersonalUser.pais + '/' + informationConsultorUser.rfc

        # Verificar si el directorio existe, si no, crearlo
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        nombre_archivo = informationConsultorUser.rfc +'.jpg'  # Puedes generar un nombre único si lo deseas
        ruta_archivo = os.path.join(ruta_destino, nombre_archivo)

        with open(ruta_archivo, 'wb') as f:
            for chunk in imagen.chunks():
                f.write(chunk)

        user.image = '/static/images/profile/' + informationPersonalUser.pais + '/' + informationConsultorUser.rfc + '/' + nombre_archivo
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
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


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
                        print("La carpeta se ha eliminado correctamente.")
                    except OSError as e:
                        print("Error al eliminar la carpeta:", e)
                else:
                    print("La carpeta no existe.")

                informationConsultorUser.rfc = rfc

            informationConsultorUser.save()

            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


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
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


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
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


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
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


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
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


@login_required
def updateExperiencia(request):
    if request.method == 'POST':
        try:
            print("Hola---experienceia")
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
                print("Hola")
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
                print(experienciaRegistrada.id)
                experiencia.descripcion = actividades
                experiencia.empresa = empresa
                experiencia.puesto = puesto
                experiencia.id_experiencia = experienciaRegistrada
                experiencia.tiempo_experiencia=tiempoExperiencia
                experiencia.fecha_entrada=fecha_entrada
                experiencia.fecha_salida=fecha_salida
                # print(experiencia.id)
                experiencia.save()
                print(experiencia.id)


            return HttpResponse(status=200)
        except Consultores.DoesNotExist:
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)

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
            return HttpResponse(status=500)
        except Usuarios.DoesNotExist:
            return HttpResponse(status=500)
        except Personas.DoesNotExist:
            return HttpResponse(status=500)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


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
        

        notification = NotificationConsultor.objects.filter(id_consultor_destinatary=informationConsultorUser.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)

        # // ONLY 4 PENDING 
        pending = NotificationConsultor.objects.filter(status='Pending', id_consultor_destinatary=informationConsultorUser.id)[:4]

        return render(request, "principal.html", {
            'indice':'Principal',
            'image':user.image,
            'informationPersonalUser': informationPersonalUser,
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
def detallesProyecto(request):
    return render(request, "detalles_proyecto.html", {
        'indice':'Principal'
    })



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
            paginator = Paginator(notification_list, 6)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationConsultor.objects.filter(status='Pending',id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
            pending = NotificationConsultor.objects.filter(status='Pending',id_consultor_destinatary=informationConsultorUser.id).order_by('-created_at')[:4]
        else:
            notification = []
            pendind = []
            pending_total = []
            

        context = {
            'indice': 'Principal',
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
            'informationPersonalUser': informationPersonalUser,
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
    print("Hola")
    try:
        conocimiento = ConocimientosConsultor(pk=int(id))
        conocimiento.delete()
        return JsonResponse({'message': 'El objeto se ha eliminado correctamente.'}, status=200)
    except ConocimientoConsultor.DoesNotExist:
        return JsonResponse({'message': 'El objeto no existe.'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'message': f'Error al eliminar el objeto: {str(e)}'}, status=500)

