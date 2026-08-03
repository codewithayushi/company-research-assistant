import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(data: dict, filename: str = "report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#334155'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        spaceAfter=4
    )

    story.append(Paragraph(f"Company Research Report: {data.get('company_name', 'N/A')}", title_style))
    story.append(Spacer(1, 8))
    
    # Company Info Table
    info_data = [
        [Paragraph("<b>Website:</b>", body_style), Paragraph(data.get('website', 'N/A'), body_style)],
        [Paragraph("<b>Phone:</b>", body_style), Paragraph(data.get('phone', 'N/A'), body_style)],
        [Paragraph("<b>Address:</b>", body_style), Paragraph(data.get('address', 'N/A'), body_style)]
    ]
    t = Table(info_data, colWidths=[100, 440])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(data.get('summary', 'No summary available.'), body_style))
    
    # Products / Services
    story.append(Paragraph("Products & Services", heading_style))
    for prod in data.get('products_services', []):
        story.append(Paragraph(f"• {prod}", body_style))
        
    # Pain Points
    story.append(Paragraph("AI-Generated Pain Points", heading_style))
    for pp in data.get('pain_points', []):
        story.append(Paragraph(f"• {pp}", body_style))
        
    # Competitors
    story.append(Paragraph("Competitor Analysis", heading_style))
    comp_data = [[Paragraph("<b>Competitor Name</b>", body_style), Paragraph("<b>Website</b>", body_style)]]
    for comp in data.get('competitors', []):
        comp_data.append([Paragraph(comp.get('name', ''), body_style), Paragraph(comp.get('website', ''), body_style)])
    
    ct = Table(comp_data, colWidths=[200, 340])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ct)
    
    doc.build(story)
    return filename