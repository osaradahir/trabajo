--
-- Base de datos: `gnosis`
--

-- --------------------------------------------------------

--
-- Estructura para la tabla `proyectos`
--
DROP TABLE IF EXISTS proyectos;

CREATE TABLE proyectos (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `proyecto_nombre` varchar(150) NOT NULL,
    `fecha_inicio` DATETIME NOT NULL,
    `fecha_fin` DATETIME NOT NULL,
    `num_consultores` int(3) NOT NULL,
    `presupuesto_base` DECIMAL(10, 2) NOT NULL,
    `id_tipo_moneda` int(10) NULL,
    `status` varchar(1) NOT NULL,
    `tipo` varchar(20) NOT NULL,
    `description` varchar(150) NOT NULL,
    `certificacion` varchar(50) NOT NULL,
    `duracion` varchar(50) NOT NULL,
    `estudiosRequeridos` varchar(50) NOT NULL,
    `fun_laborales` varchar(250) NOT NULL,
    `fecha_publicacion` DATE DEFAULT CURRENT_TIMESTAMP,
    `id_categoria` int(10) NULL,
    `id_empresa_proyecto` int(10) NULL,
    `id_modulo` int(10),
    `id_submodulo` int(10),
    `id_experiencia_requerida` int(10),
    `id_experiencia_deseable` int(10),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id),
    FOREIGN KEY (id_empresa_proyecto) REFERENCES empresa_proyecto(id),
    FOREIGN KEY (id_tipo_moneda) REFERENCES tipo_moneda(id),
    FOREIGN KEY (id_modulo) REFERENCES modulos (id),
    FOREIGN KEY (id_submodulo) REFERENCES submodulos (id),
    FOREIGN KEY (id_experiencia_requerida) REFERENCES niveles_conocimiento (id),
    FOREIGN KEY (id_experiencia_deseable) REFERENCES niveles_conocimiento (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `categorias`
--
DROP TABLE IF EXISTS categorias;
CREATE TABLE categorias(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `categoria_nombre` varchar(150) NOT NULL,
    `descripcion` varchar(150) NOT NULL    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `proyecto_consultor`
--
DROP TABLE IF EXISTS proyecto_consultor;

CREATE TABLE proyecto_consultor (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `participacion` BOOLEAN NOT NULL,
    `puntuacion` int(5),
    `comentario` varchar(30),
    `fecha_aceptacion` DATETIME NOT NULL,
    `fecha_inicio` DATETIME NOT NULL,
    `fecha_termino` DATETIME NOT NULL,
    `horario_hora_inicio` BOOLEAN NOT NULL,
    `horario_hora_final` BOOLEAN NOT NULL,
    `fun_laborales` varchar(600) NOT NULL,
    `dias_laborales` varchar(30) NOT NULL,
    `status` varchar(30) NOT NULL,
    `tarifa` DECIMAL(8,2) NOT NULL,
    `id_tipo_moneda` int(10) NULL,
    `id_consultor` int(10) NULL,
    `id_contrato` int(10) NULL,
    FOREIGN KEY (id_tipo_moneda) REFERENCES tipo_moneda(id),   
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id),
    FOREIGN KEY (id_consultor) REFERENCES consultores(id),
    FOREIGN KEY (id_contrato) REFERENCES contratos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `empresa_proyecto`
--
DROP TABLE IF EXISTS empresa_proyecto;
CREATE TABLE empresa_proyecto(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_proyecto` int(10) NULL, 
    `id_empresas` int(10) NULL,
    FOREIGN KEY (id_proyecto) references proyectos(id),
    FOREIGN KEY (id_empresas) references empresas(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `clientes_empresas`
--
DROP TABLE IF EXISTS clientes_empresas;

CREATE TABLE clientes_empresas (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `empresa_nombre` varchar(150) NOT NULL,
    `telefono` varchar(10) NOT NULL,
    `calle` varchar(50) NOT NULL,
    `colonia` varchar(50) NOT NULL,
    `numero_ext` varchar(4) NOT NULL,
    `estado` varchar(150) NOT NULL,
    `pais` varchar(150) NOT NULL,
    `codigo_postal` varchar(5) NOT NULL,
    `sitio` varchar(150) NOT NULL,
    `descripcion` varchar(250) NOT NULL,
    `ubicacion` varchar(250) NOT NULL,
    `foto` varchar(150) NULL,
    `volumen` varchar(255) NULL,
    `hardware` varchar(255) NULL,
    `temas_interes` varchar(255) NULL,
    `id_puntuaciones` int(10) NULL,
    `id_empresa_proyecto` int(10) NULL,
    `id_giro` int(10) NULL,
    FOREIGN KEY (id_puntuaciones) REFERENCES proyecto_consultor(id),
    FOREIGN KEY (id_empresa_proyecto) REFERENCES empresa_proyecto(id),
    FOREIGN KEY (id_giro) REFERENCES giro(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura para la tabla `modulos`
--
DROP TABLE IF EXISTS modulos;
CREATE TABLE modulos (
  `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `description` VARCHAR(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `submodulos`
--
DROP TABLE IF EXISTS submodulos;
CREATE TABLE submodulos (
  `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `description` VARCHAR(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `giro`
--
DROP TABLE IF EXISTS giro;
CREATE TABLE giro(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `giro_nombre` varchar(150) NOT NULL,
    `descripcion` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `inmuebles`
--

DROP TABLE IF EXISTS inmuebles;
CREATE TABLE inmuebles(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `requerimiento_personal`
--
DROP TABLE IF EXISTS requerimiento_personal;

CREATE TABLE requerimiento_personal (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `fecha` varchar(250) NOT NULL,
    `no_recursos` int(2) NOT NULL,
    `certificado` varchar(80) NOT NULL,
    `version` varchar(80) NOT NULL,
    `periodo_inicio` DATE NOT NULL,
    `periodo_fin` DATE NOT NULL,
    `lugar_asignacion` varchar(150) NOT NULL,
    `gastos_viaje` BOOLEAN NOT NULL,
    `tarifa` DECIMAL(8,2) NOT NULL,
    `sexo` varchar(1) NULL,
    `comentario` varchar(200) NULL,
    `id_rol` int(10) NULL,
    `id_especialidad` int(10) NULL,
    `id_empresa` int(10) NULL,
    `id_proyecto` int(10) NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id),
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id),
    FOREIGN KEY (id_empresa) REFERENCES empresas(id),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `contratos`
--
DROP TABLE IF EXISTS contratos;
CREATE TABLE contratos (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `titulo` varchar(120) NOT NULL,
    `fecha_firma` varchar(250) NOT NULL,
    `fecha_inicio` DATETIME NOT NULL,
    `fecha_fin` DATETIME NOT NULL,
    `fecha_promesa` DATETIME NOT NULL,
    `tarifa_dia_cliente` DECIMAL(10,4) NULL,
    `tarifa_dia_consultor` DECIMAL(10,4) NULL,
    `viaticos` varchar(30) NULL,
    `gratificacion`  DECIMAL(10,2) NULL,
    `tipoCambioManual` DECIMAL(10,4) NULL,
    `tipoCambioAuto` DECIMAL(10,4) NULL,
    `aplicada` varchar(30) NULL,
    `tipoCambio` DECIMAL(10,4) NULL,
    `gerente` varchar(30) NULL,
    `persona_tercero` varchar(180) NULL,
    `tiempo_vigencia` varchar(60) NULL,
    `id_tipo_moneda` int(10) NULL,
    `id_rol` int(10) NULL,
    `id_tipo_contrato` int(10) NULL,
    `id_tipo_contratacion` int(10) NULL,
    `id_inmueble` int(10) NULL,
    `id_proyecto_consultor` int(10) NULL,
    FOREIGN KEY (id_tipo_moneda) REFERENCES tipo_moneda(id),
    FOREIGN KEY (id_rol) REFERENCES roles(id),
    FOREIGN KEY (id_tipo_contrato) REFERENCES tipo_contrato(id),
    FOREIGN KEY (id_inmueble) REFERENCES inmuebles(id),
    FOREIGN KEY (id_proyecto_consultor) REFERENCES proyecto_consultor(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `requerimientos_experiencia`
--
DROP TABLE IF EXISTS requerimientos_experiencia;
CREATE TABLE requerimientos_experiencia(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_requerimiento` int(10) NOT NULL,
    `id_experiencia` int(10) NOT NULL,
    FOREIGN KEY (id_requerimiento) references requerimiento_personal(id),
    FOREIGN KEY (id_experiencia) references experiencias(id),
    `principal` BOOLEAN NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `roles`
--
DROP TABLE IF EXISTS roles;
CREATE TABLE roles(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(30) NOT NULL,
    `descripcion` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `actividades`
--
DROP TABLE IF EXISTS actividades;
CREATE TABLE actividades(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(30) NOT NULL,
    `descripcion` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Estructura para la tabla `tipo_contrato`
--
DROP TABLE IF EXISTS tipo_contrato;
CREATE TABLE tipo_contrato(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `actividades_proyecto`
--
DROP TABLE IF EXISTS actividades_proyecto;
CREATE TABLE actividades_proyecto(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_proyecto` int(10) NOT NULL,
    `id_actividad` int(10) NOT NULL,
    FOREIGN KEY (id_proyecto) references proyectos(id),
    FOREIGN KEY (id_actividad) references actividades(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `consultores`
--
DROP TABLE IF EXISTS consultores;

CREATE TABLE consultores (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `tipo_persona` varchar(6) NOT NULL,
    `pasaporte` varchar(30) NULL,
    `curp` varchar(16) NULL,
    `rfc` varchar(13) NULL,
    `especialidad` varchar(13) NULL,
    `id_nivel` int(10) NULL,
    `visa` varchar(20) NULL,
    `licencia_conducir` varchar(20) NOT NULL,
    `comprobante_domicilio` varchar(20) NOT NULL,
    `estadoCivil` varchar(20) NOT NULL,
    `viajar` BOOLEAN NOT NULL,
    `tarifa_hora` BOOLEAN NOT NULL,
    `cantidad_hijos` int(10) NOT NULL,
    `id_categoria` int(10) NULL,
    `id_persona` int(10) NULL,
    `id_manera_pago` int(10) NULL,
    `id_tipo_moneda` int(10) NULL,
    FOREIGN KEY (id_persona) REFERENCES requerimiento_personal(id),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id),
    FOREIGN KEY (id_manera_pago) REFERENCES manera_pago(id),
    FOREIGN KEY (id_tipo_moneda) REFERENCES tipo_moneda(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Estructura para la tabla `consultores`
--
DROP TABLE IF EXISTS experiencias_consultor;
CREATE TABLE experiencias_consultor (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_experiencia` varchar(150) NOT NULL,
    `empresa` varchar(200) NOT NULL,
    `puesto` varchar(200) NOT NULL,
    `descripcion` varchar(200) NOT NULL,
    `fecha_entrada` DATE DEFAULT CURRENT_TIMESTAMP,
    `fecha_salida` DATE DEFAULT CURRENT_TIMESTAMP,
    `tiempo_experiencia` varchar(150) NOT NULL,
    `id_consultor` int(10) NOT NULL,
    FOREIGN KEY (id_consultor) references consultores(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `instituciones`
--
DROP TABLE IF EXISTS instituciones;
CREATE TABLE instituciones (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura para la tabla `especialidades`
--
DROP TABLE IF EXISTS especialidades;
CREATE TABLE especialidades (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura para la tabla `estudios`
--
DROP TABLE IF EXISTS estudios;

CREATE TABLE estudios (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_institucion` int(150) NOT NULL,
    `id_especialidad` int(150) NOT NULL,
    `no_cedula` varchar(150) NOT NULL,
    `titulo_registrado` varchar(60) NULL,
    `libro` varchar(60) NOT NULL,
    `fecha_termino` varchar(60) NULL,
    `fecha_ingreso` DATETIME NOT NULL,
    `educacion` varchar(60) NULL,
    `id_consultor` int(10) NOT NULL,
    FOREIGN KEY (id_institucion) REFERENCES instituciones(id),
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id),
    FOREIGN KEY (id_consultor) REFERENCES consultores(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Estructura para la tabla `experiencias`
--
DROP TABLE IF EXISTS experiencias;
CREATE TABLE experiencias (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `niveles_conocimiento`
--
DROP TABLE IF EXISTS niveles_conocimiento;
CREATE TABLE niveles_conocimiento (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL,
    `descripcion` varchar(200) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `conocimientos_consultor`
--
DROP TABLE IF EXISTS conocimientos_consultor;
CREATE TABLE conocimientos_consultor (
  `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id_modulo` int(10),
  `id_submodulo` int(10),
  `id_nivel` int(10),
  `id_consultor` int(10),
  `id_nivelGnosis` int(10) DEFAULT 1,
  `estatus` VARCHAR(150) DEFAULT 'Sin Validar',
  FOREIGN KEY (id_modulo) REFERENCES modulos (id),
  FOREIGN KEY (id_submodulo) REFERENCES submodulos (id),
  FOREIGN KEY (id_nivel) REFERENCES niveles_conocimiento (id),
  FOREIGN KEY (id_consultor) REFERENCES consultores (id),
  FOREIGN KEY (id_nivelGnosis) REFERENCES niveles_conocimiento (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `datos_bancarios`
--
DROP TABLE IF EXISTS datos_bancarios;
CREATE TABLE datos_bancarios (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_banco` int(10) NOT NULL,
    `sucursal` varchar(80) NOT NULL,
    `cuentambiente` varchar(80) NOT NULL,
    `tipo_cuenta` varchar(80) NOT NULL,
    `no_cuenta_clabe` int(18) NOT NULL,
    `ejecutivo_cuenta` varchar(80) NOT NULL,
    `telefono_ejecutivo` varchar(80) NOT NULL,    
    `correo_ejecutivo` varchar(80) NOT NULL,
    `rfc_clave` varchar(80) NOT NULL,
    `dia_corte` varchar(80) NOT NULL,
    `descripcion` varchar(120) NOT NULL,
    `activo` varchar(80) NOT NULL,
    `id_usuario` int(10) NOT NULL,
    FOREIGN KEY (id_banco) references bancos(id),
    FOREIGN KEY (id_usuario) references usuarios(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `documentacion`
--
DROP TABLE IF EXISTS documentacion;
CREATE TABLE documentacion (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `ruta` int(10) NOT NULL,
    `nombre` varchar(80) NOT NULL,
    `fecha_creacion` DATETIME NOT NULL,
    `id_consultor` int(10) NOT NULL,
    `id_tipo_documento` int(10) NOT NULL,
    FOREIGN KEY (id_consultor) references consultores(id),
    FOREIGN KEY (id_tipo_documento) references tipo_documento(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `conocimientos`
--
DROP TABLE IF EXISTS conocimientos;
CREATE TABLE conocimientos (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `niveles`
--
DROP TABLE IF EXISTS niveles;
CREATE TABLE niveles (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL,
    `descripcion` varchar(200) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `bancos`
--
DROP TABLE IF EXISTS bancos;
CREATE TABLE bancos (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(150) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Estructura para la tabla `tipo_documento`
--
DROP TABLE IF EXISTS tipo_documento;
CREATE TABLE tipo_documento(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Estructura para la tabla `personas`
--
DROP TABLE IF EXISTS personas;
CREATE TABLE personas(
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(100) NOT NULL,
    `ape_pat` varchar(200) NOT NULL,
    `ape_mat` varchar(200) NOT NULL,
    `fecha_nacimiento` DATETIME NOT NULL,
    `estado_civil` varchar(100) NOT NULL,
    `colonia` varchar(200) NOT NULL,
    `municipio` varchar(100) NOT NULL,
    `ciudad` varchar(100) NOT NULL,
    `cod_post` varchar(6) NOT NULL,
    `estado` varchar(200) NOT NULL,
    `pais` varchar(200) NOT NULL,
    `telefono` varchar(10) NOT NULL,
    `ext` varchar(4) NULL,
    `nacionalidad` varchar(200) NOT NULL,
    `sexo` varchar(50) NOT NULL,
    `disponible` BOOLEAN NOT NULL,
    `referencia` varchar(150) NOT NULL,
    `descripcion` varchar(190) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `usuarios`
--
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `correo` varchar(100) NOT NULL,
    `password` varchar(100) NOT NULL,
    `image` varbinary(100) NOT NULL,
    `rol` varchar(2) NOT NULL,
    `validacion` BOOLEAN NOT NULL,
    `id_persona` int(10) NOT NULL,
    `is_staff` BOOLEAN NOT NULL
    FOREIGN KEY (id_persona) references personas(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `hijos`
--
DROP TABLE IF EXISTS hijos;
CREATE TABLE hijos (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `genero` varchar(100) NOT NULL,
    `edad` varchar(2) NOT NULL,
    `nHjo` varchar(10) NOT NULL,
    `id_persona` int(10) NULL,
    FOREIGN KEY (id_persona) references personas(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `manera_pago`
--
DROP TABLE IF EXISTS manera_pago;
CREATE TABLE manera_pago (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `tipo` varchar(40) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `tipo_moneda`
--
DROP TABLE IF EXISTS tipo_moneda;
CREATE TABLE tipo_moneda (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `tipo` varchar(40) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `idiomas`
--
DROP TABLE IF EXISTS idiomas;
CREATE TABLE idiomas (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nombre` varchar(40) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




--
-- Estructura para la tabla `idiomas_consultor`
--
DROP TABLE IF EXISTS idiomas_consultor;
CREATE TABLE idiomas_consultor (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_idioma` int(10) NOT NULL,
    `id_consultor` int(10) NOT NULL,
    `nivel` varchar(40) NOT NULL,
    FOREIGN KEY (id_idioma) references idiomas(id),
    FOREIGN KEY (id_consultor) references consultores(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `cursos_consultor`
--
DROP TABLE IF EXISTS cursos_consultor;
CREATE TABLE cursos_consultor (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `id_consultor` int(10) NOT NULL,
    `nombre_curso` varchar(80) NOT NULL,
    `id_institucion_curso` int(10) NOT NULL,
    `enlace_certificado` varchar(80) NOT NULL,
    `descripcion` varchar(80) NOT NULL,
    `fecha_termino` DATETIME NOT NULL,
    FOREIGN KEY (id_consultor) references consultores(id),
    FOREIGN KEY (id_institucion_curso) references instituciones(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `notification_consultor`
--
DROP TABLE IF EXISTS notification_consultor;
CREATE TABLE notification_consultor (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `subject` varchar(100) NOT NULL,
    `message` varchar(100) NOT NULL,
    `created_at` DATE DEFAULT CURRENT_TIMESTAMP,
    `status` ENUM('Pending', 'Read') NOT NULL DEFAULT 'Pending',
    `id_consultor_destinatary` int(10) NOT NULL,
    `action` BOOLEAN NOT NULL,
    `confirm` BOOLEAN NOT NULL,
    `data` varchar(100) NOT NULL,
    `ruta` varchar(100) NOT NULL,
    FOREIGN KEY (id_consultor_destinatary) references consultores(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura para la tabla `notification_administrador`
--
DROP TABLE IF EXISTS notification_administrador;
CREATE TABLE notification_administrador (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `subject` varchar(100) NOT NULL,
    `message` varchar(100) NOT NULL,
    `status` ENUM('Pending', 'Read') NOT NULL DEFAULT 'Pending',
    `created_at` DATE DEFAULT CURRENT_TIMESTAMP,
    `status` ENUM('Pending', 'Read') NOT NULL DEFAULT 'Pending',
    `id_persona_destinatary` int(10) NOT NULL,
    `action` BOOLEAN NOT NULL,
    `enlace` varchar(100) NOT NULL,
    `confirm` BOOLEAN NOT NULL,
    `data` varchar(100) NOT NULL,
    FOREIGN KEY (id_persona_destinatary) references consultores(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `notification_empresa`
--
DROP TABLE IF EXISTS notification_empresa;
CREATE TABLE notification_empresa (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `subject` varchar(100) NOT NULL,
    `message` varchar(100) NOT NULL,
    `created_at` DATE DEFAULT CURRENT_TIMESTAMP,
    `status` ENUM('Pending', 'Read') NOT NULL DEFAULT 'Pending',
    `id_empresa_destinatary` int(10) NOT NULL,
    FOREIGN KEY (id_empresa_destinatary) references consultores(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Estructura para la tabla `empresas`
--
DROP TABLE IF EXISTS empresas;
CREATE TABLE empresas (
    `id` int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `empresa` varchar(80) NOT NULL,
    `nivel` varchar(100) NOT NULL,
    `nombre` varchar(100) NOT NULL,
    `ape_pat` varchar(100) NOT NULL,
    `ape_mat` varchar(100) NOT NULL,
    `telefono` varchar(12) NOT NULL,
    `telefono` varchar(12) NOT NULL,
    `tamano` varchar(100) NOT NULL,
    `industria` varchar(40) NOT NULL,
    `versionSAP` varchar(20) NOT NULL,
    `colonia` varchar(200) NOT NULL,
    `municipio` varchar(100) NOT NULL,
    `ciudad` varchar(100) NOT NULL,
    `calle` varchar(100) NOT NULL,
    `n_exterior` varchar(100) NOT NULL,
    `fax` varchar(100) NOT NULL,
    `cod_post` varchar(6) NOT NULL,
    `estado` varchar(200) NOT NULL,
    `pais` varchar(200) NOT NULL,
    `id_usuario` int(10) NOT NULL,
    FOREIGN KEY (id_usuario) references usuarios(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
