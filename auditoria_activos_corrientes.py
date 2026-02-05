# ===============================================================
# SISTEMA INTEGRADO DE AUDITORÍA DE ACTIVOS CORRIENTES
# Versión 1.0 - Conforme RT 7, RT 37 y NIAs
# ===============================================================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import streamlit as st
import os
import tempfile
from generador_informe import GeneradorInformeAuditoria

# Configuración de la página
st.set_page_config(
    page_title="Auditoría de Activos Corrientes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================================================
# FUNCIONES DE GENERACIÓN DE DATOS POR RUBRO
# ===============================================================

@st.cache_data
def generar_caja():
    """Genera datos de Caja y Bancos"""
    fake_es = Faker('es_AR')
    np.random.seed(42)
    random.seed(42)
    
    num_registros = 50
    responsables = [fake_es.name() for _ in range(10)]
    tipos_transaccion = ['Venta', 'Gasto']
    metodos_pago = ['Efectivo', 'Tarjeta de Débito', 'Tarjeta de Crédito', 'Transferencia']
    saldo = 50000
    registros = []
    
    for i in range(num_registros):
        fecha_hora = fake_es.date_time_between(start_date='-6M', end_date='now')
        tipo = random.choice(tipos_transaccion)
        monto = round(random.uniform(1000, 15000), 2)
        
        if tipo == 'Venta':
            saldo += monto
        else:
            saldo -= monto
        
        registros.append({
            'id_transaccion': i + 1,
            'fecha_hora': fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            'tipo_transaccion': tipo,
            'metodo_pago': random.choice(metodos_pago),
            'monto': monto,
            'saldo_acumulado': round(saldo, 2),
            'responsable': random.choice(responsables)
        })
    
    df = pd.DataFrame(registros)
    df.sort_values(by='fecha_hora', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def generar_inversiones():
    """Genera datos de Inversiones Temporarias"""
    np.random.seed(456)
    random.seed(456)
    fake = Faker('es_AR')
    
    num_inversiones = 30
    tipos = ['Plazo Fijo', 'FCI', 'Acciones', 'Bonos', 'Cauciones']
    
    inversiones = []
    for i in range(num_inversiones):
        fecha_inicio = fake.date_between(start_date='-2y', end_date='today')
        monto_inicial = round(random.uniform(100000, 5000000), 2)
        tasa_anual = round(random.uniform(0.05, 0.15), 4)
        
        inversiones.append({
            'id_inversion': f'INV-{20000 + i}',
            'tipo': random.choice(tipos),
            'fecha_inicio': fecha_inicio,
            'monto_inicial': monto_inicial,
            'tasa_anual': tasa_anual,
            'valor_actual': round(monto_inicial * (1 + tasa_anual * random.uniform(0.8, 1.2)), 2),
            'estado': random.choice(['Activa', 'Liquidada'])
        })
    
    return pd.DataFrame(inversiones)

@st.cache_data
def generar_cuentas_cobrar():
    """Genera datos de Cuentas a Cobrar"""
    np.random.seed(123)
    random.seed(123)
    fake = Faker('es_AR')
    
    num_cuentas = 40
    estados = ['Vigente', 'Vencida', 'Pagada']
    
    cuentas = []
    for i in range(num_cuentas):
        fecha_emision = fake.date_between(start_date='-2y', end_date='-1M')
        plazo = random.choice([30, 60, 90, 120])
        fecha_venc = fecha_emision + timedelta(days=plazo)
        monto_original = round(random.uniform(10000, 250000), 2)
        estado = random.choices(estados, weights=[0.6, 0.3, 0.1])[0]
        
        if estado == 'Pagada':
            monto_cobrado = monto_original
        elif estado == 'Vencida':
            monto_cobrado = round(monto_original * random.uniform(0, 0.5), 2)
        else:
            monto_cobrado = round(monto_original * random.uniform(0, 0.8), 2)
        
        cuentas.append({
            'factura_id': f'FC-{20000 + i}',
            'cliente': fake.company(),
            'fecha_emision': fecha_emision,
            'fecha_vencimiento': fecha_venc,
            'monto_original': monto_original,
            'monto_cobrado': monto_cobrado,
            'saldo_pendiente': round(monto_original - monto_cobrado, 2),
            'estado': estado
        })
    
    return pd.DataFrame(cuentas)

@st.cache_data
def generar_inventarios():
    """Genera datos de Inventarios"""
    np.random.seed(42)
    random.seed(42)
    fake = Faker('es_AR')
    
    categorias = ['Materias Primas', 'Productos en Proceso', 'Productos Terminados']
    num_items = 60
    
    inventario = []
    for i in range(num_items):
        categoria = random.choice(categorias)
        cantidad = round(random.uniform(10, 1000), 2)
        costo_unitario = round(random.uniform(50, 500), 2)
        
        inventario.append({
            'id_item': f'INV-{1000 + i}',
            'categoria': categoria,
            'descripcion': fake.catch_phrase(),
            'cantidad': cantidad,
            'costo_unitario': costo_unitario,
            'valor_total': round(cantidad * costo_unitario, 2),
            'fecha_ingreso': fake.date_between(start_date='-1y', end_date='today')
        })
    
    return pd.DataFrame(inventario)

@st.cache_data
def generar_prepagos():
    """Genera datos de Gastos Pagados por Adelantado"""
    np.random.seed(42)
    random.seed(42)
    fake = Faker('es_AR')
    
    tipos = ['Alquiler', 'Seguro', 'Publicidad', 'Licencias', 'Mantenimiento']
    num_registros = 20
    
    prepagos = []
    for i in range(num_registros):
        fecha_pago = fake.date_between(start_date='-60d', end_date='today')
        duracion_meses = random.choice([1, 3, 6, 12])
        monto_total = round(random.uniform(5000, 200000), 2)
        
        prepagos.append({
            'id_prepago': f'PP-{1000 + i}',
            'tipo': random.choice(tipos),
            'proveedor': fake.company(),
            'fecha_pago': fecha_pago,
            'duracion_meses': duracion_meses,
            'monto_total': monto_total,
            'monto_mensual': round(monto_total / duracion_meses, 2)
        })
    
    return pd.DataFrame(prepagos)

# ===============================================================
# FUNCIONES DE AUDITORÍA
# ===============================================================

def auditoria_isolation_forest(df, features, contamination=0.1):
    """Aplica Isolation Forest para detectar anomalías"""
    X = df[features].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    modelo = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
    df['anomaly_if'] = modelo.fit_predict(X_scaled)
    df['resultado_if'] = df['anomaly_if'].map({1: 'Normal', -1: 'Anómalo'})
    
    return df

def aplicar_reglas_negocio(df, rubro):
    """Aplica reglas heurísticas según el rubro"""
    if rubro == 'Caja':
        df['alerta'] = df.apply(lambda r: 'Saldo negativo' if r.get('saldo_acumulado', 0) < 0 else None, axis=1)
    elif rubro == 'Inversiones':
        df['alerta'] = df.apply(lambda r: 'Pérdida registrada' if r.get('valor_actual', 0) < r.get('monto_inicial', 0) else None, axis=1)
    elif rubro == 'Cuentas a Cobrar':
        hoy = pd.to_datetime('today')
        df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'])
        df['alerta'] = df.apply(lambda r: f"Vencida {(hoy - r['fecha_vencimiento']).days} días" 
                                if r['estado'] == 'Vencida' and r['saldo_pendiente'] > 0 else None, axis=1)
    elif rubro == 'Inventarios':
        df['alerta'] = df.apply(lambda r: 'Cantidad <= 0' if r.get('cantidad', 0) <= 0 else None, axis=1)
    elif rubro == 'Prepagos':
        df['alerta'] = df.apply(lambda r: 'Monto inválido' if r.get('monto_total', 0) <= 0 else None, axis=1)
    
    return df

def generar_resumen_hallazgos(data_dict):
    """Genera resumen de hallazgos para todos los rubros"""
    resumen = []
    total_general = 0
    
    for rubro, df in data_dict.items():
        if 'valor_total' in df.columns:
            total = df['valor_total'].sum()
        elif 'saldo_acumulado' in df.columns:
            total = df['saldo_acumulado'].iloc[-1] if not df.empty else 0
        elif 'saldo_pendiente' in df.columns:
            total = df['saldo_pendiente'].sum()
        elif 'monto_inicial' in df.columns:
            total = df['monto_inicial'].sum()
        else:
            total = 0
        
        cantidad = len(df)
        anomalias = len(df[df.get('resultado_if', pd.Series()) == 'Anómalo']) if 'resultado_if' in df.columns else 0
        
        resumen.append({
            'Rubro': rubro,
            'Cantidad': cantidad,
            'Saldo ($)': round(total, 2),
            'Anomalías': anomalias
        })
        total_general += total
    
    resumen.append({
        'Rubro': 'TOTAL ACTIVOS CORRIENTES',
        'Cantidad': sum(r['Cantidad'] for r in resumen),
        'Saldo ($)': round(total_general, 2),
        'Anomalías': sum(r['Anomalías'] for r in resumen)
    })
    
    return pd.DataFrame(resumen)

# ===============================================================
# INTERFAZ STREAMLIT
# ===============================================================

def main():
    st.title("📊 Sistema de Auditoría de Activos Corrientes")
    st.markdown("### Conforme a RT 7, RT 37 y Normas Internacionales de Auditoría (NIAs)")
    
    st.sidebar.header("⚙️ Configuración de Auditoría")
    empresa_nombre = st.sidebar.text_input("Razón Social", "EMPRESA EJEMPLO S.A.")
    empresa_cuit = st.sidebar.text_input("CUIT", "30-12345678-9")
    fecha_auditoria = st.sidebar.date_input("Fecha de Auditoría", datetime.now())
    
    rubros_seleccionados = st.sidebar.multiselect(
        "Seleccione los rubros:",
        ["Caja y Bancos", "Inversiones Temporarias", "Cuentas a Cobrar", "Inventarios", "Gastos Pagados por Adelantado"],
        default=["Caja y Bancos", "Inversiones Temporarias", "Cuentas a Cobrar"]
    )
    
    if st.sidebar.button("🚀 Iniciar Auditoría Completa", type="primary"):
        with st.spinner('Ejecutando auditoría integral...'):
            data_dict = {}
            if "Caja y Bancos" in rubros_seleccionados:
                df = generar_caja()
                df = auditoria_isolation_forest(df, ['monto', 'saldo_acumulado'])
                df = aplicar_reglas_negocio(df, 'Caja')
                data_dict['Caja y Bancos'] = df
            
            if "Inversiones Temporarias" in rubros_seleccionados:
                df = generar_inversiones()
                df = auditoria_isolation_forest(df, ['monto_inicial', 'tasa_anual', 'valor_actual'])
                df = aplicar_reglas_negocio(df, 'Inversiones')
                data_dict['Inversiones'] = df
            
            if "Cuentas a Cobrar" in rubros_seleccionados:
                df = generar_cuentas_cobrar()
                df = auditoria_isolation_forest(df, ['monto_original', 'saldo_pendiente'])
                df = aplicar_reglas_negocio(df, 'Cuentas a Cobrar')
                data_dict['Cuentas a Cobrar'] = df

            if "Inventarios" in rubros_seleccionados:
                df = generar_inventarios()
                df = auditoria_isolation_forest(df, ['cantidad', 'costo_unitario', 'valor_total'])
                df = aplicar_reglas_negocio(df, 'Inventarios')
                data_dict['Inventarios'] = df

            if "Gastos Pagados por Adelantado" in rubros_seleccionados:
                df = generar_prepagos()
                df = auditoria_isolation_forest(df, ['monto_total', 'monto_mensual'])
                df = aplicar_reglas_negocio(df, 'Prepagos')
                data_dict['Prepagos'] = df

            st.success("✅ Auditoría completada con éxito")
            
            # Resumen Ejecutivo
            st.header("📋 I. Resumen Ejecutivo")
            resumen_df = generar_resumen_hallazgos(data_dict)
            
            col1, col2, col3, col4 = st.columns(4)
            total_row = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES'].iloc[0]
            col1.metric("Total Activos", f"${total_row['Saldo ($)']:,.2f}")
            col2.metric("Items Auditados", int(total_row['Cantidad']))
            col3.metric("Anomalías", int(total_row['Anomalías']))
            col4.metric("% Anomalías", f"{(total_row['Anomalías']/total_row['Cantidad']*100):.1f}%")
            
            st.dataframe(resumen_df, use_container_width=True)
            
            # Hallazgos Detallados
            st.header("🔍 II. Hallazgos Detallados")
            for rubro, df in data_dict.items():
                with st.expander(f"📂 {rubro}"):
                    st.dataframe(df[df['resultado_if'] == 'Anómalo'], use_container_width=True)
                    fig, ax = plt.subplots(figsize=(10, 4))
                    if rubro == 'Caja y Bancos':
                        plt.plot(pd.to_datetime(df['fecha_hora']), df['saldo_acumulado'])
                    else:
                        sns.scatterplot(data=df, x=df.columns[3], y=df.columns[4], hue='resultado_if')
                    st.pyplot(fig)

            # Descargas
            st.header("📥 III. Generación de Informe")
            if st.button("📄 Generar Informe Word (DOCX)"):
                try:
                    generador = GeneradorInformeAuditoria(empresa_nombre, empresa_cuit, fecha_auditoria)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                        generador.generar_informe(resumen_df, data_dict, tmp.name)
                        with open(tmp.name, 'rb') as f:
                            st.download_button("💾 Descargar Informe", f.read(), 
                                             file_name=f"Informe_{empresa_nombre}.docx")
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
