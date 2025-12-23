import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_catalogo (
    id_catalogo INTEGER PRIMARY KEY AUTOINCREMENT,
    cat_codigo TEXT,
    cat_nombre TEXT,
    ca_estado INTEGER
)
""")

cursor.executemany("""
INSERT OR IGNORE INTO tbl_catalogo (id_catalogo, cat_codigo, cat_nombre, ca_estado)
VALUES (?, ?, ?, ?)
""", [
    (18, 'PROV', 'Provincias', 1),
    (19, 'CANT', 'Cantones', 1),
    (20, 'PARR', 'Parroquias', 1),
    (22, 'TIPOVIVIENDA', 'Tipo de vivienda', 1),
    (23, 'TIPOTECHO', 'Tipo de techos', 1),
    (24, 'TIPOPARED', 'Tipo de pared', 1),
    (25, 'TIPOPISO', 'Tipo de piso', 1),
    (26, 'COMB-COCINA', 'Combustible cocina', 1),
    (27, 'SERV-HIG', 'Servicios higiénicos', 1),
    (28, 'ALOJAMIENTO', 'Vivienda o alojamiento', 1),
    (29, 'SERV-AGUA', 'Servicio de agua', 1),
    (30, 'ELM-BAS', 'Eliminación de basura', 1),
    (31, 'LUG-FREC-COMPRA', 'Lugares frecuentes de compra', 1),
    (32, 'TIP-VEHICULOS', 'Tipo de vehículos', 1),
    (33, 'EST-TRANSPORTE', 'Estados de transporte', 1),
    (34, 'ETNIA', 'Etnias', 1),
    (35, 'GENERO', 'Lista de géneros', 1),
    (36, 'NIV-EDU', 'Nivel de educación', 1),
    (37, 'EST-CIV', 'Estado civil', 1),
])

cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_item_catalogo (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    itc_codigo TEXT,
    itc_nombre TEXT,
    itc_descripcion TEXT,
    itc_estado INTEGER,
    id_catalogo INTEGER,
    FOREIGN KEY (id_catalogo) REFERENCES tbl_catalogo(id_catalogo)
)
""")

