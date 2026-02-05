from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import pandas as pd

class GeneradorInformeAuditoria:
    def __init__(self, empresa_nombre, empresa_cuit, fecha_auditoria):
        self.empresa_nombre = empresa_nombre
        self.empresa_cuit = empresa_cuit
        self.fecha_auditoria = fecha_auditoria
        self.doc = Document()

    def agregar_portada(self):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("INFORME DE AUDITORÍA\nACTIVOS CORRIENTES")
        run.font.size = Pt(24)
        run.bold = True
        self.doc.add_paragraph(f"\nEmpresa: {self.empresa_nombre}\nCUIT: {self.empresa_cuit}\nFecha: {datetime.now().strftime('%d/%m/%Y')}")
        self.doc.add_page_break()

    def agregar_resumen_hallazgos(self, resumen_df):
        self.doc.add_heading('RESUMEN DE HALLAZGOS', level=1)
        table = self.doc.add_table(rows=1, cols=len(resumen_df.columns))
        table.style = 'Light Grid Accent 1'
        for i, col in enumerate(resumen_df.columns):
            table.rows[0].cells[i].text = col
        for _, row in resumen_df.iterrows():
            cells = table.add_row().cells
            for i, val in enumerate(row):
                cells[i].text = str(val)

    def generar_informe(self, resumen_df, data_dict, ruta_salida):
        self.agregar_portada()
        self.agregar_resumen_hallazgos(resumen_df)
        self.doc.add_heading('DETALLE DE ANOMALÍAS', level=1)
        for rubro, df in data_dict.items():
            anomalias = df[df['resultado_if'] == 'Anómalo']
            if not anomalias.empty:
                self.doc.add_heading(rubro, level=2)
                self.doc.add_paragraph(f"Se detectaron {len(anomalias)} anomalías.")
        self.doc.save(ruta_salida)
