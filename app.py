import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path

# =====================================================
# CONFIGURACION GENERAL
# =====================================================

st.set_page_config(
    page_title="Analisis Residuos No Peligrosos Ultimos 7 Meses",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# RUTAS DEL PROYECTO
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

archivo_excel = (
    BASE_DIR
    / "ANALISIS RESIDUOS NO PELIGROSOS ULTIMOS 7 MESES.xlsx"
)

logo_superior = BASE_DIR / "logo1.png"
logo_sello = BASE_DIR / "logoredondo.png"

# =====================================================
# FUNCIONES PARA BUSCAR Y CARGAR IMAGENES
# =====================================================

def buscar_imagen(nombre_base):
    """
    Busca una imagen en la misma carpeta donde esta app.py.

    Reconoce variantes como:
    selfie.jpeg
    selfie.jpg
    selfie.PNG
    Selfie nueva.jpeg
    """

    extensiones_validas = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }

    for ruta in BASE_DIR.iterdir():
        if not ruta.is_file():
            continue

        nombre_archivo = ruta.stem.lower().strip()
        extension = ruta.suffix.lower().strip()

        if (
            nombre_archivo.startswith(
                nombre_base.lower()
            )
            and extension in extensiones_validas
        ):
            return ruta

    return None


def imagen_base64(ruta):
    """
    Convierte una imagen a Base64 para insertarla dentro del HTML.
    """

    if ruta and ruta.exists():
        with open(ruta, "rb") as imagen:
            return base64.b64encode(
                imagen.read()
            ).decode()

    return None


def obtener_mime(ruta):
    """
    Detecta el tipo de imagen para mostrarla correctamente.
    """

    if not ruta:
        return "image/jpeg"

    extension = ruta.suffix.lower()

    if extension == ".png":
        return "image/png"

    if extension == ".webp":
        return "image/webp"

    return "image/jpeg"


# =====================================================
# CARGAR IMAGENES
# =====================================================

ruta_selfie = buscar_imagen(
    "selfie"
)

selfie_base64 = imagen_base64(
    ruta_selfie
)

selfie_mime = obtener_mime(
    ruta_selfie
)

sello_base64 = imagen_base64(
    logo_sello
)

# =====================================================
# SELLO DE AGUA
# =====================================================

css_sello = ""

if sello_base64:
    css_sello = f"""
    .stApp::before {{
        content: "";
        position: fixed;
        top: 55%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 620px;
        height: 620px;
        background-image:
            url("data:image/png;base64,{sello_base64}");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.035;
        z-index: 0;
        pointer-events: none;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
    }}
    """

# =====================================================
# ESTILO VISUAL
# =====================================================

