from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor,Empresas, NotificationEmpresa, Proyectos, ProyectoConsultor, NotificationConsultor, NotificationAdministrador, CategoriasConsultor, Bancos, DatosBancarios, Contratos, Facturas, ReporteHoras, ReporteFinalActividades
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from datetime import date
from datetime import datetime
import calendar
from django.contrib.auth import login, logout, authenticate
import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from pytz import timezone
import shutil
from django.http import HttpResponseNotFound
from django.http import FileResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


@login_required
def valdarEntrevista(request):
    return render(request, 'validate_interview.html')


@login_required
def all_notifications(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        notification_list = NotificationEmpresa.objects.filter(id_empresa_destinatary_id=empresa.id)
        if notification_list.exists():
            notification_list = notification_list.order_by('-created_at')
            paginator = Paginator(notification_list, 16)
            # print(paginator)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # CANT. NOTIFICATIONS PENDING
            pending_total = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary_id=empresa.id).order_by('-created_at')

            # ONLY 4 PENDING
            pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary_id=empresa.id).order_by('-created_at')[:4]
            
            return render(request, 'notifications/all_notificationsEmpresa.html', {
                'indice': 'Principal',
                'empresa':empresa,
                'notification':notification,
                'notification_pending': pending,
                'pending':pending,
                'pending_total':pending_total
            })
        else:
            notification_list = []
            return render(request, 'notifications/all_notificationsEmpresa.html', {
                'indice': 'Principal',
                'empresa':empresa,
                'notifications': [],
                'notification_pending': [],
                'pending': [],
                'pending_total': [],
            })


    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def view_notification(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
       
        # // DATA DE LA NOTIFICACION ELEGIDA
        notification = NotificationEmpresa.objects.get(pk=id, id_empresa_destinatary=empresa.id)

        # // EL STATUS CAMBIA A 'READ' Y GUARDA
        notification.status = 'Read'
        notification.save()
        # // NOTIFICATIONS DATA
        notification_data = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')

        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending',id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
        context = {
            'indice': 'Principal',
            'empresa':empresa,
            'notification':notification,
            'notifications':notification_data,
            'pending':pending,
            'pending_total':pending_total,
        }
        return render(request, "notifications/view_notificationEmpresa.html", context)


    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def formComentariosEvaluacion(request, id, prj):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        notification_data = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')

        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending',id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
        context = {
            'indice': 'Proyectos',
            'empresa':empresa,
            'consultor':id,
            'proyecto':prj,
            'notifications':notification_data,
            'pending':pending,
            'pending_total':pending_total,
        }

        return render(request, 'form_consultor_delete.html', context)


    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def datosBancarios(request):
    try:
        if request.method == 'GET':
            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)

            notification_data = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id).order_by('-created_at')
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')

            # // ONLY 4 PENDING 
            pending = NotificationEmpresa.objects.filter(status='Pending',id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
            context = {
                'indice': 'Proyectos',
                'empresa':empresa,
                'notifications':notification_data,
                'pending':pending,
                'pending_total':pending_total,
            }

            return render(request, 'data_bancosEmpresas.html', context)

        else:
            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)

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
                queryData.rfc_clave=clave
                queryData.dia_corte=dia_corte
                queryData.descripcion=descripcion
                queryData.activo=chec
                queryData.id_usuario=user
                queryData.save()

            except DatosBancarios.DoesNotExist:
                data = DatosBancarios(id_banco=bancoNew, sucursal=sucursal,cuentambiente=cuentambiente, tipo_cuenta=tipoCuenta, no_cuenta_clabe=no_cuenta, ejecutivo_cuenta=ejecutivo_cuenta, telefono_ejecutivo=telefono_ejecutivo,correo_ejecutivo=correo_ejecutivo,rfc_clave=clave, dia_corte=dia_corte, descripcion=descripcion,activo=chec, id_usuario=user)

                data.save()

            return redirect('my_projectsCreateds')

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def formComentarios(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        comentarios = request.POST['comentarios']
        calificacion = request.POST['calificacion']
        consultor = request.POST['consultor']
        proyecto = request.POST['proyecto']

        proyectoQuery = Proyectos.objects.get(pk=int(proyecto))
        consultorQuery = Consultores.objects.get(pk=int(consultor))

        query = ProyectoConsultor.objects.get(id_proyecto=proyectoQuery, id_consultor=consultorQuery)

        if query:
            persona = Personas.objects.get(pk=consultorQuery.id_persona.id)
            persona.disponible = True
            persona.save()
            query.comentario = comentarios
            query.puntuacion = calificacion
            query.participacion = False
            query.save()

            message='Has sido eliminado del proyecto ' + str(proyectoQuery.proyecto_nombre)
            newNotificacion = NotificationConsultor(name='Gnosis SC', email='gnosis@gmail.com', subject='Te han eliminado', message=message, status='Pending', id_consultor_destinatary_id=consultorQuery.id)
            newNotificacion.save()

        
            message = 'He eliminado al consultor ' + str(consultorQuery.id_persona.nombre) + ' ' + str(consultorQuery.id_persona.ape_pat) + ' de mi proyecto ' + str(proyectoQuery.proyecto_nombre)

            notificationAdministrador = NotificationAdministrador(name=empresa.empresa, email=empresa.id_usuario.correo, subject='Consultor eliminado', message=message, status='Pending', id_persona_destinatary_id=1, action=0)
            notificationAdministrador.save()

        parametros = {
            'prj': proyectoQuery.id,
        }
        url = reverse('details_project') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)


    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def consultorEmpresa(request, id, prj):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresas = Empresas.objects.get(id_usuario=user)
        # consultor = Usuarios.objects.get(pk=68)
        consultor = Usuarios.objects.get(id_persona_id=id)
        
        if consultor.is_superuser == 1:
            redirect('principalAdmin')
        
        informationPersonalUser = Personas.objects.get(pk=consultor.id_persona_id)
        informationConsultorUser = Consultores.objects.get(id_persona=informationPersonalUser)

        proyectos = ProyectoConsultor.objects.filter(id_consultor=informationConsultorUser.id)

        if proyectos.exists():  # Verificar si hay proyectos
            cantidad_proyectos = proyectos.count()
            
            puntuacion = 0

            for proyecto in proyectos:
                puntos = proyecto.puntuacion
                if puntos is not None:  # Verificar si el valor no es None
                    puntuacion += float(puntos)

            if cantidad_proyectos != 0:  # Asegurarse de que no se esté dividiendo por cero
                puntuacionConsultor = puntuacion / cantidad_proyectos
            else:
                puntuacionConsultor = 0
                cantidad_proyectos = 0
        else:
            puntuacionConsultor = 0
            cantidad_proyectos = 0

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
        listaCategorias = list(CategoriasConsultor.objects.values())
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
                nivelGnosis = NivelesConocimiento.objects.get(pk=moduloConsulta.id_nivelGnosis_id)
                valido = moduloConsulta.estatus
                myModuls.append([id, modulo, submodulo, nivel, c, nivelGnosis, valido])
        else:
            myModuls = []


        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary_id=empresas.id)
                # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary_id=empresas.id).order_by('-created_at')
                # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary_id=empresas.id).order_by('-created_at')[:4]

        return render(request, 'consultores/profileConsultor.html', {
            'indice': 'Proyectos',
            'empresa':empresas,
            'informationPersonalUser': informationPersonalUser,
            'correo': consultor.correo,
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
            'proyectos':proyectos,
            'cantidad_proyectos':cantidad_proyectos,
            'puntuacionConsultor':puntuacionConsultor,
            'listaNivelesConocimiento':listaNivelesConocimiento,
            'misModulos':myModuls,
            'listaCategorias':listaCategorias,
            'proyecto':prj,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
            'files': [
                searchFile(cv), searchFile(ine), searchFile(actaNac), searchFile(
                    pasaporte), searchFile(domicilio), searchFile(recomendacion), searchFile(f3),
            ]
        })
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

