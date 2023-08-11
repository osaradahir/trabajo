from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor,Empresas, NotificationEmpresa, Categorias, Proyectos, EmpresaProyecto, RequerimientosModulosProyecto, RequerimientosIdiomasProyecto, PostulacionesProyecto, NotificationConsultor, EntrevistasConsultoresProyecto, ProyectoConsultor, NotificationAdministrador, PostulacionesProyectoGnosis, NotasGnosisConsultor
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from .config import cipher_suite
from cryptography.fernet import Fernet
from datetime import date
from datetime import datetime
import calendar, re
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
import os
import json
import pickle
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from pytz import timezone
import shutil
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

@login_required
def my_projects(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        empresaProyectos = EmpresaProyecto.objects.filter(id_empresa_id=empresa.id)
        query = request.GET.get('query')
        if empresaProyectos.exists():
            if not query:
                proyectos = Proyectos.objects.filter(id_empresa_proyecto__in=empresaProyectos).order_by('-id')
            else:
                proyectos = Proyectos.objects.filter(proyecto_nombre__icontains=query,id_empresa_proyecto__in=empresaProyectos).order_by('-id')

            paginator = Paginator(proyectos, 6)
            page = request.GET.get('page')
            proyecto = paginator.get_page(page)

            staffing = Proyectos.objects.filter(id_empresa_proyecto__in=empresaProyectos, status='Staffing').order_by('-id').first()
            # Obtiene la fecha actual
            fecha_actual = datetime.now().date()

            # Fecha de publicación del staffing (ejemplo)
            fecha_publicacion = staffing.fecha_publicacion

            # Calcula la diferencia de días
            diferencia = fecha_actual - fecha_publicacion
            dias_pasados = diferencia.days

            if dias_pasados > 30:
                diasStaffing = 'Hace mas de un mes'
            elif dias_pasados == 0:
                diasStaffing = 'Hoy'
            else:
                diasStaffing = str(dias_pasados) + ' días'

        else:
            proyectos = 0
            proyecto = ''
            staffing = ''
            diasStaffing = ''

        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]

        return render(request, 'my_projects.html',{
            'indice': 'Proyectos',
            'empresa':empresa,
            'proyectos':proyectos,  
            'proyecto':proyecto,
            'staffing':staffing,   
            'diasStaffing':diasStaffing,       
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def create_new_project(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        monedaCobro = list(TipoMoneda.objects.values())
        categorias = list(Categorias.objects.values())

        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]


        return render(request, 'create_new_project.html',{
            'indice': 'Proyectos',
            'empresa':empresa,
            'monedaCobro': monedaCobro,
            'categorias':categorias,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


@login_required
def requirements_project(request):
    try:
        if request.method == 'GET':
            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)

            listaModulos = list(Modulos.objects.values())
            listaSubodulos = list(Submodulos.objects.values())
            listaNivelesConocimiento = list(NivelesConocimiento.objects.values())
            
            notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
            # // ONLY 4 PENDING 
            pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]

            return render(request, 'requirements_project.html',{
                'indice': 'Proyectos',
                'empresa':empresa,
                'listaModulos':listaModulos,
                'listaSubodulos':listaSubodulos,
                'listaNivelesConocimiento':listaNivelesConocimiento,
                'notifications':notification,
                'pending':pending,
                'pending_total':pending_total,
            })
        else:
            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)
            presupuesto = request.POST['presupuesto']
            modulo = request.POST['modulo']
            submodulo = request.POST['submodulo']
            experienciaRequerida = request.POST['experienciaRequerida']
            experienciaDesesada = request.POST['experienciaDesesada']
            requerimientosModulosProyecto = []
            tabla_datos = request.POST.get('tablaDatos')  # Obtener la cadena JSON del POST

            if tabla_datos:
                try:
                    tabla_datos = json.loads(tabla_datos)
                    for fila in tabla_datos:
                        requerimientos = RequerimientosModulosProyecto(
                            id_empresa=empresa,
                            id_modulo=Modulos.objects.get(nombre=fila[0]),
                            id_submodulo=Submodulos.objects.get(nombre=fila[1]),
                            id_experiencia_requerida=NivelesConocimiento.objects.get(nombre=fila[2]),
                            id_experiencia_deseable=NivelesConocimiento.objects.get(nombre=fila[3])
                        )
                        requerimientosModulosProyecto.append([requerimientos])
                    # print(requerimientosModulosProyecto)
                    print("Con modulos adicionales")
                except json.JSONDecodeError:
                    print("Sin modulos adicionales")
            else:
                print("Sin modulos adicionales")


            params = {
                'presupuesto': cipher_suite.encrypt(presupuesto.encode('utf-8')).decode('utf-8'),
                'modulo': cipher_suite.encrypt(modulo.encode('utf-8')).decode('utf-8'),
                'submodulo': cipher_suite.encrypt(submodulo.encode('utf-8')).decode('utf-8'),
                'experienciaRequerida': cipher_suite.encrypt(experienciaRequerida.encode('utf-8')).decode('utf-8'),
                'experienciaDesesada': cipher_suite.encrypt(experienciaDesesada.encode('utf-8')).decode('utf-8'),
            }

            for i, requerimiento in enumerate(requerimientosModulosProyecto):
                requerimiento_str = pickle.dumps(requerimiento)
                requerimiento_encoded = cipher_suite.encrypt(requerimiento_str).decode('utf-8')
                params[f'requerimiento{i}'] = requerimiento_encoded

            query_string = urlencode(params)
            redirect_url = reverse('requerimientosEducationProyecto') + '?' + request.GET.urlencode() + '&' + query_string
            return redirect(redirect_url)
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def requirements_education_project(request):
    try:
        if request.method == 'GET':

            # print(request.GET.get('modulosSAP')

            user = Usuarios.objects.get(correo=request.session.get('username'))
            empresa = Empresas.objects.get(id_usuario=user)
            listaIdiomas = list(Idiomas.objects.values())
            notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
            # // CANT. NOTIFICATIONS PENDING
            pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
            # // ONLY 4 PENDING 
            pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]


            return render(request, 'requirements_education_project.html',{
                'indice': 'Proyectos',
                'empresa':empresa,
                'listaIdiomas':listaIdiomas,
                'notifications':notification,
                'pending':pending,
                'pending_total':pending_total,
            })
    
        else:
            consultoresCantidad = request.POST['consultoresCantidad']
            certificacionRequerida = request.POST['certificacionRequerida']
            estudiosRequeridos = request.POST['estudiosRequeridos']
            idiomaRequerido = request.POST['idiomaRequerido']
            nivelRequerido = request.POST['nivelRequerido']
            nivelDeseable = request.POST['nivelDeseable']

            params = {
                'consultoresCantidad': cipher_suite.encrypt(consultoresCantidad.encode('utf-8')).decode('utf-8'),
                'certificacionRequerida': cipher_suite.encrypt(certificacionRequerida.encode('utf-8')).decode('utf-8'),
                'estudiosRequeridos': cipher_suite.encrypt(estudiosRequeridos.encode('utf-8')).decode('utf-8'),
                'idiomaRequerido': cipher_suite.encrypt(idiomaRequerido.encode('utf-8')).decode('utf-8'),
                'nivelRequerido': cipher_suite.encrypt(nivelRequerido.encode('utf-8')).decode('utf-8'),
                'nivelDeseable': cipher_suite.encrypt(nivelDeseable.encode('utf-8')).decode('utf-8'),
            }

            query_string = urlencode(params)
            redirect_url = reverse('project_created') + '?' + request.GET.urlencode() + '&' + query_string
            return redirect(redirect_url)


    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def project_created(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
     
        encrypted_titulo = request.GET.get('titulo').encode('utf-8')
        encrypted_categoria = request.GET.get('categoria').encode('utf-8')
        encrypted_date_start = request.GET.get('date_start').encode('utf-8')
        encrypted_date_end = request.GET.get('date_end').encode('utf-8')
        encrypted_moneda = request.GET.get('moneda').encode('utf-8')
        encrypted_descripcion = request.GET.get('descripcion').encode('utf-8')
        encrypted_funciones = request.GET.get('funciones').encode('utf-8')

        decrypted_titulo = cipher_suite.decrypt(encrypted_titulo).decode('utf-8')
        decrypted_categoria = cipher_suite.decrypt(encrypted_categoria).decode('utf-8')
        decrypted_date_start = cipher_suite.decrypt(encrypted_date_start).decode('utf-8')
        decrypted_date_end = cipher_suite.decrypt(encrypted_date_end).decode('utf-8')
        decrypted_moneda = cipher_suite.decrypt(encrypted_moneda).decode('utf-8')
        decrypted_descripcion = cipher_suite.decrypt(encrypted_descripcion).decode('utf-8')
        decrypted_funciones = cipher_suite.decrypt(encrypted_funciones).decode('utf-8')
        # print(decrypted_titulo)

        encrypted_presupuesto = request.GET.get('presupuesto').encode('utf-8')
        encrypted_modulo = request.GET.get('modulo').encode('utf-8')
        encrypted_submodulo = request.GET.get('submodulo').encode('utf-8')
        encrypted_experienciaRequerida = request.GET.get('experienciaRequerida').encode('utf-8')
        encrypted_experienciaDesesada = request.GET.get('experienciaDesesada').encode('utf-8')

        decrypted_presupuesto = cipher_suite.decrypt(encrypted_presupuesto).decode('utf-8')
        decrypted_modulo = cipher_suite.decrypt(encrypted_modulo).decode('utf-8')
        decrypted_submodulo = cipher_suite.decrypt(encrypted_submodulo).decode('utf-8')
        decrypted_experienciaRequerida = cipher_suite.decrypt(encrypted_experienciaRequerida).decode('utf-8')
        decrypted_experienciaDesesada = cipher_suite.decrypt(encrypted_experienciaDesesada).decode('utf-8')


        encrypted_consultoresCantidad = request.GET.get('consultoresCantidad').encode('utf-8')
        encrypted_certificacionRequerida = request.GET.get('certificacionRequerida').encode('utf-8')
        encrypted_estudiosRequeridos = request.GET.get('estudiosRequeridos').encode('utf-8')
        encrypted_idiomaRequerido = request.GET.get('idiomaRequerido').encode('utf-8')
        encrypted_nivelRequerido = request.GET.get('nivelRequerido').encode('utf-8')
        encrypted_nivelDeseable = request.GET.get('nivelDeseable').encode('utf-8')

        decrypted_consultoresCantidad = cipher_suite.decrypt(encrypted_consultoresCantidad).decode('utf-8')

        decrypted_certificacionRequerida = cipher_suite.decrypt(encrypted_certificacionRequerida).decode('utf-8')
        decrypted_estudiosRequeridos = cipher_suite.decrypt(encrypted_estudiosRequeridos).decode('utf-8')
        decrypted_idiomaRequerido = cipher_suite.decrypt(encrypted_idiomaRequerido).decode('utf-8')
        decrypted_nivelRequerido = cipher_suite.decrypt(encrypted_nivelRequerido).decode('utf-8') # j
        decrypted_nivelDeseable = cipher_suite.decrypt(encrypted_nivelDeseable).decode('utf-8') # k


        categoria = Categorias.objects.get(pk=int(decrypted_categoria))
        moneda = TipoMoneda.objects.get(pk=int(decrypted_moneda))
        modulo = Modulos.objects.get(pk=int(decrypted_modulo))
        submodulo = Submodulos.objects.get(pk=int(decrypted_submodulo))
        experienciaRequerida = NivelesConocimiento.objects.get(pk=int(decrypted_experienciaRequerida))
        experienciaDeseada = NivelesConocimiento.objects.get(pk=int(decrypted_experienciaDesesada))
        idioma = Idiomas.objects.get(pk=int(decrypted_idiomaRequerido))


        proyectos = Proyectos(proyecto_nombre=decrypted_titulo, fecha_inicio=decrypted_date_start, fecha_fin=decrypted_date_end, num_consultores=decrypted_consultoresCantidad, presupuesto_base=decrypted_presupuesto, status='Staffing',  description=decrypted_descripcion, fun_laborales=decrypted_funciones, id_categoria=categoria, id_tipo_moneda=moneda, id_experiencia_deseable=experienciaDeseada, id_experiencia_requerida=experienciaRequerida, id_modulo=modulo, id_submodulo=submodulo, certificacion=decrypted_certificacionRequerida, estudiosRequeridos=decrypted_estudiosRequeridos, tipo='Completo')
        proyectos.save()

        # Calcula la diferencia entre las fechas
        fecha_inicio = datetime.strptime(decrypted_date_start, "%Y-%m-%d")
        fecha_fin = datetime.strptime(decrypted_date_end, "%Y-%m-%d")

        # Calcula la diferencia entre las fechas
        diferencia2 = fecha_fin - fecha_inicio

        # Obtén la diferencia en años, meses y días
        dias = diferencia2.days
        meses = dias // 30  # Estimación aproximada de meses
        anios = dias // 365  # Estimación aproximada de años
        resultadoTiempo = "1 Día"

        # Genera el resultado deseado
        if dias <= 0:
            resultadoTiempo = "1 Día"
        elif dias == 1:
            resultadoTiempo = "1 día"
        elif dias <= 31:
            resultadoTiempo = f"{dias} días"
        elif dias <= 365:
            if meses == 1:
                resultadoTiempo = "1 mes"
            else:
                resultadoTiempo = f"{meses} meses"
        else:
            resultadoTiempo = "Más de 1 año"

        proyectos.duracion = resultadoTiempo
        proyectos.save()


        empresaProyecto = EmpresaProyecto(id_proyecto=proyectos, id_empresa=empresa)
        empresaProyecto.save()
        proyectos.id_empresa_proyecto = empresaProyecto
        proyectos.save()

        idiomasRequeridos = RequerimientosIdiomasProyecto(id_proyecto=proyectos, id_empresa=empresa, id_idioma=idioma, nivelRequerido=decrypted_nivelRequerido, nivelDeseado=decrypted_nivelDeseable)
        idiomasRequeridos.save()

        requerimientosModulosProyecto = []
        for i in range(0, len(request.GET)):
            requerimiento_encrypted = request.GET.get(f'requerimiento{i}')
            if requerimiento_encrypted:
                requerimiento_str = cipher_suite.decrypt(requerimiento_encrypted)
                requerimiento = pickle.loads(requerimiento_str)
                requerimiento[0].id_proyecto = proyectos
                if isinstance(requerimiento[0], RequerimientosModulosProyecto):
                    try:
                        requerimiento[0].save()
                        print("Guardado exitosamente")
                    except Exception as e:
                        print("Error al guardar:", str(e))
                else:
                    pass
                requerimientosModulosProyecto.append(requerimiento[0])
            else:
                pass


        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]

        return render(request, 'project_created.html',{
            'indice': 'Proyectos',
            'empresa':empresa,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def details_project(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
        prj = request.GET.get('prj')
        monedaCobro = list(TipoMoneda.objects.values())
        categorias = list(Categorias.objects.values())

        if prj:
            empresaProyectos = EmpresaProyecto.objects.filter(id_proyecto=int(prj), id_empresa=empresa)
            if empresaProyectos.exists():           
                proyectos = Proyectos.objects.get(pk=int(prj))

                # Obtiene la fecha actual
                fecha_actual = datetime.now().date()

                # Fecha de publicación del staffing (ejemplo)
                fecha_publicacion = proyectos.fecha_publicacion

                # Calcula la diferencia de días
                diferencia = fecha_actual - fecha_publicacion
                dias_pasados = diferencia.days

                if dias_pasados > 30:
                    diasStaffing = 'Hace mas de un mes'
                elif dias_pasados == 0:
                    diasStaffing = 'Hoy'
                else:
                    diasStaffing = 'Hace ' + str(dias_pasados) + ' días'

                fecha_inicio = proyectos.fecha_inicio
                fecha_fin = proyectos.fecha_fin

                # Calcula la diferencia entre las fechas
                diferencia2 = fecha_fin - fecha_inicio

                # Obtén la diferencia en años, meses y días
                dias = diferencia2.days
                meses = dias // 30  # Estimación aproximada de meses
                anios = dias // 365  # Estimación aproximada de años
                resultadoTiempo = "1 Dia"
                # Genera el resultado deseado
                if dias <= 0:
                    resultadoTiempo = "1 Dia"
                elif dias == 1:
                    resultadoTiempo = "1 día"
                elif dias <= 31:
                    resultadoTiempo = f"{dias} días"
                elif dias <= 365:
                    if meses == 1:
                        resultadoTiempo = "1 mes"
                    else:
                        Tiempo = f"{meses} meses"
                else:
                    resultadoTiempo = f"Más de 1 año"

                listaModulos = list(Modulos.objects.values())
                listaSubodulos = list(Submodulos.objects.values())
                listaNivelesConocimiento = list(NivelesConocimiento.objects.values())
                listaIdiomas = list(Idiomas.objects.values())
                modulosRequeridos = RequerimientosModulosProyecto.objects.filter(id_empresa=empresa, id_proyecto=proyectos)
                # print(modulosRequeridos)

                idiomasRequeridos = RequerimientosIdiomasProyecto.objects.filter(id_empresa=empresa, id_proyecto=proyectos)

                postulacionesProyecto = PostulacionesProyecto.objects.filter(id_empresa=empresa, id_proyecto=proyectos)
                
                postulados = []
                cPostulados = 0
                if postulacionesProyecto:
                    for postulaciones in postulacionesProyecto:
                        id = postulaciones.id_consultor
                        if postulaciones.id_consultor.id_persona.sexo == 'M':
                            sexo = 'Hombre'
                        else:
                            sexo = 'Mujer'
                        edad = calcular_edad(str(postulaciones.id_consultor.id_persona.fecha_nacimiento))

                        modulos = ConocimientosConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                        experiencia = ""
                        if modulos:
                            for modulo in modulos:
                                experiencia += modulo.id_modulo.nombre + " "
                        else:
                            experiencia = "Sin experiencia"
                        
                        # Verificar si existen los atributos necesarios antes de asignarlos
                        if hasattr(postulaciones.id_consultor, 'tarifa_hora'):
                            pago = postulaciones.id_consultor.tarifa_hora
                        else:
                            pago = None

                        if hasattr(postulaciones.id_consultor.id_tipo_moneda, 'tipo'):
                            texto = postulaciones.id_consultor.id_tipo_moneda.tipo
                            resultado = re.search(r'\((.*?)\)', texto)
                            moneda = resultado.group(1)
                        else:
                            moneda = None
                        
                        if hasattr(postulaciones.id_consultor.id_persona, 'disponible'):
                            disponibilidad = postulaciones.id_consultor.id_persona.disponible
                            if disponibilidad:
                                disponible = 'Disponible'
                            else:
                                disponible = 'No disponible'
                        else:
                            disponibilidad = None


                        projects = ProyectoConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                        if projects.exists():  # Verificar si hay proyectos
                            cantidad_proyectos = projects.count()
                            
                            puntuacion = 0

                            for proyecto in projects:
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

                        postulados.append([sexo, edad, experiencia, pago, moneda, disponible, id, cantidad_proyectos, puntuacionConsultor])

                    cPostulados = len(postulados)


                postulacionesProyectoGnosis = PostulacionesProyectoGnosis.objects.filter(id_empresa=empresa, id_proyecto=proyectos)
                
                postuladosGnosis = []
                cPostuladosGnosis = 0
                if postulacionesProyectoGnosis:
                    for postulaciones in postulacionesProyectoGnosis:
                        id = postulaciones.id_consultor
                        if postulaciones.id_consultor.id_persona.sexo == 'M':
                            sexo = 'Hombre'
                        else:
                            sexo = 'Mujer'
                        edad = calcular_edad(str(postulaciones.id_consultor.id_persona.fecha_nacimiento))

                        modulos = ConocimientosConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                        experiencia = ""
                        if modulos:
                            for modulo in modulos:
                                experiencia += modulo.id_modulo.nombre + " "
                        else:
                            experiencia = "Sin experiencia"
                        
                        # Verificar si existen los atributos necesarios antes de asignarlos
                        if hasattr(postulaciones.id_consultor, 'tarifa_hora'):
                            pago = postulaciones.id_consultor.tarifa_hora
                        else:
                            pago = None

                        if hasattr(postulaciones.id_consultor.id_tipo_moneda, 'tipo'):
                            texto = postulaciones.id_consultor.id_tipo_moneda.tipo
                            resultado = re.search(r'\((.*?)\)', texto)
                            moneda = resultado.group(1)
                        else:
                            moneda = None
                        
                        if hasattr(postulaciones.id_consultor.id_persona, 'disponible'):
                            disponibilidad = postulaciones.id_consultor.id_persona.disponible
                            if disponibilidad:
                                disponible = 'Disponible'
                            else:
                                disponible = 'No disponible'
                        else:
                            disponibilidad = None


                        projects = ProyectoConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                        if projects.exists():  # Verificar si hay proyectos
                            cantidad_proyectos = projects.count()
                            
                            puntuacion = 0

                            for proyecto in projects:
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

                        postuladosGnosis.append([sexo, edad, experiencia, pago, moneda, disponible, id, puntuacionConsultor, cantidad_proyectos])

                    cPostuladosGnosis = len(postulados)



                entrevistasConsultoresProyecto = EntrevistasConsultoresProyecto.objects.filter(id_empresa=empresa, id_proyecto=proyectos)
                cEntrevitas = 0
                entrevistas = []
                entrevistasAgendadas = []
                if entrevistasConsultoresProyecto:
                    for entrevistasConsultor in entrevistasConsultoresProyecto:
                        id = entrevistasConsultor.id
                        consultor = entrevistasConsultor.id_consultor.id
                        if entrevistasConsultor.id_consultor.id_persona.sexo == 'M':
                            sexo = 'Hombre'
                        else:
                            sexo = 'Mujer'
                        edad = calcular_edad(str(entrevistasConsultor.id_consultor.id_persona.fecha_nacimiento))

                        modulos = ConocimientosConsultor.objects.filter(id_consultor=entrevistasConsultor.id_consultor)
                        experiencia = ""
                        if modulos:
                            for modulo in modulos:
                                experiencia += modulo.id_modulo.nombre + " "
                        else:
                            experiencia = "Sin experiencia"
                        
                        # Verificar si existen los atributos necesarios antes de asignarlos
                        if hasattr(entrevistasConsultor.id_consultor, 'tarifa_hora'):
                            pago = entrevistasConsultor.id_consultor.tarifa_hora
                        else:
                            pago = None

                        if hasattr(entrevistasConsultor.id_consultor.id_tipo_moneda, 'tipo'):
                            texto = entrevistasConsultor.id_consultor.id_tipo_moneda.tipo
                            resultado = re.search(r'\((.*?)\)', texto)
                            moneda = resultado.group(1)
                        else:
                            moneda = None
                        
                        if hasattr(entrevistasConsultor.id_consultor.id_persona, 'disponible'):
                            disponibilidad = entrevistasConsultor.id_consultor.id_persona.disponible
                            if disponibilidad:
                                disponible = 'Disponible'
                            else:
                                disponible = 'No disponible'
                        else:
                            disponibilidad = None

                        
                        if hasattr(entrevistasConsultor.id_consultor.id_persona, 'ciudad'):
                            ciudad = entrevistasConsultor.id_consultor.id_persona.ciudad
                        else:
                            ciudad = None

                        if hasattr(entrevistasConsultor.id_consultor.id_persona, 'municipio'):
                            municipio = entrevistasConsultor.id_consultor.id_persona.municipio
                        else:
                            municipio = None

                        if hasattr(entrevistasConsultor.id_consultor.id_persona, 'colonia'):
                            colonia = entrevistasConsultor.id_consultor.id_persona.colonia
                        else:
                            colonia = None

                        if not ciudad:
                            ubicacion = str(municipio) + ' '+str(colonia)
                        else:
                            ubicacion = str(ciudad) + ' ' +str(colonia)


                        projects = ProyectoConsultor.objects.filter(id_consultor=entrevistasConsultor.id_consultor)
                        if projects.exists():  # Verificar si hay proyectos
                            cantidad_proyectos = projects.count()
                            
                            puntuacion = 0

                            for proyecto in projects:
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


                        if entrevistasConsultor.fecha and entrevistasConsultor.hora:
                            entrevistasAgendadas.append([sexo, edad, experiencia, pago, moneda, disponible, id,ubicacion, entrevistasConsultor.fecha, entrevistasConsultor.hora, entrevistasConsultor.estatus, consultor, puntuacionConsultor, cantidad_proyectos])
                        else:
                            entrevistas.append([sexo, edad, experiencia, pago, moneda, disponible, id,ubicacion, puntuacionConsultor, cantidad_proyectos])
                    
                    cEntrevitas = len(entrevistas)


                consultoresProyecto = ProyectoConsultor.objects.filter(id_proyecto=proyectos, participacion=True)
                
                proyectosConsultores = []
                cProyectos = 0
                if consultoresProyecto:
                    for consulProyecto in consultoresProyecto:
                        id = consulProyecto.id_consultor
                        status = consulProyecto.status
                        # print(status)
                        if consulProyecto.id_consultor.id_persona.sexo == 'M':
                            sexo = 'Hombre'
                        else:
                            sexo = 'Mujer'

                        name = str(consulProyecto.id_consultor.id_persona.nombre) + ' ' + str(consulProyecto.id_consultor.id_persona.ape_pat) + ' ' + str(consulProyecto.id_consultor.id_persona.ape_mat)
                        edad = calcular_edad(str(consulProyecto.id_consultor.id_persona.fecha_nacimiento))

                        modulos = ConocimientosConsultor.objects.filter(id_consultor=consulProyecto.id_consultor)
                        experiencia = ""
                        if modulos:
                            for modulo in modulos:
                                experiencia += modulo.id_modulo.nombre + " "
                        else:
                            experiencia = "Sin experiencia"
                        
                        dias = consulProyecto.dias_laborales

                        inicio = consulProyecto.horario_hora_inicio.strftime("%H:%M")
                        final = consulProyecto.horario_hora_final.strftime("%H:%M")

                        horario = f"{inicio} - {final}"
                        
                        proyectosConsultores.append([sexo, edad, experiencia, id, dias, horario, status, name])

                    cProyectos = len(proyectosConsultores)
                


                notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
                # // CANT. NOTIFICATIONS PENDING
                pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
                # // ONLY 4 PENDING 
                pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]


                return render(request, 'details_project.html',{
                    'indice': 'Proyectos',
                    'empresa':empresa,
                    'listaModulos':listaModulos,
                    'listaSubodulos':listaSubodulos,
                    'listaNivelesConocimiento':listaNivelesConocimiento,
                    'listaIdiomas':listaIdiomas,
                    'proyectos':proyectos,
                    'diasStaffing':diasStaffing,
                    'monedaCobro': monedaCobro,
                    'categorias':categorias,
                    'modulosRequeridos':modulosRequeridos,
                    'idiomasRequeridos':idiomasRequeridos,
                    'postulados':postulados,
                    'postuladosGnosis':postuladosGnosis,
                    'cPostulados':cPostulados,
                    'entrevistas':entrevistas,
                    'cEntrevitas':cEntrevitas,
                    'entrevistasAgendadas':entrevistasAgendadas,
                    'proyectosConsultores':proyectosConsultores,
                    'notifications':notification,
                    'pending':pending,
                    'pending_total':pending_total,
                })

            else:
                return redirect('my_projectsCreateds')
        else:
                return redirect('my_projectsCreateds')
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def mapa(request, id:int):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        consultor = Consultores.objects.get(pk=int(id))
        if consultor.id_persona.ciudad == '':
            direccion = str(consultor.id_persona.pais) + ', ' + str(consultor.id_persona.estado) + ', ' + str(consultor.id_persona.municipio)
        else:
            direccion = str(consultor.id_persona.pais) + ', ' + str(consultor.id_persona.estado) + ', ' + str(consultor.id_persona.ciudad)
        
        nivel = ConocimientosConsultor.objects.filter(id_consultor=consultor)
        edad = calcular_edad(str(consultor.id_persona.fecha_nacimiento))
        texto = consultor.id_tipo_moneda.tipo
        patron = r"\((.*?)\)"  # Patrón para buscar el texto entre paréntesis
        moneda = re.search(patron, texto).group(1) if re.search(patron, texto) else "" 
        
        saber = Usuarios.objects.get(id_persona=consultor.id_persona)
        
        if saber.image == '':
            if consultor.id_persona.sexo == 'M':
                image = '/static/images/profile/default.jpg'
                default = True
            else:
                image = '/static/images/profile/defaultF.png'
                default = True
        else:
            image = saber.image
            default = False

        
        projects = ProyectoConsultor.objects.filter(id_consultor=consultor)
        if projects.exists():  # Verificar si hay proyectos
            cantidad_proyectos = projects.count()
                            
            puntuacion = 0

            for proyecto in projects:
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

        try:
            nota = NotasGnosisConsultor.objects.get(id_consultor_id=consultor.id)
        except NotasGnosisConsultor.DoesNotExist as error:
            nota = 'Sin comentarios'

        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]


        return render(request, 'mapa_consultores.html',{
            'indice': 'Proyectos',
            'empresa':empresa,
            'consultor':consultor,
            'direccion':direccion,
            'edad':edad,
            'moneda':moneda,
            'nivel':nivel,
            'image':image,
            'puntuacionConsultor':puntuacionConsultor,
            'default':default,
            'comentarios':nota,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def addNewProject(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        titulo = request.POST['titulo']
        categoria = request.POST['categoria']
        date_start = request.POST['date_start']
        date_end = request.POST['date-end']
        moneda = request.POST['moneda']
        descripcion = request.POST['descripcion']
        funciones = request.POST['funciones']


        params = {
            'titulo': cipher_suite.encrypt(request.POST['titulo'].encode('utf-8')).decode('utf-8'),
            'categoria': cipher_suite.encrypt(request.POST['categoria'].encode('utf-8')).decode('utf-8'),
            'date_start': cipher_suite.encrypt(request.POST['date_start'].encode('utf-8')).decode('utf-8'),
            'date_end': cipher_suite.encrypt(request.POST['date-end'].encode('utf-8')).decode('utf-8'),
            'moneda': cipher_suite.encrypt(request.POST['moneda'].encode('utf-8')).decode('utf-8'),
            'descripcion': cipher_suite.encrypt(request.POST['descripcion'].encode('utf-8')).decode('utf-8'),
            'funciones': cipher_suite.encrypt(request.POST['funciones'].encode('utf-8')).decode('utf-8'),
        }
        query_string = urlencode(params)
        url = reverse('requirements_project') + '?' + query_string

        return HttpResponseRedirect(url)

    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def updateDetails_project(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        titulo = request.POST['titulo']
        categoria = request.POST['categoria']
        date_start = request.POST['date_start']
        date_end = request.POST['date-end2']
        moneda = request.POST['moneda']
        descripcion = request.POST['descripcion']
        funciones = request.POST['funciones']
        id = request.POST['saber']
        estado = request.POST['estado']
        consultores = request.POST['consultores']
        tipo = request.POST['tipo']

        monedaObject = TipoMoneda.objects.get(pk=int(moneda)) 
        categoriaObject = Categorias.objects.get(pk=int(categoria)) 

        proyecto = Proyectos.objects.get(pk=int(id))
        proyecto.proyecto_nombre = titulo
        proyecto.fecha_inicio = date_start
        proyecto.fecha_fin = date_end
        proyecto.id_tipo_moneda = monedaObject
        proyecto.id_categoria = categoriaObject
        proyecto.description = descripcion
        proyecto.fun_laborales = funciones
        proyecto.status = estado
        proyecto.num_consultores = consultores
        proyecto.tipo = tipo

        proyecto.save()

        # Calcula la diferencia entre las fechas
        fecha_inicio = datetime.strptime(date_start, "%Y-%m-%d")
        fecha_fin = datetime.strptime(date_end, "%Y-%m-%d")

        # Calcula la diferencia entre las fechas
        diferencia2 = fecha_fin - fecha_inicio

        # Obtén la diferencia en años, meses y días
        dias = diferencia2.days
        meses = dias // 30  # Estimación aproximada de meses
        anios = dias // 365  # Estimación aproximada de años
        resultadoTiempo = "1 Día"

        # Genera el resultado deseado
        if dias <= 0:
            resultadoTiempo = "1 Día"
        elif dias == 1:
            resultadoTiempo = "1 día"
        elif dias <= 31:
            resultadoTiempo = f"{dias} días"
        elif dias <= 365:
            if meses == 1:
                resultadoTiempo = "1 mes"
            else:
                resultadoTiempo = f"{meses} meses"
        else:
            resultadoTiempo = "Más de 1 año"

        proyecto.duracion = resultadoTiempo
        proyecto.save()

        parametros = {
            'prj': proyecto.id,
        }
        url = reverse('details_project') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)
        
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')





@login_required
def updateRequerimientos_project(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        saber = request.POST['saber']
        modulo = request.POST['modulo']
        submodulo = request.POST['submodulo']
        nivelRequerido = request.POST['nivelRequerido']
        nivelDeseado = request.POST['nivelDeseado']

        moduloR = Modulos.objects.get(pk=int(modulo))
        submoduloR = Submodulos.objects.get(pk=int(submodulo))
        nivelR = NivelesConocimiento.objects.get(pk=int(nivelRequerido))
        nivelD = NivelesConocimiento.objects.get(pk=int(nivelDeseado))

        requerimiento = RequerimientosModulosProyecto.objects.get(id=int(saber))
        if requerimiento is not None:
            requerimiento.id_modulo = moduloR
            requerimiento.id_submodulo = submoduloR
            requerimiento.id_experiencia_requerida = nivelR
            requerimiento.id_experiencia_deseable = nivelD
            requerimiento.save()

            parametros = {
                'prj': requerimiento.id_proyecto.id,
            }
            url = reverse('details_project') + '?' + urlencode(parametros)
        else:
            parametros = {
                'sts': 'error',
            }
            url = reverse('my_projectsCreateds') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)
        
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def deleteRequerimientos_project(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
        requerimiento = RequerimientosModulosProyecto.objects.get(id=int(id))
        proyecto = requerimiento.id_proyecto.id
        if requerimiento is not None:
            requerimiento.delete()
            parametros = {
                'prj': proyecto,
            }
            url = reverse('details_project') + '?' + urlencode(parametros)
        else:
            parametros = {
                'sts': 'error',
            }
            url = reverse('my_projectsCreateds') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)
        
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def addRequerimientos_project(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        data = json.loads(request.body)
        if data:
            for fila in data:
                if fila[0] == '' or fila[1] == '' or fila[2] == '':
                    pass
                else:
                    requerimientos = RequerimientosModulosProyecto(
                        id_empresa=empresa,
                        id_proyecto=Proyectos.objects.get(pk=int(id)),
                        id_modulo=Modulos.objects.get(nombre=fila[0]),
                        id_submodulo=Submodulos.objects.get(nombre=fila[1]),
                        id_experiencia_requerida=NivelesConocimiento.objects.get(nombre=fila[2]),
                        id_experiencia_deseable=NivelesConocimiento.objects.get(nombre=fila[3])
                    )
                    requerimientos.save()

            return JsonResponse({'message': 'El objeto se ha agregado correctamente.'}, status=200)
        else:
            return JsonResponse({'message': 'No hay nada que agregar.'}, status=200)
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('my_projectsCreateds')




@login_required
def updateDetailsCertificaciones_project(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        certificado = request.POST['certificado']
        estudios = request.POST['estudios']
        id = request.POST['saber']
 
        proyecto = Proyectos.objects.get(pk=int(id))
        proyecto.certificacion = certificado
        proyecto.estudiosRequeridos = estudios
        proyecto.save()

        parametros = {
            'prj': proyecto.id,
        }
        url = reverse('details_project') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)
        
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


def updateRequerimientosIdioma_project(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        saber = request.POST['saber']
        nivelIdiomaRequerido = request.POST['nivelIdiomaRequerido']
        nivelIdiomaDeseado = request.POST['nivelIdiomaDeseado']
        idiomaEnviado = request.POST['idioma']
        idioma = Idiomas.objects.get(pk=int(idiomaEnviado))


        requerimiento = RequerimientosIdiomasProyecto.objects.get(id=int(saber))
        if requerimiento is not None:
            requerimiento.id_idioma = idioma
            requerimiento.nivelRequerido = nivelIdiomaRequerido
            requerimiento.nivelDeseado = nivelIdiomaDeseado
            requerimiento.save()

            parametros = {
                'prj': requerimiento.id_proyecto.id,
            }
            url = reverse('details_project') + '?' + urlencode(parametros)
        else:
            parametros = {
                'sts': 'error',
            }
            url = reverse('my_projectsCreateds') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)
        
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def addRequerimientos_idiomas_project(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
        print("Hipoola")
        data = json.loads(request.body)
        print(data)
        if data:
            for fila in data:
                if fila[0] == '' or fila[1] == '' or fila[2] == '':
                    pass
                else:
                    requerimientos = RequerimientosIdiomasProyecto(
                        id_proyecto=Proyectos.objects.get(pk=int(id)),
                        id_empresa=empresa,
                        id_idioma=Idiomas.objects.filter(Q(nombre__exact=fila[0])).first(),
                        nivelRequerido=fila[1],
                        nivelDeseado=fila[2],
                    )
                    requerimientos.save()

            return JsonResponse({'message': 'El objeto se ha agregado correctamente.'}, status=200)
        else:
            return JsonResponse({'message': 'No hay nada que agregar.'}, status=200)
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('my_projectsCreateds')



@login_required
def deleteRequerimientosIdiomas_project(request, id=None):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
        requerimiento = RequerimientosIdiomasProyecto.objects.get(id=int(id))
        proyecto = requerimiento.id_proyecto.id
        if requerimiento is not None:
            requerimiento.delete()
            parametros = {
                'prj': proyecto,
            }
            url = reverse('details_project') + '?' + urlencode(parametros)
        else:
            parametros = {
                'sts': 'error',
            }
            url = reverse('my_projectsCreateds') + '?' + urlencode(parametros)

        return HttpResponseRedirect(url)
        
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


def calcular_edad(fecha_nacimiento):
    fecha_actual = date.today()
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d %H:%M:%S%z").date()
    edad = fecha_actual.year - fecha_nacimiento.year

    # Comprobar si aún no ha llegado el cumpleaños de este año
    if fecha_actual.month < fecha_nacimiento.month or (fecha_actual.month == fecha_nacimiento.month and fecha_actual.day < fecha_nacimiento.day):
        edad -= 1

    return edad



@login_required
def deletePostulacionProyecto(request):
    try:
        data = json.loads(request.body)
        id = data['id']
        # print(id)
        proyecto = data['proyecto']
        informationConsultorUser = Consultores.objects.get(pk=id)
        proyecto = Proyectos.objects.get(pk=int(proyecto))
        empresa = proyecto.id_empresa_proyecto.id_empresa
        postulacion = PostulacionesProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)

        if postulacion:
            postulacion.delete()

            message='Tu postulacion al proyecto ' + str(proyecto.proyecto_nombre) + ' se ha eliminado'
            newNotificacion = NotificationConsultor(name='Gnosis SC', email='gnosis@gmail.com', subject='Solicitud Eliminada', message=message, status='Pending', id_consultor_destinatary_id=informationConsultorUser.id)
            newNotificacion.save()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)



@login_required
def solicitarEntrevista(request):
    try:
        data = json.loads(request.body)
        id = data['id']
        # print(id)
        proyecto = data['proyecto']

        informationConsultorUser = Consultores.objects.get(pk=id)
        proyecto = Proyectos.objects.get(pk=int(proyecto))

        empresa = proyecto.id_empresa_proyecto.id_empresa
        postulacion = PostulacionesProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)

        if postulacion:
            empresaProyecto = EmpresaProyecto.objects.get(id_proyecto=proyecto, id_empresa=empresa)
            
            entrevistasConsultoresProyecto = EntrevistasConsultoresProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor= informationConsultorUser)
            # enviar email de confirmacion
            ubicacion = str(empresa.ciudad) + ', ' + str(empresa.estado)
            
            if not entrevistasConsultoresProyecto:
                entrevistaConsultoresProyecto = EntrevistasConsultoresProyecto(id_proyecto=proyecto, id_empresa=empresa, id_consultor= informationConsultorUser)
                entrevistaConsultoresProyecto.save()
                
                postulacion.delete()


        postulacion = PostulacionesProyectoGnosis.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)

        if postulacion:
            empresaProyecto = EmpresaProyecto.objects.get(id_proyecto=proyecto, id_empresa=empresa)
                
            entrevistasConsultoresProyecto = EntrevistasConsultoresProyecto.objects.filter(id_proyecto=proyecto, id_empresa=empresa, id_consultor= informationConsultorUser)
                # enviar email de confirmacion
            ubicacion = str(empresa.ciudad) + ', ' + str(empresa.estado)
                
            if not entrevistasConsultoresProyecto:
                entrevistaConsultoresProyecto = EntrevistasConsultoresProyecto(id_proyecto=proyecto, id_empresa=empresa, id_consultor= informationConsultorUser)
                entrevistaConsultoresProyecto.save()
                    
                postulacion.delete()
                
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)


