from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.html import format_html
from datetime import date

class Proyectos(models.Model):
    proyecto_nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    num_consultores = models.IntegerField(null=True)
    presupuesto_base = models.DecimalField(max_digits=10, decimal_places=2)
    id_tipo_moneda = models.ForeignKey('TipoMoneda', null=True, on_delete=models.SET_NULL, default=1)
    status = models.CharField(max_length=20, null=True)
    tipo = models.CharField(max_length=20, null=True, default="Completo")
    description = models.CharField(max_length=1000, null=True)
    certificacion = models.CharField(max_length=50, null=True, default="ABAP")
    duracion = models.CharField(max_length=50, null=True, default="1 Mes")
    estudiosRequeridos = models.CharField(max_length=50, null=True, default="Ingeniería")
    fun_laborales = models.CharField(max_length=1000, null=True)
    fecha_publicacion = models.DateField(default=date.today)
    id_categoria = models.ForeignKey('Categorias', null=True, on_delete=models.SET_NULL)
    id_empresa_proyecto = models.ForeignKey('EmpresaProyecto', null=True, on_delete=models.SET_NULL)
    id_modulo = models.ForeignKey('Modulos', null=True, on_delete=models.SET_NULL)
    id_submodulo = models.ForeignKey('Submodulos', null=True, on_delete=models.SET_NULL)
    id_experiencia_requerida = models.ForeignKey('NivelesConocimiento', null=True, on_delete=models.SET_NULL, related_name='experiencia_requerida', default=1)
    id_experiencia_deseable = models.ForeignKey('NivelesConocimiento', null=True, on_delete=models.SET_NULL, related_name='experiencia_deseable', default=1)

    class Meta:
        db_table = 'proyectos'

class ActividadesProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_actividad = models.ForeignKey('Actividades', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'actividades_proyecto'


class Actividades(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=250)

    class Meta:
        db_table = 'actividades'



class Bancos(models.Model):
    nombre = models.CharField(max_length=150)
    class Meta:
        db_table = 'bancos'


class Categorias(models.Model):
    categoria_nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150)

    class Meta:
        
        db_table = 'categorias'


