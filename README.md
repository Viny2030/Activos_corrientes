# 📊 Sistema de Auditoría de Activos Corrientes

Sistema profesional de auditoría de activos corrientes conforme a **RT 7**, **RT 37** y **Normas Internacionales de Auditoría (NIAs)**.

## 🎯 Características Principales

### Rubros Auditados
- ✅ **Caja y Bancos**: Análisis de transacciones y saldos
- ✅ **Inversiones Temporarias**: Evaluación de rentabilidad y valuación
- ✅ **Cuentas a Cobrar**: Antigüedad y recuperabilidad
- ✅ **Inventarios**: Materias primas, productos en proceso y terminados
- ✅ **Gastos Pagados por Adelantado**: Devengamiento y vigencia

### Técnicas de Auditoría

#### 1. Machine Learning
- **Isolation Forest**: Detección de anomalías en valores atípicos
- **Local Outlier Factor (LOF)**: Identificación de outliers locales
- Análisis multivariado de características financieras

#### 2. Reglas Heurísticas de Negocio
- Validación de saldos negativos
- Verificación de vencimientos
- Control de consistencia de datos
- Alertas automáticas por criterios de riesgo

#### 3. Normativa Profesional
- **RT 7**: Normas de auditoría
- **RT 37**: Normas de auditoría, revisión, otros encargos de aseguramiento
- **NIAs**: Normas Internacionales de Auditoría
- **RT 17**: Normas contables profesionales
- **RT 31**: Valuación de inventarios

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run auditoria_activos_corrientes.py
```

4. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📖 Uso del Sistema

### 1. Configuración Inicial
En el panel lateral:
- Ingresar **Razón Social** de la empresa
- Ingresar **CUIT**
- Seleccionar **Fecha de Auditoría**
- Elegir **Rubros a Auditar**

### 2. Ejecución de Auditoría
- Hacer clic en "🚀 Iniciar Auditoría Completa"
- El sistema generará datos simulados y aplicará todos los análisis
- Visualizar resultados en pantalla

### 3. Generación de Informes

#### Informe Excel (CSV)
- Click en "📊 Descargar Resumen (CSV)"
- Archivo descargable con resumen consolidado

#### Informe Profesional (DOCX)
- Click en "📄 Generar Informe Completo (DOCX)"
- Documento Word con:
  - Portada profesional
  - Identificación del ente
  - Alcance del trabajo
  - Resumen de hallazgos
  - Hallazgos específicos por rubro
  - Opinión profesional
  - Firmas
  - Anexos con detalles

## 📊 Estructura del Informe

### Secciones del Informe DOCX

1. **Portada**
   - Título del informe
   - Datos de la empresa
   - Período auditado
   - Normas aplicadas

2. **Identificación del Ente y Período**
   - Descripción del alcance
   - Marco normativo

3. **Alcance del Trabajo**
   - Procedimientos aplicados según RT 7
   - Técnicas de auditoría utilizadas
   - Evaluación de controles internos

4. **Resumen de Hallazgos**
   - Tabla consolidada por rubro
   - Importes totales
   - Porcentajes sobre total

5. **Hallazgos Específicos por Rubro**
   - Análisis detallado
   - Anomalías detectadas
   - Recomendaciones profesionales

6. **Opinión Profesional**
   - Opinión del auditor (sin salvedades / con salvedades / adversa)
   - Fundamentación según NIAs

7. **Firmas**
   - Contador Público
   - Matrícula profesional

8. **Anexos**
   - Detalle de items con observaciones
   - Listados específicos

## 🔧 Personalización

### Agregar Nuevos Rubros

1. Crear función generadora de datos en `auditoria_activos_corrientes.py`:
```python
@st.cache_data
def generar_nuevo_rubro():
    # Lógica de generación
    return pd.DataFrame(datos)
```

2. Agregar al diccionario de datos en el flujo principal:
```python
if "Nuevo Rubro" in rubros_seleccionados:
    df_nuevo = generar_nuevo_rubro()
    df_nuevo = auditoria_isolation_forest(df_nuevo, ['campo1', 'campo2'])
    df_nuevo = aplicar_reglas_negocio(df_nuevo, 'Nuevo Rubro')
    data_dict['Nuevo Rubro'] = df_nuevo
```

### Modificar Reglas de Negocio

Editar la función `aplicar_reglas_negocio()` agregando nuevos criterios:
```python
elif rubro == 'Mi Rubro':
    df['alerta'] = df.apply(lambda r: 
        'Mi condición' if r['campo'] > umbral else None, 
        axis=1)