@login_required
def entrevistaAgendada(request):
    try:
        fecha = request.POST['date-end']
        horas = request.POST['horas']
        minutos = request.POST['minutes']
        id = request.POST['entrevista']
        proyecto = request.POST['proyecto']
        

        cadena = horas +':'+minutos
        hora_str, minutos_str = cadena.split(':')
        hora_obj = datetime.strptime(hora_str + ':' + minutos_str, '%H:%M').time() 

        entrevistasConsultoresProyecto = EntrevistasConsultoresProyecto.objects.get(pk=(id))
        entrevistasConsultoresProyecto.fecha = fecha
        entrevistasConsultoresProyecto.hora = hora_obj
        entrevistasConsultoresProyecto.save()
        usuario = Usuarios.objects.get(id_persona=entrevistasConsultoresProyecto.id_consultor.id_persona)
        # sendemail(str(usuario.correo), str(entrevistasConsultoresProyecto.id_consultor.id_persona.nombre), proyecto.proyecto_nombre, ubicacion, proyecto.tipo)
    
        message = 'La empresa a la cual te has postulado ha solicitado una entrevista el dia ' +str(entrevistasConsultoresProyecto.fecha) + ', a las ' + str(entrevistasConsultoresProyecto.hora) + '. Si estas disponible y te interesaría esta oportunidad da click en vinculo para confirmar tu entrevista.'

        data = 'id_entrevista:'+str(id)

        notificacion = NotificationConsultor(name='Gnosis SC', email='gnosis@gmail.com', subject='¡¡Excelentes Noticias!!', message=message, status='Pending', id_consultor_destinatary=entrevistasConsultoresProyecto.id_consultor, confirm=True, data=data)
        notificacion.save()

        
        url = reverse('details_project') + '?prj='+proyecto
        return redirect(url)

    except Exception as error:
        print(f"Error: {str(error)}")
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')


