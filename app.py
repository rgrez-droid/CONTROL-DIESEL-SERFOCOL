import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path


# =====================================================
# CONFIGURACION GENERAL
# =====================================================

st.set_page_config(
    page_title="Analisis Diesel SERFOCOL",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# RUTAS DEL PROYECTO
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

archivo_excel = BASE_DIR / "DIESEL SERFOCOL- V01.xlsx"


# =====================================================
# FUNCIONES PARA BUSCAR Y CARGAR IMAGENES
# =====================================================

def buscar_imagen(nombre_base):
    """
    Busca automaticamente una imagen dentro de la misma
    carpeta donde se encuentra app.py.

    Reconoce variantes como:
    selfie.jpeg
    selfie.jpg
    selfie.PNG
    selfie nueva.jpeg
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


def convertir_imagen_base64(ruta_imagen):
    """
    Convierte una imagen a Base64 para insertarla
    directamente dentro del HTML.
    """

    if ruta_imagen and ruta_imagen.exists():
        with open(
            ruta_imagen,
            "rb"
        ) as imagen:
            return base64.b64encode(
                imagen.read()
            ).decode()

    return None


def obtener_mime(ruta_imagen):
    """
    Detecta el formato de la imagen.
    """

    if not ruta_imagen:
        return "image/jpeg"

    extension = ruta_imagen.suffix.lower()

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

ruta_logo_superior = buscar_imagen(
    "logo1"
)

ruta_sello_agua = buscar_imagen(
    "logoredondo"
)

selfie_base64 = convertir_imagen_base64(
    ruta_selfie
)

logo_superior = convertir_imagen_base64(
    ruta_logo_superior
)

sello_agua = convertir_imagen_base64(
    ruta_sello_agua
)

selfie_mime = obtener_mime(
    ruta_selfie
)

logo_mime = obtener_mime(
    ruta_logo_superior
)

sello_mime = obtener_mime(
    ruta_sello_agua
)


# =====================================================
# ESTILO GENERAL DE STREAMLIT
# =====================================================

st.markdown(
    """
    <style>

        /* =============================================
           OCULTAR BARRA SUPERIOR DE STREAMLIT
        ============================================= */

        header[data-testid="stHeader"] {
            display: none !important;
        }

        div[data-testid="stToolbar"] {
            display: none !important;
        }

        div[data-testid="stDecoration"] {
            display: none !important;
        }

        div[data-testid="stStatusWidget"] {
            display: none !important;
        }

        button[data-testid="stBaseButton-headerNoPadding"] {
            display: none !important;
        }

        #MainMenu {
            visibility: hidden !important;
        }

        footer {
            visibility: hidden !important;
        }

        /* =============================================
           OCULTAR COMPLETAMENTE LA BARRA LATERAL
        ============================================= */

        section[data-testid="stSidebar"] {
            display: none !important;
        }

        button[data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        div[data-testid="collapsedControl"] {
            display: none !important;
        }

        /* =============================================
           FONDO GENERAL
        ============================================= */

        .stApp {
            background-color: #0f172a;
            color: #e5e7eb;
        }

        .main {
            background-color: #0f172a;
        }

        .block-container {
            position: relative;
            z-index: 2;
            padding-top: 1.3rem;
            padding-bottom: 1.5rem;
        }

        /* =============================================
           TITULOS DEL PANEL
        ============================================= */

        .titulo-principal {
            font-size: 42px;
            font-weight: 900;
            color: #f8fafc;
            margin-bottom: 8px;
            line-height: 1.15;
        }

        .subtitulo {
            font-size: 18px;
            color: #cbd5e1;
            margin-bottom: 25px;
            line-height: 1.4;
        }

        .section-title {
            font-size: 25px;
            font-weight: 800;
            color: #f8fafc;
            margin-top: 35px;
            margin-bottom: 15px;
            border-left: 6px solid #f59e0b;
            padding-left: 12px;
        }

        /* =============================================
           TARJETAS DE INDICADORES
        ============================================= */

        .card {
            background: linear-gradient(
                135deg,
                #1e293b,
                #111827
            );
            padding: 22px;
            border-radius: 18px;
            box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.45);
            text-align: center;
            border: 1px solid #334155;
            min-height: 118px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .card-title {
            font-size: 15px;
            color: #cbd5e1;
            font-weight: 600;
            line-height: 1.25;
        }

        .card-value {
            font-size: 31px;
            color: #f59e0b;
            font-weight: 900;
            margin-top: 8px;
        }

        /* =============================================
           TABLAS Y TEXTOS
        ============================================= */

        div[data-testid="stDataFrame"] {
            background-color: #1e293b;
            border-radius: 12px;
        }

        .stSelectbox label,
        .stMultiSelect label,
        .stDateInput label,
        .stNumberInput label,
        div[data-testid="stTextInput"] label {
            color: #e5e7eb !important;
            font-weight: 700 !important;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6,
        p,
        label {
            color: #e5e7eb;
        }

        /* =============================================
           FILTROS
        ============================================= */

        div[data-baseweb="select"] > div {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            border-radius: 10px !important;
            border: 1px solid #cbd5e1 !important;
        }

        div[data-baseweb="select"] span {
            color: #0f172a !important;
        }

        div[data-baseweb="select"] input {
            color: #0f172a !important;
            background-color: #f8fafc !important;
        }

        div[role="option"] {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }

        div[role="option"] * {
            color: #0f172a !important;
        }

        div[role="option"]:hover {
            background-color: #e2e8f0 !important;
        }

        input {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            border-radius: 8px !important;
        }

        /* =============================================
           LOGO SUPERIOR
        ============================================= */

        .logo-header {
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
            width: 100%;
            padding-top: 5px;
        }

        .logo-header img {
            width: 190px;
            max-width: 100%;
            height: auto;
            background: rgba(255, 255, 255, 0.95);
            padding: 6px;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.35);
        }

        /* =============================================
           SELLO DE AGUA
        ============================================= */

        .sello-agua {
            position: fixed;
            top: 52%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 0;
            opacity: 0.07;
            pointer-events: none;
        }

        .sello-agua img {
            width: 620px;
            max-width: 75vw;
            height: auto;
        }

        /* =============================================
           PIE DE PAGINA DEL PANEL
        ============================================= */

        .footer-panel {
            width: 100%;
            margin-top: 65px;
            padding: 24px 10px 12px 10px;
            border-top: 1px solid rgba(148, 163, 184, 0.28);
            text-align: center;
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.7;
        }

        .footer-panel strong {
            color: #e2e8f0;
            font-size: 15px;
        }

        /* =============================================
           FOTO SUPERIOR DE LA PANTALLA DE ACCESO
        ============================================= */

        .login-photo-wrapper {
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
        }

        .login-photo {
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
            object-position: center 46%;
            transform: scale(1.34);
            transform-origin: center center;
            background-color: #d1d5db;
        }

        /* =============================================
           PANTALLA DE ACCESO
        ============================================= */

        .login-title {
            text-align: center;
            color: #f8fafc;
            font-size: 42px;
            font-weight: 900;
            margin-top: 6px;
            margin-bottom: 8px;
        }

        .login-subtitle {
            text-align: center;
            color: #cbd5e1;
            font-size: 17px;
            margin-bottom: 25px;
        }

        .login-footer {
            text-align: center;
            margin-top: 34px;
            padding-top: 18px;
            border-top: 1px solid rgba(148, 163, 184, 0.30);
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
        }

        .login-footer strong {
            color: #e2e8f0;
            font-size: 14px;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #ef4444 !important;
            border: none !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            font-weight: 800 !important;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background-color: #dc2626 !important;
            color: #ffffff !important;
        }

        /* =============================================
           AJUSTES PARA CELULARES
        ============================================= */

        @media (max-width: 900px) {
            .login-photo-wrapper {
                width: 145px;
                height: 145px;
                margin-top: 20px;
            }

            .login-photo {
                object-position: center 46%;
                transform: scale(1.34);
            }

            .login-title {
                font-size: 34px;
            }

            .login-subtitle {
                font-size: 15px;
            }

            .titulo-principal {
                font-size: 34px;
            }
        }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# ACCESO RESTRINGIDO
# =====================================================

def validar_acceso():
    """
    Permite visualizar el panel solamente despues
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
                "No se encontro una fotografia cuyo nombre comience "
                "por 'selfie' dentro de la misma carpeta de app.py."
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
# SELLO DE AGUA
# =====================================================

if sello_agua:
    st.markdown(
        f"""
        <div class="sello-agua">
            <img
                src="data:{sello_mime};base64,{sello_agua}"
                alt="Sello de agua"
            >
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# ENCABEZADO DEL PANEL
# =====================================================

columna_titulo, columna_logo = st.columns(
    [5, 1.2]
)

with columna_titulo:
    st.markdown(
        """
        <div class="titulo-principal">
            ⛽ Control de Consumo de Diesel SERFOCOL
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitulo">
            Visualizacion consolidada para el seguimiento operacional del
            consumo de diesel por periodo, descripcion, equipo y operador.
        </div>
        """,
        unsafe_allow_html=True
    )

with columna_logo:
    if logo_superior:
        st.markdown(
            f"""
            <div class="logo-header">
                <img
                    src="data:{logo_mime};base64,{logo_superior}"
                    alt="Logo"
                >
            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# LECTURA Y ANALISIS DE LA PLANILLA
# =====================================================

try:

    # ---------------------------------------------------
    # LECTURA DEL ARCHIVO
    # ---------------------------------------------------

    df = pd.read_excel(
        archivo_excel,
        header=8,
        usecols="A:F"
    )

    # ---------------------------------------------------
    # LIMPIEZA GENERAL
    # ---------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    df = df.loc[
        :,
        ~df.columns.str.contains(
            "Unnamed"
        )
    ]

    df = df.dropna(
        how="all"
    )

    if "Lts" not in df.columns:
        st.error(
            "No se encontro la columna 'Lts'."
        )

        st.write(
            "Columnas detectadas:"
        )

        st.write(
            list(
                df.columns
            )
        )

        st.stop()

    if "Fechas" not in df.columns:
        st.error(
            "No se encontro la columna 'Fechas'."
        )

        st.write(
            "Columnas detectadas:"
        )

        st.write(
            list(
                df.columns
            )
        )

        st.stop()

    df = df.dropna(
        subset=[
            "Fechas",
            "Lts"
        ],
        how="all"
    )

    df["Lts"] = pd.to_numeric(
        df["Lts"],
        errors="coerce"
    )

    df = df[
        df["Lts"].notna()
    ]

    df = df[
        df["Lts"] > 0
    ]

    df["Fechas"] = pd.to_datetime(
        df["Fechas"],
        errors="coerce",
        dayfirst=True
    )

    df = df[
        df["Fechas"].notna()
    ]

    # ---------------------------------------------------
    # MESES EN ESPANOL
    # ---------------------------------------------------

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

    orden_meses = list(
        meses_espanol.values()
    )

    df["Año"] = (
        df["Fechas"]
        .dt
        .year
        .astype(int)
    )

    df["Mes"] = (
        df["Fechas"]
        .dt
        .month
    )

    df["Mes_Nombre"] = (
        df["Mes"]
        .map(
            meses_espanol
        )
    )

    df["Periodo"] = (
        df["Fechas"]
        .dt
        .strftime(
            "%Y-%m"
        )
    )

    df["Fecha"] = (
        df["Fechas"]
        .dt
        .strftime(
            "%d-%m-%Y"
        )
    )

    # ---------------------------------------------------
    # FILTROS VISIBLES
    # ---------------------------------------------------

    st.markdown(
        '<div class="section-title">🔎 Filtros de analisis</div>',
        unsafe_allow_html=True
    )

    df_filtrado = df.copy()

    columna_filtro_1, columna_filtro_2, columna_filtro_3 = st.columns(
        3
    )

    with columna_filtro_1:
        años_seleccionados = st.multiselect(
            "Año",
            sorted(
                df["Año"]
                .dropna()
                .unique()
            ),
            placeholder="Seleccionar año"
        )

        if años_seleccionados:
            df_filtrado = df_filtrado[
                df_filtrado["Año"]
                .isin(
                    años_seleccionados
                )
            ]

    with columna_filtro_2:
        meses_disponibles = [
            mes
            for mes in orden_meses
            if mes in df[
                "Mes_Nombre"
            ]
            .dropna()
            .unique()
        ]

        meses_seleccionados = st.multiselect(
            "Mes",
            meses_disponibles,
            placeholder="Seleccionar mes"
        )

        if meses_seleccionados:
            df_filtrado = df_filtrado[
                df_filtrado[
                    "Mes_Nombre"
                ]
                .isin(
                    meses_seleccionados
                )
            ]

    with columna_filtro_3:
        if "Descripción" in df.columns:
            descripciones_seleccionadas = st.multiselect(
                "Descripcion",
                sorted(
                    df[
                        "Descripción"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                ),
                placeholder="Seleccionar descripcion"
            )

            if descripciones_seleccionadas:
                df_filtrado = df_filtrado[
                    df_filtrado[
                        "Descripción"
                    ]
                    .isin(
                        descripciones_seleccionadas
                    )
                ]

    # ---------------------------------------------------
    # FILTRO POR RANGO DE FECHAS
    # ---------------------------------------------------

    st.markdown(
        '<div class="section-title">📅 Filtro por rango de fechas</div>',
        unsafe_allow_html=True
    )

    fecha_minima = (
        df["Fechas"]
        .min()
        .date()
    )

    fecha_maxima = (
        df["Fechas"]
        .max()
        .date()
    )

    rango_fechas = st.date_input(
        "Selecciona rango de fechas",
        value=(
            fecha_minima,
            fecha_maxima
        )
    )

    if len(
        rango_fechas
    ) == 2:
        fecha_inicio, fecha_fin = rango_fechas

        df_filtrado = df_filtrado[
            (
                df_filtrado[
                    "Fechas"
                ]
                .dt
                .date
                >= fecha_inicio
            )
            &
            (
                df_filtrado[
                    "Fechas"
                ]
                .dt
                .date
                <= fecha_fin
            )
        ]

    # ---------------------------------------------------
    # INDICADORES PRINCIPALES
    # ---------------------------------------------------

    st.markdown(
        '<div class="section-title">📌 Indicadores principales</div>',
        unsafe_allow_html=True
    )

    total_litros = (
        df_filtrado[
            "Lts"
        ]
        .sum()
    )

    total_registros = len(
        df_filtrado
    )

    promedio_carga = (
        df_filtrado[
            "Lts"
        ]
        .mean()
        if total_registros > 0
        else 0
    )

    consumo_por_mes = (
        df_filtrado
        .groupby(
            "Periodo"
        )[
            "Lts"
        ]
        .sum()
    )

    promedio_mensual_consumo = (
        consumo_por_mes.mean()
        if not consumo_por_mes.empty
        else 0
    )

    columna_indicador_1, columna_indicador_2, columna_indicador_3, columna_indicador_4 = st.columns(
        4
    )

    with columna_indicador_1:
        st.markdown(
            f'<div class="card"><div class="card-title">Total litros consumidos</div><div class="card-value">{total_litros:,.0f} L</div></div>',
            unsafe_allow_html=True
        )

    with columna_indicador_2:
        st.markdown(
            f'<div class="card"><div class="card-title">Cantidad de registros</div><div class="card-value">{total_registros}</div></div>',
            unsafe_allow_html=True
        )

    with columna_indicador_3:
        st.markdown(
            f'<div class="card"><div class="card-title">Promedio por carga</div><div class="card-value">{promedio_carga:,.1f} L</div></div>',
            unsafe_allow_html=True
        )

    with columna_indicador_4:
        st.markdown(
            f'<div class="card"><div class="card-title">Promedio mensual de consumo diesel</div><div class="card-value">{promedio_mensual_consumo:,.0f} L</div></div>',
            unsafe_allow_html=True
        )

    # ---------------------------------------------------
    # ANALISIS GRAFICO
    # ---------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Analisis grafico de consumos</div>',
        unsafe_allow_html=True
    )

    if df_filtrado.empty:
        st.warning(
            "No existen datos para mostrar con los filtros seleccionados."
        )

    else:

        # -----------------------------------------------
        # CONSUMO ANUAL
        # -----------------------------------------------

        consumo_anual = (
            df_filtrado
            .groupby(
                "Año"
            )[
                "Lts"
            ]
            .sum()
            .reset_index()
            .sort_values(
                "Año"
            )
        )

        años_grafico = (
            consumo_anual[
                "Año"
            ]
            .tolist()
        )

        grafico_anual = px.bar(
            consumo_anual,
            x="Año",
            y="Lts",
            text="Lts",
            title="Consumo anual de diesel",
            color="Lts",
            color_continuous_scale="Oranges",
            template="plotly_dark"
        )

        grafico_anual.update_traces(
            texttemplate="%{text:,.0f} L",
            textposition="outside"
        )

        grafico_anual.update_layout(
            height=440,
            xaxis_title="Año",
            yaxis_title="Litros",
            showlegend=False,
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(
                color="#e5e7eb"
            ),
            title_font=dict(
                size=24,
                color="#f8fafc"
            )
        )

        grafico_anual.update_xaxes(
            tickmode="array",
            tickvals=años_grafico,
            ticktext=[
                str(
                    año
                )
                for año in años_grafico
            ]
        )

        st.plotly_chart(
            grafico_anual,
            use_container_width=True
        )

        # -----------------------------------------------
        # TENDENCIA MENSUAL
        # -----------------------------------------------

        consumo_mensual = (
            df_filtrado
            .groupby(
                [
                    "Año",
                    "Mes",
                    "Mes_Nombre"
                ]
            )[
                "Lts"
            ]
            .sum()
            .reset_index()
            .sort_values(
                [
                    "Año",
                    "Mes"
                ]
            )
        )

        consumo_mensual[
            "Mes_Año"
        ] = (
            consumo_mensual[
                "Mes_Nombre"
            ]
            + " "
            + consumo_mensual[
                "Año"
            ]
            .astype(str)
        )

        grafico_mensual = px.line(
            consumo_mensual,
            x="Mes_Año",
            y="Lts",
            markers=True,
            title="Tendencia mensual de consumo",
            template="plotly_dark"
        )

        grafico_mensual.update_traces(
            line=dict(
                width=4,
                color="#f59e0b"
            ),
            marker=dict(
                size=10,
                color="#f97316"
            )
        )

        grafico_mensual.update_layout(
            height=440,
            xaxis_title="Mes",
            yaxis_title="Litros",
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(
                color="#e5e7eb"
            ),
            title_font=dict(
                size=24,
                color="#f8fafc"
            )
        )

        st.plotly_chart(
            grafico_mensual,
            use_container_width=True
        )

        # -----------------------------------------------
        # DISTRIBUCION MENSUAL
        # -----------------------------------------------

        st.markdown(
            '<div class="section-title">🥧 Distribucion mensual del consumo</div>',
            unsafe_allow_html=True
        )

        distribucion_mensual = (
            df_filtrado
            .groupby(
                [
                    "Mes",
                    "Mes_Nombre"
                ]
            )[
                "Lts"
            ]
            .sum()
            .reset_index()
            .sort_values(
                "Mes"
            )
        )

        total_consumo_mensual = (
            distribucion_mensual[
                "Lts"
            ]
            .sum()
        )

        distribucion_mensual[
            "Porcentaje"
        ] = (
            distribucion_mensual[
                "Lts"
            ]
            / total_consumo_mensual
            * 100
        )

        grafico_distribucion_mensual = px.pie(
            distribucion_mensual,
            names="Mes_Nombre",
            values="Lts",
            title="Participacion mensual del consumo de diesel",
            hole=0.55,
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )

        grafico_distribucion_mensual.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Litros consumidos: %{value:,.0f} L<br>"
                "Participacion: %{percent}<extra></extra>"
            ),
            marker=dict(
                line=dict(
                    color="#0f172a",
                    width=2
                )
            )
        )

        grafico_distribucion_mensual.update_layout(
            height=580,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(
                color="#e5e7eb"
            ),
            title_font=dict(
                size=24,
                color="#f8fafc"
            ),
            legend_title_text="Mes",
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02
            ),
            annotations=[
                dict(
                    text=f"{total_consumo_mensual:,.0f} L<br>Total",
                    x=0.5,
                    y=0.5,
                    font_size=22,
                    font_color="#f8fafc",
                    showarrow=False
                )
            ]
        )

        st.plotly_chart(
            grafico_distribucion_mensual,
            use_container_width=True
        )

        # -----------------------------------------------
        # TABLA RESUMEN MENSUAL
        # -----------------------------------------------

        st.markdown(
            '<div class="section-title">📋 Resumen mensual de participacion</div>',
            unsafe_allow_html=True
        )

        tabla_distribucion_mensual = (
            distribucion_mensual
            .copy()
        )

        tabla_distribucion_mensual[
            "Litros"
        ] = (
            tabla_distribucion_mensual[
                "Lts"
            ]
            .round(0)
            .astype(int)
        )

        tabla_distribucion_mensual[
            "Participacion"
        ] = (
            tabla_distribucion_mensual[
                "Porcentaje"
            ]
            .round(1)
            .astype(str)
            + "%"
        )

        tabla_distribucion_mensual = (
            tabla_distribucion_mensual[
                [
                    "Mes_Nombre",
                    "Litros",
                    "Participacion"
                ]
            ]
            .rename(
                columns={
                    "Mes_Nombre": "Mes"
                }
            )
        )

        st.dataframe(
            tabla_distribucion_mensual,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------------------------
        # COMPARATIVO MENSUAL POR AÑO
        # -----------------------------------------------

        st.markdown(
            '<div class="section-title">📆 Consumo mensual por año</div>',
            unsafe_allow_html=True
        )

        consumo_mes_barra = (
            df_filtrado
            .groupby(
                [
                    "Año",
                    "Mes",
                    "Mes_Nombre"
                ]
            )[
                "Lts"
            ]
            .sum()
            .reset_index()
            .sort_values(
                [
                    "Año",
                    "Mes"
                ]
            )
        )

        consumo_mes_barra[
            "Año_Texto"
        ] = (
            consumo_mes_barra[
                "Año"
            ]
            .astype(str)
        )

        grafico_mes_barra = px.bar(
            consumo_mes_barra,
            x="Mes_Nombre",
            y="Lts",
            color="Año_Texto",
            barmode="group",
            text="Lts",
            title="Comparativo mensual por año",
            template="plotly_dark",
            labels={
                "Año_Texto": "Año",
                "Mes_Nombre": "Mes",
                "Lts": "Litros"
            }
        )

        grafico_mes_barra.update_traces(
            texttemplate="%{text:,.0f} L",
            textposition="outside"
        )

        grafico_mes_barra.update_layout(
            height=500,
            xaxis_title="Mes",
            yaxis_title="Litros",
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(
                color="#e5e7eb"
            ),
            title_font=dict(
                size=24,
                color="#f8fafc"
            ),
            legend_title_text="Año"
        )

        st.plotly_chart(
            grafico_mes_barra,
            use_container_width=True
        )

        # -----------------------------------------------
        # RESUMEN POR EQUIPO
        # -----------------------------------------------

        st.markdown(
            '<div class="section-title">📅 Resumen de consumo por equipo</div>',
            unsafe_allow_html=True
        )

        if "Equipo" in df_filtrado.columns:
            resumen_equipo = (
                df_filtrado
                .pivot_table(
                    index="Equipo",
                    columns="Año",
                    values="Lts",
                    aggfunc="sum",
                    fill_value=0
                )
            )

            st.dataframe(
                resumen_equipo,
                use_container_width=True
            )

        else:
            st.info(
                "No se encontro la columna 'Equipo' en la planilla."
            )

    # ---------------------------------------------------
    # TABLA GENERAL
    # ---------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Registro general de diesel</div>',
        unsafe_allow_html=True
    )

    columnas_mostrar = [
        "Fecha",
        "Descripción",
        "Operador",
        "Equipo",
        "N° Salida Existencia",
        "Lts",
        "Año",
        "Mes_Nombre",
        "Periodo"
    ]

    columnas_mostrar = [
        columna
        for columna in columnas_mostrar
        if columna in df_filtrado.columns
    ]

    tabla_mostrar = (
        df_filtrado[
            columnas_mostrar
        ]
        .copy()
    )

    st.dataframe(
        tabla_mostrar,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------------
    # ALERTAS
    # ---------------------------------------------------

    st.markdown(
        '<div class="section-title">🚨 Alertas de control</div>',
        unsafe_allow_html=True
    )

    limite_litros = st.number_input(
        "Definir limite de litros por carga",
        min_value=0,
        value=50,
        step=1
    )

    alertas = df_filtrado[
        df_filtrado[
            "Lts"
        ] > limite_litros
    ]

    if not alertas.empty:
        st.warning(
            "Existen cargas que superan el limite definido."
        )

        alertas_mostrar = (
            alertas[
                columnas_mostrar
            ]
            .copy()
        )

        st.dataframe(
            alertas_mostrar,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "No existen cargas sobre el limite definido."
        )


# =====================================================
# MANEJO DE ERRORES
# =====================================================

except FileNotFoundError:
    st.error(
        "No se encontro la planilla Excel."
    )

    st.write(
        "Verifica que el archivo este en la misma carpeta "
        "que app.py y que mantenga exactamente este nombre:"
    )

    st.code(
        "DIESEL SERFOCOL- V01.xlsx"
    )

except Exception as error:
    st.error(
        "Ocurrio un error al cargar la planilla."
    )

    st.write(
        error
    )


# =====================================================
# PIE DE PAGINA
# =====================================================

st.markdown(
    """
    <div class="footer-panel">
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