cursor.executemany("""
INSERT OR IGNORE INTO tbl_item_catalogo (id_item, itc_codigo, itc_nombre, itc_descripcion, itc_estado, id_catalogo)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    (2, 'CAR', 'Carchi', 'Provincia de Carchi', 1, 18),
    (3, 'IMB', 'Imbabura', 'Provincia de Imbabura', 1, 18),
    (4, 'IBARRA', 'Ibarra', 'Cantón de Imbabura', 1, 19),
    (5, 'ANTON', 'Antonio Ante', 'Cantón de Imbabura', 1, 19),
    (6, 'COTAC', 'Cotacachi', 'Cantón de Imbabura', 1, 19),
    (7, 'OTAV', 'Otavalo', 'Cantón de Imbabura', 1, 19),
    (8, 'PIMAM', 'Pimampiro', 'Cantón de Imbabura', 1, 19),
    (9, 'URCU', 'Urcuquí', 'Cantón de Imbabura', 1, 19),
    (10, 'TULCÁN', 'Tulcán', 'Cantón de Carchi', 1, 19),
    (11, 'BOLÍVAR', 'Bolívar', 'Cantón de Carchi', 1, 19),
    (12, 'ESPEJO', 'Espejo', 'Cantón de Carchi', 1, 19),
    (13, 'MIRA', 'Mira', 'Cantón de Carchi', 1, 19),
    (14, 'MONTÚFAR', 'Montúfar', 'Cantón de Carchi', 1, 19),
    (99, 'PARR-IB-URB', 'Alpachaca', 'Parroquia urbana de Ibarra', 1, 20),
    (100, 'PARR-IB-URB', 'Caranqui', 'Parroquia urbana de Ibarra', 1, 20),
    (101, 'PARR-IB-URB', 'El Sagrario', 'Parroquia urbana de Ibarra', 1, 20),
    (102, 'PARR-IB-URB', 'La Dolorosa de Priorato', 'Parroquia urbana de Ibarra', 1, 20),
    (103, 'PARR-IB-URB', 'San Francisco', 'Parroquia urbana de Ibarra', 1, 20),
    (104, 'PARR-IB-RURAL', 'Ambuquí', 'Parroquia rural de Ibarra', 1, 20),
    (105, 'PARR-IB-RURAL', 'Angochagua', 'Parroquia rural de Ibarra', 1, 20),
    (106, 'PARR-IB-RURAL', 'La Carolina', 'Parroquia rural de Ibarra', 1, 20),
    (107, 'PARR-IB-RURAL', 'La Esperanza', 'Parroquia rural de Ibarra', 1, 20),
    (108, 'PARR-IB-RURAL', 'Lita', 'Parroquia rural de Ibarra', 1, 20),
    (109, 'PARR-IB-RURAL', 'Salinas', 'Parroquia rural de Ibarra', 1, 20),
    (110, 'PARR-IB-RURAL', 'San Antonio de Ibarra', 'Parroquia rural de Ibarra', 1, 20),
    (111, 'PARR-OT-URB', 'Otavalo', 'Parroquia urbana de Otavalo', 1, 20),
    (112, 'PARR-OT-URB', 'San Pablo del Lago', 'Parroquia urbana de Otavalo', 1, 20),
    (113, 'PARR-OT-RURAL', 'Eugenio Espejo', 'Parroquia rural de Otavalo', 1, 20),
    (114, 'PARR-OT-RURAL', 'González Suárez', 'Parroquia rural de Otavalo', 1, 20),
    (115, 'PARR-OT-RURAL', 'San Rafael', 'Parroquia rural de Otavalo', 1, 20),
    (116, 'PARR-OT-RURAL', 'San Juan de Ilumán', 'Parroquia rural de Otavalo', 1, 20),
    (117, 'PARR-OT-RURAL', 'Dr. Miguel Egas Cabezas', 'Parroquia rural de Otavalo', 1, 20),
    (118, 'PARR-OT-RURAL', 'San José de Quichinche', 'Parroquia rural de Otavalo', 1, 20),
    (119, 'PARR-OT-RURAL', 'San Pedro de Pataquí', 'Parroquia rural de Otavalo', 1, 20),
    (120, 'PARR-OT-RURAL', 'Selva Alegre', 'Parroquia rural de Otavalo', 1, 20),
    (121, 'PARR-CO-URB', 'Cotacachi', 'Parroquia urbana de Cotacachi', 1, 20),
    (122, 'PARR-CO-RURAL', 'García Moreno', 'Parroquia rural de Cotacachi', 1, 20),
    (123, 'PARR-CO-RURAL', 'Quiroga', 'Parroquia rural de Cotacachi', 1, 20),
    (124, 'PARR-CO-RURAL', 'Apuela', 'Parroquia rural de Cotacachi', 1, 20),
    (125, 'PARR-CO-RURAL', 'Plaza Gutiérrez', 'Parroquia rural de Cotacachi', 1, 20),
    (126, 'PARR-CO-RURAL', 'Vacas Galindo', 'Parroquia rural de Cotacachi', 1, 20),
    (127, 'PARR-AA-URB', 'Atuntaqui', 'Parroquia urbana de Antonio Ante', 1, 20),
    (128, 'PARR-AA-RURAL', 'Andrade Marín', 'Parroquia rural de Antonio Ante', 1, 20),
    (129, 'PARR-AA-RURAL', 'Imbaya', 'Parroquia rural de Antonio Ante', 1, 20),
    (130, 'PARR-AA-RURAL', 'Natabuela', 'Parroquia rural de Antonio Ante', 1, 20),
    (131, 'PARR-AA-RURAL', 'Chaltura', 'Parroquia rural de Antonio Ante', 1, 20),
    (132, 'PARR-AA-RURAL', 'San Roque', 'Parroquia rural de Antonio Ante', 1, 20),
    (133, 'PARR-PI-URB', 'Pimampiro', 'Parroquia urbana de Pimampiro', 1, 20),
    (134, 'PARR-PI-RURAL', 'Chugá', 'Parroquia rural de Pimampiro', 1, 20),
    (135, 'PARR-PI-RURAL', 'Mariano Acosta', 'Parroquia rural de Pimampiro', 1, 20),
    (136, 'PARR-PI-RURAL', 'San Francisco de Sigsipam', 'Parroquia rural de Pimampiro', 1, 20),
    (137, 'PARR-UR-URB', 'Urcuquí', 'Parroquia urbana de Urcuquí', 1, 20),
    (138, 'PARR-UR-RURAL', 'Pablo Arenas', 'Parroquia rural de Urcuquí', 1, 20),
    (139, 'PARR-UR-RURAL', 'San Blas', 'Parroquia rural de Urcuquí', 1, 20),
    (140, 'PARR-UR-RURAL', 'Tahuando', 'Parroquia rural de Urcuquí', 1, 20),
    (141, 'PARR-TU-URB', 'Tulcán', 'Parroquia urbana de Tulcán', 1, 20),
    (142, 'PARR-TU-RURAL', 'El Carmelo', 'Parroquia rural de Tulcán', 1, 20),
    (143, 'PARR-TU-RURAL', 'Huaca', 'Parroquia rural de Tulcán', 1, 20),
    (144, 'PARR-TU-RURAL', 'Julio Andrade', 'Parroquia rural de Tulcán', 1, 20),
    (145, 'PARR-TU-RURAL', 'La Libertad', 'Parroquia rural de Tulcán', 1, 20),
    (146, 'PARR-TU-RURAL', 'Maldonado', 'Parroquia rural de Tulcán', 1, 20),
    (147, 'PARR-TU-RURAL', 'Pioter', 'Parroquia rural de Tulcán', 1, 20),
    (148, 'PARR-TU-RURAL', 'Tufiño', 'Parroquia rural de Tulcán', 1, 20),
    (149, 'PARR-TU-RURAL', 'Urbanización Nueva Loja', 'Parroquia rural de Tulcán', 1, 20),
    (150, 'PARR-BO-URB', 'Bolívar', 'Parroquia urbana de Bolívar', 1, 20),
    (151, 'PARR-BO-RURAL', 'Garcia Moreno', 'Parroquia rural de Bolívar', 1, 20),
    (152, 'PARR-BO-RURAL', 'Los Andes', 'Parroquia rural de Bolívar', 1, 20),
    (153, 'PARR-BO-RURAL', 'Monte Olivo', 'Parroquia rural de Bolívar', 1, 20),
    (154, 'PARR-BO-RURAL', 'San Vicente de Pusir', 'Parroquia rural de Bolívar', 1, 20),
    (155, 'PARR-ES-URB', 'El Ángel', 'Parroquia urbana de Espejo', 1, 20),
    (156, 'PARR-ES-RURAL', 'La Libertad', 'Parroquia rural de Espejo', 1, 20),
    (157, 'PARR-ES-RURAL', 'San Isidro', 'Parroquia rural de Espejo', 1, 20),
    (158, 'PARR-ES-RURAL', 'El Goaltal', 'Parroquia rural de Espejo', 1, 20),
    (159, 'PARR-MI-URB', 'Mira', 'Parroquia urbana de Mira', 1, 20),
    (160, 'PARR-MI-RURAL', 'Concepción', 'Parroquia rural de Mira', 1, 20),
    (161, 'PARR-MI-RURAL', 'Jacinto Jijón y Caamaño', 'Parroquia rural de Mira', 1, 20),
    (162, 'PARR-MI-RURAL', 'Juan Montalvo', 'Parroquia rural de Mira', 1, 20),
    (163, 'PARR-MO-URB', 'San Gabriel', 'Parroquia urbana de Montúfar', 1, 20),
    (164, 'PARR-MO-RURAL', 'Cristóbal Colón', 'Parroquia rural de Montúfar', 1, 20),
    (165, 'PARR-MO-RURAL', 'Chitán de Navarretes', 'Parroquia rural de Montúfar', 1, 20),
    (166, 'PARR-MO-RURAL', 'Fernández Salvador', 'Parroquia rural de Montúfar', 1, 20),
    (167, 'PARR-MO-RURAL', 'La Paz', 'Parroquia rural de Montúfar', 1, 20),
    (168, 'VIVIENDA', 'Casa', 'Tipo de vivienda: Casa', 1, 22),
    (169, 'VIVIENDA', 'Departamento', 'Tipo de vivienda: Departamento', 1, 22),
    (170, 'VIVIENDA', 'Cuartos', 'Tipo de vivienda: Cuartos', 1, 22),
    (171, 'VIVIENDA', 'Mediagua', 'Tipo de vivienda: Mediagua', 1, 22),
    (172, 'TECHO', 'Losa', 'Tipo de techo: Losa', 1, 23),
    (173, 'TECHO', 'Eternit', 'Tipo de techo: Eternit', 1, 23),
    (174, 'TECHO', 'Zinc', 'Tipo de techo: Zinc', 1, 23),
    (175, 'TECHO', 'Teja', 'Tipo de techo: Teja', 1, 23),
    (176, 'PARED', 'Hormigón', 'Tipo de pared: Hormigón', 1, 24),
    (177, 'PARED', 'Ladrillo', 'Tipo de pared: Ladrillo', 1, 24),
    (178, 'PARED', 'Bloque', 'Tipo de pared: Bloque', 1, 24),
    (179, 'PARED', 'Adobe', 'Tipo de pared: Adobe', 1, 24),
    (180, 'PARED', 'Madera', 'Tipo de pared: Madera', 1, 24),
    (181, 'PISO', 'Duela', 'Tipo de piso Duela', 1, 25),
    (182, 'PISO', 'Hormigón', 'Tipo de piso Hormigón', 1, 25),
    (183, 'PISO', 'Tabla', 'Tipo de piso Tabla', 1, 25),
    (184, 'PISO', 'Céramica', 'Tipo de piso Céramica', 1, 25),
    (185, 'PISO', 'Tierra', 'Tipo de piso Tierra', 1, 25),
    (186, 'PISO', 'Ladrillo', 'Tipo de piso Ladrillo', 1, 25),
    (187, 'COMB-COCINA', 'Gas', 'Combustible de cocina: Gas', 1, 26),
    (188, 'COMB-COCINA', 'Electricidad', 'Combustible de cocina: Electricidad', 1, 26),
    (189, 'COMB-COCINA', 'Leña', 'Combustible de cocina: Leña', 1, 26),
    (190, 'COMB-COCINA', 'No cocina', 'No utiliza cocina', 1, 26),
    (191, 'SERV-HIG', 'Alcantarillado', 'Servicio higiénico: Alcantarillado', 1, 27),
    (192, 'SERV-HIG', 'Pozo séptico', 'Servicio higiénico: Pozo séptico', 1, 27),
    (193, 'SERV-HIG', 'Pozo ciego', 'Servicio higiénico: Pozo ciego', 1, 27),
    (194, 'SERV-HIG', 'Letrina', 'Servicio higiénico: Letrina', 1, 27),
    (195, 'SERV-HIG', 'No tiene', 'No cuenta con servicio higiénico', 1, 27),
    (196, 'ALOJAMIENTO', 'Propia y esta pagada', 'Vivienda propia totalmente pagada', 1, 28),
    (197, 'ALOJAMIENTO', 'Propia (regalada, heredad', 'Vivienda propia por herencia, regalo o posesión', 1, 28),
    (198, 'ALOJAMIENTO', 'Prestada', 'Vivienda prestada por familiares u otros', 1, 28),
    (199, 'ALOJAMIENTO', 'Propia y esta pagadando', 'Vivienda propia en proceso de pago', 1, 28),
    (200, 'ALOJAMIENTO', 'Arrienda', 'Vivienda alquilada', 1, 28),
    (201, 'ALOJAMIENTO', 'Anticresis', 'Vivienda bajo contrato de anticresis', 1, 28),
    (202, 'SERV-AGUA', 'Red Pública', 'Abastecimiento de agua mediante red pública', 1, 29),
    (203, 'SERV-AGUA', 'Pozo', 'Abastecimiento de agua mediante pozo propio o comunitario', 1, 29),
    (204, 'SERV-AGUA', 'Río o vertiente, acequia ', 'Agua proveniente de fuentes naturales como ríos, vertientes, acequias o canales', 1, 29),
    (205, 'SERV-AGUA', 'Carro repartidor', 'Abastecimiento de agua mediante reparto en carro', 1, 29),
    (206, 'SERV-AGUA', 'Otros', 'Otro tipo de abastecimiento de agua no especificado', 1, 29),
    (217, 'ELM-BAS', 'Carro recolector', 'Eliminación de basura mediante carro recolector municipal o privado', 1, 30),
    (218, 'ELM-BAS', 'Lo botan a la calle, quebrada o rio', 'La basura es arrojada a lugares inadecuados como calles, quebradas o ríos', 1, 30),
    (219, 'ELM-BAS', 'La queman', 'La basura es eliminada quemándola', 1, 30),
    (220, 'ELM-BAS', 'Reciclan/entierran', 'Reciclaje o entierro de la basura en el terreno', 1, 30),
    (221, 'ELM-BAS', 'Composta', 'La basura orgánica es convertida en compostaje', 1, 30),
    (222, 'LUG-FREC-COMPRA', 'Supermercado', 'Compras frecuentes en supermercados grandes o cadenas comerciales', 1, 31),
    (223, 'LUG-FREC-COMPRA', 'Mercados', 'Compras frecuentes en mercados municipales o populares', 1, 31),
    (224, 'LUG-FREC-COMPRA', 'Ferias', 'Compras frecuentes en ferias ocasionales o ambulantes', 1, 31),
    (225, 'LUG-FREC-COMPRA', 'Micromercados', 'Compras frecuentes en minimercados o locales pequeños', 1, 31),
    (226, 'LUG-FREC-COMPRA', 'Tienda del barrio', 'Compras frecuentes en tiendas pequeñas del vecindario', 1, 31),
    (227, 'LUG-FREC-COMPRA', 'Trueques', 'Intercambio de productos mediante trueques', 1, 31),
    (228, 'LUG-FREC-COMPRA', 'Otros', 'Otros lugares no especificados donde se realizan compras', 1, 31),
    (229, 'TIP-VEHICULOS', 'Carro', 'Vehículo tipo automóvil con motor de combustión o eléctrico', 1, 32),
    (230, 'TIP-VEHICULOS', 'Moto', 'Motocicleta de combustión interna', 1, 32),
    (231, 'TIP-VEHICULOS', 'Pasola a gasolina', 'Scooter o pasola que funciona con gasolina', 1, 32),
    (232, 'TIP-VEHICULOS', 'Moto o pasola eléctrica', 'Vehículo de dos ruedas impulsado por energía eléctrica', 1, 32),
    (233, 'EST-TRANSPORTE', 'Bueno', 'Estado del medio de transporte: bueno', 1, 33),
    (234, 'EST-TRANSPORTE', 'Regular', 'Estado del medio de transporte: regular', 1, 33),
    (235, 'EST-TRANSPORTE', 'Malo', 'Estado del medio de transporte: malo', 1, 33),
    (236, 'ETNIA', 'Mestizo', 'Mestizo', 1, 34),
    (237, 'ETNIA', 'Afroecuatoriano', 'Afroecuatoriano', 1, 34),
    (238, 'ETNIA', 'Indígena', 'Indígena', 1, 34),
    (239, 'ETNIA', 'Montubio', 'Montubio', 1, 34),
    (240, 'ETNIA', 'Blanco', 'Blanco', 1, 34),
    (241, 'ETNIA', 'Otro', 'Otro', 1, 34),
    (242, 'GENERO', 'Masculino', 'Masculino', 1, 35),
    (243, 'GENERO', 'Femenino', 'Femenino', 1, 35),
    (244, 'GENERO', 'Otro', 'Otro', 1, 35),
    (245, 'GENERO', 'Prefiero no decirlo', 'Prefiero no decirlo', 1, 35),
    (246, 'NIV_EDUC', 'Primaria', 'Primaria', 1, 36),
    (247, 'NIV_EDUC', 'Secundaria', 'Secundaria', 1, 36),
    (248, 'NIV_EDUC', 'Bachillerato', 'Bachillerato', 1, 36),
    (249, 'NIV_EDUC', 'Universitaria', 'Universitaria', 1, 36),
    (250, 'NIV_EDUC', 'Ninguna', 'Ninguna', 1, 36),
    (251, 'EST-CIV', 'Soltero/a', 'Soltero/a', 1, 37),
    (252, 'EST-CIV', 'Casado/a', 'Casado/a', 1, 37),
    (253, 'EST-CIV', 'Unión libre', 'Unión libre', 1, 37),
    (254, 'EST-CIV', 'Separado/a', 'Separado/a', 1, 37),
    (255, 'EST-CIV', 'Viudo/a', 'Viudo/a', 1, 37),
    (258, 'TIP-VEHICULOS', 'Ninguno', 'Ninguno', 1, 32),
    (259, 'EST-TRANSPORTE', 'Ninguno', 'Ninguno', 1, 33)
])


# Crear la tabla tbl_datos_generales_parentesco
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_datos_generales_parentesco (
    id_datos_generales_parentesco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_datos_parentescos INTEGER NOT NULL,
    id_datos_generales INTEGER NOT NULL,
    datos_generales_parentesco_estado INTEGER DEFAULT 1,
    FOREIGN KEY (id_datos_parentescos) REFERENCES tbl_datos_parentesco(id_datos_parentesco),
    FOREIGN KEY (id_datos_generales) REFERENCES tbl_datos_generales(id_datos_generales)
);
""")