def sendemail(email, name, puesto, ubicacion, tipo):
    to = email
    name = name
    # se envian los datos al email template
    html_content = render_to_string(
        "emails/email_interview.html", {"name": name, "puesto":puesto, "ubicacion":ubicacion, "tipo":tipo}
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
    print("envieee")
    email.send()
    return "Correo enviado"




@login_required
def validarEntrevistaGnosis(request):
    try:
        data = json.loads(request.body)
        id = data['consultor']
        print(id)
        proyecto = data['proyecto']

        informationConsultorUser = Consultores.objects.get(pk=id)
        proyecto = Proyectos.objects.get(pk=int(proyecto))
        empresa = proyecto.id_empresa_proyecto.id_empresa

        consulta = EntrevistasConsultoresProyecto.objects.get(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)
        if consulta.estatus == 'Confirmada':
            data = 'id_consultor:'+str(id)+',id_proyecto:'+str(proyecto.id)
            message = 'Necesito que validen al consultor ' + str(informationConsultorUser.id_persona.nombre) + ' ' + str(informationConsultorUser.id_persona.ape_pat) + ' para mi proyecto: ' + str(proyecto.proyecto_nombre)

            notificationAdministrador = NotificationAdministrador(name=empresa.empresa, email=empresa.id_usuario.correo, subject='Validar consultor', message=message, status='Pending', id_persona_destinatary_id=1, action=True, data=data)
            notificationAdministrador.save()

        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)


