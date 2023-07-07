from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor, NotificationConsultor, NotificationAdministrador
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
import calendar
from django.contrib.auth import login, logout, authenticate
import os
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from pytz import timezone
from django.conf import settings
from django.http import FileResponse
from django.urls import reverse
from django.http import HttpResponseNotFound


@login_required
def miConsultorProfile(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalAdministradorUser = Personas.objects.get(pk=user.id_persona_id)
        
        # consultor = Usuarios.objects.get(pk=68)
        consultor = Usuarios.objects.get(id_persona=int(id))
        
        if consultor.is_superuser == 1:
            redirect('principalAdmin')
        
        
        informationPersonalUser = Personas.objects.get(pk=consultor.id_persona_id)
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
                nivelGnosis = NivelesConocimiento.objects.get(pk=moduloConsulta.id_nivelGnosis_id)
                valido = moduloConsulta.estatus
                myModuls.append([id, modulo, submodulo, nivel, c, nivelGnosis, valido])
        else:
            myModuls = []

        notification_list = NotificationAdministrador.objects.filter(id_persona_destinatary=informationPersonalAdministradorUser.id).order_by('-created_at')
        # //Pagination

        # //Cantidad de notificaciones que apareceran antes de crear otra page
        if notification_list.exists():
            paginator = Paginator(notification_list, 6)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationAdministrador.objects.filter(status='Pending',id_persona_destinatary=informationPersonalAdministradorUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
            pending = NotificationAdministrador.objects.filter(status='Pending',id_persona_destinatary=informationPersonalAdministradorUser.id).order_by('-created_at')[:4]
        else:
            notification = []
            pending = []
            pending_total = []

        return render(request, 'profileConsultor.html', {
            'titulo': 'Mi perfil',
            'indice': 'Consultores',
            'image':consultor.image,
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
def principal(request):
    try:

        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
        print(informationPersonalUser.id)
        notification_list = NotificationAdministrador.objects.filter(id_persona_destinatary=informationPersonalUser.id).order_by('-created_at')
        # //Pagination
        print(notification_list)
        # //Cantidad de notificaciones que apareceran antes de crear otra page
        if notification_list.exists():
            paginator = Paginator(notification_list, 6)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationAdministrador.objects.filter(status='Pending',id_persona_destinatary=informationPersonalUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
            pending = NotificationAdministrador.objects.filter(status='Pending',id_persona_destinatary=informationPersonalUser.id).order_by('-created_at')[:4]
        else:
            notification = []
            pending = []
            pending_total = []
        
        listaIdiomas = list(Idiomas.objects.values())
        listaModulos = list(Modulos.objects.values())
        listaSubodulos = list(Submodulos.objects.values())
        listaNivelesConocimiento = list(NivelesConocimiento.objects.values())

        return render(request, 'principalAdministradores.html',{
            'informationPersonalUser': informationPersonalUser,
            'indice':'Principal',
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
            'listaIdiomas': listaIdiomas,
            'listaModulos':listaModulos,
            'listaSubodulos':listaSubodulos,
            'listaNivelesConocimiento':listaNivelesConocimiento,
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


@login_required
def updateModulosSAPAdmin(request):
    if request.method == 'POST':
        try:
            consultorID = request.POST.get('saber', '')
            nivelConsultor = request.POST.get('nivelConsultor', '')
            nivelGnosis = request.POST.get('nivelGnosis', '')
            print(consultorID)
            print(nivelConsultor)
            print(nivelGnosis)
            user = Usuarios.objects.get(pk=68)
            informationPersonalUser = Personas.objects.get(
                pk=user.id_persona_id)
            informationConsultorUser = Consultores.objects.get(
                id_persona=informationPersonalUser)

            nivelesConocimientoConsultor = NivelesConocimiento.objects.get(pk=int(nivelConsultor))
            nivelesConocimientoGnosis = NivelesConocimiento.objects.get(pk=int(nivelGnosis))

            if consultorID and nivelConsultor and nivelGnosis:
                print(user.id)
                consulta = ConocimientosConsultor.objects.filter(
                    Q(pk=consultorID) & Q(id_consultor=informationConsultorUser))
                print(consulta)
                if consulta.exists():
                    print(consulta)
                    objeto_consulta = consulta.first()
                    objeto_consulta.id_nivel = nivelesConocimientoConsultor
                    objeto_consulta.id_nivelGnosis = nivelesConocimientoGnosis
                    objeto_consulta.estatus = 'Validado'
                    objeto_consulta.save()
                    
                    newNotificacion = NotificationConsultor(name='Gnosis SC', email='gnosis@gmail.com', subject='Validacion exitosa Modulos SAP Test', message='Validacion exitosa Modulos SAP', status='Pending', id_consultor_destinatary_id=informationConsultorUser.id)
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
def all_notifications(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)

        notification_list = NotificationAdministrador.objects.filter(id_persona_destinatary_id=informationPersonalUser.id)
        if notification_list.exists():
        
            notification_list = notification_list.order_by('-created_at')
            paginator = Paginator(notification_list, 6)
            print(paginator)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # CANT. NOTIFICATIONS PENDING
            pending_total = NotificationAdministrador.objects.filter(status='Pending', id_persona_destinatary_id=informationPersonalUser.id).order_by('-created_at')

            # ONLY 4 PENDING
            pending = NotificationAdministrador.objects.filter(status='Pending', id_persona_destinatary_id=informationPersonalUser.id).order_by('-created_at')[:4]
            
            return render(request, 'notifications/all_notificationsAdministrador.html', {
                'informationPersonalUser': informationPersonalUser,
                'indice': 'Principal',
                'notification':notification,
                'notification_pending': pending,
                'pending':pending,
                'pending_total':pending_total
            })
        else:
            notification_list = []
            return render(request, 'notifications/all_notificationsAdministrador.html', {
                'informationPersonalUser': informationPersonalUser,
                'indice': 'Principal',
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
def view_notification(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        informationPersonalUser = Personas.objects.get(pk=user.id_persona_id)
       
        # // DATA DE LA NOTIFICACION ELEGIDA
        notification = NotificationAdministrador.objects.get(pk=id, id_persona_destinatary=informationPersonalUser.id)

        # // EL STATUS CAMBIA A 'READ' Y GUARDA
        notification.status = 'Read'
        notification.save()
        # // NOTIFICATIONS DATA
        notification_data = NotificationAdministrador.objects.filter(id_persona_destinatary=informationPersonalUser.id).order_by('-created_at')
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationAdministrador.objects.filter(status='Pending', id_persona_destinatary=informationPersonalUser.id).order_by('-created_at')

        # // ONLY 4 PENDING 
        pending = NotificationAdministrador.objects.filter(status='Pending',id_persona_destinatary=informationPersonalUser.id).order_by('-created_at')[:4]
        context = {
            'indice': 'Principal',
            'informationPersonalUser': informationPersonalUser,
            'notification':notification,
            'notifications':notification_data,
            'pending':pending,
            'pending_total':pending_total,
        }
        return render(request, "notifications/view_notificationAdministrador.html", context)


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
def getConsultoresDisponiblesWithFilters(request):
    if request.method == 'POST':
        try:
            moduloFilter = request.POST.get('modulo-filter', '')
            submoduloFilter = request.POST.get('submodulo-filter', '')
            nivelFilter = request.POST.get('nivel-filter', '')
            tarifaFilter = request.POST.get('tarifa-filter', '')
            disponibleFilter = request.POST.get('disponible-filter', '')
            NdisponibleFilter = request.POST.get('Ndisponible-filter', '')
            nivelInglesFilter = request.POST.get('nivelIngles-filter', '')
            nivelEstudiosFilter = request.POST.get('nivelEstudios-filter', '')
            certificadosFilter = request.POST.get('certificados-filter', '')
            print("---- Datos recibidos ----")
            print("mod " + moduloFilter)
            print("sub " + submoduloFilter)
            print("nivel " + nivelFilter)
            print("tarifa " + tarifaFilter)
            print("disp " + disponibleFilter)
            print("ndisp " + NdisponibleFilter)
            print("ingle " + nivelInglesFilter)
            print("estudi " + nivelEstudiosFilter)
            print("certif " + certificadosFilter)

            print("\n")

            if disponibleFilter:
                print("disponible")
                personas = Personas.objects.filter(disponible=int(disponibleFilter))

            if NdisponibleFilter:
                print("no dispo")
                personas = Personas.objects.filter(disponible=int(NdisponibleFilter))
            print("\n")

            consultores = Consultores.objects.filter(id_persona__in=personas, tarifa_hora__lte=int(tarifaFilter))
            
            if not moduloFilter and not submoduloFilter and not nivelFilter:
                print("no hay modulo aplicados")
                consultoresModulosSAP = []
            else:
                print("hay modulos aplicados")
                conocimientosConsultor = ConocimientosConsultor.objects.filter(id_consultor__in=consultores)
                if moduloFilter:
                    print("modulo")
                    modulo = Modulos.objects.get(pk=int(moduloFilter))
                    conocimientosConsultor = conocimientosConsultor.filter(id_modulo=modulo)
                print("\n")
                if submoduloFilter:
                    print("submo")
                    submodulo = Submodulos.objects.get(pk=int(submoduloFilter))
                    conocimientosConsultor = conocimientosConsultor.filter(id_submodulo=submodulo)
                print("\n")
                if nivelFilter:
                    print("nivelk")
                    nivelK = NivelesConocimiento.objects.get(pk=int(nivelFilter))
                    conocimientosConsultor = conocimientosConsultor.filter(id_nivel=nivelK)
                print("\n")
                

                consultoresModulosSAP = []
                for modulosSAP in conocimientosConsultor:
                    consultoresR = Consultores.objects.filter(pk=modulosSAP.id_consultor_id)
                    # print(consultores)
            
                consultores = Consultores.objects.filter(id__in=conocimientosConsultor.values_list('id_consultor_id', flat=True))
            

            resultadosIngles = []
            if nivelInglesFilter:
                print("nivel imgles")
                for consultor in consultores:
                    try:
                        nivelIngles = IdiomasConsultor.objects.get(id_consultor=consultor.id, id_idioma=3, nivel=nivelInglesFilter)
                        # print("si")
                        resultadosIngles.append(nivelIngles)
                        # Resto de tu lógica aquí
                    except IdiomasConsultor.DoesNotExist:
                        # print("no")
                        pass
                # print(resultadosIngles)
                consultores = Consultores.objects.filter(id__in=[resultado.id_consultor.id for resultado in resultadosIngles])
            else:
                print("no hay nivel ingles")

            print("\n")

            resultadosEstudios = []
            if nivelEstudiosFilter:
                print("estudios educativos")
                for consultor in consultores:
                    try:
                        estudios = Estudios.objects.get(id_consultor=consultor.id, educacion=nivelEstudiosFilter)
                        # print("si")
                        resultadosEstudios.append(estudios)
                        # Resto de tu lógica aquí
                    except Estudios.DoesNotExist:
                        pass
                # print(resultadosIngles)
                consultores = Consultores.objects.filter(id__in=[resultado.id_consultor.id for resultado in resultadosEstudios])
            else:
                print("no hay nivel estudios")
            print("\n")


            resultadoscertificicaciones = []
            if certificadosFilter:
                print("certificados")
                for consultor in consultores:
                    try:
                        certificados = CursosConsultor.objects.get(id_consultor=consultor.id, nombre_curso__icontains=certificadosFilter)
                        # print("si")
                        resultadoscertificicaciones.append(certificados)
                        # Resto de tu lógica aquí
                    except CursosConsultor.DoesNotExist:
                        # print("no")
                        pass
                # print(resultadosIngles)
                consultores = Consultores.objects.filter(id__in=[resultado.id_consultor.id for resultado in resultadoscertificicaciones])
            else:
                print("no hay nivel certificados")
            print("\n")
            # print(consultores)

        
            
            correos = []
            for consultor in consultores:
                # print(consultor.id_persona)
                usuarios = Usuarios.objects.filter(id_persona=consultor.id_persona, is_superuser=0)
                if usuarios.exists():
                    correo = usuarios[0].correo
                    correos.append(correo)

            usuariosPersona = Usuarios.objects.filter(correo__in=correos)
            #print(usuariosPersona)
            
            personasResultado = []
            for usuario in usuariosPersona:
                persona = Personas.objects.get(pk=usuario.id_persona_id)
                personasResultado.append(persona)

            resultados = []
            # print(resultados)
            for persona in personasResultado:
                img = Usuarios.objects.get(id_persona_id=persona.id)
                
                if not img.image:
                    if persona.sexo == 'M':
                        imgn = '/static/images/profile/default.jpg'
                    else:
                        imgn = '/static/images/profile/defaultF.png'
                else:
                    imgn = img.image
                # Agregar los campos que desees incluir en la respuesta
                resultados.append({
                    'id':persona.id,
                    'nombre': persona.nombre,
                    'ape_pat': persona.ape_pat,
                    'ape_mat': persona.ape_mat,
                    'municipio':persona.municipio,
                    'ciudad':persona.ciudad,
                    'colonia':persona.colonia,
                    'image':imgn
                    # Agrega más campos si es necesario
                })
            # print(resultados)

            # Crear el diccionario de respuesta
            response_data = {
                'status': 200,  # Código de estado de respuesta exitosa
                'message': 'Búsqueda exitosa',
                'results': resultados,
            }

            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)




@login_required
def queryForName(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '')
            apepa = request.POST.get('apepa', '')
            apema = request.POST.get('apema', '')

            personas = Personas.objects.filter(nombre__icontains=nombre, ape_pat__icontains=apepa, ape_mat__icontains=apema)

            consultores = Consultores.objects.filter(id_persona__in=personas)

            correos = []
            for consultor in consultores:
                usuarios = Usuarios.objects.filter(id_persona=consultor.id_persona, is_superuser=0)
                if usuarios.exists():
                    correo = usuarios[0].correo
                    correos.append(correo)

            usuariosPersona = Usuarios.objects.filter(correo__in=correos)
            personasResultado = []
            for usuario in usuariosPersona:
                persona = Personas.objects.get(pk=usuario.id_persona_id)
                personasResultado.append(persona)

            resultados = []
            for persona in personasResultado:
                img = Usuarios.objects.get(id_persona_id=persona.id)
                
                if not img.image:
                    if persona.sexo == 'M':
                        imgn = '/static/images/profile/default.jpg'
                    else:
                        imgn = '/static/images/profile/defaultF.png'
                else:
                    imgn = img.image
                # Agregar los campos que desees incluir en la respuesta
                resultados.append({
                    'id':persona.id,
                    'nombre': persona.nombre,
                    'ape_pat': persona.ape_pat,
                    'ape_mat': persona.ape_mat,
                    'municipio':persona.municipio,
                    'ciudad':persona.ciudad,
                    'colonia':persona.colonia,
                    'image':imgn
                    # Agrega más campos si es necesario
                })

            # Crear el diccionario de respuesta
            response_data = {
                'status': 200,  # Código de estado de respuesta exitosa
                'message': 'Búsqueda exitosa',
                'results': resultados,
            }

            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)



@login_required
def getConsultoresDisponibles(request):
    if request.method == 'GET':
        try:
            nombre = request.POST.get('nombre', '')
            apepa = request.POST.get('apepa', '')
            apema = request.POST.get('apema', '')

            personas = Personas.objects.filter(disponible=1)

            consultores = Consultores.objects.filter(id_persona__in=personas)

            correos = []
            for consultor in consultores:
                usuarios = Usuarios.objects.filter(id_persona=consultor.id_persona, is_superuser=0)
                if usuarios.exists():
                    correo = usuarios[0].correo
                    correos.append(correo)

            usuariosPersona = Usuarios.objects.filter(correo__in=correos)
            personasResultado = []
            for usuario in usuariosPersona:
                persona = Personas.objects.get(pk=usuario.id_persona_id)
                personasResultado.append(persona)

            resultados = []
            for persona in personasResultado:
                img = Usuarios.objects.get(id_persona_id=persona.id)
                
                if not img.image:
                    if persona.sexo == 'M':
                        imgn = '/static/images/profile/default.jpg'
                    else:
                        imgn = '/static/images/profile/defaultF.png'
                else:
                    imgn = img.image

                # Agregar los campos que desees incluir en la respuesta
                resultados.append({
                    'id':persona.id,
                    'nombre': persona.nombre,
                    'ape_pat': persona.ape_pat,
                    'ape_mat': persona.ape_mat,
                    'municipio':persona.municipio,
                    'ciudad':persona.ciudad,
                    'colonia':persona.colonia,
                    'image':imgn
                    # Agrega más campos si es necesario
                })

            # Crear el diccionario de respuesta
            response_data = {
                'status': 200,  # Código de estado de respuesta exitosa
                'message': 'Búsqueda exitosa',
                'results': resultados,
            }

            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)


@login_required
def consultorDocumentacion(request):
    try:
        # Lógica para obtener la ruta del archivo PDF
        # ruta_pdf = "PDF/México/456784567895/456784567895_CV.pdf"
        pais = request.GET.get('pais', None)  
        rfc = request.GET.get('rfc', None)
        id = request.GET.get('id', None)  
        format = request.GET.get('format', None)  
        file = request.GET.get('file', None)
        nombre_pdf = rfc+'_'+file+'.'+format
        # consultor = Usuarios.objects.get(pk=68)
        informationConsultorUser = Consultores.objects.get(pk=int(id))
        informationPersonalUser = Personas.objects.get(pk=informationConsultorUser.id_persona_id)

        # Generar la URL para el archivo PDF
        url_pdf = reverse('servir_pdf', kwargs={'pais': pais, 'rfc': rfc, 'nombre_pdf': nombre_pdf})
        # Redirigir al usuario a la URL del PDF
        return redirect(url_pdf)
    
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('principalAdmin')
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        # Error generado por que el usuario no realizo su registro completo, para solucionar el error se debera borrar todo el rastro del usuario, y buscar las relaciones perdidas
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('principalAdmin')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


def servir_pdf(request, pais, rfc, nombre_pdf):
    ruta_pdf = os.path.join(settings.MEDIA_ROOT, 'PDF', pais, rfc, nombre_pdf)
    if os.path.exists(ruta_pdf):
        return FileResponse(open(ruta_pdf, 'rb'), content_type='application/pdf')
    else:
        return HttpResponseNotFound()


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
        return '1'
    else:
        return '0'