```

### Ajustar Sensibilidad de Anomalías

Modificar el parámetro `contamination` en la función `auditoria_isolation_forest()`:
```python
# Más estricto (menos anomalías)
contamination=0.05

# Menos estricto (más anomalías)
contamination=0.15
```

## 📚 Marco Normativo

### Resoluciones Técnicas FACPCE

- **RT 7**: Normas de auditoría
- **RT 17**: Normas contables profesionales - Desarrollo de cuestiones de aplicación general
- **RT 31**: Modificación de la RT 17 - Normas contables profesionales: desarrollo de cuestiones de aplicación particular - Inventarios
- **RT 37**: Normas de auditoría, revisión, otros encargos de aseguramiento, certificación y servicios relacionados

### Normas Internacionales de Auditoría (NIAs)

- **NIA 200**: Objetivos globales del auditor independiente
- **NIA 315**: Identificación y valoración de riesgos
- **NIA 330**: Respuestas del auditor a los riesgos valorados
- **NIA 500**: Evidencia de auditoría
- **NIA 505**: Confirmaciones externas
- **NIA 520**: Procedimientos analíticos
- **NIA 530**: Muestreo de auditoría

## 🎓 Procedimientos de Auditoría Aplicados

### Según RT 7

1. **Confirmaciones externas**
   - Circularización de bancos
   - Confirmación de saldos con clientes
   - Verificación con custodios de inversiones

2. **Inspección de documentación**
   - Análisis de comprobantes
   - Revisión de contratos
   - Verificación de conciliaciones

3. **Pruebas de corte**
   - Verificación de registros al cierre
   - Análisis de eventos posteriores

4. **Procedimientos analíticos**
   - Análisis de ratios
   - Comparaciones con períodos anteriores
   - Técnicas de Machine Learning

5. **Evaluación de controles internos**
   - Pruebas de controles
   - Evaluación de segregación de funciones
   - Análisis de autorizaciones

## 🤖 Algoritmos de Machine Learning

### Isolation Forest
- **Propósito**: Detectar anomalías globales
- **Ventaja**: Eficiente con grandes volúmenes de datos
- **Uso**: Identificación de valores atípicos en importes y saldos

### Local Outlier Factor (LOF)
- **Propósito**: Detectar anomalías locales
- **Ventaja**: Identifica outliers en contextos específicos
- **Uso**: Análisis de densidad de datos por categorías

### Criterios de Detección
- Contamination: 10% (configurable)
- Features: Variables numéricas relevantes
- Normalización: StandardScaler

## 📈 Visualizaciones

El sistema genera automáticamente:
- Gráficos de evolución temporal
- Distribuciones por categoría
- Scatter plots de anomalías
- Gráficos de barras comparativos
- Histogramas de distribución

## ⚠️ Limitaciones

1. **Datos Simulados**: El sistema genera datos de ejemplo. Para uso en producción, conectar con bases de datos reales.

2. **Validación Manual**: Los hallazgos automáticos requieren validación profesional del auditor.

3. **Marco Legal**: El informe debe ser revisado y firmado por un Contador Público matriculado.

4. **Personalización**: Cada empresa puede requerir ajustes específicos en reglas y criterios.

## 🔐 Seguridad y Confidencialidad

- No almacena datos reales en el sistema
- Todos los datos generados son ficticios
- Para uso con datos reales, implementar controles de acceso
- Cumplir con normativa de protección de datos personales (Ley 25.326)

## 📞 Soporte y Contacto

Para consultas sobre:
- Normativa profesional: Consultar con FACPCE o Consejo Profesional local
- Aspectos técnicos: Revisar documentación de librerías utilizadas
- Implementación específica: Adaptar código según necesidades

## 📝 Licencia

Este sistema es una herramienta de auditoría profesional. Su uso debe realizarse bajo la supervisión de un Contador Público matriculado.

## 🔄 Actualizaciones

### Versión 1.0
- ✅ Auditoría de 5 rubros de activos corrientes
- ✅ Algoritmos de Machine Learning
- ✅ Generación de informes DOCX profesionales
- ✅ Visualizaciones interactivas
- ✅ Conforme a RT 7, RT 37 y NIAs

### Próximas Versiones
- 🔲 Conexión con bases de datos reales
- 🔲 Importación de archivos Excel/CSV
- 🔲 Más rubros de auditoría
- 🔲 Dashboard ejecutivo
- 🔲 Exportación a PDF
- 🔲 Sistema de usuarios y permisos

---

**Desarrollado con criterios profesionales de auditoría y tecnología de análisis de datos**
