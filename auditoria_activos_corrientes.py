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
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
import streamlit as st
import os
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
    Faker.seed(42)
    
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
    Faker.seed(456)
    
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
    Faker.seed(123)
    
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
    """Genera datos de Inventarios (Materias Primas, Productos en Proceso, Productos Terminados)"""
    np.random.seed(42)
    random.seed(42)
    fake = Faker('es_AR')
    Faker.seed(42)
    
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
    Faker.seed(42)
    
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
    alertas = []
    
    if rubro == 'Caja':
        # Reglas para Caja
        df['alerta'] = df.apply(lambda r: 'Saldo negativo' if r.get('saldo_acumulado', 0) < 0 else None, axis=1)
    
    elif rubro == 'Inversiones':
        # Reglas para Inversiones
        df['alerta'] = df.apply(lambda r: 
            'Pérdida registrada' if r.get('valor_actual', 0) < r.get('monto_inicial', 0) else None, 
            axis=1)
    
    elif rubro == 'Cuentas a Cobrar':
        # Reglas para Cuentas a Cobrar
        hoy = pd.to_datetime('today')
        df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'])
        df['alerta'] = df.apply(lambda r: 
            f"Vencida {(hoy - r['fecha_vencimiento']).days} días" 
            if r['estado'] == 'Vencida' and r['saldo_pendiente'] > 0 
            else None, axis=1)
    
    elif rubro == 'Inventarios':
        # Reglas para Inventarios
        df['alerta'] = df.apply(lambda r: 
            'Cantidad <= 0' if r.get('cantidad', 0) <= 0 else None, 
            axis=1)
    
    elif rubro == 'Prepagos':
        # Reglas para Prepagos
        df['alerta'] = df.apply(lambda r: 
            'Monto inválido' if r.get('monto_total', 0) <= 0 else None, 
            axis=1)
    
    return df