# Crear la tabla tbl_datos_parentesco
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_datos_parentesco (
    id_datos_parentesco INTEGER PRIMARY KEY AUTOINCREMENT,
    datos_parentesco_nombres TEXT,
    datos_parentesco_apellidos TEXT,
    datos_parentesco_documento TEXT,
    datos_parentesco_celular_telf TEXT,
    datos_parentesco_etnia INTEGER,
    datos_parentesco_genero INTEGER,
    datos_parentesco_nivel_educacion INTEGER,
    datos_parentesco_fecha_de_nacimiento TEXT,
    datos_parentesco_edad INTEGER,
    datos_parentesco_estado_civil INTEGER,
    datos_parentesco_discapacidad INTEGER,
    datos_parentesco_enfermedad_catastrofica TEXT,
    datos_parentesco_trabaja TEXT,
    datos_parentesco_ocupacion TEXT,
    datos_parentesco_ingreso_mensual REAL,
    datos_parentesco_parentesco TEXT,
    datos_parentesco_estado INTEGER DEFAULT 1
);
""")

# Crear la tabla tbl_funcionalidad
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_funcionalidad (
    id_funcionalidad INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionalidad_nombre_funcion TEXT,
    funcionalidad_url TEXT,
    funcionalidad_estado INTEGER,
    funcionalidad_created_at TEXT DEFAULT (datetime('now','localtime'))
);
""")

