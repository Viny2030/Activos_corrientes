import streamlit as st
import pandas as pd
from datetime import datetime

# Importación de los módulos de auditoría (tus archivos)
import caja
import conciliacion_bancaria
import cuentas_a_cobrar
import inversiones_temporarias
import colocaciones
import materias_primas
import gastos_pagados_por_adelantado1
import otros_activos_corrientes1
from generador_informes import renderizar_informe_formal

# Configuración única de la página
st.set_page_config(page_title="Auditoría Algorítmica de Activos Corrientes", layout="wide")

# Inicializar almacenamiento de resultados en la sesión
if 'resultados' not in st.session_state:
    st.session_state['resultados'] = {}

# Barra Lateral - Navegación
st.sidebar.title("🔍 Auditoría Phd. Monteverde")
st.sidebar.markdown("---")
opcion = st.sidebar.selectbox(
    "Seleccione el Rubro:",
    [
        "Inicio",
        "Caja y Tesorería",
        "Conciliación Bancaria",
        "Cuentas a Cobrar",
        "Inversiones Temporarias",
        "Colocaciones",
        "Materias Primas",
        "Gastos Prepagos",
        "Otros Activos Corrientes",
        "INFORME FINAL (RT 37/NIA)"
    ]
)

# --- Lógica de la Aplicación ---

if opcion == "Inicio":
    st.title("Sistema Integral de Auditoría: Activos Corrientes")
    st.write("Bienvenido al entorno de evaluación algorítmica. Utilice el menú lateral para procesar cada rubro.")
    st.info("Al ejecutar cada módulo, los hallazgos se guardarán automáticamente para el Informe Final.")

elif opcion == "Caja y Tesorería":
    st.header("Módulo: Caja y Tesorería")
    df = caja.generar_dataframe_caja()
    # Ejecuta la lógica y guarda el DF auditado
    st.session_state['resultados']['Caja y Tesorería'] = df
    st.success("Análisis de Caja completado.")
    # (Aquí puedes llamar a una función de visualización dentro de caja.py si existe)

elif opcion == "Conciliación Bancaria":
    st.header("Módulo: Conciliación Bancaria")
    # Lógica de conciliacion_bancaria.py
    st.info("Procesando Fuzzy Matching...")
    # st.session_state['resultados']['Conciliación'] = ...

elif opcion == "Cuentas a Cobrar":
    st.header("Módulo: Cuentas a Cobrar")
    df = cuentas_a_cobrar.generar_datos_simulados()
    st.session_state['resultados']['Cuentas a Cobrar'] = df
    st.dataframe(df.head())

elif opcion == "Inversiones Temporarias":
    st.header("Módulo: Inversiones Temporarias")
    df = inversiones_temporarias.generar_datos_simulados()
    st.session_state['resultados']['Inversiones'] = df

elif opcion == "Materias Primas":
    st.header("Módulo: Inventarios / Materias Primas")
    df = materias_primas.generar_datos_simulados()
    st.session_state['resultados']['Materias Primas'] = df

elif opcion == "INFORME FINAL (RT 37/NIA)":
    if not st.session_state['resultados']:
        st.warning("⚠️ No hay datos procesados. Por favor, ejecute la auditoría en los rubros anteriores.")
    else:
        # Llamamos al generador que replica tu PDF de ejemplo
        renderizar_informe_formal(st.session_state['resultados'])