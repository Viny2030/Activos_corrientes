"""
SCRIPT DE DEMOSTRACIÓN
Genera un informe de auditoría de ejemplo sin necesidad de interfaz Streamlit
"""

from datetime import datetime
from generador_informe import GeneradorInformeAuditoria
import pandas as pd
import numpy as np

def demo_generacion_informe():
    """Genera un informe de auditoría de demostración"""
    
    print("=" * 60)
    print("DEMOSTRACIÓN - GENERADOR DE INFORMES DE AUDITORÍA")
    print("=" * 60)
    
    # Datos de la empresa
    empresa_nombre = "EMPRESA EJEMPLO S.A."
    empresa_cuit = "30-12345678-9"
    fecha_auditoria = datetime.now()
    
    print(f"\nEmpresa: {empresa_nombre}")
    print(f"CUIT: {empresa_cuit}")
    print(f"Fecha: {fecha_auditoria.strftime('%d/%m/%Y')}")
    
    # Crear resumen simulado
    resumen_data = {
        'Rubro': [
            'Caja y Bancos',
            'Inversiones Temporarias',
            'Cuentas a Cobrar',
            'Inventarios',
            'Gastos Pagados por Adelantado',
            'TOTAL ACTIVOS CORRIENTES'
        ],
        'Cantidad': [50, 30, 40, 60, 20, 200],
        'Saldo ($)': [450000, 2500000, 1800000, 3200000, 350000, 8300000],
        'Anomalías': [3, 2, 5, 4, 1, 15]
    }
    
    resumen_df = pd.DataFrame(resumen_data)
    
    print("\n" + "=" * 60)
    print("RESUMEN DE ACTIVOS CORRIENTES")
    print("=" * 60)
    print(resumen_df.to_string(index=False))
    
    # Crear datos de ejemplo para cada rubro
    data_dict = {}
    
    # Caja y Bancos
    df_caja = pd.DataFrame({
        'id_transaccion': range(1, 51),
        'fecha_hora': pd.date_range('2026-01-01', periods=50, freq='D'),
        'tipo_transaccion': np.random.choice(['Venta', 'Gasto'], 50),
        'monto': np.random.uniform(1000, 15000, 50),
        'saldo_acumulado': np.cumsum(np.random.uniform(-5000, 10000, 50)),
        'resultado_if': np.random.choice(['Normal', 'Anómalo'], 50, p=[0.94, 0.06]),
        'alerta': [None] * 47 + ['Saldo negativo', None, 'Saldo negativo']
    })
    data_dict['Caja y Bancos'] = df_caja
    
    # Inversiones
    df_inv = pd.DataFrame({
        'id_inversion': [f'INV-{i}' for i in range(20000, 20030)],
        'tipo': np.random.choice(['Plazo Fijo', 'FCI', 'Acciones'], 30),
        'monto_inicial': np.random.uniform(100000, 5000000, 30),
        'valor_actual': np.random.uniform(100000, 5200000, 30),
        'resultado_if': np.random.choice(['Normal', 'Anómalo'], 30, p=[0.93, 0.07]),
        'alerta': [None] * 28 + ['Pérdida registrada', None]
    })
    data_dict['Inversiones Temporarias'] = df_inv
    
    # Cuentas a Cobrar
    df_cc = pd.DataFrame({
        'factura_id': [f'FC-{i}' for i in range(20000, 20040)],
        'cliente': [f'Cliente {i}' for i in range(1, 41)],
        'monto_original': np.random.uniform(10000, 250000, 40),
        'saldo_pendiente': np.random.uniform(0, 200000, 40),
        'estado': np.random.choice(['Vigente', 'Vencida', 'Pagada'], 40, p=[0.6, 0.3, 0.1]),
        'resultado_if': np.random.choice(['Normal', 'Anómalo'], 40, p=[0.88, 0.12]),
        'alerta': [None] * 35 + ['Vencida 120 días'] * 3 + [None, None]
    })
    data_dict['Cuentas a Cobrar'] = df_cc
    
    # Inventarios
    df_inv_stock = pd.DataFrame({
        'id_item': [f'INV-{i}' for i in range(1000, 1060)],
        'categoria': np.random.choice(['Materias Primas', 'Productos en Proceso', 'Productos Terminados'], 60),
        'descripcion': [f'Item {i}' for i in range(1, 61)],
        'cantidad': np.random.uniform(10, 1000, 60),
        'valor_total': np.random.uniform(5000, 50000, 60),
        'resultado_if': np.random.choice(['Normal', 'Anómalo'], 60, p=[0.93, 0.07]),
        'alerta': [None] * 56 + ['Cantidad <= 0'] * 2 + [None, None]
    })
    data_dict['Inventarios'] = df_inv_stock
    
    # Prepagos
    df_prepagos = pd.DataFrame({
        'id_prepago': [f'PP-{i}' for i in range(1000, 1020)],
        'tipo': np.random.choice(['Alquiler', 'Seguro', 'Publicidad'], 20),
        'monto_total': np.random.uniform(5000, 200000, 20),
        'monto_mensual': np.random.uniform(500, 20000, 20),
        'resultado_if': np.random.choice(['Normal', 'Anómalo'], 20, p=[0.95, 0.05]),
        'alerta': [None] * 19 + ['Monto inválido']
    })
    data_dict['Gastos Pagados por Adelantado'] = df_prepagos
    
    # Generar informe
    print("\n" + "=" * 60)
    print("GENERANDO INFORME...")
    print("=" * 60)
    
    generador = GeneradorInformeAuditoria(
        empresa_nombre=empresa_nombre,
        empresa_cuit=empresa_cuit,
        fecha_auditoria=fecha_auditoria
    )
    
    ruta_salida = "/home/claude/Informe_Demo_Auditoria_Activos_Corrientes.docx"
    generador.generar_informe(resumen_df, data_dict, ruta_salida)
    
    print(f"\n✅ Informe generado exitosamente en:")
    print(f"   {ruta_salida}")
    
    print("\n" + "=" * 60)
    print("CARACTERÍSTICAS DEL INFORME")
    print("=" * 60)
    print("✓ Portada profesional")
    print("✓ Identificación del ente y período")
    print("✓ Alcance del trabajo según RT 7")
    print("✓ Resumen de hallazgos con tabla")
    print("✓ Hallazgos específicos por rubro")
    print("✓ Opinión profesional")
    print("✓ Firmas")
    print("✓ Anexos con detalles")
    
    print("\n" + "=" * 60)
    print("CONFORMIDAD NORMATIVA")
    print("=" * 60)
    print("✓ RT 7 - Normas de auditoría")
    print("✓ RT 37 - Normas de aseguramiento")
    print("✓ NIAs - Normas Internacionales de Auditoría")
    print("✓ RT 17 - Normas contables profesionales")
    print("✓ RT 31 - Valuación de inventarios")
    
    print("\n" + "=" * 60)
    
    return ruta_salida

if __name__ == "__main__":
    try:
        demo_generacion_informe()
        print("\n🎉 Demostración completada exitosamente")
    except Exception as e:
        print(f"\n❌ Error en la demostración: {str(e)}")
        raise
