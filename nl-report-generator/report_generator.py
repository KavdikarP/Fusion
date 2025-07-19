import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from pptx import Presentation
from pptx.util import Inches

def generate_excel(df, file_path):
    df.to_excel(file_path, index=False, engine='openpyxl')

def generate_pdf(df, file_path):
    doc = SimpleDocTemplate(file_path)
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    doc.build([table])

def generate_ppt(df, file_path):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    rows, cols = df.shape
    table = slide.shapes.add_table(rows+1, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(5)).table

    for i, col_name in enumerate(df.columns):
        table.cell(0, i).text = str(col_name)

    for row_idx, row in enumerate(df.values):
        for col_idx, value in enumerate(row):
            table.cell(row_idx+1, col_idx).text = str(value)

    prs.save(file_path)