@login_required
def allMapa(request, id:int):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        postulacionesProyecto = PostulacionesProyecto.objects.filter(id_proyecto_id=int(id))
        postulados = []
        cPostulados = 0
        if postulacionesProyecto:
            for postulaciones in postulacionesProyecto:
                id = postulaciones.id_consultor.id
                
                if postulaciones.id_consultor.id_persona.ciudad == '':
                    direccion = str(postulaciones.id_consultor.id_persona.pais) +', '+str(postulaciones.id_consultor.id_persona.estado) + ', '+str(postulaciones.id_consultor.id_persona.municipio)
                else:
                    direccion = str(postulaciones.id_consultor.id_persona.pais) +', '+str(postulaciones.id_consultor.id_persona.estado) + ', '+str(postulaciones.id_consultor.id_persona.ciudad)


                if postulaciones.id_consultor.id_persona.sexo == 'M':
                    sexo = 'Hombre'
                else:
                    sexo = 'Mujer'
                edad = calcular_edad(str(postulaciones.id_consultor.id_persona.fecha_nacimiento))

                modulos = ConocimientosConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                experiencia = ""
                if modulos:
                    titulo = str(modulos[0].id_modulo.nombre)
                    nivel = str(modulos[0].id_nivel.nombre) 
                    for modulo in modulos:
                        experiencia += modulo.id_modulo.nombre + " "
                else:
                    experiencia = "Sin experiencia"
                    titulo = ""
                    nivel = ""
                        
                # Verificar si existen los atributos necesarios antes de asignarlos
                if hasattr(postulaciones.id_consultor, 'rfc'):
                    rfc = postulaciones.id_consultor.rfc
                else:
                    rfc = None

                # Verificar si existen los atributos necesarios antes de asignarlos
                if hasattr(postulaciones.id_consultor, 'tarifa_hora'):
                    pago = postulaciones.id_consultor.tarifa_hora
                else:
                    pago = None

                if hasattr(postulaciones.id_consultor.id_tipo_moneda, 'tipo'):
                    texto = postulaciones.id_consultor.id_tipo_moneda.tipo
                    resultado = re.search(r'\((.*?)\)', texto)
                    moneda = resultado.group(1)
                else:
                    moneda = None
                        
                if hasattr(postulaciones.id_consultor.id_persona, 'disponible'):
                    disponibilidad = postulaciones.id_consultor.id_persona.disponible
                    if disponibilidad:
                        disponible = 'Disponible'
                    else:
                        disponible = 'No disponible'
                else:
                    disponibilidad = None
                
                comentarios = 'Aun no hay comentarios'
                descripcion = 'Aun no hay descripción'

                saber = Usuarios.objects.get(id_persona=postulaciones.id_consultor.id_persona)
        
                if saber.image == '':
                    if postulaciones.id_consultor.id_persona.sexo == 'M':
                        image = '/static/images/profile/default.jpg'
                        default = True
                    else:
                        image = '/static/images/profile/defaultF.png'
                        default = True
                else:
                    image = saber.image
                    default = False


                projects = ProyectoConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                if projects.exists():  # Verificar si hay proyectos
                    cantidad_proyectos = projects.count()
                    puntuacion = 0

                    for proyecto in projects:
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

                postulados.append([sexo, edad, experiencia, pago, moneda, disponible, id, titulo, nivel, direccion, comentarios, experiencia, descripcion, rfc, image, default, puntuacionConsultor])
            
            
            cPostulados = len(postulados)

        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
        return render(request, 'mapa_alls.html',{
            'indice': 'Proyectos',
            'empresa':empresa,
            'postulacionesProyecto':postulacionesProyecto[0],
            'postulados':postulados,
            'cPostulados':cPostulados,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def nuevaEntrevista(request):
    try:
        data = json.loads(request.body)
        id = data['consultor']
        
        proyecto = data['proyecto']
        empresa = data['empresa']

        informationConsultorUser = Consultores.objects.get(pk=id)
        proyecto = Proyectos.objects.get(pk=int(proyecto))
        empresa = proyecto.id_empresa_proyecto.id_empresa

    
        entrevista = EntrevistasConsultoresProyecto(id_proyecto=proyecto, id_empresa=empresa, id_consultor=informationConsultorUser)
        entrevista.save()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)

    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)



