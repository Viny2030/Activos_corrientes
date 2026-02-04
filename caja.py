# ===============================================================
# PARTE 1: GENERACIÓN DE DATOS (Función)
# ===============================================================
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import streamlit as st
import matplotlib.patches as mpatches


@st.cache_data
def generar_dataframe_caja():
    """Genera y devuelve un DataFrame simulado de transacciones de caja."""
    fake_es = Faker ('es_AR')
    np.random.seed (42)
    random.seed (42)
    Faker.seed (42)

    descripciones_gasto = [
        "Pago de servicios", "Compra de suministros", "Mantenimiento de equipos",
        "Gastos de representación", "Alquiler de oficina", "Pago a proveedores",
        "Reparación de maquinaria", "Transporte y logística", "Capacitación del personal",
        "Honorarios profesionales"
    ]
    num_registros = 50  # Aumentado para mejor visualización
    responsables = [fake_es.name () for _ in range (10)]
    tipos_transaccion = ['Venta', 'Gasto']
    metodos_pago = ['Efectivo', 'Tarjeta de Débito', 'Tarjeta de Crédito', 'Transferencia']
    categorias_productos = ['Electrónica', 'Alimentos', 'Ropa', 'Accesorios', 'Juguetes']
    saldo = 50000
    registros = []

    for i in range (num_registros):
        fecha_hora_transaccion = fake_es.date_time_between (start_date='-6M', end_date='now')
        tipo_transaccion = random.choice (tipos_transaccion)
        monto = round (random.uniform (1000, 15000), 2)

        if tipo_transaccion == 'Venta':
            saldo += monto
        else:
            saldo -= monto

        registro = {
            'id_transaccion': i + 1,
            'fecha_hora': fecha_hora_transaccion.strftime ('%Y-%m-%d %H:%M:%S'),
            'tipo_transaccion': tipo_transaccion,
            'metodo_pago': random.choice (metodos_pago),
            'monto': monto,
            'saldo_acumulado': round (saldo, 2),
            'cajero_id': fake_es.random_int (min=1, max=10),
            'numero_ticket': fake_es.unique.bothify (text='TK-########'),
            'cliente_id': fake_es.random_int (min=1000, max=9999) if random.random () > 0.3 else None,
            'producto_categoria': random.choice (categorias_productos) if tipo_transaccion == 'Venta' else None,
            'descripcion': random.choice (descripciones_gasto) if tipo_transaccion == 'Gasto' else None,
            'responsable': random.choice (responsables)
        }
        registros.append (registro)

    df = pd.DataFrame (registros)
    df.sort_values (by='fecha_hora', inplace=True)
    df.reset_index (drop=True, inplace=True)
    return df


