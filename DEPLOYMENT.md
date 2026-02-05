# 🚀 Guía de Deployment en Render

Esta guía explica cómo desplegar el Sistema de Auditoría de Activos Corrientes en Render (similar a https://pasivos-corrientes.onrender.com/)

## 📋 Pre-requisitos

1. Cuenta en GitHub (gratuita)
2. Cuenta en Render (gratuita - https://render.com)
3. Archivos del proyecto

## 🔧 Paso 1: Preparar el Repositorio

### 1.1. Crear repositorio en GitHub

1. Ir a https://github.com y crear un nuevo repositorio
2. Nombre sugerido: `auditoria-activos-corrientes`
3. Descripción: "Sistema profesional de auditoría de activos corrientes"
4. Público o Privado según preferencia

### 1.2. Subir archivos al repositorio

Asegurarse de incluir todos estos archivos:
```
auditoria-activos-corrientes/
├── auditoria_activos_corrientes.py
├── generador_informe.py
├── demo.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

### 1.3. Crear archivo de configuración de Streamlit

Crear carpeta `.streamlit` en la raíz del proyecto y dentro crear `config.toml`:

```toml
[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 10000
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## 🌐 Paso 2: Configurar Render

### 2.1. Crear nuevo Web Service

1. Ir a https://dashboard.render.com
2. Click en "New +" → "Web Service"
3. Conectar con GitHub y seleccionar el repositorio

### 2.2. Configuración del servicio

#### Build & Deploy
- **Name**: `auditoria-activos-corrientes` (o el nombre que prefieras)
- **Region**: Oregon (US West) - o la más cercana
- **Branch**: `main` (o el nombre de tu rama principal)
- **Runtime**: Python 3
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  streamlit run auditoria_activos_corrientes.py --server.port=$PORT --server.address=0.0.0.0
  ```

#### Instance Type
- **Free** (suficiente para demo y uso moderado)
- **Starter** ($7/mes) para mejor rendimiento
- **Standard** ($25/mes) para uso profesional

### 2.3. Variables de Entorno (Opcional)

Si se requieren configuraciones específicas:
```
STREAMLIT_SERVER_PORT=10000
STREAMLIT_SERVER_HEADLESS=true
```

## 🎯 Paso 3: Deploy

1. Click en "Create Web Service"
2. Render comenzará a:
   - Clonar el repositorio
   - Instalar dependencias
   - Iniciar la aplicación

3. El proceso toma 3-5 minutos
4. Una vez completado, la URL estará disponible (ejemplo: `https://auditoria-activos-corrientes.onrender.com`)

## ✅ Verificación

1. Abrir la URL proporcionada por Render
2. Verificar que la aplicación carga correctamente
3. Probar funcionalidades:
   - Selección de rubros
   - Generación de auditoría
   - Descarga de CSV
   - Generación de informe DOCX

## 🔄 Actualizaciones Automáticas

Render detectará automáticamente cambios en GitHub:
1. Hacer cambios en el código localmente
2. Hacer commit y push a GitHub
3. Render detecta el cambio y re-deploya automáticamente

## ⚠️ Consideraciones Importantes

### Limitaciones del Plan Free de Render

- **Sleep después de 15 minutos de inactividad**
  - Primera carga puede tomar 30-60 segundos
  - Solución: Plan Starter ($7/mes) mantiene servicio activo

- **750 horas/mes de uso gratuito**
  - Suficiente para demo y desarrollo
  - Para producción, considerar plan de pago

- **Reinicio cada 24 horas**
  - Datos temporales se pierden
  - Los informes generados deben descargarse inmediatamente

### Optimizaciones

1. **Caché de datos**
   ```python
   @st.cache_data
   def funcion_pesada():
       # Código
   ```

2. **Lazy loading**
   - Cargar datos solo cuando se necesitan
   - No generar todo al inicio

3. **Compresión de recursos**
   - Optimizar imágenes
   - Minimizar datos en memoria

## 🔐 Seguridad en Producción

### Para uso con datos reales:

1. **Autenticación**
   ```python
   import streamlit_authenticator as stauth
   
   authenticator = stauth.Authenticate(
       config['credentials'],
       config['cookie']['name'],
       config['cookie']['key'],
       config['cookie']['expiry_days']
   )
   
   name, authentication_status, username = authenticator.login('Login', 'main')
   
   if authentication_status:
       # Contenido de la app
   ```

2. **Variables de entorno para secretos**
   - No incluir credenciales en el código
   - Usar variables de entorno en Render

3. **HTTPS**
   - Render proporciona HTTPS automáticamente
   - No requiere configuración adicional

4. **Backup de datos**
   - Implementar exportación automática
   - Almacenamiento externo (AWS S3, etc.)

## 📊 Monitoreo

### Logs en Render

1. Ir al dashboard del servicio
2. Tab "Logs" muestra toda la actividad
3. Útil para debugging

### Métricas

Render proporciona:
- CPU usage
- Memory usage
- Bandwidth
- Response time

## 🆘 Troubleshooting

### Error: "Application failed to start"

**Causa**: Dependencias faltantes o incorrectas

**Solución**: 
- Verificar `requirements.txt`
- Agregar versiones específicas
- Revisar logs de build

### Error: "Port binding failed"

**Causa**: Puerto incorrecto

**Solución**: 
```bash
streamlit run app.py --server.port=$PORT
```

### Error: "Out of memory"

**Causa**: Plan Free tiene 512MB RAM

**Solución**:
- Optimizar código
- Reducir datos en memoria
- Upgrade a plan Starter

### Aplicación muy lenta

**Causa**: Sleep en plan Free

**Solución**:
- Upgrade a plan de pago
- O aceptar delay inicial

## 💡 Tips Adicionales

### Custom Domain

1. En Render, ir a Settings → Custom Domains
2. Agregar dominio (ej: `auditoria.tuempresa.com`)
3. Configurar DNS según instrucciones
4. Render provisiona SSL automáticamente

### Múltiples Ambientes

Crear servicios separados:
- `auditoria-activos-dev` (desarrollo)
- `auditoria-activos-staging` (testing)
- `auditoria-activos-prod` (producción)

### Backup Automático

Configurar GitHub Actions para:
- Backup de configuraciones
- Tests automáticos antes de deploy
- Notificaciones de deploy

## 📚 Recursos Adicionales

- Documentación oficial de Render: https://render.com/docs
- Documentación de Streamlit: https://docs.streamlit.io
- Deploy Streamlit en Render: https://docs.streamlit.io/deploy/tutorials/render

## 🎓 Ejemplo Completo

URL del proyecto de referencia: https://pasivos-corrientes.onrender.com/

Características implementadas:
- ✅ Deploy automático desde GitHub
- ✅ HTTPS automático
- ✅ Logs en tiempo real
- ✅ Reinicio automático en caso de error
- ✅ Escalado según tráfico (planes de pago)

---

**¿Necesitas ayuda?**

Si encuentras problemas durante el deployment:
1. Revisar logs en Render Dashboard
2. Verificar que todas las dependencias estén en requirements.txt
3. Asegurar que el código funciona localmente primero
4. Consultar documentación oficial de Render

---

**Fecha de creación**: 05/02/2026
**Versión del sistema**: 1.0
