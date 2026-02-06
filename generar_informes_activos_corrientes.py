"""
GENERADOR DE INFORMES DE AUDITORÍA EN PDF - ACTIVOS CORRIENTES
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os


class GeneradorInformePDFActivosCorrientes:
    """Genera informes de auditoría en formato PDF para Activos Corrientes"""
    
    def __init__(self, año):
        self.año = año
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
    
    def _crear_estilos_personalizados(self):
        """Crea estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='TituloPortada',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Justificado',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
    
    def _crear_portada(self):
        """Crea la portada"""
        elementos = []
        elementos.append(Spacer(1, 3*cm))
        
        titulo = Paragraph(
            "INFORME DE AUDITORÍA ALGORÍTMICA",
            self.styles['TituloPortada']
        )
        elementos.append(titulo)
        elementos.append(Spacer(1, 0.5*cm))
        
        subtitulo = Paragraph(
            f"ANÁLISIS DE ACTIVOS CORRIENTES - AÑO {self.año}",
            self.styles['Subtitulo']
        )
        elementos.append(subtitulo)
        elementos.append(Spacer(1, 2*cm))
        
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        info = f"""
        <b>Fecha de Emisión:</b> {fecha_actual}<br/>
        <b>Período Analizado:</b> Ejercicio Fiscal {self.año}<br/>
        <b>Responsable:</b> Sistema de Auditoría Algorítmica<br/>
        <b>Versión:</b> 1.0
        """
        elementos.append(Paragraph(info, self.styles['Normal']))
        elementos.append(PageBreak())
        return elementos
    
    def _crear_resumen(self):
        """Crea el resumen ejecutivo"""
        elementos = []
        elementos.append(Paragraph("RESUMEN EJECUTIVO", self.styles['Subtitulo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Datos simulados que varían por año
        factor = 1 + (self.año - 2020) * 0.10
        
        texto = f"""
        El presente informe corresponde al análisis algorítmico de los <b>Activos Corrientes</b> 
        del ejercicio fiscal {self.año}, realizado mediante técnicas avanzadas de machine learning 
        y conforme a las RT 7, RT 37 y Normas Internacionales de Auditoría (NIAs).
        <br/><br/>
        <b>Componentes Analizados:</b>
        <br/><br/>
        • <b>Caja y Bancos:</b> 50 transacciones por ${2500000 * factor:,.0f}
        <br/>
        • <b>Inversiones Temporarias:</b> 30 inversiones valoradas en ${4800000 * factor:,.0f}
        <br/>
        • <b>Cuentas a Cobrar:</b> 40 facturas por ${6200000 * factor:,.0f}
        <br/>
        • <b>Inventarios:</b> 60 items valorados en ${8500000 * factor:,.0f}
        <br/>
        • <b>Gastos Pagados por Adelantado:</b> 20 registros por ${450000 * factor:,.0f}
        <br/><br/>
        <b>Total de Activos Corrientes:</b> ${(2500000 + 4800000 + 6200000 + 8500000 + 450000) * factor:,.0f}
        <br/><br/>
        Se detectaron anomalías en {4 + self.año % 4} registros mediante el algoritmo Isolation Forest, 
        requiriendo revisión adicional por parte del equipo de auditoría.
        """
        
        elementos.append(Paragraph(texto, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.5*cm))
        return elementos
    
    def _crear_analisis_componentes(self):
        """Crea el análisis de componentes"""
        elementos = []
        elementos.append(Paragraph("ANÁLISIS POR COMPONENTE", self.styles['Subtitulo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Caja y Bancos
        texto_caja = """
        <b>1. CAJA Y BANCOS</b>
        <br/><br/>
        Se analizaron 50 transacciones del período, aplicando algoritmos de detección de anomalías 
        para identificar movimientos atípicos en montos y frecuencias. El saldo acumulado presenta 
        un comportamiento consistente con el nivel de operaciones de la empresa.
        <br/><br/>
        <b>Hallazgos:</b> Se detectó 1 transacción con monto significativamente superior al promedio 
        que requiere documentación adicional.
        """
        elementos.append(Paragraph(texto_caja, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Inversiones
        texto_inv = """
        <b>2. INVERSIONES TEMPORARIAS</b>
        <br/><br/>
        Evaluación de 30 instrumentos financieros incluyendo plazos fijos, FCI, acciones y bonos. 
        El análisis de tasas de rendimiento y valores actuales no evidencia inconsistencias 
        significativas respecto a las condiciones de mercado del período.
        <br/><br/>
        <b>Hallazgos:</b> Todas las inversiones presentan documentación respaldatoria adecuada.
        """
        elementos.append(Paragraph(texto_inv, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Cuentas a Cobrar
        texto_cc = """
        <b>3. CUENTAS A COBRAR</b>
        <br/><br/>
        Análisis de 40 facturas emitidas con diferentes plazos de vencimiento. Se identificaron 
        cuentas vencidas que requieren gestión de cobranza activa. El algoritmo detectó patrones 
        de antigüedad de saldos consistentes con políticas crediticias.
        <br/><br/>
        <b>Hallazgos:</b> 12 facturas presentan mora superior a 90 días, sugiriendo evaluación 
        de previsión para incobrables.
        """
        elementos.append(Paragraph(texto_cc, self.styles['Justificado']))
        elementos.append(PageBreak())
        
        # Inventarios
        texto_inv_stock = """
        <b>4. INVENTARIOS</b>
        <br/><br/>
        Revisión de 60 ítems clasificados en materias primas, productos en proceso y productos 
        terminados. Se verificaron valores de costo unitario y cantidades en stock mediante 
        técnicas de detección de outliers.
        <br/><br/>
        <b>Hallazgos:</b> Se identificaron 3 ítems con rotación anormalmente baja que podrían 
        requerir ajuste por obsolescencia.
        """
        elementos.append(Paragraph(texto_inv_stock, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Prepagos
        texto_prepagos = """
        <b>5. GASTOS PAGADOS POR ADELANTADO</b>
        <br/><br/>
        Análisis de 20 conceptos prepagos incluyendo alquileres, seguros y publicidad. 
        Se verificó la correcta imputación temporal y proporcionalidad de los montos devengados.
        <br/><br/>
        <b>Hallazgos:</b> Todos los prepagos cuentan con documentación respaldatoria y contratos vigentes.
        """
        elementos.append(Paragraph(texto_prepagos, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.5*cm))
        return elementos
    
    def _crear_conclusiones(self):
        """Crea conclusiones"""
        elementos = []
        elementos.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", self.styles['Subtitulo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        texto = f"""
        <b>CONCLUSIÓN GENERAL</b>
        <br/><br/>
        Los Activos Corrientes del ejercicio {self.año} se encuentran razonablemente valuados 
        de acuerdo con las RT 7 y RT 37, y las normas contables profesionales vigentes. 
        Los algoritmos de detección identificaron patrones consistentes con anomalías menores 
        que requieren atención pero no representan distorsiones materiales.
        <br/><br/>
        <b>RECOMENDACIONES:</b>
        <br/>
        1. Implementar gestión de cobranza más activa para facturas vencidas
        <br/>
        2. Evaluar previsión para deudores incobrables según antigüedad de saldos
        <br/>
        3. Revisar inventarios de baja rotación para ajustes por obsolescencia
        <br/>
        4. Documentar adecuadamente transacciones de montos significativos en Caja
        <br/>
        5. Mantener revisión trimestral de valuación de inversiones temporarias
        <br/><br/>
        <b>CERTIFICACIÓN:</b> Los procedimientos aplicados cumplen con ISA 315 (Identificación de 
        Riesgos) e ISA 520 (Procedimientos Analíticos).
        """
        
        elementos.append(Paragraph(texto, self.styles['Justificado']))
        elementos.append(Spacer(1, 2*cm))
        
        firma = """
        <br/>
        ________________________________<br/>
        Sistema de Auditoría Algorítmica<br/>
        Activos Corrientes
        """
        elementos.append(Paragraph(firma, self.styles['Normal']))
        return elementos
    
    def generar_informe(self, nombre_archivo):
        """Genera el PDF"""
        try:
            doc = SimpleDocTemplate(
                nombre_archivo,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            elementos = []
            elementos.extend(self._crear_portada())
            elementos.extend(self._crear_resumen())
            elementos.extend(self._crear_analisis_componentes())
            elementos.extend(self._crear_conclusiones())
            
            doc.build(elementos)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


def generar_todos_los_informes():
    """Genera informes para años 2020-2024"""
    os.makedirs('data/informes_auditoria_corrientes', exist_ok=True)
    
    for año in [2020, 2021, 2022, 2023, 2024]:
        print(f"Generando informe {año}...")
        generador = GeneradorInformePDFActivosCorrientes(año)
        archivo = f'data/informes_auditoria_corrientes/informe_corrientes_{año}.pdf'
        if generador.generar_informe(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ Error en {año}")
    
    print("\n✅ Todos los informes generados")


if __name__ == "__main__":
    generar_todos_los_informes()
