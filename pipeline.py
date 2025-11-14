creemos el pipeline por partes

Fase 1: Configuración (El "Encabezado")

Imports: Copia todos los import de todas tus celdas y ponlos juntos al inicio del script.

Constantes: Define todas tus constantes globales. Esto incluye rutas de archivos (BASE_EXPORT_DIR, PLANIFICACION_FILE, etc.), hiperparámetros (HPARAMS_CLASIFICADOR_BINARIO), y umbrales (UMBRAL_MINIMO_DATOS, CLUSTERS_A_EXCLUIR)

este es todo el codigo:

### Creacion de Modulos.py


%%writefile normalizacion.py

# Ejemplo de uso

#ventas['producto_normalizado'] = ventas['Producto'].apply(normalizar_texto)

import re

import pandas as pd

from unidecode import unidecode

import unicodedata

def normalizar_texto(texto):

    """

    Normaliza texto para mejorar matching

    """

    if pd.isna(texto):

        return ""


    texto = str(texto).lower().strip()

    # Normalizar espacios múltiples

    texto = re.sub(r'\s+', ' ', texto)

    # 1. Normalizar unicode (ángulo → angulo)

    texto = unicodedata.normalize('NFKD', str(texto))

    texto = ''.join([c for c in texto if not unicodedata.combining(c)])

    # Normalizar comas y puntos

    texto = re.sub(r'(\d)[.,](\d)', r'\1.\2', texto)  # 2,4 → 2.4

    texto = re.sub(r'0+(\d{1,2}\s*mm)', r'\1', texto)  # 035mm → 35mm

    # Normalizar unidades

    texto = texto.replace('mts', 'm').replace('mt', 'm').replace('ml', 'm')

    texto = texto.replace('kl', 'kg').replace('kgs', 'kg')

    texto = texto.replace('mm.', 'mm').replace('m.', 'm')

    # 4. Limpiar puntuación

    texto = re.sub(r'[^\w\s.]', '', texto)

    texto = re.sub(r'\.{2,}', '.', texto)


    return texto


# Creamos archivo de módulo, define la fuente de verdad (las categorías y sus palabras clave).

%%writefile categorias.py

def crear_categorias_completo():

    """

    Carga el catálogo maestro desde el documento proporcionado

    """

    categorias = {



        'Perfiles Estructurales': ['pgc-', 'pgu-', 'pgo-', 'perfil estructural', 'perfil pgc', 'perfil pgu', 'pgc', 'Perfil PGC'],

        'Perfiles CMC': ['cmc perfil', 'cmc montante', 'cmc solera', 'cmc angulo'],

        'Perfiles ECO': ['eco perfil', 'eco montante', 'eco solera', 'eco omega', 'eco angulo', 'eco', 'eco perfil omega'],

        'Perfiles de Tabiquería': ['montante de','solera', 'solera de', 'perfil omega', 'angulo interno', 'perfil esquinero', 'esquinero de', 'esquineros', 'esquinero','esquiner'], # Añadido para Perfiles Esquinero

        'Cielos y Revestimientos': ['placa pvc', 'placa de pvc', 'placa pvc brasilera', 'brasilera', 'revestimiento', 'perimetral acustica', 'placa pvc brasilera', 'cielo pvc', 'placa pvc', 'placa de pvc', 'perimetral pvc', 'perfil desmontable', 'central de', 'transversal de', 'transversal', 'placa radar', 'radar', 'conector', 'perimetral de', 'union h', 'buña', 'buna', 'placa fibra mineral', 'usg radar', 'placa encore', 'placa gypsum', 'placa pebbled', 'placa plus desing', 'placa de aluminio', 'perimetral pvc', 'core'], # Añadido para placas acústicas y perfiles de cielo

        'Placas de Yeso': ['placa knauf', 'plus vinil', 'placa plus vinil', 'yeso','plussvinil','placa de yeso', 'placa desmontable usg', 'placa gyplac verde', 'placa sp glass', 'placa gyplac roja', 'placa plus vinyl', 'knauf sp glass', 'knauf', 'plus vinil', 'placa plus vinil'], # Añadido para placas especiales y plus vinyl

        'Placas Cementicias': ['placa cementicia', 'placa aquapanel', 'placa durock', 'placa de fibrocemento'], # Añadido para fibrocemento

        'Tableros': ['tablero osb','OSB'],

        'Fijaciones': ['tornillo', 'perfnos', 'expansion', 't1', 't2', 'perno', 'tarugo', 'anclaje', 'gancho', 'perno de expansion', 'perno de anclaje', 'perno de exoancion', 'pernos de anclaje', 't1 punta aguja', 't2 punta de broca'], # Añadido para Pernos y Tornillos T1/T2

        'Aislantes Térmicos': ['lana de vidrio', 'rolac', 'membrana', 'fieltro', 'aislante', 'fibra de vidrio'], # Añadido para fibra de vidrio

        'Masillas y Acabados': ['masilla','cinta','cints', 'cantonera', 'junta', 'banda acustica', 'impermeabilizante', 'sikalastic'], # Añadido para Sika/Impermeabilizantes

        'Herramientas': ['espatula', 'espatulas', 'disco de corte', 'disco', 'corte', 'tijera de aviacion', 'tijera', 'nivel laser', 'nivel de mano', 'nivel', 'espatula', 'cierra para', 'cierra', 'sierra', 'cutter', 'cizalla', 'charola', 'bandeja de plastico', 'estilete', 'cinturon porta', 'cinturon', 'porta herramientas', 'bandeja', 'dados magneticos', 'plstico'], # Añadido para todas las herramientas

        'Materiales Estructurales': ['fierro corrugado', 'hierro corrugado', 'fierro de construccion'], # Añadido para Fierro de Construcción

    }

    return categorias


# Creamos archivo de módulo

%%writefile catalogo_productos.py

def crear_catalogo_completo():

    catalogo_dict = {

        # Perfiles Montante 35mm

        "Perfil Montante de 35 mm x 2.40": "Perfil Montante de 35 mm x 2.40 m x 0,50 mm",

        "Montante de 35 mm x 2,40 m x 0,50": "Perfil Montante de 35 mm x 2.40 m x 0,50 mm",

        "Perfil Montante de 35 mm x 2,40 m": "Perfil Montante de 35 mm x 2.40 m x 0,50 mm",

        "Perfil Montante de 35 mm x 2.40 x 0,5 mm": "Perfil Montante de 35 mm x 2.40 m x 0,50 mm",

        " Montante de 35 mm x 3,00 m.": "Perfil Montante de 35 mm x 3,00 m x 0,50 mm",

        "montante de 35 mm x 240 m x 0,50": "Perfil Montante de 35 mm x 2.40 m x 0,50 mm",

        "Montante de 35 mm x 2,40 m.": "Perfil Montante de 35 mm x 2.40 m x 0,50 mm",

        "eco montante de 35 mm x 3,00 m x 0,42 mm": "Perfil Montante de 35 mm x 3,00 m x 0,42 mm",

        "Ecoperfil solera de 35 mm x 3,00 m x 0,42 mm": "Perfil Montante de 35 mm x 3,00 m x 0,42 mm",

        "perfil montante eco de 3,00 m.": "Perfil Montante de 35 mm x 3,00 m x 0,50 mm",

        "Eco Perfil Montante de 35 mm x 2.40": "Perfil Montante de 35 mm x 3,00 m x 0,50 mm",

        "ECO Montante de 35 mm x 3,00 m.": "Perfil Montante de 35 mm x 3,00 m x 0,50 mm",

        "Eco montante de 3,00 m": "Perfil Montante de 35 mm x 3,00 m x 0,50 mm",


        # Perfiles Montante 70mm

        "Montante de 70 mm x 2,40 m x 0,50 mm": "Perfil Montante de 70 mm x 2.40 m x 0,50 mm",

        "Montante de 70 mm x 2,40 m.": "Perfil Montante de 70 mm x 2.40 m x 0,50 mm",

        "Perfil Montante de 70 mm x 2,40 ml x 0,50 mm": "Perfil Montante de 70 mm x 2.40 m x 0,50 mm",

        " Montante de 70 mm x 3,00 m.": "Perfil Montante de 70 mm x 3,00 m x 0,50 mm",

        "Perfil Ecomontante de 70 mm x 3,00 m": "Perfil Montante de 70 mm x 3,00 m x 0,50 mm",

        "ECO Montante de 70 mm x 3,00 m.": "Perfil Montante de 70 mm x 3,00 m x 0,50 mm",

        "Perfil ecomontante de 70 mm x 3,00 m": "Perfil Montante de 70 mm x 3,00 m x 0,50 mm",

        "Perfil liviano Eco Montante de 70 mm x 3,00 m.": "Perfil Montante de 70 mm x 3,00 m x 0,50 mm",

        "Eco perfil montante de 70 mm x 2,40 m x 0,50 mm": "Perfil Montante de 70 mm x 3,00 m x 0,50 mm",

        # Soleras

        "Solera de 35 x 2,40": "Perfil Solera de 35 mm x 2.40 m x 0,50 mm",

        "Solera de 70 x 2,40": "Perfil Solera de 70 mm x 2.40 m x 0,50 mm",

        " Solera de 70 mm x 2,40 m.": "Perfil Solera de 70 mm x 2.40 m x 0,50 mm",

        "Perfil solera de 70 mm x 2,40 m x 0,50 m":"Perfil Solera de 70 mm x 2.40 m x 0,50 mm",

        "Perfil solera de 70 mm x 2,40 m x 0,5 mm":"Perfil Solera de 70 mm x 2.40 m x 0,50 mm",

        "Perfil solera 70 mm x 2,40 m": "Perfil Solera de 70 mm x 2.40 m x 0,50 mm",

        "Perfil solera de 70 mm x 2,40": "Perfil Solera de 70 mm x 2.40 m x 0,50 mm",

        "Solera de 35 mm x 2,40 m. x 0,5": "Perfil Solera de 35 mm x 2.40 m x 0,50 mm",

        "Solera de 35 mm x 2,40 m. x 0,5 mm": "Perfil Solera de 35 mm x 2.40 m x 0,50 mm",

        "Eco perfil solera de 35 mm x 3,00 m": "Perfil Solera de 35 mm x 3,00 m x 0,50 mm",

        "eco perfil solera de 35 mm x 3,00": "Perfil Solera de 35 mm x 3,00 m x 0,50 mm",

        "Eco perfil Solera de 35 mm x 3,00 m": "Perfil Solera de 35 mm x 3,00 m x 0,50 mm",

        "Eco solera de 35 mm x 3,00 m x 0,42": "Perfil Solera de 35 mm x 3,00 m x 0,42 mm",

        "ECO Solera de 35 mm x 3 m.": "Perfil Solera de 35 mm x 3,00 m x 0,50 mm",

        "ECO Solera de 70 mm x 3 m.": "Perfil Solera de 70 mm x 3,00 m x 0,50 mm",

        "Perfil ecosolera de de 70 mm": "Perfil Solera de 70 mm x 3,00 m x 0,50 mm",

        "Perfil Ecosolera de 70 mm x 3,00 m x 0,42 mm": "Perfil Solera de 70 mm x 3,00 m x 0,42 mm",

        "ECO Perfil Solera de 70 mm x 3,00 ml x 0,42 mm": "Perfil Solera de 70 mm x 3,00 m x 0,42 mm",

        "Eco solera de 35 mm de 35 mm x 3,00 m x 0,42": "Perfil Solera de 35 mm x 3,00 m x 0,42 mm",

        "Eco perfil solera de 70 mm x 3,00 m" : "Perfil Solera de 70 mm x 3,00 m x 0,50 mm",

        # Omegas

        "Omega Liviano de 22 x 3.60m": "Perfil Omega Liviano de 22 mm x 3.60 m x 0,50 mm",

        " Omega Liviano de 22 x 3 m.": "Perfil Omega Liviano de 22 mm x 3,00 m x 0,50 mm",

        " Omega Liviano de 22 x 3,60 m.": "Perfil Omega Liviano de 22 mm x 3.60 m x 0,50 mm",

        "Perfil Omega de 0,5 mm x 3,60 m": "Perfil Omega Liviano de 22 mm x 3.60 m x 0,50 mm",

        "Perfil omega de 3,60 ml x 0,5 mm": "Perfil Omega Liviano de 22 mm x 3.60 m x 0,50 mm",

        "Perfil Omega de 3,60 m x 0,5 mm": "Perfil Omega Liviano de 22 mm x 3.60 m x 0,50 mm",

        "perfil omega de 3,60 m  X 0,5 MM": "Perfil Omega Liviano de 22 mm x 3.60 m x 0,50 mm",

        "Eco perfil omega de 3,00 m": "Perfil Omega de 3,00 m x 0,50 mm",

        "Eco perfil omega de 3,00 ml": "Perfil Omega de 3,00 m x 0,50 mm",

        "eco perfil omega de 3,00 ml x 0,42 mm": "Perfil Omega de 3,00 m x 0,50 mm",

        "Eco Perfil omega de 3,00 ml": "Perfil Omega de 3,00 m x 0,50 mm",

        "ECO Omega Liviano de 22 x 3 m.": "Perfil Omega de 3,00 m x 0,50 mm",

        "Eco perfil omega de 3,00":"Perfil Omega de 3,00 m x 0,50 mm",

        "Eco perfil omega liviano": "Perfil Omega de 3,00 m x 0,50 mm",

        # Ángulos Internos

        "Perfil angulo interno de 3,00 ml x 0,50 mm": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "perfil angulo interno de 3,00 X 0,5 MM": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Perfil liviano Angulo interno de 3,00 m": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Angulo interno de 3,00 m": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Angulo Interno de 35 mm x 3,00 m.": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Perfil angulo interno de 25 mm x 3,00 ml": "Perfil Angulo Interno de 25 mm x 3,00 m x 0,50 mm",

        " Angulo Interno de 35 mm x 3,00 m.": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Perfil angulo interno de 3,00 ml": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Angulo Interno de 35 mm x 3,00 m": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "angulo interno de 35 mm x 3,00 m": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "perfil angulo interno de 3,00 ml x 0,42 mm": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,42 mm",

        "Eco angulo interno de 3,00 m": "ECO Perfil Angulo Interno de 35 mm x 3,00 ml x 0,50 mm",

        "eco perfil angulo interno de 3,00 ml": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "perfil angulo interno eco de 3,00 m": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Perfil angulo interno ECO de 3,00 m": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Eco Perfil Angulo interno de 3,00 ml x 0,42 mm": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,42 mm",

        "Ecoperfil angulo interno": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        "Perfil eco angulo de 3,00": "Perfil Angulo Interno de 35 mm x 3,00 m x 0,50 mm",

        # ECO Perfiles - Montantes






        # ECO Perfiles - Soleras



        # ECO Perfiles - Omega


        # ECO Perfiles - Ángulos


        # CMC Perfiles - Montantes

        "CMC PERFIL MONTANTE 34 DE 3 Mts": "CMC Perfil Montante de 34 mm x 3,00 ml x 0,42 mm",

        "CMC Perfil Montante de 34 mm x 3,00 m.": "CMC Perfil Montante de 34 mm x 3,00 ml x 0,42 mm",

        "CMC Montante de 34 mm x 3,00 m": "CMC Perfil Montante de 34 mm x 3,00 ml x 0,42 mm",

        "cmc perfil montante 34 de 3 mts": "CMC Perfil Montante de 34 mm x 3,00 ml x 0,42 mm",

        "CMC Montante 34 x 3,00 mts": "CMC Perfil Montante de 34 mm x 3,00 ml x 0,42 mm",


        "CMC PERFIL MONTANTE DE 69 DE 3 Mts.": "CMC Perfil Montante de 69 mm x 3,00 ml x 0,42 mm",

        "CMC Perfil Montante de 69 mm x 3,00 m.": "CMC Perfil Montante de 69 mm x 3,00 ml x 0,42 mm",

        "CMC Montante de 69 mm x 3,00 m": "CMC Perfil Montante de 69 mm x 3,00 ml x 0,42 mm",

        "cmc montante de 69mm x 3,00m": "CMC Perfil Montante de 69 mm x 3,00 ml x 0,42 mm",

        "CMC Montante 69 x 3,00 mts": "CMC Perfil Montante de 69 mm x 3,00 ml x 0,42 mm",


        # CMC Perfiles - Soleras

        "CMC PERFIL SOLERA DE 35 DE 3 Mts.": "CMC Perfil Solera de 35 mm x 3,00 ml x 0,42 mm",

        "CMC Perfil Solera de 35 mm x 3,00 m.": "CMC Perfil Solera de 35 mm x 3,00 ml x 0,42 mm",

        "CMC Solera de 35 mm x 3,00 m": "CMC Perfil Solera de 35 mm x 3,00 ml x 0,42 mm",

        "cmc perfil solera 35 de 3 mts": "CMC Perfil Solera de 35 mm x 3,00 ml x 0,42 mm",


        "CMC PERFIL SOLERA DE 70 DE 3 Mts.": "CMC Perfil Solera de 70 mm x 3,00 ml x 0,42 mm",

        "CMC Perfil Solera de 70 mm x 3,00 m.": "CMC Perfil Solera de 70 mm x 3,00 ml x 0,42 mm",

        "CMC Solera de 70 mm x 3,00 m": "CMC Perfil Solera de 70 mm x 3,00 ml x 0,42 mm",

        "cmc perfil solera 70 de 3 mts": "CMC Perfil Solera de 70 mm x 3,00 ml x 0,42 mm",


        # CMC Ángulos

        "Cmc angulo interno de 3,00 m x 0,42 mm": "CMC Perfil Angulo interno de 35 mm x 3,00 ml x 0,42 mm",

        "CMC Angulo Interno de 35 mm x 3,00 m.": "CMC Perfil Angulo interno de 35 mm x 3,00 ml x 0,42 mm",

        "cmc Perfil Angulo interno de 3,00 ml x 0,42 mm": "CMC Perfil Angulo interno de 35 mm x 3,00 ml x 0,42 mm",

        "CMC Angulo Interno 3 m": "CMC Perfil Angulo interno de 35 mm x 3,00 ml x 0,42 mm",


        # Cantoneras / Buñas

        "Cantonera de 31mm x 2.40m BARBIERI": "Cantonera de 31 mm x 2.40 m",

        "Cantonera de 31mm x 2.40m construtek": "Cantonera de 31 mm x 2.40 m",

        "Cantonera drywall de 2,40": "Cantonera de 31 mm x 2.40 m",

        "Eco perfil esquinero de 2,40 m": "Cantonera de 31 mm x 2.40 m",

        "Perfil liviano esquinero de 2,40 m": "Cantonera de 31 mm x 2.40 m",

        "Perfil esquinero de 2,40 construteck": "Cantonera de 31 mm x 2.40 m",

        "Esquineros drywall de 2,40 m": "Cantonera de 31 mm x 2.40 m",

        "esquinero drywall de 2,40 m": "Cantonera de 31 mm x 2.40 m",

        "Cantonera constructec de 31 mm x 2,4m": "Cantonera de 31 mm x 2.40 m",

        "Cantonera construtec de 31 mm x 2,40 m.": "Cantonera de 31 mm x 2.40 m",

        "Cantonera contrutec de 2,40 m": "Cantonera de 31 mm x 2.40 m",

        "Buna Perimetral x 2.60 m": "Buña Perimetral x 2.60 m",

        "Buna perimetral de 2,60 m.": "Buña Perimetral x 2.60 m",

        "Buña perimetral de 2,60 m": "Buña Perimetral x 2.60 m",

        "Buna perimetral de 2,60 m.": "Buña Perimetral x 2.60 m",


        # PGC Perfiles

        "PGC-40 x 0,94 x 6,00 m.": "PGC-40 x 0,94 x 6,00 m",

        "Perfil PGC de 40 mm x 6,00 ml": "PGC-40 x 0,94 x 6,00 m",

        "Perfil PGC de 40 mm": "PGC-40 x 0,94 x 6,00 m",

        "perfil pgc de 40 mm x 6,00": "PGC-40 x 0,94 x 6,00 m",


        "Perfil PGC de 60 mm x 6,00 ml": "PGC-60 x 0,94 x 6,00 m",

        "perfil estr. pgc de 60 mm x 6,00 m": "PGC-60 x 0,94 x 6,00 m",


        "PGC-61 x 0,94 x 6,00 m.": "PGC-61 x 0,94 x 6,00 m",

        "Perfil PGC de 61 mm x 6,00 ml": "PGC-61 x 0,94 x 6,00 m",

        "perfil estructural pgc de 61 mm x 6,00 m": "PGC-61 x 0,94 x 6,00 m",

        "Perfil estructural PGC de 61 mm x 6,00 m": "PGC-61 x 0,94 x 6,00 m",


        "PGC-90 x 0,94 x 6,00 m.": "PGC-90 x 0,94 x 6,00 m",

        "Perfil PGC de 90 mm x 6,00 m": "PGC-90 x 0,94 x 6,00 m",

        "perfil estructural pgc de 90 mm x 6,00 m": "PGC-90 x 0,94 x 6,00 m",

        "perfil pgc de 90 mm x 4,00 m": "PGC-90 x 0,94 x 4,00 m",

        "Perfil PGC  de 90 mm x 6,00 ml": "PGC-90 x 0,94 x 6,00 m",


        "PGC-100 x 0,94 x 6,00 m.": "PGC-100 x 0,94 x 6,00 m",

        "Perfil PGC de 150 mm x 6,00 ml": "PGC-150 x 0,94 x 6,00 m",

        "PGC-150 x 0,94 x 6,00 m.": "PGC-150 x 0,94 x 6,00 m",


        # PGU Perfiles

        "Perfil PGU de 40 mm x 4,00 ml": "PGU-40 x 0,94 x 4,00 m",

        "PGU-40 x 0,94 x 6,00 m.": "PGU-40 x 0,94 x 6,00 m",


        "Perfil PGU de 61 mm x 6,00 m": "PGU-61 x 0,94 x 6,00 m",

        "Perfil PGU de 62 mm x 4,00 ml": "PGU-62 x 0,94 x 4,00 m",

        "perfil estr. pgu de 62 mm x 6,00 m": "PGU-62 x 0,94 x 6,00 m",

        "PGU-62 x 0,94 x 4,00 m.": "PGU-62 x 0,94 x 4,00 m",


        "Perfil PGU de 63 mm x 4,00 m": "PGU-63 x 0,94 x 4,00 m",

        "PGU-63 x 0,94 x 6,00 m.": "PGU-63 x 0,94 x 6,00 m",

        "perfil estructural pgu de 63 mm": "PGU-63 x 0,94 x 6,00 m",


        "Perfil PGU de 90 mm x 4,00 m": "PGU-90 x 0,94 x 4,00 m",

        "Perfil PGU de 90 mm x 6,00 ml": "PGU-90 x 0,94 x 6,00 m",

        "Perfil PGU  de 90 mm x 6,00 ml":"PGU-90 x 0,94 x 6,00 m",


        "PGU-92 x 0,94 x 4,00 m.": "PGU-92 x 0,94 x 4,00 m",

        "Perfil PGU de 92 mm": "PGU-92 x 0,94 x 4,00 m",

        "perfil estructural pgu de 92 mm x 4,00 m": "PGU-92 x 0,94 x 4,00 m",

        "pgu de 92 mm x 4,00 m": "PGU-92 x 0,94 x 4,00 m",

        "perfil pgu de 4,00 m": "PGU-92 x 0,94 x 4,00 m",

        "perfil pgu de 92 mm x 6,00 m": "PGU-92 x 0,94 x 6,00 m",

        "perfil pgo de 92 x 6,00 m": "PGU-92 x 0,94 x 6,00 m", # Variante incorrecta mapeada a PGU

        "Perfil PGU de 92 mm x 4,00 m": "PGU-92 x 0,94 x 4,00 m",


        "PGU-102 x 0,94 x 4,00 m.": "PGU-102 x 0,94 x 4,00 m",

        "Perfil PGU de 150 mm x 4,00 m": "PGU-150 x 0,94 x 4,00 m",

        "Perfil PGU de 152 mm x 4,00 m": "PGU-152 x 0,94 x 4,00 m",


        # PGO Perfiles

        "PGO-37 x 0,94 x 6,00 m": "PGO-37 x 0,94 x 6,00 m",

        "PGO-37 x 0,94 x 6,00 m.": "PGO-37 x 0,94 x 6,00 m",

        "Perfil PGO 6,00 m": "PGO-37 x 0,94 x 6,00 m",

        "perfil pgo de 6,00 m": "PGO-37 x 0,94 x 6,00 m",

        "perfil estructural pgo de 6,00 m": "PGO-37 x 0,94 x 6,00 m",

        "PGO-37 x 0,94 x 6,00 m.": "PGO-37 x 0,94 x 6,00 m",

        "Perfil PGO de 92 x 6,00 m":"PGO-37 x 0,94 x 6,00 m",

        # Perfiles Desmontables

        "Central 3.66": "Perfil Desmontable Central de 3,66 m",

        "Central de 3.66": "Perfil Desmontable Central de 3,66 m",

        "perfil central de 3.66 m": "Perfil Desmontable Central de 3,66 m",

        "Perfil Desmontable Central de 3,66 m. TRX": "Perfil Desmontable Central de 3,66 m",


        "Transversal 1.22": "Perfil Desmontable Transversal de 1,22 m",

        "Transversal de 1.22": "Perfil Desmontable Transversal de 1,22 m",

        "Transversal de 1,22 m. TRX": "Perfil Desmontable Transversal de 1,22 m",


        "Transversal 0.61": "Perfil Desmontable Transversal de 0,61 m",

        "Perfil transversal de 1,22 ml": "Perfil Desmontable Transversal de 1,22 m",

        "Transversal de 0.61": "Perfil Desmontable Transversal de 0,61 m",

        "Perfil transversal de 0,61 ml": "Perfil Desmontable Transversal de 0,61 m",

        "Transversal de 0,61 m. TRX": "Perfil Desmontable Transversal de 0,61 m",

        "Perfileria acustica transversal de 1,21 m": "Perfil Desmontable Transversal de 1,22 m",

        "Perfil transversal": "Perfil Desmontable Transversal de 1,22 m",


        "Perimetral 3.05": "Perfil Desmontable Perimetral de 3,05 m",

        "Perimetral de 3.05": "Perfil Desmontable Perimetral de 3,05 m",

        "Perimetral de 3,05 m. TRX": "Perfil Desmontable Perimetral de 3,05 m",

        # Cielos PVC

        "Cielo PVC 13,5mm Barbieri": "Cielo PVC de 13.5 mm (0.20 x 6.00 m)",

        "cielo pvc de 13.5mm (0.20 x 6 mts) barbieri": "Cielo PVC de 13.5 mm (0.20 x 6.00 m)",

        "Perimetral acustica blanca de 3,00 m": "Perfil Perimetral PVC de 13.5 mm (3.00 m)",

        "Placa de PVC color blanco ind. Brasilera de 10 mm x 0,20 m x 6,00 m": "Cielo PVC de 10 mm (0.20 x 6.00 m)",

        "Cielo PVC 8mm Barbieri": "Cielo PVC de 8 mm (0.20 x 6.00 m)",

        "cielo pvc de 8mm (0.20 x 6 mts) barbieri": "Cielo PVC de 8 mm (0.20 x 6.00 m)",


        "Union H 13,5mm Barbieri": "Perfil Unión H PVC de 13.5 mm (3.00 m)",

        "union h de 13,5mm (0.20 x 3 mts) barbieri": "Perfil Unión H PVC de 13.5 mm (3.00 m)",

        "Conector H de de 6,00 m": "Perfil Unión H PVC de 13.5 mm (6.00 m)",

        "Conector H": "Perfil Unión H PVC de 13.5 mm (6.00 m)",

        "Conector H de 10 mm x 6,00 color blanco": "Perfil Unión H PVC de 10 mm (6.00 m)",


        "Perimetral 13,5mm Barbieri": "Perfil Perimetral PVC de 13.5 mm (3.00 m)",

        "perimetral de 13,5mm (3mts) fabrica barbieri": "Perfil Perimetral PVC de 13.5 mm (3.00 m)",


        "Cielo PVC Tecnoperfil 10 mm 0,20x6 metros": "Cielo PVC de 10 mm (0.20 x 6.00 m)",

        "Cielo PVC de 10 mm (0,20 x 6,00 m) - Tecnoperfil": "Cielo PVC de 10 mm (0.20 x 6.00 m)",

        "Cielo pvc color blanco de 10 mm x 0,20 x 2,40 m": "Cielo PVC de 10 mm (0.20 x 6.00 m)",

        "Placa PVC de 10 mm x 6,00 m": "Cielo PVC de 10 mm (0.20 x 6.00 m)",

        "Cielo PVC de 10mm de 0,2 x 6m": "Cielo PVC de 10 mm (0.20 x 6.00 m)",

        "Placa pvc de 0,20 m x 6,00 m de 10 mm. Ind. Brasilera": "Cielo PVC de 10 mm (0.20 x 6.00 m)",


        "Union H Tecnoperfil": "Perfil Unión H PVC de 10 mm (6.00 m)",

        "Union H de 10 mm x 6,00 m ": "Perfil Unión H PVC de 10 mm (6.00 m)",

        "Union H PVC de 10 MM x 6,00 m": "Perfil Unión H PVC de 10 mm (6.00 m)",

        "Union H PVC de 10 mm x 6,00 m. - Tecnoperfil": "Perfil Unión H PVC de 10 mm (6.00 m)",


        "Perimetral Tecnoperfil": "Perfil Perimetral PVC de 10 mm (6.00 m)",

        "Perimetral pvc de 10 mm x 6,00": "Perfil Perimetral PVC de 10 mm (6.00 m)",

        "Perimetral  de 10mm x 6m": "Perfil Perimetral PVC de 10 mm (6.00 m)",

        "Perimetral de 10mm x 6m": "Perfil Perimetral PVC de 10 mm (6.00 m)",

        "Perfil perimetral de PVC color blanco de 6,00 m": "Perfil Perimetral PVC de 10 mm (6.00 m)",


        # Placas de Yeso

        "Placa de yeso carton de 12,5 x 1,20 x 2,40 m": "Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)", # Mapeo de variante genérica a la marca más probable

        "Placa de Knauf de 12,5 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Placa de Yeso  Knauf de 12,5 mm de (1,20 x 2,40 m)":"Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Placa de Yeso Knauf de 12,5 mm de (1,20 x 2,40 m)":"Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Placa de Yeso carton Knauf de 10 mm x 1,20 x 2,40 m ind. Argentina": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton Knauf  de 10 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton Knauf de 10 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "placa de yeso carton de 10 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton Knauf de 10 mm x 1,20 x 2,40 m. ind. Argentina": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton de 10 mm Knauf de 10 mm x 1,20 x 2,40 m":"Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton de 10 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton de12,5 mm x 1,20 x 2,40 m resit. A la humedad": "Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso carton Knauf RH de 10 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf RH de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso Drywall RH  de 12,5 mm  x 2,40 m Knauf": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso Knauf RH  12,5 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso carton RH de 12,5 mm x 1,20 x 2,40": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso Knauf RH de 12,5 x 1,20 x 2,40 m": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso RH de 12,5 x 1,20 x 2,40 m": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "Placasde yeso carton de 10 mm x 1,20 m": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Pcas de yeso RH Kanauf":"Placa de Yeso Knauf RH de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso RH Kanauf":"Placa de Yeso Knauf RH de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton Nauf resit. A la humedad":"Placa de Yeso Knauf RH de 10 mm (1.20 x 2.40 m)",

        "Placa de 10 mm x 1,20 x 2,40": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso carton de 1,20 x 2,40 x 12,5 mm resist. A la humedad (  baños ,133,66 m2 )":"Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yesoKnauf  de 10,00 mm x 1,20 x 2,40": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de Yeso de 9,5 mm de (1,20 x 2,40 m).- Durlock": "Placa de Yeso Durlock de 9,5 mm (1.20 x 2.40 m)",

        "KNAUF SP GLASS 1,20X2,40X12,50MM": "Placa de Yeso SP KNAUF  de 12,5 mm (1.20 x 2.40 m)",

        "PLACA SP GLASS KNAUF": "Placa de Yeso SP KNAUF de 12,5 mm (1.20 x 2.40 m)",

        "Placa Knauf SP GLASS de 12,5 mm de (1,20 x 2,40 m).-": "Placa de Yeso SP KNAUF de 12,5 mm (1.20 x 2.40 m)",

        "Placa de Yeso de 9,5 mm de (1,20 x 2,40 m).- Placo": "Placa de Yeso Placo de 9,5 mm (1.20 x 2.40 m)",

        "Placa de Yeso Gyplac de 12,7 mm de (1,22 x 2,44 m)": "Placa de Yeso Gyplac de 12,7 mm (1.22 x 2.44 m)",

        "Placa de yeso carton GYPLACK de 1,20 x 2,40 m x 12,5 mm  resist. Al fuego ( 164,25 m2 )":"Placa de Yeso Gyplac RF de 12,7 mm (1.22 x 2.44 m)",

        "Placa GYPLAC Roja RF de 12,7 mm": "Placa de Yeso Gyplac RF (Roja) de 12,7 mm (1.22 x 2.44 m)",

        "Placa Gyplac Verde RF de 12,7 mm de (1,22 x 2,44 m).-": "Placa de Yeso Gyplac RF (Verde) de 12,7 mm (1.22 x 2.44 m)",

        "Placa Gyplac Verde RH de 12,7 mm de (1,22 x 2,44 m).-": "Placa de Yeso Gyplac RH (Verde) de 12,7 mm (1.22 x 2.44 m)",

        "Placa Knauf Verde RH de 12,5 mm de (1,20 x 2,40 m).-": "Placa de Yeso Knauf RH (Verde) de 12,5 mm (1.20 x 2.40 m)",

        "Placa Plus Vinyl de 0,61 x 0,61": "Placa de Yeso Plus Vinyl de 0,61 x 0,61 m",

        "PROVISION E INSTALACION DE CIELO FALSO ACUSTICO DESMONTABLE CON PANEL PLUSSVINIL  , MODULO DE 0,61 X 0,61 M": "Placa de Yeso Plus Vinyl de 0,61 x 0,61 m",

        "Placa de yeso carton de 12,5 mm x 2,40 x 1,20":"Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Plca de yeso Knauf de 10 mm de 1,20 x 2,40 m":"Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "Placa de yeso de 10,00 mm x 1,20 x 2,40": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        # Placas Knauf

        "Placa Knauf 1.20x2.40x10mm": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "placa knauf std 1.20x2.40x10mm": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "placa yeso knauf 1.20x2.40x10mm": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",


        "Placa Knauf 12.5mm 1.20x2.40": "Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso carton Knauf de 10 mm x 1,20 x 2,40 m (69,20 m2 dormitorios  )": "Placa de Yeso Knauf de 10 mm (1.20 x 2.40 m)",

        "placa de yeso carton knauf de 12,5 mm x 1,20 x 2,40 m": "Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",

        "Placa de yeso carton de 12,5 mm x 1,20 x 2,40 m Resistente  al fuego ( plcaca roja )":"Placa de Yeso Knauf de 12,5 mm (1.20 x 2.40 m)",


        "Placa Knauf RH 1.20x2.40x12.5mm": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",

        "placa knauf verde rh 12.5mm 1.20x2.40": "Placa de Yeso Knauf RH de 12,5 mm (1.20 x 2.40 m)",


        "Placa Knauf RF 1.20x2.40x12.5mm": "Placa de Yeso Knauf RF de 12,5 mm (1.20 x 2.40 m)",

        "placa knauf rosa rf 1.20x2.40": "Placa de Yeso Knauf RF de 12,5 mm (1.20 x 2.40 m)",

        # Placas vinyl Frame

        "Panel Plus Vinil de 0,61 x 0,61 x 0,08 mm":"Placa Plus Vinyl de 0,61 x 0,61 m",

        "Placa Pusvinil de 0,61 x 0,61 m ( medida americana)": "Placa Plus Vinyl de 0,61 x 0,61 m",

        "Placa PLUS VINIL gypsum de 0,61 x 0,61 m color blanco de 8 mm": "Placa Plus Vinyl de 0,61 x 0,61 m",

        "Placa de Yeso Plus Vinyl de 0,61 x 0,61 m": "Placa Plus Vinyl de 0,61 x 0,61 m",


        # Placas Desmontables (Fibra Mineral)

        "Placa desmontable USG": "Placa Desmontable Fibra Mineral USG 0.61 x 1.22 m",

        "placa desmontable durlock 0.61 x 1.22": "Placa Desmontable Fibra Mineral USG 0.61 x 1.22 m", # Mapeo a USG como estándar

        "Placa GYPSUM de 0,61 x 0,61 m": "Placa Desmontable Fibra Mineral GYPSUM 0.61 x 0.61 m",

        "Placa Radar de 0,61 x 0,61 m borde tegulado": "Placa Desmontable Fibra Mineral RADAR 0.61 x 0.61 m",

        "Placa Radar de 0,61 x 0,61 m con borde rebajado": "Placa Desmontable Fibra Mineral RADAR 0.61 x 0.61 m",

        "PLACA PEBBLED SLT 0,61 x 0,61": "Placa Desmontable Fibra Mineral PEBBLED SLT 0.61 x 0.61 m",

        "Placa Pebbled SLT 0.61x0.61": "Placa Desmontable Fibra Mineral PEBBLED SLT 0.61 x 0.61 m",

        "Placa Pebbled Borde Recto 0.61x1.22": "Placa Desmontable Fibra Mineral PEBBLED Borde Recto 0.61 x 1.22 m",

        "Placa Mars SQ 0.61x1.22" : "Placa Desmontable Fibra Mineral MARS SQ 0.61 x 1.22 m",

        "Placa Radar SQ 0.60x0.60": "Placa Desmontable Fibra Mineral RADAR SQ 0.60 x 0.60 m",

        "Placa Radar USG 0.61x1.22": "Placa Desmontable Fibra Mineral RADAR USG 0.61 x 1.22 m",

        "Placa Plus Desing de 0,61 x 01,21 m con borde tegulado": "Placa Desmontable Fibra Mineral PLUS DESING 0.61 x 1.21 m",

        "Placa de Fibra mineral PLUS DESING de 0,60 x 0,60 m borde tegulado": "Placa Desmontable Fibra Mineral PLUS DESING 0.60 x 0.60 m",

        "USG Radar Clima - Plus SLT 0,61 x 0,61 Tegulada desde Fábrica": "Placa Desmontable Fibra Mineral RADAR USG 0.61 x 0.61 m",

        "USG Radar Clima - Plus SLT 0,61 x 0,61 Tegulada": "Placa Desmontable Fibra Mineral RADAR USG 0.61 x 0.61 m",

        "USG Radar Clima - Plus(tegulada) 0,61 x 0,61": "Placa Desmontable Fibra Mineral RADAR USG 0.61 x 0.61 m",

        "Placa Plus CORE 0,60x0,60x15mm": "Placa Desmontable Fibra Mineral Plus CORE de 15 mm (0.60 x 0.60 m)",

        "Placa Plus Core": "Placa Desmontable Fibra Mineral Plus CORE de 15 mm (0.60 x 0.60 m)",

        "Placa ENCORE de 0,61 x 0,61 m": "Placa Desmontable Fibra Mineral ENCORE de 13 mm (0.61 x 0.61 m)",

        "Placa plus core de 0,603 x 0,603 m borde tegulado": "Placa Fibra Mineral Plus CORE de 0,603 x 0,603 m",

        # Placas Cementicias

        "Placa Cementicia 1.20x2.40x8mm Volcan": "Placa Cementicia de 8 mm (1.20 x 2.40 m) - Volcan",

        "placa cementicia 1.20x2.40x8mm duralit": "Placa Cementicia de 8 mm (1.20 x 2.40 m) - Duralit",

        "Placa de fibrocemento Duralit de 8 mm": "Placa Cementicia de 8 mm (1.20 x 2.40 m) - Duralit",

        "Placa Cementicia 1.20x2.40x6mm Volcan": "Placa Cementicia de 6 mm (1.20 x 2.40 m) - Volcan",

        "placa cementicia 1.20x2.40x6mm duralit": "Placa Cementicia de 6 mm (1.20 x 2.40 m) - Duralit",

        "placa cementicia 1.20x2.40x10mm duralit": "Placa Cementicia de 10 mm (1.20 x 2.40 m) - Duralit",


        "Placa Aquapanel Universal 1.20x2.40x8mm": "Placa Cementicia Aquapanel Universal de 8 mm (1.20 x 2.40 m)",

        "Placa USG Durock de 12.5mm (1.22x2.44)": "Placa Cementicia USG Durock de 12.5 mm (1.22 x 2.44 m)",

        "Placa de yeso carton GYPLACK de 12,7 mm x 1,22 x 2,44 m resistente a la humedad": "Placa Cementicia USG Durock de 12.7 mm (1.22 x 2.44 m)",

        "Placa de Fibrocemento 10 mm (1.22 x 2.44 m)": "Placa Cementicia de Fibrocemento de 10 mm (1.22 x 2.44 m)",

        # Placa Alumino

        "Placa de Aluminio blanca TRX": "Placa Aluminio Blanca de (0.61 x 0.61 m)",

        "Placa de Aluminio Blanca": "Placa Aluminio Blanca de (0.61 x 0.61 m)",

        # Tornillos

        "Tornillo T1 Pta Aguja": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "t1 aguja": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "tornillo t1 punta de aguja": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "Tornillo T1 Punta Aguja (caja 500 unid)": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "Tornillo T1 aguja": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "Tornillo T1 punta aguja": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "Tornillo T1 punta de aguja": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "Torniullo T1 PUNTA DE AGUJA ": "Tornillo T1 Punta Aguja (caja 500 unid)",

        "Tornillo T1 aguja caja de 1000 pzas.": "Tornillo T1 Punta Aguja (caja 1000 unid)",

        "Tornillo T1 aguja  caja de 1000 unidades": "Tornillo T1 Punta Aguja (caja 1000 unid)",

        "Tornillo T1 aguja caja de 1000 unidades": "Tornillo T1 Punta Aguja (caja 1000 unid)",


        "Tornillo T1 Pta Broca": "Tornillo T1 Punta Broca (caja 500 unid)",

        "t1 broca": "Tornillo T1 Punta Broca (caja 500 unid)",

        "Tornillo T1 Punta Broca (caja 500 unid)": "Tornillo T1 Punta Broca (caja 500 unid)",

        "Tornillo T1 puinta de broca": "Tornillo T1 Punta Broca (caja 500 unid)",

        "Tornillo T1 punta de broca": "Tornillo T1 Punta Broca (caja 500 unid)",

        "Tornillos T1. punta de broca": "Tornillo T1 Punta Broca (caja 500 unid)",

        "Tornillo T1 broca caja de 1000 pzas.": "Tornillo T1 Punta Broca (caja 500 unid)",


        "Tornillo T2 Pta Aguja": "Tornillo T2 Punta Aguja (caja 1000 unid)",

        "t2 aguja": "Tornillo T2 Punta Aguja (caja 1000 unid)",

        "Tornillo T2 Punta Aguja (caja 1000 unid)": "Tornillo T2 Punta Aguja (caja 1000 unid)",

        "Tornillo T2 punta de aguja": "Tornillo T2 Punta Aguja (caja 1000 unid)",

        "Tornillos T2 aguja": "Tornillo T2 Punta Aguja (caja 1000 unid)",

        "Tornillo T2 punta de aguja caja de 1000 unidades": "Tornillo T2 Punta Aguja (caja 1000 unid)",


        "Tornillo T2 Pta Broca": "Tornillo T2 Punta Broca (caja 1000 unid)",

        "t2 broca": "Tornillo T2 Punta Broca (caja 1000 unid)",

        "Tornillo T2 Punta Broca": "Tornillo T2 Punta Broca (caja 1000 unid)",

        "Tornillos T2 punta de broca ": "Tornillo T2 Punta Broca (caja 1000 unid)",


        "Tornillo T3 Broca 1 1/2": "Tornillo T3 Punta Broca 1 1/2\"",

        "T4 Broca Pieza": "Tornillo T4 Punta Broca (pieza)",

        "T4 Aguja Pieza": "Tornillo T4 Punta Aguja (pieza)",


        "Tornillo Cabeza Hexagonal": "Tornillo Cabeza Hexagonal (caja 1000 unid)",

        "tornillo hexagonal": "Tornillo Cabeza Hexagonal (caja 1000 unid)",

        "Tornillos Hexagonales punta de broca": "Tornillo Cabeza Hexagonal (caja 1000 unid)",

        "Tornillo Cabeza Hexagonal (caja 1000 unid)": "Tornillo Cabeza Hexagonal (caja 1000 unid)",


        "Tornillo de Expansion (3/8 x 2 1/4)": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Perno de Exoancion":"Tornillo de Expansión (3/8 x 2 1/4)",

        "Perno de Expansión": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Perno de expansión": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Pernos de expansión": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Pernos de expansión 3/8/ 21/4":"Tornillo de Expansión (3/8 x 2 1/4)",

        "tornillo de expansion 3/8 x 2 1/4": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Tornillo Expansion (3/8 X 2 1/4)": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Perno de anclaje": "Tornillo de Expansión (3/8 x 2 1/4)",

        "Tornillos de anclajes" : "Tornillo de Expansión (3/8 x 2 1/4)",

        "tornillo con aleta": "Tornillo con aleta (pieza)",

        "Tornillo de encarne Nro 6": "Tornillo de encarne N°6 (pieza)",

        "Tarugo Nro 6": "Tarugo N°6 (pieza)",

        "tarugo 6": "Tarugo N°6 (pieza)",


        "Tornillo Autoperforante 14x4": "Tornillo Autoperforante 14x4 (pieza)",

        "Tornillo Autoperforante 14x5": "Tornillo Autoperforante 14x5 (pieza)",


        "Gancho J-120": "Gancho J-120 (pieza)",

        "ganchos j120": "Gancho J-120 (pieza)",


        # Aislantes - Lana de Vidrio/Rolac/Membrana/Fieltro

        "Lana de vidrio Volcan de 100 mm (1,20x7,50 mt)": "Lana de Vidrio Volcan de 100 mm (1.20 x 7.50 m)",

        "lana de vidrio volcan 100mm": "Lana de Vidrio Volcan de 100 mm (1.20 x 7.50 m)",

        "lana vidrio volcan 100mm": "Lana de Vidrio Volcan de 100 mm (1.20 x 7.50 m)",


        "Lana de vidrio Volcan de 70 mm 0,6x24 mt(2 rollos) Volcan": "Lana de Vidrio Volcan de 70 mm (0.60 x 24 m) (2 rollos)",

        "lana vidrio volcan 70mm 0.6x24": "Lana de Vidrio Volcan de 70 mm (0.60 x 24 m) (2 rollos)",


        "ROLAC PLATA DE 50MM 1.20x24mts VOLCAN": "Rolac Plata de 50 mm (1.20 x 24 m)",

        "FIBRA DE VIDRIO ROLACK PLATA DE 50 MM X 1,20 X 18 ML  ISOVER IND. ARGENTINA":"Rolac Plata Isover de 50 mm (1.20 x 18 m)",

        "Rolac Plata de 50mm (1,2x18m) ISOVER": "Rolac Plata Isover de 50 mm (1.20 x 18 m)",

        "rolac plata isover 50mm 1.20x18m": "Rolac Plata Isover de 50 mm (1.20 x 18 m)",

        "rolac plata 50mm 1.2x24": "Rolac Plata Isover de 50 mm (1.20 x 24 m)",

        "Rolac Plata 100 mm": "Rolac Plata Isover de 100 mm (1.20 x 18 m)",

        "rolac plata 100mm": "Rolac Plata Isover de 100 mm (1.20 x 18 m)",

        "fibra de vidrio ISOVER rolack plata de 50 mm x 1,20 x 18 m": "Rolac Plata Isover de 50 mm (1.20 x 18 m)",


        "Lana de Vidrio de 70mm (1,20 x 13m) - Isover": "Lana de Vidrio Isover de 70 mm (1.20 x 13 m) (2 rollos por paquete)",

        "lana vidrio isover 70mm 1.2x13": "Lana de Vidrio Isover de 70 mm (1.20 x 13 m) (2 rollos por paquete)",


        "Membrana rufi 5 doble aluminio": "Membrana Rufi de 5 mm Doble Aluminio",

        "membrana rufi 5 doble alu": "Membrana Rufi de 5 mm Doble Aluminio",

        "Membrana rufi 10 doble aluminio": "Membrana Rufi de 10 mm Doble Aluminio",

        "Membrana hidrofuca Tyvec de 0,91 m x 30,5 m": "Membrana Hidrófuga de 0.91 m × 30.5 m",


        "Membrana Aluminizada de 10mm (TBA 10) (1 x 20 mts) Isolant": "Membrana Isolant Aluminizada de 10 mm (1.00 x 20.00 m)",

        "Membrana Isolant TBA 10 (1x20m)": "Membrana Isolant Aluminizada de 10 mm (1.00 x 20.00 m)",

        "aislante termico doble aluminio tipo rufi de 20 ml x 1,00 m": "Membrana Isolant Aluminizada de 10 mm (1.00 x 20.00 m)",

        "membrana isolant tba10 1x20": "Membrana Isolant Aluminizada de 10 mm (1.00 x 20.00 m)",

        "membrana aluminizada 10mm isolan": "Membrana Isolant Aluminizada de 10 mm (1.00 x 20.00 m)",


        "Fieltro WF 4+POP 1200x12500x70mm": "Fieltro Feltro WF4+POP 1200 x 12500 x 70 mm",

        "Feltro WF 4+POP 1200x12500x70mm": "Fieltro Feltro WF4+POP 1200 x 12500 x 70 mm",

        "fieltro wf4pop 1200x12500x70": "Fieltro Feltro WF4+POP 1200 x 12500 x 70 mm",


        "Fieltro WF 4+POP PC 60 1200x12500x70mm": "Fieltro Feltro WF4+POP PC60 1200 x 12500 x 70 mm",

        "Fieltro Tensado ALU HIDR de 50mm": "Fieltro Tensado Alu/Hidr. de 50 mm",

        "fieltro tensado alu hidr 50mm": "Fieltro Tensado Alu/Hidr. de 50 mm",


        "Solarmaxi-Pro de 25x1,20MtsX25mm": "Aislante Solarmaxi-Pro de 25 mm (1.20 x 25 m)",

        "aislante solarmaxipro 25x1.20x25": "Aislante Solarmaxi-Pro de 25 mm (1.20 x 25 m)",


        # Cintas (Masillas y Acabados)

        "Cinta Vertex Fibrotape 0.52mmx50m": "Cinta Vertex Fibrotape 0.52 mm x 50 m",

        "cinta vertex fibrotape 0.52mmx50m": "Cinta Vertex Fibrotape 0.52 mm x 50 m",

        "cinta brasilit vertex fibrotape 0.52x50": "Cinta Vertex Fibrotape 0.52 mm x 50 m",

        "Cinta Constructek 75 m": "Cinta Constructec de 50 mm x 75 m",

        "Cinta Constructec 75m": "Cinta Constructec de 50 mm x 75 m",

        "cinta construtec 75 mts": "Cinta Constructec de 50 mm x 75 m",

        "Cinta Construtec de 50 mm x 75 m.": "Cinta Constructec de 50 mm x 75 m",


        "CINTA MALHA GRX 100MMx50M Rollo": "Cinta Malla GRX de 100 mm x 50 m",

        "Cinta Malha GRX 100MMx50M": "Cinta Malla GRX de 100 mm x 50 m",

        "Cinta Malla GRX 100MMx50M": "Cinta Malla GRX de 100 mm x 50 m",

        "Malla junta rigida": "Cinta Malla GRX de 100 mm x 50 m",

        "Cinta malla": "Cinta Malla GRX de 100 mm x 50 m",

        "CINTA TRAMADA CON FIBRA DE VIDRIO 90Mts": "Cinta Tramada con Fibra de Vidrio 90 m",

        "Cinta Malha GRX de 100 mm x 50 mtrs.": "Cinta Malla GRX de 100 mm x 50 m",

        "cinta malla para placa cementicia de 45 ml": "Cinta Malla para Placa Cementicia de 100 mm × 45 m",


        "Cinta de Papel con Fleje Metalico GYPLAC Rollo": "Cinta de Papel con Fleje Metálico de 50 mm × 30 m",

        "Cints de papel rollo de 75 m":"Cinta Malla Gyplac de 50 mm x 75 m",

        "Cinta de papel microperforado Gyplack de 75 ml": "Cinta Malla Gyplac de 50 mm x 75 m",

        "Cinta de papel microperforado de 75 ml": "Cinta Malla Gyplac de 50 mm x 75 m",

        "Cinta Gyplac Fleje Metálico": "Cinta de Papel con Fleje Metálico de 50 mm × 30 m",

        "Cinta de Papel con Fleje Metálico de 50 mm × 30 m": "Cinta de Papel con Fleje Metálico de 50 mm × 30 m",


        "Cinta Gyplac 75m": "Cinta Malla Gyplac de 50 mm x 75 m",

        "Cinta Gyplac de 75 m": "Cinta Malla Gyplac de 50 mm x 75 m",

        "Cinta Gyplac de 50 mm x 75 m.": "Cinta Malla Gyplac de 50 mm x 75 m",

        "Cinta Construtec de 50 mm x 75 m.": "Cinta Constructec de 50 mm x 75 m",

        "Cinta de 75 ml": "Cinta Malla Gyplac de 50 mm x 75 m",


        "Cinta Fibrotape Vertex 100mmx50m": "Cinta Malla Fibrotape de 100 mm x 50 m",

        "Cinta fibrotape para placa exterior": "Cinta Malla Fibrotape de 100 mm x 50 m",

        "Cinta malla fibro tape de 45 m l x 10 cm": "Cinta Malla Fibrotape  de 100 mm × 45 m",

        "Cinta Vertex Fibrotape 100x50m": "Cinta Malla Fibrotape de 100 mm x 50 m",

        "cinta vertex 100x50": "Cinta Malla Fibrotape de 100 mm x 50 m",

        "cinta malla fibrotape de 10 cm x 45,7 ml":"Cinta Malla Fibrotape de 100 mm x 45,7 m",


        # Discos de Corte

        "Disco de Corte Pegatec 4''": "Disco de Corte Pegatec 4\"",

        "disco corte pegatec 4\"": "Disco de Corte Pegatec 4\"",

        "disco corte 4''": "Disco de Corte Pegatec 4\"",


        "Disco de Corte Pegatec 7''": "Disco de Corte Pegatec 7\"",

        "disco corte pegatec 7\"": "Disco de Corte Pegatec 7\"",

        "disco corte 7''": "Disco de Corte Pegatec 7\"",


        "Disco de Corte Pegatec 9''": "Disco de Corte Pegatec 9\"",

        "disco corte pegatec 9\"": "Disco de Corte Pegatec 9\"",

        "disco corte 9''": "Disco de Corte Pegatec 9\"",

        "dico corte 9\"": "Disco de Corte Pegatec 9\"",

        "DISCO DE CORTE 9'' NORTON": "Disco de Corte Norton 9\"", # Nuevo producto

        "DISCO DE CORTE DE 9'' PEGATEC": "Disco de Corte Pegatec 9\"",


        "Disco de Corte Pegatec 12''": "Disco de Corte Pegatec 12\"",

        "disco corte pegatec 12\"": "Disco de Corte Pegatec 12\"",

        "disco corte 12''": "Disco de Corte Pegatec 12\"",


        # Tableros OSB

        "Tablero OSB de 9,5 mm": "Tablero OSB de 9.5 mm (1.22 x 2.44 m)",

        "tablero osb 9.5mm": "Tablero OSB de 9.5 mm (1.22 x 2.44 m)",

        "tabler osb 9.5": "Tablero OSB de 9.5 mm (1.22 x 2.44 m)",

        "TABLERO OSB DE 9,5 MM X 1,22 X 2,44 M": "Tablero OSB de 9.5 mm (1.22 x 2.44 m)",


        "Tablero OSB de 11,1 mm": "Tablero OSB de 11.1 mm (1.22 x 2.44 m)",

        "tablero osb 11.1mm": "Tablero OSB de 11.1 mm (1.22 x 2.44 m)",

        "Placa OSB de 11,10 mm x 1,22 x 2,44 m": "Tablero OSB de 11.1 mm (1.22 x 2.44 m)",

        "Placa OSB de 11,10 mm x 1,22 x 2,44 m": "Tablero OSB de 11.1 mm (1.22 x 2.44 m)",


        "Tablero OSB de 15 mm": "Tablero OSB de 15 mm (1.22 x 2.44 m)",

        "tablero osb 15mm": "Tablero OSB de 15 mm (1.22 x 2.44 m)",

        "tablero obs 15mm": "Tablero OSB de 15 mm (1.22 x 2.44 m)",

        "TABLERO OSB DE 15 MM X 1,22 M X 2,44 M": "Tablero OSB de 15 mm (1.22 x 2.44 m)",


        # Masillas

        "Masilla Construtek de 20KG": "Masilla Constructec de 20 kg",

        "masilla construtec 20 kg": "Masilla Constructec de 20 kg",

        "masilla construtec de 20 kl": "Masilla Constructec de 20 kg",

        "Masilla Construtec Balde 20 kg": "Masilla Constructec de 20 kg",

        "masilla construteck de 20 kl lista para usar": "Masilla Constructec de 20 kg",

        "Masilla Construteck de 20 kg.": "Masilla Constructec de 20 kg",

        "Masilla Construteck lista para usar en caja de 20 kl": "Masilla Constructec de 20 kg",


        "MASILLA PLUS EXTRA FINA ANCLAFLEX 20KG": "Masilla Anclaflex Plus Extra Fina de 20 kg",

        "Masilla Plus Extra Fina Anclaflex 20 kg": "Masilla Anclaflex Plus Extra Fina de 20 kg",

        "Masilla Anclaflex Balde 20 kg": "Masilla Anclaflex Plus Extra Fina de 20 kg",


        "Masilla Maxi Pro 20 kg Balde": "Masilla Maxi Pro Profesional de 20 kg",

        "Masilla Profesional Maxi Pro de 20 kg.":"Masilla Maxi Pro Profesional de 20 kg",


        "Masilla Placo Balde 25 kg": "Masilla Placomix balde de 25 kg",

        "masilla placo de 25 kg.": "Masilla Placomix balde de 25 kg",

        "masilla placo de 25, kl": "Masilla Placomix balde de 25 kg",

        "Masilla Placo Balde 6 kg": "Masilla Placomix balde de 6 kg",

        "Masilla Placo de 6 kg Bolsa": "Masilla Placomix balde de 6 kg",

        "Masilla balde de 25 kl": "Masilla Placomix balde de 25 kg",

        "Masilla Aquapanel 25 kg": "Masilla Placomix balde de 25 kg",

        "Masilla Exterior Aquapanel 25 kg": "Masilla Placomix balde de 25 kg",


        "Masilla Placomix 25kg": "Masilla Placomix balde de 25 kg",

        "Masilla Placomix Balde 25kg": "Masilla Placomix balde de 25 kg",

        "masilla placomix de 25 kl": "Masilla Placomix balde de 25 kg",

        "Masilla Placo Mix de 25 kg.": "Masilla Placomix balde de 25 kg",

        "Masilla Placo Mix de 6 kg.": "Masilla Placomix balde de 6 kg", # Nuevo producto


        "Masilla Profesional 25 kg Balde": "Masilla Placomix balde de 25 kg",

        "Masilla Basecoat Exterior 25kg": "Masilla Placomix balde de 25 kg",

        "masilla basecoat en bolsa de 25 kl para placa de cemento": "Masilla Placomix balde de 25 kg",

        "Masilla para placa cementicia Aqua panel Knauf de 25 kl ( bolsa para preparar )": "Masilla Placomix balde de 25 kg",

        # Otros Acabados/Accesorios (Masillas y Acabados / Cielos)

        "Cantonera de Vyniyl 41mm": "Cantonera de Vinyl de 41 mm",

        "cantonera vynil 41mm": "Cantonera de Vinyl de 41 mm",

        "cantonera vinil 41mm": "Cantonera de Vinyl de 41 mm",


        "Banda Acustica de 5CMx25M": "Banda Acústica de 5 cm x 25 m",

        "banda acustica 5cmx25m": "Banda Acústica de 5 cm x 25 m",


        "Junta de dilatacion Barbieri": "Junta de Dilatación Barbieri",

        "junta dilatacion barbieri": "Junta de Dilatación Barbieri",


        # Herramientas

        "Espatula de 8 ": "Espatula de 8",

        "Espatula mediana":"Espatula de 8",

        "Espatula para masilla de 5\" cod. 40017":"Espatula de 5",

        "Espatula tolsen 40024": "Espatula de 5",

        "Bandeja de plstico cod.20651": "Bandeja porta masilla (plástica)",

        "Estilete de aluminio cod. 30008": "Cutter profesional",

        "ESTILETE INDUSTRIAL (30019)": "Cutter profesional",

        "ESPATULA  DE 125MM (40017)": "Espatula de 125 mm",

        "ESPATULA 8\" (40023)": "Espatula de 8",

        "Cizalla para perfiles": "Cizalla para perfiles de tabiquería",

        "Tijera de aviacion": "Tijera de aviación",

        "TIJERA AVIACION DERECHA": "Tijera de aviación (derecha)",

        "Nivel de mano 1,20 m": "Nivel de mano de 1,20 m",

        "Nivel laser": "Nivel láser",

        "Espatula 6''": "Espátula 6\"",

        "Cierra para fibra de vidrio cutter cod. 31014": "Sierra para fibra de vidrio (código 31014)",

        "Cierra universal 31013": "Sierra para placas (código 31013)",

        "Cierra para placas cod. 31013": "Sierra para placas (código 31013)",

        "Cutter profesional": "Cutter profesional",

        "Bandeja para masilla": "Bandeja porta masilla (plástica)",

        "CHAROLA PLASCTICO": "Bandeja porta masilla (plástica)",

        "CHAROLA PLASCTICO":"Bandeja porta masilla (plástica)",

        "Bandeja porta masilla inox": "Bandeja porta masilla (acero inoxidable)",

        "CHAROLA TRUPPER 30023": "Charola Trupper (código 30023)",

        "Cinturon porta herramientas": "Cinturón porta herramientas",

        "Dado Magnético de 8mm (10 unid.)": "Dados magnéticos de 8 mm (caja de 10 unid.)",

        "Dado Magnético de 1/4 (10 unid.)": "Dados magnéticos de 8 mm (caja de 10 unid.)",

        "JGO DE DADOS MAGNETICOS 3PZA": "Dados magnéticos de 8 mm (caja de 10 unid.)",

        "Pintura impermeabilizante para techo SIKA GRIS X 18 L": "Pintura impermeabilizante para techo SIKA GRIS",

        "SIKALASTIC-1K X 20 KG (Gris)":"Pintura impermeabilizante para techo SIKA GRIS",

        # Fierros

        "Fierro Corrugado 12 mm Las Lomas": "Fierro Corrugado 12 mm Las Lomas",

        "hierro corrugado 12 mm": "Fierro Corrugado 12 mm Las Lomas",

        "fierro corrugado de 12 mm x 12m lomas": "Fierro Corrugado 12 mm x 12 m Las Lomas",


        "Fierro Corrugado 9,5 mm Las Lomas": "Fierro Corrugado 9.5 mm Las Lomas",

        "Fierro Corrugado 9.5 mm Lomas": "Fierro Corrugado 9.5 mm Las Lomas",

        "hierro corrugado 9.5 mm x 12 m": "Fierro Corrugado 9.5 mm x 12 m Las Lomas",

        "Fierro Corrugado 9,5 mm Las Lomas": "Fierro Corrugado 9.5 mm Las Lomas",


        "Fierro Corrugado 8 mm Las Lomas": "Fierro Corrugado 8 mm Las Lomas",

        "Fierro de Construcción 8 mm": "Fierro Corrugado 8 mm Las Lomas",


        "Fierro Corrugado 6 mm Gerdau": "Fierro Corrugado 6 mm Gerdau",

        "fierro 6mm gerdau": "Fierro Corrugado 6 mm Gerdau",

        "hierro corrugado 6 mm": "Fierro Corrugado 6 mm Gerdau",

        "fierro corrugado gerdau 6 mm x 12 m": "Fierro Corrugado 6 mm x 12 m Gerdau",

    }

    return catalogo_dict


# 📁 FASE 1: Comprensión del Negocio (CRISP-DM)

PlusSteel busca optimizar la planificación de inventario mediante predicción de demanda. Se enfrenta a retos como:


- Nombres de productos inconsistentes

- Alta variabilidad de demanda

- Productos con poco historial

- Necesidad de agrupar productos por función constructiva


Este sistema tiene como objetivo ayudar al equipo comercial, operaciones y logística a tomar decisiones informadas para compras y distribución.


---



## Librerias Necesarias en todo el notebook


# fuzzywuzzy[speedup] requiere python-levenshtein.

!pip -q install pandas openpyxl thefuzz[speedup] Unidecode fuzzywuzzy python-levenshtein shap imbalanced-learn lightgbm xgboost


# 1. LIBRERÍAS CORE PARA MANIPULACIÓN DE DATOS Y LIMPIEZA

import os, re, numpy as np, pandas as pd

import json

from datetime import datetime, timedelta

import re # Para expresiones regulares en limpieza

from unidecode import unidecode # Para normalización de texto (quitar tildes)

from numpy import log1p # Para transformaciones logarítmicas

import warnings

warnings.filterwarnings('ignore')

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

from catalogo_productos import crear_catalogo_completo

from normalizacion import normalizar_texto

# 2. LIBRERÍAS DE VISUALIZACIÓN Y UTILIDADES

import matplotlib.pyplot as plt

import seaborn as sns

import joblib # Para guardar y cargar modelos

from scipy import stats # Para análisis estadístico

# Configuración básica para visualizaciones

plt.style.use('ggplot')

sns.set_style('whitegrid')

# 3. LIBRERÍAS DE PROCESAMIENTO DE TEXTO Y FUZZY MATCHING

from thefuzz import fuzz, process

from sklearn.feature_extraction.text import TfidfVectorizer


# 4. LIBRERÍAS DE MACHINE LEARNING (SCIKIT-LEARN)

# Módulos de Preparación y Validación

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, TimeSeriesSplit

from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline


# Módulos de Clustering y Vecinos

from sklearn.cluster import KMeans, DBSCAN

from sklearn.neighbors import NearestNeighbors


# Modelos y Ensembles

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso

from sklearn.ensemble import GradientBoostingRegressor # Regresor

import lightgbm as lgb # LightGBM (Clasificación/Regresión)

import xgboost as xgb # XGBoost (Clasificación/Regresión)


# Módulos de Evaluación de Métricas

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    roc_auc_score,

    roc_curve,

    precision_recall_curve,

    average_precision_score,

    confusion_matrix,

    mean_absolute_error,

    mean_squared_error,

    r2_score,

    silhouette_score # Para clustering

)


# 5. LIBRERÍAS PARA DATOS DESBALANCEADOS (IMBALANCED-LEARN)

from imblearn.over_sampling import SMOTE

from imblearn.under_sampling import RandomUnderSampler

from imblearn.combine import SMOTETomek, SMOTEENN

from sklearn.utils import resample # Para resample manual


# 6. EXPLICABILIDAD DE MODELOS (SHAP)

import shap

np.random.seed(42)

# 7. CONFIGURACIÓN FINAL

pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', 100) # Dejé esta activa para facilitar la exploración

print("✅ Toolkit de proyecto cargado (incluyendo instalación de paquetes avanzados).")




## CONFIGURACION GLOBAL


# CELDA DE CONFIGURACION GLOBAL

%%writefile configuracion_global.py

# ============================================================

# 0. SEMILLA GLOBAL DE ALEATORIEDAD

# ============================================================

# Usada para K-Means, división de datos y todos los modelos (RF, XGB, Ridge)

RANDOM_STATE = 42



# ============================================================

# 1. RUTAS DE ARCHIVOS Y DIRECTORIOS

# ============================================================

# Rutas de los archivos de entrada (usados en Celda 3)

DETALLE_FILES = [

    "/content/Detalle_Venta_2017_rellenado.xlsx",

    "/content/Detalle_Venta_2018_rellenado.xlsx",

    "/content/Detalle_Venta_2019_rellenado.xlsx",

    "/content/Detalle_Venta_2020_rellenado.xlsx",

    "/content/Detalle_Venta_2021_rellenado.xlsx",

    "/content/Detalle_Venta_2022_rellenado.xlsx",

    "/content/Detalle_Venta_2023_rellenado.xlsx",

    "/content/Detalle_Venta_2024_rellenado.xlsx",

    "/content/Detalle_Venta_2025_rellenado.xlsx"


]


LIBRO_FILES = [

    "/content/Libro_2017_rellenado.xlsx",

    "/content/Libro_2018_rellenado.xlsx",

    "/content/Libro_2019_rellenado.xlsx",

    "/content/Libro_2020_rellenado.xlsx",

    "/content/Libro_2021_rellenado.xlsx",

    "/content/Libro_2022_rellenado.xlsx",

    "/content/Libro_2023_rellenado.xlsx",

    "/content/Libro_2024_rellenado.xlsx",

    "/content/Libro_2025_rellenado.xlsx"

]


# Ruta del catálogo de categorías (usado en Celda 4.2)

RUTA_CATEGORIAS_JSON = 'catalogo_categorias.json'


# Directorio base para guardar modelos y metadatos (usado en Celda de Exportación)

BASE_EXPORT_DIR = 'models_export'



# ============================================================

# 2. PARÁMETROS DE NEGOCIO Y CLUSTERING

# ============================================================

# Cortes para análisis ABC (Usado en Celda 5.0)

ABC_CORTES = (0.80, 0.95)


# (Opcional) Cortes para análisis XYZ (Definido en Celda 2)

XYZ_CV_CORTES = (0.30, 0.80)


# Parámetros de Clustering (Usados en Celda 5.0)

KMEANS_K_OPTIMO_RANGE = range(2, 8) # Rango para buscar K óptimo

DBSCAN_EPS_PERCENTIL = 0.9          # Percentil para estimar 'eps'

DBSCAN_MIN_SAMPLES = 3              # Min_samples para DBSCAN



# ============================================================

# 3. PARÁMETROS DE LIMPIEZA Y NORMALIZACIÓN

# ============================================================

# Umbral para Fuzzy Matching (Usado en Celda 4.1)

FUZZY_THRESHOLD = 80


# Configuración de Embeddings (Usado en Celda 4.0 y 4.1)

USE_EMBEDDINGS = True

MODELO_EMBEDDING = 'paraphrase-multilingual-MiniLM-L12-v2'

EMBEDDING_THRESHOLD = 0.85 # Umbral de similitud semántica


# Factor de conversión para tornillos (Usado en Celda 4D)

FACTOR_CONVERSION_TORNILLOS = 1000



# ============================================================

# 4. PARÁMETROS DE MODELADO (SPLIT Y CV)

# ============================================================

# Fracción de datos para el conjunto de prueba (Usado en Celdas 7, 8, 10)

TEST_SIZE_FRAC = 0.2


# Número de divisiones para TimeSeriesSplit (Usado en Celda 7)

CV_SPLITS = 5



# ============================================================

# 5. HIPERPARÁMETROS DE MODELOS

# ============================================================


# --- 5.1. CLASIFICACIÓN (TAREA A - Ocurrencia) ---


# Método de balanceo (smotetomek, smoteenn, smote, none) (Usado en Celda 7)

BALANCEO_METHOD = 'smotetomek'


# Hiperparámetros RandomForest (Usados en Celda 10 - Simulación Final)

HPARAMS_RF_CLF = {

    'n_estimators': 100,

    'max_depth': 8,

    'random_state': RANDOM_STATE,

    'n_jobs': -1,

    'class_weight': 'balanced' # Manejo de desbalance si no se usa SMOTE

}


# Hiperparámetros XGBoost (Usados en Celda 7 - Comparación)

HPARAMS_XGB_CLF = {

    'n_estimators': 200,

    'max_depth': 6,

    'learning_rate': 0.1,

    'random_state': RANDOM_STATE,

    'eval_metric': 'logloss',

    'use_label_encoder': False

    # scale_pos_weight se calcula dinámicamente en la celda

}


# Hiperparámetros LightGBM (Usados en Celda 7 - Comparación)

HPARAMS_LGBM_CLF = {

    'n_estimators': 200,

    'max_depth': 6,

    'learning_rate': 0.1,

    'class_weight': 'balanced',

    'random_state': RANDOM_STATE,

    'verbose': -1

}



# --- 5.2. REGRESIÓN (TAREA B - Magnitud) ---


# Hiperparámetros Ridge (Usado en Celda 8 y 10 - Simulación Final)

HPARAMS_RIDGE_REG = {

    'alpha': 1.0,

    'random_state': RANDOM_STATE

}


# Hiperparámetros Gradient Boosting (Usado en Celda 8 - Comparación)

HPARAMS_GBR_REG = {

    'n_estimators': 150,

    'max_depth': 5,

    'learning_rate': 0.1,

    'random_state': RANDOM_STATE

}


# Hiperparámetros XGBoost Regressor (Usado en Celda 8 - Comparación)

HPARAMS_XGB_REG = {

    'n_estimators': 150,

    'max_depth': 6,

    'learning_rate': 0.1,

    'random_state': RANDOM_STATE,

    'n_jobs': -1

}



# ============================================================

# 6. PARÁMETROS DE SIMULACIÓN (TAREA D)

# ============================================================

# Factores (Alpha) para calcular el Stock de Seguridad (SS = Alpha * std_error)

COEFICIENTES_SS = [0, 1.0, 1.5]



# ============================================================

# 7. PARÁMETROS DE INTERPRETABILIDAD (SHAP)

# ============================================================

# Número de muestras a usar para los gráficos SHAP (para evitar OOM)

SHAP_MAX_SAMPLES = 500

# Número máximo de features a mostrar en los gráficos de importancia

SHAP_MAX_FEATURES = 20



print("="*60)

print("✅ CONFIGURACIÓN GLOBAL CARGADA")

print(f"   RANDOM_STATE = {RANDOM_STATE}")

print(f"   TEST_SIZE_FRAC = {TEST_SIZE_FRAC}")

print(f"   BALANCEO_METHOD = {BALANCEO_METHOD}")

print(f"   FUZZY_THRESHOLD = {FUZZY_THRESHOLD}")

print("="*60)


## ETL


### Preparacion del ETL


#### Importacion de Librerias


from configuracion_global import DETALLE_FILES, LIBRO_FILES

import sqlite3 # Librería para bases de datos SQLITE

from IPython.display import display # Necesario para mostrar dataframes en notebooks


#### Funciones y Validacion


# --- 1. FUNCIONES DE UTILIDAD Y VALIDACIÓN (SIN CAMBIOS) ---


def to_date(x):

    """Convierte el valor a tipo datetime, manejando errores."""

    try:

        return pd.to_datetime(x)

    except:

        return pd.NaT


def detect_year_from_path(path):

    """Detecta el año a partir del nombre del archivo.

      Un "asistente" que lee el nombre de los archivos para saber qué Detalle va con qué Libro

      """

    m = re.search(r"(20\d{2})", os.path.basename(path))

    return int(m.group(1)) if m else None


def read_detalle_strict(path):

    """Carga y valida estrictamente las columnas del Detalle de Venta."""

    df = pd.read_excel(path, sheet_name=0) # Asumiendo la primera hoja

    needed = ["ID_Venta","Producto","Cantidad","Unidad","Precio_Unitario_BS","Importe_Producto_BS"]

    if any(c not in df.columns for c in needed):

        raise ValueError(f"[Detalle] Faltan columnas críticas en {path}. Requeridas: {needed}")

    df = df[needed].copy()


    # Limpiar y convertir tipos de datos

    df["Producto"] = df["Producto"].astype(str).str.strip()

    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")

    df["Precio_Unitario_BS"] = pd.to_numeric(df["Precio_Unitario_BS"], errors="coerce")

    df["Importe_Producto_BS"] = pd.to_numeric(df["Importe_Producto_BS"], errors="coerce")


    # Eliminar filas donde no hay ID de Venta

    df = df.dropna(subset=["ID_Venta"])


    print(f"  [Detalle] Cargado {len(df)} filas de {os.path.basename(path)}")

    print(f"  [Detalle] IDs únicos: {df['ID_Venta'].nunique()}")

    return df


def read_libro_strict(path):

    """Carga y valida estrictamente las columnas del Libro/Encabezado."""

    df = pd.read_excel(path, sheet_name=0) # Asumiendo la primera hoja

    needed = ["ID_Venta","Fecha_Realizacion","Cliente","Asesor_Comercial",

              "Monto_USD","Monto_BS","Seguimiento","Motivo_Perdida","Tipo_Cliente"]

    if any(c not in df.columns for c in needed):

        raise ValueError(f"[Libro] Faltan columnas críticas en {path}. Requeridas: {needed}")

    df = df[needed].copy()


    # Eliminar filas donde no hay ID de Venta

    df = df.dropna(subset=["ID_Venta"])


    # Convertir fecha

    df["Fecha_Realizacion"] = df["Fecha_Realizacion"].map(to_date)


    print(f"  [Libro] Cargado {len(df)} filas de {os.path.basename(path)}")

    print(f"  [Libro] IDs únicos: {df['ID_Venta'].nunique()}")

    return df


def validate_merge(det, lib, merged, year):

    """Valida que el merge no haya perdido información crítica.

      Es el Auditor Final. Su trabajo es revisar el ensamblaje más tarde para asegurarse de que no perdimos dinero o productos en el proceso.

      """

    print(f"\n{'='*60}")

    print(f"VALIDACIÓN DE MERGE - AÑO {year}")

    print(f"{'='*60}")


    # 1. Verificar que todas las filas de detalle se conserven (usando left join)

    if len(merged) != len(det):

        print(f"⚠️  ALERTA: Filas en detalle={len(det):,}, pero merged={len(merged):,}")

    else:

        print(f"✓ Todas las {len(det):,} filas de detalle se conservaron")


    # 2. Identificar IDs de detalle que NO están en libro

    ids_detalle = set(det['ID_Venta'].unique())

    ids_libro = set(lib['ID_Venta'].unique())

    ids_sin_match = ids_detalle - ids_libro


    if ids_sin_match:

        print(f"⚠️  {len(ids_sin_match)} IDs de detalle SIN match en libro:")

        print(f"   {sorted(list(ids_sin_match))[:10]}{'...' if len(ids_sin_match) > 10 else ''}")


        # Contar cuántas filas afecta

        filas_sin_match = det[det['ID_Venta'].isin(ids_sin_match)]

        print(f"   Esto afecta a {len(filas_sin_match)} filas de detalle")

    else:

        print(f"✓ Todos los IDs de detalle tienen match en libro")


    # 3. Contar valores nulos en columnas críticas del merge

    columnas_libro = ["Fecha_Realizacion","Cliente","Asesor_Comercial"]

    nulos_por_columna = {}

    for col in columnas_libro:

        nulos = merged[col].isna().sum()

        nulos_por_columna[col] = nulos

        if nulos > 0:

            print(f"⚠️  {nulos:,} valores nulos en '{col}'")


    if all(n == 0 for n in nulos_por_columna.values()):

        print(f"✓ No hay valores nulos en columnas de libro")


    # 4. Verificar integridad de montos

    total_importe_detalle = det['Importe_Producto_BS'].sum()

    total_importe_merged = merged['Importe_Producto_BS'].sum()


    if abs(total_importe_detalle - total_importe_merged) < 0.01:

        print(f"✓ Suma de importes conservada: {total_importe_merged:,.2f} BS")

    else:

        print(f"⚠️  DIFERENCIA en importes:")

        print(f"   Detalle: {total_importe_detalle:,.2f} BS")

        print(f"   Merged:  {total_importe_merged:,.2f} BS")


    print(f"{'='*60}\n")


    return {

        'ids_sin_match': ids_sin_match,

        'filas_perdidas': len(det) - len(merged),

        'nulos_por_columna': nulos_por_columna

    }







### Creacion del Staging Area


#### Crear una Conexion SQlite temporaria (para realizar las consultas) **Staging Area**


# LOAD

# CONEXIÓN A LA BASE DE DATOS SQLITE (en memoria)

# Es una base de datos vacía, limpia y súper rápida porque vive en la memoria RAM.

DB_PATH = ':memory:'

conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_COLNAMES)

print(f"Conexión a DB SQLite establecida en {DB_PATH}")


reportes_validacion = {}

archivos_procesados = 0


for det_path in DETALLE_FILES:

    if not os.path.exists(det_path):

        print(f"[AVISO] ⚠️ Archivo de Detalle no existe: {os.path.basename(det_path)}. Omitiendo.")

        continue


    year = detect_year_from_path(det_path)

    libro_path = None


    # Buscar el archivo de Libro correspondiente al año

    for p in LIBRO_FILES:

        if os.path.exists(p) and str(year) in os.path.basename(p):

            libro_path = p

            break


    if libro_path is None:

        print(f"[AVISO] ⚠️ No encontré Libro para el año {year} ({os.path.basename(det_path)}). Omitiendo.")

        continue


    try:

        # Cargar archivos con validaciones estrictas

        det = read_detalle_strict(det_path)

        lib = read_libro_strict(libro_path)


        # MERGE con 'left' para NO perder ninguna fila de detalle

        merged = det.merge(

            lib[["ID_Venta","Fecha_Realizacion","Cliente","Asesor_Comercial",

                 "Monto_USD","Monto_BS","Seguimiento","Motivo_Perdida","Tipo_Cliente"]],

            on="ID_Venta",

            how="left",  # LEFT mantiene TODAS las filas de detalle

            validate="m:1",  # Valida que sea many-to-one (muchos detalles, un libro)

            indicator=True  # Agrega columna '_merge' para diagnosticar

        )


        print(f"  [Merge] Fusionado Detalle y Libro para {year}. Filas: {len(merged):,}")


        # Validar el merge

        reporte = validate_merge(det, lib, merged, year)

        reportes_validacion[year] = reporte


        # Diagnóstico con indicator

        merge_stats = merged['_merge'].value_counts()

        print(f"  [Diagnóstico _merge]:")

        for estado, count in merge_stats.items():

            print(f"    {estado}: {count:,}")


        # Eliminar columna de diagnóstico

        merged = merged.drop(columns=['_merge'])


        # === INSERCIÓN A LA BASE DE DATOS ===

        # Se usa 'append' para agregar datos al final de la tabla 'ventas_unificadas'

        merged.to_sql(

            'ventas_unificadas',

            conn,

            if_exists='append',

            index=False,

            method='multi',

            chunksize=10000

        )

        print(f"  [DB] ✅ Datos de {year} insertados en la tabla 'ventas_unificadas'.")

        archivos_procesados += 1


    except ValueError as ve:

        print(f"❌ ERROR: Falló la validación estricta para el año {year}: {ve}")

    except Exception as e:

        print(f"❌ ERROR inesperado en el procesamiento de archivos para {year}: {e}")



### Creacion del Dataframe Ventas y reportes


Ahora creamos nuestro producto final: el DataFrame ventas


if archivos_procesados > 0:

    # Leer toda la data de la DB a un DataFrame final

    sql_query = "SELECT * FROM ventas_unificadas" # EXTRACT (Consolidación)


    """BASICAMENTE AQUI ES DONDE EXTRAE TODOS LOS ARCHIVOS QUE COLOCASTE EN EL COLAB

       Y CONTIENEN EL FORMATO CORRECTO PARA CREAR EL DATAFRAME

    """

    ventas = pd.read_sql(sql_query, conn)

    print(f"\n[DB Read]  Datos leídos de 'ventas_unificadas'. Filas totales: {len(ventas):,}")


    # Limpieza de fechas (ahora con los datos leídos de la DB)

    initial_rows = len(ventas)

    # Renombrar para usar 'Fecha' como columna principal para el pipeline

    ventas = ventas.rename(columns={'Fecha_Realizacion': 'Fecha'}) # TRANSFORM (Estandarización y Limpieza)

    ventas["Fecha"] = ventas["Fecha"].map(to_date)

    ventas = ventas.dropna(subset=["Fecha"]).copy()

    rows_after_dropna = len(ventas)

    print(f"[Clean]  Filas después de eliminar nulos en Fecha: {rows_after_dropna:,}")

    print(f"        Descartadas: {initial_rows - rows_after_dropna:,}")




> Aquí es donde creamos nuevas columnas que le dan "inteligencia" a nuestros datos para el análisis



    # Crear columnas adicionales

    ventas["Total_BS"] = ventas["Importe_Producto_BS"]

    # Corregir la columna "Mes" para ser el inicio del mes

    ventas["Mes"] = ventas["Fecha"].dt.to_period("M").dt.to_timestamp()

    ventas["Año"] = ventas["Fecha"].dt.year


#### Reporte del Mergeo



    print("REPORTE FINAL DE CARGA Y MERGEO")

    print(f"{'='*70}")

    print(f"Total filas finales: {len(ventas):,}")

    print(f"Rango de fechas: {ventas['Fecha'].min()} a {ventas['Fecha'].max()}")

    print(f"IDs de venta únicos: {ventas['ID_Venta'].nunique():,}")

    print(f"Productos únicos: {ventas['Producto'].nunique():,}")

    print(f"Total ventas en BS: {ventas['Total_BS'].sum():,.2f}")

    print(f"\nDistribución por año (Filas de Detalle):")

    print(ventas['Año'].value_counts().sort_index())

    print(f"{'='*70}\n")


    # Mostrar muestra

    print("Vista rápida de los datos:")

    display(ventas.head(8))


    # Verificar integridad final

    print("\n[Verificación de Integridad]")

    print(f"Filas con Cliente nulo: {ventas['Cliente'].isna().sum():,}")

    print(f"Filas con Asesor nulo: {ventas['Asesor_Comercial'].isna().sum():,}")

    print(f"Filas con Fecha nula: {ventas['Fecha'].isna().sum():,}")


    # Si hay IDs sin match, mostrar ejemplo

    ids_sin_info = ventas[ventas['Cliente'].isna()]

    if len(ids_sin_info) > 0:

        print(f"\n⚠️ Ejemplo de {len(ids_sin_info):,} filas sin info de libro:")

        display(ids_sin_info[['ID_Venta','Producto','Importe_Producto_BS','Cliente']].head())




### Cerrar la conexion SQlite con el Staging area



# ==============================================================================

# 4. CERRAR CONEXIÓN Y LIMPIAR RECURSOS

# ==============================================================================

# Es una buena práctica liberar el recurso de memoria al finalizar el uso de la DB.

if 'conn' in locals() and conn:

    conn.close()

    print("\n✅ Conexión a base de datos (en memoria) cerrada.")


## PRUEBA DE BASE DE DATOS SQLITE



# Celda 2 — Configuración

DETALLE_FILES = ["/content/Detalle_Venta_2022_rellenado.xlsx",

                 "/content/Detalle_Venta_2023_rellenado.xlsx",

                 "/content/Detalle_Venta_2024_rellenado.xlsx",

                 "/content/Detalle_Venta_2025_rellenado.xlsx"]

LIBRO_FILES   = ["/content/Libro_2022_rellenado.xlsx",

                 "/content/Libro_2023_rellenado.xlsx",

                 "/content/Libro_2024_rellenado.xlsx",

                 "/content/Libro_2025_rellenado.xlsx"]

ABC_CORTES     = (0.80, 0.95)

XYZ_CV_CORTES  = (0.30, 0.80)

KMEANS_K       = 3

USAR_KMEANS    = True

PRIORIZA_ALTA  = True

UMBRAL_FUZZY   = 90



# Celda 3 — Carga Detalle/Libro con Validaciones Completas


def to_date(x):

    try:

        return pd.to_datetime(x)

    except:

        return pd.NaT


def detect_year_from_path(path):

    m = re.search(r"(20\d{2})", os.path.basename(path))

    return int(m.group(1)) if m else None


def read_detalle_strict(path):

    df = pd.read_excel(path)

    needed = ["ID_Venta","Producto","Cantidad","Unidad","Precio_Unitario_BS","Importe_Producto_BS"]

    if any(c not in df.columns for c in needed):

        raise ValueError(f"[Detalle] Faltan columnas en {path}")

    df = df[needed].copy()


    # Limpiar datos

    df["Producto"] = df["Producto"].astype(str).str.strip()

    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")

    df["Precio_Unitario_BS"] = pd.to_numeric(df["Precio_Unitario_BS"], errors="coerce")

    df["Importe_Producto_BS"] = pd.to_numeric(df["Importe_Producto_BS"], errors="coerce")


    # Eliminar filas completamente vacías

    df = df.dropna(subset=["ID_Venta"])


    print(f"  [Detalle] Cargado {len(df)} filas de {path}")

    print(f"  [Detalle] IDs únicos: {df['ID_Venta'].nunique()}")

    return df


def read_libro_strict(path):

    df = pd.read_excel(path)

    needed = ["ID_Venta","Fecha_Realizacion","Cliente","Asesor_Comercial",

              "Monto_USD","Monto_BS","Seguimiento","Motivo_Perdida","Tipo_Cliente"]

    if any(c not in df.columns for c in needed):

        raise ValueError(f"[Libro] Faltan columnas en {path}")

    df = df[needed].copy()


    # Eliminar filas completamente vacías

    df = df.dropna(subset=["ID_Venta"])


    df["Fecha_Realizacion"] = df["Fecha_Realizacion"].map(to_date)


    print(f"  [Libro] Cargado {len(df)} filas de {path}")

    print(f"  [Libro] IDs únicos: {df['ID_Venta'].nunique()}")

    return df


def validate_merge(det, lib, merged, year):

    """Valida que el merge no haya perdido información crítica"""

    print(f"\n{'='*60}")

    print(f"VALIDACIÓN DE MERGE - AÑO {year}")

    print(f"{'='*60}")


    # 1. Verificar que todas las filas de detalle se conserven

    if len(merged) != len(det):

        print(f"⚠️  ALERTA: Filas en detalle={len(det)}, pero merged={len(merged)}")

    else:

        print(f"✓ Todas las {len(det)} filas de detalle se conservaron")


    # 2. Identificar IDs de detalle que NO están en libro

    ids_detalle = set(det['ID_Venta'].unique())

    ids_libro = set(lib['ID_Venta'].unique())

    ids_sin_match = ids_detalle - ids_libro


    if ids_sin_match:

        print(f"⚠️  {len(ids_sin_match)} IDs de detalle SIN match en libro:")

        print(f"   {sorted(list(ids_sin_match))[:10]}{'...' if len(ids_sin_match) > 10 else ''}")


        # Contar cuántas filas afecta

        filas_sin_match = det[det['ID_Venta'].isin(ids_sin_match)]

        print(f"   Esto afecta a {len(filas_sin_match)} filas de detalle")

    else:

        print(f"✓ Todos los IDs de detalle tienen match en libro")


    # 3. Contar valores nulos en columnas críticas del merge

    columnas_libro = ["Fecha_Realizacion","Cliente","Asesor_Comercial"]

    nulos_por_columna = {}

    for col in columnas_libro:

        nulos = merged[col].isna().sum()

        nulos_por_columna[col] = nulos

        if nulos > 0:

            print(f"⚠️  {nulos} valores nulos en '{col}'")


    if all(n == 0 for n in nulos_por_columna.values()):

        print(f"✓ No hay valores nulos en columnas de libro")


    # 4. Verificar integridad de montos

    total_importe_detalle = det['Importe_Producto_BS'].sum()

    total_importe_merged = merged['Importe_Producto_BS'].sum()


    if abs(total_importe_detalle - total_importe_merged) < 0.01:

        print(f"✓ Suma de importes conservada: {total_importe_merged:,.2f} BS")

    else:

        print(f"⚠️  DIFERENCIA en importes:")

        print(f"   Detalle: {total_importe_detalle:,.2f} BS")

        print(f"   Merged:  {total_importe_merged:,.2f} BS")


    print(f"{'='*60}\n")


    return {

        'ids_sin_match': ids_sin_match,

        'filas_perdidas': len(det) - len(merged),

        'nulos_por_columna': nulos_por_columna

    }


# Rutas de archivos

DETALLE_FILES = ["/content/Detalle_Venta_2022_rellenado.xlsx",

                 "/content/Detalle_Venta_2023_rellenado.xlsx",

                 "/content/Detalle_Venta_2024_rellenado.xlsx",

                 "/content/Detalle_Venta_2025_rellenado.xlsx"]

LIBRO_FILES   = ["/content/Libro_2022_rellenado.xlsx",

                 "/content/Libro_2023_rellenado.xlsx",

                 "/content/Libro_2024_rellenado.xlsx",

                 "/content/Libro_2025_rellenado.xlsx"]


frames = []

reportes_validacion = {}


for det_path in DETALLE_FILES:

    if not os.path.exists(det_path):

        print(f"[AVISO] No existe detalle: {det_path}")

        continue


    year = detect_year_from_path(det_path)

    libro_path = None


    for p in LIBRO_FILES:

        if os.path.exists(p) and str(year) in os.path.basename(p):

            libro_path = p

            break


    if libro_path is None:

        print(f"[AVISO] No encontré Libro para {det_path}.")

        continue


    # Cargar archivos

    det = read_detalle_strict(det_path)

    lib = read_libro_strict(libro_path)


    # MERGE con 'left' para NO perder ninguna fila de detalle

    merged = det.merge(

        lib[["ID_Venta","Fecha_Realizacion","Cliente","Asesor_Comercial",

             "Monto_USD","Monto_BS","Seguimiento","Motivo_Perdida","Tipo_Cliente"]],

        on="ID_Venta",

        how="left",  # LEFT mantiene TODAS las filas de detalle

        validate="m:1",  # Valida que sea many-to-one (muchos detalles, un libro)

        indicator=True  # Agrega columna '_merge' para diagnosticar

    )


    print(f"  [Merge] Fusionado Detalle y Libro para {year}. Filas: {len(merged)}")


    # Validar el merge

    reporte = validate_merge(det, lib, merged, year)

    reportes_validacion[year] = reporte


    # Diagnóstico con indicator

    merge_stats = merged['_merge'].value_counts()

    print(f"  [Diagnóstico _merge]:")

    for estado, count in merge_stats.items():

        print(f"    {estado}: {count}")


    # Eliminar columna de diagnóstico

    merged = merged.drop(columns=['_merge'])


    frames.append(merged)


# Concatenar todos los años

ventas = pd.concat(frames, ignore_index=True)

print(f"\n[Concat] Concatenado años. Filas totales: {len(ventas)}")


# Limpieza de fechas

initial_rows = len(ventas)

ventas["Fecha"] = ventas["Fecha_Realizacion"].map(to_date)

ventas = ventas.dropna(subset=["Fecha"]).copy()

rows_after_dropna = len(ventas)

print(f"[Clean] Filas después de eliminar nulos en Fecha: {rows_after_dropna}")

print(f"        Descartadas: {initial_rows - rows_after_dropna}")


# Crear columnas adicionales

ventas["Total_BS"] = ventas["Importe_Producto_BS"]

ventas["Mes"] = ventas["Fecha"].dt.to_period("M").dt.to_timestamp()

ventas["Año"] = ventas["Fecha"].dt.year


# REPORTE FINAL

print(f"\n{'='*70}")

print("REPORTE FINAL DE MERGEO")

print(f"{'='*70}")

print(f"Total filas finales: {len(ventas):,}")

print(f"Rango de fechas: {ventas['Fecha'].min()} a {ventas['Fecha'].max()}")

print(f"IDs de venta únicos: {ventas['ID_Venta'].nunique():,}")

print(f"Productos únicos: {ventas['Producto'].nunique():,}")

print(f"Total ventas en BS: {ventas['Total_BS'].sum():,.2f}")

print(f"\nDistribución por año:")

print(ventas['Año'].value_counts().sort_index())

print(f"{'='*70}\n")


# Mostrar muestra

print("Vista rápida de los datos:")

display(ventas.head(8))


# Verificar integridad final

print("\n[Verificación de Integridad]")

print(f"Filas con Cliente nulo: {ventas['Cliente'].isna().sum()}")

print(f"Filas con Asesor nulo: {ventas['Asesor_Comercial'].isna().sum()}")

print(f"Filas con Fecha nula: {ventas['Fecha'].isna().sum()}")


# Si hay IDs sin match, mostrar ejemplo

ids_sin_info = ventas[ventas['Cliente'].isna()]

if len(ids_sin_info) > 0:

    print(f"\n⚠️ Ejemplo de {len(ids_sin_info)} filas sin info de libro:")

    display(ids_sin_info[['ID_Venta','Producto','Importe_Producto_BS','Cliente']].head())


## Exploracion de Datos (EDA)


### Preparacion EDA


# Configuración de estilo

sns.set(style="whitegrid")

warnings.filterwarnings('ignore')


# --- Verificación de Datos ---

if 'ventas' not in locals():

    # Esta es la forma robusta: detiene la celda si 'ventas' no existe.

    raise NameError(

        "❌ ERROR: No se encuentra el DataFrame 'ventas'. "

        "Por favor, ejecuta la 'Celda 3 - Carga y Unificación' primero."

    )

else:

    print(f"\n✅ DataFrame 'ventas' encontrado. {len(ventas):,} filas listas para analizar.")

    print(f"   Rango de fechas: {ventas['Fecha'].min().date()} a {ventas['Fecha'].max().date()}")



### Analisis de Nulos y Distribuicion



#### Informacion General de Tipos de datos y Nulos


print("\n[1.1] Información General del DataFrame (Tipos y Nulos):")

# .info() nos muestra los tipos de datos y cuántos valores no nulos hay.

ventas.info()


#### Resumen Estadístico de Variables Numéricas


# .describe() nos da la media, desviación estándar, min, max y percentiles.

# Útil para detectar outliers (ej. una 'Cantidad' de 99999).

display(ventas[['Cantidad', 'Precio_Unitario_BS', 'Total_BS', 'Monto_BS']].describe().apply(lambda s: s.apply('{:,.2f}'.format)))



#### Cantidad de Cotizaciones que acabaron en Efectuada o Perdida (Seguimiento)


# --- 1.3. Distribución del Target de Negocio (Seguimiento) ---

print("\n[1.3] Distribución de Ventas (Efectuadas vs. Perdidas):")

# ¿Cuántas ventas cerramos vs. cuántas perdimos?

plt.figure(figsize=(10, 5))

sns.countplot(

    data=ventas,

    x='Seguimiento',

    palette={'EFECTUADA': 'g', 'PERDIDA': 'r'},

    order=ventas['Seguimiento'].value_counts().index

)

plt.title('Distribución de Ventas: Efectuadas vs. Perdidas', fontsize=16)

plt.ylabel('Conteo de Filas (Productos)')

plt.xlabel('Estado del Seguimiento')

plt.show()



#### EL mejor Asesor Comercial (Tasa de Éxito (Conversión) por Asesor)




# Calcular el conteo total de oportunidades (filas) por asesor

conteo_total = ventas['Asesor_Comercial'].value_counts()


# Calcular el conteo de éxitos (EFECTUADA) por asesor

conteo_exito = ventas[ventas['Seguimiento'] == 'EFECTUADA']['Asesor_Comercial'].value_counts()


# Calcular la tasa de éxito (evitando división por cero)

tasa_exito = (conteo_exito.reindex(conteo_total.index, fill_value=0) / conteo_total) * 100


# --- Filtrado ---

# Filtramos asesores con pocas oportunidades para un análisis más justo

min_oportunidades = 20

tasa_exito_filtrada = tasa_exito[conteo_total > min_oportunidades].sort_values(ascending=False)


plt.figure(figsize=(12, 8))


# Crear el gráfico de barras

ax = sns.barplot(

    x=tasa_exito_filtrada.values,

    y=tasa_exito_filtrada.index,

    palette='viridis_r' # 'viridis_r' (verde para alto, azul para bajo)

)


plt.title(f'Tasa de Éxito (%) por Asesor (con > {min_oportunidades} oportunidades)', fontsize=16)

plt.xlabel('Tasa de Éxito (%)')

plt.ylabel('Asesor Comercial')


# Añadir etiquetas de porcentaje (%)

for p in ax.patches:

    width = p.get_width()

    ax.text(

        width + 0.5, # Posición X (un poco a la derecha)

        p.get_y() + p.get_height() / 2, # Posición Y (centrado)

        f'{width:.1f}%', # Texto con 1 decimal

        va='center',

        ha='left',

        fontsize=10

    )


ax.set_xlim(right=ax.get_xlim()[1] * 1.1) # Espacio para etiquetas

plt.show()

print(f"NOTA: Este gráfico muestra la eficiencia. Un asesor puede tener pocas ventas (Top 10 Asesores) pero una alta tasa de éxito.")



#### Distribuicion de las variables Numericas


print("\n[1.5] Distribución de 'Total_BS' (Importe por Producto):")

# ¿Cómo se distribuyen los valores de los productos?

plt.figure(figsize=(12, 6))

sns.histplot(

    ventas['Total_BS'],

    bins=50,

    kde=True

)

plt.title('Distribución del Valor por Producto (Total_BS)', fontsize=16)

plt.xlabel('Valor en BS')

plt.ylabel('Frecuencia')

# La mayoría de los valores están pegados a 0. Esto es un 'skew' (sesgo) extremo.

# Usamos una escala logarítmica para ver la distribución real.

plt.xscale('log')

plt.xlabel('Valor en BS (Escala Logarítmica)')

plt.show()

print("NOTA: El histograma muestra un fuerte sesgo a la derecha (long-tail).")

print("La mayoría de los productos tienen un valor bajo, con unos pocos outliers de valor muy alto.")

print("Esto justifica la necesidad de un Análisis ABC (Celda 5) para segmentarlos.")



> **DISTRIBUCIONES:**


 * Las ventas (BS) y cantidades están **extremadamente sesgadas** (sesgo a la derecha). La gran mayoría de las ventas son de bajo valor, con unas pocas ventas de valor muy alto.






* Esto **justifica plenamente** la necesidad del **Análisis ABC (Celda 5)** para separar los productos "A" (vitales) de los "C" (triviales).






### ANÁLISIS BIVARIADO (Relaciones entre variables)


#### ¿Quiénes son los asesores que más venden (en BS)


print("\n[2.1] Total de Ventas (BS) por Asesor (Top 10):")

# Agrupamos por asesor y sumamos el 'Total_BS' solo de ventas 'EFECTUADA'

ventas_efectuadas = ventas[ventas['Seguimiento'] == 'EFECTUADA']

asesor_ventas_bs = ventas_efectuadas.groupby('Asesor_Comercial')['Total_BS'].sum().sort_values(ascending=False).head(10)


plt.figure(figsize=(12, 6))

ax_bs = sns.barplot(

    x=asesor_ventas_bs.values,

    y=asesor_ventas_bs.index,

    palette='viridis'

)

plt.title('Top 10 Asesores por Total de Ventas (BS) Efectuadas', fontsize=16)

plt.xlabel('Total Vendido (BS)')

plt.ylabel('Asesor Comercial')

# Formatear el eje X para mostrar moneda (sigue siendo útil)

ax_bs.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Bs {x:,.0f}'))


# --- INICIO DE LA MODIFICACIÓN: Añadir etiquetas de datos ---

# Añadir etiquetas de datos (el valor en Bs)

for p in ax_bs.patches:

    width = p.get_width() # El valor en BS

    ax_bs.text(

        width + (ax_bs.get_xlim()[1] * 0.01), # Posición X (un poco a la derecha)

        p.get_y() + p.get_height() / 2,     # Posición Y (centro de la barra)

        f'Bs {width:,.0f}',                  # El texto (formateado)

        va='center',                         # Alineación vertical

        ha='left',                           # Alineación horizontal

        fontsize=9,

        color='black'

    )


# Ajustar el límite X para dar espacio a las etiquetas

ax_bs.set_xlim(right=ax_bs.get_xlim()[1] * 1.15)

# --- FIN DE LA MODIFICACIÓN ---


plt.show()


#### ¿Por qué perdemos ventas?


# --- 2.2. ¿Por qué perdemos ventas? ---

print("\n[2.2] Principales Motivos de Pérdida:")

# (Asume que ejecutaste la Celda 3.5 de limpieza de motivos)

plt.figure(figsize=(12, 7))

ax_mot = sns.countplot(

    data=ventas[ventas['Seguimiento'] == 'PERDIDA'],

    y='Motivo_Perdida',

    order=ventas[ventas['Seguimiento'] == 'PERDIDA']['Motivo_Perdida'].value_counts().iloc[:15].index, # Top 15

    palette='Reds_r'

)

plt.title('Top 15 Motivos de Venta Perdida', fontsize=16)

plt.xlabel('Conteo')

plt.ylabel('Motivo de Pérdida')

# Añadir etiquetas

for p in ax_mot.patches:

    ax_mot.annotate(f'{int(p.get_width())}',

                   (p.get_width() + 3, p.get_y() + p.get_height() / 2),

                   va='center',

                   ha='left',

                   fontsize=9)

ax_mot.set_xlim(right=ax_mot.get_xlim()[1] * 1.1)

plt.show()



### ANÁLISIS TEMPORAL (Tendencias y Estacionalidad)


#### ¿Cómo han evolucionado las ventas (BS) en el tiempo?


print("\n[3.1] Tendencia de Ventas (BS) Totales por Mes:")

# Agrupamos por la columna 'Mes' que creamos en el ETL

ventas_por_mes = ventas[ventas['Seguimiento'] == 'EFECTUADA'].groupby('Mes')['Total_BS'].sum()


plt.figure(figsize=(16, 7))

ax_trend = ventas_por_mes.plot(

    linewidth=2,

    marker='o',

    linestyle='-',

    color='blue'

)

plt.title('Ventas Mensuales (BS) a lo largo del Tiempo', fontsize=16)

plt.xlabel('Fecha (Mes)')

plt.ylabel('Total Vendido (BS)')

ax_trend.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Bs {x:,.0f}'))

plt.show()



#### ¿Cómo ha evolucionado el CONTEO de ventas en el tiempo?


# --- 3.2. ¿Cómo ha evolucionado el CONTEO de ventas en el tiempo? ---

print("\n[3.2] Tendencia del Conteo de Ventas (Transacciones) por Mes:")

# Agrupamos por 'Mes' y contamos los ID_Venta únicos

conteo_ventas_por_mes = ventas[ventas['Seguimiento'] == 'EFECTUADA'].groupby('Mes')['ID_Venta'].nunique()


plt.figure(figsize=(16, 7))

conteo_ventas_por_mes.plot(

    linewidth=2,

    marker='o',

    linestyle='-',

    color='green'

)

plt.title('Conteo de Ventas Mensuales (Transacciones Únicas) a lo largo del Tiempo', fontsize=16)

plt.xlabel('Fecha (Mes)')

plt.ylabel('Número de Ventas Únicas')

plt.show()



#### ¿Existe estacionalidad? (Heatmap)


# --- 3.3. ¿Existe estacionalidad? (Heatmap) ---

print("\n[3.3] Heatmap de Estacionalidad (Ventas por Mes y Año):")

# Creamos una tabla pivote

# Usamos .copy() para evitar el SettingWithCopyWarning

ventas_efectuadas_copy = ventas[ventas['Seguimiento'] == 'EFECTUADA'].copy()

ventas_efectuadas_copy['mes_num'] = ventas_efectuadas_copy['Fecha'].dt.month

heatmap_data = pd.pivot_table(

    ventas_efectuadas_copy,

    values='Total_BS',

    index='Año',

    columns='mes_num',

    aggfunc='sum'

)

# Renombrar columnas para claridad

heatmap_data.columns = [

    'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',

    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'

]


plt.figure(figsize=(14, 7))

sns.heatmap(

    heatmap_data,

    annot=True,

    fmt=",.0f", # Formato de miles sin decimales

    cmap="YlGnBu", # Paleta de color (Yellow-Green-Blue)

    linewidths=.5,

    annot_kws={"size": 10} # Ajustar tamaño de fuente

)

plt.title('Heatmap de Estacionalidad: Ventas Totales (BS) por Mes y Año', fontsize=16)

plt.xlabel('Mes')

plt.ylabel('Año')

plt.show()

print("NOTA: El heatmap es perfecto para ver patrones. ¿Es Diciembre siempre bajo? ¿Es Agosto siempre alto?")



> **PATRONES TEMPORALES:**


* Los gráficos de series temporales (lineplot y heatmap) muestran **tendencias y posible estacionalidad** (ej. picos o valles en ciertos meses).

* Esto confirma que usar features basados en el tiempo (como 'mes', 'trimestre', 'lags') en nuestros modelos de ML (Celda 7) es la estrategia correcta.







# 📁 FASE 3: Preparación de los Datos

### ✔️ Normalización de Productos

Se aplica un proceso de limpieza y un diccionario maestro (`catalogo`) para consolidar productos con nombres similares.


### ✔️ Clasificación por Categoría Funcional

Basado en reglas textuales usando palabras clave del nombre del producto.


### ✔️ Series Temporales

- Se completan periodos faltantes

- Se generan series mensuales, trimestrales y semanales


Resultado: dataset limpio y estructurado para análisis y modelado.


---

Aquí agrupamos toda la parte de normalización de productos, Limpiar, transformar y crear variables


## Limpieza


### Evaluando Motivos de Perdida de las cotizaciones


    pd.set_option('display.max_rows', None)


    # 2. Imprime la lista completa

    display(ventas['Motivo_Perdida'].value_counts(dropna=False))


    # 3. Resetea la configuración para no afectar otras celdas

    pd.reset_option('display.max_rows')


> **Observaciones**


- None: 5327 datos

  >Datos nulos. Definitivamente es 'inválido' para el análisis.

- cambio de sistema     508

  >Es cuando el cliente cambio de opinion y opto por otro tipo de materiales de construccion generalmente al de tradicional

- por falta de stock     461

  >Es cuando falta el stock que solicita el cliente de algun producto que cotizó

- muy caro     284

  >Es cuando el cliente decide que es muy caro y retrocede en la compra

- competencia     279

  >Es cuando perdemos el cliente por la competencia




---





**Existen valores invalidos como motivo de perdida:**

* NO ENTENDI

* cuellar

* compro con rafa

* esta comprando 90 placas a la semana

* termine de comprar

* esta semana

* hasta julio

* "****"

* *espacios*



**Motivos clasicos de "voy a volvere" , "llamare" "esperare confirmacion del cliente"**

* llamaran, llamara, llamara en agosto, llamara en septiembre, esperar llamada

* nos avisara

* volvera a llamar

* ira consultar

* respuesta del cliente

* vendra outra fecha

* llamara en 10 dias

* lo veran

* de la respuesta del cliente

* respuesta del dueño

* de contabilidad

* el cliente confirmara

* de la gerencia

* por confirmar

* cliente confirmacion

* su cliente esperar

* su cliente va confirmar

* autorizacion

* aprobacion del cliente

* pase bloqueo

* hasta regularizar

* item por regularizar en obra



### Cambiar los valores invalidos por NO ESPECIFICADO


print("\nPASO 1: Limpiando 'Motivo_Perdida' (Ventas PERDIDA)...")


valores_ruido = [

    'NO ENTENDI',

    'cuellar',

    'compro con rafa',

    'esta comprando 90 placas a la semana',

    'termine de comprar',

    'esta semana',

    'hasta julio',

    '****',

    ' ' # Espacio en blanco

]


# Crear los filtros

filas_perdida = ventas['Seguimiento'] == 'PERDIDA'

filas_con_nan = ventas['Motivo_Perdida'].isna()

filas_invalidas = ventas['Motivo_Perdida'].isin(valores_ruido)


# Combinar filtros

# (PERDIDA) Y ( (Nulas) O (Inválidas) )

filas_a_limpiar_mask = filas_perdida & (filas_con_nan | filas_invalidas)


#  Aplicar la limpieza

# Rellenamos todos los NaN y ruido con 'No Especificado'

ventas.loc[filas_a_limpiar_mask, 'Motivo_Perdida'] = 'No Especificado'


print(f"✅ 'Motivo_Perdida' limpiado. {filas_a_limpiar_mask.sum():,} filas rellenadas con 'No Especificado'.")




# Filtro: Ventas exitosas Y que tengan el motivo vacío

filas_efectuada_mask = (ventas['Seguimiento'] == 'EFECTUADA') & (ventas['Motivo_Perdida'].isna())


# Aplicar la etiqueta 'NO REQUIERE'

ventas.loc[filas_efectuada_mask, 'Motivo_Perdida'] = 'NO REQUIERE'


print(f" 'Motivo_Perdida' etiquetado. {filas_efectuada_mask.sum():,} filas 'EFECTUADA' marcadas como 'NO REQUIERE'.")


print("\nVista rápida de 'Motivo_Perdida' (limpio):")

display(ventas['Motivo_Perdida'].value_counts(dropna=False).head(10))


### Columna Tipo_cliente


# --- Diagnóstico: Conteo de Valores ---

print("\n--- Conteo de Valores Únicos en 'Tipo_Cliente' (Antes de la Limpieza) ---")


# Forzar a Pandas a mostrar TODAS las filas (None = ilimitado)

# Esto es para replicar cómo vimos los 121 motivos de pérdida.

pd.set_option('display.max_rows', None)


# Usamos value_counts(dropna=False) para asegurarnos de que veamos los 'NaN'

display(ventas['Tipo_Cliente'].value_counts(dropna=False))


# Resetear la opción a su valor por defecto

pd.reset_option('display.max_rows')


#### Limpieza y Estandarizacion de Tipo_cliente


print("   > Acción: Unificando 'EMPRESA', 'empresa', 'Empresa' -> 'empresa'")

print(f"   > Acción: Rellenando {ventas['Tipo_Cliente'].isna().sum()} 'None' (NaN) -> 'cliente particular'")


# 1. Unificar duplicados (EMPRESA, empresa, Empresa -> 'empresa')

#    .str.lower() convierte todo a minúsculas (ej. 'EMPRESA' -> 'empresa')

#    .str.strip() elimina espacios en blanco al inicio/fin si los hubiera

#    .fillna() es crucial para reemplazar los 'None' con 'cliente particular'

ventas['Tipo_Cliente'] = ventas['Tipo_Cliente'].str.lower().str.strip().fillna('cliente particular')


# 2. Reporte final del paso

print("\n   > Distribución final de 'Tipo_Cliente' (Limpiada):")

display(ventas['Tipo_Cliente'].value_counts(dropna=False))



#### Creacion de la columna de Comportamiento


print("\n" + "="*70)

print("PASO 3: (NUEVO) Creando 'Tipo_Comportamiento' (Behavioral)")

print("="*70)


# 3.1. Calcular el historial de compras por cliente

# Contamos cuántas transacciones 'EFECTUADA' tiene cada cliente

print("   > Analizando historial de compras por 'Cliente'...")

ventas['venta_exitosa'] = (ventas['Seguimiento'] == 'EFECTUADA').astype(int)


# Agrupamos por Cliente y contamos compras exitosas y cotizaciones totales (basado en ID_Venta únicos)

perfil_cliente = ventas.groupby('Cliente').agg(

    compras_exitosas=('venta_exitosa', 'sum'),

    total_cotizaciones=('ID_Venta', 'nunique')

)


# 3.2. Definir las reglas de negocio

def asignar_comportamiento(row):

    if row['compras_exitosas'] > 1:

        return 'Cliente Recurrente'

    elif row['compras_exitosas'] == 1:

        return 'Cliente Nuevo'

    elif row['compras_exitosas'] == 0 and row['total_cotizaciones'] > 0:

        return 'Cliente Potencial' # Solo cotizó, nunca compró

    else:

        return 'Indefinido' # Casos extraños


print("   > Asignando etiquetas: 'Cliente Recurrente', 'Cliente Nuevo', 'Cliente Potencial'...")

perfil_cliente['Tipo_Comportamiento'] = perfil_cliente.apply(asignar_comportamiento, axis=1)


# 3.3. Mapear los resultados de vuelta al DataFrame principal

ventas['Tipo_Comportamiento'] = ventas['Cliente'].map(perfil_cliente['Tipo_Comportamiento'])


# 3.4. Reporte final del paso

print("\n   > Distribución final de 'Tipo_Comportamiento' (Creada):")

display(ventas['Tipo_Comportamiento'].value_counts(dropna=False))



### Crear otra columna para tener una variable de recurrencia de los clientes


print("\nPASO 2: Enriqueciendo 'Tipo_Cliente'...")


# 2.1. Calcular el historial de compras

# Agrupamos por 'Cliente' y contamos cuántas ventas 'EFECTUADA' únicas tienen

# Usamos .drop_duplicates() para contar transacciones, no productos

historial_compras = ventas[ventas['Seguimiento'] == 'EFECTUADA'].drop_duplicates(subset=['ID_Venta', 'Cliente'])

conteo_compras = historial_compras['Cliente'].value_counts()


# 2.2. Mapear conteos a la columna 'Tipo_Cliente'

# .map() asignará el número de compras a cada fila basado en el 'Cliente'

ventas['conteo_temporal'] = ventas['Cliente'].map(conteo_compras)


# 2.3. Definir la lógica de asignación

def asignar_tipo_cliente(row):

    conteo = row['conteo_temporal']

    seguimiento = row['Seguimiento']


    if pd.isna(conteo) or conteo == 0:

        # Si no tiene compras (NaN) y su seguimiento es PERDIDA

        if seguimiento == 'PERDIDA':

            return 'Cliente Potencial'

        else:

            return 'Indefinido' # Casos raros

    elif conteo == 1:

        return 'Cliente Nuevo'

    elif conteo > 1:

        return 'Cliente Recurrente'

    else:

        return 'Indefinido'


# 2.4. Aplicar la lógica

ventas['Tipo_Cliente'] = ventas.apply(asignar_tipo_cliente, axis=1)


# 2.5. Limpiar columnas temporales

ventas = ventas.drop(columns=['conteo_temporal'])


print("✅ 'Tipo_Cliente' rellenado con lógica 'Nuevo'/'Recurrente'/'Potencial'.")

print("\nDistribución del Nuevo 'Tipo_Cliente':")

display(ventas['Tipo_Cliente'].value_counts(dropna=False))



#### Optimizacion de memoria y cambio de categoria cuando es necesario


print("\n" + "="*70)

print("PASO 4: Optimizando Memoria (Downcasting)")

print("="*70)


print("Uso de memoria ANTES de la optimización:")

mem_usage_before = ventas.memory_usage(deep=True).sum()

print(f"   > {mem_usage_before / 1024**2:.2f} MB")


# 4.1. Convertir Floats

float_cols = ventas.select_dtypes(include=['float64']).columns

for col in float_cols:

    ventas[col] = pd.to_numeric(ventas[col], downcast='float')


# 4.2. Convertir Integers (Asegurarse de que no haya NaN primero)

int_cols = ventas.select_dtypes(include=['int64']).columns

for col in int_cols:

    ventas[col] = pd.to_numeric(ventas[col], downcast='integer')


# 4.3. Convertir 'Object' a 'Category' (si la cardinalidad es baja)

# 'venta_exitosa' se creó como int, así que no se toca aquí

object_cols = ventas.select_dtypes(include=['object']).columns

for col in object_cols:

    if col not in ['ID_Venta', 'Cliente', 'Producto']: # Columnas de alta cardinalidad

        num_unique_values = ventas[col].nunique()

        if num_unique_values / len(ventas) < 0.5:

            ventas[col] = ventas[col].astype('category')

            print(f"   > Columna '{col}' convertida a 'category'.")


# 4.4. Convertir la nueva columna 'Tipo_Comportamiento' a category

if 'Tipo_Comportamiento' in ventas.columns:

     ventas['Tipo_Comportamiento'] = ventas['Tipo_Comportamiento'].astype('category')

     print(f"   > Columna 'Tipo_Comportamiento' convertida a 'category'.")



print("\nUso de memoria DESPUÉS de la optimización:")

mem_usage_after = ventas.memory_usage(deep=True).sum()

print(f"   > {mem_usage_after / 1024**2:.2f} MB")

print(f"   > Reducción: {100 * (mem_usage_before - mem_usage_after) / mem_usage_before:.1f}%")


# 4.5. Mostrar .info() final

print("\n   > Información final del DataFrame (Optimizado):")

ventas.info()


## Normalización


> Cuando los productos tienen errores de tipeo o **nombres inconsistentes**, no se

pueden agrupar bien para análisis. **Por eso se crea un diccionario** de correspondencias, también **llamado catálogo**, donde se *asigna un nombre unificado por cada variante detectada*.


### Defincion de Funciones Para cargar el categorias y clasificar por categoria , convertir unidades de tornillo





def cargar_categorias_desde_json(ruta='catalogo_categorias.json'):

    """

    Carga el catálogo de categorías desde un archivo JSON externo.

    """

    try:

        with open(ruta, 'r', encoding='utf-8') as f:

            categorias = json.load(f)

        return categorias

    except FileNotFoundError:

        print(f" No se encontró el archivo: {ruta}")

        return {}

    except Exception as e:

        print(f" Error al cargar categorías: {e}")

        return {}


# --- DEFINICIÓN FUNCIÓN 2: CLASIFICACIÓN QUE SE USARA PARA CLASIFICAR LOS PRODUCTOS ---


def clasificar_categorias(df, categorias_dict):

    """

    Clasifica productos en categorías usando palabras clave

    """



    print(" PASO 2: CLASIFICACIÓN POR CATEGORÍA")



    def extraer_categoria(nombre_producto):

        if pd.isna(nombre_producto):

            return 'Sin Categoría'


        nombre = str(nombre_producto).lower()


        for categoria, palabras_clave in categorias_dict.items():

            if any(palabra in nombre for palabra in palabras_clave):

                return categoria


        return 'Otros'


    df_copy = df.copy()

    df_copy['categoria'] = df_copy['producto_normalizado'].apply(

        lambda x: extraer_categoria(x)

    )


    # Estadísticas

    print("\n DISTRIBUCIÓN POR CATEGORÍA:")

    distribucion = df_copy['categoria'].value_counts()


    for categoria, cantidad in distribucion.items():

        pct = (cantidad / len(df_copy)) * 100

        print(f"    • {categoria:<35} {cantidad:>8,} ({pct:>5.1f}%)")


    # Productos únicos por categoría

    print("\n PRODUCTOS ÚNICOS POR CATEGORÍA:")

    productos_por_cat = df_copy.groupby('categoria')['producto_normalizado'].nunique().sort_values(ascending=False)


    for categoria, cantidad in productos_por_cat.items():

        print(f"    • {categoria:<35} {cantidad:>5} productos únicos")


    return df_copy

# DEFINICION NORMALIZAR UNIDADES A CAJAS

def convertir_tornillos_a_cajas(df_categorizado, factor_conversion=1000):

    """

    Convierte la columna 'Cantidad' de unidades a cajas SOLO para productos

    que son 'Tornillos' dentro de la categoría 'Fijaciones'.


    """


    df_ajustado = df_categorizado.copy()


    # 1. Definir la condición de filtrado doble

    # Filtro 1: Categoría debe ser 'Fijaciones'

    filtro_categoria = df_ajustado['categoria'] == 'Fijaciones'


    # Filtro 2: El nombre normalizado del producto debe contener 'tornillo' (en minúsculas)

    # NOTA: Asumimos que su función normalizar_texto o el catálogo maestro ya estandarizó estos nombres

    filtro_producto = df_ajustado['producto_normalizado'].str.lower().str.contains('tornillo', na=False)


    # Condición final: debe cumplir AMBOS filtros

    productos_a_convertir = filtro_categoria & filtro_producto


    # Verificar cuántos registros serán afectados

    num_registros_afectados = productos_a_convertir.sum()


    if num_registros_afectados == 0:

        print(" No se encontraron registros de 'Tornillos' en la categoría 'Fijaciones'. No se realizó la conversión.")

        return df_ajustado


    print(f" Registros a convertir (Tornillos en Fijaciones): {num_registros_afectados:,}")

    print(f" Factor de conversión (Unidades/Caja): {factor_conversion:,}")


    # 2. Aplicar la conversión solo a los registros identificados

    df_ajustado.loc[productos_a_convertir, 'Cantidad'] = \

        df_ajustado.loc[productos_a_convertir, 'Cantidad'] / factor_conversion


    # 3. Métricas de ajuste

    suma_antes = df_categorizado.loc[productos_a_convertir, 'Cantidad'].sum()

    suma_despues = df_ajustado.loc[productos_a_convertir, 'Cantidad'].sum()


    print(f"\n Metricas de Conversión (solo Tornillos):")

    print(f"   Suma total de Cantidad ANTES (Unidades): {suma_antes:,.0f}")

    print(f"   Suma total de Cantidad DESPUÉS (Cajas): {suma_despues:,.2f}")

    print(" Ajuste de cantidades completado.")


    return df_ajustado

print("\n Funciones normalizar_productos(), clasificar_categorias(), convertir_unidades_a_cajas() definidas.")

print(" Entorno listo para Celda 4.1")


### Definicion de las funciones de NORMALIZACION PRODUCTOS


from configuracion_global import (

        FUZZY_THRESHOLD,

        USE_EMBEDDINGS,

        EMBEDDING_THRESHOLD,

        MODELO_EMBEDDING

    )

def normalizar_productos_avanzado(df, catalogo_dict, threshold=80, use_embeddings=True, embedding_threshold=0.85):

    """

    Normalización híbrida usando:

    1. Coincidencia exacta

    2. Fuzzy matching (similitud de texto)

    3. Embeddings semánticos (detecta sinónimos y contexto)


    Parameters:

    -----------

    df : DataFrame

        DataFrame con columna 'Producto'

    catalogo_dict : dict

        Diccionario de productos maestros

    threshold : int

        Umbral para fuzzy matching (0-100)

    use_embeddings : bool

        Si True, usa embeddings para similitud semántica

    embedding_threshold : float

        Umbral para similitud de embeddings (0-1)

    """


    print("\n" + "="*70)

    print(" PASO 1: NORMALIZACIÓN AVANZADA DE PRODUCTOS")

    print("="*70)


    # Verificar disponibilidad de embeddings

    if use_embeddings and not USE_EMBEDDINGS:

        print("  Embeddings no disponibles. Usando solo fuzzy matching.")

        use_embeddings = False


    # Obtener productos únicos

    productos_unicos = df['Producto'].unique()

    print(f"\n Productos únicos a procesar: {len(productos_unicos):,}")


    # Crear columna normalizada

    df_copy = df.copy()

    df_copy['producto_normalizado'] = df_copy['Producto']

    df_copy['metodo_normalizacion'] = 'sin_cambio'

    df_copy['similitud_score'] = 0.0


    # Preparar catálogo normalizado

    print(" Preparando catálogo normalizado...")

    catalogo_norm = {normalizar_texto(k): v for k, v in catalogo_dict.items()}

    nombres_maestros = list(set(catalogo_norm.values()))


    print(f"    • Entradas en catálogo: {len(catalogo_norm)}")

    print(f"    • Nombres maestros únicos: {len(nombres_maestros)}")


    # --- CARGAR MODELO DE EMBEDDINGS ---

    if use_embeddings:

        print(f"\n Cargando modelo de embeddings...")

        print("    Modelo: paraphrase-multilingual-MiniLM-L12-v2")

        print("    (Optimizado para español y detección de sinónimos)")


        try:

            model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


            # Generar embeddings del catálogo

            print("    Generando embeddings del catálogo...")

            catalogo_texts = list(catalogo_norm.keys()) + nombres_maestros

            catalogo_embeddings = model.encode(catalogo_texts, show_progress_bar=False)


            print(f"     {len(catalogo_embeddings)} embeddings generados")

        except Exception as e:

            print(f"     Error cargando modelo: {e}")

            print("    Continuando solo con fuzzy matching...")

            use_embeddings = False


    # Diccionario caché

    normalizacion_cache = {}

    metodo_cache = {}

    score_cache = {}


    # Contadores

    exactas = 0

    fuzzy_alta = 0

    fuzzy_baja = 0

    embedding_match = 0

    sin_cambio = 0


    print(f"\n Procesando productos con método híbrido...")


    for i, producto in enumerate(productos_unicos):

        if i % 50 == 0:

            print(f"  Progreso: {i}/{len(productos_unicos)} ({i/len(productos_unicos)*100:.1f}%)", end='\r')


        if pd.isna(producto):

            normalizacion_cache[producto] = producto

            metodo_cache[producto] = 'sin_cambio'

            score_cache[producto] = 0.0

            sin_cambio += 1

            continue


        # Normalizar texto base

        producto_norm = normalizar_texto(producto)


        # ============================================================

        # NIVEL 1: Coincidencia EXACTA

        # ============================================================

        if producto_norm in catalogo_norm:

            normalizacion_cache[producto] = catalogo_norm[producto_norm]

            metodo_cache[producto] = 'exacta'

            score_cache[producto] = 1.0

            exactas += 1

            continue


        # ============================================================

        # NIVEL 2: Fuzzy ALTA similitud

        # ============================================================

        resultado_fuzzy = process.extractOne(

            producto_norm,

            list(catalogo_norm.keys()),

            scorer=fuzz.token_sort_ratio

        )


        if resultado_fuzzy and resultado_fuzzy[1] >= threshold:

            normalizacion_cache[producto] = catalogo_norm[resultado_fuzzy[0]]

            metodo_cache[producto] = 'fuzzy_alta'

            score_cache[producto] = resultado_fuzzy[1] / 100

            fuzzy_alta += 1

            continue


        # ============================================================

        # NIVEL 3: EMBEDDINGS (Similitud Semántica)

        # ============================================================

        if use_embeddings:

            try:

                # Generar embedding del producto actual

                producto_embedding = model.encode([producto_norm], show_progress_bar=False)


                # Calcular similitud con todos los productos del catálogo

                similarities = cosine_similarity(producto_embedding, catalogo_embeddings)[0]

                max_sim_idx = np.argmax(similarities)

                max_similarity = similarities[max_sim_idx]


                if max_similarity >= embedding_threshold:

                    mejor_match = catalogo_texts[max_sim_idx]


                    # Mapear al nombre maestro

                    if mejor_match in catalogo_norm:

                        producto_final = catalogo_norm[mejor_match]

                    else:

                        producto_final = mejor_match


                    normalizacion_cache[producto] = producto_final

                    metodo_cache[producto] = 'embedding'

                    score_cache[producto] = float(max_similarity)

                    embedding_match += 1

                    continue

            except Exception as e:

                pass  # Si falla embeddings, continuar con fuzzy


        # ============================================================

        # NIVEL 4: Fuzzy BAJA similitud (nombres maestros)

        # ============================================================

        resultado_maestro = process.extractOne(

            producto_norm,

            nombres_maestros,

            scorer=fuzz.token_sort_ratio

        )


        if resultado_maestro and resultado_maestro[1] >= threshold - 10:

            normalizacion_cache[producto] = resultado_maestro[0]

            metodo_cache[producto] = 'fuzzy_baja'

            score_cache[producto] = resultado_maestro[1] / 100

            fuzzy_baja += 1

            continue


        # ============================================================

        # NIVEL 5: Sin coincidencia

        # ============================================================

        normalizacion_cache[producto] = producto

        metodo_cache[producto] = 'sin_cambio'

        score_cache[producto] = 0.0

        sin_cambio += 1


    print(f"\n Procesamiento completo                                 ")


    # Aplicar normalización

    df_copy['producto_normalizado'] = df_copy['Producto'].map(normalizacion_cache)

    df_copy['metodo_normalizacion'] = df_copy['Producto'].map(metodo_cache)

    df_copy['similitud_score'] = df_copy['Producto'].map(score_cache)


    # Estadísticas

    productos_despues = df_copy['producto_normalizado'].nunique()

    reduccion = len(productos_unicos) - productos_despues

    pct_reduccion = (reduccion / len(productos_unicos)) * 100


    print("\n📊 RESULTADOS DE NORMALIZACIÓN AVANZADA:")

    print(f"    • Productos únicos ANTES:     {len(productos_unicos):,}")

    print(f"    • Productos únicos DESPUÉS:   {productos_despues:,}")

    print(f"    • Productos consolidados:     {reduccion:,} ({pct_reduccion:.1f}%)")

    print(f"\n    Métodos utilizados:")

    print(f"       Coincidencias exactas:        {exactas:,} ({exactas/len(productos_unicos)*100:.1f}%)")

    print(f"       Fuzzy alta (≥{threshold}%):        {fuzzy_alta:,} ({fuzzy_alta/len(productos_unicos)*100:.1f}%)")


    if use_embeddings:

        print(f"       Embeddings (≥{embedding_threshold*100:.0f}%):      {embedding_match:,} ({embedding_match/len(productos_unicos)*100:.1f}%)")


    print(f"       Fuzzy baja (≥{threshold-10}%):        {fuzzy_baja:,} ({fuzzy_baja/len(productos_unicos)*100:.1f}%)")

    print(f"        Sin cambio:                   {sin_cambio:,} ({sin_cambio/len(productos_unicos)*100:.1f}%)")


    # Ejemplos por método

    print("\n Ejemplos de normalización por método:")


    for metodo in ['exacta', 'fuzzy_alta', 'embedding', 'fuzzy_baja']:

        ejemplos_metodo = df_copy[df_copy['metodo_normalizacion'] == metodo][

            ['Producto', 'producto_normalizado', 'similitud_score']

        ].drop_duplicates().head(3)


        if len(ejemplos_metodo) > 0:

            print(f"\n  [{metodo.upper()}]")

            for idx, row in ejemplos_metodo.iterrows():

                print(f"    {row['Producto'][:40]:<40} → {row['producto_normalizado'][:40]:<40} (score: {row['similitud_score']:.2f})")


    return df_copy, normalizacion_cache, productos_unicos, metodo_cache


print("\n Funciones de normalización avanzada definidas")

print(f"   Modo embeddings: {'ACTIVADO ' if USE_EMBEDDINGS else 'DESACTIVADO '}")


from configuracion_global import (

        FUZZY_THRESHOLD,

        USE_EMBEDDINGS,

        EMBEDDING_THRESHOLD,

        MODELO_EMBEDDING

    )


# --- CARGAR CATÁLOGO DE PRODUCTOS ---

print(" Cargando catálogo de productos...")

catalogo = crear_catalogo_completo()

print(f" Catálogo de productos: {len(catalogo)} entradas\n")



print("  CONFIGURACIÓN:")

print(f"    • Fuzzy threshold: {FUZZY_THRESHOLD}%")

print(f"    • Embedding threshold: {EMBEDDING_THRESHOLD}")

print(f"    • Usar embeddings: {'SÍ ' if USE_EMBEDDINGS else 'NO⚠️'}")


# --- EJECUTAR NORMALIZACIÓN AVANZADA ---

ventas_normalizado, cache_normalizacion, productos_unicos, metodo_cache = normalizar_productos_avanzado(

    ventas,

    catalogo,

    threshold=FUZZY_THRESHOLD,

    use_embeddings=USE_EMBEDDINGS,

    embedding_threshold=EMBEDDING_THRESHOLD

)



print(" ANÁLISIS DE CALIDAD DE NORMALIZACIÓN")


# Distribución por método

metodos_dist = ventas_normalizado['metodo_normalizacion'].value_counts()

print("\n Distribución por método:")

for metodo, count in metodos_dist.items():

    pct = (count / len(ventas_normalizado)) * 100

    print(f"    {metodo:20s}: {count:>10,} ({pct:>5.1f}%)")


# Score promedio por método

score_por_metodo = ventas_normalizado.groupby('metodo_normalizacion')['similitud_score'].agg(['mean', 'min', 'max'])

print("\n Scores de similitud por método:")

print(score_por_metodo.round(3))


# --- PRODUCTOS CON BAJA CONFIANZA ---

print("\n  Productos con baja confianza (score < 0.85):")

baja_confianza = ventas_normalizado[

    (ventas_normalizado['similitud_score'] < 0.85) &

    (ventas_normalizado['similitud_score'] > 0)

][['Producto', 'producto_normalizado', 'metodo_normalizacion', 'similitud_score']].drop_duplicates()


if len(baja_confianza) > 0:

    print(f"    Total: {len(baja_confianza)} productos")

    print("\n    Top 10 para revisión manual:")

    for idx, row in baja_confianza.head(10).iterrows():

        print(f"    {row['Producto'][:35]:<35} → {row['producto_normalizado'][:35]:<35} [{row['metodo_normalizacion']:12s}] (score: {row['similitud_score']:.2f})")

else:

    print("     No hay productos con baja confianza")


# --- GUARDAR RESULTADOS ---


print(" GUARDANDO RESULTADOS DE NORMALIZACIÓN")


# 1. Mapeo completo con metadata

mapeo_completo = pd.DataFrame({

    'producto_original': list(cache_normalizacion.keys()),

    'producto_normalizado': list(cache_normalizacion.values()),

    'metodo': [metodo_cache.get(k, 'sin_cambio') for k in cache_normalizacion.keys()],

    'score': [ventas_normalizado[ventas_normalizado['Producto'] == k]['similitud_score'].iloc[0]

              if k in ventas_normalizado['Producto'].values and not ventas_normalizado[ventas_normalizado['Producto'] == k].empty

              else 0.0

              for k in cache_normalizacion.keys()]

})

mapeo_completo = mapeo_completo.sort_values('score', ascending=False)

mapeo_completo.to_excel('04_mapeo_normalizacion_avanzado.xlsx', index=False)

print(" 04_mapeo_normalizacion_avanzado.xlsx")







### Consolidacion de Estadisticas


# 2. Consolidación con estadísticas

consolidacion = ventas_normalizado.groupby('producto_normalizado').agg({

    'Producto': lambda x: list(x.unique()),

    'Cantidad': 'sum',

    'Importe_Producto_BS': 'sum',

    'metodo_normalizacion': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'sin_cambio',

    'similitud_score': 'mean'

}).reset_index()


consolidacion['n_variantes'] = consolidacion['Producto'].apply(len)

productos_consolidados = consolidacion[consolidacion['n_variantes'] > 1].sort_values(

    'n_variantes', ascending=False

)


if len(productos_consolidados) > 0:

    consolidacion_export = productos_consolidados.copy()

    # Corrección: Asegura que todos los elementos sean strings antes de 'join'

    consolidacion_export['variantes'] = consolidacion_export['Producto'].apply(

        lambda x: ' | '.join(map(str, x[:10]))  # Limitar a 10 variantes

    )

    consolidacion_export = consolidacion_export[[

        'producto_normalizado', 'n_variantes', 'variantes',

        'Cantidad', 'Importe_Producto_BS', 'metodo_normalizacion', 'similitud_score'

    ]]

    consolidacion_export = consolidacion_export.sort_values('Cantidad', ascending=False)

    consolidacion_export.to_excel('04_productos_consolidados_avanzado.xlsx', index=False)

    print(" 04_productos_consolidados_avanzado.xlsx")


    print(f"\n Top 10 productos consolidados (por volumen):")

    for idx, row in consolidacion_export.head(10).iterrows():

        print(f"    {row['producto_normalizado'][:40]:<40} → {row['n_variantes']:>3} variantes | Qty: {row['Cantidad']:>8,.0f} | {row['metodo_normalizacion']}")


# 4. Estadísticas de normalización

stats = pd.DataFrame({

    'metodo': metodos_dist.index,

    'cantidad': metodos_dist.values,

    'porcentaje': (metodos_dist.values / len(ventas_normalizado) * 100).round(2)

})

stats.to_excel('04_estadisticas_normalizacion.xlsx', index=False)

print(" 04_estadisticas_normalizacion.xlsx")


productos_antes = len(productos_unicos)

productos_despues = ventas_normalizado['producto_normalizado'].nunique()

reduccion = productos_antes - productos_despues

mejora_embeddings = metodos_dist.get('embedding', 0)


print(f"""

 MÉTRICAS DE NORMALIZACIÓN AVANZADA:

    • Productos únicos ANTES:        {productos_antes:,}

    • Productos únicos DESPUÉS:       {productos_despues:,}

    • Reducción lograda:             {reduccion:,} ({reduccion/max(1, productos_antes)*100:.1f}%)

    • Productos consolidados:        {len(productos_consolidados) if len(productos_consolidados) > 0 else 0}


 MEJORA POR EMBEDDINGS:

    • Matches por similitud semántica: {mejora_embeddings:,}

    • Sinónimos detectados:          {'Ayudo' if mejora_embeddings > 0 else ' No disponible'}

    • Contexto comprendido:          {'Ayudo' if mejora_embeddings > 0 else ' No disponible'}


 ARCHIVOS GENERADOS:

    • 04_mapeo_normalizacion_avanzado.xlsx

    • 04_productos_consolidados_avanzado.xlsx

    • 04_productos_revisar.xlsx

    • 04_estadisticas_normalizacion.xlsx


 VARIABLES CREADAS:

    • ventas_normalizado: DataFrame con productos normalizados

    • cache_normalizacion: Diccionario de mapeo

    • metodo_cache: Métodos usados por producto


    """)


# Advertencias finales

if len(baja_confianza) > 0:

    print(f"  ATENCIÓN: {len(baja_confianza)} productos con baja confianza")

    print("    Revisa: 04_productos_revisar.xlsx")


if not USE_EMBEDDINGS:

    print("\n SUGERENCIA: Instala sentence-transformers para mejorar la detección de sinónimos")

    print("    pip install sentence-transformers")


### Creacion archivo de baja confianza


# 3. Productos para revisión manual

if len(baja_confianza) > 0:

    baja_confianza.to_excel('04_productos_revisar.xlsx', index=False)

    print(" 04_productos_revisar.xlsx (productos con score < 0.85)")


### Clasificar los productos normalizados


> Asignar a cada producto una categoría funcional, como Perfiles, Techo, Tabiquería, etc., utilizando un catálogo previamente definido.


    # --- CARGAR CATÁLOGO DE CATEGORÍAS ---

    print(" Cargando catálogo de categorías...")

    categorias = cargar_categorias_desde_json() # Cargar catálogo de categorías Llama a una función que lee un archivo .json que contiene un diccionario

    print(f" Catálogo de categorías: {len(categorias)} categorías")

    print(f"    Categorías: {', '.join(categorias.keys())}\n")


    # --- EJECUTAR PASO 2: ClLASIFICAION DE PRODUCTOS ---

    ventas_categorizado = clasificar_categorias(

        ventas_normalizado,

        categorias

    )

    # Se usa una función clasificar_categorias(df, catalogo) que:


    # Lee el producto_normalizado


    # Busca si contiene alguna palabra clave del catálogo


    # IMPORTANTE: Asigna la categoría correspondiente


    # IMPORTANTE: Este paso agrega una nueva columna al dataframe: categoria


    # --- GUARDAR RESULTADOS DE CLASIFICACIÓN ---


    # 1. DataFrame completo (normalizado + categorizado)

    ventas_categorizado.to_excel('04_ventas_normalizado_categorizado.xlsx', index=False)

    print(" 04_ventas_normalizado_categorizado.xlsx")


    # 2. Resumen por categoría Agrupa los productos por categoria y suma:


    # ----- Cantidad


    # ------ Importe_Producto_BS


    # ------- Crea un resumen por producto dentro de cada categoría, ordenado por ventas.


    resumen_categoria = ventas_categorizado.groupby(['categoria', 'producto_normalizado']).agg({

        'Cantidad': 'sum',

        'Importe_Producto_BS': 'sum'

    }).reset_index()

    resumen_categoria.columns = ['categoria', 'producto', 'cantidad_total', 'venta_total']

    resumen_categoria = resumen_categoria.sort_values(['categoria', 'venta_total'], ascending=[True, False])

    resumen_categoria.to_excel('04_resumen_por_categoria.xlsx', index=False)

    print(" 04_resumen_por_categoria.xlsx")



    # Cuántas categorías fueron detectadas


    # Cuántos productos quedaron sin clasificar (categoria == 'Otros')


    # Qué porcentaje del dataset tiene una categoría válida


    categorias_encontradas = ventas_categorizado['categoria'].nunique()


    print(f"""

 MÉTRICAS DE CATEGORIZACIÓN:

    • Categorías identificadas:   {categorias_encontradas}

    • Productos sin categoría:    {(ventas_categorizado['categoria'] == 'Otros').sum():,}

    • Cobertura de categorización: {((len(ventas_categorizado) - (ventas_categorizado['categoria'] == 'Otros').sum()) / len(ventas_categorizado) * 100):.1f}%


 ARCHIVOS GENERADOS:

    • 04_ventas_normalizado_categorizado.xlsx

    • 04_resumen_por_categoria.xlsx


 VARIABLES CREADAS:

    • ventas_categorizado: DataFrame con productos normalizados + categorías

    """)


    # Top 5 categorías por volumen de ventas

    # -------- Agrupa por categoría y suma ventas


    # ---------Muestra las 5 categorías con mayor volumen de venta


    print(" TOP 5 CATEGORÍAS POR VOLUMEN DE VENTAS (Importe_Producto_BS):")

    top_categorias = ventas_categorizado.groupby('categoria')['Importe_Producto_BS'].sum().sort_values(ascending=False).head(5)

    for categoria, venta in top_categorias.items():

        print(f"    {categoria:<35} BS {venta:>12,.2f}")


    # Configuración de estilo

    sns.set_style("whitegrid")


    # --- GRÁFICO 1: Distribución de Ventas (BS) por Categoría ---

    print("Generando Gráfico 1: Ventas Totales (BS) por Categoría...")


    ventas_por_categoria = ventas_categorizado.groupby('categoria')['Importe_Producto_BS'].sum().sort_values(ascending=False)


    plt.figure(figsize=(12, 8))

    sns.barplot(

        y=ventas_por_categoria.index,

        x=ventas_por_categoria.values,

        palette='plasma'

    )

    plt.title('Ventas Totales (BS) por Categoría', fontsize=16, weight='bold')

    plt.xlabel('Ventas Totales (BS)')

    plt.ylabel('Categoría')

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Bs {x:,.0f}'))

    plt.tight_layout()

    plt.show()


    # --- GRÁFICO 2: Distribución de Registros (Conteo) por Categoría ---

    print("\nGenerando Gráfico 2: Número de Registros por Categoría...")


    conteo_por_categoria = ventas_categorizado['categoria'].value_counts().sort_values(ascending=False)


    plt.figure(figsize=(12, 8))

    sns.barplot(

        y=conteo_por_categoria.index,

        x=conteo_por_categoria.values,

        palette='ocean_r'

    )

    plt.title('Número de Registros de Venta por Categoría', fontsize=16, weight='bold')

    plt.xlabel('Cantidad de Registros')

    plt.ylabel('Categoría')

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

    plt.tight_layout()

    plt.show()



### Normalizacion de Unidades equivalentes (unidades de tornillo)


    df_categorizado = convertir_tornillos_a_cajas(

        df_categorizado=ventas_categorizado,

        factor_conversion=1000

    )


    print("\n✅ DataFrame ajustado (df_ventas_ajustado) listo para el análisis ABC/Clustering.")


    # El siguiente paso (Clustering/ABC) debe usar 'df_ventas_ajustado'

    # en lugar de 'ventas_categorizado'.



## Clasificacion por diferentes metodos (ABC, K-MEANS, DBSCAN)


Por volumen de ventas (alto, medio, bajo): usando modelos no supervisados:


Análisis ABC


K-Means


DBSCAN


### DEFINICION DE MODELOS


# --- VERIFICACIÓN DE DATOS ---

if 'ventas_normalizado' not in locals() and 'ventas_normalizado' not in globals():

    print("  No se encuentra 'ventas_normalizado'.")

    print("   Asegúrate de haber ejecutado las celdas de la sección 4.")

else:

    print(" DataFrame 'ventas_normalizado' detectado.")



def clasificar_abc_pareto(df_datos):

    """

    Clasifica productos usando Análisis ABC (Pareto 80/20)

    """

    print("\n MÉTODO 1: ANÁLISIS ABC PARETO")

    print("-" * 70)


    # Calcular ventas por producto

    ventas_producto = df_datos.groupby('producto_normalizado').agg(

        qty_total=('Cantidad', 'sum'),

        qty_promedio=('Cantidad', 'mean'),

        frecuencia=('Cantidad', 'count'),

        venta_total=('Importe_Producto_BS', 'sum'),

        venta_promedio=('Importe_Producto_BS', 'mean')

    ).reset_index()


    ventas_producto.rename(columns={'producto_normalizado': 'producto'}, inplace=True)

    ventas_producto = ventas_producto.sort_values('venta_total', ascending=False)


    # Calcular porcentaje acumulado

    total_ventas = ventas_producto['venta_total'].sum()

    ventas_producto['pct_acumulado'] = (

        ventas_producto['venta_total'].cumsum() / total_ventas * 100

    )


    # Clasificar ABC

    def asignar_clase_abc(pct_acum):

        if pct_acum <= 80:

            return 'A - Alta'

        elif pct_acum <= 95:

            return 'B - Media'

        else:

            return 'C - Baja'


    ventas_producto['clase_abc'] = ventas_producto['pct_acumulado'].apply(asignar_clase_abc)


    # Estadísticas

    print("\n Distribución ABC:")

    for clase in ['A - Alta', 'B - Media', 'C - Baja']:

        if clase in ventas_producto['clase_abc'].values:

            subset = ventas_producto[ventas_producto['clase_abc'] == clase]

            pct_prods = len(subset) / len(ventas_producto) * 100

            pct_ventas = subset['venta_total'].sum() / total_ventas * 100

            print(f"\n{clase}:")

            print(f"  Productos: {len(subset)} ({pct_prods:.1f}%)")

            print(f"  Ventas: BS {subset['venta_total'].sum():,.0f} ({pct_ventas:.1f}%)")

            print(f"  Venta promedio: BS {subset['venta_promedio'].mean():,.0f}")


    return ventas_producto



def clasificar_kmeans_optimizado(df_datos, n_clusters=3):

    """

    K-Means con optimizaciones para evitar desbalanceo extremo

    """

    print("\n MÉTODO 2: K-MEANS OPTIMIZADO")

    print("-" * 70)


    # Calcular métricas

    metricas = df_datos.groupby('producto_normalizado').agg({

        'Cantidad': ['sum', 'mean', 'std', 'count'],

        'Importe_Producto_BS': ['sum', 'mean']

    }).reset_index()


    metricas.columns = ['producto', 'qty_total', 'qty_promedio', 'qty_std',

                        'frecuencia', 'venta_total', 'venta_promedio']

    metricas['qty_std'] = metricas['qty_std'].fillna(0)


    # MEJORA 1: Log-scaling

    metricas['qty_total_log'] = np.log1p(metricas['qty_total'])

    metricas['venta_total_log'] = np.log1p(metricas['venta_total'])

    metricas['frecuencia_log'] = np.log1p(metricas['frecuencia'])


    features_cols = ['qty_total_log', 'venta_total_log', 'frecuencia_log', 'qty_promedio']

    X = metricas[features_cols].values

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # MEJORA 3: Encontrar k óptimo

    silhouette_scores = []

    inertias = []

    k_values = range(2, 8) # Probar de 2 a 7 clusters


    print("\n Buscando número óptimo de clusters...")

    for k in k_values:

        kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)

        labels = kmeans_temp.fit_predict(X_scaled)

        # Evitar error si hay un solo cluster (poco probable)

        if len(set(labels)) > 1:

            sil_score = silhouette_score(X_scaled, labels)

            silhouette_scores.append(sil_score)

            print(f"  k={k}: Silhouette={sil_score:.3f}")

        else:

            silhouette_scores.append(-1) # Penalizar

            print(f"  k={k}: No se pudo calcular Silhouette (un solo cluster)")

        inertias.append(kmeans_temp.inertia_)


    # Usar k con mejor Silhouette

    k_optimal = k_values[np.argmax(silhouette_scores)]

    print(f"\n K óptimo: {k_optimal} (Silhouette: {max(silhouette_scores):.3f})")


    # Entrenar con k óptimo

    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)

    metricas['cluster'] = kmeans.fit_predict(X_scaled) # fit_predict aplica el algoritmo y asigna un grupo a cada producto.


    # Etiquetar clusters por promedio de ventas

    cluster_sales = metricas.groupby('cluster')['venta_total'].mean().sort_values(ascending=False)


    etiquetas_map = {}

    nombres_clases = ['A - Alta', 'B - Media', 'C - Baja', 'D - Extra 1', 'E - Extra 2', 'F - Extra 3']

    for idx, cluster_id in enumerate(cluster_sales.index):

        etiquetas_map[cluster_id] = nombres_clases[idx]


    metricas['clase_kmeans'] = metricas['cluster'].map(etiquetas_map)


    # Estadísticas

    print("\n Distribución K-Means:")

    for clase in sorted(etiquetas_map.values()):

        if clase in metricas['clase_kmeans'].values:

            subset = metricas[metricas['clase_kmeans'] == clase]

            print(f"\n{clase}: {len(subset)} productos")

            print(f"  Venta promedio: BS {subset['venta_total'].mean():,.0f}")

            print(f"  Cantidad promedio: {subset['qty_total'].mean():.0f} unidades")


    # Devolvemos métricas COMPLETAS para visualización

    return metricas, silhouette_scores, inertias

def subsegmentar_clase_a_kmeans(df_clase_a, k_range=range(2, 6)):

    """

    Aplica K-Means (con log/scale) SÓLO al subconjunto de productos Clase A.

    Recibe el DataFrame ya agregado de 'clasificar_abc_pareto'.

    """

    print("\n" + "="*70)

    print("💎 MÉTODO 4: SUB-SEGMENTACIÓN K-MEANS (SÓLO CLASE A)")

    print("-" * 70)


    # La entrada 'df_clase_a' ya está agregada (es df_abc_final filtrado)

    # Solo necesitamos copiarla para no modificar el original.

    metricas = df_clase_a.copy()


    needed_cols = ['producto', 'qty_total', 'frecuencia', 'venta_total', 'qty_promedio']

    if not all(col in metricas.columns for col in needed_cols):

        raise ValueError("El DataFrame de entrada no tiene las columnas agregadas necesarias (ej. 'venta_total', 'frecuencia').")


    if len(metricas) < max(k_range):

        print(f"⚠️  Advertencia: Pocos productos en Clase A ({len(metricas)}). Reduciendo rango de K.")

        k_range = range(2, max(2, len(metricas))) # Asegurar al menos k=2 si es posible


    # --- Transformación Logarítmica ---

    metricas['qty_total_log'] = log1p(metricas['qty_total'])

    metricas['venta_total_log'] = log1p(metricas['venta_total'])

    metricas['frecuencia_log'] = log1p(metricas['frecuencia'])

    metricas['qty_promedio_log'] = log1p(metricas['qty_promedio'])


    features_cols = ['venta_total_log', 'frecuencia_log', 'qty_total_log', 'qty_promedio_log']

    X = metricas[features_cols].values


    # --- Escalado ---

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # Encontrar k óptimo

    silhouette_scores = []

    inertias = []

    k_values = k_range


    print("\n🔍 Buscando K óptimo para Clase A...")

    for k in k_values:

        kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)

        labels = kmeans_temp.fit_predict(X_scaled)


        if len(set(labels)) > 1:

            sil_score = silhouette_score(X_scaled, labels)

            silhouette_scores.append(sil_score)

            print(f"   k={k}: Silhouette={sil_score:.3f}")

        else:

            silhouette_scores.append(-1) # Penalizar

            print(f"   k={k}: No se pudo calcular Silhouette (un solo cluster)")

        inertias.append(kmeans_temp.inertia_)


    # Usar k con mejor Silhouette

    k_optimal = k_values[np.argmax(silhouette_scores)]

    print(f"\n✅ K óptimo para Clase A: {k_optimal} (Silhouette: {max(silhouette_scores):.3f})")


    # Entrenar con k óptimo

    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)

    metricas['cluster'] = kmeans.fit_predict(X_scaled)


    # Etiquetar clusters por promedio de ventas

    cluster_sales = metricas.groupby('cluster')['venta_total'].mean().sort_values(ascending=False)


    etiquetas_map = {}

    # Nuevas etiquetas para los sub-segmentos de Clase A

    nombres_clases = ['A.1 (Valor Alto)', 'A.2 (Valor Medio)', 'A.3 (Valor Bajo)', 'A.4', 'A.5']

    for idx, cluster_id in enumerate(cluster_sales.index):

        if idx < len(nombres_clases):

             etiquetas_map[cluster_id] = nombres_clases[idx]

        else:

             etiquetas_map[cluster_id] = f'Cluster A.{idx}'


    metricas['subclase_kmeans'] = metricas['cluster'].map(etiquetas_map)


    # Estadísticas

    print("\n📊 Distribución K-Means (Solo Clase A):")

    for clase in sorted(etiquetas_map.values()):

        if clase in metricas['subclase_kmeans'].values:

            subset = metricas[metricas['subclase_kmeans'] == clase]

            print(f"\n{clase}: {len(subset)} productos")

            print(f"   Venta promedio: BS {subset['venta_total'].mean():,.0f}")

            print(f"   Frecuencia promedio: {subset['frecuencia'].mean():.1f} ventas")


    return metricas, silhouette_scores, inertias

def clasificar_dbscan(df_datos):

    """

    DBSCAN identifica clusters naturales + outliers (ruido)

    """

    print("\n MÉTODO 3: DBSCAN (CLUSTERING POR DENSIDAD)")

    print("-" * 70)


    metricas = df_datos.groupby('producto_normalizado').agg({

        'Cantidad': ['sum', 'mean', 'count'],

        'Importe_Producto_BS': ['sum', 'mean']

    }).reset_index()

    metricas.columns = ['producto', 'qty_total', 'qty_promedio', 'frecuencia',

                        'venta_total', 'venta_promedio']


    metricas['qty_total_log'] = np.log1p(metricas['qty_total'])

    metricas['venta_total_log'] = np.log1p(metricas['venta_total'])

    metricas['frecuencia_log'] = np.log1p(metricas['frecuencia'])


    features_cols = ['qty_total_log', 'venta_total_log', 'frecuencia_log', 'qty_promedio']

    X = metricas[features_cols].values

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # Encontrar eps adaptativo

    neighbors = NearestNeighbors(n_neighbors=5)

    neighbors_fit = neighbors.fit(X_scaled)

    distances, indices = neighbors_fit.kneighbors(X_scaled)

    distances = np.sort(distances[:, -1], axis=0)

    eps = distances[int(len(distances) * 0.9)]

    print(f" EPS adaptativo: {eps:.3f}")


    dbscan = DBSCAN(eps=eps, min_samples=3)

    metricas['cluster_dbscan'] = dbscan.fit_predict(X_scaled)


    n_clusters = len(set(metricas['cluster_dbscan'])) - (1 if -1 in metricas['cluster_dbscan'] else 0)

    n_ruido = (metricas['cluster_dbscan'] == -1).sum()


    print(f"\n Resultados DBSCAN:")

    print(f"  Clusters encontrados: {n_clusters}")

    print(f"  Productos outlier (ruido): {n_ruido}")


    # Reclasificar

    etiquetas_map = {-1: 'D - Outlier'}

    cluster_sales = metricas[metricas['cluster_dbscan'] != -1].groupby('cluster_dbscan')['venta_total'].mean().sort_values(ascending=False)


    nombres_clases = ['A - Alta', 'B - Media', 'C - Baja']

    for idx, cluster_id in enumerate(cluster_sales.index):

        if idx < len(nombres_clases):

            etiquetas_map[cluster_id] = nombres_clases[idx]

        else:

            etiquetas_map[cluster_id] = f'Cluster {idx+1}'


    metricas['clase_dbscan'] = metricas['cluster_dbscan'].map(etiquetas_map)


    print("\n Distribución DBSCAN:")

    print(metricas['clase_dbscan'].value_counts())


    return metricas[['producto', 'clase_dbscan', 'qty_total', 'frecuencia', 'venta_total']]



def clasificar_demanda_avanzada(df_datos):

    """

    Ejecuta los 3 métodos y retorna una comparativa

    """


    print("EJECUTANDO CLASIFICACIÓN AVANZADA DE DEMANDA")



    # Método 1: ABC

    df_abc = clasificar_abc_pareto(df_datos)


    # Método 2: K-Means mejorado

    df_kmeans, _, _ = clasificar_kmeans_optimizado(df_datos)


    # Método 3: DBSCAN

    df_dbscan = clasificar_dbscan(df_datos)


    # Crear DataFrame comparativo

    df_comparativa = df_abc.copy()

    df_comparativa = df_comparativa.merge(

        df_kmeans[['producto', 'clase_kmeans']],

        on='producto',

        how='left'

    )

    df_comparativa = df_comparativa.merge(

        df_dbscan[['producto', 'clase_dbscan']],

        on='producto',

        how='left'

    )



    print("COMPARATIVA DE MÉTODOS")



    print("\n ABC PARETO:")

    print(df_comparativa['clase_abc'].value_counts())


    print("\n K-MEANS OPTIMIZADO:")

    print(df_comparativa['clase_kmeans'].value_counts())


    print("\n DBSCAN:")

    print(df_comparativa['clase_dbscan'].value_counts().sort_index())


    # Guardar comparativa

    df_comparativa.to_excel('05_comparativa_clasificacion_demanda.xlsx', index=False)

    print("\n Comparativa guardada: 05_comparativa_clasificacion_demanda.xlsx")



    print(" RECOMENDACIÓN DE MÉTODO")


    print("""

    MEJOR OPCIÓN: Usar ABC PARETO (Método 1)


    Razones:

    1. Alineado con la realidad de negocio (80/20).

    2. Fácil de interpretar para decisiones gerenciales.

    3. No depende de parámetros complejos (como 'k' o 'eps').

    4. Permite entrenar modelos de predicción SEPARADOS

       para cada clase (A, B, C), lo cual es ideal.

    """)


    return df_comparativa, df_abc, df_kmeans, df_dbscan


print("\n Funciones de clasificación (ABC, K-Means, DBSCAN) definidas.")


#### ABC


### CLASIFICACION ABC CON TOTAL DE PRODUCTOS


#### ABC


    # --- EJECUTAR MÉTODO 1: ABC ---

    df_abc_final = clasificar_abc_pareto(ventas_normalizado)


    # Guardar clasificación general ABC (recomendada)

    df_abc_final.to_excel('05_clasificacion_abc_final.xlsx', index=False)

    print(" 05_clasificacion_abc_final.xlsx (Clasificación Completa)")


    #  FILTRAR PRODUCTOS CLASE A (Pareto 80/20)

    df_clase_A = df_abc_final[df_abc_final['clase_abc'] == 'A - Alta']

    print(f"\n Productos seleccionados 'Clase A': {len(df_clase_A)}")


    #  Guardar solo productos clase A

    df_clase_A.to_excel('05_productos_clase_A.xlsx', index=False)

    print(" 05_productos_clase_A.xlsx (Solo Clase A)")


    print(f"Productos clase A: {(df_abc_final['clase_abc'] == 'A - Alta').sum()}")

    print(f"Productos clase B: {(df_abc_final['clase_abc'] == 'B - Media').sum()}")

    print(f"Productos clase C: {(df_abc_final['clase_abc'] == 'C - Baja').sum()}")



##### Visualizacion ABC


    sns.set_style("whitegrid")


    # --- GRÁFICO 1: Contribución de Ventas por Clase ---

    print("Generando Gráfico 1: Contribución de Ventas (BS) por Clase ABC...")


    plt.figure(figsize=(10, 6))

    contrib_ventas = df_abc_final.groupby('clase_abc')['venta_total'].sum().sort_index()


    splot = sns.barplot(

        x=contrib_ventas.index,

        y=contrib_ventas.values,

        palette={'A - Alta':'#4CAF50', 'B - Media':'#FFC107', 'C - Baja':'#F44336'}

    )

    plt.title('Contribución Total de Ventas (BS) por Clase ABC', fontsize=16, weight='bold')

    plt.ylabel('Ventas Totales (BS)')

    plt.xlabel('Clase ABC')


    # Formatear eje Y

    from matplotlib.ticker import FuncFormatter

    splot.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'Bs {x:,.0f}'))


    # Añadir etiquetas de valor

    for p in splot.patches:

        splot.annotate(f'Bs {p.get_height():,.0f}',

                       (p.get_x() + p.get_width() / 2., p.get_height()),

                       ha = 'center', va = 'center',

                       xytext = (0, 9),

                       textcoords = 'offset points',

                       weight='bold')

    plt.show()


    # --- GRÁFICO 2: Conteo de Productos por Clase ---

    print("\nGenerando Gráfico 2: Conteo de Productos por Clase ABC...")


    plt.figure(figsize=(10, 6))

    conteo_prods = df_abc_final['clase_abc'].value_counts().sort_index()


    splot_conteo = sns.barplot(

        x=conteo_prods.index,

        y=conteo_prods.values,

        palette={'A - Alta':'#4CAF50', 'B - Media':'#FFC107', 'C - Baja':'#F44336'}

    )

    plt.title('Número de Productos Únicos por Clase ABC', fontsize=16, weight='bold')

    plt.ylabel('Cantidad de Productos')

    plt.xlabel('Clase ABC')


    # Añadir etiquetas de valor

    for p in splot_conteo.patches:

        splot_conteo.annotate(f'{int(p.get_height())} Prod.',

                             (p.get_x() + p.get_width() / 2., p.get_height()),

                             ha = 'center', va = 'center',

                             xytext = (0, 9),

                             textcoords = 'offset points',

                             weight='bold')

    plt.show()


**OBSERVACIONEs:** Podemos observar que los segmento 19 productos para que esten en la clase A lo cual es muy bueno para poder enfocar en productos que rinden mas para la empresa de PLusSteel por lo que haremos es continuar con esos productos para lograr hacer un pronostico clave


K-MEANS


### K-MEANS

Usamos K-MEANS para lograr ver como se comportan los productos importantes (Clase A)


    # --- EJECUTAR MÉTODO 2: K-Means ---

    # Guardamos los 3 resultados para usarlos en la celda de visualización

    df_kmeans_final, silhouette_scores_kmeans, inertias_kmeans = clasificar_kmeans_optimizado(

        ventas_normalizado

    )

    # Guardar clasificación K-Means

    df_kmeans_final.to_excel('05_clasificacion_kmeans_final.xlsx', index=False)

    print(" 05_clasificacion_kmeans_final.xlsx (Clasificación Completa)")


    print("\n" + "="*70)

    print(" CELDA 5.2 COMPLETADA CON ÉXITO")

    print("="*70)

    print("Distribución de productos K-Means:")

    print(df_kmeans_final['clase_kmeans'].value_counts().sort_index())


    print("\n Variables creadas para visualización:")

    print("  • df_kmeans_final")

    print("  • silhouette_scores_kmeans")

    print("  • inertias_kmeans")




    sns.set_style("whitegrid")

    k_values = range(2, 2 + len(silhouette_scores_kmeans))


    # --- GRÁFICO 1: Puntuación de Silueta (Elección de K) ---

    print("Generando Gráfico 1: Puntuación de Silueta vs. Número de Clusters (k)...")


    plt.figure(figsize=(10, 5))

    plt.plot(k_values, silhouette_scores_kmeans, marker='o', linestyle='--')


    # Marcar el k óptimo

    k_optimal = k_values[np.argmax(silhouette_scores_kmeans)]

    max_score = max(silhouette_scores_kmeans)

    plt.axvline(x=k_optimal, color='red', linestyle=':', label=f'K Óptimo = {k_optimal} (Score: {max_score:.3f})')


    plt.title('Método de la Silueta para K-Means', fontsize=16, weight='bold')

    plt.xlabel('Número de Clusters (k)')

    plt.ylabel('Puntuación de Silueta')

    plt.legend()

    plt.xticks(k_values)

    plt.grid(True)

    plt.show()


    # --- GRÁFICO 2: Visualización de Clusters (Scatter) ---

    print("\nGenerando Gráfico 2: Visualización de Clusters K-Means...")


    # Usamos las columnas logarítmicas que están en df_kmeans_final

    plt.figure(figsize=(12, 8))

    sns.scatterplot(

        data=df_kmeans_final,

        x='venta_total_log',

        y='frecuencia_log',

        hue='clase_kmeans',

        palette='bright',

        s=100, # Tamaño del punto

        alpha=0.8 # Transparencia

    )


    plt.title('Clusters K-Means (Ventas vs. Frecuencia)', fontsize=16, weight='bold')

    plt.xlabel('Venta Total (Logarítmica)')

    plt.ylabel('Frecuencia de Venta (Logarítmica)')

    plt.legend(title='Clase K-Means')

    plt.show()



#### Ejecución de K-MEANS (Solamente para la clase A)


# 1. Filtrar solo los datos de Clase A del resultado de ABC

df_clase_a_data = df_abc_final[df_abc_final['clase_abc'] == 'A - Alta'].copy()


if len(df_clase_a_data) < 2:

        # El código DENTRO de 'if' DEBE tener 2 niveles de sangría (8 espacios)

        print(f"⚠️  No hay suficientes productos en Clase A ({len(df_clase_a_data)}) para sub-segmentar. Omitiendo.")

        # Crear variables vacías para que la celda de visualización no falle

        df_clase_a_subsegmented = pd.DataFrame()

        sil_scores_a = []

        inertias_a = []

else:

        # El código DENTRO de 'else' DEBE tener 2 niveles de sangría (8 espacios)

        print(f"Sub-segmentando {len(df_clase_a_data)} productos de Clase A...")


        # 2. Ejecutar la nueva función de sub-segmentación

        # Estas variables (df_clase_a_subsegmented, sil_scores_a, inertias_a)

        # se crean como globales y serán usadas por la siguiente celda.

        df_clase_a_subsegmented, sil_scores_a, inertias_a = subsegmentar_clase_a_kmeans(

        df_clase_a_data

        )


        df_clase_a_subsegmented.to_excel('07_clasificacion_clase_A_subsegmentos.xlsx', index=False)

        print("✅ 07_clasificacion_clase_A_subsegmentos.xlsx (Sub-segmentos de Clase A)")




#### Visualizacion de K-MEANS (Solamente para la clase A)


# 1. Visualizar los resultados de la sub-segmentación

print("\nGenerando Gráfico 1: Puntuación de Silueta (Solo Clase A)...")

sns.set_style("whitegrid")

k_values_a = range(2, 2 + len(sil_scores_a))


plt.figure(figsize=(10, 5))

plt.plot(k_values_a, sil_scores_a, marker='o', linestyle='--')


k_optimal_a = k_values_a[np.argmax(sil_scores_a)]

max_score_a = max(sil_scores_a)

plt.axvline(x=k_optimal_a, color='red', linestyle=':', label=f'K Óptimo = {k_optimal_a} (Score: {max_score_a:.3f})')


plt.title('Método de la Silueta para K-Means (Solo Clase A)', fontsize=16, weight='bold')

plt.xlabel('Número de Clusters (k)')

plt.ylabel('Puntuación de Silueta')

plt.legend()

plt.xticks(k_values_a)

plt.grid(True)

plt.show()


# --- GRÁFICO 2: Visualización de Clusters (Scatter) ---

print("\nGenerando Gráfico 2: Visualización de Clusters K-Means (Solo Clase A)...")


plt.figure(figsize=(12, 8))

sns.scatterplot(

    data=df_clase_a_subsegmented,

    x='venta_total_log',

    y='frecuencia_log',

    hue='subclase_kmeans',  # Usar la nueva columna de sub-clase

    palette='deep',

    s=120,

    alpha=0.9,

    edgecolor='black'

)


plt.title('Sub-Clusters K-Means (Ventas vs. Frecuencia - Solo Clase A)', fontsize=16, weight='bold')

plt.xlabel('Venta Total (Logarítmica)')

plt.ylabel('Frecuencia de Venta (Logarítmica)')

plt.legend(title='Sub-Clase A')

plt.show()



**OBSERVACIONES:** al ejecutar la sub-segmentación de K-Means! El gráfico muestra (con los 3 clusters de Clase A bien definidos) estamos usando la frecuencia para determinar si se venden con alta frecuencia o con baja dentro del grupo A y tambien si generan alta venta. Por lo que podemos determinar lo siguiente de los grupos



---



> Cluster A-Alta (Azul): "Vacas Lecheras". Productos de alta venta Y alta frecuencia. Son estables y fáciles de predecir. "Súper-Estrella". Generan alta venta Y se venden con alta frecuencia. Son las "vacas lecheras", predecibles y de alto valor.



---



> Cluster A-Media (Naranja): "Regulares". Venta y frecuencia media. Productos importantes con un comportamiento de venta y frecuencia intermedio.



---



> Cluster A-Baja (Verde): "Ballenas" o "Volátiles". Productos de alta venta (o valor) pero MUY baja frecuencia. Son difíciles e impredecibles. Estos son los más interesantes. Siguen siendo "Clase A" (generan buen volumen total), pero lo hacen con baja frecuencia y ventas más bajas (relativamente), estos son tus productos "volátiles" o "de oportunidad".



---




**DECISIÓN:** Para los productos de Clase A, no usaré un solo modelo. Usaré 3 modelos de pronóstico diferentes, uno para cada sub-clúster que K-Means encontró


# FILTRADO Y PREPARACIÓN DE PRODUCTOS CLASE A


## OTRO FILTRADO


# ============================================================================

# CELDA 8: PREPARACIÓN DE SERIES TEMPORALES CON SUBSEGMENTACIÓN K-MEANS

# Versión mejorada que integra los resultados de clustering de Celda 7.1

# ============================================================================




print("="*70)

print("📦 CELDA 8: SERIES TEMPORALES + SUBSEGMENTACIÓN K-MEANS")

print("="*70)


# ============================================================================

# VERIFICACIÓN DE DATOS REQUERIDOS

# ============================================================================


required_vars = {

    'ventas_normalizado': 'DataFrame con productos normalizados',

    'df_abc_final': 'DataFrame con clasificación ABC',

    'df_clase_a_subsegmented': 'DataFrame con subsegmentación K-Means de Clase A'

}


print("\n🔍 Verificando variables requeridas...")

for var_name, descripcion in required_vars.items():

    if var_name not in locals() and var_name not in globals():

        print(f"\n❌ ERROR: No se encuentra '{var_name}' ({descripcion})")

        if var_name == 'df_clase_a_subsegmented':

            print(f"   ⚠️  Ejecuta la CELDA 7.1 (subsegmentación K-Means) primero")

        else:

            print(f"   ⚠️  Ejecuta las celdas anteriores primero")

        raise NameError(f"Variable '{var_name}' no encontrada")


print("✅ Todas las variables encontradas\n")


# ============================================================================

# PASO 1: IDENTIFICAR PRODUCTOS CLASE A

# ============================================================================


def obtener_productos_clase_a(df_abc):

    """

    Extrae lista de productos clasificados como Clase A

    """

    print("🔍 PASO 1: Identificando productos Clase A...")


    productos_a = df_abc[df_abc['clase_abc'] == 'A - Alta']['producto'].tolist()


    print(f"✅ Productos Clase A identificados: {len(productos_a)}")


    # Mostrar estadísticas

    stats_a = df_abc[df_abc['clase_abc'] == 'A - Alta'].agg({

        'venta_total': ['sum', 'mean', 'min', 'max'],

        'qty_total': ['sum', 'mean'],

        'frecuencia': 'mean'

    })


    print(f"\n📊 Estadísticas Clase A:")

    print(f"  • Venta total: BS {stats_a['venta_total']['sum']:,.0f}")

    print(f"  • Venta promedio: BS {stats_a['venta_total']['mean']:,.0f}")

    print(f"  • Rango ventas: BS {stats_a['venta_total']['min']:,.0f} - BS {stats_a['venta_total']['max']:,.0f}")

    print(f"  • Cantidad total: {stats_a['qty_total']['sum']:,.0f} unidades")

    print(f"  • Frecuencia promedio: {stats_a['frecuencia']['mean']:.1f} pedidos")


    return productos_a


# ============================================================================

# PASO 2: FILTRAR DATASET COMPLETO PARA CLASE A

# ============================================================================


def filtrar_datos_clase_a(df_datos, productos_a):

    """

    Filtra el dataset completo dejando solo transacciones de productos Clase A

    """

    print("\n🔎 PASO 2: Filtrando dataset para productos Clase A...")


    # Filtrar

    df_clase_a = df_datos[df_datos['producto_normalizado'].isin(productos_a)].copy()


    # Asegurar formato fecha

    df_clase_a['Fecha'] = pd.to_datetime(df_clase_a['Fecha'], errors='coerce')


    # Ordenar por fecha

    df_clase_a = df_clase_a.sort_values('Fecha').reset_index(drop=True)


    print(f"✅ Dataset Clase A creado:")

    print(f"  • Registros totales: {len(df_clase_a):,}")

    print(f"  • Productos únicos: {df_clase_a['producto_normalizado'].nunique()}")

    print(f"  • Rango fechas: {df_clase_a['Fecha'].min().strftime('%Y-%m-%d')} → {df_clase_a['Fecha'].max().strftime('%Y-%m-%d')}")

    print(f"  • Venta total: BS {df_clase_a['Importe_Producto_BS'].sum():,.2f}")


    return df_clase_a


# ============================================================================

# PASO 3: CREAR SERIES TEMPORALES POR PRODUCTO (MENSUAL)

# ============================================================================


def crear_series_temporales_clase_a(df_clase_a, freq='M'):

    """

    Crea series temporales mensuales por cada producto Clase A


    Parámetros:

    -----------

    freq : str

        'M' = mensual (recomendado)

        'W' = semanal

        'Q' = trimestral

    """

    print(f"\n📅 PASO 3: Creando series temporales ({freq})...")


    # Crear periodo

    if freq == 'M':

        df_clase_a['periodo'] = df_clase_a['Fecha'].dt.to_period('M')

        periodo_nombre = "mensual"

    elif freq == 'W':

        df_clase_a['periodo'] = df_clase_a['Fecha'].dt.to_period('W')

        periodo_nombre = "semanal"

    elif freq == 'Q':

        df_clase_a['periodo'] = df_clase_a['Fecha'].dt.to_period('Q')

        periodo_nombre = "trimestral"

    else:

        raise ValueError("freq debe ser 'M', 'W' o 'Q'")


    # Agregar por producto y periodo

    series_temporales = df_clase_a.groupby(['producto_normalizado', 'periodo']).agg({

        'Cantidad': 'sum',

        'Importe_Producto_BS': 'sum',

        'Fecha': 'count'  # número de transacciones

    }).reset_index()


    series_temporales.columns = ['producto', 'periodo', 'cantidad_vendida',

                                 'venta_bs', 'num_transacciones']


    # Convertir periodo a timestamp para facilitar modelado

    series_temporales['fecha'] = series_temporales['periodo'].dt.to_timestamp()


    print(f"✅ Series temporales creadas:")

    print(f"  • Frecuencia: {periodo_nombre}")

    print(f"  • Productos: {series_temporales['producto'].nunique()}")

    print(f"  • Periodos totales: {len(series_temporales)}")

    print(f"  • Rango: {series_temporales['fecha'].min().strftime('%Y-%m-%d')} → {series_temporales['fecha'].max().strftime('%Y-%m-%d')}")


    return series_temporales


# ============================================================================

# PASO 4: COMPLETAR SERIES TEMPORALES (RELLENAR GAPS)

# ============================================================================


def completar_series_temporales(series_temporales):

    """

    Completa periodos faltantes con ceros (meses sin ventas).


    CRÍTICO para modelos de series temporales:

    - Sin este paso, no habría ejemplos de clase 0 (no venta)

    - Los modelos de clasificación necesitan ambas clases

    """

    print("\n🔧 PASO 4: Completando periodos faltantes (gaps)...")


    series_completas = []


    for producto in series_temporales['producto'].unique():

        subset = series_temporales[series_temporales['producto'] == producto].copy()


        # Crear rango completo de fechas

        fecha_min = subset['fecha'].min()

        fecha_max = subset['fecha'].max()


        rango_completo = pd.date_range(start=fecha_min, end=fecha_max, freq='MS')


        # Crear DataFrame con rango completo

        df_completo = pd.DataFrame({

            'fecha': rango_completo,

            'producto': producto

        })


        # Merge con datos reales

        df_completo = df_completo.merge(

            subset[['fecha', 'cantidad_vendida', 'venta_bs', 'num_transacciones']],

            on='fecha',

            how='left'

        )


        # Rellenar NaN con 0 (meses sin ventas)

        df_completo[['cantidad_vendida', 'venta_bs', 'num_transacciones']] = \

            df_completo[['cantidad_vendida', 'venta_bs', 'num_transacciones']].fillna(0)


        series_completas.append(df_completo)


    df_series_completas = pd.concat(series_completas, ignore_index=True)


    periodos_agregados = len(df_series_completas) - len(series_temporales)


    print(f"✅ Series completadas:")

    print(f"  • Registros antes: {len(series_temporales):,}")

    print(f"  • Registros después: {len(df_series_completas):,}")

    print(f"  • Periodos agregados (gaps): {periodos_agregados:,}")

    print(f"  • Porcentaje de gaps: {periodos_agregados/len(df_series_completas)*100:.1f}%")


    return df_series_completas


# ============================================================================

# PASO 4.5: INTEGRAR SUBSEGMENTACIÓN K-MEANS (NUEVO)

# ============================================================================


def integrar_subsegmentacion_kmeans(series_completas, df_subsegmentado):

    """

    Integra los resultados de K-Means (Celda 7.1) en las series temporales.


    CRÍTICO: Este paso conecta el clustering con el modelado de series temporales.

    Permite entrenar modelos específicos por sub-clúster (Vacas Lecheras, Regulares, Ballenas).


    Parámetros:

    -----------

    series_completas : DataFrame

        Series temporales completas (con gaps rellenados)

    df_subsegmentado : DataFrame

        Resultado de Celda 7.1 con columnas:

        - producto

        - cluster (0, 1, 2)

        - subclase_kmeans ('Vacas Lecheras', 'Regulares', 'Ballenas')


    Returns:

    --------

    DataFrame con columna adicional 'subclase_kmeans'

    """

    print("\n🔗 PASO 4.5: Integrando subsegmentación K-Means...")


    # Verificar que df_subsegmentado tenga las columnas necesarias

    columnas_requeridas = ['producto', 'subclase_kmeans']

    if not all(col in df_subsegmentado.columns for col in columnas_requeridas):

        print(f"❌ ERROR: df_clase_a_subsegmented debe tener columnas: {columnas_requeridas}")

        print(f"   Columnas encontradas: {df_subsegmentado.columns.tolist()}")

        raise ValueError("Columnas faltantes en df_subsegmentación")


    # Seleccionar solo las columnas necesarias para el merge

    subseg_map = df_subsegmentado[['producto', 'subclase_kmeans']].copy()


    # Verificar duplicados (cada producto debe tener una única subclase)

    if subseg_map.duplicated(subset=['producto']).any():

        print("⚠️  Advertencia: Productos duplicados en subsegmentación. Tomando el primero.")

        subseg_map = subseg_map.drop_duplicates(subset=['producto'], keep='first')


    # Merge con series temporales

    series_con_kmeans = series_completas.merge(

        subseg_map,

        on='producto',

        how='left'  # LEFT para mantener todos los productos, incluso si falta su subclase

    )


    # Verificar resultados del merge

    productos_sin_subclase = series_con_kmeans['subclase_kmeans'].isna().sum()


    if productos_sin_subclase > 0:

        print(f"⚠️  Advertencia: {productos_sin_subclase:,} registros sin subclase K-Means")

        print(f"   Esto puede ocurrir si hay productos nuevos o con datos insuficientes")


        # Opcional: Asignar una categoría por defecto

        series_con_kmeans['subclase_kmeans'] = series_con_kmeans['subclase_kmeans'].fillna('Sin Clasificar')


    # Estadísticas del merge

    print(f"\n✅ Subsegmentación integrada:")

    print(f"  • Total registros: {len(series_con_kmeans):,}")

    print(f"  • Registros con subclase: {(~series_con_kmeans['subclase_kmeans'].isna()).sum():,}")


    # Distribución por sub-clúster

    print(f"\n📊 Distribución de registros por sub-clúster:")

    distribucion = series_con_kmeans['subclase_kmeans'].value_counts()

    for subclase, count in distribucion.items():

        pct = (count / len(series_con_kmeans)) * 100

        print(f"  • {subclase}: {count:,} registros ({pct:.1f}%)")


    # Verificar que cada producto tenga una única subclase

    productos_con_multiples_subclases = series_con_kmeans.groupby('producto')['subclase_kmeans'].nunique()

    productos_inconsistentes = productos_con_multiples_subclases[productos_con_multiples_subclases > 1]


    if len(productos_inconsistentes) > 0:

        print(f"\n⚠️  ADVERTENCIA: {len(productos_inconsistentes)} productos tienen múltiples subclases")

        print(f"   Esto NO debería ocurrir. Verificar Celda 7.1")

    else:

        print(f"\n✅ Validación: Cada producto tiene una única subclase")


    return series_con_kmeans


# ============================================================================

# PASO 5: ANÁLISIS EXPLORATORIO POR SUBSEGMENTO

# ============================================================================


def analizar_por_subsegmento(series_con_kmeans):

    """

    Genera análisis exploratorio desagregado por sub-clúster K-Means

    """

    print("\n📊 PASO 5: Análisis exploratorio por subsegmento...")


    # Análisis por sub-clúster

    analisis_subsegmento = series_con_kmeans.groupby('subclase_kmeans').agg({

        'producto': 'nunique',

        'cantidad_vendida': ['mean', 'std', 'sum'],

        'venta_bs': ['mean', 'sum'],

        'num_transacciones': 'sum'

    }).reset_index()


    analisis_subsegmento.columns = [

        'subclase_kmeans', 'num_productos',

        'qty_promedio', 'qty_std', 'qty_total',

        'venta_promedio', 'venta_total', 'transacciones_total'

    ]


    # Calcular coeficiente de variación

    analisis_subsegmento['cv'] = analisis_subsegmento['qty_std'] / (analisis_subsegmento['qty_promedio'] + 1)


    print(f"\n{'='*70}")

    print("ANÁLISIS COMPARATIVO POR SUB-CLÚSTER")

    print(f"{'='*70}")


    for idx, row in analisis_subsegmento.iterrows():

        print(f"\n🏷️  {row['subclase_kmeans']}:")

        print(f"  • Productos: {int(row['num_productos'])}")

        print(f"  • Cantidad promedio: {row['qty_promedio']:.2f} ± {row['qty_std']:.2f}")

        print(f"  • Coeficiente de Variación (CV): {row['cv']:.2f}")

        print(f"  • Cantidad total: {row['qty_total']:,.0f} unidades")

        print(f"  • Venta total: BS {row['venta_total']:,.2f}")

        print(f"  • Transacciones: {int(row['transacciones_total']):,}")


    return analisis_subsegmento


# ============================================================================

# PASO 6: VISUALIZACIÓN COMPARATIVA

# ============================================================================


def visualizar_comparativo_subsegmentos(series_con_kmeans):

    """

    Visualiza comparación entre sub-clústeres

    """

    print("\n📊 PASO 6: Generando visualizaciones comparativas...")


    fig, axes = plt.subplots(2, 2, figsize=(16, 12))


    # 1. Distribución de cantidad vendida por sub-clúster

    ax1 = axes[0, 0]

    series_con_kmeans.boxplot(column='cantidad_vendida', by='subclase_kmeans', ax=ax1)

    ax1.set_title('Distribución de Cantidad Vendida por Sub-Clúster', fontsize=12, weight='bold')

    ax1.set_xlabel('Sub-Clúster')

    ax1.set_ylabel('Cantidad Vendida')

    plt.sca(ax1)

    plt.xticks(rotation=15)


    # 2. Frecuencia de ventas (registros > 0) por sub-clúster

    ax2 = axes[0, 1]

    freq_ventas = series_con_kmeans[series_con_kmeans['cantidad_vendida'] > 0].groupby('subclase_kmeans').size()

    freq_ventas.plot(kind='bar', ax=ax2, color=['#2ecc71', '#3498db', '#e74c3c'])

    ax2.set_title('Frecuencia de Ventas por Sub-Clúster', fontsize=12, weight='bold')

    ax2.set_xlabel('Sub-Clúster')

    ax2.set_ylabel('Número de Periodos con Venta')

    ax2.tick_params(axis='x', rotation=15)


    # 3. Proporción de gaps (periodos sin venta) por sub-clúster

    ax3 = axes[1, 0]

    gaps_analysis = series_con_kmeans.groupby('subclase_kmeans').agg({

        'cantidad_vendida': lambda x: (x == 0).sum() / len(x) * 100

    })

    gaps_analysis.plot(kind='bar', ax=ax3, color='coral', legend=False)

    ax3.set_title('Porcentaje de Periodos sin Venta (Gaps)', fontsize=12, weight='bold')

    ax3.set_xlabel('Sub-Clúster')

    ax3.set_ylabel('% Gaps')

    ax3.tick_params(axis='x', rotation=15)


    # 4. Serie temporal de un producto ejemplo por sub-clúster

    ax4 = axes[1, 1]

    for subclase in series_con_kmeans['subclase_kmeans'].unique():

        if pd.notna(subclase) and subclase != 'Sin Clasificar':

            subset = series_con_kmeans[series_con_kmeans['subclase_kmeans'] == subclase]

            # Tomar un producto representativo (el de mayor venta)

            prod_top = subset.groupby('producto')['cantidad_vendida'].sum().idxmax()

            serie_ejemplo = subset[subset['producto'] == prod_top].sort_values('fecha')


            ax4.plot(serie_ejemplo['fecha'], serie_ejemplo['cantidad_vendida'],

                    label=f"{subclase} ({prod_top[:20]}...)", marker='o', markersize=4)


    ax4.set_title('Ejemplos de Series Temporales por Sub-Clúster', fontsize=12, weight='bold')

    ax4.set_xlabel('Fecha')

    ax4.set_ylabel('Cantidad Vendida')

    ax4.legend(fontsize=8)

    ax4.grid(True, alpha=0.3)


    plt.tight_layout()

    plt.savefig('08_comparativo_subsegmentos_kmeans.png', dpi=150, bbox_inches='tight')

    print("✅ Gráfico guardado: 08_comparativo_subsegmentos_kmeans.png")

    plt.show()


# ============================================================================

# PASO 7: GUARDAR RESULTADOS

# ============================================================================


def guardar_resultados(df_clase_a, series_completas_con_kmeans, analisis_subsegmento):

    """

    Guarda todos los resultados de la celda

    """

    print("\n💾 PASO 7: Guardando resultados...")


    try:

        # 1. Datos transaccionales Clase A

        df_clase_a.to_excel('08_datos_clase_a.xlsx', index=False)

        print("✅ 08_datos_clase_a.xlsx")


        # 2. Series temporales completas CON subsegmentación

        series_completas_con_kmeans.to_excel('08_series_temporales_clase_a_con_kmeans.xlsx', index=False)

        print("✅ 08_series_temporales_clase_a_con_kmeans.xlsx")


        # 3. Análisis por subsegmento

        analisis_subsegmento.to_excel('08_analisis_subsegmentos.xlsx', index=False)

        print("✅ 08_analisis_subsegmentos.xlsx")


        print("\n✅ Todos los archivos guardados correctamente")


    except Exception as e:

        print(f"❌ Error al guardar archivos: {e}")


# ============================================================================

# MAIN: EJECUTAR TODO EL PIPELINE

# ============================================================================


def main():

    """

    Ejecuta todo el pipeline de preparación de series temporales

    """

    try:

        print("\n" + "="*70)

        print("EJECUTANDO PIPELINE COMPLETO")

        print("="*70)


        # PASO 1: Obtener productos A

        productos_clase_a = obtener_productos_clase_a(df_abc_final)


        # PASO 2: Filtrar datos

        df_clase_a = filtrar_datos_clase_a(ventas_normalizado, productos_clase_a)


        # PASO 3: Crear series temporales (MENSUAL)

        series_temporales_a = crear_series_temporales_clase_a(df_clase_a, freq='M')


        # PASO 4: Completar gaps

        series_completas_a = completar_series_temporales(series_temporales_a)


        # PASO 4.5: ⭐ INTEGRAR SUBSEGMENTACIÓN K-MEANS (NUEVO)

        series_completas_con_kmeans = integrar_subsegmentacion_kmeans(

            series_completas_a,

            df_clase_a_subsegmented

        )


        # PASO 5: Análisis por subsegmento

        analisis_subsegmento = analizar_por_subsegmento(series_completas_con_kmeans)


        # PASO 6: Visualizar

        visualizar_comparativo_subsegmentos(series_completas_con_kmeans)


        # PASO 7: Guardar resultados

        guardar_resultados(df_clase_a, series_completas_con_kmeans, analisis_subsegmento)


        # ====================================================================

        # RESUMEN FINAL

        # ====================================================================


        print("\n" + "="*70)

        print("✅ CELDA 8 COMPLETADA CON ÉXITO")

        print("="*70)

        print(f"""

Resumen:

  📦 Productos Clase A: {len(productos_clase_a)}

  📊 Registros históricos: {len(df_clase_a):,}

  📅 Periodos mensuales: {series_completas_con_kmeans['fecha'].nunique()}

  🏷️  Sub-clústeres K-Means: {series_completas_con_kmeans['subclase_kmeans'].nunique()}

  💰 Venta total: BS {df_clase_a['Importe_Producto_BS'].sum():,.2f}


Distribución por sub-clúster:

{series_completas_con_kmeans['subclase_kmeans'].value_counts().to_string()}


✅ Variable 'series_completas_con_kmeans' creada y lista para CELDA 9 (Modelado)


💡 PRÓXIMO PASO: En Celda 9, podrás entrenar modelos específicos por sub-clúster:

   - Modelo para "Vacas Lecheras" (alta frecuencia, bajo monto)

   - Modelo para "Regulares" (frecuencia media, monto medio)

   - Modelo para "Ballenas" (baja frecuencia, alto monto)

        """)


        # Retornar la variable principal para uso en siguientes celdas

        return series_completas_con_kmeans


    except Exception as e:

        print(f"\n❌ ERROR: {str(e)}")

        import traceback

        traceback.print_exc()

        raise


# ============================================================================

# EJECUTAR

# ============================================================================


if __name__ == "__main__":

    series_completas_a = main()

else:

    # Si se importa como módulo

    series_completas_a = main()


**OBSERVACIONES CLUSTER A.3:** Rellenó los meses sin venta (los 82 "gaps", que es un 15.1% de los datos). Veremos como quedaron los CLusters:

>Cluster "Vaca Lechera" (Estable y Predecible) **A.3 (Valor Bajo)**

por qué?:

* CV más bajo (0.70): Este es el grupo más estable

* En el grafico 2 muestra que tiene una de las barras más altas de "Frecuencia de Ventas"

* En el grafico 3 muestra que tiene una de las barras más bajas de "Períodos sin Venta"

* En el grafico 4 muestra su línea (verde) como la más consistente y menos volátil

**CONCLUSION:** Son 4 productos que se venden de forma constante y predecible.


---


**OBSERVACIONES CLUSTER A.2:**

>Cluster "Outlier Puro"

POR QUÉ?

* CV Explotado (3.15): El más volátil de todos

* El Gráfico 3 muestra que tiene el mayor porcentaje de meses sin venta.

* Gráfico de Serie Temporal: El Gráfico 4 (línea naranja) lo confirma: es una línea plana de ceros con un pico masivo e impredecible.

**CONCLUSION:** Este producto es una anomalía pura, por lo tanto se excluyera


---


**OBSERVACIONES CLUSTER A.1, A.4, A.5 :**

>Cluster "Los Volátiles"

POR QUE?

* CVs Altos (1.20, 1.53, 2.61): Todos son muy volátiles.

* En el grafico 1 muestra que A.1 y A.4 tienen rangos enormes y muchos outliers (los puntos).

* El Gráfico 3 muestra que A.5 (junto con A.2) es el que tiene más meses en cero (ventas intermitentes).

**CONCLUSION:** Estos 3 grupos (que suman 14 productos) son tus productos "Clase A" de alto riesgo: generan mucho valor pero son muy difíciles de predecir.


## PREPARACION DE SERIES TEMPORALES Y SEGEMENTACION DE K-MEANS SEGMENTADO


# ============================================================================

# CELDA 7.1: EJECUCIÓN de Sub-Segmentación K-Means (SÓLO CLASE A)

#

# OBJETIVO:

# 1. Filtrar los productos 'Clase A' (del Bloque 1 de Celda 7).

# 2. Ejecutar la función 'subsegmentar_clase_a_kmeans' (Definición 4 de Celda 7).

# 3. Guardar los resultados en variables globales para la celda de visualización.

# ============================================================================

import pandas as pd

import traceback


print("\n" + "="*70)

print("🚀 EJECUTANDO: SUB-SEGMENTACIÓN K-MEANS (SÓLO CLASE A)")

print("="*70)


# El bloque 'try' comienza sin sangría

try:

    # El código DENTRO de 'try' DEBE tener 1 nivel de sangría (4 espacios)

    if 'df_abc_final' not in locals():

        raise NameError("No se encontró 'df_abc_final'. Asegúrese de que el Bloque 1 (ABC) de la Celda 7 se haya ejecutado.")


    # 1. Filtrar solo los datos de Clase A del resultado de ABC

    # Esta es la lógica que pegaste, ahora con la sangría correcta

    df_clase_a_data = df_abc_final[df_abc_final['clase_abc'] == 'A - Alta'].copy()

    if 'producto' in df_clase_a_data.columns:

        df_clase_a_data['producto'] = df_clase_a_data['producto'].str.strip()

    else:

        print("ADVERTENCIA: No se encontró la columna 'producto' en df_clase_a_data")

    # --- FIN DE LA CORRECCIÓN ---

    if len(df_clase_a_data) < 2:

        # El código DENTRO de 'if' DEBE tener 2 niveles de sangría (8 espacios)

        print(f"⚠️  No hay suficientes productos en Clase A ({len(df_clase_a_data)}) para sub-segmentar. Omitiendo.")

        # Crear variables vacías para que la celda de visualización no falle

        df_clase_a_subsegmented = pd.DataFrame()

        sil_scores_a = []

        inertias_a = []

    else:

        # El código DENTRO de 'else' DEBE tener 2 niveles de sangría (8 espacios)

        print(f"Sub-segmentando {len(df_clase_a_data)} productos de Clase A...")


        # 2. Ejecutar la nueva función de sub-segmentación

        # Asumimos que subsegmentar_clase_a_kmeans está definida en la Celda 7.0

        # Estas variables se crean como globales y serán usadas por la Celda 7.2

        df_clase_a_subsegmented, sil_scores_a, inertias_a = subsegmentar_clase_a_kmeans(

            df_clase_a_data

        )


        df_clase_a_subsegmented.to_excel('07_clasificacion_clase_A_subsegmentos.xlsx', index=False)

        print("✅ 07_clasificacion_clase_A_subsegmentos.xlsx (Sub-segmentos de Clase A)")


# El bloque 'except' DEBE estar alineado con 'try' (sin sangría)

except Exception as e:

    # El código DENTRO de 'except' DEBE tener 1 nivel de sangría (4 espacios)

    print(f"❌ ERROR durante la sub-segmentación de Clase A: {e}")

    traceback.print_exc()


# Este print está FUERA del 'try...except' (sin sangría)

print("\n✅ EJECUCIÓN de Sub-segmentación (Clase A) completada.")

print("➡️  PRÓXIMO PASO: Celda 7.2 (Visualización de Sub-segmentos).")


# ============================================================================

# CELDA 8: PREPARACIÓN DE SERIES TEMPORALES CON SUBSEGMENTACIÓN K-MEANS

# Versión mejorada que integra los resultados de clustering de Celda 7.1

# ============================================================================


import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from datetime import datetime

import warnings

warnings.filterwarnings('ignore')


print("="*70)

print("📦 CELDA 8: SERIES TEMPORALES + SUBSEGMENTACIÓN K-MEANS")

print("="*70)


# ============================================================================

# VERIFICACIÓN DE DATOS REQUERIDOS

# ============================================================================


required_vars = {

    'ventas_normalizado': 'DataFrame con productos normalizados',

    'df_abc_final': 'DataFrame con clasificación ABC',

    'df_clase_a_subsegmented': 'DataFrame con subsegmentación K-Means de Clase A'

}


print("\n🔍 Verificando variables requeridas...")

for var_name, descripcion in required_vars.items():

    if var_name not in locals() and var_name not in globals():

        print(f"\n❌ ERROR: No se encuentra '{var_name}' ({descripcion})")

        if var_name == 'df_clase_a_subsegmented':

            print(f"    ⚠️  Ejecuta la CELDA 7.1 (subsegmentación K-Means) primero")

        else:

            print(f"    ⚠️  Ejecuta las celdas anteriores primero")

        raise NameError(f"Variable '{var_name}' no encontrada")


print("✅ Todas las variables encontradas\n")


# ============================================================================

# PASO 1: IDENTIFICAR PRODUCTOS CLASE A

# ============================================================================


def obtener_productos_clase_a(df_abc):

    """

    Extrae lista de productos clasificados como Clase A

    """

    print("🔍 PASO 1: Identificando productos Clase A...")


    productos_a = df_abc[df_abc['clase_abc'] == 'A - Alta']['producto'].tolist()


    print(f"✅ Productos Clase A identificados: {len(productos_a)}")


    # Mostrar estadísticas

    stats_a = df_abc[df_abc['clase_abc'] == 'A - Alta'].agg({

        'venta_total': ['sum', 'mean', 'min', 'max'],

        'qty_total': ['sum', 'mean'],

        'frecuencia': 'mean'

    })


    print(f"\n📊 Estadísticas Clase A:")

    print(f"  • Venta total: BS {stats_a['venta_total']['sum']:,.0f}")

    print(f"  • Venta promedio: BS {stats_a['venta_total']['mean']:,.0f}")

    print(f"  • Rango ventas: BS {stats_a['venta_total']['min']:,.0f} - BS {stats_a['venta_total']['max']:,.0f}")

    print(f"  • Cantidad total: {stats_a['qty_total']['sum']:,.0f} unidades")

    print(f"  • Frecuencia promedio: {stats_a['frecuencia']['mean']:.1f} pedidos")


    return productos_a


# ============================================================================

# PASO 2: FILTRAR DATASET COMPLETO PARA CLASE A

# ============================================================================


def filtrar_datos_clase_a(df_datos, productos_a):

    """

    Filtra el dataset completo dejando solo transacciones de productos Clase A

    """

    print("\n🔎 PASO 2: Filtrando dataset para productos Clase A...")


    # Filtrar

    df_clase_a = df_datos[df_datos['producto_normalizado'].isin(productos_a)].copy()


    # Asegurar formato fecha

    df_clase_a['Fecha'] = pd.to_datetime(df_clase_a['Fecha'], errors='coerce')


    # Ordenar por fecha

    df_clase_a = df_clase_a.sort_values('Fecha').reset_index(drop=True)


    print(f"✅ Dataset Clase A creado:")

    print(f"  • Registros totales: {len(df_clase_a):,}")

    print(f"  • Productos únicos: {df_clase_a['producto_normalizado'].nunique()}")

    print(f"  • Rango fechas: {df_clase_a['Fecha'].min().strftime('%Y-%m-%d')} → {df_clase_a['Fecha'].max().strftime('%Y-%m-%d')}")

    print(f"  • Venta total: BS {df_clase_a['Importe_Producto_BS'].sum():,.2f}")


    return df_clase_a


# ============================================================================

# PASO 3: CREAR SERIES TEMPORALES POR PRODUCTO (MENSUAL)

# ============================================================================


def crear_series_temporales_clase_a(df_clase_a, freq='M'):

    """

    Crea series temporales mensuales por cada producto Clase A


    Parámetros:

    -----------

    freq : str

        'M' = mensual (recomendado)

        'W' = semanal

        'Q' = trimestral

    """

    print(f"\n📅 PASO 3: Creando series temporales ({freq})...")


    # Crear periodo

    if freq == 'M':

        df_clase_a['periodo'] = df_clase_a['Fecha'].dt.to_period('M')

        periodo_nombre = "mensual"

    elif freq == 'W':

        df_clase_a['periodo'] = df_clase_a['Fecha'].dt.to_period('W')

        periodo_nombre = "semanal"

    elif freq == 'Q':

        df_clase_a['periodo'] = df_clase_a['Fecha'].dt.to_period('Q')

        periodo_nombre = "trimestral"

    else:

        raise ValueError("freq debe ser 'M', 'W' o 'Q'")


    # Agregar por producto y periodo

    series_temporales = df_clase_a.groupby(['producto_normalizado', 'periodo']).agg({

        'Cantidad': 'sum',

        'Importe_Producto_BS': 'sum',

        'Fecha': 'count'  # número de transacciones

    }).reset_index()


    series_temporales.columns = ['producto', 'periodo', 'cantidad_vendida',

                                 'venta_bs', 'num_transacciones']


    # Convertir periodo a timestamp para facilitar modelado

    series_temporales['fecha'] = series_temporales['periodo'].dt.to_timestamp()


    print(f"✅ Series temporales creadas:")

    print(f"  • Frecuencia: {periodo_nombre}")

    print(f"  • Productos: {series_temporales['producto'].nunique()}")

    print(f"  • Periodos totales: {len(series_temporales)}")

    print(f"  • Rango: {series_temporales['fecha'].min().strftime('%Y-%m-%d')} → {series_temporales['fecha'].max().strftime('%Y-%m-%d')}")


    return series_temporales


# ============================================================================

# PASO 4: COMPLETAR SERIES TEMPORALES (RELLENAR GAPS)

# ============================================================================


def completar_series_temporales(series_temporales):

    """

    Completa periodos faltantes con ceros (meses sin ventas).


    CRÍTICO para modelos de series temporales:

    - Sin este paso, no habría ejemplos de clase 0 (no venta)

    - Los modelos de clasificación necesitan ambas clases

    """

    print("\n🔧 PASO 4: Completando periodos faltantes (gaps)...")


    series_completas = []


    # Determinar el rango global de fechas para todos los productos

    fecha_min_global = series_temporales['fecha'].min()

    fecha_max_global = series_temporales['fecha'].max()

    rango_completo_global = pd.date_range(start=fecha_min_global, end=fecha_max_global, freq='MS')


    print(f"   > Rango global de fechas: {fecha_min_global.date()} a {fecha_max_global.date()}")


    for producto in series_temporales['producto'].unique():

        subset = series_temporales[series_temporales['producto'] == producto].copy()


        # Crear DataFrame con rango completo

        df_completo = pd.DataFrame({

            'fecha': rango_completo_global,

            'producto': producto

        })


        # Merge con datos reales del producto

        df_completo = df_completo.merge(

            subset[['fecha', 'cantidad_vendida', 'venta_bs', 'num_transacciones']],

            on='fecha',

            how='left'

        )


        # Rellenar NaN con 0 (meses sin ventas)

        df_completo[['cantidad_vendida', 'venta_bs', 'num_transacciones']] = \

            df_completo[['cantidad_vendida', 'venta_bs', 'num_transacciones']].fillna(0)


        series_completas.append(df_completo)


    df_series_completas = pd.concat(series_completas, ignore_index=True)


    periodos_agregados = len(df_series_completas) - len(series_temporales)


    print(f"✅ Series completadas (alineadas globalmente):")

    print(f"  • Registros antes: {len(series_temporales):,}")

    print(f"  • Registros después: {len(df_series_completas):,}")

    print(f"  • Periodos agregados (gaps): {periodos_agregados:,}")

    print(f"  • Porcentaje de gaps: {periodos_agregados/max(1, len(df_series_completas))*100:.1f}%")


    return df_series_completas


# ============================================================================

# PASO 4.5: INTEGRAR SUBSEGMENTACIÓN K-MEANS (NUEVO)

# ============================================================================


def integrar_subsegmentacion_kmeans(series_completas, df_subsegmentado):

    """

    Integra los resultados de K-Means (Celda 7.1) en las series temporales.


    CRÍTICO: Este paso conecta el clustering con el modelado de series temporales.

    Permite entrenar modelos específicos por sub-clúster (Vacas Lecheras, Regulares, Ballenas).


    Parámetros:

    -----------

    series_completas : DataFrame

        Series temporales completas (con gaps rellenados)

    df_subsegmentado : DataFrame

        Resultado de Celda 7.1 con columnas:

        - producto

        - cluster (0, 1, 2)

        - subclase_kmeans ('Vacas Lecheras', 'Regulares', 'Ballenas')


    Returns:

    --------

    DataFrame con columna adicional 'subclase_kmeans'

    """

    print("\n🔗 PASO 4.5: Integrando subsegmentación K-Means...")


    # Verificar que df_subsegmentado tenga las columnas necesarias

    columnas_requeridas = ['producto', 'subclase_kmeans']

    if not all(col in df_subsegmentado.columns for col in columnas_requeridas):

        print(f"❌ ERROR: df_clase_a_subsegmented debe tener columnas: {columnas_requeridas}")

        print(f"    Columnas encontradas: {df_subsegmentado.columns.tolist()}")

        raise ValueError("Columnas faltantes en df_subsegmentación")


    # Seleccionar solo las columnas necesarias para el merge

    subseg_map = df_subsegmentado[['producto', 'subclase_kmeans']].copy()


    # Verificar duplicados (cada producto debe tener una única subclase)

    if subseg_map.duplicated(subset=['producto']).any():

        print("⚠️  Advertencia: Productos duplicados en subsegmentación. Tomando el primero.")

        subseg_map = subseg_map.drop_duplicates(subset=['producto'], keep='first')


    # Merge con series temporales

    series_con_kmeans = series_completas.merge(

        subseg_map,

        on='producto',

        how='left'  # LEFT para mantener todos los productos, incluso si falta su subclase

    )


    # Verificar resultados del merge

    productos_sin_subclase = series_con_kmeans['subclase_kmeans'].isna().sum()


    if productos_sin_subclase > 0:

        print(f"⚠️  Advertencia: {productos_sin_subclase:,} registros sin subclase K-Means")

        print(f"    Esto puede ocurrir si hay productos nuevos o con datos insuficientes")


        # Asignar una categoría por defecto

        series_con_kmeans['subclase_kmeans'] = series_con_kmeans['subclase_kmeans'].fillna('Sin Clasificar')


    # Estadísticas del merge

    print(f"\n✅ Subsegmentación integrada:")

    print(f"  • Total registros: {len(series_con_kmeans):,}")

    print(f"  • Registros con subclase: {(~series_con_kmeans['subclase_kmeans'].isna()).sum():,}")


    # Distribución por sub-clúster

    print(f"\n📊 Distribución de registros por sub-clúster:")

    distribucion = series_con_kmeans['subclase_kmeans'].value_counts()

    for subclase, count in distribucion.items():

        pct = (count / len(series_con_kmeans)) * 100

        print(f"  • {subclase}: {count:,} registros ({pct:.1f}%)")


    # Verificar que cada producto tenga una única subclase

    productos_con_multiples_subclases = series_con_kmeans.groupby('producto')['subclase_kmeans'].nunique()

    productos_inconsistentes = productos_con_multiples_subclases[productos_con_multiples_subclases > 1]


    if len(productos_inconsistentes) > 0:

        print(f"\n⚠️  ADVERTENCIA: {len(productos_inconsistentes)} productos tienen múltiples subclases")

        print(f"    Esto NO debería ocurrir. Verificar Celda 7.1")

    else:

        print(f"\n✅ Validación: Cada producto tiene una única subclase")


    return series_con_kmeans


# ============================================================================

# PASO 5: ANÁLISIS EXPLORATORIO POR SUBSEGMENTO

# ============================================================================


def analizar_por_subsegmento(series_con_kmeans):

    """

    Genera análisis exploratorio desagregado por sub-clúster K-Means

    """

    print("\n📊 PASO 5: Análisis exploratorio por subsegmento...")


    # Análisis por sub-clúster

    analisis_subsegmento = series_con_kmeans.groupby('subclase_kmeans').agg({

        'producto': 'nunique',

        'cantidad_vendida': ['mean', 'std', 'sum'],

        'venta_bs': ['mean', 'sum'],

        'num_transacciones': 'sum'

    }).reset_index()


    analisis_subsegmento.columns = [

        'subclase_kmeans', 'num_productos',

        'qty_promedio', 'qty_std', 'qty_total',

        'venta_promedio', 'venta_total', 'transacciones_total'

    ]


    # Calcular coeficiente de variación

    analisis_subsegmento['cv'] = analisis_subsegmento['qty_std'] / (analisis_subsegmento['qty_promedio'] + 1e-6) # Evitar división por cero


    print(f"\n{'='*70}")

    print("ANÁLISIS COMPARATIVO POR SUB-CLÚSTER")

    print(f"{'='*70}")


    for idx, row in analisis_subsegmento.iterrows():

        print(f"\n🏷️   {row['subclase_kmeans']}:")

        print(f"  • Productos: {int(row['num_productos'])}")

        print(f"  • Cantidad promedio (mensual): {row['qty_promedio']:.2f} ± {row['qty_std']:.2f}")

        print(f"  • Coeficiente de Variación (CV): {row['cv']:.2f}")

        print(f"  • Cantidad total: {row['qty_total']:,.0f} unidades")

        print(f"  • Venta total: BS {row['venta_total']:,.2f}")

        print(f"  • Transacciones: {int(row['transacciones_total']):,}")


    return analisis_subsegmento


# ============================================================================

# PASO 6: VISUALIZACIÓN COMPARATIVA

# ============================================================================


def visualizar_comparativo_subsegmentos(series_con_kmeans):

    """

    Visualiza comparación entre sub-clústeres

    """

    print("\n📊 PASO 6: Generando visualizaciones comparativas...")


    fig, axes = plt.subplots(2, 2, figsize=(16, 12))


    # 1. Distribución de cantidad vendida por sub-clúster (SIN OUTLIERS)

    ax1 = axes[0, 0]

    sns.boxplot(

        data=series_con_kmeans,

        x='subclase_kmeans',

        y='cantidad_vendida',

        ax=ax1,

        showfliers=False, # Ocultar outliers para ver mejor las cajas

        palette='deep'

    )

    ax1.set_title('Distribución de Cantidad Vendida (sin outliers)', fontsize=12, weight='bold')

    ax1.set_xlabel('Sub-Clúster')

    ax1.set_ylabel('Cantidad Vendida (Mensual)')

    ax1.tick_params(axis='x', rotation=15)


    # 2. Frecuencia de ventas (registros > 0) por sub-clúster

    ax2 = axes[0, 1]

    freq_ventas = series_con_kmeans[series_con_kmeans['cantidad_vendida'] > 0].groupby('subclase_kmeans').size().sort_values(ascending=False)

    freq_ventas.plot(kind='bar', ax=ax2, color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6'])

    ax2.set_title('Frecuencia de Ventas por Sub-Clúster', fontsize=12, weight='bold')

    ax2.set_xlabel('Sub-Clúster')

    ax2.set_ylabel('Número de Periodos con Venta')

    ax2.tick_params(axis='x', rotation=15)


    # 3. Proporción de gaps (periodos sin venta) por sub-clúster

    ax3 = axes[1, 0]

    gaps_analysis = series_con_kmeans.groupby('subclase_kmeans').agg({

        'cantidad_vendida': lambda x: (x == 0).sum() / len(x) * 100

    }).sort_values('cantidad_vendida', ascending=False)


    gaps_analysis.plot(kind='bar', ax=ax3, color='coral', legend=False)

    ax3.set_title('Porcentaje de Periodos sin Venta (Gaps)', fontsize=12, weight='bold')

    ax3.set_xlabel('Sub-Clúster')

    ax3.set_ylabel('% Gaps')

    ax3.tick_params(axis='x', rotation=15)


    # 4. Serie temporal de un producto ejemplo por sub-clúster

    ax4 = axes[1, 1]

    # Usar un colormap

    colors = plt.cm.get_cmap('tab10', len(series_con_kmeans['subclase_kmeans'].unique()))


    for i, subclase in enumerate(series_con_kmeans['subclase_kmeans'].unique()):

        if pd.notna(subclase) and subclase != 'Sin Clasificar':

            subset = series_con_kmeans[series_con_kmeans['subclase_kmeans'] == subclase]

            # Tomar un producto representativo (el de mayor venta)

            prod_top = subset.groupby('producto')['cantidad_vendida'].sum().idxmax()

            serie_ejemplo = subset[subset['producto'] == prod_top].sort_values('fecha')


            ax4.plot(serie_ejemplo['fecha'], serie_ejemplo['cantidad_vendida'],

                     label=f"{subclase} ({prod_top[:20]}...)",

                     marker='o', markersize=4, color=colors(i))


    ax4.set_title('Ejemplos de Series Temporales por Sub-Clúster', fontsize=12, weight='bold')

    ax4.set_xlabel('Fecha')

    ax4.set_ylabel('Cantidad Vendida')

    ax4.legend(fontsize=8, loc='upper left')

    ax4.grid(True, alpha=0.3)


    plt.tight_layout()

    plt.savefig('08_comparativo_subsegmentos_kmeans.png', dpi=150, bbox_inches='tight')

    print("✅ Gráfico guardado: 08_comparativo_subsegmentos_kmeans.png")

    plt.show()


# ============================================================================

# PASO 7: GUARDAR RESULTADOS

# ============================================================================


def guardar_resultados(df_clase_a, series_completas_con_kmeans, analisis_subsegmento):

    """

    Guarda todos los resultados de la celda

    """

    print("\n💾 PASO 7: Guardando resultados...")


    try:

        # 1. Datos transaccionales Clase A

        df_clase_a.to_excel('08_datos_clase_a.xlsx', index=False)

        print("✅ 08_datos_clase_a.xlsx")


        # 2. Series temporales completas CON subsegmentación

        series_completas_con_kmeans.to_excel('08_series_temporales_clase_a_con_kmeans.xlsx', index=False)

        print("✅ 08_series_temporales_clase_a_con_kmeans.xlsx")


        # 3. Análisis por subsegmento

        analisis_subsegmento.to_excel('08_analisis_subsegmentos.xlsx', index=False)

        print("✅ 08_analisis_subsegmentos.xlsx")


        print("\n✅ Todos los archivos guardados correctamente")


    except Exception as e:

        print(f"❌ Error al guardar archivos: {e}")


# ============================================================================

# MAIN: EJECUTAR TODO EL PIPELINE

# ============================================================================


def main():

    """

    Ejecuta todo el pipeline de preparación de series temporales

    """

    try:

        print("\n" + "="*70)

        print("EJECUTANDO PIPELINE COMPLETO")

        print("="*70)


        # PASO 1: Obtener productos A

        productos_clase_a = obtener_productos_clase_a(df_abc_final)


        # PASO 2: Filtrar datos

        df_clase_a = filtrar_datos_clase_a(ventas_normalizado, productos_clase_a)


        if df_clase_a.empty:

            print("⚠️ No se encontraron registros de ventas para los productos Clase A. El proceso se detiene.")

            return None # Retornar None si no hay datos


        # PASO 3: Crear series temporales (MENSUAL)

        series_temporales_a = crear_series_temporales_clase_a(df_clase_a, freq='M')


        if series_temporales_a.empty:

            print("⚠️ No se pudieron crear series temporales. El proceso se detiene.")

            return None # Retornar None


        # PASO 4: Completar gaps

        series_completas_a = completar_series_temporales(series_temporales_a)


        # PASO 4.5: ⭐ INTEGRAR SUBSEGMENTACIÓN K-MEANS (NUEVO)

        series_completas_con_kmeans = integrar_subsegmentacion_kmeans(

            series_completas_a,

            df_clase_a_subsegmented

        )


        # PASO 5: Análisis por subsegmento

        analisis_subsegmento = analizar_por_subsegmento(series_completas_con_kmeans)


        # PASO 6: Visualizar

        visualizar_comparativo_subsegmentos(series_completas_con_kmeans)


        # PASO 7: Guardar resultados

        guardar_resultados(df_clase_a, series_completas_con_kmeans, analisis_subsegmento)


        # ====================================================================

        # RESUMEN FINAL

        # ====================================================================


        print("\n" + "="*70)

        print("✅ CELDA 8 COMPLETADA CON ÉXITO")

        print("="*70)

        print(f"""

Resumen:

  📦 Productos Clase A: {len(productos_clase_a)}

  📊 Registros históricos: {len(df_clase_a):,}

  📅 Periodos mensuales: {series_completas_con_kmeans['fecha'].nunique()}

  🏷️   Sub-clústeres K-Means: {series_completas_con_kmeans['subclase_kmeans'].nunique()}

  💰 Venta total: BS {df_clase_a['Importe_Producto_BS'].sum():,.2f}


Distribución por sub-clúster:

{series_completas_con_kmeans['subclase_kmeans'].value_counts().to_string()}


✅ Variable 'series_completas_con_kmeans' creada y lista para CELDA 9 (Modelado)


💡 PRÓXIMO PASO: En Celda 9, podrás entrenar modelos específicos por sub-clúster:

   - Modelo para '1. Nucleo Estable'

   - Modelo para '2. Volumen Inconsistente'

   - Modelo para '3. Venta Ocasional (Riesgo Alto)'

        """)


        # Retornar la variable principal para uso en siguientes celdas

        return series_completas_con_kmeans


    except Exception as e:

        print(f"\n❌ ERROR: {str(e)}")

        import traceback

        traceback.print_exc()

        raise


# ============================================================================

# EJECUTAR

# ============================================================================


# Usar '__name__ == "__main__"' es una buena práctica para scripts de Python,

# pero en un notebook, simplemente llamar a main() está bien.

# Lo mantenemos para robustez.

if __name__ == "__main__" or "google.colab" in str(get_ipython()):

    series_completas_con_kmeans = main()


## CELDA 10.5 Entrena


# ============================================================================

# CELDA 10.5: MODELO DOBLE-CLASIFICADOR (CLASIFICADOR BINARIO + RANGOS)

#

# VERSIÓN 2: Simplificado a 2 Rangos (Baja/Alta)

#

# ARQUITECTURA:

# 1. Clasificador Binario: ¿Venta o No Venta? (Ya funciona)

# 2. Clasificador de Rangos: Si hay venta, ¿es Baja (0-50%) o Alta (50-100%)?

# ============================================================================


import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

import joblib

import os

import json

import warnings

warnings.filterwarnings('ignore')


from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (

    classification_report, confusion_matrix, roc_auc_score, roc_curve,

    f1_score, precision_score, recall_score, accuracy_score

)


# --- Importar Configuración ---

try:

    from configuracion_global import RANDOM_STATE, TEST_SIZE_FRAC, BASE_EXPORT_DIR

except ImportError:

    RANDOM_STATE = 42

    TEST_SIZE_FRAC = 0.2

    BASE_EXPORT_DIR = 'modelos_exportados'


print("="*80)

print("🎯 CELDA 10.5: MODELO DOBLE-CLASIFICADOR (2 RANGOS)")

print("="*80)


# ============================================================================

# CONFIGURACIÓN

# ============================================================================

UMBRAL_MINIMO_DATOS = 80

UMBRAL_PROB_DEFAULT = 0.5

CLUSTERS_A_EXCLUIR = ['4. Anomalia (Excluir)', 'Anomalía', 'Anomalia' ] #'A.2 (Valor Medio)' RECOMENDACIONES Y LIMITACIONES


# Hiperparámetros

HPARAMS_CLASIFICADOR_BINARIO = {

    'n_estimators': 100,

    'max_depth': 8,

    'min_samples_split': 10,

    'min_samples_leaf': 5,

    'random_state': RANDOM_STATE,

    'n_jobs': -1

}


# Hiperparámetros Optimizados (de la iteración anterior)

HPARAMS_CLASIFICADOR_RANGOS = {

    'n_estimators': 150,

    'max_depth': 10,

    'min_samples_split': 5,

    'min_samples_leaf': 5,

    'random_state': RANDOM_STATE,

    'n_jobs': -1,

    'class_weight': 'balanced'

}



print(f"\n⚙️ CONFIGURACIÓN:")

print(f"    • Datos mínimos: {UMBRAL_MINIMO_DATOS} filas")

print(f"    • Clasificador 1: Binario (Venta/No Venta)")

print(f"    • Clasificador 2: 2 Rangos (Baja/Alta)")


# ============================================================================

# VERIFICACIÓN

# ============================================================================

if 'series_completas_con_kmeans' not in locals() and 'series_completas_con_kmeans' not in globals():

    raise NameError("❌ 'series_completas_con_kmeans' no encontrado")


print(f"✅ Dataset cargado: {len(series_completas_con_kmeans):,} filas\n")


# ============================================================================

# PREPARACIÓN DE DATOS CON 2 RANGOS

# ============================================================================


def preparar_datos_doble_clasificador(df_segmento):

    """

    Prepara datos para modelo doble-clasificador:

    1. Target binario: venta_ocurrio (0/1)

    2. Target rangos: rango_venta (0=Baja, 1=Alta)

    3. Features de Precio y Operacionales

    """

    print("    > Preparando datos para doble-clasificador...")


    df_prep = df_segmento.copy()


    # Target 1: Clasificación binaria

    df_prep['venta_ocurrio'] = (df_prep['cantidad_vendida'] > 0).astype(int)


    # ====================================================================

    # Target 2: Clasificación de Rangos (2 RANGOS)

    # ====================================================================

    ventas_positivas = df_prep[df_prep['venta_ocurrio'] == 1]['cantidad_vendida']


    limites_rangos = None

    df_prep['rango_venta'] = -1  # Default para 'No Venta'


    if len(ventas_positivas) > 30:

        # Calcular mediana (cuantil 0.50)

        q_50 = ventas_positivas.quantile(0.50)


        limites_rangos = {'q_50': float(q_50)}

        print(f"    > Límites de rangos calculados (2 RANGOS):")

        print(f"        • Baja (0): < {q_50:.1f}")

        print(f"        • Alta (1): >= {q_50:.1f}")


        # Crear target multi-clase (0=Baja, 1=Alta)

        indices_venta = df_prep[df_prep['venta_ocurrio'] == 1].index


        df_prep.loc[indices_venta, 'rango_venta'] = pd.cut(

            ventas_positivas,

            bins=[-np.inf, q_50, np.inf],

            labels=[0, 1], # 0=Baja, 1=Alta

            right=False # ¡Importante! q_50 va a la clase Alta

        ).astype(int)


        # Distribución de rangos

        dist_rangos = df_prep[df_prep['rango_venta'] >= 0]['rango_venta'].value_counts().sort_index()

        print(f"    > Distribución de rangos:")

        print(f"        • Baja (0): {dist_rangos.get(0, 0)} muestras")

        print(f"        • Alta (1): {dist_rangos.get(1, 0)} muestras")

    else:

        print(f"    > ⚠️ No hay suficientes ventas ({len(ventas_positivas)}) para definir rangos")


    # ====================================================================

    # FEATURE ENGINEERING

    # ====================================================================


    features_list = []


    print("    > Generando features de Precio y Operacionales...")

    for producto in df_prep['producto'].unique():

        df_prod = df_prep[df_prep['producto'] == producto].sort_values('fecha').copy()


        # 1. FEATURES DE PRECIO

        cantidad_segura = df_prod['cantidad_vendida'].replace(0, np.nan)

        df_prod['precio_implicito'] = df_prod['venta_bs'] / cantidad_segura

        df_prod['precio_implicito'] = df_prod['precio_implicito'].ffill().bfill()

        df_prod['precio_implicito'] = df_prod['precio_implicito'].fillna(0)


        precio_medio_hist = df_prod['precio_implicito'].mean()

        if precio_medio_hist > 0:

            df_prod['precio_relativo'] = (df_prod['precio_implicito'] / precio_medio_hist) - 1.0

        else:

            df_prod['precio_relativo'] = 0.0


        df_prod['hubo_descuento_implicito'] = (df_prod['precio_relativo'] < -0.05).astype(int)


        # 2. FEATURES OPERACIONALES

        df_prod['fecha_ultima_compra'] = df_prod['fecha'].where(df_prod['venta_ocurrio'] == 1).ffill()

        if 'fecha_ultima_compra' in df_prod.columns:

            df_prod['dias_desde_ultima_compra'] = (df_prod['fecha'] - df_prod['fecha_ultima_compra']).dt.days

            df_prod['dias_desde_ultima_compra'] = df_prod['dias_desde_ultima_compra'].fillna(0).astype(int)

        else:

            df_prod['dias_desde_ultima_compra'] = 0


        racha_no_venta = (df_prod['venta_ocurrio'] != 0).cumsum()

        df_prod['racha_de_no_venta'] = df_prod.groupby(racha_no_venta).cumcount()


        # 3. FEATURES TEMPORALES Y LAGS

        df_prod['mes'] = df_prod['fecha'].dt.month

        df_prod['trimestre'] = df_prod['fecha'].dt.quarter

        df_prod['mes_sin'] = np.sin(2 * np.pi * df_prod['mes'] / 12)

        df_prod['mes_cos'] = np.cos(2 * np.pi * df_prod['mes'] / 12)


        for lag in [1, 3, 6]:

            df_prod[f'lag_{lag}'] = df_prod['cantidad_vendida'].shift(lag)

            df_prod[f'venta_ocurrio_lag_{lag}'] = df_prod['venta_ocurrio'].shift(lag)


        for ventana in [3, 6]:

            df_prod[f'media_movil_{ventana}'] = (

                df_prod['cantidad_vendida'].shift(1)

                .rolling(window=ventana, min_periods=1).mean()

            )


        for ventana in [3, 6, 12]:

            df_prod[f'tasa_ocurrencia_{ventana}'] = (

                df_prod['venta_ocurrio'].shift(1)

                .rolling(window=ventana, min_periods=1).mean()

            )


        features_list.append(df_prod)


    df_features = pd.concat(features_list, ignore_index=True)


    feature_cols = [col for col in df_features.columns if col not in

                    ['producto', 'fecha', 'cantidad_vendida', 'venta_bs',

                     'num_transacciones', 'periodo', 'venta_ocurrio',

                     'subclase_kmeans', 'grupo_venta', 'rango_venta',

                     'fecha_ultima_compra', 'precio_implicito']]


    df_features = df_features.replace([np.inf, -np.inf], np.nan)

    df_features = df_features.dropna(subset=feature_cols)

    df_features = df_features.fillna(0)


    print(f"    > ✅ {len(df_features):,} filas | {len(feature_cols)} features")

    print(f"    > 📊 Distribución binaria: {df_features['venta_ocurrio'].value_counts().to_dict()}")


    return df_features, feature_cols, limites_rangos


# ============================================================================

# ENTRENAMIENTO DEL MODELO DOBLE-CLASIFICADOR (CORREGIDO)

# ============================================================================


def entrenar_modelo_doble_clasificador(X_train, y_train_cls, y_train_rango,

                                        X_test, y_test_cls, y_test_rango,

                                        hparams_cls1, hparams_cls2,

                                        umbral_prob=UMBRAL_PROB_DEFAULT):

    """

    Entrena el modelo doble-clasificador:

    ETAPA 1: Clasificador Binario (Venta/No Venta)

    ETAPA 2: Clasificador de Rangos (Baja/Alta) - CORREGIDO

    """


    # ========== ETAPA 1: CLASIFICADOR BINARIO ==========

    clases_unicas_train = np.unique(y_train_cls)

    n_clases = len(clases_unicas_train)


    print(f"\n    📊 ETAPA 1: Entrenando Clasificador Binario...")

    print(f"    > Clases en train: {clases_unicas_train} (n={n_clases})")


    if n_clases == 1:

        clase_dominante = clases_unicas_train[0]

        print(f"    > ⚠️ Solo hay clase {clase_dominante} en train")


        if clase_dominante == 0:

            y_pred_cls = np.zeros(len(X_test), dtype=int)

            y_pred_cls_proba = np.zeros(len(X_test))

            clasificador_binario = None

        else:

            y_pred_cls = np.ones(len(X_test), dtype=int)

            y_pred_cls_proba = np.ones(len(X_test))

            clasificador_binario = None


        accuracy_cls1 = accuracy_score(y_test_cls, y_pred_cls)

        precision_cls1 = precision_score(y_test_cls, y_pred_cls, zero_division=1)

        recall_cls1 = recall_score(y_test_cls, y_pred_cls, zero_division=1)

        f1_cls1 = f1_score(y_test_cls, y_pred_cls, zero_division=1)

        auc_cls1 = 1.0 if clase_dominante == 1 else 0.0

    else:

        clasificador_binario = RandomForestClassifier(**hparams_cls1)

        clasificador_binario.fit(X_train, y_train_cls)


        proba_array = clasificador_binario.predict_proba(X_test)


        if proba_array.shape[1] == 2:

            y_pred_cls_proba = proba_array[:, 1]

        else:

            y_pred_cls_proba = proba_array[:, 0]


        y_pred_cls = (y_pred_cls_proba >= umbral_prob).astype(int)


        accuracy_cls1 = accuracy_score(y_test_cls, y_pred_cls)

        precision_cls1 = precision_score(y_test_cls, y_pred_cls, zero_division=0)

        recall_cls1 = recall_score(y_test_cls, y_pred_cls, zero_division=0)

        f1_cls1 = f1_score(y_test_cls, y_pred_cls, zero_division=0)


        try:

            auc_cls1 = roc_auc_score(y_test_cls, y_pred_cls_proba)

        except:

            auc_cls1 = 0.0


    print(f"    > Accuracy: {accuracy_cls1:.3f}")

    print(f"    > Precision: {precision_cls1:.3f}")

    print(f"    > Recall: {recall_cls1:.3f}")

    print(f"    > F1-Score: {f1_cls1:.3f}")

    print(f"    > AUC-ROC: {auc_cls1:.3f}")


    # ========== ETAPA 2: CLASIFICADOR DE RANGOS (CORREGIDO) ==========

    print("\n    📊 ETAPA 2: Entrenando Clasificador de Rangos...")


    mask_train_venta = y_train_cls == 1

    X_train_rangos = X_train[mask_train_venta]

    y_train_rangos_filtrado = y_train_rango[mask_train_venta]


    clasificador_rangos = None

    reporte_cls2 = None

    auc_cls2 = 0.0

    y_pred_rangos_proba_all = None


    clases_rangos_train = np.unique(y_train_rangos_filtrado)


    if len(X_train_rangos) < 30:

        print(f"    > ⚠️ Datos insuficientes para rangos ({len(X_train_rangos)} < 30)")

    elif len(clases_rangos_train) < 2:

        print(f"    > ⚠️ Solo hay {len(clases_rangos_train)} clase(s) de rangos en train")

    else:

        print(f"    > Clases de rangos en train: {clases_rangos_train}")


        clasificador_rangos = RandomForestClassifier(**hparams_cls2)

        clasificador_rangos.fit(X_train_rangos, y_train_rangos_filtrado)


        print(f"    > ✅ Clasificador de rangos entrenado")


        mask_test_venta = y_test_cls == 1


        if mask_test_venta.sum() > 5:

            y_test_rangos_filtrado = y_test_rango[mask_test_venta]

            X_test_rangos = X_test[mask_test_venta]


            y_pred_rangos = clasificador_rangos.predict(X_test_rangos)

            y_pred_rangos_proba = clasificador_rangos.predict_proba(X_test_rangos)


            # --- CORRECCIÓN 1: Classification Report (labels y targets) ---

            try:

                reporte_cls2 = classification_report(

                    y_test_rangos_filtrado,

                    y_pred_rangos,

                    labels=[0, 1],

                    target_names=['Baja', 'Alta'],

                    zero_division=0

                )

                print(f"\n    📊 Reporte Clasificador de Rangos:")

                print(reporte_cls2)

            except:

                reporte_cls2 = "No se pudo generar reporte"


            # --- CORRECCIÓN 2: AUC (ahora es binario) ---

            try:

                if len(np.unique(y_test_rangos_filtrado)) > 1:

                    # Usar solo la prob de la clase 1, no multi_class

                    auc_cls2 = roc_auc_score(

                        y_test_rangos_filtrado,

                        y_pred_rangos_proba[:, 1]

                    )

                    print(f"    > AUC-ROC (Binario): {auc_cls2:.3f}")

                else:

                     print(f"    > ⚠️ Solo 1 clase en test, no se puede calcular AUC.")

            except Exception as e:

                print(f"    > ⚠️ No se pudo calcular AUC: {e}")


            # --- CORRECCIÓN 3: np.full (shape de 3 a 2) ---

            y_pred_rangos_proba_all = np.full((len(X_test), 2), np.nan)

            y_pred_rangos_proba_all[mask_test_venta] = y_pred_rangos_proba

        else:

            print(f"    > ⚠️ No hay suficientes ventas en test para evaluar rangos")


    resultado = {

        'clasificador_binario': clasificador_binario,

        'clasificador_rangos': clasificador_rangos,

        'y_pred_cls': y_pred_cls,

        'y_pred_cls_proba': y_pred_cls_proba,

        'y_pred_rangos_proba': y_pred_rangos_proba_all,

        'accuracy_cls1': accuracy_cls1,

        'precision_cls1': precision_cls1,

        'recall_cls1': recall_cls1,

        'f1_cls1': f1_cls1,

        'auc_cls1': auc_cls1,

        'reporte_cls2': reporte_cls2,

        'auc_cls2': auc_cls2,

        'umbral_prob': umbral_prob,

        'n_clases_train': n_clases

    }


    return resultado


# ============================================================================

# VISUALIZACIONES (CORREGIDO)

# ============================================================================


def generar_visualizaciones_doble_clasificador(resultado, y_test_cls, y_test_rango, X_test_scaled, limites_rangos, prefijo_segmento=""):

    """Visualizaciones para modelo doble-clasificador (2 Rangos)"""


    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

    fig.suptitle(f'Modelo Doble-Clasificador (2 Rangos) - {prefijo_segmento}\n'

                 f'Clasificador 1: F1={resultado["f1_cls1"]:.3f} | '

                 f'Clasificador 2: AUC={resultado["auc_cls2"]:.3f}',

                 fontsize=16, weight='bold')


    # 1. Confusion Matrix (Binario)

    ax1 = axes[0, 0]

    cm = confusion_matrix(y_test_cls, resultado['y_pred_cls'])

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1,

                xticklabels=['No Venta', 'Venta'],

                yticklabels=['No Venta', 'Venta'])

    ax1.set_xlabel('Predicho')

    ax1.set_ylabel('Real')

    ax1.set_title(f'Matriz Confusión (Binario)\nAccuracy={resultado["accuracy_cls1"]:.3f}')


    # 2. ROC Curve (Binario)

    ax2 = axes[0, 1]

    try:

        fpr, tpr, _ = roc_curve(y_test_cls, resultado['y_pred_cls_proba'])

        ax2.plot(fpr, tpr, linewidth=2, label=f'AUC={resultado["auc_cls1"]:.3f}')

        ax2.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')

        ax2.set_xlabel('False Positive Rate')

        ax2.set_ylabel('True Positive Rate')

        ax2.set_title('Curva ROC (Clasificador Binario)')

        ax2.legend()

        ax2.grid(True, alpha=0.3)

    except:

        ax2.text(0.5, 0.5, 'ROC no disponible', ha='center', va='center')


    # 3. Distribución de Probabilidades (Binario)

    ax3 = axes[0, 2]

    ax3.hist(resultado['y_pred_cls_proba'][y_test_cls == 0],

             bins=20, alpha=0.5, label='No Venta (real)', color='red')

    ax3.hist(resultado['y_pred_cls_proba'][y_test_cls == 1],

             bins=20, alpha=0.5, label='Venta (real)', color='green')

    ax3.axvline(resultado['umbral_prob'], color='black', linestyle='--',

                linewidth=2, label=f'Umbral={resultado["umbral_prob"]}')

    ax3.set_xlabel('Probabilidad Predicha')

    ax3.set_ylabel('Frecuencia')

    ax3.set_title('Distribución de Probabilidades (Binario)')

    ax3.legend()

    ax3.grid(True, alpha=0.3)


    # 4. Confusion Matrix (Rangos) - CORREGIDO

    ax4 = axes[1, 0]

    if resultado['clasificador_rangos'] is not None:

        mask_test_venta = y_test_cls == 1

        if mask_test_venta.sum() > 0:

            y_test_rangos_filtrado = y_test_rango[mask_test_venta]

            X_test_venta = X_test_scaled[mask_test_venta]


            try:

                y_pred_rangos_filtrado = resultado['clasificador_rangos'].predict(X_test_venta)


                cm_rangos = confusion_matrix(y_test_rangos_filtrado,

                                             y_pred_rangos_filtrado,

                                             labels=[0, 1]) # <-- CORREGIDO

                sns.heatmap(cm_rangos, annot=True, fmt='d', cmap='Greens', ax=ax4,

                            xticklabels=['Baja', 'Alta'], # <-- CORREGIDO

                            yticklabels=['Baja', 'Alta']) # <-- CORREGIDO

                ax4.set_xlabel('Predicho')

                ax4.set_ylabel('Real')

                ax4.set_title('Matriz Confusión (Rangos)')

            except Exception as e:

                ax4.text(0.5, 0.5, f'Error en matriz: {str(e)[:50]}',

                         ha='center', va='center', fontsize=10)

        else:

            ax4.text(0.5, 0.5, 'No hay ventas en test', ha='center', va='center')

    else:

        ax4.text(0.5, 0.5, 'Clasificador de rangos no entrenado', ha='center', va='center')


    # 5. Distribución de Rangos Reales - CORREGIDO

    ax5 = axes[1, 1]

    if limites_rangos is not None:

        mask_venta = y_test_rango >= 0

        if mask_venta.sum() > 0:

            y_test_rango_filtrado = y_test_rango[mask_venta]

            ax5.hist(y_test_rango_filtrado, bins=[-0.5, 0.5, 1.5], alpha=0.7, edgecolor='black', color='steelblue') # <-- CORREGIDO

            ax5.set_xticks([0, 1]) # <-- CORREGIDO

            ax5.set_xticklabels(['Baja', 'Alta']) # <-- CORREGIDO

            ax5.set_ylabel('Frecuencia')

            ax5.set_title(f'Distribución de Rangos Reales\nLímite: {limites_rangos["q_50"]:.1f}') # <-- CORREGIDO

            ax5.grid(axis='y', alpha=0.3)

        else:

            ax5.text(0.5, 0.5, 'No hay datos de rangos', ha='center', va='center')

    else:

        ax5.text(0.5, 0.5, 'Límites de rangos no definidos', ha='center', va='center')


    # 6. Métricas del Modelo

    ax6 = axes[1, 2]

    metricas = {

        'Accuracy\n(Binario)': resultado['accuracy_cls1'],

        'F1-Score\n(Binario)': resultado['f1_cls1'],

        'AUC\n(Binario)': resultado['auc_cls1'],

        'AUC\n(Rangos)': resultado['auc_cls2']

    }

    colors = ['green' if v > 0.6 else 'orange' if v > 0.4 else 'red' for v in metricas.values()]

    bars = ax6.bar(range(len(metricas)), metricas.values(), color=colors, alpha=0.7, edgecolor='black')

    ax6.set_xticks(range(len(metricas)))

    ax6.set_xticklabels(metricas.keys(), rotation=15, ha='right')

    ax6.set_ylabel('Score')

    ax6.set_title('Panel de Métricas')

    ax6.set_ylim([0, 1])

    ax6.grid(axis='y', alpha=0.3)


    for bar, valor in zip(bars, metricas.values()):

        ax6.text(bar.get_x() + bar.get_width()/2, valor, f'{valor:.2f}',

                 ha='center', va='bottom', fontsize=9, weight='bold')


    plt.tight_layout(rect=[0, 0.03, 1, 0.96])


    nombre_archivo = f'10_5_doble_clasif_{prefijo_segmento}'.replace('.', '_').replace(' ', '_').replace('(', '').replace(')', '')

    plt.savefig(f'{nombre_archivo}.png', dpi=150, bbox_inches='tight')

    print(f"    > ✅ Gráfico: {nombre_archivo}.png")

    plt.close()


# ============================================================================

# BUCLE PRINCIPAL

# ============================================================================


modelos_doble_clasif_segmentados = {}

scalers_doble_clasif_segmentados = {}

resultados_doble_clasif_segmentados = {}

features_doble_clasif_segmentados = {}

limites_rangos_segmentados = {}


subclases_unicas = series_completas_con_kmeans['subclase_kmeans'].unique()


print(f"\n{'='*80}")

print(f"🚀 MODELADO DOBLE-CLASIFICADOR")

print(f"{'='*80}\n")


for subclase in subclases_unicas:

    subclase_str = str(subclase)

    print("\n" + "="*80)

    print(f"🎯 SEGMENTO: '{subclase_str}'")

    print("="*80)


    if any(excluir in subclase_str for excluir in CLUSTERS_A_EXCLUIR):

        print(f"    > ⚠️ EXCLUIDO")

        continue


    df_segmento = series_completas_con_kmeans[

        series_completas_con_kmeans['subclase_kmeans'] == subclase

    ].copy()


    print(f"    > {len(df_segmento):,} filas totales")


    # PASO 1: PREPARACIÓN

    print("\n📋 PASO 1: Preparación de datos...")

    df_features, feature_cols, limites_rangos = preparar_datos_doble_clasificador(df_segmento)


    if len(df_features) < UMBRAL_MINIMO_DATOS:

        print(f"    > ❌ INSUFICIENTE (<{UMBRAL_MINIMO_DATOS})")

        continue


    if limites_rangos is None:

        print(f"    > ❌ No se pudieron calcular límites de rangos")

        continue


    # PASO 2: SPLIT TEMPORAL

    print("\n📋 PASO 2: Split temporal...")

    fechas_unicas = sorted(df_features['fecha'].unique())

    split_idx = int(len(fechas_unicas) * (1 - TEST_SIZE_FRAC))

    fecha_split = fechas_unicas[split_idx]


    mask_train = df_features['fecha'] < fecha_split

    mask_test = df_features['fecha'] >= fecha_split


    X = df_features[feature_cols].values

    y_cls = df_features['venta_ocurrio'].values

    y_rango = df_features['rango_venta'].values


    X_train = X[mask_train]

    X_test = X[mask_test]

    y_train_cls = y_cls[mask_train]

    y_test_cls = y_cls[mask_test]

    y_train_rango = y_rango[mask_train]

    y_test_rango = y_rango[mask_test]


    print(f"    > Fecha split: {pd.to_datetime(fecha_split).strftime('%Y-%m')}")

    print(f"    > Train: {len(X_train):,} muestras")

    print(f"    > Test: {len(X_test):,} muestras")


    if len(X_test) < 10:

        print(f"    > ⚠️ Test muy pequeño. OMITIENDO.")

        continue


    # ESCALADO

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)


    # PASO 3: ENTRENAMIENTO

    print("\n📋 PASO 3: Entrenamiento del modelo doble-clasificador...")

    resultado = entrenar_modelo_doble_clasificador(

        X_train_scaled, y_train_cls, y_train_rango,

        X_test_scaled, y_test_cls, y_test_rango,

        HPARAMS_CLASIFICADOR_BINARIO, HPARAMS_CLASIFICADOR_RANGOS

    )


    # PASO 4: VISUALIZACIÓN

    print("\n📋 PASO 4: Visualización...")

    generar_visualizaciones_doble_clasificador(resultado, y_test_cls, y_test_rango, X_test_scaled, limites_rangos, prefijo_segmento=subclase_str)


    # PASO 5: GUARDAR

    modelos_doble_clasif_segmentados[subclase_str] = {

        'clasificador_binario': resultado['clasificador_binario'],

        'clasificador_rangos': resultado['clasificador_rangos']

    }

    scalers_doble_clasif_segmentados[subclase_str] = scaler

    features_doble_clasif_segmentados[subclase_str] = feature_cols

    limites_rangos_segmentados[subclase_str] = limites_rangos


    resultados_doble_clasif_segmentados[subclase_str] = {

        'metricas': {k: v for k, v in resultado.items()

                     if k not in ['clasificador_binario', 'clasificador_rangos',

                                   'y_pred_cls', 'y_pred_cls_proba', 'y_pred_rangos_proba']},

        'n_train': len(X_train),

        'n_test': len(X_test),

        'proporcion_ventas_train': (y_train_cls == 1).mean(),

        'proporcion_ventas_test': (y_test_cls == 1).mean(),

        'limites_rangos': limites_rangos

    }


    print(f"    > ✅ Resultados guardados")


# ============================================================================

# REPORTE FINAL

# ============================================================================

print("\n" + "="*80)

print("📊 REPORTE FINAL - MODELO DOBLE-CLASIFICADOR")

print("="*80)


if not resultados_doble_clasif_segmentados:

    print("❌ No se entrenó ningún modelo")

else:

    # Crear directorio

    dir_doble_clasif = os.path.join(BASE_EXPORT_DIR, 'doble_clasificador')

    if not os.path.exists(dir_doble_clasif):

        os.makedirs(dir_doble_clasif)


    # Tabla de resumen

    resumen_data = []

    for subclase, data in resultados_doble_clasif_segmentados.items():

        metricas = data['metricas']

        limites = data['limites_rangos']

        resumen_data.append({

            'Sub-Clase': subclase,

            'Accuracy': metricas['accuracy_cls1'],

            'F1-Score': metricas['f1_cls1'],

            'AUC (Binario)': metricas['auc_cls1'],

            'AUC (Rangos)': metricas['auc_cls2'],

            'Límite Mediana': limites['q_50'],

            'N Train': data['n_train']

        })


    df_resumen = pd.DataFrame(resumen_data).sort_values('F1-Score', ascending=False)


    print("\n" + "="*80)

    print("📈 RESUMEN DE RENDIMIENTO")

    print("="*80)

    print(df_resumen.to_string(index=False))


    # Estadísticas

    f1_medio = df_resumen['F1-Score'].mean()

    auc_rangos_medio = df_resumen['AUC (Rangos)'].mean()


    print(f"\n📊 F1-Score Promedio (Clasificador Binario): {f1_medio:.3f}")

    print(f"📊 AUC Promedio (Clasificador Rangos): {auc_rangos_medio:.3f}")


    # Exportar

    joblib.dump(modelos_doble_clasif_segmentados, os.path.join(dir_doble_clasif, 'modelos_doble_clasif.pkl'))

    joblib.dump(scalers_doble_clasif_segmentados, os.path.join(dir_doble_clasif, 'scalers_doble_clasif.pkl'))

    joblib.dump(features_doble_clasif_segmentados, os.path.join(dir_doble_clasif, 'features_doble_clasif.pkl'))

    joblib.dump(limites_rangos_segmentados, os.path.join(dir_doble_clasif, 'limites_rangos.pkl'))


    with open(os.path.join(dir_doble_clasif, 'metricas_doble_clasif.json'), 'w') as f:

        json.dump(resultados_doble_clasif_segmentados, f, indent=4, default=str)


    df_resumen.to_csv(os.path.join(dir_doble_clasif, 'resumen_doble_clasif.csv'), index=False)


    print(f"\n✅ Artefactos exportados a '{dir_doble_clasif}/'")


print("\n" + "="*80)

print("✅ CELDA 10.5 COMPLETADA")

print("="*80)

print("\n📦 Variables creadas:")

print("    • modelos_doble_clasif_segmentados")

print("    • scalers_doble_clasif_segmentados")

print("    • features_doble_clasif_segmentados")

print("    • limites_rangos_segmentados")

print("    • resultados_doble_clasif_segmentados")

print("\n💡 VENTAJAS DEL MODELO (2 RANGOS):")

print("    • Problema más simple y más fácil de predecir.")

print("    • La predicción ahora es P(Venta) -> P(Baja) o P(Alta)")

print("\n🎯 SIGUIENTE: Celda 10.7 (Optimización de Umbral para Clasificador Binario)")


## CELDA 10.6 Optimiza


### CELDA 10.6 V2



# ============================================================================

# 🎯 CELDA 10.6: OPTIMIZACIÓN DE UMBRAL (PARA DOBLE-CLASIFICADOR)

#

# OBJETIVO: Encontrar el umbral óptimo (P(Venta)) para el Clasificador 1 (Binario)

#           maximizando el F1-Score.

#

# NOTA: Se elimina toda la lógica del regresor, ya no se usa.

# ============================================================================


import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

import joblib

import os

import json

import warnings

warnings.filterwarnings('ignore')


from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (

    accuracy_score, precision_score, recall_score, f1_score

)


# --- Configuración ---

try:

    # --- VERIFICACIÓN DE VARIABLES DE CELDAS ANTERIORES ---

    # Necesitamos las funciones y HPs de la Celda 10.5

    _ = preparar_datos_doble_clasificador

    _ = HPARAMS_CLASIFICADOR_BINARIO

    _ = series_completas_con_kmeans


    RANDOM_STATE = locals().get('RANDOM_STATE', 42)

    TEST_SIZE_FRAC = locals().get('TEST_SIZE_FRAC', 0.2)

    BASE_EXPORT_DIR = locals().get('BASE_EXPORT_DIR', 'modelos_exportados')


except NameError as e:

    print(f"❌ ERROR: {e}")

    raise NameError("Parece que no has ejecutado la Celda 10.5 (Doble-Clasificador) antes.")


print("="*80)

print("🎯 CELDA 10.6: OPTIMIZACIÓN DE UMBRAL (Clasificador Binario)")

print("="*80)


# ============================================================================

# CONFIGURACIÓN

# ============================================================================

UMBRAL_MINIMO_DATOS = 80

UMBRALES_A_PROBAR = np.linspace(0.1, 0.95, 18)  # 18 umbrales

METRICA_OPTIMIZAR = 'f1_score' # 'f1_score', 'accuracy', 'precision', 'recall'

CLUSTERS_A_EXCLUIR = ['4. Anomalia (Excluir)', 'Anomalía', 'Anomalia', 'A.2 (Valor Medio)']


print(f"\n⚙️ CONFIGURACIÓN:")

print(f"    • Umbrales a probar: {len(UMBRALES_A_PROBAR)}")

print(f"    • Rango: {UMBRALES_A_PROBAR.min():.2f} - {UMBRALES_A_PROBAR.max():.2f}")

print(f"    • Métrica a optimizar: {METRICA_OPTIMIZAR}")


# ============================================================================

# FUNCIÓN DE OPTIMIZACIÓN DE UMBRAL (SIMPLIFICADA)

# ============================================================================


def optimizar_umbral_binario(clasificador, X_test, y_test_cls,

                             umbrales, metrica_objetivo='f1_score'):

    """

    Optimiza el umbral de probabilidad para el clasificador binario.

    """


    print(f"    🔍 Optimizando umbral (métrica: {metrica_objetivo})...")

    print(f"    > Probando {len(umbrales)} umbrales...")


    resultados = []


    # ===== OBTENER PROBABILIDADES (MANEJO ROBUSTO) =====

    if clasificador is None:

        # Caso: No hay clasificador (solo 1 clase en train, ej. A.3)

        print(f"    > ⚠️ No hay clasificador entrenado (solo 1 clase en train)")

        print(f"    > Saltando optimización (umbral no aplicable)")


        # Retornar resultados dummy

        for umbral in umbrales:

            resultados.append({

                'umbral': umbral,

                'accuracy': 1.0, 'precision': 1.0,

                'recall': 1.0, 'f1_score': 1.0,

            })


        df_resultados = pd.DataFrame(resultados)

        umbral_optimo = 0.5  # Valor por defecto


        print(f"    > ℹ️ Umbral por defecto: {umbral_optimo} (no optimizable)")


        return df_resultados, umbral_optimo


    # ===== CASO NORMAL: Clasificador entrenado =====

    proba_array = clasificador.predict_proba(X_test)


    if proba_array.shape[1] == 2:

        y_pred_proba = proba_array[:, 1]

    elif proba_array.shape[1] == 1:

        y_pred_proba = proba_array[:, 0]

        print(f"    > ⚠️ predict_proba retornó 1 columna")

    else:

        raise ValueError(f"predict_proba tiene shape inesperado: {proba_array.shape}")


    # ===== PROBAR CADA UMBRAL =====

    for umbral in umbrales:

        y_pred_cls = (y_pred_proba >= umbral).astype(int)


        # Métricas de clasificación

        accuracy = accuracy_score(y_test_cls, y_pred_cls)

        precision = precision_score(y_test_cls, y_pred_cls, zero_division=0)

        recall = recall_score(y_test_cls, y_pred_cls, zero_division=0)

        f1 = f1_score(y_test_cls, y_pred_cls, zero_division=0)


        resultados.append({

            'umbral': umbral,

            'accuracy': accuracy,

            'precision': precision,

            'recall': recall,

            'f1_score': f1,

        })


    df_resultados = pd.DataFrame(resultados)


    # Encontrar umbral óptimo

    idx_optimo = df_resultados[metrica_objetivo].idxmax()

    umbral_optimo = df_resultados.loc[idx_optimo, 'umbral']


    print(f"    ✅ Umbral óptimo encontrado: {umbral_optimo:.2f}")

    print(f"    > Métricas con umbral óptimo:")

    print(f"       • Accuracy: {df_resultados.loc[idx_optimo, 'accuracy']:.3f}")

    print(f"       • Precision: {df_resultados.loc[idx_optimo, 'precision']:.3f}")

    print(f"       • Recall: {df_resultados.loc[idx_optimo, 'recall']:.3f}")

    print(f"       • F1-Score: {df_resultados.loc[idx_optimo, 'f1_score']:.3f}")


    return df_resultados, umbral_optimo


# ============================================================================

# VISUALIZACIÓN (SIMPLIFICADA)

# ============================================================================


def generar_visualizacion_optimizacion_binaria(df_resultados, umbral_optimo, prefijo_segmento=""):

    """Genera gráficos de la optimización de umbral (solo clasificador)"""


    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    fig.suptitle(f'Optimización de Umbral (Binario) - {prefijo_segmento}\n'

                 f'Umbral Óptimo: {umbral_optimo:.2f}',

                 fontsize=16, weight='bold')


    # 1. Métricas de Clasificación vs Umbral

    ax1 = axes[0]

    ax1.plot(df_resultados['umbral'], df_resultados['accuracy'], 'o-', label='Accuracy', markersize=5)

    ax1.plot(df_resultados['umbral'], df_resultados['precision'], 's-', label='Precision', markersize=5)

    ax1.plot(df_resultados['umbral'], df_resultados['recall'], '^-', label='Recall', markersize=5)

    ax1.plot(df_resultados['umbral'], df_resultados['f1_score'], 'd-', label='F1-Score', linewidth=3)

    ax1.axvline(umbral_optimo, color='red', linestyle='--', linewidth=2, label=f'Óptimo ({umbral_optimo:.2f})')

    ax1.set_xlabel('Umbral de Probabilidad')

    ax1.set_ylabel('Score')

    ax1.set_title('Métricas de Clasificación vs Umbral')

    ax1.legend()

    ax1.grid(True, alpha=0.3)

    ax1.set_ylim([0, 1.05])


    # 2. Trade-off Precision-Recall

    ax2 = axes[1]

    scatter = ax2.scatter(df_resultados['recall'], df_resultados['precision'],

                          c=df_resultados['umbral'], cmap='viridis', s=100,

                          edgecolors='black', linewidth=0.5)


    # Marcar umbral óptimo

    idx_optimo = df_resultados[METRICA_OPTIMIZAR].idxmax()

    ax2.scatter([df_resultados.loc[idx_optimo, 'recall']],

                [df_resultados.loc[idx_optimo, 'precision']],

                color='red', s=300, marker='*', zorder=5,

                edgecolors='black', linewidth=2, label=f'Óptimo ({umbral_optimo:.2f})')


    ax2.set_xlabel('Recall')

    ax2.set_ylabel('Precision')

    ax2.set_title('Trade-off Precision-Recall')

    ax2.legend()

    ax2.grid(True, alpha=0.3)


    cbar = plt.colorbar(scatter, ax=ax2)

    cbar.set_label('Umbral')


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


    nombre_archivo = f'10_6_optimizacion_umbral_{prefijo_segmento}'.replace('.', '_').replace(' ', '_').replace('(', '').replace(')', '')

    plt.savefig(f'{nombre_archivo}.png', dpi=150, bbox_inches='tight')

    print(f"    > ✅ Gráfico: {nombre_archivo}.png")

    plt.close()


# ============================================================================

# BUCLE PRINCIPAL

# ============================================================================


umbrales_optimizados = {}

resultados_optimizacion = {}


print(f"\n{'='*80}")

print(f"🚀 OPTIMIZACIÓN DE UMBRALES POR SEGMENTO")

print(f"{'='*80}\n")


for subclase in series_completas_con_kmeans['subclase_kmeans'].unique():

    subclase_str = str(subclase)

    print("\n" + "="*80)

    print(f"🎯 SEGMENTO: '{subclase_str}'")

    print("="*80)


    if any(excluir in subclase_str for excluir in CLUSTERS_A_EXCLUIR):

        print(f"    > ⚠️ EXCLUIDO")

        continue


    df_segmento = series_completas_con_kmeans[

        series_completas_con_kmeans['subclase_kmeans'] == subclase

    ].copy()


    print(f"    > {len(df_segmento):,} filas totales")


    # PASO 1: PREPARACIÓN

    print("\n📋 PASO 1: Preparación de datos...")

    # Usar la función de preparación de la Celda 10.5 (Doble-Clasificador)

    df_features, feature_cols, _ = preparar_datos_doble_clasificador(df_segmento)


    if len(df_features) < UMBRAL_MINIMO_DATOS:

        print(f"    > ❌ INSUFICIENTE (<{UMBRAL_MINIMO_DATOS})")

        continue


    # PASO 2: SPLIT TEMPORAL

    print("\n📋 PASO 2: Split temporal...")

    fechas_unicas = sorted(df_features['fecha'].unique())

    split_idx = int(len(fechas_unicas) * (1 - TEST_SIZE_FRAC))

    fecha_split = fechas_unicas[split_idx]


    mask_train = df_features['fecha'] < fecha_split

    mask_test = df_features['fecha'] >= fecha_split


    X = df_features[feature_cols].values

    y_cls = df_features['venta_ocurrio'].values


    X_train = X[mask_train]

    X_test = X[mask_test]

    y_train_cls = y_cls[mask_train]

    y_test_cls = y_cls[mask_test]


    print(f"    > Train: {len(X_train):,} | Test: {len(X_test):,}")


    if len(X_test) < 10:

        print(f"    > ⚠️ Test muy pequeño. OMITIENDO.")

        continue


    # ESCALADO

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)


    # PASO 3: ENTRENAR CLASIFICADOR BINARIO

    print("\n📋 PASO 3: Entrenando clasificador binario base...")


    clases_unicas = np.unique(y_train_cls)


    if len(clases_unicas) == 1:

        print(f"    > ⚠️ Solo hay clase {clases_unicas[0]} en train")

        clasificador = None

    else:

        # Usar los HPs de la Celda 10.5

        clasificador = RandomForestClassifier(**HPARAMS_CLASIFICADOR_BINARIO)

        clasificador.fit(X_train_scaled, y_train_cls)

        print(f"    > ✅ Clasificador entrenado")


    # PASO 4: OPTIMIZAR UMBRAL

    print("\n📋 PASO 4: Optimización de umbral...")

    df_resultados_umbral, umbral_optimo = optimizar_umbral_binario(

        clasificador, X_test_scaled, y_test_cls,

        UMBRALES_A_PROBAR, metrica_objetivo=METRICA_OPTIMIZAR

    )


    # PASO 5: VISUALIZACIÓN

    print("\n📋 PASO 5: Visualización...")

    generar_visualizacion_optimizacion_binaria(df_resultados_umbral, umbral_optimo, prefijo_segmento=subclase_str)


    # GUARDAR

    umbrales_optimizados[subclase_str] = umbral_optimo

    resultados_optimizacion[subclase_str] = df_resultados_umbral.to_dict('records')


    print(f"    > ✅ Resultados guardados")


# ============================================================================

# REPORTE FINAL

# ============================================================================

print("\n" + "="*80)

print("📊 REPORTE FINAL - OPTIMIZACIÓN DE UMBRALES")

print("="*80)


if umbrales_optimizados:

    print(f"\n✅ Umbrales optimizados para {len(umbrales_optimizados)} segmentos:\n")


    for segmento, umbral in umbrales_optimizados.items():

        print(f"       • {segmento}: {umbral:.2f}")


    # Exportar

    dir_optimizacion = os.path.join(BASE_EXPORT_DIR, 'optimizacion_umbral')

    if not os.path.exists(dir_optimizacion):

        os.makedirs(dir_optimizacion)


    with open(os.path.join(dir_optimizacion, 'umbrales_optimizados.json'), 'w') as f:

        json.dump(umbrales_optimizados, f, indent=4)


    with open(os.path.join(dir_optimizacion, 'resultados_optimizacion.json'), 'w') as f:

        json.dump(resultados_optimizacion, f, indent=4, default=str)


    print(f"\n✅ Resultados exportados a '{dir_optimizacion}/'")

else:

    print("\n⚠️ No se optimizaron umbrales para ningún segmento")


print("\n" + "="*80)

print("✅ CELDA 10.6 COMPLETADA")

print("="*80)

print("\n📦 Variables creadas:")

print("    • umbrales_optimizados (dict con umbral óptimo por segmento)")

print("    • resultados_optimizacion (dict con curvas completas)")

print("\n💡 SIGUIENTE: Celda 10.7 (Validación Cruzada Temporal)")


## CELDA 10.7 Valida



### CELDA 10.7 V2


# ============================================================================

# 🔍 CELDA 10.7: VALIDACIÓN CON EXPANDING WINDOW (PARA DOBLE-CLASIFICADOR)

#

# OBJETIVO: Validar la estabilidad temporal del nuevo modelo doble-clasificador.

# ============================================================================


import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

import joblib

import os

import json

import warnings

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import f1_score, roc_auc_score, classification_report

from sklearn.model_selection import BaseCrossValidator

from pandas.tseries.offsets import DateOffset


warnings.filterwarnings('ignore')


# ============================================================================

# CLASE REQUERIDA: ExpandingWindowSplitter (Simplificada y corregida)

# ============================================================================


class ExpandingWindowSplitter(BaseCrossValidator):

    """

    Validador cruzado temporal de ventana expandible.

    Genera splits donde 'train' crece y 'test' es un bloque fijo.

    Devuelve los LABELS (índice) de las filas para train/test.

    """

    def __init__(self, time_col, n_splits=5, min_train_months=12, test_months=3):

        self.time_col = time_col

        self.n_splits = n_splits

        self.min_train_months = min_train_months

        self.test_months = test_months


    def split(self, X, y=None, groups=None):

        # X es df_features

        df = X.copy()

        df[self.time_col] = pd.to_datetime(df[self.time_col])

        df = df.sort_values(self.time_col)


        unique_months = df[self.time_col].dt.to_period('M').unique()

        unique_months = sorted(unique_months) # Corregido


        if len(unique_months) < self.min_train_months + self.test_months:

            raise ValueError(

                f"Datos insuficientes. Se necesitan {self.min_train_months + self.test_months} "

                f"meses únicos, pero solo hay {len(unique_months)}"

            )


        for i in range(self.n_splits):

            train_end_idx = self.min_train_months + (i * self.test_months) - 1

            test_end_idx = train_end_idx + self.test_months


            if test_end_idx >= len(unique_months):

                break


            train_end_month = unique_months[train_end_idx]

            test_end_month = unique_months[test_end_idx]


            train_mask = (df[self.time_col].dt.to_period('M') <= train_end_month)

            test_mask = (df[self.time_col].dt.to_period('M') > train_end_month) & \

                          (df[self.time_col].dt.to_period('M') <= test_end_month)


            # Devolver los LABELS (el .index) de las filas que coinciden

            train_indices = df[train_mask].index.to_list()

            test_indices = df[test_mask].index.to_list()


            if len(test_indices) == 0 or len(train_indices) == 0:

                continue


            yield train_indices, test_indices


    def get_n_splits(self, X=None, y=None, groups=None):

        return self.n_splits



print("="*80)

print("🔍 CELDA 10.7: VALIDACIÓN CON EXPANDING WINDOW (DOBLE-CLASIFICADOR)")

print("="*80)


# ============================================================================

# VERIFICACIÓN DE VARIABLES EN MEMORIA

# ============================================================================

print("Verificando funciones y variables de celdas anteriores...")

try:

    _ = preparar_datos_doble_clasificador

    _ = entrenar_modelo_doble_clasificador

    _ = HPARAMS_CLASIFICADOR_BINARIO

    _ = HPARAMS_CLASIFICADOR_RANGOS

    _ = UMBRAL_MINIMO_DATOS

    _ = CLUSTERS_A_EXCLUIR

    _ = series_completas_con_kmeans


    RANDOM_STATE = locals().get('RANDOM_STATE', 42)

    BASE_EXPORT_DIR = locals().get('BASE_EXPORT_DIR', 'modelos_exportados')

    UMBRAL_PROB_DEFAULT = locals().get('UMBRAL_PROB_DEFAULT', 0.5)


    print("✅ Funciones y variables cargadas.")

except NameError as e:

    print(f"❌ ERROR: {e}")

    raise NameError("Parece que no has ejecutado la Celda 10.5 antes. Por favor, ejecútala y vuelve a intentarlo.")


# ============================================================================

# CONFIGURACIÓN DE VALIDACIÓN

# ============================================================================

N_FOLDS = 5

MIN_TRAIN_MONTHS = 12

TEST_MONTHS = 3


print(f"\n⚙️ CONFIGURACIÓN DE CV:")

print(f"   • Número de folds: {N_FOLDS}")

print(f"   • Meses mínimos train: {MIN_TRAIN_MONTHS}")

print(f"   • Meses por test: {TEST_MONTHS}")


if 'umbrales_optimizados' in locals():

    print("✅ Umbrales optimizados (Celda 10.6) cargados.")

    umbrales_a_usar = umbrales_optimizados

else:

    print(f"⚠️ Variable 'umbrales_optimizados' no encontrada.")

    print(f"   Usando umbral default {UMBRAL_PROB_DEFAULT}")

    umbrales_a_usar = {}


if 'series_completas_con_kmeans' not in locals():

    raise NameError("❌ 'series_completas_con_kmeans' no encontrado")


print(f"✅ Dataset cargado: {len(series_completas_con_kmeans):,} filas\n")


# ============================================================================

# FUNCIÓN DE VISUALIZACIÓN

# ============================================================================


def generar_visualizaciones_cv_temporal_doble_clasif(

    f1_scores_cls1, auc_scores_cls2, fold_fechas, prefijo_segmento=""

):

    """Visualiza el rendimiento de la validación cruzada para el modelo doble-clasificador."""


    if not f1_scores_cls1:

        print("   > ⚠️ No hay datos para visualizar.")

        return


    n_folds = len(f1_scores_cls1)

    fold_labels = [f"Fold {i+1}\n({fechas['test_start'].strftime('%Y-%m')})" for i, fechas in enumerate(fold_fechas)]


    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    fig.suptitle(f'Validación Cruzada Temporal - {prefijo_segmento}', fontsize=16, weight='bold')


    ax1 = axes[0]

    ax1.plot(fold_labels, f1_scores_cls1, 'o-', label='F1 (Binario)', color='b', markersize=8)

    f1_mean = np.nanmean(f1_scores_cls1)

    ax1.axhline(f1_mean, color='b', linestyle='--', label=f'Media = {f1_mean:.3f}')

    ax1.set_title('Estabilidad F1-Score (Clasif. Binario)')

    ax1.set_ylabel('F1-Score')

    ax1.set_xlabel('Período de Test')

    ax1.set_ylim([0, 1.05])

    ax1.legend()

    ax1.grid(True, alpha=0.3)


    ax2 = axes[1]

    auc_scores_nan = np.array(auc_scores_cls2, dtype=float)

    auc_mean = np.nanmean(auc_scores_nan)


    ax2.plot(fold_labels, auc_scores_nan, 's-', label='AUC (Rangos)', color='g', markersize=8)

    ax2.axhline(auc_mean, color='g', linestyle='--', label=f'Media = {auc_mean:.3f}')

    ax2.axhline(0.5, color='r', linestyle=':', label='Azar (0.5)')

    ax2.set_title('Estabilidad AUC (Clasif. de Rangos)')

    ax2.set_ylabel('AUC (One-vs-Rest)')

    ax2.set_xlabel('Período de Test')

    ax2.set_ylim([0, 1.05])

    ax2.legend()

    ax2.grid(True, alpha=0.3)


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


    nombre_archivo = f'10_7_cv_temporal_{prefijo_segmento}'.replace('.', '_').replace(' ', '_').replace('(', '').replace(')', '')

    plt.savefig(f'{nombre_archivo}.png', dpi=150, bbox_inches='tight')

    print(f"   > ✅ Gráfico: {nombre_archivo}.png")

    plt.close()


# ============================================================================

# BUCLE PRINCIPAL DE VALIDACIÓN

# ============================================================================


resultados_cv_segmentados = {}


print(f"\n{'='*80}")

print(f"🚀 VALIDACIÓN CRUZADA TEMPORAL POR SEGMENTO")

print(f"{'='*80}\n")


for subclase in series_completas_con_kmeans['subclase_kmeans'].unique():

    subclase_str = str(subclase)

    print("\n" + "="*80)

    print(f"🎯 SEGMENTO: '{subclase_str}'")

    print("="*80)


    if any(excluir in subclase_str for excluir in CLUSTERS_A_EXCLUIR):

        print(f"   > ⚠️ EXCLUIDO")

        continue


    df_segmento = series_completas_con_kmeans[

        series_completas_con_kmeans['subclase_kmeans'] == subclase

    ].copy()


    try:

        df_features, feature_cols, _ = preparar_datos_doble_clasificador(df_segmento)

    except Exception as e:

        print(f"   > ❌ Error en preparación: {e}")

        continue


    if len(df_features) < UMBRAL_MINIMO_DATOS:

        print(f"   > ❌ INSUFICIENTE (<{UMBRAL_MINIMO_DATOS})")

        continue


    umbral_segmento = umbrales_a_usar.get(subclase_str, UMBRAL_PROB_DEFAULT)

    print(f"   • Umbral (Binario): {umbral_segmento:.2f}")


    print("\n   🔍 Creando folds temporales...")

    splitter = ExpandingWindowSplitter(

        time_col='fecha',

        n_splits=N_FOLDS,

        min_train_months=MIN_TRAIN_MONTHS,

        test_months=TEST_MONTHS

    )


    try:

        folds = list(splitter.split(df_features))

        print(f"   ✅ {len(folds)} folds creados")

    except ValueError as e:

        print(f"   ❌ Error al crear folds: {e}")

        continue


    f1_scores_cls1 = []

    auc_scores_cls2 = []

    fold_fechas = []


    for fold_idx, (train_idx, test_idx) in enumerate(folds):

        print(f"\n   📊 Fold {fold_idx + 1}/{len(folds)}")


        # ==========================================================

        # AQUÍ ESTABA EL ERROR

        # df_train = df_features.iloc[train_idx]  <-- INCORRECTO

        # df_test = df_features.iloc[test_idx]   <-- INCORRECTO


        df_train = df_features.loc[train_idx] # <-- CORRECTO (usar labels)

        df_test = df_features.loc[test_idx]  # <-- CORRECTO (usar labels)

        # ==========================================================


        fold_fechas.append({

            'train_start': df_train['fecha'].min(),

            'train_end': df_train['fecha'].max(),

            'test_start': df_test['fecha'].min(),

            'test_end': df_test['fecha'].max()

        })


        print(f"      Train: {fold_fechas[-1]['train_start'].strftime('%Y-%m')} → {fold_fechas[-1]['train_end'].strftime('%Y-%m')} ({len(df_train)} muestras)")

        print(f"      Test:  {fold_fechas[-1]['test_start'].strftime('%Y-%m')} → {fold_fechas[-1]['test_end'].strftime('%Y-%m')} ({len(df_test)} muestras)")


        X_train = df_train[feature_cols].values

        X_test = df_test[feature_cols].values


        y_train_cls = df_train['venta_ocurrio'].values

        y_test_cls = df_test['venta_ocurrio'].values


        y_train_rango = df_train['rango_venta'].values

        y_test_rango = df_test['rango_venta'].values


        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X_train)

        X_test_scaled = scaler.transform(X_test)


        try:

            resultado = entrenar_modelo_doble_clasificador(

                X_train_scaled, y_train_cls, y_train_rango,

                X_test_scaled, y_test_cls, y_test_rango,

                HPARAMS_CLASIFICADOR_BINARIO, HPARAMS_CLASIFICADOR_RANGOS,

                umbral_prob=umbral_segmento

            )


            f1_cls1 = resultado['f1_cls1']

            auc_cls2 = resultado['auc_cls2']


            f1_scores_cls1.append(f1_cls1)

            auc_scores_cls2.append(auc_cls2)


            print(f"      → F1 (Binario): {f1_cls1:.3f} | AUC (Rangos): {auc_cls2:.3f}")


        except ValueError as e:

            print(f"      → ⚠️ Omitiendo fold (error en entrenamiento): {e}")

            f1_scores_cls1.append(np.nan)

            auc_scores_cls2.append(np.nan)


    if not f1_scores_cls1 or np.isnan(f1_scores_cls1).all():

        print(f"   ❌ No se pudo ejecutar CV (ningún fold válido)")

        continue


    print("\n   📊 ESTADÍSTICAS AGREGADAS ({} folds):".format(len(f1_scores_cls1) - np.isnan(f1_scores_cls1).sum()))


    f1_mean = np.nanmean(f1_scores_cls1)

    f1_std = np.nanstd(f1_scores_cls1)

    auc_mean = np.nanmean(auc_scores_cls2)

    auc_std = np.nanstd(auc_scores_cls2)


    print(f"      • F1-Score (Binario) promedio: {f1_mean:.3f} ± {f1_std:.3f}")

    print(f"      • AUC (Rangos) promedio: {auc_mean:.3f} ± {auc_std:.3f}")


    try:

        q1_f1 = np.nanquantile(f1_scores_cls1, 0.25)

        problem_folds_f1 = [i+1 for i, f1 in enumerate(f1_scores_cls1) if f1 < q1_f1]

        if problem_folds_f1:

            print(f"      ⚠️ Folds problemáticos (F1 < Q1={q1_f1:.3f}): {problem_folds_f1}")

    except:

        pass


    generar_visualizaciones_cv_temporal_doble_clasif(

        f1_scores_cls1, auc_scores_cls2, fold_fechas, prefijo_segmento=subclase_str

    )


    resultados_cv_segmentados[subclase_str] = {

        'f1_mean': f1_mean,

        'f1_std': f1_std,

        'auc_rangos_mean': auc_mean,

        'auc_rangos_std': auc_std,

        'n_folds_validos': len(f1_scores_cls1) - np.isnan(f1_scores_cls1).sum(),

        'folds_data': {

            'f1_scores': f1_scores_cls1,

            'auc_scores': auc_scores_cls2

        }

    }


# ============================================================================

# REPORTE FINAL

# ============================================================================

print("\n" + "="*80)

print("📊 REPORTE FINAL - VALIDACIÓN CRUZADA TEMPORAL (DOBLE-CLASIFICADOR)")

print("="*80)


if not resultados_cv_segmentados:

    print("❌ No se generaron resultados de CV.")

else:

    dir_cv = os.path.join(BASE_EXPORT_DIR, 'cv_temporal_doble_clasif')

    if not os.path.exists(dir_cv):

        os.makedirs(dir_cv)


    resumen_data = []

    for subclase, data in resultados_cv_segmentados.items():

        resumen_data.append({

            'Sub-Clase': subclase,

            'F1 (Binario) Mean': data['f1_mean'],

            'F1 (Binario) Std': data['f1_std'],

            'AUC (Rangos) Mean': data['auc_rangos_mean'],

            'AUC (Rangos) Std': data['auc_rangos_std'],

            'N Folds': data['n_folds_validos']

        })


    df_resumen = pd.DataFrame(resumen_data).sort_values('F1 (Binario) Mean', ascending=False)


    print("\n" + "="*80)

    print("📈 RESUMEN DE RENDIMIENTO")

    print("="*80)

    print(df_resumen.to_string(index=False))


    with open(os.path.join(dir_cv, 'resultados_cv.json'), 'w') as f:

        json.dump(resultados_cv_segmentados, f, indent=4, default=str)


    df_resumen.to_csv(os.path.join(dir_cv, 'resumen_cv.csv'), index=False)


    print(f"\n✅ Artefactos exportados a '{dir_cv}/'")


print("\n" + "="*80)

print("✅ CELDA 10.7 COMPLETADA")

print("="*80)


print("\n📦 Variable creada:")

print("   • resultados_cv_segmentados")


print("\n💡 INTERPRETACIÓN:")

print("   • F1 (Binario) Mean: Rendimiento promedio para predecir Venta/No Venta.")

print("   • AUC (Rangos) Mean: Rendimiento promedio para predecir Baja/Media/Alta (si > 0.55 es útil).")

print("   • Std (Std Dev): Si es alta (> 0.15), el modelo es inestable en el tiempo.")

print("\n🎯 SIGUIENTE: Celda 11 (Sistema de Re-entrenamiento Automático)")


## CELDA 11 Monitorea y Re-entrena (¡el paso más importante!)


### CELDA 11 ACTUALIZADA


# ============================================================================

# 🔄 CELDA 11: SISTEMA DE RE-ENTRENAMIENTO Y ALERTAS (MLOps)

#

# ADAPTADO PARA EL MODELO DOBLE-CLASIFICADOR

#

# OBJETIVO:

# 1. Monitorear el rendimiento del modelo en "nuevos" datos.

# 2. Detectar "Drift" (cuando el modelo se degrada).

# 3. Re-entrenar automáticamente si el rendimiento cae por debajo de umbrales críticos.

#

# MÉTRICAS MONITOREADAS:

# - F1-Score (Binario): ¿Sigue prediciendo bien "Venta/No Venta"?

# - AUC (Rangos): ¿Sigue prediciendo bien "Baja/Alta"?

# ============================================================================


import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

import joblib

import os

import json

import warnings

from datetime import datetime

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import f1_score, roc_auc_score, accuracy_score


warnings.filterwarnings('ignore')


# ============================================================================

# VERIFICACIÓN DE VARIABLES EN MEMORIA

# ============================================================================

print("Verificando funciones y variables de celdas anteriores...")

try:

    # Funciones de Celda 10.5

    _ = preparar_datos_doble_clasificador

    _ = entrenar_modelo_doble_clasificador


    # Artefactos de Celda 10.5

    _ = modelos_doble_clasif_segmentados

    _ = scalers_doble_clasif_segmentados

    _ = features_doble_clasif_segmentados

    _ = limites_rangos_segmentados

    _ = resultados_doble_clasif_segmentados


    # Umbrales de Celda 10.6

    _ = umbrales_optimizados


    # Datos base

    _ = series_completas_con_kmeans


    # HParams de Celda 10.5

    _ = HPARAMS_CLASIFICADOR_BINARIO

    _ = HPARAMS_CLASIFICADOR_RANGOS


    # Configuración global

    RANDOM_STATE = locals().get('RANDOM_STATE', 42)

    BASE_EXPORT_DIR = locals().get('BASE_EXPORT_DIR', 'modelos_exportados')

    UMBRAL_PROB_DEFAULT = locals().get('UMBRAL_PROB_DEFAULT', 0.5)

    TEST_SIZE_FRAC = locals().get('TEST_SIZE_FRAC', 0.2) # Para simular "nuevos" datos


    print("✅ Funciones y variables cargadas.")

except NameError as e:

    print(f"❌ ERROR: {e}")

    raise NameError("Parece que no has ejecutado las Celdas 10.5 y 10.6. Por favor, ejecútalas y vuelve a intentarlo.")


# ============================================================================

# CONFIGURACIÓN DEL SISTEMA MLOps (¡NUEVOS UMBRALES!)

# ============================================================================


# Umbrales Críticos (disparan re-entrenamiento)

UMBRAL_CRITICO_F1_BINARIO = 0.85  # Si el F1 baja de 0.85 (era 1.0)

UMBRAL_CRITICO_AUC_RANGOS = 0.55  # Si el AUC baja de 0.55 (apenas mejor que el azar)


# Umbrales de Drift (disparan alertas de advertencia)

# Factor multiplicativo: ej. 0.9 = "alerta si el rendimiento cae un 10%"

UMBRAL_DRIFT_F1_BINARIO = 0.95  # Alerta si F1 cae 5% vs. baseline

UMBRAL_DRIFT_AUC_RANGOS = 0.90  # Alerta si AUC cae 10% vs. baseline


print(f"\n⚙️ CONFIGURACIÓN DEL SISTEMA MLOps:")

print(f"   • Umbral Crítico F1 (Binario): < {UMBRAL_CRITICO_F1_BINARIO}")

print(f"   • Umbral Crítico AUC (Rangos): < {UMBRAL_CRITICO_AUC_RANGOS}")

print(f"   • Umbral Drift AUC (Rangos): < 10% del baseline")


# Directorio de salida

dir_reentrenamiento = os.path.join(BASE_EXPORT_DIR, 'reentrenamiento_doble_clasif')

if not os.path.exists(dir_reentrenamiento):

    os.makedirs(dir_reentrenamiento)


# ============================================================================

# BUCLE PRINCIPAL DE MONITOREO Y RE-ENTRENAMIENTO

# ============================================================================


print(f"\n{'='*80}")

print(f"🚀 EJECUTANDO PIPELINE DE RE-ENTRENAMIENTO Y ALERTAS")

print(f"{'='*80}\n")


# Almacenes para resultados

alertas_generadas = []

modelos_reentrenados = {}

scalers_reentrenados = {}

reporte_monitoreo = []


for subclase_str in modelos_doble_clasif_segmentados.keys():

    print("\n" + "="*80)

    print(f"🎯 PROCESANDO: {subclase_str}")

    print("="*80)


    reentrenado = False

    f1_actual = np.nan

    auc_actual = np.nan


    try:

        # ====================================================================

        # PASO 1: Cargar artefactos y datos "nuevos"

        # ====================================================================

        print("\n📊 PASO 1: Cargando artefactos y simulando datos nuevos...")


        # Cargar artefactos

        modelo_actual = modelos_doble_clasif_segmentados[subclase_str]

        scaler_actual = scalers_doble_clasif_segmentados[subclase_str]

        features_actuales = features_doble_clasif_segmentados[subclase_str]

        metricas_baseline = resultados_doble_clasif_segmentados[subclase_str]['metricas']

        umbral_segmento = umbrales_optimizados.get(subclase_str, UMBRAL_PROB_DEFAULT)


        baseline_f1 = metricas_baseline.get('f1_cls1', 1.0)

        baseline_auc = metricas_baseline.get('auc_cls2', 0.5)


        # Simulación de datos: Preparamos TODOS los datos y usamos el 20% final

        # (el mismo test set de Celda 10.5) como nuestros "datos de monitoreo".

        df_segmento_full = series_completas_con_kmeans[

            series_completas_con_kmeans['subclase_kmeans'] == subclase_str

        ].copy()


        df_features, feature_cols, _ = preparar_datos_doble_clasificador(df_segmento_full)


        fechas_unicas = sorted(df_features['fecha'].unique())

        split_idx = int(len(fechas_unicas) * (1 - TEST_SIZE_FRAC))

        fecha_split = fechas_unicas[split_idx]

        mask_test = df_features['fecha'] >= fecha_split


        df_monitoreo = df_features[mask_test].copy()


        if len(df_monitoreo) < 10:

            print(f"   > ⚠️ Datos de monitoreo insuficientes (<10). OMITIENDO.")

            continue


        print(f"   > Baseline F1: {baseline_f1:.3f} | Baseline AUC: {baseline_auc:.3f}")

        print(f"   > {len(df_monitoreo)} filas de datos nuevos para monitorear.")


        # ====================================================================

        # PASO 2: Evaluar modelo actual en datos "nuevos"

        # ====================================================================

        print("\n📊 PASO 2: Evaluando rendimiento del modelo actual...")


        X_monitoreo = df_monitoreo[feature_cols].values

        y_cls_real = df_monitoreo['venta_ocurrio'].values

        y_rango_real = df_monitoreo['rango_venta'].values


        X_monitoreo_scaled = scaler_actual.transform(X_monitoreo)


        # Modelo 1 (Binario)

        cls_binario = modelo_actual['clasificador_binario']


        if cls_binario is None:

            # Caso especial (como A.3): El modelo sabe que siempre hay venta

            print("   > Modelo Binario es 'None' (segmento de solo ventas).")

            # Asignamos la predicción perfecta (predecir siempre 1)

            y_pred_cls = np.ones(len(y_cls_real), dtype=int)

            f1_actual = f1_score(y_cls_real, y_pred_cls, zero_division=0)

        else:

            # Caso normal (como A.5 y A.4)

            y_pred_cls_proba = cls_binario.predict_proba(X_monitoreo_scaled)[:, 1]

            y_pred_cls = (y_pred_cls_proba >= umbral_segmento).astype(int)

            f1_actual = f1_score(y_cls_real, y_pred_cls, zero_division=0)


        # Modelo 2 (Rangos)

        cls_rangos = modelo_actual['clasificador_rangos']

        if cls_rangos is None:

            print("   > ⚠️ Clasificador de rangos no existe. Omitiendo evaluación AUC.")

            auc_actual = np.nan

        else:

            mask_venta_real = y_cls_real == 1

            if mask_venta_real.sum() < 5:

                print("   > ⚠️ No hay suficientes ventas reales en datos nuevos. Omitiendo AUC.")

                auc_actual = np.nan

            else:

                X_monitoreo_rangos = X_monitoreo_scaled[mask_venta_real]

                y_rango_real_filtrado = y_rango_real[mask_venta_real]


                if len(np.unique(y_rango_real_filtrado)) < 2:

                    print("   > ⚠️ Solo 1 clase de rangos en datos nuevos. Omitiendo AUC.")

                    auc_actual = np.nan

                else:

                    y_pred_rangos_proba = cls_rangos.predict_proba(X_monitoreo_rangos)[:, 1]

                    auc_actual = roc_auc_score(y_rango_real_filtrado, y_pred_rangos_proba)


        print(f"   > Rendimiento Actual F1 (Binario): {f1_actual:.3f}")

        print(f"   > Rendimiento Actual AUC (Rangos): {auc_actual:.3f}")


        # ====================================================================

        # PASO 3: Detectar Drift

        # ====================================================================

        print("\n📊 PASO 3: Detectando drift...")

        alertas_segmento = []


        # Chequeos Críticos

        if f1_actual < UMBRAL_CRITICO_F1_BINARIO:

            alertas_segmento.append(('CRITICAL', f'F1 (Binario) críticamente bajo: {f1_actual:.3f} < {UMBRAL_CRITICO_F1_BINARIO}'))


        if not np.isnan(auc_actual) and auc_actual < UMBRAL_CRITICO_AUC_RANGOS:

            alertas_segmento.append(('CRITICAL', f'AUC (Rangos) críticamente bajo: {auc_actual:.3f} < {UMBRAL_CRITICO_AUC_RANGOS}'))


        # Chequeos de Drift (Warning)

        if f1_actual < baseline_f1 * UMBRAL_DRIFT_F1_BINARIO:

            alertas_segmento.append(('WARNING', f'Drift en F1 (Binario): {f1_actual:.3f} < {baseline_f1 * UMBRAL_DRIFT_F1_BINARIO:.3f}'))


        if not np.isnan(auc_actual) and auc_actual < baseline_auc * UMBRAL_DRIFT_AUC_RANGOS:

             alertas_segmento.append(('WARNING', f'Drift en AUC (Rangos): {auc_actual:.3f} < {baseline_auc * UMBRAL_DRIFT_AUC_RANGOS:.3f}'))


        if not alertas_segmento:

            print("   > ✅ Sin drift detectado. Modelo estable.")

        else:

            for tipo, msg in alertas_segmento:

                print(f"   > 🚨 ALERTA {tipo}: {msg}")

                alertas_generadas.append({

                    'timestamp': datetime.now().isoformat(),

                    'segmento': subclase_str,

                    'tipo': tipo,

                    'mensaje': msg

                })


        # ====================================================================

        # PASO 4: Aplicar estrategia de corrección (Re-entrenamiento)

        # ====================================================================

        if any(a[0] == 'CRITICAL' for a in alertas_segmento):

            print("\n🔄 PASO 4: Re-entrenando modelo (Rendimiento Crítico)...")

            reentrenado = True


            # Usar TODOS los datos para re-entrenar

            X_full = df_features[feature_cols].values

            y_cls_full = df_features['venta_ocurrio'].values

            y_rango_full = df_features['rango_venta'].values


            # 1. Re-entrenar Scaler

            scaler_nuevo = StandardScaler()

            X_full_scaled = scaler_nuevo.fit_transform(X_full)


            # 2. Re-entrenar Modelos

            resultado_nuevo = entrenar_modelo_doble_clasificador(

                X_full_scaled, y_cls_full, y_rango_full, # Train

                X_full_scaled, y_cls_full, y_rango_full, # Test (solo para que corra, no se usa)

                HPARAMS_CLASIFICADOR_BINARIO,

                HPARAMS_CLASIFICADOR_RANGOS,

                umbral_prob=umbral_segmento

            )


            # 3. Guardar nuevos artefactos

            modelos_reentrenados[subclase_str] = {

                'clasificador_binario': resultado_nuevo['clasificador_binario'],

                'clasificador_rangos': resultado_nuevo['clasificador_rangos']

            }

            scalers_reentrenados[subclase_str] = scaler_nuevo

            print("   > ✅ Re-entrenamiento completado y artefactos guardados.")


        else:

            print("\n📊 PASO 4: No se requiere re-entrenamiento.")


    except Exception as e:

        print(f"\n❌ ERROR FATAL procesando segmento {subclase_str}: {e}")

        alertas_generadas.append({

            'timestamp': datetime.now().isoformat(),

            'segmento': subclase_str,

            'tipo': 'FATAL',

            'mensaje': str(e)

        })


    finally:

        # Guardar reporte de esta ejecución

        reporte_monitoreo.append({

            'segmento': subclase_str,

            'f1_baseline': baseline_f1,

            'f1_actual': f1_actual,

            'auc_baseline': baseline_auc,

            'auc_actual': auc_actual,

            'reentrenado': reentrenado

        })


# ============================================================================

# REPORTE FINAL

# ============================================================================

print("\n" + "="*80)

print("📋 RESUMEN FINAL - PIPELINE MLOps")

print("="*80)


# Resumen de Rendimiento

df_reporte = pd.DataFrame(reporte_monitoreo).set_index('segmento')

print("\n📈 RESUMEN DE MONITOREO:")

print(df_reporte.to_string(float_format="%.3f"))


# Resumen de Alertas

print("\n🚨 RESUMEN DE ALERTAS:")

if not alertas_generadas:

    print("   > 💚 No se generaron alertas.")

else:

    df_alertas = pd.DataFrame(alertas_generadas)

    print(df_alertas[['segmento', 'tipo', 'mensaje']].to_string())


    # Exportar alertas

    df_alertas.to_csv(os.path.join(dir_reentrenamiento, 'alertas_mlops.csv'), index=False)

    with open(os.path.join(dir_reentrenamiento, 'alertas_mlops.json'), 'w') as f:

        json.dump(alertas_generadas, f, indent=4, default=str)


# Exportar Modelos Re-entrenados

if modelos_reentrenados:

    print(f"\n💾 Exportando {len(modelos_reentrenados)} modelos re-entrenados...")

    joblib.dump(modelos_reentrenados, os.path.join(dir_reentrenamiento, 'modelos_reentrenados.pkl'))

    joblib.dump(scalers_reentrenados, os.path.join(dir_reentrenamiento, 'scalers_reentrenados.pkl'))

else:

    print("\n💾 No hubo modelos para re-entrenar.")


# Exportar reporte de monitoreo

df_reporte.to_csv(os.path.join(dir_reentrenamiento, 'reporte_monitoreo.csv'))


print(f"\n✅ Artefactos exportados a '{dir_reentrenamiento}/'")

print("\n" + "="*80)

print("✅ CELDA 11 COMPLETADA - SISTEMA DE RE-ENTRENAMIENTO ACTIVO")

print("="*80)


alertas_mlops.csv: Este es el que te falta. Se crea solo si se detecta CUALQUIER tipo de alerta (Warning o Critical). Si tus modelos están todos sanos (🟢 OK), es normal que este archivo no se cree.

modelos_reentrenados.pkl


scalers_reentrenados.pkl

Tu nota es 100% correcta. Esos dos archivos SOLO se crearán si la Celda 11 detecta un drift CRÍTICO (🔴) y decide que el modelo es irrecuperable y necesita re-entrenarse desde cero.


## CELDA 12 V2 Predice (usando los modelos re-entrenados)


# ============================================================================

# 🎯 CELDA 12: SISTEMA DE PREDICCIÓN FINAL (API DE INFERENCIA)

#

# OBJETIVO:

# 1. Cargar TODOS los artefactos (base, re-entrenados, scalers, features, etc.)

# 2. Consolidar los modelos: Reemplazar modelos base con los re-entrenados (MLOps).

# 3. Crear una función única que prediga P(Venta) y P(Baja/Alta).

# ============================================================================


import pandas as pd

import numpy as np

import joblib

import os

import warnings

warnings.filterwarnings('ignore')


print("="*80)

print("🎯 CELDA 12: SISTEMA DE PREDICCIÓN FINAL (DOBLE-CLASIFICADOR)")

print("="*80)


# ============================================================================

# 1. CARGA DE ARTEFACTOS (BASE + RE-ENTRENADOS)

# ============================================================================

print("📤 1. Cargando todos los artefactos del pipeline...")


try:

    # Directorios

    dir_base = os.path.join(BASE_EXPORT_DIR, 'doble_clasificador')

    dir_reentrenado = os.path.join(BASE_EXPORT_DIR, 'reentrenamiento_doble_clasif')


    # Cargar Modelos BASE (de Celda 10.5)

    modelos_base = joblib.load(os.path.join(dir_base, 'modelos_doble_clasif.pkl'))


    # Cargar Artefactos de SOPORTE (Scalers, Features, Límites)

    scalers_prod = joblib.load(os.path.join(dir_base, 'scalers_doble_clasif.pkl'))

    features_prod = joblib.load(os.path.join(dir_base, 'features_doble_clasif.pkl'))

    limites_prod = joblib.load(os.path.join(dir_base, 'limites_rangos.pkl'))


    # Cargar Umbrales (de Celda 10.6)

    umbrales_prod = umbrales_optimizados # Ya está en memoria


    # Cargar Modelos RE-ENTRENADOS (de Celda 11)

    if os.path.exists(os.path.join(dir_reentrenado, 'modelos_reentrenados.pkl')):

        modelos_reentrenados = joblib.load(os.path.join(dir_reentrenado, 'modelos_reentrenados.pkl'))

        scalers_reentrenados = joblib.load(os.path.join(dir_reentrenado, 'scalers_reentrenados.pkl'))

        print(f"   > ✅ {len(modelos_reentrenados)} modelos re-entrenados cargados.")

    else:

        print("   > ⚠️ No se encontraron modelos re-entrenados (Celda 11 no ejecutada).")

        modelos_reentrenados = {}

        scalers_reentrenados = {}


except Exception as e:

    print(f"❌ ERROR: No se pudieron cargar los artefactos. ¿Ejecutaste las celdas 10.5, 10.6 y 11? \n   {e}")

    raise e


# ============================================================================

# 2. CONSOLIDACIÓN DE MODELOS (LÓGICA MLOps)

# ============================================================================

print("\n🔄 2. Consolidando modelos (MLOps)...")


# Empezamos con los modelos base

modelos_produccion = modelos_base.copy()

scalers_produccion = scalers_prod.copy()


# Sobrescribimos los modelos que fueron re-entrenados en Celda 11

for segmento, modelo in modelos_reentrenados.items():

    if segmento in modelos_produccion:

        print(f"   > Aplicando parche MLOps: Reemplazando modelo '{segmento}' por versión re-entrenada.")

        modelos_produccion[segmento] = modelo

        scalers_produccion[segmento] = scalers_reentrenados[segmento]


print("   > ✅ Modelos de producción listos.")


# ============================================================================

# 3. FUNCIÓN DE PREDICCIÓN UNIFICADA

# ============================================================================


def predecir_producto(df_nuevos_features, segmento):

    """

    Predice las probabilidades de 'No Venta', 'Venta Baja' y 'Venta Alta'

    para un conjunto de datos y un segmento dado.

    """


    print(f"\n--- Prediciendo para Segmento: {segmento} ---")


    # 1. Cargar artefactos para este segmento

    try:

        modelo_dict = modelos_produccion[segmento]

        scaler = scalers_produccion[segmento]

        feature_cols = features_prod[segmento]

        umbral = umbrales_prod.get(segmento, 0.5)

        limites = limites_prod[segmento]

    except KeyError:

        return {'error': f'Artefactos no encontrados para el segmento {segmento}'}


    # 2. Preparar datos

    X = df_nuevos_features[feature_cols].values

    X_scaled = scaler.transform(X)


    cls_binario = modelo_dict['clasificador_binario']

    cls_rangos = modelo_dict['clasificador_rangos']


    # 3. Predicción Etapa 1 (¿Venta o No Venta?)

    if cls_binario is None:

        # Caso especial (ej. A.3): 100% ventas

        print("   > Estrategia: Solo Rangos (Segmento 100% ventas)")

        prob_venta = np.ones(len(X))

    else:

        # Caso normal (ej. A.5, A.4)

        print("   > Estrategia: Doble-Clasificador (Venta + Rango)")

        prob_venta = cls_binario.predict_proba(X_scaled)[:, 1]


    # 4. Predicción Etapa 2 (¿Baja o Alta?)

    if cls_rangos is None:

        # Esto no debería pasar si la preparación de datos funcionó

        print("   > ADVERTENCIA: Clasificador de rangos es 'None'. Usando 50/50.")

        prob_rangos = np.full((len(X), 2), 0.5)

    else:

        prob_rangos = cls_rangos.predict_proba(X_scaled) # Devuelve [P(Baja), P(Alta)]


    # 5. Combinar probabilidades

    prob_no_venta = 1.0 - prob_venta

    prob_venta_baja = prob_venta * prob_rangos[:, 0]

    prob_venta_alta = prob_venta * prob_rangos[:, 1]


    # 6. Generar resultado

    resultados = {

        'segmento': segmento,

        'limite_baja_alta': limites['q_50'],

        'P(No Venta)': np.mean(prob_no_venta),

        'P(Venta Baja)': np.mean(prob_venta_baja),

        'P(Venta Alta)': np.mean(prob_venta_alta),

        'suma_prob': np.mean(prob_no_venta + prob_venta_baja + prob_venta_alta), # Debe ser 1.0

        'prob_total_venta': np.mean(prob_venta)

    }


    return resultados


# ============================================================================

# 4. EJEMPLO DE INFERENCIA

# ============================================================================

print("\n" + "="*80)

print("📊 EJEMPLO: Inferencia en Producción")

print("="*80)


# --- Simulación: Cargar "datos nuevos" para predecir ---

# Usaremos los mismos datos que preparamos en la Celda 11

# (En un caso real, aquí cargarías datos nuevos y les harías Feature Engineering)

try:

    print("Simulando datos nuevos para el segmento A.5...")

    df_segmento_a5 = series_completas_con_kmeans[

        series_completas_con_kmeans['subclase_kmeans'] == 'A.5'

    ].copy()


    df_nuevos_features_a5, _, _ = preparar_datos_doble_clasificador(df_segmento_a5)


    # --- Ejecutar predicción para A.5 ---

    # El sistema usará automáticamente el modelo RE-ENTRENADO (AUC 0.923)

    prediccion_a5 = predecir_producto(df_nuevos_features_a5, 'A.5')


    print("\n--- RESULTADO (Segmento A.5) ---")

    print(json.dumps(prediccion_a5, indent=4, default=str))



    print("\nSimulando datos nuevos para el segmento A.4...")

    df_segmento_a4 = series_completas_con_kmeans[

        series_completas_con_kmeans['subclase_kmeans'] == 'A.4'

    ].copy()


    df_nuevos_features_a4, _, _ = preparar_datos_doble_clasificador(df_segmento_a4)


    # --- Ejecutar predicción para A.4 ---

    # El sistema usará automáticamente el modelo BASE (ya que no se re-entrenó)

    prediccion_a4 = predecir_producto(df_nuevos_features_a4, 'A.4')


    print("\n--- RESULTADO (Segmento A.4) ---")

    print(json.dumps(prediccion_a4, indent=4, default=str))


except Exception as e:

    print(f"\n❌ Error en el ejemplo de inferencia: {e}")

    print("   Asegúrate de que 'series_completas_con_kmeans' esté disponible.")


print("\n" + "="*80)

print("✅ CELDA 12 COMPLETADA")

print("="*80)

print("\n💡 ¡PIPELINE COMPLETO!")

print("   Has construido un sistema que:")

print("   1. Prepara y entrena un modelo Doble-Clasificador (Celda 10.5)")

print("   2. Optimiza sus umbrales (Celda 10.6)")

print("   3. Valida su estabilidad en el tiempo (Celda 10.7)")

print("   4. Monitorea el 'drift' y se re-entrena automáticamente (Celda 11)")

print("   5. Usa los mejores modelos para hacer predicciones (Celda 12)")


## APP DE PREDICCION DE DEMANDA


!pip install streamlit


%%writefile app.py

import streamlit as st

import pandas as pd

import numpy as np

import joblib

import os

import re

import unicodedata

import json

from unidecode import unidecode

from datetime import datetime

from dateutil.relativedelta import relativedelta

from sentence_transformers import SentenceTransformer  # Necesario para preparar_datos

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

import warnings


warnings.filterwarnings('ignore')


# --- CONFIGURACIÓN DE RUTAS ---

BASE_EXPORT_DIR = 'models_export'

DATA_FILE = '08_series_temporales_clase_a_con_kmeans.xlsx'

DIR_BASE_MODELOS = os.path.join(BASE_EXPORT_DIR, 'doble_clasificador')

DIR_REENTRENADOS = os.path.join(BASE_EXPORT_DIR, 'reentrenamiento_doble_clasif')

DIR_UMBRALES = os.path.join(BASE_EXPORT_DIR, 'optimizacion_umbral')


# =============================================================================

# FUNCIONES AUXILIARES (COPIADAS DE TU NOTEBOOK)

# =============================================================================


# --- De normalizacion.py ---

def normalizar_texto(texto):

    """

    Normaliza texto para mejorar matching

    """

    if pd.isna(texto):

        return ""


    texto = str(texto).lower().strip()

    texto = re.sub(r'\s+', ' ', texto)

    try:

        texto = unidecode(texto)

    except:

        pass # Fallback si unidecode falla

    texto = re.sub(r'(\d)[.,](\d)', r'\1.\2', texto)

    texto = re.sub(r'[^\w\s.]', '', texto)

    texto = re.sub(r'\.{2,}', '.', texto)

    return texto


# --- De Celda 10.5: Feature Engineering ---

# NOTA: Se asume que SentenceTransformer está disponible

@st.cache_resource

def get_sentence_model():

    # Esta función se cachea para no cargar el modelo de embeddings cada vez

    try:

        return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    except Exception as e:

        st.error(f"Error cargando modelo de embeddings: {e}")

        return None


def preparar_datos_doble_clasificador(df_segmento):

    """

    Prepara datos para modelo doble-clasificador:

    1. Target binario: venta_ocurrio (0/1)

    2. Target rangos: rango_venta (0=Baja, 1=Alta)

    3. Features de Precio y Operacionales

    """

    # Esta función es una réplica de la Celda 10.5


    df_prep = df_segmento.copy()

    df_prep['fecha'] = pd.to_datetime(df_prep['fecha'])


    # Target 1: Clasificación binaria

    df_prep['venta_ocurrio'] = (df_prep['cantidad_vendida'] > 0).astype(int)


    # Target 2: Clasificación de Rangos (2 RANGOS)

    ventas_positivas = df_prep[df_prep['venta_ocurrio'] == 1]['cantidad_vendida']

    limites_rangos = None

    df_prep['rango_venta'] = -1  # Default para 'No Venta'


    if len(ventas_positivas) > 10: # Umbral bajo para inferencia

        q_50 = ventas_positivas.quantile(0.50)

        limites_rangos = {'q_50': float(q_50)}

        indices_venta = df_prep[df_prep['venta_ocurrio'] == 1].index

        df_prep.loc[indices_venta, 'rango_venta'] = pd.cut(

            ventas_positivas,

            bins=[-np.inf, q_50, np.inf],

            labels=[0, 1], # 0=Baja, 1=Alta

            right=False

        ).astype(int)


    # FEATURE ENGINEERING

    features_list = []


    for producto in df_prep['producto'].unique():

        df_prod = df_prep[df_prep['producto'] == producto].sort_values('fecha').copy()


        # 1. FEATURES DE PRECIO

        cantidad_segura = df_prod['cantidad_vendida'].replace(0, np.nan)

        df_prod['precio_implicito'] = df_prod['venta_bs'] / cantidad_segura

        df_prod['precio_implicito'] = df_prod['precio_implicito'].ffill().bfill()

        df_prod['precio_implicito'] = df_prod['precio_implicito'].fillna(0)


        precio_medio_hist = df_prod['precio_implicito'][df_prod['precio_implicito'] > 0].mean()

        if precio_medio_hist > 0:

            df_prod['precio_relativo'] = (df_prod['precio_implicito'] / precio_medio_hist) - 1.0

        else:

            df_prod['precio_relativo'] = 0.0


        df_prod['hubo_descuento_implicito'] = (df_prod['precio_relativo'] < -0.05).astype(int)


        # 2. FEATURES OPERACIONALES

        df_prod['fecha_ultima_compra'] = df_prod['fecha'].where(df_prod['venta_ocurrio'] == 1).ffill()

        if 'fecha_ultima_compra' in df_prod.columns and not df_prod['fecha_ultima_compra'].isna().all():

            df_prod['dias_desde_ultima_compra'] = (df_prod['fecha'] - df_prod['fecha_ultima_compra']).dt.days

            df_prod['dias_desde_ultima_compra'] = df_prod['dias_desde_ultima_compra'].fillna(0).astype(int)

        else:

            df_prod['dias_desde_ultima_compra'] = 0


        racha_no_venta = (df_prod['venta_ocurrio'] != 0).cumsum()

        df_prod['racha_de_no_venta'] = df_prod.groupby(racha_no_venta).cumcount()


        # 3. FEATURES TEMPORALES Y LAGS

        df_prod['mes'] = df_prod['fecha'].dt.month

        df_prod['trimestre'] = df_prod['fecha'].dt.quarter

        df_prod['mes_sin'] = np.sin(2 * np.pi * df_prod['mes'] / 12)

        df_prod['mes_cos'] = np.cos(2 * np.pi * df_prod['mes'] / 12)


        for lag in [1, 3, 6]:

            df_prod[f'lag_{lag}'] = df_prod['cantidad_vendida'].shift(lag)

            df_prod[f'venta_ocurrio_lag_{lag}'] = df_prod['venta_ocurrio'].shift(lag)


        for ventana in [3, 6]:

            df_prod[f'media_movil_{ventana}'] = (

                df_prod['cantidad_vendida'].shift(1)

                .rolling(window=ventana, min_periods=1).mean()

            )


        for ventana in [3, 6, 12]:

            df_prod[f'tasa_ocurrencia_{ventana}'] = (

                df_prod['venta_ocurrio'].shift(1)

                .rolling(window=ventana, min_periods=1).mean()

            )


        features_list.append(df_prod)


    if not features_list:

        return pd.DataFrame(), [], None


    df_features = pd.concat(features_list, ignore_index=True)


    feature_cols = [col for col in df_features.columns if col not in

                    ['producto', 'fecha', 'cantidad_vendida', 'venta_bs',

                     'num_transacciones', 'periodo', 'venta_ocurrio',

                     'subclase_kmeans', 'grupo_venta', 'rango_venta',

                     'fecha_ultima_compra', 'precio_implicito']]


    df_features = df_features.replace([np.inf, -np.inf], np.nan)

    # Llenamos NaNs para la predicción

    df_features = df_features.fillna(0)


    return df_features, feature_cols, limites_rangos


# =============================================================================

# FUNCIÓN DE PREDICCIÓN (ADAPTADA DE CELDA 12)

# =============================================================================


def predecir_producto(df_single_row_features, segmento, modelos_prod, scalers_prod, features_prod, limites_prod, umbrales_prod):

    """

    Predice las probabilidades para una ÚNICA fila de features.

    """

    try:

        # 1. Cargar artefactos para este segmento

        modelo_dict = modelos_prod[segmento]

        scaler = scalers_prod[segmento]

        feature_cols = features_prod[segmento]

        umbral = umbrales_prod.get(segmento, 0.5)

        limites = limites_prod[segmento]

    except KeyError as e:

        st.error(f"Error: No se encontraron artefactos para el segmento '{segmento}'. ¿Se entrenó el modelo? (Error: {e})")

        return None


    # 2. Alinear columnas y escalar

    # Aseguramos que la fila tenga todas las columnas que el modelo espera, en el orden correcto

    X_pred = df_single_row_features.reindex(columns=feature_cols).fillna(0)

    X_scaled = scaler.transform(X_pred)


    cls_binario = modelo_dict.get('clasificador_binario')

    cls_rangos = modelo_dict.get('clasificador_rangos')


    if cls_rangos is None:

        st.error(f"Error: El clasificador de rangos para '{segmento}' no está cargado.")

        return None


    # 3. Predicción Etapa 1 (¿Venta o No Venta?)

    if cls_binario is None:

        # Caso especial (ej. A.3): 100% ventas

        prob_venta = 1.0

    else:

        # Caso normal

        prob_venta = cls_binario.predict_proba(X_scaled)[0, 1]


    # 4. Predicción Etapa 2 (¿Baja o Alta?)

    prob_rangos = cls_rangos.predict_proba(X_scaled)[0] # Devuelve [P(Baja), P(Alta)]


    # 5. Combinar probabilidades

    prob_no_venta = 1.0 - prob_venta

    prob_venta_baja = prob_venta * prob_rangos[0]

    prob_venta_alta = prob_venta * prob_rangos[1]


    # 6. Suma de comprobación

    suma_total = prob_no_venta + prob_venta_baja + prob_venta_alta


    # 7. Generar resultado

    resultados = {

        'segmento': segmento,

        'limite_baja_alta_cant': limites.get('q_50', 0),

        'P(No Venta)': prob_no_venta,

        'P(Venta Baja)': prob_venta_baja,

        'P(Venta Alta)': prob_venta_alta,

        'suma_prob_check': suma_total,

        'prob_total_venta': prob_venta,

        'umbral_optimizado_usado': umbral

    }

    return resultados


# =============================================================================

# FUNCIÓN DE CARGA DE DATOS Y ARTEFACTOS (CACHEADA)

# =============================================================================


@st.cache_data

def load_artifacts_and_data():

    """

    Carga todos los artefactos (modelos, scalers) y el archivo de datos principal.

    Se cachea para alta velocidad.

    """

    # Cargar Modelos BASE

    try:

        modelos_base = joblib.load(os.path.join(DIR_BASE_MODELOS, 'modelos_doble_clasif.pkl'))

        scalers_prod = joblib.load(os.path.join(DIR_BASE_MODELOS, 'scalers_doble_clasif.pkl'))

        features_prod = joblib.load(os.path.join(DIR_BASE_MODELOS, 'features_doble_clasif.pkl'))

        limites_prod = joblib.load(os.path.join(DIR_BASE_MODELOS, 'limites_rangos.pkl'))

    except FileNotFoundError:

        st.error(f"Error Crítico: No se encontraron los artefactos base en '{DIR_BASE_MODELOS}'. Ejecuta la Celda 10.5.")

        return None


    # Cargar Umbrales

    try:

        with open(os.path.join(DIR_UMBRALES, 'umbrales_optimizados.json'), 'r') as f:

            umbrales_prod = json.load(f)

    except FileNotFoundError:

        st.warning(f"No se encontró 'umbrales_optimizados.json'. Usando 0.5 por defecto. Ejecuta la Celda 10.6 para optimizar.")

        umbrales_prod = {}


    # Cargar Modelos RE-ENTRENADOS (si existen)

    try:

        modelos_reentrenados = joblib.load(os.path.join(DIR_REENTRENADOS, 'modelos_reentrenados.pkl'))

        scalers_reentrenados = joblib.load(os.path.join(DIR_REENTRENADOS, 'scalers_reentrenados.pkl'))

    except FileNotFoundError:

        modelos_reentrenados = {}

        scalers_reentrenados = {}


    # Consolidar (MLOps): Sobrescribir base con re-entrenados

    modelos_produccion = modelos_base.copy()

    scalers_produccion = scalers_prod.copy()

    for segmento, modelo in modelos_reentrenados.items():

        if segmento in modelos_produccion:

            modelos_produccion[segmento] = modelo

            scalers_produccion[segmento] = scalers_reentrenados[segmento]


    # Cargar Datos Históricos

    try:

        df_series = pd.read_excel(DATA_FILE)

    except FileNotFoundError:

        st.error(f"Error Crítico: No se encontró el archivo de datos '{DATA_FILE}'. Ejecuta la Celda 8.")

        return None


    return modelos_produccion, scalers_produccion, features_prod, limites_prod, umbrales_prod, df_series


# =============================================================================

# INTERFAZ DE USUARIO DE STREAMLIT

# =============================================================================


st.set_page_config(layout="wide", page_title="Predicción PlusSteel")

st.title("📦 Sistema de Predicción de Demanda PlusSteel")

st.markdown("Esta aplicación utiliza un modelo de Machine Learning (Doble Clasificador segmentado por K-Means) para predecir la demanda del próximo mes.")


# Cargar todo

with st.spinner("Cargando modelos y datos históricos..."):

    carga = load_artifacts_and_data()


if carga is None:

    st.error("La aplicación no pudo iniciarse. Faltan archivos de modelo o datos. Por favor, revisa los logs.")

else:

    modelos_prod, scalers_prod, features_prod, limites_prod, umbrales_prod, df_series = carga


    # Inicializar el modelo de embeddings

    get_sentence_model()


    st.success("¡Modelos y datos cargados exitosamente!")


    # --- UI de Selección ---

    lista_productos = sorted(df_series['producto'].unique())

    producto_sel = st.selectbox("Seleccione un producto de Clase A para predecir:", lista_productos)


    if st.button(f"Generar Predicción para el Próximo Mes"):

        with st.spinner(f"Generando features y ejecutando predicción para '{producto_sel}'..."):

            try:

                # 1. Obtener historial y segmento del producto

                df_historial_prod = df_series[df_series['producto'] == producto_sel].copy()

                df_historial_prod['fecha'] = pd.to_datetime(df_historial_prod['fecha'])

                segmento = df_historial_prod['subclase_kmeans'].iloc[0]


                st.info(f"Producto '{producto_sel}' pertenece al segmento: **{segmento}**")


                # --- VALIDACIÓN DE MODELO ---

                # Verificar si tenemos un modelo entrenado para este segmento

                if segmento not in modelos_prod:

                    st.error(f"**Error: Modelo No Encontrado**")

                    st.warning(f"No existe un modelo entrenado para el segmento **'{segmento}'**.")

                    st.info(f"Esto generalmente ocurre porque el segmento tenía muy pocos datos históricos (el umbral era < {80} filas) y fue omitido automáticamente durante el entrenamiento en la Celda 10.5 del notebook para garantizar la calidad.")

                    st.stop() # Detiene la ejecución aquí

                # --- FIN DE VALIDACIÓN ---


                # 2. Crear la fila futura para la cual queremos predecir

                fecha_ultima = df_historial_prod['fecha'].max()

                fecha_prediccion = (fecha_ultima + relativedelta(months=1)).replace(day=1)


                # Creamos un DataFrame con la nueva fila

                # Las columnas 'cantidad_vendida', 'venta_bs', etc., se dejan como 0 o NaN

                # ya que `preparar_datos` las usará como lags

                df_futuro = pd.DataFrame([{

                    'producto': producto_sel,

                    'fecha': fecha_prediccion,

                    'cantidad_vendida': 0, # Placeholder

                    'venta_bs': 0, # Placeholder

                    'num_transacciones': 0, # Placeholder

                    'subclase_kmeans': segmento

                }])


                df_combined = pd.concat([df_historial_prod, df_futuro], ignore_index=True)


                # 3. Correr Feature Engineering

                # Esta función crea lags, medias móviles, etc., para todas las filas.

                df_features_full, feature_cols, _ = preparar_datos_doble_clasificador(df_combined)


                # 4. Extraer solo la última fila (la fila de predicción)

                df_features_pred = df_features_full.iloc[[-1]]


                # 5. Llamar a la predicción

                resultado = predecir_producto(

                    df_features_pred,

                    segmento,

                    modelos_prod,

                    scalers_prod,

                    features_prod,

                    limites_prod,

                    umbrales_prod

                )


                # 6. Mostrar resultados

                if resultado:

                    st.subheader(f"Predicción para: {producto_sel} (Próximo Mes: {fecha_prediccion.strftime('%Y-%m')})")


                    limite_cant = resultado['limite_baja_alta_cant']

                    p_no = resultado['P(No Venta)']

                    p_baja = resultado['P(Venta Baja)']

                    p_alta = resultado['P(Venta Alta)']


                    col1, col2, col3 = st.columns(3)

                    col1.metric("Probabilidad de NO Venta", f"{p_no:.1%}")

                    col2.metric(f"Prob. Venta BAJA (< {limite_cant:.0f} u.)", f"{p_baja:.1%}")

                    col3.metric(f"Prob. Venta ALTA (> {limite_cant:.0f} u.)", f"{p_alta:.1%}")


                    # Lógica de recomendación simple

                    if p_no > 0.6:

                        st.warning("**Recomendación:** Baja probabilidad de venta. Considerar no reabastecer o mantener stock mínimo.")

                    elif p_alta > p_baja:

                        st.success(f"**Recomendación:** Alta probabilidad de venta y en rango ALTO (> {limite_cant:.0f} u.). **Priorizar reabastecimiento.**")

                    else:

                        st.info(f"**Recomendación:** Probabilidad de venta en rango BAJO (< {limite_cant:.0f} u.). Reabastecer con cautela.")


                    with st.expander("Ver JSON completo de la predicción"):

                        st.json(resultado)

                else:

                    st.error("No se pudo generar la predicción.")


            except Exception as e:

                st.error(f"Ocurrió un error inesperado durante la predicción:")

                st.exception(e)


!zip -r models_export.zip /content/models_export



!zip -r models_export.zip /content/models_export


Soluciona el Dilema del "Stock Actual": La forma en que lo manejaste es perfecta. En lugar de detenerte porque no tienes un archivo de stock actual, la celda se enfoca en lo que el modelo sí puede hacer:


    Pronostica la demanda (demanda_esperada).


    Calcula el Stock de Seguridad Inteligente (stock_seguridad_sugerido).


    Calcula el punto_reorden (demanda_esperada + stock_seguridad_sugerido).


Esto es más valioso que un simple "Comprar 100". Le das al gerente de compras la inteligencia para que él pueda restarle su "Stock Actual" y tomar la decisión final.

Lógica Correcta y Reutilización:


    Itera correctamente sobre la lista de productos de Clase A de series_completas_con_kmeans.


    Reutiliza de forma inteligente la lógica de predicción de tu app.py (combinar historial + fila futura, llamar a preparar_datos..., y luego a predecir_producto). Esto garantiza que las predicciones del notebook coincidan con las del dashboard.


Calidad de Código (Muy Alta):


    Verificación de Dependencias: El bloque al inicio que revisa que todas las funciones y variables existan es una práctica profesional y te ahorrará muchos errores.


    Robustez: El try...except dentro del bucle tqdm es perfecto. Si un producto falla, lo registra en errores.txt y continúa con el siguiente, en lugar de detener todo el proceso.


    Generación de Reportes: No solo creas el CSV, sino que imprimes un "Resumen Ejecutivo" en la consola y guardas un resumen_planificacion.json. Esto es increíblemente útil.


## CELDA 13 PLANIFICACION DE LA DEMANDA


# ============================================================================

# 🎯 CELDA 13: GENERACIÓN DE RECOMENDACIONES DE PLANIFICACIÓN DE DEMANDA

#

# OBJETIVO:

# 1. Iterar sobre CADA producto de Clase A (series_completas_con_kmeans)

# 2. Obtener su predicción de demanda (P(Venta), P(Baja), P(Alta))

# 3. Calcular Stock de Seguridad Probabilístico

# 4. Generar recomendaciones de compra

# 5. Guardar todo en "planificacion_demanda.csv"

#

# DEPENDENCIAS:

# - Celda 8: series_completas_con_kmeans

# - Celda 10.5: preparar_datos_doble_clasificador, modelos, scalers

# - Celda 12: predecir_producto

# ============================================================================


import pandas as pd

import numpy as np

import warnings

from datetime import datetime

from dateutil.relativedelta import relativedelta

from tqdm import tqdm


warnings.filterwarnings('ignore')


print("="*80)

print("🎯 CELDA 13: GENERACIÓN DE PLANIFICACIÓN DE DEMANDA")

print("="*80)


# ============================================================================

# VERIFICACIÓN DE DEPENDENCIAS

# ============================================================================

print("\n🔍 Verificando dependencias...")


required_vars = {

    'series_completas_con_kmeans': 'DataFrame con productos Clase A (Celda 8)',

    'modelos_doble_clasif_segmentados': 'Modelos entrenados (Celda 10.5)',

    'scalers_doble_clasif_segmentados': 'Scalers (Celda 10.5)',

    'features_doble_clasif_segmentados': 'Features (Celda 10.5)',

    'limites_rangos_segmentados': 'Límites de rangos (Celda 10.5)',

    'umbrales_optimizados': 'Umbrales optimizados (Celda 10.6)',

    'preparar_datos_doble_clasificador': 'Función de preparación (Celda 10.5)',

    'predecir_producto': 'Función de predicción (Celda 12)'

}


missing_vars = []

for var_name, descripcion in required_vars.items():

    if var_name not in locals() and var_name not in globals():

        missing_vars.append(f"  ❌ {var_name}: {descripcion}")

    else:

        print(f"  ✅ {var_name}")


if missing_vars:

    print("\n❌ ERROR: Faltan las siguientes dependencias:")

    for msg in missing_vars:

        print(msg)

    raise NameError("Ejecuta las celdas 8, 10.5, 10.6 y 12 antes de continuar.")


print("✅ Todas las dependencias disponibles\n")


# ============================================================================

# FUNCIÓN: CALCULAR STOCK DE SEGURIDAD PROBABILÍSTICO

# ============================================================================

def calcular_stock_seguridad_probabilistico(prob_venta_alta, prob_venta_baja,

                                           limite_baja_alta, nivel_servicio=0.95):

    """

    Calcula el stock de seguridad basado en probabilidades de demanda.


    Parámetros:

    -----------

    prob_venta_alta : float

        Probabilidad de venta alta (rango alto)

    prob_venta_baja : float

        Probabilidad de venta baja (rango bajo)

    limite_baja_alta : float

        Límite que separa baja de alta demanda (q_50)

    nivel_servicio : float

        Nivel de servicio deseado (default: 95%)


    Returns:

    --------

    dict con:

        - stock_seguridad: Unidades de stock de seguridad

        - demanda_esperada: Demanda esperada (media ponderada)

        - demanda_max: Demanda máxima considerada

    """

    # Demanda esperada (media ponderada)

    # Asumimos que:

    # - Venta Baja tiene demanda promedio = limite_baja_alta * 0.5

    # - Venta Alta tiene demanda promedio = limite_baja_alta * 1.5

    demanda_baja_promedio = limite_baja_alta * 0.5

    demanda_alta_promedio = limite_baja_alta * 1.5


    demanda_esperada = (

        prob_venta_baja * demanda_baja_promedio +

        prob_venta_alta * demanda_alta_promedio

    )


    # Desviación estándar (asumimos CV = 0.5 como heurística)

    desviacion_std = demanda_esperada * 0.5


    # Factor Z para el nivel de servicio

    # 95% → Z=1.645, 99% → Z=2.33

    if nivel_servicio >= 0.99:

        z_score = 2.33

    elif nivel_servicio >= 0.95:

        z_score = 1.645

    elif nivel_servicio >= 0.90:

        z_score = 1.28

    else:

        z_score = 1.0


    # Stock de seguridad = Z * σ

    stock_seguridad = z_score * desviacion_std


    # Demanda máxima (percentil 95)

    demanda_max = demanda_esperada + stock_seguridad


    return {

        'stock_seguridad': max(0, stock_seguridad),

        'demanda_esperada': max(0, demanda_esperada),

        'demanda_max': max(0, demanda_max)

    }


# ============================================================================

# FUNCIÓN: GENERAR RECOMENDACIÓN DE ACCIÓN

# ============================================================================

def generar_recomendacion_accion(prob_no_venta, prob_venta_baja, prob_venta_alta,

                                 stock_actual=0):

    """

    Genera una recomendación de acción basada en probabilidades.


    Returns:

    --------

    str: 'COMPRAR URGENTE', 'COMPRAR', 'MANTENER', 'NO COMPRAR'

    """

    # Caso 1: Alta probabilidad de no venta

    if prob_no_venta > 0.6:

        if stock_actual > 0:

            return 'NO COMPRAR - Liquidar stock'

        else:

            return 'NO COMPRAR'


    # Caso 2: Alta probabilidad de venta alta

    if prob_venta_alta > 0.5:

        return 'COMPRAR URGENTE'


    # Caso 3: Probabilidad moderada de venta

    if prob_venta_baja > 0.3 or prob_venta_alta > 0.2:

        return 'COMPRAR'


    # Caso 4: Incertidumbre

    if stock_actual > 0:

        return 'MANTENER'

    else:

        return 'COMPRAR CON CAUTELA'


# ============================================================================

# PASO 1: OBTENER LISTA DE PRODUCTOS CLASE A

# ============================================================================

print("📦 PASO 1: Obteniendo productos de Clase A...")


productos_clase_a = series_completas_con_kmeans[['producto', 'subclase_kmeans']].drop_duplicates()

total_productos = len(productos_clase_a)


print(f"✅ {total_productos} productos de Clase A identificados")

print(f"\nDistribución por segmento:")

for segmento, count in productos_clase_a['subclase_kmeans'].value_counts().items():

    print(f"  • {segmento}: {count} productos")


# ============================================================================

# PASO 2: ITERAR Y GENERAR PREDICCIONES

# ============================================================================

print(f"\n📊 PASO 2: Generando predicciones para {total_productos} productos...")

print("(Esto puede tomar varios minutos)\n")


lista_planificacion = []

errores = []


# Usar tqdm para barra de progreso

for idx, row in tqdm(productos_clase_a.iterrows(), total=total_productos, desc="Procesando"):

    producto_actual = row['producto']

    segmento_actual = row['subclase_kmeans']


    try:

        # ====================================================================

        # 2.1. Obtener historial del producto

        # ====================================================================

        df_historial = series_completas_con_kmeans[

            series_completas_con_kmeans['producto'] == producto_actual

        ].copy()


        if len(df_historial) == 0:

            errores.append(f"Sin historial: {producto_actual}")

            continue


        df_historial['fecha'] = pd.to_datetime(df_historial['fecha'])


        # ====================================================================

        # 2.2. Crear fila futura para predicción

        # ====================================================================

        fecha_ultima = df_historial['fecha'].max()

        fecha_prediccion = (fecha_ultima + relativedelta(months=1)).replace(day=1)


        df_futuro = pd.DataFrame([{

            'producto': producto_actual,

            'fecha': fecha_prediccion,

            'cantidad_vendida': 0,  # Placeholder

            'venta_bs': 0,

            'num_transacciones': 0,

            'subclase_kmeans': segmento_actual

        }])


        df_combined = pd.concat([df_historial, df_futuro], ignore_index=True)


        # ====================================================================

        # 2.3. Generar features (usando función de Celda 10.5)

        # ====================================================================

        df_features_full, feature_cols, _ = preparar_datos_doble_clasificador(df_combined)


        if df_features_full.empty:

            errores.append(f"Features vacías: {producto_actual}")

            continue


        # Extraer solo la última fila (predicción)

        df_features_pred = df_features_full.iloc[[-1]]


        # ====================================================================

        # 2.4. Obtener predicción (usando función de Celda 12)

        # ====================================================================

        resultado_pred = predecir_producto(

            df_features_pred,

            segmento_actual,


        )


        if resultado_pred is None:

            errores.append(f"Predicción falló: {producto_actual}")

            continue


        # ====================================================================

        # 2.5. Calcular stock de seguridad

        # ====================================================================

        stock_info = calcular_stock_seguridad_probabilistico(

            prob_venta_alta=resultado_pred['P(Venta Alta)'],

            prob_venta_baja=resultado_pred['P(Venta Baja)'],

            limite_baja_alta=resultado_pred['limite_baja_alta'],

            nivel_servicio=0.95

        )


        # ====================================================================

        # 2.6. Generar recomendación de acción

        # ====================================================================

        # Nota: Aquí asumo stock_actual=0. Si tienes datos reales de inventario,

        # deberías cargarlos y pasarlos a la función.

        accion_recomendada = generar_recomendacion_accion(

            prob_no_venta=resultado_pred['P(No Venta)'],

            prob_venta_baja=resultado_pred['P(Venta Baja)'],

            prob_venta_alta=resultado_pred['P(Venta Alta)'],

            stock_actual=0  # Cambiar si tienes datos de inventario

        )


        # ====================================================================

        # 2.7. Calcular métricas adicionales

        # ====================================================================

        # Venta histórica promedio (últimos 6 meses)

        venta_historica_promedio = df_historial.tail(6)['cantidad_vendida'].mean()


        # Desviación estándar histórica

        venta_historica_std = df_historial.tail(6)['cantidad_vendida'].std()


        # ====================================================================

        # 2.8. Guardar resultados

        # ====================================================================

        lista_planificacion.append({

            # Identificación

            'producto': producto_actual,

            'segmento': segmento_actual,

            'fecha_prediccion': fecha_prediccion.strftime('%Y-%m-%d'),


            # Probabilidades

            'prob_no_venta': resultado_pred['P(No Venta)'],

            'prob_venta_baja': resultado_pred['P(Venta Baja)'],

            'prob_venta_alta': resultado_pred['P(Venta Alta)'],


            # Demanda

            'demanda_esperada': stock_info['demanda_esperada'],

            'demanda_maxima': stock_info['demanda_max'],

            'limite_baja_alta': resultado_pred['limite_baja_alta'],


            # Stock

            'stock_actual': 0,  # Cambiar si tienes datos reales

            'stock_seguridad_sugerido': stock_info['stock_seguridad'],

            'punto_reorden': stock_info['demanda_esperada'] + stock_info['stock_seguridad'],


            # Histórico

            'venta_promedio_6m': venta_historica_promedio,

            'venta_std_6m': venta_historica_std,


            # Recomendación

            'accion_recomendada': accion_recomendada,


            # Metadata

            'timestamp_generacion': datetime.now().isoformat()

        })


    except Exception as e:

        errores.append(f"Error en {producto_actual}: {str(e)}")

        continue


# ============================================================================

# PASO 3: CREAR DATAFRAME Y GUARDAR

# ============================================================================

print(f"\n💾 PASO 3: Creando archivo de planificación...")


if not lista_planificacion:

    print("❌ ERROR: No se generaron predicciones. Revisa los errores.")

    if errores:

        print("\nErrores encontrados:")

        for error in errores[:10]:  # Mostrar primeros 10

            print(f"  • {error}")

else:

    df_planificacion = pd.DataFrame(lista_planificacion)


    # Ordenar por probabilidad de venta alta (descendente)

    df_planificacion = df_planificacion.sort_values('prob_venta_alta', ascending=False)


    # Guardar archivo

    archivo_salida = 'planificacion_demanda.csv'

    df_planificacion.to_csv(archivo_salida, index=False)


    print(f"✅ Archivo '{archivo_salida}' creado exitosamente")

    print(f"   • Total de productos: {len(df_planificacion)}")

    print(f"   • Columnas: {len(df_planificacion.columns)}")


    # ========================================================================

    # PASO 4: GENERAR RESUMEN EJECUTIVO

    # ========================================================================

    print(f"\n📊 PASO 4: Resumen Ejecutivo de Planificación")

    print("="*80)


    # Resumen por acción recomendada

    print("\n🎯 Distribución de Acciones Recomendadas:")

    resumen_acciones = df_planificacion['accion_recomendada'].value_counts()

    for accion, count in resumen_acciones.items():

        pct = (count / len(df_planificacion)) * 100

        print(f"  • {accion}: {count} productos ({pct:.1f}%)")


    # Resumen por segmento

    print("\n🏷️  Distribución por Segmento:")

    resumen_segmentos = df_planificacion.groupby('segmento').agg({

        'demanda_esperada': 'sum',

        'stock_seguridad_sugerido': 'sum',

        'producto': 'count'

    }).round(2)

    resumen_segmentos.columns = ['Demanda Total', 'Stock Seguridad Total', 'N° Productos']

    print(resumen_segmentos.to_string())


    # Top 10 productos críticos (mayor prob_venta_alta)

    print("\n🔥 Top 10 Productos Prioritarios (Mayor Probabilidad Venta Alta):")

    top_10 = df_planificacion.nlargest(10, 'prob_venta_alta')[

        ['producto', 'segmento', 'prob_venta_alta', 'demanda_esperada', 'accion_recomendada']

    ]

    print(top_10.to_string(index=False))


    # Productos con baja probabilidad de venta (candidatos a liquidación)

    print("\n⚠️  Productos con Alta Probabilidad de NO Venta (>60%):")

    baja_demanda = df_planificacion[df_planificacion['prob_no_venta'] > 0.6]

    if len(baja_demanda) > 0:

        print(f"   • Total: {len(baja_demanda)} productos")

        print(baja_demanda[['producto', 'prob_no_venta', 'accion_recomendada']].head(5).to_string(index=False))

    else:

        print("   • Ninguno (¡excelente!)")


    # ========================================================================

    # PASO 5: GUARDAR RESUMEN

    # ========================================================================

    resumen_dict = {

        'fecha_generacion': datetime.now().isoformat(),

        'total_productos': len(df_planificacion),

        'productos_comprar_urgente': int((df_planificacion['accion_recomendada'] == 'COMPRAR URGENTE').sum()),

        'productos_comprar': int((df_planificacion['accion_recomendada'] == 'COMPRAR').sum()),

        'productos_mantener': int((df_planificacion['accion_recomendada'] == 'MANTENER').sum()),

        'productos_no_comprar': int((df_planificacion['accion_recomendada'].str.contains('NO COMPRAR')).sum()),

        'demanda_total_esperada': float(df_planificacion['demanda_esperada'].sum()),

        'stock_seguridad_total': float(df_planificacion['stock_seguridad_sugerido'].sum())

    }


    import json

    with open('resumen_planificacion.json', 'w') as f:

        json.dump(resumen_dict, f, indent=4)


    print(f"\n✅ Resumen guardado en 'resumen_planificacion.json'")


# ============================================================================

# REPORTE DE ERRORES

# ============================================================================

if errores:

    print(f"\n⚠️  Se encontraron {len(errores)} errores durante el procesamiento:")

    for error in errores[:10]:

        print(f"  • {error}")


    if len(errores) > 10:

        print(f"  ... y {len(errores) - 10} más")


    # Guardar errores

    with open('errores_planificacion.txt', 'w') as f:

        for error in errores:

            f.write(f"{error}\n")

    print("  Errores completos guardados en 'errores_planificacion.txt'")


# ============================================================================

# FINALIZACIÓN

# ============================================================================

print("\n" + "="*80)

print("✅ CELDA 13 COMPLETADA")

print("="*80)

print(f"""

📁 Archivos generados:

  • planificacion_demanda.csv        - Dataset completo con predicciones

  • resumen_planificacion.json       - Resumen ejecutivo en JSON

  • errores_planificacion.txt        - Log de errores (si hubo)


📊 Variables creadas:

  • df_planificacion                 - DataFrame con toda la planificación

  • lista_planificacion              - Lista raw de resultados


🚀 Siguiente paso:

  • Usa 'planificacion_demanda.csv' en la Pestaña 2 del dashboard

  • O impórtalo en tu sistema ERP/WMS

""")
