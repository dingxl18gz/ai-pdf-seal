from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

pdf_path = "test.pdf"
c = canvas.Canvas(pdf_path, pagesize=letter)

c.drawString(100, 750, "Page 1 - Test Document")
c.drawString(100, 700, "This is a test PDF for stamping.")
c.showPage()

c.drawString(100, 750, "Page 2 - Test Document")
c.drawString(100, 700, "The stamp should appear on both pages.")
c.showPage()

c.save()
print(f"Created: {pdf_path}")