# Insertar los datos de ejemplo
funcionalidades = [
    (1, 'Cerrar sesión', '/logout', 1, '2025-07-21 16:07:36'),
    (2, 'Formulario de datos generales', '/formGeneralInformation', 1, '2025-07-21 16:07:36'),
    (3, 'Obtener provincias', '/getProvinces', 1, '2025-07-21 16:07:36'),
    (4, 'Obtener ciudades', '/getCities', 1, '2025-07-21 16:07:36'),
    (5, 'Obtener parroquias', '/getParishes', 1, '2025-07-21 16:07:36'),
    (6, 'Obtener tipos de vivienda', '/getTypesHousing', 1, '2025-07-21 16:07:36'),
    (7, 'Obtener tipos de techo', '/getRoofTypes', 1, '2025-07-21 16:07:36'),
    (8, 'Obtener tipos de pared', '/getWallTypes', 1, '2025-07-21 16:07:36'),
    (9, 'Obtener tipos de piso', '/getFloorTypes', 1, '2025-07-21 16:07:36'),
    (10, 'Obtener tipos de combustible cocina', '/getCookingFuel', 1, '2025-07-21 16:07:36'),
    (11, 'Obtener servicios higiénicos', '/getHygienicService', 1, '2025-07-21 16:07:36'),
    (12, 'Vivienda o alojamiento', '/getHousing', 1, '2025-07-21 16:07:36'),
    (13, 'Obtener servicios de agua', '/getWaterServices', 1, '2025-07-21 16:07:36'),
    (14, 'Obtener eliminación de basura', '/getGarbageRemoval', 1, '2025-07-21 16:07:36'),
    (15, 'Obtener lugares frecuentes de compra', '/getFrequentShopPlaces', 1, '2025-07-21 16:07:36'),
    (16, 'Obtener tipo de vehículos', '/getVehiclesTypes', 1, '2025-07-21 16:07:36'),
    (17, 'Obtener estado de transporte', '/getTransportStatus', 1, '2025-07-21 16:07:36'),
    (18, 'Insertar datos generales y parentesco', '/insertGeneralInformation', 1, '2025-07-21 16:07:36'),
    (19, 'Obtener lista de etnias', '/getEthnicity', 1, '2025-07-21 16:07:36'),
    (20, 'Obtener lista de géneros', '/getGenders', 1, '2025-07-21 16:07:36'),
    (21, 'Obtener niveles de educación', '/getEducationLevel', 1, '2025-07-21 16:07:36'),
    (22, 'Obtener lista de estado civil', '/getMaritalStatus', 1, '2025-07-21 16:07:36'),
    (23, 'Datos registrados', '/informationRecords', 1, '2025-07-21 16:07:36'),
    (24, 'Vista para modificar perfil personal', '/profile', 1, '2025-07-21 16:07:36'),
    (25, 'Obtener parentescos', '/getRelationShipId', 1, '2025-07-21 16:07:36'),
    (26, 'Dar de baja registro de información general con parentescos', '/deleteGeneralInformationRecord', 1, '2025-07-21 16:07:36'),
    (27, 'Actualizar perfil', '/updateProfile', 1, '2025-07-21 16:07:36'),
    (28, 'Actualizar contraseña', '/updateProfilePassword', 1, '2025-07-21 16:07:36'),
    (29, 'Exportar excel', '/exportExcel', 1, '2025-07-21 16:07:36'),
    (30, 'Actualizar rol de usuario', '/updateRolUser', 1, '2025-07-21 16:07:36'),
    (31, 'Obtener documento de usuario', '/getDocument', 1, '2025-07-21 16:07:36'),
    (32, 'Obtener roles', '/getRoles', 1, '2025-07-21 16:07:36')
]