def searchFile(ruta):
    if os.path.exists(ruta):
        #print(ruta)
        return '1'
    else:
        return '0'





@login_required
def consultorFacturas(request, id, prj):
    try:
        if request.method == 'GET':
            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)
            
            informationConsultorUser = Consultores.objects.get(pk=int(id))
            proyecto = Proyectos.objects.get(pk=int(prj))

            colaborador = ProyectoConsultor.objects.filter(id_proyecto=proyecto,id_consultor=informationConsultorUser)

            if colaborador:
                id_proyecto_consultor_list = colaborador.values_list('id', flat=True)

                try:
                    # Obtener todos los contratos asociados a los id_proyecto_consultor
                    contratos = Contratos.objects.get(id_proyecto_consultor__in=id_proyecto_consultor_list)
                except Contratos.DoesNotExist as error:
                    contratos = None

                facturas = Facturas.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)

                regitrosFacturas = []
                for f in facturas:
                    id = f.id
                    periodo = f.periodo
                    fecha = f.id_documentacion.fecha_creacion
                    directory = str(f.id_documentacion.ruta) + '/' + str(f.id_documentacion.nombre)
                    entregado = searchFile(directory)
                    validacionGnosis = f.validacionGnosis
                    validacionEmpresa = f.validacionEmpresa
                    tipoCambio = f.tipoCambioMXN
                    tipoCambioUSD = f.tipoCambioUSD

                    regitrosFacturas.append([periodo, entregado, validacionGnosis, validacionEmpresa, fecha, id, f.id_documentacion.ruta,f.id_documentacion.nombre,tipoCambio,tipoCambioUSD ])


            notification_data = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id).order_by('-created_at')
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')

            # // ONLY 4 PENDING 
            pending = NotificationEmpresa.objects.filter(status='Pending',id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
            context = {
                'indice': 'Proyectos',
                'empresa':empresa,
                'contrato':contratos,
                'facturas':regitrosFacturas,
                'persona':informationConsultorUser.id_persona,
                'notifications':notification_data,
                'pending':pending,
                'pending_total':pending_total,
            }

            return render(request, 'consultores/facturas.html', context)

        
            

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def validarFacturas(request):
    try:
        if request.method == 'POST':
            facturaValue = request.POST['factura']
    
            factura = Facturas.objects.get(pk=int(facturaValue))
            
            if 'validar' in request.POST:
                factura.validacionEmpresa = 'Aceptada'
                factura.save()
            else:
                factura.validacionEmpresa = 'Rechazada'
                factura.save()

            message = 'Ya puedes consultar el estado de tu factura de parte de ' + str(factura.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.empresa) +' para el proyecto ' + str(factura.id_proyecto_consultor.id_proyecto.proyecto_nombre)

            newNotificacion = NotificationConsultor(name=str(factura.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.empresa), email=str(factura.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.id_usuario.correo), subject='El estado de tu factura', message=message, status='Pending', id_consultor_destinatary_id=factura.id_proyecto_consultor.id_consultor.id)
                
            newNotificacion.save()

            url = reverse('consultorFacturas', args=[factura.id_proyecto_consultor.id_consultor.id, factura.id_proyecto_consultor.id_proyecto.id])

            # Redirigir a la URL construida
            return redirect(url)
            
    except Facturas.DoesNotExist as error:
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
def consultorDocumentosShowXML(request):
    try:
        ruta = request.GET.get('ruta', None)  
        nombre_file = request.GET.get('nameFile', None)
        
        ruta_xml = os.path.join(ruta, nombre_file)
        
        # print(ruta_xml)
        if os.path.exists(ruta_xml):
            return FileResponse(open(ruta_xml, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        else:
            return HttpResponseNotFound()
    
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')




@login_required
def consultorReportes(request, id, prj):
    try:
        if request.method == 'GET':
            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)
            
            informationConsultorUser = Consultores.objects.get(pk=int(id))
            proyecto = Proyectos.objects.get(pk=int(prj))

            colaborador = ProyectoConsultor.objects.filter(id_proyecto=proyecto,id_consultor=informationConsultorUser)

            if colaborador:
                id_proyecto_consultor_list = colaborador.values_list('id', flat=True)

                # Obtener todos los contratos asociados a los id_proyecto_consultor
                contratos = Contratos.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)

                reportesHoras = ReporteHoras.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)

                regitrosReportesHoras = []
                for f in reportesHoras:
                    id = f.id
                    periodo = f.periodo
                    fecha = f.id_documentacion.fecha_creacion
                    directory = str(f.id_documentacion.ruta) + '/' + str(f.id_documentacion.nombre)
                    entregado = searchFile(directory)
                    validacionGnosis = f.validacionGnosis
                    validacionEmpresa = f.validacionEmpresa

                    regitrosReportesHoras.append([periodo, entregado, validacionGnosis, validacionEmpresa, fecha, id, f.id_documentacion.ruta,f.id_documentacion.nombre ])


                reportesFinales = ReporteFinalActividades.objects.filter(id_proyecto_consultor__in=id_proyecto_consultor_list)

                regitrosReportesFinales = []
                for f in reportesFinales:
                    id = f.id
                    periodo = f.periodo
                    fecha = f.id_documentacion.fecha_creacion
                    directory = str(f.id_documentacion.ruta) + '/' + str(f.id_documentacion.nombre)
                    entregado = searchFile(directory)
                    validacionGnosis = f.validacionGnosis
                    validacionEmpresa = f.validacionEmpresa

                    regitrosReportesFinales.append([periodo, entregado, validacionGnosis, validacionEmpresa, fecha, id, f.id_documentacion.ruta,f.id_documentacion.nombre ])

            notification_data = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id).order_by('-created_at')
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')

            # // ONLY 4 PENDING 
            pending = NotificationEmpresa.objects.filter(status='Pending',id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
            context = {
                'indice': 'Proyectos',
                'empresa':empresa,
                'contrato':contratos,
                'reporteHoras':regitrosReportesHoras,
                'reportesFinales':regitrosReportesFinales,
                'persona':informationConsultorUser.id_persona,
                'notifications':notification_data,
                'pending':pending,
                'pending_total':pending_total,
            }

            return render(request, 'consultores/reportes.html', context)

        
            

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')
    except Empresas.DoesNotExist as error:
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
def validarHoras(request):
    try:
        if request.method == 'POST':
            reporteHora = request.POST['reporteHora']
    
            reporte = ReporteHoras.objects.get(pk=int(reporteHora))
            
            if 'validar' in request.POST:
                reporte.validacionEmpresa = 'Aceptada'
                reporte.save()
            else:
                reporte.validacionEmpresa = 'Rechazada'
                reporte.save()

            message = 'Ya puedes consultar el estado de tu reporte de horas de parte de ' + str(reporte.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.empresa) +' para el proyecto ' + str(reporte.id_proyecto_consultor.id_proyecto.proyecto_nombre)

            newNotificacion = NotificationConsultor(name=str(reporte.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.empresa), email=str(reporte.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.id_usuario.correo), subject='El estado de tu reporte de horas', message=message, status='Pending', id_consultor_destinatary_id=reporte.id_proyecto_consultor.id_consultor.id)
                
            newNotificacion.save()

            url = reverse('consultorReportes', args=[reporte.id_proyecto_consultor.id_consultor.id, reporte.id_proyecto_consultor.id_proyecto.id])

            # Redirigir a la URL construida
            return redirect(url)
            
    except Facturas.DoesNotExist as error:
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
def validarReporteFinal(request):
    try:
        if request.method == 'POST':
            reporteFinal = request.POST['reporteFinal']
    
            reporte = ReporteFinalActividades.objects.get(pk=int(reporteFinal))
            
            if 'validar' in request.POST:
                reporte.validacionEmpresa = 'Aceptada'
                reporte.save()
            else:
                reporte.validacionEmpresa = 'Rechazada'
                reporte.save()

            message = 'Ya puedes consultar el estado de tu reporte final de actividades de parte de ' + str(reporte.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.empresa) +' para el proyecto ' + str(reporte.id_proyecto_consultor.id_proyecto.proyecto_nombre)

            newNotificacion = NotificationConsultor(name=str(reporte.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.empresa), email=str(reporte.id_proyecto_consultor.id_proyecto.id_empresa_proyecto.id_empresa.id_usuario.correo), subject='El estado de tu reporte final', message=message, status='Pending', id_consultor_destinatary_id=reporte.id_proyecto_consultor.id_consultor.id)
                
            newNotificacion.save()

            url = reverse('consultorReportes', args=[reporte.id_proyecto_consultor.id_consultor.id, reporte.id_proyecto_consultor.id_proyecto.id])

            # Redirigir a la URL construida
            return redirect(url)
            
    except Facturas.DoesNotExist as error:
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
def curriculum_vitaeEmpresa(request, id):
    try:
        
        try:
            informationConsultorUser = Consultores.objects.get(pk=id)
            informationPersonalUser = Personas.objects.get(pk=informationConsultorUser.id_persona.id)
            user = Usuarios.objects.get(id_persona=informationPersonalUser)
    
            #SE PIDEN LOS DATOS A LOS MODELOS
            estudios = Estudios.objects.filter (id_consultor = informationConsultorUser ) #educacion
            curso = CursosConsultor.objects.filter  (id_consultor = informationConsultorUser  ) #certificaciones
            modulos = ConocimientosConsultor.objects.filter( id_consultor = informationConsultorUser  )
            idiomas = IdiomasConsultor.objects.filter( id_consultor = informationConsultorUser)
            proyectoConsultor = ProyectoConsultor.objects.filter(id_consultor = informationConsultorUser  )

            # Pasar los datos al HTML que servirá como plantilla para el PDF
            template_path = "consultores/curriculum.html"
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

        except IdiomasConsultor.DoesNotExist as error:
            print(f"Error: {str(error)}")
            return redirect('my_projectsCreateds')

        except ProyectoConsultor.DoesNotExist as error:
            print(f"Error: {str(error)}")
            return redirect('my_projectsCreateds')
    
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return redirect('my_projectsCreateds')
    except Exception as e:
        print(e)
        return redirect('my_projectsCreateds')