# ===============================================================
# PARTE 2: ANÁLISIS DE AUDITORÍA Y DETECCIÓN DE ANOMALÍAS (Función)
# ===============================================================
@st.cache_data
def analizar_datos(df):
    """Aplica reglas de auditoría y detección de anomalías al DataFrame."""
    df['fecha_hora'] = pd.to_datetime (df['fecha_hora'])
    df['diferencia_saldo'] = df['saldo_acumulado'].diff ().fillna (0).round (2)
    df['error_saldo'] = df.apply (
        lambda row: 'Venta con saldo decreciente' if row['tipo_transaccion'] == 'Venta' and row[
            'diferencia_saldo'] < 0 else ('Gasto con saldo creciente' if row['tipo_transaccion'] == 'Gasto' and row[
            'diferencia_saldo'] > 0 else None), axis=1)
    df['error_descripcion'] = df.apply (
        lambda r: 'Gasto sin descripción' if r['tipo_transaccion'] == 'Gasto' and pd.isnull (
            r['descripcion']) else None, axis=1)
    df['error_categoria'] = df.apply (
        lambda r: 'Venta sin categoría' if r['tipo_transaccion'] == 'Venta' and pd.isnull (
            r['producto_categoria']) else None, axis=1)
    df['hora'] = df['fecha_hora'].dt.hour
    df['error_horario'] = df.apply (lambda r: 'Gasto fuera de horario (7-21)' if r['tipo_transaccion'] == 'Gasto' and (
                r['hora'] < 7 or r['hora'] > 21) else None, axis=1)
    gastos_por_cajero = df[df['tipo_transaccion'] == 'Gasto'].groupby ('cajero_id').size ()
    cajeros_sospechosos = gastos_por_cajero[gastos_por_cajero > 3].index.tolist ()
    df['alerta_cajero'] = df.apply (lambda r: 'Cajero con muchos gastos (>3)' if r['tipo_transaccion'] == 'Gasto' and r[
        'cajero_id'] in cajeros_sospechosos else None, axis=1)
    df['alerta_duplicada'] = df.duplicated (['id_transaccion', 'fecha_hora'], keep=False).apply (
        lambda x: 'Transacción duplicada' if x else None)

    def detectar_outliers_iqr(df_segmento, columna_monto):
        if df_segmento.empty: return pd.Series ([False] * len (df_segmento), index=df_segmento.index)
        Q1, Q3 = df_segmento[columna_monto].quantile ([0.25, 0.75])
        IQR = Q3 - Q1
        if IQR == 0: return pd.Series (False, index=df_segmento.index)
        limite_inferior, limite_superior = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        return ~df_segmento[columna_monto].between (limite_inferior, limite_superior)

    for tipo in df['tipo_transaccion'].unique ():
        subset_indices = df['tipo_transaccion'] == tipo
        is_outlier = detectar_outliers_iqr (df[subset_indices], 'monto')
        df.loc[subset_indices, 'alerta_monto_irregular'] = is_outlier.apply (
            lambda x: f'Monto {tipo} irregular (outlier)' if x else None)

    features_ia = df[['monto', 'diferencia_saldo']].copy ()

    # -------------------------------------------------------------
    # Algoritmos de Machine Learning
    # -------------------------------------------------------------

    # Decision Tree (Clasificación)
    df['tipo_encoded'] = df['tipo_transaccion'].apply (lambda x: 1 if x == 'Venta' else 0)
    features_dt = df[['monto', 'diferencia_saldo']].copy ()
    labels_dt = df['tipo_encoded']
    tree_classifier = DecisionTreeClassifier (random_state=42)
    tree_classifier.fit (features_dt, labels_dt)
    df['prediccion_dt'] = tree_classifier.predict (features_dt)
    df['alerta_dt'] = df.apply (
        lambda r: 'Predicción de DT incorrecta' if r['prediccion_dt'] != r['tipo_encoded'] else None, axis=1)

    # One-Class SVM (Detección de Anomalías)
    scaler = StandardScaler ()
    scaled_features = scaler.fit_transform (features_ia)
    svm = OneClassSVM (kernel='rbf', gamma='auto', nu=0.05)
    df['svm_anomaly'] = svm.fit_predict (scaled_features)
    df['alerta_svm'] = df['svm_anomaly'].apply (lambda x: 'Anomalía detectada por SVM' if x == -1 else None)

    # Isolation Forest (Detección de Anomalías)
    iso_forest = IsolationForest (random_state=42, contamination=0.05)
    df['is_anomaly'] = iso_forest.fit_predict (features_ia)
    df['alerta_fraude_ia'] = df['is_anomaly'].apply (
        lambda x: 'Anomalía detectada por Isolation Forest' if x == -1 else None)

    # -------------------------------------------------------------

    df['dia_semana_es'] = df['fecha_hora'].dt.day_name ().replace (
        {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
         'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
    )
    alert_cols = ['error_saldo', 'error_descripcion', 'error_categoria', 'error_horario',
                  'alerta_cajero', 'alerta_duplicada', 'alerta_monto_irregular',
                  'alerta_fraude_ia', 'alerta_dt', 'alerta_svm']
    df['alertas'] = df[alert_cols].apply (lambda row: ', '.join (row.dropna ()), axis=1)
    df_alertas = df[df['alertas'] != ''].copy ()

    return df, df_alertas


# ===============================================================
# PARTE 3: APLICACIÓN STREAMLIT
# ===============================================================
def main():
    st.set_page_config (layout="wide", page_title="Auditoría de Caja")
    st.title ('💰 Auditoría y Detección de Fraude en Caja')
    st.markdown ("""
        Esta aplicación simula transacciones de caja y aplica reglas de auditoría y modelos
        de IA para detectar posibles anomalías y fraudes.
    """)

    df = generar_dataframe_caja ()
    df, df_alertas = analizar_datos (df)

    # --- Sidebar interactiva para filtros ---
    st.sidebar.header ('Filtros')

    # Filtro por tipo de transacción
    tipos_transaccion = df['tipo_transaccion'].unique ().tolist ()
    tipos_seleccionados = st.sidebar.multiselect (
        'Selecciona el Tipo de Transacción',
        options=tipos_transaccion,
        default=tipos_transaccion
    )

    # Filtro por rango de fechas
    fecha_min = df['fecha_hora'].min ().date ()
    fecha_max = df['fecha_hora'].max ().date ()
    fecha_inicio = st.sidebar.date_input ('Fecha de Inicio', value=fecha_min)
    fecha_fin = st.sidebar.date_input ('Fecha de Fin', value=fecha_max)

    # Convertir las fechas a tipo datetime para la comparación
    fecha_inicio_dt = pd.to_datetime (fecha_inicio)
    fecha_fin_dt = pd.to_datetime (fecha_fin) + pd.Timedelta (days=1, seconds=-1)

    # Aplicar filtros
    df_filtrado = df[
        (df['tipo_transaccion'].isin (tipos_seleccionados)) &
        (df['fecha_hora'] >= fecha_inicio_dt) &
        (df['fecha_hora'] <= fecha_fin_dt)
        ]
    df_alertas_filtrado = df_alertas[
        (df_alertas['tipo_transaccion'].isin (tipos_seleccionados)) &
        (df_alertas['fecha_hora'] >= fecha_inicio_dt) &
        (df_alertas['fecha_hora'] <= fecha_fin_dt)
        ]

    st.subheader ('🔍 Datos Filtrados (Vista Previa)')
    st.dataframe (df_filtrado.head (10))

    # Botón para descargar CSV
    csv = df_alertas_filtrado.to_csv (index=False).encode ('utf-8')
    st.download_button (
        label="Descargar Alertas en CSV 📊",
        data=csv,
        file_name='transacciones_con_alertas.csv',
        mime='text/csv',
    )

    st.subheader ('📝 Resumen de Alertas')

    total_transacciones = len (df_filtrado)
    total_alertas = len (df_alertas_filtrado)
    porcentaje_alertas = (total_alertas / total_transacciones) * 100 if total_transacciones > 0 else 0
    total_anomalias_if = (df_filtrado['alerta_fraude_ia'] == 'Anomalía detectada por Isolation Forest').sum ()
    total_anomalias_svm = (df_filtrado['alerta_svm'] == 'Anomalía detectada por SVM').sum ()

    col1, col2, col3, col4 = st.columns (4)
    col1.metric ("Transacciones Analizadas", total_transacciones)
    col2.metric ("Transacciones con Alertas", total_alertas, f"{porcentaje_alertas:.2f}%")
    col3.metric ("Anomalías por Isolation Forest", total_anomalias_if)
    col4.metric ("Anomalías por SVM", total_anomalias_svm)

    if not df_alertas_filtrado.empty:
        st.write ('**Transacciones con Alertas**')
        st.dataframe (df_alertas_filtrado[['id_transaccion', 'fecha_hora', 'monto', 'alertas']])

    st.subheader ('📈 Visualizaciones de los Algoritmos')
    sns.set (style="whitegrid")

    # --- Gráfico 1: Comparación de Anomalías con Isolation Forest y SVM ---
    st.write ('### 1. Comparación de Detección de Anomalías (Isolation Forest vs. SVM)')
    st.markdown ("""
        Aquí se visualizan las transacciones, destacando las anomalías detectadas por dos algoritmos
        diferentes: Isolation Forest y One-Class SVM.
    """)
    fig_anomalias, ax_anomalias = plt.subplots (figsize=(12, 6))
    sns.scatterplot (data=df_filtrado, x='monto', y='diferencia_saldo', hue='tipo_transaccion',
                     style='tipo_transaccion', ax=ax_anomalias, s=100)

    # Destacar anomalías de Isolation Forest
    anomalias_if = df_filtrado[df_filtrado['alerta_fraude_ia'].notnull ()]
    ax_anomalias.scatter (anomalias_if['monto'], anomalias_if['diferencia_saldo'], s=200, facecolors='none',
                          edgecolors='red', label='Anomalía IF', linewidths=2)

    # Destacar anomalías de SVM
    anomalias_svm = df_filtrado[df_filtrado['alerta_svm'].notnull ()]
    ax_anomalias.scatter (anomalias_svm['monto'], anomalias_svm['diferencia_saldo'], s=200, facecolors='none',
                          edgecolors='orange', label='Anomalía SVM', linewidths=2, marker='X')

    ax_anomalias.set_title ('Detección de Anomalías (Isolation Forest vs. SVM)')
    ax_anomalias.set_xlabel ('Monto de Transacción ($)')
    ax_anomalias.set_ylabel ('Diferencia de Saldo')
    ax_anomalias.legend ()
    st.pyplot (fig_anomalias)

    # --- Gráfico 2: Alertas del Árbol de Decisión ---
    st.write ('### 2. Predicciones Incorrectas del Árbol de Decisión')
    st.markdown ("""
        Este gráfico muestra las transacciones donde el **Árbol de Decisión** hizo una predicción incorrecta
        sobre el tipo de transacción (Venta o Gasto) basándose en el monto. Esto podría indicar
        transacciones atípicas o fuera del patrón habitual.
    """)
    fig_dt, ax_dt = plt.subplots (figsize=(12, 6))
    sns.scatterplot (data=df_filtrado, x='monto', y='tipo_transaccion', hue='tipo_transaccion',
                     style='tipo_transaccion', ax=ax_dt, s=100)

    # Destacar las predicciones incorrectas del árbol de decisión
    errores_dt = df_filtrado[df_filtrado['alerta_dt'].notnull ()]
    ax_dt.scatter (errores_dt['monto'], errores_dt['tipo_transaccion'], s=300, facecolors='none', edgecolors='purple',
                   label='Error de Predicción', linewidths=2)

    ax_dt.set_title ('Errores de Predicción del Árbol de Decisión')
    ax_dt.set_xlabel ('Monto de Transacción ($)')
    ax_dt.set_ylabel ('Tipo de Transacción')

    # Crear leyenda manualmente para la alerta de error
    error_patch = mpatches.Circle ((0, 0), radius=1, color='purple', linestyle='--', label='Error de Predicción')

    handles, labels = ax_dt.get_legend_handles_labels ()
    handles.append (error_patch)
    labels.append ('Error de Predicción')
    ax_dt.legend (handles=handles, labels=labels, title='Transacción')

    st.pyplot (fig_dt)


if __name__ == '__main__':
    main ()