@login_required
def eliminarEntrevista(request):
    try:
        data = json.loads(request.body)
        id = data['entrevista']
        proyecto = data['proyecto']
        empresa = data['empresa']

        entrevista = EntrevistasConsultoresProyecto.objects.get(pk=int(id))
        entrevista.delete()
        proyecto = Proyectos.objects.get(pk=int(proyecto))

        message='Tu entrevista al proyecto ' + str(proyecto.proyecto_nombre) + ' ha sido cancelada'

        newNotificacion = NotificationConsultor(name='Gnosis SC', email='gnosis@gmail.com', subject='Entrevista Cancelada ', message=message, status='Pending', id_consultor_destinatary_id=entrevista.id_consultor.id)
        newNotificacion.save()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)



@login_required
def solicitarReporteHoras(request):
    try:
        data = json.loads(request.body)
        id = data['consultor']
        proyecto = data['proyecto']
        empresa = data['empresa']

        consultor = Consultores.objects.get(pk=int(id))

        
        proyecto = Proyectos.objects.get(pk=int(proyecto))

        message='Solicitamos tu reporte de horas del proyecto ' + str(proyecto.proyecto_nombre)

        newNotificacion = NotificationConsultor(name=str(proyecto.id_empresa_proyecto.id_empresa.empresa), email=str(proyecto.id_empresa_proyecto.id_empresa.id_usuario.correo), subject='Solicitud reporte de horas', message=message, status='Pending', id_consultor_destinatary_id=consultor.id)
        
        newNotificacion.save()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)




