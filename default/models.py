from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class Proyectos(models.Model):
    proyecto_nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    num_consultores = models.IntegerField()
    presupuesto_base = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_moneda = models.CharField(max_length=25)
    status = models.CharField(max_length=1)
    description = models.CharField(max_length=150)
    experiencia = models.CharField(max_length=150)
    fun_laborales = models.CharField(max_length=250)
    id_categoria = models.ForeignKey('Categorias', null=True, on_delete=models.SET_NULL)
    id_proyecto_consultor = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)
    id_empresa_proyecto = models.ForeignKey('EmpresaProyecto', null=True, on_delete=models.SET_NULL)

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


class Conocimientos(models.Model):
    nombre = models.CharField(max_length=150)
    description = models.CharField(max_length=150)

    class Meta:
        db_table = 'conocimientos'


class ConocimientosConsultor(models.Model):
    id_conocimiento = models.ForeignKey('Conocimientos', null=True, on_delete=models.SET_NULL)
    id_nivel = models.ForeignKey('Niveles', null=True, on_delete=models.SET_NULL)
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'conocimientos_consultor'


class Consultores(models.Model):
    tipo_persona = models.CharField(max_length=6)
    pasaporte = models.CharField(max_length=30, blank=True, null=True)
    curp = models.CharField(max_length=16, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    visa = models.CharField(max_length=20, blank=True, null=True)
    licencia = models.CharField(max_length=20)
    tarifa_hora = models.CharField(max_length=20)
    id_persona = models.ForeignKey('Personas', null=True, on_delete=models.SET_NULL)
    id_categoria_consultor = models.ForeignKey('Categorias', null=True, on_delete=models.SET_NULL)
    id_manera_pago = models.ForeignKey('ManeraPago', null=True, on_delete=models.SET_NULL, default=1)
    id_tipo_moneda = models.ForeignKey('TipoMoneda', null=True, on_delete=models.SET_NULL, default=1)

    class Meta:
        db_table = 'consultores'


class Contratos(models.Model):
    titulo = models.CharField(max_length=120)
    fecha_firma = models.CharField(max_length=250)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tarifa_dia = models.DecimalField(max_digits=8, decimal_places=2)
    viaticos = models.CharField(max_length=30)
    gerente = models.CharField(max_length=30)
    tiempo_vigencia = models.CharField(max_length=10, blank=True, null=True)
    tipo_moneda = models.CharField(max_length=25)
    id_rol = models.ForeignKey('Roles', null=True, on_delete=models.SET_NULL)
    id_tipo_contrato = models.ForeignKey('TipoContrato', null=True, on_delete=models.SET_NULL)
    id_inmueble = models.ForeignKey('Inmuebles', null=True, on_delete=models.SET_NULL)
    id_proyecto_consultor = models.ForeignKey('ProyectoConsultor', null=True, on_delete=models.SET_NULL)

    class Meta:       
        db_table = 'contrato'


class DatosBancarios(models.Model):
    id_banco = models.ForeignKey('Bancos', null=True, on_delete=models.SET_NULL)
    sucursal = models.CharField(max_length=80)
    no_cuenta_clabe = models.IntegerField()
    id_usuario = models.ForeignKey('Usuarios', null=True, on_delete=models.SET_NULL)

    class Meta:    
        db_table = 'datos_bancarios'



class Documentacion(models.Model):
    ruta = models.IntegerField()
    nombre = models.CharField(max_length=80)
    fecha_creacion = models.DateTimeField()
    id_consultor = models.ForeignKey('Consultores', null=True, on_delete=models.SET_NULL)
    id_tipo_documento = models.ForeignKey('TipoDocumento', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'documentacion'


class EmpresaProyecto(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', null=True, on_delete=models.SET_NULL)
    id_empresas = models.ForeignKey('ClientesEmpresas', null=True, on_delete=models.SET_NULL)

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


class Empresas(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'Empresas'

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
    edad = models.CharField(max_length=2)
    id_persona = models.ForeignKey('Personas', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'hijos'



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
    calle = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
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

    class Meta:
        db_table = 'personas'


class ProyectoConsultor(models.Model):
    puntuacion = models.IntegerField(blank=True, null=True)
    comentario = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.CharField(max_length=10, blank=True, null=True)
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
    nombre = models.CharField(max_length=30)

    class Meta:
        db_table = 'tipo_contrato'


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=20)

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
    rol = models.CharField(max_length=2)
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