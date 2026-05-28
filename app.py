import streamlit as st
import pandas as pd 
import plotly.express as px

# -------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------------

st.set_page_config(
    page_title="Control de Diésel SERFOCOL",
    page_icon="⛽",
    layout="wide"
)

# -------------------------------------------------------
# ESTILO OSCURO PROFESIONAL
# -------------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #e5e7eb;
    }

    .main {
        background-color: #0f172a;
    }

    .titulo-principal {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .subtitulo {
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 25px;
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

    .card {
        background: linear-gradient(135deg, #1e293b, #111827);
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0px 4px 16px rgba(0,0,0,0.45);
        text-align: center;
        border: 1px solid #334155;
    }

    .card-title {
        font-size: 15px;
        color: #cbd5e1;
        font-weight: 600;
    }

    .card-value {
        font-size: 31px;
        color: #f59e0b;
        font-weight: 900;
        margin-top: 8px;
    }

    div[data-testid="stDataFrame"] {
        background-color: #1e293b;
        border-radius: 12px;
    }

    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label,
    .stNumberInput label {
        color: #e5e7eb !important;
        font-weight: 600;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# TÍTULO
# -------------------------------------------------------

st.markdown(
    '<div class="titulo-principal">⛽ Dashboard de Control de Diésel SERFOCOL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Panel web profesional para analizar consumos de diésel por año, mes, equipo y operador.</div>',
    unsafe_allow_html=True
)

# -------------------------------------------------------
# ARCHIVO EXCEL
# -------------------------------------------------------

archivo_excel = "DIESEL SERFOCOL- V01.xlsx"

try:
    # -------------------------------------------------------
    # LECTURA DE EXCEL
    # -------------------------------------------------------

    df = pd.read_excel(
        archivo_excel,
        header=8,
        usecols="A:F"
    )

    # -------------------------------------------------------
    # LIMPIEZA GENERAL
    # -------------------------------------------------------

    df.columns = df.columns.astype(str).str.strip()
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]
    df = df.dropna(how="all")

    if "Lts" not in df.columns:
        st.error("No se encontró la columna 'Lts'.")
        st.write("Columnas detectadas:")
        st.write(list(df.columns))
        st.stop()

    if "Fechas" in df.columns:
        df = df.dropna(subset=["Fechas", "Lts"], how="all")

    df["Lts"] = pd.to_numeric(df["Lts"], errors="coerce")
    df = df[df["Lts"].notna()]
    df = df[df["Lts"] > 0]

    df["Fechas"] = pd.to_datetime(df["Fechas"], errors="coerce", dayfirst=True)
    df = df[df["Fechas"].notna()]

    # -------------------------------------------------------
    # FECHAS Y MESES EN ESPAÑOL
    # -------------------------------------------------------

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

    df["Año"] = df["Fechas"].dt.year.astype(int)
    df["Mes"] = df["Fechas"].dt.month
    df["Mes_Nombre"] = df["Mes"].map(meses_espanol)
    df["Periodo"] = df["Fechas"].dt.strftime("%Y-%m")
    df["Fecha"] = df["Fechas"].dt.strftime("%d-%m-%Y")

    st.success("Planilla cargada correctamente.")

    # -------------------------------------------------------
    # FILTROS
    # -------------------------------------------------------

    st.markdown('<div class="section-title">🔎 Filtros de análisis</div>', unsafe_allow_html=True)

    df_filtrado = df.copy()

    colf1, colf2, colf3, colf4 = st.columns(4)

    with colf1:
        años = st.multiselect(
            "Año",
            sorted(df["Año"].dropna().unique())
        )

        if años:
            df_filtrado = df_filtrado[df_filtrado["Año"].isin(años)]

    with colf2:
        if "Equipo" in df.columns:
            equipos = st.multiselect(
                "Equipo",
                sorted(df["Equipo"].dropna().unique())
            )

            if equipos:
                df_filtrado = df_filtrado[df_filtrado["Equipo"].isin(equipos)]

    with colf3:
        if "Operador" in df.columns:
            operadores = st.multiselect(
                "Operador",
                sorted(df["Operador"].dropna().unique())
            )

            if operadores:
                df_filtrado = df_filtrado[df_filtrado["Operador"].isin(operadores)]

    with colf4:
        if "Descripción" in df.columns:
            descripciones = st.multiselect(
                "Descripción",
                sorted(df["Descripción"].dropna().unique())
            )

            if descripciones:
                df_filtrado = df_filtrado[df_filtrado["Descripción"].isin(descripciones)]

    # -------------------------------------------------------
    # FILTRO POR RANGO DE FECHAS
    # -------------------------------------------------------

    st.markdown('<div class="section-title">📅 Filtro por rango de fechas</div>', unsafe_allow_html=True)

    fecha_min = df["Fechas"].min()
    fecha_max = df["Fechas"].max()

    rango_fechas = st.date_input(
        "Selecciona rango de fechas",
        value=(fecha_min, fecha_max)
    )

    if len(rango_fechas) == 2:
        inicio, fin = rango_fechas

        df_filtrado = df_filtrado[
            (df_filtrado["Fechas"].dt.date >= inicio) &
            (df_filtrado["Fechas"].dt.date <= fin)
        ]

    # -------------------------------------------------------
    # INDICADORES
    # -------------------------------------------------------

    st.markdown('<div class="section-title">📌 Indicadores principales</div>', unsafe_allow_html=True)

    total_litros = df_filtrado["Lts"].sum()
    total_registros = len(df_filtrado)
    promedio_carga = df_filtrado["Lts"].mean() if total_registros > 0 else 0
    total_equipos = df_filtrado["Equipo"].nunique() if "Equipo" in df_filtrado.columns else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Total litros consumidos</div>
            <div class="card-value">{total_litros:,.0f} L</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Cantidad de registros</div>
            <div class="card-value">{total_registros}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Promedio por carga</div>
            <div class="card-value">{promedio_carga:,.1f} L</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Equipos registrados</div>
            <div class="card-value">{total_equipos}</div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # CONFIGURACIÓN GENERAL DE GRÁFICOS
    # -------------------------------------------------------

    template_dark = "plotly_dark"

    grafico_layout = dict(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=24, color="#f8fafc"),
        coloraxis_colorbar=dict(
            title=dict(text="Litros")
        )
    )

    # -------------------------------------------------------
    # GRÁFICOS
    # -------------------------------------------------------

    st.markdown('<div class="section-title">📊 Análisis gráfico de consumos</div>', unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("No existen datos para mostrar con los filtros seleccionados.")

    else:
        # ---------------------------------------------------
        # CONSUMO ANUAL
        # ---------------------------------------------------

        consumo_anual = (
            df_filtrado.groupby("Año")["Lts"]
            .sum()
            .reset_index()
            .sort_values("Año")
        )

        años_grafico = consumo_anual["Año"].tolist()

        fig_anual = px.bar(
            consumo_anual,
            x="Año",
            y="Lts",
            text="Lts",
            title="Consumo anual de diésel",
            color="Lts",
            color_continuous_scale="Oranges",
            template=template_dark
        )

        fig_anual.update_traces(
            texttemplate="%{text:,.0f} L",
            textposition="outside"
        )

        fig_anual.update_layout(
            height=440,
            xaxis_title="Año",
            yaxis_title="Litros",
            showlegend=False,
            **grafico_layout
        )

        fig_anual.update_xaxes(
            tickmode="array",
            tickvals=años_grafico,
            ticktext=[str(año) for año in años_grafico]
        )

        fig_anual.update_coloraxes(colorbar_title="Litros")

        st.plotly_chart(fig_anual, use_container_width=True)

        # ---------------------------------------------------
        # TENDENCIA MENSUAL
        # ---------------------------------------------------

        consumo_mensual = (
            df_filtrado.groupby(["Año", "Mes", "Mes_Nombre"])["Lts"]
            .sum()
            .reset_index()
            .sort_values(["Año", "Mes"])
        )

        consumo_mensual["Mes_Año"] = (
            consumo_mensual["Mes_Nombre"] + " " + consumo_mensual["Año"].astype(str)
        )

        fig_mensual = px.line(
            consumo_mensual,
            x="Mes_Año",
            y="Lts",
            markers=True,
            title="Tendencia mensual de consumo",
            template=template_dark
        )

        fig_mensual.update_traces(
            line=dict(width=4, color="#f59e0b"),
            marker=dict(size=10, color="#f97316")
        )

        fig_mensual.update_layout(
            height=440,
            xaxis_title="Mes",
            yaxis_title="Litros",
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(color="#e5e7eb"),
            title_font=dict(size=24, color="#f8fafc")
        )

        st.plotly_chart(fig_mensual, use_container_width=True)

        # ---------------------------------------------------
        # DISTRIBUCIÓN MENSUAL DEL CONSUMO
        # ---------------------------------------------------

        st.markdown(
            '<div class="section-title">🥧 Distribución mensual del consumo</div>',
            unsafe_allow_html=True
        )

        distribucion_mensual = (
            df_filtrado.groupby(["Mes", "Mes_Nombre"])["Lts"]
            .sum()
            .reset_index()
            .sort_values("Mes")
        )

        total_consumo_mensual = distribucion_mensual["Lts"].sum()

        distribucion_mensual["Porcentaje"] = (
            distribucion_mensual["Lts"] / total_consumo_mensual * 100
        )

        fig_distribucion_mensual = px.pie(
            distribucion_mensual,
            names="Mes_Nombre",
            values="Lts",
            title="Participación mensual del consumo de diésel",
            hole=0.55,
            template=template_dark,
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )

        fig_distribucion_mensual.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Litros consumidos: %{value:,.0f} L<br>"
                "Participación: %{percent}<extra></extra>"
            ),
            marker=dict(
                line=dict(color="#0f172a", width=2)
            )
        )

        fig_distribucion_mensual.update_layout(
            height=580,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#e5e7eb"),
            title_font=dict(size=24, color="#f8fafc"),
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

        st.plotly_chart(fig_distribucion_mensual, use_container_width=True)

        # ---------------------------------------------------
        # TABLA RESUMEN MENSUAL
        # ---------------------------------------------------

        st.markdown(
            '<div class="section-title">📋 Resumen mensual de participación</div>',
            unsafe_allow_html=True
        )

        tabla_distribucion_mensual = distribucion_mensual.copy()
        tabla_distribucion_mensual["Litros"] = tabla_distribucion_mensual["Lts"].round(0).astype(int)
        tabla_distribucion_mensual["Participación"] = tabla_distribucion_mensual["Porcentaje"].round(1).astype(str) + "%"

        tabla_distribucion_mensual = tabla_distribucion_mensual[
            ["Mes_Nombre", "Litros", "Participación"]
        ]

        tabla_distribucion_mensual = tabla_distribucion_mensual.rename(
            columns={
                "Mes_Nombre": "Mes"
            }
        )

        st.dataframe(tabla_distribucion_mensual, use_container_width=True)

        # ---------------------------------------------------
        # RANKING EQUIPO / OPERADOR
        # ---------------------------------------------------

        st.markdown('<div class="section-title">🏆 Ranking de consumo</div>', unsafe_allow_html=True)

        colb1, colb2 = st.columns(2)

        with colb1:
            if "Equipo" in df_filtrado.columns:
                consumo_equipo = (
                    df_filtrado.groupby("Equipo")["Lts"]
                    .sum()
                    .reset_index()
                    .sort_values("Lts", ascending=True)
                )

                fig_equipo = px.bar(
                    consumo_equipo,
                    x="Lts",
                    y="Equipo",
                    orientation="h",
                    text="Lts",
                    title="Ranking de consumo por equipo",
                    color="Lts",
                    color_continuous_scale="Oranges",
                    template=template_dark
                )

                fig_equipo.update_traces(
                    texttemplate="%{text:,.0f} L",
                    textposition="outside"
                )

                fig_equipo.update_layout(
                    height=520,
                    xaxis_title="Litros",
                    yaxis_title="Equipo",
                    showlegend=False,
                    **grafico_layout
                )

                fig_equipo.update_coloraxes(colorbar_title="Litros")

                st.plotly_chart(fig_equipo, use_container_width=True)

        with colb2:
            if "Operador" in df_filtrado.columns:
                consumo_operador = (
                    df_filtrado.groupby("Operador")["Lts"]
                    .sum()
                    .reset_index()
                    .sort_values("Lts", ascending=True)
                )

                fig_operador = px.bar(
                    consumo_operador,
                    x="Lts",
                    y="Operador",
                    orientation="h",
                    text="Lts",
                    title="Ranking de consumo por operador",
                    color="Lts",
                    color_continuous_scale="Blues",
                    template=template_dark
                )

                fig_operador.update_traces(
                    texttemplate="%{text:,.0f} L",
                    textposition="outside"
                )

                fig_operador.update_layout(
                    height=520,
                    xaxis_title="Litros",
                    yaxis_title="Operador",
                    showlegend=False,
                    **grafico_layout
                )

                fig_operador.update_coloraxes(colorbar_title="Litros")

                st.plotly_chart(fig_operador, use_container_width=True)

        # ---------------------------------------------------
        # CONSUMO MENSUAL POR AÑO
        # ---------------------------------------------------

        st.markdown('<div class="section-title">📆 Consumo mensual por año</div>', unsafe_allow_html=True)

        consumo_mes_barra = (
            df_filtrado.groupby(["Año", "Mes", "Mes_Nombre"])["Lts"]
            .sum()
            .reset_index()
            .sort_values(["Año", "Mes"])
        )

        consumo_mes_barra["Año_Texto"] = consumo_mes_barra["Año"].astype(str)

        fig_mes_barra = px.bar(
            consumo_mes_barra,
            x="Mes_Nombre",
            y="Lts",
            color="Año_Texto",
            barmode="group",
            text="Lts",
            title="Comparativo mensual por año",
            template=template_dark,
            labels={
                "Año_Texto": "Año",
                "Mes_Nombre": "Mes",
                "Lts": "Litros"
            }
        )

        fig_mes_barra.update_traces(
            texttemplate="%{text:,.0f} L",
            textposition="outside"
        )

        fig_mes_barra.update_layout(
            height=500,
            xaxis_title="Mes",
            yaxis_title="Litros",
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(color="#e5e7eb"),
            title_font=dict(size=24, color="#f8fafc"),
            legend_title_text="Año"
        )

        st.plotly_chart(fig_mes_barra, use_container_width=True)

        # ---------------------------------------------------
        # RESUMEN ANUAL POR EQUIPO
        # ---------------------------------------------------

        st.markdown('<div class="section-title">📅 Resumen anual de consumo por equipo</div>', unsafe_allow_html=True)

        if "Equipo" in df_filtrado.columns:
            resumen_anual_equipo = df_filtrado.pivot_table(
                index="Equipo",
                columns="Año",
                values="Lts",
                aggfunc="sum",
                fill_value=0
            )

            st.dataframe(resumen_anual_equipo, use_container_width=True)

    # -------------------------------------------------------
    # TABLA GENERAL
    # -------------------------------------------------------

    st.markdown('<div class="section-title">📋 Registro general de diésel</div>', unsafe_allow_html=True)

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

    columnas_mostrar = [col for col in columnas_mostrar if col in df_filtrado.columns]

    tabla_mostrar = df_filtrado[columnas_mostrar].copy()

    st.dataframe(tabla_mostrar, use_container_width=True)

    # -------------------------------------------------------
    # ALERTAS
    # -------------------------------------------------------

    st.markdown('<div class="section-title">🚨 Alertas de control</div>', unsafe_allow_html=True)

    limite = st.number_input(
        "Definir límite de litros por carga",
        min_value=0,
        value=50
    )

    alertas = df_filtrado[df_filtrado["Lts"] > limite]

    if not alertas.empty:
        st.warning("Existen cargas que superan el límite definido.")

        alertas_mostrar = alertas[columnas_mostrar].copy()
        st.dataframe(alertas_mostrar, use_container_width=True)
    else:
        st.success("No existen cargas sobre el límite definido.")

    # -------------------------------------------------------
    # DESCARGA
    # -------------------------------------------------------

    st.markdown('<div class="section-title">⬇️ Descargar información</div>', unsafe_allow_html=True)

    csv = tabla_mostrar.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar datos filtrados",
        data=csv,
        file_name="control_diesel_filtrado.csv",
        mime="text/csv"
    )

# -------------------------------------------------------
# MANEJO DE ERRORES
# -------------------------------------------------------

except FileNotFoundError:
    st.error("No se encontró la planilla Excel.")
    st.write("Verifica que el archivo esté en la misma carpeta que app.py.")
    st.code(archivo_excel)

except Exception as e:
    st.error("Ocurrió un error al cargar la planilla.")
    st.write(e)