class ClientesEmpresas(models.Model):
    empresa_nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=10)
    calle = models.CharField(max_length=50)
    colonia = models.CharField(max_length=50)
    numero_ext = models.CharField(max_length=4)
    estado = models.CharField(max_length=150)
    pais = models.CharField(max_length=150)
    codigo_postal = models.CharField(max_length=5)
    sitio = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250)
    ubicacion = models.CharField(max_length=250)
    foto = models.CharField(max_length=150, blank=True, null=True)
    volumen = models.CharField(max_length=255, blank=True, null=True)
    hardware = models.CharField(max_length=255, blank=True, null=True)
    temas_interes = models.CharField(max_length=255, blank=True, null=True)
    id_puntuaciones = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)
    id_empresa_proyecto = models.ForeignKey('EmpresaProyecto', null=True, on_delete=models.SET_NULL)
    id_giro = models.ForeignKey('Giro', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'clientes_empresas'


class Modulos(models.Model):
    nombre = models.CharField(max_length=150)
    description = models.CharField(max_length=150)

    class Meta:
        db_table = 'modulos'


class Submodulos(models.Model):
    nombre = models.CharField(max_length=150)
    description = models.CharField(max_length=150)

    class Meta:
        db_table = 'submodulos'


class ConocimientosConsultor(models.Model):
    id_modulo = models.ForeignKey('Modulos', null=True, on_delete=models.SET_NULL)
    id_submodulo = models.ForeignKey('Submodulos', null=True, on_delete=models.SET_NULL)
    id_nivel = models.ForeignKey('NivelesConocimiento', null=True, on_delete=models.SET_NULL, related_name='conocimientosconsultor_nivel')
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    id_nivelGnosis = models.ForeignKey('NivelesConocimiento', null=True, on_delete=models.SET_NULL, default=1, related_name='conocimientosconsultor_nivelgnosis')
    estatus = models.CharField(max_length=150, default='Sin Validar')

    class Meta:
        db_table = 'conocimientos_consultor'



class Consultores(models.Model):
    tipo_persona = models.CharField(max_length=6)
    pasaporte = models.CharField(max_length=30, blank=True, null=True)
    curp = models.CharField(max_length=19, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    especialidad = models.CharField(max_length=13, blank=True, default="")
    id_nivel = models.ForeignKey('NivelesConocimiento', on_delete=models.SET_NULL, null=True, default=1)
    visa = models.CharField(max_length=20, blank=True, null=True)
    licencia_conducir = models.CharField(max_length=20, default="")
    comprobante_domicilio = models.CharField(max_length=20, default="")
    estadoCivil = models.CharField(max_length=20, default="")
    viajar = models.BooleanField(default=True)
    tarifa_hora = models.IntegerField(null=True, default=0)
    cantidad_hijos = models.IntegerField(null=True, default=0)
    id_categoria = models.ForeignKey('CategoriasConsultor', default=2, null=True, on_delete=models.SET_NULL)
    id_persona = models.ForeignKey('Personas', null=True, on_delete=models.SET_NULL)
    id_manera_pago = models.ForeignKey('ManeraPago', null=True, on_delete=models.SET_NULL, default=1)
    id_tipo_moneda = models.ForeignKey('TipoMoneda', null=True, on_delete=models.SET_NULL, default=1)

    class Meta:
        db_table = 'consultores'


class Contratos(models.Model):
    titulo = models.CharField(max_length=120) # si
    fecha_firma = models.CharField(max_length=250) # si
    fecha_inicio = models.DateTimeField() # si
    fecha_fin = models.DateTimeField() # si
    fecha_promesa = models.DateTimeField(default=timezone.now) # si
    tarifa_dia_cliente = models.DecimalField(max_digits=10, decimal_places=4, null=True) # si
    tarifa_dia_consultor = models.DecimalField(max_digits=10, decimal_places=4, null=True) # si
    viaticos = models.CharField(max_length=30, null=True) # si
    gratificacion = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) # si
    tipoCambioManual = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True) # si
    tipoCambioAuto = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True) # si
    aplicada = models.CharField(max_length=30, null=True)
    tipoCambio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True) # si
    gerente = models.CharField(max_length=30, null=True) 
    persona_tercero = models.CharField(max_length=180, blank=True, null=True)
    tiempo_vigencia = models.CharField(max_length=60, blank=True, null=True)
    id_tipo_moneda = models.ForeignKey('TipoMoneda', null=True, on_delete=models.SET_NULL, default=1)
    id_rol = models.ForeignKey('Roles', null=True, on_delete=models.SET_NULL)
    id_tipo_contrato = models.ForeignKey('TipoContrato', null=True, on_delete=models.SET_NULL)
    id_tipo_contratacion = models.ForeignKey('TipoContrataciones', null=True, on_delete=models.SET_NULL)
    id_inmueble = models.ForeignKey('Inmuebles', null=True, on_delete=models.SET_NULL)
    id_proyecto_consultor = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)

    class Meta:       
        db_table = 'contrato'


class TipoContrataciones(models.Model):
    contratacion = models.CharField(max_length=60, default="")

    class Meta:       
        db_table = 'tipo_contratacion'


class Facturas(models.Model):
    id_proyecto_consultor = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)
    validacionGnosis = models.CharField(max_length=20, default="Pendiente")
    validacionEmpresa = models.CharField(max_length=20, default="Pendiente")
    periodo = models.CharField(max_length=20, default="")
    num_mes_declarado = models.CharField(max_length=10, default="")
    fecha_cobranza = models.DateTimeField(default=timezone.now)
    fecha_pago = models.DateTimeField(default=timezone.now)
    tipoCambioMXN = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0.00) # si
    tipoCambioUSD = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0.00) # si
    id_documentacion = models.ForeignKey('Documentacion', null=True, on_delete=models.SET_NULL)

    class Meta:       
        db_table = 'facturas'


class ReporteHoras(models.Model):
    id_proyecto_consultor = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)
    validacionGnosis = models.CharField(max_length=20, default="Pendiente")
    validacionEmpresa = models.CharField(max_length=20, default="Pendiente")
    periodo = models.CharField(max_length=20, default="")
    id_documentacion = models.ForeignKey('Documentacion', null=True, on_delete=models.SET_NULL)

    class Meta:       
        db_table = 'reportes_horas'



