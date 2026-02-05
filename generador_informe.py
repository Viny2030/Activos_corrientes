# ===============================================================
# GENERADOR DE INFORMES DE AUDITORÍA EN FORMATO DOCX - V2.1
# Optimizado para Render y Streamlit Cloud
# ===============================================================

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from datetime import datetime
import pandas as pd
import traceback
import io

class GeneradorInformeAuditoria:
    """Genera informes profesionales de auditoría en formato DOCX"""
    
    def __init__(self, empresa_nombre, empresa_cuit, fecha_auditoria):
        try:
            self.empresa_nombre = empresa_nombre
            self.empresa_cuit = empresa_cuit
            # Aseguramos que fecha_auditoria sea datetime si viene como string
            if isinstance(fecha_auditoria, str):
                self.fecha_auditoria = datetime.strptime(fecha_auditoria, '%Y-%m-%d')
            else:
                self.fecha_auditoria = fecha_auditoria
                
            self.doc = Document()
            self._configurar_estilos()
        except Exception as e:
            raise Exception(f"Error al inicializar generador: {e}")
    
    def _configurar_estilos(self):
        styles = self.doc.styles
        if 'Titulo Principal' not in [s.name for s in styles]:
            titulo_style = styles.add_style('Titulo Principal', WD_STYLE_TYPE.PARAGRAPH)
            titulo_format = titulo_style.font
            titulo_format.name = 'Arial'
            titulo_format.size = Pt(16)
            titulo_format.bold = True
            titulo_format.color.rgb = RGBColor(0, 51, 102)

    def agregar_portada(self):
        titulo = self.doc.add_paragraph()
        titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = titulo.add_run("INFORME DE AUDITORÍA\nSOBRE ACTIVOS CORRIENTES")
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)
        
        self.doc.add_paragraph()
        datos = self.doc.add_paragraph()
        datos.alignment = WD_ALIGN_PARAGRAPH.CENTER
        datos_text = f"""
Empresa Auditada: {self.empresa_nombre}
CUIT: {self.empresa_cuit}
Período Auditado: {self.fecha_auditoria.strftime('%m/%Y')}
Fecha del Informe: {datetime.now().strftime('%d de %B de %Y')}

Normas Aplicadas: RT 7, RT 37, NIAs
        """
        datos.add_run(datos_text)
        self.doc.add_page_break()

    def agregar_seccion_identificacion(self):
        self.doc.add_heading('I. IDENTIFICACIÓN DEL ENTE Y PERÍODO AUDITADO', level=1)
        texto = f"Hemos auditado los activos corrientes de {self.empresa_nombre}, CUIT {self.empresa_cuit}, correspondientes al período finalizado el {self.fecha_auditoria.strftime('%d de %B de %Y')}. La auditoría se realizó conforme a las Normas Internacionales de Auditoría (NIAs) y las Resoluciones Técnicas 7 y 37 de FACPCE."
        p = self.doc.add_paragraph(texto)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def agregar_seccion_alcance(self):
        self.doc.add_heading('II. ALCANCE DEL TRABAJO', level=1)
        self.doc.add_heading('2.1. Procedimientos Aplicados (Según RT 7)', level=2)
        procedimientos = [
            "Confirmaciones externas de saldos", "Inspección de documentación respaldatoria",
            "Pruebas de corte de operaciones", "Análisis de antigüedad de saldos",
            "Aplicación de técnicas analíticas con Machine Learning"
        ]
        for proc in procedimientos:
            self.doc.add_paragraph(proc, style='List Bullet')

    def agregar_resumen_hallazgos(self, resumen_df):
        self.doc.add_heading('III. RESUMEN DE HALLAZGOS', level=1)
        table = self.doc.add_table(rows=1, cols=4)
        table.style = 'Light Grid Accent 1'
        hdr_cells = table.rows[0].cells
        for i, text in enumerate(['RUBRO', 'CANTIDAD', 'SALDO ($)', '% TOTAL']):
            hdr_cells[i].text = text
            hdr_cells[i].paragraphs[0].runs[0].font.bold = True

        total_general = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Saldo ($)'].iloc[0]
        for _, row in resumen_df.iterrows():
            row_cells = table.add_row().cells
            row_cells[0].text = str(row['Rubro'])
            row_cells[1].text = f"{int(row['Cantidad'])}"
            row_cells[2].text = f"{row['Saldo ($)']:,.2f}"
            if row['Rubro'] != 'TOTAL ACTIVOS CORRIENTES':
                porc = (row['Saldo ($)'] / total_general * 100) if total_general > 0 else 0
                row_cells[3].text = f"{porc:.1f}%"
            else:
                row_cells[3].text = "100.0%"
                for cell in row_cells: cell.paragraphs[0].runs[0].font.bold = True

    def agregar_hallazgos_especificos(self, data_dict):
        self.doc.add_heading('IV. HALLAZGOS ESPECÍFICOS POR RUBRO', level=1)
        for i, (rubro, df) in enumerate(data_dict.items(), 1):
            self.doc.add_heading(f'4.{i}. {rubro}', level=2)
            anomalias = len(df[df.get('resultado_if', pd.Series()) == 'Anómalo'])
            self.doc.add_paragraph(f"Total de items auditados: {len(df)}")
            self.doc.add_paragraph(f"Anomalías detectadas (ML): {anomalias}")
            if anomalias > 0:
                p = self.doc.add_paragraph(f"⚠️ Observación: Se detectaron {anomalias} items con características atípicas.", style='Quote')

    def agregar_opinion_profesional(self, total_activos, total_anomalias, total_items):
        self.doc.add_heading('V. OPINION PROFESIONAL', level=1)
        tasa = (total_anomalias / total_items * 100) if total_items > 0 else 0
        if tasa < 5:
            txt = f"En nuestra opinión, los activos corrientes de {self.empresa_nombre} al {self.fecha_auditoria.strftime('%d/%m/%Y')} por ${total_activos:,.2f} se presentan razonablemente."
        else:
            txt = f"En nuestra opinión, excepto por las salvedades indicadas, los activos corrientes se presentan razonablemente."
        self.doc.add_paragraph(txt).alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def agregar_firmas(self):
        self.doc.add_paragraph("\n\n")
        table = self.doc.add_table(rows=2, cols=2)
        table.cell(0, 0).text = "_______________________\nContador Público"
        table.cell(0, 1).text = "_______________________\nSocio Director"
        for row in table.rows:
            for cell in row.cells: cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    def generar_informe(self, resumen_df, data_dict, ruta_salida=None):
        """Genera el informe. Si ruta_salida es None, devuelve un BytesIO."""
        try:
            self.agregar_portada()
            self.agregar_seccion_identificacion()
            self.agregar_seccion_alcance()
            self.agregar_resumen_hallazgos(resumen_df)
            self.agregar_hallazgos_especificos(data_dict)
            
            total_activos = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Saldo ($)'].iloc[0]
            total_anomalias = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Anomalías'].iloc[0]
            total_items = resumen_df[resumen_df['Rubro'] == 'TOTAL ACTIVOS CORRIENTES']['Cantidad'].iloc[0]
            
            self.agregar_opinion_profesional(total_activos, total_anomalias, total_items)
            self.agregar_firmas()
            
            if ruta_salida:
                self.doc.save(ruta_salida)
                return ruta_salida
            else:
                target = io.BytesIO()
                self.doc.save(target)
                target.seek(0)
                return target
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            raise
