INSERT INTO `idiomas` (`id`, `nombre`) VALUES
(1, 'Chino (mandarín)'),
(2, 'Español'),
(3, 'Inglés'),
(4, 'Hindi'),
(5, 'Árabe'),
(6, 'Portugués'),
(7, 'Bengalí'),
(8, 'Ruso'),
(9, 'Japonés'),
(10, 'Punjabi'),
(11, 'Alemán'),
(12, 'Javanés'),
(13, 'Wu (Shanghainés)'),
(14, 'Telugu'),
(15, 'Vietnamita'),
(16, 'Coreano'),
(17, 'Francés'),
(18, 'Maratí'),
(19, 'Tamil'),
(20, 'Urdu'),
(21, 'Turco'),
(22, 'Italiano'),
(23, 'Yue (Cantonés)'),
(24, 'Tailandés'),
(25, 'Gujarati'),
(26, 'Jin'),
(27, 'Persa'),
(28, 'Polaco'),
(29, 'Pashto'),
(30, 'Kannada'),
(31, 'Indonesio'),
(32, 'Malayo'),
(33, 'Hebreo'),
(34, 'Árabe'),
(35, 'Bengalí'),
(36, 'Maratí'),
(37, 'Tamil'),
(38, 'Gujarati'),
(39, 'Telugu'),
(40, 'Punjabi'),
(41, 'Tagalo'),
(42, 'Ucraniano'),
(43, 'Birmano'),
(44, 'Sundanés'),
(45, 'Amárico'),
(46, 'Javanés'),
(47, 'Griego moderno'),
(48, 'Chino (cantonés)'),
(49, 'Chino (mandarín)'),
(50, 'Chino (wú)'),
(51, 'Chino (jin)'),
(52, 'Chino (yue)'),
(53, 'Chino (min)'),
(54, 'Chino (xiang)'),
(55, 'Chino (hakka)'),
(56, 'Chino (gan)'),
(57, 'Chino (huizhou)'),
(58, 'Chino (ping)'),
(59, 'Chino (jinyu)'),
(60, 'Chino (qian)');


INSERT INTO `modulos` (`id`, `nombre`, `description`) VALUES
(1, 'MM', ''),
(2, 'FI', ''),
(3, 'CRM', ''),
(4, 'HR', ''),
(5, 'FICO', ''),
(6, 'CO', ''),
(7, 'Logistico', ''),
(8, 'Basis', ''),
(9, 'SD', ''),
(10, 'ABAP', '');


INSERT INTO `niveles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Nivel básico', 'Es el nivel inicial donde se introducen los conceptos fundamentales y se adquieren habilidades básicas en el tema del curso.'),
(2, 'Nivel intermedio', 'Después del nivel básico, se avanza al nivel intermedio, donde se profundiza en los conocimientos y habilidades, y se abordan temas más complejos.'),
(3, 'Nivel avanzado', 'En este nivel, se exploran conceptos y habilidades más avanzadas, se realizan proyectos más complejos y se desarrolla un mayor nivel de experiencia y dominio en el tema del curso.'),
(4, 'Nivel experto', 'En algunos casos, puede existir un nivel experto que está destinado a aquellos que desean alcanzar un nivel de dominio excepcional en el tema del curso. Este nivel implica un alto nivel de especialización y puede requerir experiencia práctica y conocimientos profundos.');


INSERT INTO `niveles_conocimiento` (`id`, `nombre`, `descripcion`) VALUES
(1, 'K0', 'Conocimiento a nivel introductorio'),
(2, 'K1', 'De 1 a 2 proyectos. de 1 a 3 años de experiencia'),
(3, 'K2', 'De 3 a S proyectos.prox. de 3 a 5 años de experiencia'),
(4, 'K3', 'Dominio de la funcionalidad.Más de 5 años en proyecto'),
(5, 'K4', 'Experto de la funcionalidad con más de 5 años en proyectos y ha estado como líder');


INSERT INTO `submodulos` (`id`, `nombre`, `description`) VALUES
(2, 'LE-TRA', ''),
(3, 'MRP', ''),
(4, 'GL, TX', ''),
(5, 'FSCM', ''),
(6, 'PA', ''),
(7, 'OM', ''),
(8, 'PD', ''),
(9, 'TR', ''),
(10, 'PY', ''),
(11, 'TM', ''),
(12, 'ESS', ''),
(13, 'WS', ''),
(14, 'ABAP', ''),
(15, 'Data conversion', ''),
(16, 'Testing Consultor', ''),
(17, 'AFS', ''),
(18, 'GL', ''),
(19, 'PC', ''),
(20, 'Variant Configuration', ''),
(21, 'BO', ''),
(22, 'BW', ''),
(23, 'MM', '');


INSERT INTO `tipo_moneda` (`id`, `tipo`) VALUES
(1, 'Peso mexicano (MXN)'),
(2, 'Dólar estadounidense (USD)'),
(3, 'Euro (EUR)'),
(4, 'Yen japonés (JPY)'),
(5, 'Libra esterlina (GBP)'),
(6, 'Dólar australiano (AUD)'),
(7, 'Dólar canadiense (CAD)'),
(8, 'Franco suizo (CHF)'),
(9, 'Yuan chino (CNY)'),
(10, 'Corona sueca (SEK)'),
(11, 'Dólar neozelandés (NZD)'),
(12, 'Dólar de Singapur (SGD)'),
(13, 'Dólar de Hong Kong (HKD)'),
(14, 'Corona noruega (NOK)'),
(15, 'Won surcoreano (KRW)'),
(16, 'Lira turca (TRY)'),
(17, 'Rublo ruso (RUB)'),
(18, 'Rand sudafricano (ZAR)'),
(19, 'Real brasileño (BRL)'),
(20, 'Rupia india (INR)');


INSERT INTO `categorias`(`categoria_nombre`, `descripcion`) VALUES ('Bolsa de trabajo', 'Descripcion catergoria'),('Categoria 2', 'Descripcion catergoria'),('Categoria 3', 'Descripcion catergoria'),('Categoria 4', 'Descripcion catergoria');


INSERT INTO `manera_pago` (`id`, `tipo`) VALUES
(1, 'Nomina'),
(2, 'Efectivo');


INSERT INTO `categorias_consultor`(`id`, `categoria_nombre`, `descripcion`) VALUES 
(1,'Mala','Consultor con malas reseñas.'), 
(2,'Regular','Consultor con reseñas regulares.'),
(3,'Buena','Consultor con buenas reseñas.'),
(4,'Excelente','Consultor con reseñas excelentes.');