class ReporteFinalActividades(models.Model):
    id_proyecto_consultor = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)
    validacionGnosis = models.CharField(max_length=20, default="Pendiente")
    validacionEmpresa = models.CharField(max_length=20, default="Pendiente")
    periodo = models.CharField(max_length=20, default="")
    id_documentacion = models.ForeignKey('Documentacion', null=True, on_delete=models.SET_NULL)

    class Meta:       
        db_table = 'reportes_final_actividades'


class DatosBancarios(models.Model):
    id_banco = models.ForeignKey('Bancos', null=True, on_delete=models.SET_NULL)
    sucursal = models.CharField(max_length=80, default="")
    cuentambiente = models.CharField(max_length=80, default="")
    tipo_cuenta = models.CharField(max_length=80, default="")
    no_cuenta_clabe = models.CharField(max_length=80, default="")
    ejecutivo_cuenta = models.CharField(max_length=80, default="")
    telefono_ejecutivo = models.CharField(max_length=80, default="")
    correo_ejecutivo = models.CharField(max_length=80, default="")
    rfc_clave = models.CharField(max_length=80, default="")
    dia_corte = models.CharField(max_length=80, default="")
    descripcion = models.CharField(max_length=120, default="")
    activo = models.BooleanField(default=True)
    id_usuario = models.ForeignKey('Usuarios', null=True, on_delete=models.SET_NULL)

    class Meta:    
        db_table = 'datos_bancarios'



