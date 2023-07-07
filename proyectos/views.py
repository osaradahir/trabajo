from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor,Empresas, NotificationEmpresa, Categorias, Proyectos, EmpresaProyecto
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from .config import cipher_suite
from cryptography.fernet import Fernet
from datetime import date
from datetime import datetime
import calendar
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
import os
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from pytz import timezone
import shutil

@login_required
def my_projects(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)

        empresaProyectos = EmpresaProyecto.objects.filter(id_empresa_id=empresa.id)
        query = request.GET.get('query')
        if empresaProyectos.exists():
            if not query:
                proyectos = Proyectos.objects.filter(id_empresa_proyecto__in=empresaProyectos)
            else:
                proyectos = Proyectos.objects.filter(proyecto_nombre__icontains=query,id_empresa_proyecto__in=empresaProyectos)

            paginator = Paginator(proyectos, 4)
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
            presupuesto = request.POST['presupuesto']
            modulo = request.POST['modulo']
            submodulo = request.POST['submodulo']
            experienciaRequerida = request.POST['experienciaRequerida']
            experienciaDesesada = request.POST['experienciaDesesada']

            params = {
                'presupuesto': cipher_suite.encrypt(presupuesto.encode('utf-8')).decode('utf-8'),
                'modulo': cipher_suite.encrypt(modulo.encode('utf-8')).decode('utf-8'),
                'submodulo': cipher_suite.encrypt(submodulo.encode('utf-8')).decode('utf-8'),
                'experienciaRequerida': cipher_suite.encrypt(experienciaRequerida.encode('utf-8')).decode('utf-8'),
                'experienciaDesesada': cipher_suite.encrypt(experienciaDesesada.encode('utf-8')).decode('utf-8'),
            }
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
        print(decrypted_titulo)

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
        decrypted_nivelRequerido = cipher_suite.decrypt(encrypted_nivelRequerido).decode('utf-8')
        decrypted_nivelDeseable = cipher_suite.decrypt(encrypted_nivelDeseable).decode('utf-8')


        categoria = Categorias.objects.get(pk=int(decrypted_categoria))
        moneda = TipoMoneda.objects.get(pk=int(decrypted_moneda))
        modulo = Modulos.objects.get(pk=int(decrypted_modulo))
        submodulo = Submodulos.objects.get(pk=int(decrypted_submodulo))
        experienciaRequerida = NivelesConocimiento.objects.get(pk=int(decrypted_experienciaRequerida))
        experienciaDeseada = NivelesConocimiento.objects.get(pk=int(decrypted_experienciaDesesada))
        idoma = Idiomas.objects.get(pk=int(decrypted_idiomaRequerido))

        proyectos = Proyectos(proyecto_nombre=decrypted_titulo, fecha_inicio=decrypted_date_start, fecha_fin=decrypted_date_end, num_consultores=decrypted_consultoresCantidad, presupuesto_base=decrypted_presupuesto, status='Staffing',  description=decrypted_descripcion, fun_laborales=decrypted_funciones, id_categoria=categoria, id_tipo_moneda=moneda, id_experiencia_deseable=experienciaDeseada, id_experiencia_requerida=experienciaRequerida, id_modulo=modulo, id_submodulo=submodulo)
        proyectos.save()

        empresaProyecto = EmpresaProyecto(id_proyecto=proyectos, id_empresa=empresa)
        empresaProyecto.save()
        proyectos.id_empresa_proyecto = empresaProyecto
        proyectos.save()

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


        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]


        return render(request, 'details_project.html',{
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
def mapa(request):
    try:
        user = Usuarios.objects.get(correo=request.session.get('username'))
        empresa = Empresas.objects.get(id_usuario=user)


        notification = NotificationEmpresa.objects.filter(id_empresa_destinatary=empresa.id)
        # // CANT. NOTIFICATIONS PENDING
        pending_total= NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')
        # // ONLY 4 PENDING 
        pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary=empresa.id).order_by('-created_at')[:4]


        return render(request, 'mapa_consultores.html',{
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