@login_required
def solicitarContrato(request):
    try:
        data = json.loads(request.body)
        id = data['consultor']
        proyecto = data['proyecto']
        contrato = data['contrato']
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
        consultor = Consultores.objects.get(pk=int(id))  
        proyecto = Proyectos.objects.get(pk=int(proyecto))

        query = ProyectoConsultor.objects.filter(id_consultor=consultor, id_proyecto=proyecto, status='Aceptada').first()

        if query:
            data = 'id_consultor:'+str(id)+',id_proyecto:'+str(proyecto.id)
            message = 'Necesito que generen el contrato ' + str(contrato) + ' para el consultor ' + str(consultor.id_persona.nombre) + ' ' + str(consultor.id_persona.ape_pat) + ' para mi proyecto: ' + str(proyecto.proyecto_nombre)

            notificationAdministrador = NotificationAdministrador(name=empresa.empresa, email=empresa.id_usuario.correo, subject='Necesito una contratación', message=message, status='Pending', id_persona_destinatary_id=1, action=True, data=data, enlace="contratoConsultor")
            notificationAdministrador.save()
        
        return HttpResponse(status=200)
    except Consultores.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Usuarios.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Personas.DoesNotExist as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)
    except Exception as error:
        print(f"Error: {str(error)}")
        return HttpResponse(status=500)