st.markdown(
    f"""
    <style>

        /* =============================================
           OCULTAR BARRA SUPERIOR DE STREAMLIT
        ============================================= */

        header[data-testid="stHeader"] {{
            display: none !important;
        }}

        div[data-testid="stToolbar"] {{
            display: none !important;
        }}

        div[data-testid="stDecoration"] {{
            display: none !important;
        }}

        div[data-testid="stStatusWidget"] {{
            display: none !important;
        }}

        button[data-testid="stBaseButton-headerNoPadding"] {{
            display: none !important;
        }}

        #MainMenu {{
            visibility: hidden !important;
        }}

        footer {{
            visibility: hidden !important;
        }}

        /* =============================================
           OCULTAR MENU LATERAL
        ============================================= */

        section[data-testid="stSidebar"] {{
            display: none !important;
        }}

        button[data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        div[data-testid="collapsedControl"] {{
            display: none !important;
        }}

        /* =============================================
           FONDO GENERAL
        ============================================= */

        .stApp {{
            background-color: #0f172a;
            color: #ffffff;
        }}

        {css_sello}

        html,
        body {{
            color: #ffffff;
        }}

        .block-container {{
            padding-top: 1.3rem;
            padding-bottom: 1.5rem;
        }}

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            color: #ffffff !important;
            font-weight: 800 !important;
        }}

        /* =============================================
           FOTO SUPERIOR CENTRADA
        ============================================= */

        .login-photo-wrapper {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 175px;
            height: 175px;
            margin: 28px auto 18px auto;
            border-radius: 50%;
            overflow: hidden;
            border: 4px solid #f59e0b;
            background-color: #d1d5db;
            box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.42);
        }}

        .login-photo {{
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
            object-position: center 46%;
            transform: scale(1.34);
            transform-origin: center center;
            background-color: #d1d5db;
        }}

        /* =============================================
           PANTALLA DE ACCESO
        ============================================= */

        .login-title {{
            text-align: center;
            color: #f8fafc;
            font-size: 42px;
            font-weight: 900;
            margin-top: 6px;
            margin-bottom: 8px;
        }}

        .login-subtitle {{
            text-align: center;
            color: #cbd5e1;
            font-size: 17px;
            margin-bottom: 25px;
        }}

        .login-footer {{
            text-align: center;
            margin-top: 34px;
            padding-top: 18px;
            border-top: 1px solid rgba(148, 163, 184, 0.30);
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
        }}

        .login-footer strong {{
            color: #e2e8f0;
            font-size: 14px;
        }}

        div[data-testid="stTextInput"] label {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stTextInput"] input {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            border-radius: 8px !important;
        }}

        div[data-testid="stButton"] > button[kind="primary"] {{
            background-color: #ef4444 !important;
            border: none !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            font-weight: 800 !important;
        }}

        div[data-testid="stButton"] > button[kind="primary"]:hover {{
            background-color: #dc2626 !important;
            color: #ffffff !important;
        }}

        /* =============================================
           AJUSTE PARA CELULARES
        ============================================= */

        @media (max-width: 900px) {{
            .login-photo-wrapper {{
                width: 145px;
                height: 145px;
                margin-top: 20px;
            }}

            .login-photo {{
                object-position: center 46%;
                transform: scale(1.34);
            }}

            .login-title {{
                font-size: 34px;
            }}

            .login-subtitle {{
                font-size: 15px;
            }}
        }}

        /* =============================================
           ENCABEZADO PRINCIPAL
        ============================================= */

        .titulo-principal {{
            font-size: 46px;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 12px;
            line-height: 1.15;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.45);
        }}

        .subtitulo {{
            font-size: 21px;
            color: #e2e8f0;
            margin-bottom: 35px;
            line-height: 1.45;
            max-width: 1450px;
            font-weight: 500;
        }}

        /* =============================================
           TITULO DE FILTROS
        ============================================= */

        .seccion-filtros {{
            border-left: 8px solid #f59e0b;
            padding-left: 20px;
            font-size: 34px;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 25px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.45);
        }}

        label {{
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 17px !important;
        }}

        /* =============================================
           CAJAS DE SELECCION
        ============================================= */

        div[data-baseweb="select"] > div {{
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
        }}

        div[data-baseweb="select"] > div > div {{
            color: #0f172a !important;
        }}

        div[data-baseweb="select"] > div > div * {{
            color: #0f172a !important;
        }}

        div[data-baseweb="select"] span {{
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        div[data-baseweb="select"] input {{
            color: #0f172a !important;
            background-color: #f8fafc !important;
            font-weight: 600 !important;
        }}

        div[data-baseweb="select"] input::placeholder {{
            color: #64748b !important;
            opacity: 1 !important;
        }}

        div[data-baseweb="select"] svg {{
            fill: #0f172a !important;
            color: #0f172a !important;
        }}

        /* =============================================
           ELEMENTOS DEL MULTISELECT
        ============================================= */

        span[data-baseweb="tag"] {{
            background-color: #ef4444 !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border-radius: 8px !important;
        }}

        span[data-baseweb="tag"] span {{
            color: #ffffff !important;
        }}

        span[data-baseweb="tag"] svg {{
            fill: #ffffff !important;
            color: #ffffff !important;
        }}

        /* =============================================
           OPCIONES DESPLEGABLES
        ============================================= */

        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        div[role="listbox"],
        ul[role="listbox"] {{
            background-color: #f8fafc !important;
        }}

        div[role="option"],
        li[role="option"] {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        div[role="option"] *,
        li[role="option"] * {{
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        div[role="option"]:hover,
        li[role="option"]:hover {{
            background-color: #e2e8f0 !important;
        }}

        /* =============================================
           CAMPOS NUMERICOS
        ============================================= */

        input {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        /* =============================================
           INDICADORES
        ============================================= */

        div[data-testid="stMetric"] {{
            background-color: rgba(30, 41, 59, 0.96);
            padding: 24px;
            border-radius: 14px;
            border: 1px solid #475569;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
        }}

        div[data-testid="stMetricLabel"] {{
            color: #e2e8f0 !important;
            font-size: 18px !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: #ffffff !important;
            font-size: 32px !important;
            font-weight: 900 !important;
        }}

        /* =============================================
           TABLAS Y SEPARADORES
        ============================================= */

        .stDataFrame {{
            background-color: #ffffff;
            border-radius: 10px;
        }}

        hr {{
            border-color: #334155 !important;
        }}

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# ACCESO RESTRINGIDO
# =====================================================

def validar_acceso():
    """
    Permite visualizar el dashboard solamente despues
    de validar el usuario y la contrasena registrados
    dentro de Streamlit Secrets.
    """

    if st.session_state.get(
        "autenticado",
        False
    ):
        return True

    columna_izquierda, columna_login, columna_derecha = st.columns(
        [1, 1.2, 1]
    )

    with columna_login:

        # -----------------------------------------------
        # FOTOGRAFIA SUPERIOR
        # -----------------------------------------------

        if selfie_base64:
            st.markdown(
                f"""
                <div class="login-photo-wrapper">
                    <img
                        src="data:{selfie_mime};base64,{selfie_base64}"
                        class="login-photo"
                        alt="Fotografia"
                    >
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.warning(
                "No se encontro una fotografia cuyo nombre comience por "
                "'selfie' dentro de la misma carpeta de app.py."
            )

        # -----------------------------------------------
        # TITULO DEL ACCESO
        # -----------------------------------------------

        st.markdown(
            """
            <div class="login-title">
                🔐 Acceso restringido
            </div>

            <div class="login-subtitle">
                Ingresa tu usuario y contrasena para visualizar el panel.
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------------------
        # FORMULARIO DE ACCESO
        # -----------------------------------------------

        usuario = st.text_input(
            "Usuario",
            key="login_usuario"
        )

        contrasena = st.text_input(
            "Contrasena",
            type="password",
            key="login_contrasena"
        )

        boton_ingresar = st.button(
            "Ingresar",
            type="primary",
            use_container_width=True
        )

        if boton_ingresar:
            try:
                usuarios_autorizados = st.secrets[
                    "usuarios"
                ]

                if (
                    usuario in usuarios_autorizados
                    and contrasena
                    == usuarios_autorizados[usuario]
                ):
                    st.session_state[
                        "autenticado"
                    ] = True

                    st.session_state[
                        "usuario"
                    ] = usuario

                    st.rerun()

                else:
                    st.error(
                        "Usuario o contrasena incorrectos."
                    )

            except Exception:
                st.error(
                    "No se encontraron usuarios configurados en Secrets."
                )

        # -----------------------------------------------
        # TEXTO INFERIOR CENTRADO
        # -----------------------------------------------

        st.markdown(
            """
            <div class="login-footer">
                <strong>
                    Panel desarrollado por Ricardo Grez
                </strong>
                <br>
                Administrador de Contrato | SAIVAM
                <br>
                Acceso restringido para usuarios autorizados
            </div>
            """,
            unsafe_allow_html=True
        )

    return False


if not validar_acceso():
    st.stop()

# =====================================================
# CARGAR Y TRANSFORMAR DATOS
# =====================================================

@st.cache_data
def cargar_datos(ruta_excel):
    df = pd.read_excel(
        ruta_excel,
        sheet_name="Hoja1",
        header=None
    )

    df = df.dropna(
        how="all"
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    registros = []
    columna_fecha = None

    for col in range(
        len(df.columns)
    ):
        posibles_fechas = pd.to_datetime(
            df.iloc[2:, col],
            errors="coerce"
        )

        if posibles_fechas.notna().sum() >= 2:
            columna_fecha = col
            break

    if columna_fecha is None:
        raise ValueError(
            "No se encontro la columna de fechas en la planilla."
        )

    meses_espanol = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    for fila in range(
        2,
        len(df)
    ):
        fecha = pd.to_datetime(
            df.iloc[
                fila,
                columna_fecha
            ],
            errors="coerce"
        )

        if pd.isna(
            fecha
        ):
            continue

        anio = fecha.year
        mes_numero = fecha.month
        mes_nombre = meses_espanol[
            mes_numero
        ]

        periodo = (
            f"{mes_nombre} {anio}"
        )

        residuo_actual = None

        for col in range(
            columna_fecha + 1,
            len(df.columns)
        ):
            nombre_residuo = df.iloc[
                0,
                col
            ]

            concepto = df.iloc[
                1,
                col
            ]

            if pd.notna(
                nombre_residuo
            ):
                residuo_actual = str(
                    nombre_residuo
                ).strip()

            if (
                pd.isna(concepto)
                or residuo_actual is None
            ):
                continue

            concepto = str(
                concepto
            ).strip()

            if concepto == "Traslados":
                traslados = pd.to_numeric(
                    df.iloc[
                        fila,
                        col
                    ],
                    errors="coerce"
                )

                camion_carro = pd.to_numeric(
                    df.iloc[
                        fila,
                        col + 1
                    ],
                    errors="coerce"
                )

                peso_promedio = pd.to_numeric(
                    df.iloc[
                        fila,
                        col + 2
                    ],
                    errors="coerce"
                )

                traslados = (
                    0
                    if pd.isna(
                        traslados
                    )
                    else traslados
                )

                camion_carro = (
                    0
                    if pd.isna(
                        camion_carro
                    )
                    else camion_carro
                )

                peso_promedio = (
                    0
                    if pd.isna(
                        peso_promedio
                    )
                    else peso_promedio
                )

                toneladas = (
                    traslados
                    * peso_promedio
                ) / 1000

                registros.append({
                    "Fecha": fecha,
                    "Año": anio,
                    "Mes numero": mes_numero,
                    "Mes": mes_nombre,
                    "Periodo": periodo,
                    "Residuo": residuo_actual,
                    "Traslados": traslados,
                    "Salidas camion y carro":
                        camion_carro,
                    "Peso promedio por traslado kg":
                        peso_promedio,
                    "Toneladas estimadas":
                        toneladas
                })

    return pd.DataFrame(
        registros
    )

# =====================================================
# ENCABEZADO DEL PANEL
# =====================================================

col_titulo, col_logo = st.columns(
    [5, 1]
)

with col_titulo:
    st.markdown(
        """
        <div class="titulo-principal">
            ♻️ Analisis Residuos No Peligrosos Ultimos 7 Meses
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitulo">
            El objetivo de este analisis es entregar una vision mas clara
            del comportamiento operacional de los principales residuos
            gestionados, identificando la cantidad de traslados realizados,
            el uso de camion y carro, y las toneladas estimadas movilizadas
            por cada tipo de residuo.
        </div>
        """,
        unsafe_allow_html=True
    )

with col_logo:
    if logo_superior.exists():
        st.image(
            str(
                logo_superior
            ),
            width=190
        )

# =====================================================
# DASHBOARD PRINCIPAL
# =====================================================

try:
    df = cargar_datos(
        archivo_excel
    )

    # =================================================
    # FILTROS
    # =================================================

    st.markdown(
        """
        <div class="seccion-filtros">
            🔎 Filtros de analisis
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:
        filtro_anio = st.multiselect(
            "Año",
            sorted(
                df["Año"]
                .unique()
            ),
            default=sorted(
                df["Año"]
                .unique()
            )
        )

    with col2:
        meses_ordenados = (
            df[
                [
                    "Mes numero",
                    "Mes"
                ]
            ]
            .drop_duplicates()
            .sort_values(
                "Mes numero"
            )[
                "Mes"
            ]
            .tolist()
        )

        filtro_mes = st.multiselect(
            "Mes",
            meses_ordenados,
            default=meses_ordenados
        )

    with col3:
        filtro_residuo = st.multiselect(
            "Residuo / disposicion",
            sorted(
                df["Residuo"]
                .unique()
            ),
            default=sorted(
                df["Residuo"]
                .unique()
            )
        )

    col4, col5 = st.columns(
        2
    )

    with col4:
        filtro_tipo_salida = st.selectbox(
            "Tipo de analisis",
            [
                "Todos los traslados",
                "Solo salidas con camion y carro",
                "Solo salidas sin camion y carro"
            ]
        )

    with col5:
        filtro_minimo_traslados = st.number_input(
            "Minimo de traslados",
            min_value=0,
            value=0,
            step=1
        )

    # =================================================
    # APLICAR FILTROS
    # =================================================

    df_filtrado = df[
        (
            df["Año"]
            .isin(
                filtro_anio
            )
        )
        &
        (
            df["Mes"]
            .isin(
                filtro_mes
            )
        )
        &
        (
            df["Residuo"]
            .isin(
                filtro_residuo
            )
        )
        &
        (
            df["Traslados"]
            >= filtro_minimo_traslados
        )
    ]

    if (
        filtro_tipo_salida
        == "Solo salidas con camion y carro"
    ):
        df_filtrado = df_filtrado[
            df_filtrado[
                "Salidas camion y carro"
            ] > 0
        ]

    elif (
        filtro_tipo_salida
        == "Solo salidas sin camion y carro"
    ):
        df_filtrado = df_filtrado[
            df_filtrado[
                "Salidas camion y carro"
            ] == 0
        ]

    # =================================================
    # INDICADORES PRINCIPALES
    # =================================================

    st.markdown(
        "---"
    )

    st.subheader(
        "📌 Indicadores principales"
    )

    total_traslados = (
        df_filtrado[
            "Traslados"
        ]
        .sum()
    )

    total_camion_carro = (
        df_filtrado[
            "Salidas camion y carro"
        ]
        .sum()
    )

    total_toneladas = (
        df_filtrado[
            "Toneladas estimadas"
        ]
        .sum()
    )

    promedio_mensual_traslados = (
        df_filtrado
        .groupby(
            "Periodo"
        )[
            "Traslados"
        ]
        .sum()
        .mean()
        if not df_filtrado.empty
        else 0
    )

    promedio_mensual_camion_carro = (
        df_filtrado
        .groupby(
            "Periodo"
        )[
            "Salidas camion y carro"
        ]
        .sum()
        .mean()
        if not df_filtrado.empty
        else 0
    )

    promedio_mensual_toneladas = (
        df_filtrado
        .groupby(
            "Periodo"
        )[
            "Toneladas estimadas"
        ]
        .sum()
        .mean()
        if not df_filtrado.empty
        else 0
    )

    promedio_toneladas_traslado = (
        total_toneladas
        / total_traslados
        if total_traslados > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(
        4
    )

    col1.metric(
        "Total traslados",
        f"{total_traslados:,.0f}"
    )

    col2.metric(
        "Promedio mensual traslados",
        f"{promedio_mensual_traslados:,.2f}"
    )

    col3.metric(
        "Salidas camion y carro",
        f"{total_camion_carro:,.0f}"
    )

    col4.metric(
        "Toneladas por traslado",
        f"{promedio_toneladas_traslado:,.2f}"
    )

    col5, col6, col7 = st.columns(
        3
    )

    col5.metric(
        "Toneladas estimadas",
        f"{total_toneladas:,.2f}"
    )

    col6.metric(
        "Promedio mensual camion y carro",
        f"{promedio_mensual_camion_carro:,.2f}"
    )

    col7.metric(
        "Promedio mensual toneladas",
        f"{promedio_mensual_toneladas:,.2f}"
    )

    # =================================================
    # RESUMEN CONSOLIDADO
    # =================================================

    st.subheader(
        "📊 Resumen consolidado por residuo / disposicion"
    )

    resumen = (
        df_filtrado
        .groupby(
            "Residuo"
        )
        .agg(
            Total_traslados=(
                "Traslados",
                "sum"
            ),
            Total_salidas_camion_y_carro=(
                "Salidas camion y carro",
                "sum"
            ),
            Total_toneladas_estimadas=(
                "Toneladas estimadas",
                "sum"
            ),
            Promedio_mensual_traslados=(
                "Traslados",
                "mean"
            ),
            Promedio_mensual_camion_y_carro=(
                "Salidas camion y carro",
                "mean"
            ),
            Promedio_peso_por_traslado_kg=(
                "Peso promedio por traslado kg",
                "mean"
            )
        )
        .reset_index()
    )

    resumen[
        "Promedio toneladas por traslado"
    ] = (
        resumen[
            "Total_toneladas_estimadas"
        ]
        /
        resumen[
            "Total_traslados"
        ]
    ).fillna(
        0
    )

    resumen = (
        resumen
        .rename(
            columns={
                "Residuo":
                    "Residuo / disposicion",
                "Total_traslados":
                    "Total traslados",
                "Total_salidas_camion_y_carro":
                    "Total salidas camion y carro",
                "Total_toneladas_estimadas":
                    "Total toneladas estimadas",
                "Promedio_mensual_traslados":
                    "Promedio mensual traslados",
                "Promedio_mensual_camion_y_carro":
                    "Promedio mensual camion y carro",
                "Promedio_peso_por_traslado_kg":
                    "Promedio peso por traslado kg"
            }
        )
        .round(
            2
        )
    )

    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # PROMEDIOS MENSUALES POR DISPOSICION
    # =================================================

    st.subheader(
        "📈 Promedio mensual por residuo / disposicion"
    )

    promedio_disposicion = (
        df_filtrado
        .groupby(
            "Residuo"
        )
        .agg(
            Promedio_mensual_traslados=(
                "Traslados",
                "mean"
            ),
            Promedio_mensual_camion_y_carro=(
                "Salidas camion y carro",
                "mean"
            ),
            Promedio_mensual_toneladas=(
                "Toneladas estimadas",
                "mean"
            )
        )
        .reset_index()
        .round(
            2
        )
        .rename(
            columns={
                "Residuo":
                    "Residuo / disposicion",
                "Promedio_mensual_traslados":
                    "Promedio mensual traslados",
                "Promedio_mensual_camion_y_carro":
                    "Promedio mensual camion y carro",
                "Promedio_mensual_toneladas":
                    "Promedio mensual toneladas"
            }
        )
    )

    col_g1, col_g2 = st.columns(
        2
    )

    with col_g1:
        fig_torta = px.pie(
            promedio_disposicion,
            names="Residuo / disposicion",
            values="Promedio mensual traslados",
            hole=0.45,
            title=(
                "Distribucion del promedio mensual "
                "de traslados"
            )
        )

        fig_torta.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_torta.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            legend=dict(
                font=dict(
                    color="#ffffff",
                    size=13
                ),
                orientation="h",
                yanchor="bottom",
                y=-0.30,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(
            fig_torta,
            use_container_width=True
        )

    with col_g2:
        fig_barras_promedio = px.bar(
            promedio_disposicion
            .sort_values(
                "Promedio mensual traslados",
                ascending=False
            ),
            x="Residuo / disposicion",
            y="Promedio mensual traslados",
            text="Promedio mensual traslados",
            title=(
                "Promedio mensual de traslados "
                "por disposicion"
            )
        )

        fig_barras_promedio.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_barras_promedio.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            xaxis_title="Residuo / disposicion",
            yaxis_title="Promedio mensual de traslados"
        )

        st.plotly_chart(
            fig_barras_promedio,
            use_container_width=True
        )

    col_g3, col_g4 = st.columns(
        2
    )

    with col_g3:
        fig_camion = px.bar(
            promedio_disposicion
            .sort_values(
                "Promedio mensual camion y carro",
                ascending=False
            ),
            x="Residuo / disposicion",
            y="Promedio mensual camion y carro",
            text="Promedio mensual camion y carro",
            title=(
                "Promedio mensual de salidas "
                "con camion y carro"
            )
        )

        fig_camion.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_camion.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            xaxis_title="Residuo / disposicion",
            yaxis_title="Promedio mensual camion y carro"
        )

        st.plotly_chart(
            fig_camion,
            use_container_width=True
        )

    with col_g4:
        fig_toneladas = px.bar(
            promedio_disposicion
            .sort_values(
                "Promedio mensual toneladas",
                ascending=False
            ),
            x="Residuo / disposicion",
            y="Promedio mensual toneladas",
            text="Promedio mensual toneladas",
            title=(
                "Promedio mensual de toneladas "
                "estimadas"
            )
        )

        fig_toneladas.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_toneladas.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            xaxis_title="Residuo / disposicion",
            yaxis_title="Promedio mensual toneladas"
        )

        st.plotly_chart(
            fig_toneladas,
            use_container_width=True
        )

    # =================================================
    # RESUMEN MENSUAL
    # =================================================

    st.subheader(
        "📅 Resumen mensual"
    )

    resumen_mensual = (
        df_filtrado
        .groupby(
            [
                "Fecha",
                "Periodo"
            ]
        )
        .agg(
            Total_traslados=(
                "Traslados",
                "sum"
            ),
            Total_salidas_camion_y_carro=(
                "Salidas camion y carro",
                "sum"
            ),
            Total_toneladas_estimadas=(
                "Toneladas estimadas",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "Fecha"
        )
    )

    resumen_mensual_tabla = (
        resumen_mensual
        .drop(
            columns=[
                "Fecha"
            ]
        )
        .rename(
            columns={
                "Total_traslados":
                    "Total traslados",
                "Total_salidas_camion_y_carro":
                    "Total salidas camion y carro",
                "Total_toneladas_estimadas":
                    "Total toneladas estimadas"
            }
        )
        .round(
            2
        )
    )

    st.dataframe(
        resumen_mensual_tabla,
        use_container_width=True,
        hide_index=True
    )

    fig_linea = px.line(
        resumen_mensual,
        x="Periodo",
        y="Total_traslados",
        markers=True,
        title="Evolucion mensual de traslados"
    )

    fig_linea.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#ffffff",
            size=15
        ),
        title_font=dict(
            size=22,
            color="#ffffff"
        ),
        xaxis_title="Periodo",
        yaxis_title="Total traslados"
    )

    st.plotly_chart(
        fig_linea,
        use_container_width=True
    )

    # =================================================
    # PIE DE PAGINA
    # =================================================

    st.markdown(
        """
        <div style="
            text-align: center;
            margin-top: 55px;
            padding: 24px 12px 10px 12px;
            color: #cbd5e1;
            font-size: 15px;
            line-height: 1.65;
            border-top: 1px solid rgba(148, 163, 184, 0.25);
        ">
            <strong>
                Panel desarrollado por Ricardo Grez
            </strong>
            <br>
            Administrador de Contrato | SAIVAM
            <br>
            Version 1.0 | Ultima actualizacion: Mayo 2026
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# MANEJO DE ERRORES
# =====================================================

except FileNotFoundError:
    st.error(
        "No se encontro la planilla Excel."
    )

    st.write(
        "El archivo debe estar en la misma carpeta que app.py "
        "y llamarse exactamente:"
    )

    st.code(
        "ANALISIS RESIDUOS NO PELIGROSOS ULTIMOS 7 MESES.xlsx"
    )

except Exception as error:
    st.error(
        "Ocurrio un error al cargar el dashboard."
    )

    st.write(
        error
    )