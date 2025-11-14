from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

import os

# Correct path to your font
font_path = r"D:\Work Place\per - Copy\Text\Story_Script\StoryScript-Regular.ttf"

# Check if file exists
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font not found: {font_path}")

# Register font with ReportLab
pdfmetrics.registerFont(TTFont("StoryScript", font_path))

def create_certificate_with_custom_font(name, output_file="certificate_custom_font.pdf",border_image="border.jpg",sign = "images/sign1.png" , logo="images/ampics_logo.png"):
    # Register custom fonts (Roboto Regular & Bold)
    

    # Page setup
    width, height = landscape(A4)
    c = canvas.Canvas(output_file, pagesize=(width, height))

    if os.path.exists(border_image):
        c.drawImage(border_image, 0, 0, width, height, preserveAspectRatio=False)

    if os.path.exists(logo):
        c.drawImage(logo, 60, height - 160, width=120, height=170,
                    preserveAspectRatio=True, mask='auto')

    # Title with bold font
    c.setFont("StoryScript", 45)
    c.drawCentredString(width/2, height - 150, "Certificate of Achievement")

    # Subtitle with regular font
    c.setFont("StoryScript", 30)
    c.drawCentredString(width/2, height - 190, "This certificate is proudly presented to")

    # Recipient Name
    c.setFont("StoryScript", 40)
    c.drawCentredString(width/2, height - 260, name)

    # Body Text
    c.setFont("StoryScript", 14)
    c.drawCentredString(width/2, height - 300, "has successfully completed a 1.5-hours webinar on")

    c.setFont("StoryScript", 20)
    c.drawCentredString(width/2, height - 340, "Flask Web Development")

    c.setFont("StoryScript", 14)
    c.drawCentredString(width/2, height - 380, "During the program, the participant demonstrated practical skills in building RESTful APIs, templating with Jinja2,")

    c.setFont("StoryScript", 14)
    c.drawCentredString(width/2, height - 400, "database integration using SQLAlchemy, user authentication, and deploying Flask applications.")
    # Signature & Date
    c.setFont("StoryScript", 20)
    c.drawString(100, 80, "Date: ______________")
    c.drawRightString(width - 100, 80, "Signature: ______________")

    if os.path.exists(sign):
        c.drawImage(sign, width - 250, 65, width=120, height=100,
                    preserveAspectRatio=True, mask='auto')

    c.save()
    print(f"Certificate saved as {output_file}")

# Example usage
create_certificate_with_custom_font("Aditya Shah")