@login_required
def solicitarContratoRenovacion(request):
    try:
        consultor = request.POST['consultor']
        proyecto = request.POST['proyecto']
        razon = request.POST['razon']
        comentarios = request.POST['comentarios']
        
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)
        consultor = Consultores.objects.get(pk=int(consultor))  
        proyecto = Proyectos.objects.get(pk=int(proyecto))


        query = ProyectoConsultor.objects.filter(id_consultor=consultor, id_proyecto=proyecto, status='Aceptada').first()

        if query:
            
            data = 'id_consultor:'+str(consultor.id)+',id_proyecto:'+str(proyecto.id)
            
            message = 'Necesito una renovacion de contrato de contrato base para el consultor ' + str(consultor.id_persona.nombre) + ' ' + str(consultor.id_persona.ape_pat) + ' para mi proyecto:  \n' + str(proyecto.proyecto_nombre) + ' por la siguiente razon: \n' + str(razon) + ', y mis comentarios son: \n' + str(comentarios)

            notificationAdministrador = NotificationAdministrador(name=empresa.empresa, email=empresa.id_usuario.correo, subject='Necesito una renovacion de contrato', message=message, status='Pending', id_persona_destinatary_id=1, action=True, data=data, enlace="contratoConsultor")
            notificationAdministrador.save()


            messageConsultor='La empresa ' + str(empresa.empresa) + ' ha solicitado una renovacion de contrato para el proyecto ' + str(proyecto.proyecto_nombre) + ' por la siguiente razon: ' + str(razon)
            
            newNotificacion = NotificationConsultor(name='Gnosis SC', email='gnosis@gmail.com', subject='Renovacion de contrato', message=messageConsultor, status='Pending', id_consultor_destinatary_id=consultor.id)
            newNotificacion.save()



        return redirect('consultorEmpresa', id=consultor.id_persona.id, prj=proyecto.id)
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')



