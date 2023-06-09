from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
import calendar
from django.contrib.auth import login, logout, authenticate
import os
from django.http import HttpResponseRedirect
from default import views


@login_required
def miProfile(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        informationConsultorUser = Consultores.objects.get(
            id_persona=informationPersonalUser)
        edad = calcular_edad(informationPersonalUser.fecha_nacimiento)
        maneraPago2 = ManeraPago.objects.get(
            pk=informationConsultorUser.id_manera_pago_id)

        tipoMoneda = TipoMoneda.objects.get(
            pk=informationConsultorUser.id_tipo_moneda_id)
        codigo_moneda = tipoMoneda.tipo.split('(')[1].split(')')[0]
        experienciasConsultor = ExperienciasConsultor.objects.filter(
            id_consultor=informationConsultorUser).order_by('-id').first()

        experienciaInicio = obtener_mes(experienciasConsultor.fecha_entrada)
        experienciaTermino = obtener_mes(experienciasConsultor.fecha_salida)

        if experienciasConsultor.tiempo_experiencia == 'Sigue Trabajando' or experienciasConsultor.tiempo_experiencia == '0':
            experienciaTermino = 'En proceso'

        estudiosConsultor = Estudios.objects.filter(
            id_consultor=informationConsultorUser).order_by('-id').first()

        institucion = Instituciones.objects.get(
            pk=estudiosConsultor.id_institucion_id)

        educacionInicio = obtener_mes(estudiosConsultor.fecha_ingreso)

        if estudiosConsultor.fecha_termino == 'Sigue Estudiando':
            educacionTermino = 'En proceso'
        elif len(estudiosConsultor.fecha_termino) == 10 and estudiosConsultor.fecha_termino[4] == '-' and estudiosConsultor.fecha_termino[7] == '-':
            # 2021-12-17
            componentes = estudiosConsultor.fecha_termino.split('-')
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

            print(meses[int(componentes[1])-1] + ' ' + componentes[0])
            educacionTermino = meses[int(
                componentes[1])-1] + ' ' + componentes[0]
        else:
            fecha = datetime.strptime(
                estudiosConsultor.fecha_termino, '%Y-%m-%d %H:%M:%S.%f')
            educacionTermino = obtener_mes(fecha)

        ruta = 'PDF/' + informationPersonalUser.pais + '/' + \
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

        # misIdiomas = list(IdiomasConsultor.objects.filter(id_consultor_id=informationConsultorUser.id))

        misIdiomas = IdiomasConsultor.objects.filter(
            id_consultor_id=informationConsultorUser.id)
        myLenguajes = []

        for idioma in misIdiomas:
            id = idioma.id
            nombre_idioma = Idiomas.objects.get(pk=idioma.id_idioma_id)
            nivel = idioma.nivel.split()[1]
            myLenguajes.append([id, nombre_idioma, nivel])

        return render(request, 'miProfile.html', {
            'titulo': 'Mi perfil',
            'indice': 'Perfil',
            'informationPersonalUser': informationPersonalUser,
            'correo': request.session.get('username'),
            'edad': edad,
            'maneraPago2': maneraPago2,
            'informationConsultorUser': informationConsultorUser,
            'maneraPago': maneraPago,
            'tipoMoneda': codigo_moneda,
            'experienciasConsultor': experienciasConsultor,
            'experienciaInicio': experienciaInicio,
            'experienciaTermino': experienciaTermino,
            'estudiosConsultor': estudiosConsultor,
            'institucion': institucion,
            'educacionInicio': educacionInicio,
            'educacionTermino': educacionTermino,
            'monedaCobro': monedaCobro,
            'maneraPago': maneraPago,
            'listaIdiomas': listaIdiomas,
            'misIdiomas': myLenguajes,
            'files': [
                searchFile(cv), searchFile(ine), searchFile(actaNac), searchFile(
                    pasaporte), searchFile(domicilio), searchFile(recomendacion), searchFile(f3),
            ]
        })

    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('login')


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

        directory = 'PDF/' + informationPersonalUser.pais + '/' + rfc

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
                    return redirect('login')

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
                print(maneraPago)
                informationConsultorUser.id_manera_pago = maneraPago
                print(informationConsultorUser.id)

            if hora:
                informationConsultorUser.tarifa_hora = hora

            if rfc:
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


def searchFile(ruta):
    if os.path.exists(ruta):
        return '1'
    else:
        return '0'

@login_required
def principal(request):
    return render(request, "principal.html")



@login_required
def detallesProyecto(request):
    return render(request, "detalles_proyecto.html")