cursor.executemany("""
INSERT OR IGNORE INTO tbl_funcionalidad (
    id_funcionalidad, funcionalidad_nombre_funcion, funcionalidad_url, funcionalidad_estado, funcionalidad_created_at
) VALUES (?, ?, ?, ?, ?)
""", funcionalidades)

# tbl_rol
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_rol (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    rol_nombre TEXT,
    rol_estado INTEGER,
    rol_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.executemany("""
INSERT OR IGNORE INTO tbl_rol (id_rol, rol_nombre, rol_estado, rol_created_at)
VALUES (?, ?, ?, ?)
""", [
    (1, 'Administrador', 1, '2025-06-15 22:39:11'),
    (2, 'Empleado', 1, '2025-06-15 22:39:11'),
    (3, 'Gestión Operativa', 1, '2025-07-21 16:12:02'),
    (4, 'Gestión Social', 1, '2025-07-21 16:12:02')
])

# tbl_rol_access
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_rol_access  (
    id_principal_rol_access INTEGER PRIMARY KEY AUTOINCREMENT,
    id_rol INTEGER NOT NULL,
    id_funcionalidad INTEGER NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES tbl_rol(id_rol),
    FOREIGN KEY (id_funcionalidad) REFERENCES tbl_funcionalidad(id_funcionalidad)
)
""")
# tbl_users

cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_users (
    id_users INTEGER PRIMARY KEY AUTOINCREMENT,
    users_nombre TEXT,
    users_nombreUsuario TEXT NOT NULL,
    users_apellido TEXT,
    users_cedula TEXT,
    users_email TEXT,
    users_telefono TEXT,
    users_fecha_de_nacimiento DATE NOT NULL,
    users_genero TEXT,
    users_contrasenia TEXT NOT NULL,
    users_estado INTEGER,
    users_activation_token TEXT,
    users_reset_token TEXT,
    users_reset_token_expires_at DATETIME,
    users_updated_at DATETIME,
    users_created_at DATETIME DEFAULT (CURRENT_TIMESTAMP)
)
""")

