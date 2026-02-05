#!/usr/bin/env python3
"""
Script de test para verificar que la generación de informes funciona correctamente
"""

import tempfile
import os
from datetime import datetime
import pandas as pd
import numpy as np

print("=" * 60)
print("TEST DE GENERACIÓN DE INFORMES")
print("=" * 60)

# Test 1: Importaciones
print("\n1. Verificando importaciones...")
try:
    from generador_informe import GeneradorInformeAuditoria
    print("   ✅ generador_informe importado correctamente")
except Exception as e:
    print(f"   ❌ Error al importar: {e}")
    exit(1)

# Test 2: Creación de datos de prueba
print("\n2. Creando datos de prueba...")
resumen_data = {
    'Rubro': ['Caja y Bancos', 'TOTAL ACTIVOS CORRIENTES'],
    'Cantidad': [10, 10],
    'Saldo ($)': [100000, 100000],
    'Anomalías': [1, 1]
}
resumen_df = pd.DataFrame(resumen_data)

data_dict = {
    'Caja y Bancos': pd.DataFrame({
        'id_transaccion': range(1, 11),
        'monto': np.random.uniform(1000, 5000, 10),
        'resultado_if': ['Normal'] * 9 + ['Anómalo'],
        'alerta': [None] * 9 + ['Test']
    })
}
print("   ✅ Datos de prueba creados")

# Test 3: Verificación de directorio temporal
print("\n3. Verificando directorio temporal...")
try:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        test_path = tmp.name
    print(f"   ✅ Directorio temporal disponible: {os.path.dirname(test_path)}")
    os.unlink(test_path)
except Exception as e:
    print(f"   ❌ Error con directorio temporal: {e}")
    exit(1)

# Test 4: Generación de informe
print("\n4. Generando informe de prueba...")
try:
    generador = GeneradorInformeAuditoria(
        empresa_nombre="EMPRESA TEST S.A.",
        empresa_cuit="30-12345678-9",
        fecha_auditoria=datetime.now()
    )
    print("   ✅ Generador creado")
    
    # Usar directorio temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        ruta_informe = tmp.name
    
    generador.generar_informe(resumen_df, data_dict, ruta_informe)
    print(f"   ✅ Informe generado en: {ruta_informe}")
    
    # Verificar que existe
    if os.path.exists(ruta_informe):
        size = os.path.getsize(ruta_informe)
        print(f"   ✅ Archivo creado correctamente ({size} bytes)")
        os.unlink(ruta_informe)
    else:
        print("   ❌ Archivo no se generó")
        exit(1)
        
except Exception as e:
    print(f"   ❌ Error al generar informe: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
print("=" * 60)
print("\nEl sistema está listo para funcionar en Render")
