from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textwrap
import uuid

def generate_pdf(story_text: str, title="Bedtime Story"):
    filename = f"story_{uuid.uuid4().hex}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 80, title)

    c.setFont("Helvetica", 12)
    y = height - 120

    # Wrap story text into lines
    lines = textwrap.wrap(story_text, width=90)

    for line in lines:
        if y < 50:   # new page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50
        c.drawString(50, y, line)
        y -= 20

    c.save()
    return filename
