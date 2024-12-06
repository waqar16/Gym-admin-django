from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from .models import GymMember
from io import BytesIO
from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.staticfiles import finders

def generate_pdf_receipt(income, member):
    """
    Generate a premium-styled PDF receipt inspired by the uploaded invoice design.
    :param income: GymIncomeExpense instance (income type).
    :return: HttpResponse containing the PDF file.
    """
    print(member)
    member_info = get_object_or_404(GymMember, id=member)
    firstname = member_info.first_name
    lastname = member_info.last_name
    membership_valid_from = member_info.membership_valid_from
    membership_valid_to = member_info.membership_valid_to
    membership_status = member_info.membership_status

    buffer = BytesIO()
    margin = 30  # 30 points padding on each side
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        leftMargin=margin, 
        rightMargin=margin, 
        topMargin=margin, 
        bottomMargin=margin
    )
    styles = getSampleStyleSheet()

    elements = []
    
    logo_path = finders.find('logo.jpg')
    try:
        logo = Image(logo_path, width=100, height=120)
        elements.append(logo)
    except FileNotFoundError:
        elements.append(Paragraph("<b><font size=12 color='red'>Logo not found</font></b>", styles['Normal']))

    elements.append(Spacer(1, 20))

    # Header with invoice title
    elements.append(Paragraph("<b><font size=24 color='navy'>INVOICE</font></b>", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # "From" and "Bill To" section
    from_bill_data = [
        ["From", "Bill To", "Invoice Details"],
        [
            "Fitness First Gym",
            f"{firstname} {lastname}\n{"Member ID: " + str(income.mp_id)}",
            f"Invoice #: {income.mp_id}\nInvoice Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\nPayment Status: {"Paid"}",
        ],
    ]
    from_bill_table = Table(from_bill_data, colWidths=[200, 200, 200])
    from_bill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(from_bill_table)
    elements.append(Spacer(1, 20))

    # Details Table
    details_data = [
        ["Field", "Details"],
        ["ID", str(income.mp_id)],
        ["Invoice Label", "Membership Fee"],
        ["Membership Valid From", str(membership_valid_from)],
        ["Membership Valid To", str(membership_valid_to)],
        ["Membership Status", str(membership_status)],
        ["Payment Status", "Paid"],
        ["Date", str(datetime.date.today())],
        ["Amount", f"{income.paid_amount:.2f}"],
    ]

    details_table = Table(details_data, colWidths=[150, 350])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 20))

    # Footer with terms
    footer = [
        Paragraph("<font size=10 color='grey'>This is a computer-generated receipt and does not require physical signature.</font>", styles['Normal']),
        Spacer(1, 6),
    ]
    elements.extend(footer)

    # Build the PDF
    doc.build(elements)
    buffer.seek(0)

    # Return as an HTTP response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{income.mp_id}.pdf"'
    return response