@login_required
def allMapaGnosis(request, id:int):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        postulacionesProyecto = PostulacionesProyectoGnosis.objects.filter(id_proyecto_id=int(id))
        postulados = []
        cPostulados = 0
        if postulacionesProyecto:
            for postulaciones in postulacionesProyecto:
                id = postulaciones.id_consultor.id
                
                if postulaciones.id_consultor.id_persona.ciudad == '':
                    direccion = str(postulaciones.id_consultor.id_persona.pais) +', '+str(postulaciones.id_consultor.id_persona.estado) + ', '+str(postulaciones.id_consultor.id_persona.municipio)
                else:
                    direccion = str(postulaciones.id_consultor.id_persona.pais) +', '+str(postulaciones.id_consultor.id_persona.estado) + ', '+str(postulaciones.id_consultor.id_persona.ciudad)


                if postulaciones.id_consultor.id_persona.sexo == 'M':
                    sexo = 'Hombre'
                else:
                    sexo = 'Mujer'
                edad = calcular_edad(str(postulaciones.id_consultor.id_persona.fecha_nacimiento))

                modulos = ConocimientosConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                experiencia = ""
                if modulos:
                    titulo = str(modulos[0].id_modulo.nombre)
                    nivel = str(modulos[0].id_nivel.nombre) 
                    for modulo in modulos:
                        experiencia += modulo.id_modulo.nombre + " "
                else:
                    experiencia = "Sin experiencia"
                    titulo = ""
                    nivel = ""
                        
                # Verificar si existen los atributos necesarios antes de asignarlos
                if hasattr(postulaciones.id_consultor, 'rfc'):
                    rfc = postulaciones.id_consultor.rfc
                else:
                    rfc = None

                # Verificar si existen los atributos necesarios antes de asignarlos
                if hasattr(postulaciones.id_consultor, 'tarifa_hora'):
                    pago = postulaciones.id_consultor.tarifa_hora
                else:
                    pago = None

                if hasattr(postulaciones.id_consultor.id_tipo_moneda, 'tipo'):
                    texto = postulaciones.id_consultor.id_tipo_moneda.tipo
                    resultado = re.search(r'\((.*?)\)', texto)
                    moneda = resultado.group(1)
                else:
                    moneda = None
                        
                if hasattr(postulaciones.id_consultor.id_persona, 'disponible'):
                    disponibilidad = postulaciones.id_consultor.id_persona.disponible
                    if disponibilidad:
                        disponible = 'Disponible'
                    else:
                        disponible = 'No disponible'
                else:
                    disponibilidad = None


                if hasattr(postulaciones.id_consultor.id_persona, 'descripcion'):
                    descripcion = postulaciones.id_consultor.id_persona.descripcion
                    if descripcion:
                        descripcion = postulaciones.id_consultor.id_persona.descripcion
                    else:
                        descripcion = 'Aun no hay descripción'
                else:
                    descripcion = 'Aun no hay descripción'
                
                
                comentarios = 'Aun no hay comentarios'
                

                saber = Usuarios.objects.get(id_persona=postulaciones.id_consultor.id_persona)
        
                if saber.image == '':
                    if postulaciones.id_consultor.id_persona.sexo == 'M':
                        image = '/static/images/profile/default.jpg'
                        default = True
                    else:
                        image = '/static/images/profile/defaultF.png'
                        default = True
                else:
                    image = saber.image
                    default = False


                projects = ProyectoConsultor.objects.filter(id_consultor=postulaciones.id_consultor)
                if projects.exists():  # Verificar si hay proyectos
                    cantidad_proyectos = projects.count()
                    puntuacion = 0

                    for proyecto in projects:
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

                postulados.append([sexo, edad, experiencia, pago, moneda, disponible, id, titulo, nivel, direccion, comentarios, experiencia, descripcion, rfc, image, default, puntuacionConsultor])
            
            
            cPostulados = len(postulados)

        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]
        return render(request, 'mapa_alls.html',{
            'indice': 'Proyectos',
            'empresa':empresa,
            'postulacionesProyecto':postulacionesProyecto[0],
            'postulados':postulados,
            'cPostulados':cPostulados,
            'notifications':notification,
            'pending':pending,
            'pending_total':pending_total,
        })
    
    
    except Empresas.DoesNotExist as error:
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
    except Exception as e:
        print(e)
        messages.error(
            request, 'Ha ocurrido un error al procesar la solicitud. Ponte en contacto con soporte tecnico')
        return redirect('logout')

