from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_pdf(data):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Кошторис обручок")
    y -= 40

    p.setFont("Helvetica", 12)

    for key, value in data.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20

    p.setFont("Helvetica-Bold", 14)
    y -= 10
    p.drawString(50, y, f"ЗАГАЛЬНА СУМА: {data['Разом']} ₴")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf