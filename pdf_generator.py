from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def make_pdf(rows,total,photos=None):

    buf=io.BytesIO()
    p=canvas.Canvas(buf,pagesize=A4)
    w,h=A4

    y=h-60
    p.setFont("Helvetica-Bold",14)
    p.drawString(50,y,"КОШТОРИС ОБРУЧОК")
    y-=30

    p.setFont("Helvetica",9)

    for r in rows:
        if r["type"]=="section":
            y-=15
            p.setFont("Helvetica-Bold",10)
            p.drawString(50,y,r["title"])
            y-=10
            p.setFont("Helvetica",9)
        else:
            p.drawString(50,y,r["c1"])
            p.drawString(220,y,r["c2"])
            p.drawString(380,y,r["c3"])
            y-=12

        if y<60:
            p.showPage()
            y=h-60

    p.setFont("Helvetica-Bold",12)
    p.drawString(50,y-20,f"ЗАГАЛОМ: {total:.2f} ₴")

    p.save()
    return buf.getvalue()