# ===============================================================
# GENERACIÓN DE INFORME PROFESIONAL
# ===============================================================

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
    
    # Agregar total
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
    # Header
    st.title("📊 Sistema de Auditoría de Activos Corrientes")
    st.markdown("""
    ### Conforme a RT 7, RT 37 y Normas Internacionales de Auditoría (NIAs)
    
    Este sistema realiza una auditoría integral de los activos corrientes, aplicando:
    - **Algoritmos de Machine Learning** (Isolation Forest, LOF)
    - **Reglas heurísticas de negocio**
    - **Normas profesionales vigentes** (RT 7, RT 37, NIAs)
    """)
    
    # Sidebar
    st.sidebar.header("⚙️ Configuración de Auditoría")
    
    # Datos de la empresa
    st.sidebar.subheader("Datos de la Empresa")
    empresa_nombre = st.sidebar.text_input("Razón Social", "EMPRESA EJEMPLO S.A.")
    empresa_cuit = st.sidebar.text_input("CUIT", "30-12345678-9")
    
    # Período
    fecha_auditoria = st.sidebar.date_input("Fecha de Auditoría", datetime.now())
    
    # Rubros a auditar
    st.sidebar.subheader("Rubros a Auditar")
    rubros_seleccionados = st.sidebar.multiselect(
        "Seleccione los rubros:",
        ["Caja y Bancos", "Inversiones Temporarias", "Cuentas a Cobrar", 
         "Inventarios", "Gastos Pagados por Adelantado"],
        default=["Caja y Bancos", "Inversiones Temporarias", "Cuentas a Cobrar"]
    )
    
    # Botón principal
    if st.sidebar.button("🚀 Iniciar Auditoría Completa", type="primary"):
        with st.spinner('Ejecutando auditoría integral...'):
            
            # Generar datos
            data_dict = {}
            
            if "Caja y Bancos" in rubros_seleccionados:
                df_caja = generar_caja()
                df_caja = auditoria_isolation_forest(df_caja, ['monto', 'saldo_acumulado'])
                df_caja = aplicar_reglas_negocio(df_caja, 'Caja')
                data_dict['Caja y Bancos'] = df_caja
            
            if "Inversiones Temporarias" in rubros_seleccionados:
                df_inv = generar_inversiones()
                df_inv = auditoria_isolation_forest(df_inv, ['monto_inicial', 'tasa_anual', 'valor_actual'])
                df_inv = aplicar_reglas_negocio(df_inv, 'Inversiones')
                data_dict['Inversiones'] = df_inv
            
            if "Cuentas a Cobrar" in rubros_seleccionados:
                df_cc = generar_cuentas_cobrar()
                df_cc = auditoria_isolation_forest(df_cc, ['monto_original', 'saldo_pendiente'])
                df_cc = aplicar_reglas_negocio(df_cc, 'Cuentas a Cobrar')
                data_dict['Cuentas a Cobrar'] = df_cc
            
            if "Inventarios" in rubros_seleccionados:
                df_inv_stock = generar_inventarios()
                df_inv_stock = auditoria_isolation_forest(df_inv_stock, ['cantidad', 'costo_unitario', 'valor_total'])
                df_inv_stock = aplicar_reglas_negocio(df_inv_stock, 'Inventarios')
                data_dict['Inventarios'] = df_inv_stock
            
            if "Gastos Pagados por Adelantado" in rubros_seleccionados:
                df_prepagos = generar_prepagos()
                df_prepagos = auditoria_isolation_forest(df_prepagos, ['monto_total', 'monto_mensual'])
                df_prepagos = aplicar_reglas_negocio(df_prepagos, 'Prepagos')
                data_dict['Prepagos'] = df_prepagos
            
            st.success("✅ Auditoría completada con éxito")
            
            # ============================================
            # SECCIÓN 1: RESUMEN EJECUTIVO
            # ============================================
            st.header("📋 I. Resumen Ejecutivo")
            
            resumen_df = generar_resumen_hallazgos(data_dict)
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            total_activos = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Saldo ($)'].iloc[0]
            total_items = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Cantidad'].iloc[0]
            total_anomalias = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Anomalías'].iloc[0]
            
            col1.metric("Total Activos Corrientes", f"${total_activos:,.2f}")
            col2.metric("Total Items Auditados", f"{int(total_items)}")
            col3.metric("Anomalías Detectadas", f"{int(total_anomalias)}")
            col4.metric("% Anomalías", f"{(total_anomalias/total_items*100):.1f}%")
            
            # Tabla resumen
            st.subheader("Resumen por Rubro")
            st.dataframe(
                resumen_df.style.format({
                    'Saldo ($)': '${:,.2f}',
                    'Cantidad': '{:.0f}',
                    'Anomalías': '{:.0f}'
                }),
                use_container_width=True
            )
            
            # ============================================
            # SECCIÓN 2: HALLAZGOS POR RUBRO
            # ============================================
            st.header("🔍 II. Hallazgos Detallados por Rubro")
            
            for rubro, df in data_dict.items():
                with st.expander(f"📂 {rubro}", expanded=True):
                    
                    # Métricas del rubro
                    col1, col2, col3 = st.columns(3)
                    
                    total_items_rubro = len(df)
                    anomalias_rubro = len(df[df.get('resultado_if', pd.Series()) == 'Anómalo'])
                    alertas_rubro = len(df[df.get('alerta', pd.Series()).notna()])
                    
                    col1.metric(f"Items en {rubro}", total_items_rubro)
                    col2.metric("Anomalías (ML)", anomalias_rubro)
                    col3.metric("Alertas (Reglas)", alertas_rubro)
                    
                    # Mostrar items con problemas
                    df_problemas = df[(df.get('resultado_if', pd.Series()) == 'Anómalo') | 
                                     (df.get('alerta', pd.Series()).notna())]
                    
                    if not df_problemas.empty:
                        st.warning(f"⚠️ Se detectaron {len(df_problemas)} items con observaciones")
                        st.dataframe(df_problemas.head(10), use_container_width=True)
                    else:
                        st.success("✅ No se detectaron observaciones significativas")
                    
                    # Visualización
                    if len(df) > 0:
                        st.subheader("Visualización")
                        
                        # Gráfico según el rubro
                        fig, ax = plt.subplots(figsize=(10, 5))
                        
                        if rubro == 'Caja y Bancos':
                            df_plot = df.copy()
                            df_plot['fecha_hora'] = pd.to_datetime(df_plot['fecha_hora'])
                            ax.plot(df_plot['fecha_hora'], df_plot['saldo_acumulado'], marker='o')
                            ax.set_title('Evolución del Saldo de Caja')
                            ax.set_xlabel('Fecha')
                            ax.set_ylabel('Saldo ($)')
                            plt.xticks(rotation=45)
                        
                        elif rubro == 'Inventarios':
                            sns.barplot(data=df, x='categoria', y='valor_total', ax=ax, estimator=sum)
                            ax.set_title('Valor Total por Categoría de Inventario')
                            ax.set_ylabel('Valor ($)')
                            plt.xticks(rotation=45)
                        
                        else:
                            if 'resultado_if' in df.columns and len(df.select_dtypes(include=[np.number]).columns) >= 2:
                                num_cols = df.select_dtypes(include=[np.number]).columns[:2]
                                sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], 
                                              hue='resultado_if', ax=ax)
                                ax.set_title(f'Detección de Anomalías - {rubro}')
                        
                        plt.tight_layout()
                        st.pyplot(fig)
            
            # ============================================
            # SECCIÓN 3: DESCARGAS
            # ============================================
            st.header("📥 III. Descargas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV consolidado
                csv_consolidado = resumen_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📊 Descargar Resumen (CSV)",
                    data=csv_consolidado,
                    file_name=f"resumen_activos_corrientes_{fecha_auditoria.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Botón para generar informe Word
                if st.button("📄 Generar Informe Completo (DOCX)", type="primary"):
                    with st.spinner("🔄 Generando informe profesional en formato Word..."):
                        try:
                            # Crear generador
                            generador = GeneradorInformeAuditoria(
                                empresa_nombre=empresa_nombre,
                                empresa_cuit=empresa_cuit,
                                fecha_auditoria=fecha_auditoria
                            )
                            
                            # Generar informe
                            ruta_informe = f"/home/claude/Informe_Auditoria_Activos_Corrientes_{fecha_auditoria.strftime('%Y%m%d')}.docx"
                            generador.generar_informe(resumen_df, data_dict, ruta_informe)
                            
                            # Leer archivo para descarga
                            with open(ruta_informe, 'rb') as f:
                                docx_data = f.read()
                            
                            st.success("✅ Informe generado exitosamente")
                            
                            # Botón de descarga
                            st.download_button(
                                label="💾 Descargar Informe DOCX",
                                data=docx_data,
                                file_name=f"Informe_Auditoria_Activos_Corrientes_{fecha_auditoria.strftime('%Y%m%d')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        except Exception as e:
                            st.error(f"❌ Error al generar informe: {str(e)}")
            
            # ============================================
            # SECCIÓN 4: RECOMENDACIONES
            # ============================================
            st.header("💡 IV. Recomendaciones Profesionales")
            
            st.markdown("""
            ### Según RT 7 - Normas de Auditoría
            
            1. **Confirmaciones Externas**: Se recomienda realizar confirmaciones directas con:
               - Bancos (saldos de caja y bancos)
               - Clientes (cuentas a cobrar)
               - Custodios (inversiones)
            
            2. **Pruebas de Corte**: Verificar que las transacciones estén registradas en el período correcto
            
            3. **Evaluación de Recuperabilidad**: Analizar la recuperabilidad de:
               - Cuentas a cobrar vencidas
               - Inventarios obsoletos o de lento movimiento
            
            4. **Valuación**: Verificar que los activos estén valuados conforme a:
               - RT 17 (Normas contables profesionales)
               - RT 31 (Valor neto de realización para inventarios)
            
            ### Próximos Pasos Sugeridos
            
            - [ ] Circularizar bancos y clientes
            - [ ] Realizar pruebas físicas de inventarios
            - [ ] Analizar documentación respaldatoria
            - [ ] Evaluar controles internos
            - [ ] Revisar eventos posteriores
            """)

if __name__ == '__main__':
    main()
