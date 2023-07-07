from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from default.models import Usuarios, Personas, Consultores, Experiencias, ExperienciasConsultor, Instituciones, Estudios, ManeraPago, TipoMoneda, Idiomas, IdiomasConsultor, Modulos, Submodulos, NivelesConocimiento, ConocimientosConsultor, CursosConsultor,Empresas, NotificationEmpresa
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from datetime import date
from datetime import datetime
import calendar
from django.contrib.auth import login, logout, authenticate
import os
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from pytz import timezone
import shutil


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
            paginator = Paginator(notification_list, 6)
            print(paginator)
            page = request.GET.get('page')
            notification = paginator.get_page(page)

            # CANT. NOTIFICATIONS PENDING
            pending_total = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary_id=empresa.id).order_by('-created_at')

            # ONLY 4 PENDING
            pending = NotificationEmpresa.objects.filter(status='Pending', id_empresa_destinatary_id=empresa.id).order_by('-created_at')[:4]
            
            return render(request, 'notifications/all_notificationsAdministrador.html', {
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


