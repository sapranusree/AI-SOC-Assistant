from reportlab.pdfgen import canvas

def generate_report(result):

    pdf_file = "incident_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.drawString(
        50,
        800,
        "AI SOC Incident Report"
    )

    y = 760

    for line in result.split("\n"):

        c.drawString(
            50,
            y,
            line[:100]
        )

        y -= 20

        if y < 50:
            c.showPage()
            y = 800

    c.save()

    return pdf_file