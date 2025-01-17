from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime


def build_stocks_table(acciones):
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)

        data = [['Nombre', 'Simbolo', 'Ultimo Precio (BS)', 'Monto Efectivo (BS)', 'Variacion', 'Titulos Negociados']]

        style = TableStyle([
            ('BACKGROUND', (0,0), (6,0), colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMMARGIN', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 5),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])

        for item in acciones:
            data.append([item['nombre'], item['simbolo'], item['ultimo_precio'], item['monto_efectivo'], item['variacion'], item['titulos_negociados']])
        
        tabla = Table(data)
        tabla.setStyle(style)

        styles = getSampleStyleSheet()
        style_header = styles['Heading1']
        titulo = Paragraph(f'Acciones Cotizadas en la Bolsa de Valores de Caracas  |  {datetime.now().strftime("%d/%m/%Y")}', style_header)
        spacer = Spacer(1, 20)
        elements = []
        elements.append(titulo)
        elements.append(spacer)
        elements.append(tabla)
        pdf.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