class Documentacion(models.Model):
    ruta =  models.CharField(max_length=120)
    nombre = models.CharField(max_length=180)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    id_tipo_documento = models.ForeignKey('TipoDocumento', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'documentacion'


class EmpresaProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'empresa_proyecto'


class Especialidades(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'especialidades'


class Inmuebles(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'inmuebles'


class Estudios(models.Model):
    id_institucion = models.ForeignKey('Instituciones', null=True, on_delete=models.SET_NULL)
    id_especialidad = models.ForeignKey('Especialidades', null=True, on_delete=models.SET_NULL)
    no_cedula = models.CharField(max_length=150)
    titulo_registrado = models.CharField(max_length=150, blank=True, null=True)
    libro = models.CharField(max_length=60)
    fecha_termino = models.CharField(max_length=40)
    educacion = models.CharField(max_length=60, blank=True, null=True)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    fecha_ingreso = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'estudios'

class Instituciones(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'instituciones'

class Experiencias(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'experiencias'


class ExperienciasConsultor(models.Model):
    id_experiencia = models.ForeignKey('Experiencias', null=True, on_delete=models.SET_NULL)
    empresa = models.CharField(max_length=200, default='NE')
    puesto = models.CharField(max_length=200, default='NE')
    descripcion = models.CharField(max_length=800)
    fecha_entrada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(default=timezone.now)
    tiempo_experiencia = models.CharField(max_length=150)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'experiencias_consultor'


class Giro(models.Model):
    giro_nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250)

    class Meta:
        db_table = 'giro'


class Hijos(models.Model):
    genero = models.CharField(max_length=100)
    edad = models.CharField(max_length=10)
    nHjo = models.CharField(max_length=10, default="")
    id_persona = models.ForeignKey('Personas', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'hijos'


class NivelesConocimiento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=200)

    class Meta:
        db_table = 'niveles_conocimiento'



class Niveles(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=200)

    class Meta:
        db_table = 'niveles'


class Personas(models.Model):
    nombre = models.CharField(max_length=100)
    ape_pat = models.CharField(max_length=200)
    ape_mat = models.CharField(max_length=200)
    fecha_nacimiento = models.DateTimeField()
    estado_civil = models.CharField(max_length=100)
    colonia = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    cod_post = models.CharField(max_length=6)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    ext = models.CharField(max_length=4, blank=True, null=True)
    nacionalidad = models.CharField(max_length=200)
    sexo = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    referencia = models.CharField(max_length=150, default="")
    descripcion = models.CharField(max_length=190, default="")

    class Meta:
        db_table = 'personas'


class ProyectoConsultor(models.Model):
    participacion = models.BooleanField(default=True)
    puntuacion = models.CharField(max_length=10, null=True, default="0")
    comentario = models.CharField(max_length=1000, null=True, default="Sin comentarios")
    fecha_aceptacion = models.DateTimeField(default=timezone.now)
    fecha_inicio = models.DateField(null=True)
    fecha_termino = models.DateField(null=True)
    horario_hora_inicio = models.TimeField(null=True)
    horario_hora_final = models.TimeField(null=True)
    fun_laborales = models.CharField(max_length=600, null=True)
    dias_laborales = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True)
    tarifa = models.IntegerField(null=True, default=0)
    id_tipo_moneda = models.ForeignKey('TipoMoneda', null=True, on_delete=models.SET_NULL, default=1)
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    id_contrato = models.ForeignKey('Contratos', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'proyecto_consultor'



class RequerimientoPersonal(models.Model):
    fecha = models.CharField(max_length=250)
    no_recursos = models.IntegerField()
    certificado = models.CharField(max_length=80)
    version = models.CharField(max_length=80)
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    lugar_asignacion = models.CharField(max_length=150)
    gastos_viaje = models.IntegerField()
    tarifa = models.DecimalField(max_digits=8, decimal_places=2)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    comentario = models.CharField(max_length=200, blank=True, null=True)
    id_rol = models.ForeignKey('Roles', null=True, on_delete=models.SET_NULL)
    id_especialidad = models.ForeignKey('Especialidades', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('ClientesEmpresas', null=True, on_delete=models.SET_NULL)
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'requerimiento_personal'


class RequerimientosExperiencia(models.Model):
    id_requerimiento = models.ForeignKey('RequerimientoPersonal', null=True, on_delete=models.SET_NULL)
    id_experiencia = models.ForeignKey('Experiencias', null=True, on_delete=models.SET_NULL)
    principal = models.IntegerField()

    class Meta:  
        db_table = 'requerimientos_experiencia'


class Roles(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=250)

    class Meta:  
        db_table = 'roles'


class TipoContrato(models.Model):
    nombre = models.CharField(max_length=60)

    class Meta:
        db_table = 'tipo_contrato'


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'tipo_documento'


class UsuariosManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El campo "correo" es obligatorio.')
        user = self.model(correo=self.normalize_email(correo), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class Usuarios(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    rol = models.CharField(max_length=16)
    validacion = models.BooleanField(default=True)
    id_persona = models.ForeignKey('Personas', null=True, on_delete=models.SET_NULL)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []

    objects = UsuariosManager()

    class Meta:
        db_table = 'usuarios'



class ManeraPago(models.Model):
    tipo = models.CharField(max_length=40)

    class Meta:
        db_table = 'manera_pago'


class TipoMoneda(models.Model):
    tipo = models.CharField(max_length=40)

    class Meta:
        db_table = 'tipo_moneda'


class Idiomas(models.Model):
    nombre = models.CharField(max_length=40)

    class Meta:
        db_table = 'idiomas'


class IdiomasConsultor(models.Model):
    id_idioma = models.ForeignKey('Idiomas', null=True, on_delete=models.SET_NULL)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    nivel = models.CharField(max_length=40, default="")
    
    class Meta:
        db_table = 'idiomas_consultor'


class CursosConsultor(models.Model):
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    nombre_curso = models.CharField(max_length=80, default="")
    id_institucion_curso = models.ForeignKey('Instituciones', null=True, on_delete=models.SET_NULL)
    enlace_certificado = models.CharField(max_length=100, default="")
    descripcion = models.CharField(max_length=400, default="")
    fecha_termino = models.DateField()

    class Meta:
        db_table = 'cursos_consultor'


class NotificationConsultor(models.Model):
    
    STATUS = (
        ('Pending', 'Pending'),
        ('Read', 'Read'),
    )
    name=models.CharField(max_length=100)
    #correo
    email=models.CharField(max_length=100)
    # asusnto
    subject=models.CharField(max_length=100)
    # contenido 
    message = models.TextField(max_length=200)
    # fecha en que se creo
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)
    # id consultor 
    id_consultor_destinatary = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    action = models.BooleanField(default=False)
    confirm = models.BooleanField(default=False)
    data = models.CharField(max_length=100, default="")
    ruta = models.CharField(max_length=100, default="")

    class Meta:
        db_table="notification_consultor" 



class NotificationAdministrador(models.Model):
    
    STATUS = (
        ('Pending', 'Pending'),
        ('Read', 'Read'),
    )
    name=models.CharField(max_length=100)
    #correo
    email=models.CharField(max_length=100)
    # asusnto
    subject=models.CharField(max_length=100)
    # contenido 
    message = models.TextField(max_length=600)
    # fecha en que se creo
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)
    # id consultor 
    id_persona_destinatary = models.ForeignKey('Personas', null=True, on_delete=models.SET_NULL)
    action = models.BooleanField(default=False)
    enlace = models.CharField(max_length=100, default="")
    confirm = models.BooleanField(default=False)
    data = models.CharField(max_length=100, default="")

    class Meta:
        db_table="notification_administrador" 


class NotificationEmpresa(models.Model):
    
    STATUS = (
        ('Pending', 'Pending'),
        ('Read', 'Read'),
    )
    name=models.CharField(max_length=100)
    #correo
    email=models.CharField(max_length=100)
    # asusnto
    subject=models.CharField(max_length=100)
    # contenido 
    message = models.TextField(max_length=200)
    # fecha en que se creo
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)
    # id consultor 
    id_empresa_destinatary = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table="notification_empresa" 



class Empresas(models.Model):
    empresa = models.CharField(max_length=80, default="")
    nivel = models.CharField(max_length=80, default="")
    nombre = models.CharField(max_length=100, default="")
    ape_pat = models.CharField(max_length=200, default="")
    ape_mat = models.CharField(max_length=200, default="")
    telefono = models.CharField(max_length=12, default="")
    telefono = models.CharField(max_length=12, default="")
    tamano = models.CharField(max_length=120, default="")
    industria = models.CharField(max_length=40, default="")
    versionSAP = models.CharField(max_length=20, default="")
    colonia = models.CharField(max_length=200, default="")
    municipio = models.CharField(max_length=100, default="")
    ciudad = models.CharField(max_length=100, default="")
    calle = models.CharField(max_length=100, default="")
    n_exterior = models.CharField(max_length=100, default="")
    fax = models.CharField(max_length=100, default="")
    cod_post = models.CharField(max_length=6, default="")
    estado = models.CharField(max_length=200, default="")
    pais = models.CharField(max_length=200, default="")
    id_usuario = models.ForeignKey('Usuarios', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'empresas'

class RequerimientosModulosProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)
    id_modulo = models.ForeignKey('Modulos', null=True, on_delete=models.SET_NULL)
    id_submodulo = models.ForeignKey('Submodulos', null=True, on_delete=models.SET_NULL)
    id_experiencia_requerida = models.ForeignKey('NivelesConocimiento', null=True, on_delete=models.SET_NULL, related_name='requerimientos_modulos_proyecto_experiencia_requerida', default=1)
    id_experiencia_deseable = models.ForeignKey('NivelesConocimiento', null=True, on_delete=models.SET_NULL, related_name='requerimientos_modulos_proyecto_experiencia_deseable', default=1)

    class Meta:
        db_table = 'requerimientos_modulos_proyecto'


class RequerimientosIdiomasProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)
    id_idioma = models.ForeignKey('Idiomas', null=True, on_delete=models.SET_NULL)
    nivelRequerido = models.CharField(max_length=40, default="")
    nivelDeseado = models.CharField(max_length=40, default="")

    class Meta:
        db_table = 'requerimientos_idiomas_proyecto'


class PostulacionesProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'postulaciones_proyecto'

    
class EntrevistasConsultoresProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True)
    estatus = models.CharField(max_length=30, default="")

    class Meta:
        db_table = 'entrevistas_consultores_proyecto'


class CategoriasConsultor(models.Model):
    categoria_nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150)

    class Meta:
        
        db_table = 'categorias_consultor'


class PostulacionesProyectoGnosis(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresa = models.ForeignKey('Empresas', null=True, on_delete=models.SET_NULL)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'postulaciones_proyecto_gnosis'


class NotasGnosisConsultor(models.Model):
    fecha_creacion = models.DateTimeField(default=timezone.now)
    nota = models.CharField(max_length=650)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'notas_gnosis_consultor'