# tbl_user_rol

cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_user_rol (
    id_users_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    id_users INTEGER NOT NULL,
    id_rol INTEGER NOT NULL,
    user_rol_estado INTEGER,
    user_rol_created_at DATETIME DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (id_users) REFERENCES tbl_users(id_users),
    FOREIGN KEY (id_rol) REFERENCES tbl_rol(id_rol)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_datos_generales_PRUEBA (
    id_datos_generales INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,

    datos_cedula_voluntario TEXT NOT NULL,

    datos_parentesco_id INTEGER,
    datos_provincia INTEGER,
    datos_canton TEXT,
    datos_tipo_parroquias TEXT,
    datos_parroquias INTEGER,
    datos_comunidades TEXT,
    datos_barrios TEXT,

    datos_tipo_viviendas INTEGER,
    datos_techos INTEGER,
    datos_paredes INTEGER,
    datos_pisos INTEGER,
    datos_cuarto INTEGER,

    datos_combustibles_cocina INTEGER,
    datos_servicios_higienicos INTEGER,

    datos_viviendas INTEGER,
    datos_pago_vivienda REAL,

    datos_agua INTEGER,
    datos_pago_agua REAL,

    datos_pago_luz INTEGER,
    datos_cantidad_luz REAL,

    datos_internet INTEGER,
    datos_pago_internet REAL,

    datos_tv_cable INTEGER,
    datos_tv_pago REAL,

    datos_eliminacion_basura INTEGER,
    datos_lugares_mayor_frecuencia_viveres INTEGER,
    datos_gastos_viveres_alimentacion INTEGER,

    datos_medio_transporte TEXT,
    datos_estado_transporte TEXT,

    datos_terrenos INTEGER,
    datos_celular INTEGER,
    datos_cantidad_celulare INTEGER,
    datos_plan_celular INTEGER,

    datos_observacion TEXT,
    datos_resultado TEXT,
    datos_resultado_sistema TEXT,

    datos_estado INTEGER DEFAULT 1,
    datos_consentimiento INTEGER DEFAULT 1,

    datos_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    sincronizado INTEGER DEFAULT 0

);
""")


# cursor.execute("""
# ALTER TABLE tbl_datos_generales
# ADD COLUMN datos_cedula_voluntario TEXT NOT NULL DEFAULT '';
# """)

conn.commit()
conn.close()

print("✔ Todas las tablas creadas correctamente.")

