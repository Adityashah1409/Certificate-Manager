from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, gold, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime
from models import CertificateTemplate
from certificate_texts import format_certificate_text


# Font registration - handles missing font gracefully
def register_custom_fonts():
    """Register custom fonts with fallback handling"""
    try:
        font_path = r"D:\Work Place\per - Copy\Text\Story_Script\StoryScript-Regular.ttf"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont("StoryScript", font_path))
            return True
        else:
            print(f"Warning: Custom font not found at {font_path}")
            return False
    except Exception as e:
        print(f"Error registering custom font: {e}")
        return False

# Initialize fonts on module load
CUSTOM_FONT_AVAILABLE = register_custom_fonts()


# Initialize fonts on module load
CUSTOM_FONT_AVAILABLE = register_custom_fonts()


def hex_to_color(hex_string):
    """Convert hex color to ReportLab color object"""
    try:
        return HexColor(hex_string)
    except:
        return black


def get_font(font_name, fallback="Helvetica"):
    """Get font with fallback if custom font not available"""
    if font_name == "StoryScript" and CUSTOM_FONT_AVAILABLE:
        return "StoryScript"
    return fallback


def get_image_paths(event, upload_folder):
    """Get all image paths from event with proper fallbacks"""
    background_image = None
    logo_image = None
    signature_image = None
    
    # Debug prints
    print(f"Event ID: {event.id}")
    print(f"Upload folder: {upload_folder}")
    
    # Background image from event
    if hasattr(event, 'background_path') and event.background_path:
        background_image = os.path.join(upload_folder, event.background_path)
        print(f"Background: {background_image}, exists: {os.path.exists(background_image)}")
    else:
        print("No background path in event")
    
    # Logo image from event
    if hasattr(event, 'logo_path') and event.logo_path:
        logo_image = os.path.join(upload_folder, event.logo_path)
        print(f"Logo: {logo_image}, exists: {os.path.exists(logo_image)}")
    else:
        print("No logo path in event")
    
    # Signature image from event
    if hasattr(event, 'signature_path') and event.signature_path:
        signature_image = os.path.join(upload_folder, event.signature_path)
        print(f"Signature: {signature_image}, exists: {os.path.exists(signature_image)}")
    else:
        print("No signature path in event")
    
    return background_image, logo_image, signature_image

def draw_image_if_exists(canvas, image_path, x, y, width, height, preserveAspectRatio=True, mask='auto'):
    """Safely draw image if it exists"""
    if image_path and os.path.exists(image_path):
        try:
            canvas.drawImage(image_path, x, y, width=width, height=height, 
                           preserveAspectRatio=preserveAspectRatio, mask=mask)
            print(f"✓ Image drawn successfully: {os.path.basename(image_path)}")
            return True
        except Exception as e:
            print(f"✗ Error drawing image {os.path.basename(image_path)}: {e}")
            return False
    else:
        print(f"✗ Image not found or path is None: {image_path}")
        return False

def draw_certificate_background(c, width, height, background_image=None, default_color='#FAFAFA'):
    """Draw certificate background - image or color"""
    background_drawn = False
    
    if background_image and os.path.exists(background_image):
        try:
            c.drawImage(background_image, 0, 0, width, height, preserveAspectRatio=False)
            background_drawn = True
            print("✓ Background image drawn")
        except Exception as e:
            print(f"✗ Error drawing background: {e}")
    
    # Fallback to color background
    if not background_drawn:
        c.setFillColor(HexColor(default_color))
        c.rect(0, 0, width, height, fill=1)
        print("✓ Default background color applied")
    
    return background_drawn

def draw_ornamental_border(c, width, height, config, background_image=None):
    """Draw image background first, then ornamental border"""
    
    # Draw background image if provided and exists
    if background_image and os.path.exists(background_image):
        try:
            c.drawImage(background_image, 0, 0, width=width, height=height, 
                       preserveAspectRatio=False, mask='auto')
            print("✓ Background image drawn in ornamental border")
        except Exception as e:
            print(f"✗ Error drawing background image: {e}")
    
    # Continue with existing ornamental border code
    margin = 40
    border_color = hex_to_color(config.get('colors', {}).get('primary', '#D4AF37'))
    accent_color = hex_to_color(config.get('colors', {}).get('accent', '#8B4513'))

    c.setStrokeColor(border_color)
    c.setLineWidth(4)
    c.rect(margin, margin, width - 2*margin, height - 2*margin)

    inner_margin = margin + 20
    c.setStrokeColor(accent_color)
    c.setLineWidth(2)
    c.rect(inner_margin, inner_margin, width - 2*inner_margin, height - 2*inner_margin)

    corner_size = 40
    corners = [
        (margin + 15, height - margin - 15),
        (width - margin - 15, height - margin - 15),
        (margin + 15, margin + 15),
        (width - margin - 15, margin + 15)
    ]

    c.setStrokeColor(border_color)
    c.setLineWidth(3)

    for x, y in corners:
        c.arc(x - corner_size/2, y - corner_size/2, x + corner_size/2, y + corner_size/2, 0, 90)
        c.line(x - corner_size/3, y, x + corner_size/3, y)
        c.line(x, y - corner_size/3, x, y + corner_size/3)

def draw_decorative_elements(c, width, height, colors):
    """Add decorative flourishes and elements"""
    primary = hex_to_color(colors.get('primary', '#D4AF37'))
    accent = hex_to_color(colors.get('accent', '#8B4513'))
    
    # Top decorative line
    c.setStrokeColor(primary)
    c.setLineWidth(3)
    line_y = height - 160
    c.line(width/2 - 150, line_y, width/2 + 150, line_y)
    
    # Decorative circles at line ends
    c.setFillColor(accent)
    c.circle(width/2 - 150, line_y, 6, fill=1)
    c.circle(width/2 + 150, line_y, 6, fill=1)
    
    # Central decorative element
    c.setFillColor(primary)
    c.circle(width/2, line_y, 10, fill=1)
    
    # Bottom decorative elements
    bottom_y = 200
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    
    # Left flourish
    c.arc(150, bottom_y - 30, 250, bottom_y + 30, 0, 180)
    # Right flourish
    c.arc(width - 250, bottom_y - 30, width - 150, bottom_y + 30, 0, 180)


def generate_custom_font_certificate(event, student, certificate_folder):
    """Generate certificate with custom StoryScript font and dynamic text (NO RANKING)"""
    filename = f"certificate_custom_{student.id}_{event.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(certificate_folder, filename)
    
    try:
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        
        width, height = landscape(A4)
        c = canvas.Canvas(filepath, pagesize=(width, height))
        
        # Get image paths and certificate text
        background_image, logo_image, signature_image = get_image_paths(event, upload_folder)
        cert_text = format_certificate_text(event, student)  # NO RANKING PARAMETER
        
        # Draw background and logo
        draw_certificate_background(c, width, height, background_image)
        if logo_image:
            draw_image_if_exists(c, logo_image, 60, height - 160, 120, 120)
        
        # Dynamic Title based on event type
        title_font = get_font("StoryScript", "Helvetica-Bold")
        c.setFont(title_font, 45)
        c.setFillColor(HexColor('#D4AF37'))
        c.drawCentredString(width/2, height - 150, cert_text['title'])
        
        # Dynamic Subtitle
        c.setFont(title_font, 30)
        c.setFillColor(HexColor('#333333'))
        c.drawCentredString(width/2, height - 190, cert_text['subtitle'])
        
        # Student Name
        c.setFont(title_font, 40)
        c.setFillColor(HexColor('#000000'))
        c.drawCentredString(width/2, height - 260, student.name.upper())
        
        # Dynamic Accomplishment
        body_font = get_font("StoryScript", "Helvetica")
        c.setFont(body_font, 16)
        c.setFillColor(HexColor('#333333'))
        c.drawCentredString(width/2, height - 300, cert_text['accomplishment'])
        
        # Event title with emphasis
        c.setFont(body_font, 24)
        c.setFillColor(HexColor('#D4AF37'))
        c.drawCentredString(width/2, height - 340, f'"{event.title}"')
        
        # Dynamic closing
        c.setFont(body_font, 14)
        c.setFillColor(HexColor('#555555'))
        c.drawCentredString(width/2, height - 370, cert_text['closing'])
        
        # Event details
        detail_y = height - 410
        c.setFont(body_font, 12)
        c.setFillColor(HexColor('#666666'))
        
        event_details = []
        if hasattr(event, 'organizer') and event.organizer:
            event_details.append(f"Organized by: {event.organizer}")
        if hasattr(event, 'location') and event.location:
            event_details.append(f"Venue: {event.location}")
        if hasattr(event, 'start_date') and event.start_date:
            if hasattr(event, 'end_date') and event.end_date and event.start_date != event.end_date:
                event_details.append(f"Date: {event.start_date.strftime('%B %d, %Y')} - {event.end_date.strftime('%B %d, %Y')}")
            else:
                event_details.append(f"Date: {event.start_date.strftime('%B %d, %Y')}")
        
        for detail in event_details[:3]:
            c.drawCentredString(width/2, detail_y, detail)
            detail_y -= 18
        
        # Signature section
        signature_y = 120
        c.setFont(body_font, 14)
        c.setFillColor(HexColor('#333333'))
        
        c.drawString(100, signature_y, f"Date: {datetime.now().strftime('%B %d, %Y')}")
        c.drawRightString(width - 100, signature_y, "Authorized Signature")
        
        # Draw signature
        if signature_image:
            draw_image_if_exists(c, signature_image, width - 250, signature_y + 10, 120, 50)
        
        # Certificate ID and footer
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor('#888888'))
        cert_id = f"Certificate ID: CERT-{event.id}-{student.id}-{datetime.now().strftime('%Y%m%d')}"
        c.drawCentredString(width/2, 40, cert_id)
        
        c.setFont("Helvetica-Oblique", 7)
        c.drawCentredString(width/2, 25, "Generated by Certificate Management System")
        
        c.save()
        print(f"✓ Custom certificate saved: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating custom certificate: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_enhanced_certificate(event, student, certificate_folder):
    """Enhanced certificate with dual signatures and dynamic text (NO RANKING)"""
    filename = f"certificate_{student.id}_{event.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(certificate_folder, filename)
    
    try:
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        
        width, height = landscape(A4)
        c = canvas.Canvas(filepath, pagesize=(width, height))
        
        # Get image paths and certificate text
        background_image, logo_image, signature_image = get_image_paths(event, upload_folder)
        cert_text = format_certificate_text(event, student)  # NO RANKING PARAMETER
        
        # Draw background and logo
        draw_certificate_background(c, width, height, background_image)
        if logo_image:
            draw_image_if_exists(c, logo_image, 60, height - 160, 120, 120)
        
        # Use custom font if available
        title_font = get_font("StoryScript", "Helvetica-Bold")
        body_font = get_font("StoryScript", "Helvetica")
        
        # Dynamic Title
        c.setFont(title_font, 45)
        c.setFillColor(HexColor('#D4AF37'))
        c.drawCentredString(width/2, height - 150, cert_text['title'])
        
        # Dynamic Subtitle
        c.setFont(title_font, 30)
        c.setFillColor(HexColor('#333333'))
        c.drawCentredString(width/2, height - 190, cert_text['subtitle'])
        
        # Student Name
        c.setFont(title_font, 40)
        c.setFillColor(HexColor('#000000'))
        c.drawCentredString(width/2, height - 260, student.name.upper())
        
        # Dynamic Accomplishment
        c.setFont(body_font, 16)
        c.setFillColor(HexColor('#333333'))
        c.drawCentredString(width/2, height - 300, cert_text['accomplishment'])
        
        # Event title with highlight
        c.setFont(body_font, 24)
        c.setFillColor(HexColor('#D4AF37'))
        c.drawCentredString(width/2, height - 340, f'"{event.title}"')
        
        # Dynamic closing
        c.setFont(body_font, 14)
        c.setFillColor(HexColor('#555555'))
        c.drawCentredString(width/2, height - 370, cert_text['closing'])
        
        # Event details
        details_y = height - 410
        c.setFont(body_font, 12)
        c.setFillColor(HexColor('#666666'))
        
        basic_details = []
        if hasattr(event, 'organizer') and event.organizer:
            basic_details.append(f"Organized by: {event.organizer}")
        if hasattr(event, 'location') and event.location:
            basic_details.append(f"Venue: {event.location}")
        if hasattr(event, 'start_date') and event.start_date:
            if hasattr(event, 'end_date') and event.end_date and event.start_date != event.end_date:
                basic_details.append(f"Date: {event.start_date.strftime('%B %d, %Y')} - {event.end_date.strftime('%B %d, %Y')}")
            else:
                basic_details.append(f"Date: {event.start_date.strftime('%B %d, %Y')}")
        
        for detail in basic_details:
            c.drawCentredString(width/2, details_y, detail)
            details_y -= 18
        
        # Dual signature section
        signature_y = 120
        
        # LEFT SIGNATURE
        left_sig_x = 150
        if signature_image:
            draw_image_if_exists(c, signature_image, left_sig_x - 50, signature_y + 10, 100, 40)
        
        c.setStrokeColor(HexColor('#333333'))
        c.setLineWidth(1)
        c.line(left_sig_x - 60, signature_y, left_sig_x + 60, signature_y)
        
        c.setFont(body_font, 11)
        c.setFillColor(HexColor('#333333'))
        c.drawCentredString(left_sig_x, signature_y - 15, "Director/Principal")
        
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(HexColor('#666666'))
        c.drawCentredString(left_sig_x, signature_y - 30, "Authorized Signature")
        
        # RIGHT DATE
        right_sig_x = width - 150
        c.line(right_sig_x - 60, signature_y, right_sig_x + 60, signature_y)
        
        c.setFont(body_font, 11)
        c.setFillColor(HexColor('#333333'))
        c.drawCentredString(right_sig_x, signature_y - 15, "Program Coordinator")
        
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(HexColor('#666666'))
        c.drawCentredString(right_sig_x, signature_y - 30, f"Date: {datetime.now().strftime('%B %d, %Y')}")
        
        # Certificate ID
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor('#999999'))
        cert_id = f"Certificate ID: CERT-{event.id}-{student.id}-{datetime.now().strftime('%Y%m%d')}"
        c.drawCentredString(width/2, 40, cert_id)
        
        # Footer
        c.setFont("Helvetica-Oblique", 7)
        c.drawCentredString(width/2, 25, "Generated by Certificate Management System")
        
        c.save()
        print(f"✓ Enhanced certificate saved: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating enhanced certificate: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_premium_certificate(event, student, template, certificate_folder):
    """Generate premium certificate with template support"""
    filename = f"certificate_{student.id}_{event.id}_{template.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(certificate_folder, filename)
    
    try:
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        
        config = template.template_config
        colors = config.get('colors', {})
        fonts = config.get('fonts', {})
        
        # ADD EVENT BACKGROUND IMAGE SUPPORT
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        
        # Try event background first, then template background
        background_drawn = False
        if hasattr(event, 'background_path') and event.background_path:
            background_image = os.path.join(upload_folder, event.background_path)
            if os.path.exists(background_image):
                try:
                    c.drawImage(background_image, 0, 0, width, height, preserveAspectRatio=False)
                    background_drawn = True
                    print("✓ Event background image drawn in premium certificate")
                except Exception as e:
                    print(f"✗ Error drawing event background: {e}")
        
        # Fallback to default background if no event background
        if not background_drawn:
            c.setFillColor(HexColor('#FAFAFA'))
            c.rect(0, 0, width, height, fill=1)
            
            # Add subtle watermark
            c.saveState()
            c.setFillColor(HexColor('#F5F5F5'))
            watermark_font = get_font("StoryScript", "Helvetica-Bold")
            c.setFont(watermark_font, 120)
            c.rotate(45)
            c.setFillAlpha(0.05)
            c.drawString(200, -100, "CERTIFIED")
            c.restoreState()
        
        # Draw ornamental border (but pass None as background since we already drew it)
        draw_ornamental_border(c, width, height, config, background_image=None)
        
        # ADD EVENT LOGO SUPPORT - prioritize event logo over template logo
        logo_drawn = False
        if hasattr(event, 'logo_path') and event.logo_path:
            event_logo = os.path.join(upload_folder, event.logo_path)
            if os.path.exists(event_logo):
                try:
                    c.drawImage(event_logo, 80, height - 130, 80, 80, preserveAspectRatio=True, mask='auto')
                    logo_drawn = True
                    print("✓ Event logo drawn in premium certificate")
                except Exception as e:
                    print(f"✗ Error drawing event logo: {e}")
        
        # Fallback to template logo if no event logo
        if not logo_drawn and template.logo_image and os.path.exists(template.logo_image):
            try:
                c.drawImage(template.logo_image, 80, height - 130, 80, 80, preserveAspectRatio=True)
                print("✓ Template logo drawn in premium certificate")
            except Exception as e:
                print(f"✗ Error drawing template logo: {e}")
        
        # Institution name
        header_font = get_font("StoryScript", "Helvetica-Bold")
        c.setFont(header_font, 16)
        c.setFillColor(hex_to_color(colors.get('text', '#333333')))
        
        organizer_name = getattr(event, 'organizer', 'Institution Name')
        c.drawCentredString(width/2, height - 80, organizer_name.upper())
        
        # Main title with elegant styling
        c.setFont(header_font, 42)
        c.setFillColor(hex_to_color(colors.get('primary', '#D4AF37')))
        title_y = height - 140
        c.drawCentredString(width/2, title_y, "CERTIFICATE")
        
        c.setFont(header_font, 28)
        c.drawCentredString(width/2, title_y - 35, "OF ACHIEVEMENT")
        
        # Add decorative elements
        draw_decorative_elements(c, width, height, colors)
        
        # Certification text
        body_font = get_font("StoryScript", "Helvetica-Oblique")
        c.setFont(body_font, 18)
        c.setFillColor(hex_to_color(colors.get('text', '#555555')))
        text_y = height - 220
        c.drawCentredString(width/2, text_y, "This is proudly presented to")
        
        # Student name with elegant box
        name_y = text_y - 60
        name_box_width = len(student.name) * 18 + 60
        name_box_height = 50
        
        # Name background box
        c.setFillColor(hex_to_color(colors.get('primary', '#D4AF37')))
        c.setStrokeColor(hex_to_color(colors.get('accent', '#8B4513')))
        c.setLineWidth(2)
        c.rect((width - name_box_width)/2, name_y - 15, name_box_width, name_box_height, fill=1, stroke=1)
        
        # Student name
        name_font = get_font("StoryScript", "Helvetica-Bold")
        c.setFont(name_font, 36)
        c.setFillColor(white)
        c.drawCentredString(width/2, name_y + 5, student.name.upper())
        
        # Achievement description
        achievement_y = name_y - 80
        c.setFont(body_font, 16)
        c.setFillColor(hex_to_color(colors.get('text', '#444444')))
        
        # Include event type in description
        event_type_text = ""
        if hasattr(event, 'event_type') and event.event_type:
            event_type_text = f" ({event.event_type.value})"
        
        c.drawCentredString(width/2, achievement_y, f"for outstanding participation in {event.title}{event_type_text}")
        
        # Event title with highlight
        event_y = achievement_y - 50
        c.setFont(name_font, 24)
        c.setFillColor(hex_to_color(colors.get('primary', '#D4AF37')))
        c.drawCentredString(width/2, event_y, f'"{event.title}"')
        
        # Event details box
        details_y = event_y - 100
        details_box_height = 80
        details_box_width = 400
        
        # Details background
        c.setFillColor(HexColor('#F8F9FA'))
        c.setStrokeColor(hex_to_color(colors.get('accent', '#8B4513')))
        c.setLineWidth(1)
        c.rect((width - details_box_width)/2, details_y - details_box_height/2, 
               details_box_width, details_box_height, fill=1, stroke=1)
        
        # Event details text
        c.setFont(body_font, 13)
        c.setFillColor(hex_to_color(colors.get('text', '#333333')))
        
        details_lines = []
        
        if hasattr(event, 'event_type') and event.event_type:
            details_lines.append(f"Event Type: {event.event_type.value}")
        
        if hasattr(event, 'location') and event.location:
            details_lines.append(f"Venue: {event.location}")
        
        if hasattr(event, 'start_date') and event.start_date:
            if hasattr(event, 'end_date') and event.end_date and event.start_date != event.end_date:
                details_lines.append(f"Date: {event.start_date.strftime('%B %d, %Y')} - {event.end_date.strftime('%B %d, %Y')}")
            else:
                details_lines.append(f"Date: {event.start_date.strftime('%B %d, %Y')}")
        elif hasattr(event, 'date') and event.date:
            details_lines.append(f"Date: {event.date.strftime('%B %d, %Y')}")
        
        for i, line in enumerate(details_lines[:3]):  # Limit to 3 lines
            c.drawCentredString(width/2, details_y + 20 - (i * 18), line)
        
        # Signature section
        signature_y = 140
        
        # Left signature area - prioritize event signature over template signature
        left_sig_x = 120
        signature_drawn = False
        if hasattr(event, 'signature_path') and event.signature_path:
            event_signature = os.path.join(upload_folder, event.signature_path)
            if os.path.exists(event_signature):
                try:
                    c.drawImage(event_signature, left_sig_x - 40, signature_y, 80, 30, preserveAspectRatio=True, mask='auto')
                    signature_drawn = True
                    print("✓ Event signature drawn in premium certificate")
                except Exception as e:
                    print(f"✗ Error drawing event signature: {e}")
        
        # Fallback to template signature
        if not signature_drawn and template.signature_image and os.path.exists(template.signature_image):
            try:
                c.drawImage(template.signature_image, left_sig_x - 40, signature_y, 80, 30, preserveAspectRatio=True)
                print("✓ Template signature drawn in premium certificate")
            except Exception as e:
                print(f"✗ Error drawing template signature: {e}")
        
        c.setFont(body_font, 11)
        c.setFillColor(black)
        c.drawCentredString(left_sig_x, signature_y - 15, "Director/Principal")
        c.setLineWidth(1)
        c.line(left_sig_x - 60, signature_y - 20, left_sig_x + 60, signature_y - 20)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(left_sig_x, signature_y - 35, "Authorized Signature")
        
        # Right date area
        right_date_x = width - 120
        c.setFont(body_font, 11)
        c.drawCentredString(right_date_x, signature_y - 15, f"{datetime.now().strftime('%B %d, %Y')}")
        c.line(right_date_x - 60, signature_y - 20, right_date_x + 60, signature_y - 20)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(right_date_x, signature_y - 35, "Date of Issue")
        
        # Certificate ID
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor('#888888'))
        cert_id = f"CERT-{event.id}-{student.id}-{datetime.now().strftime('%Y%m%d')}"
        c.drawString(60, 60, f"Certificate ID: {cert_id}")
        
        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(hex_to_color(colors.get('accent', '#8B4513')))
        footer_text = f"Generated using {template.name} • Certificate Management System"
        c.drawCentredString(width/2, 40, footer_text)
        
        c.save()
        print(f"✓ Premium certificate saved: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating premium certificate: {e}")
        import traceback
        traceback.print_exc()
        return None



def generate_certificate_with_template(event, student, template, certificate_folder):
    """Generate certificate using specific template"""
    return generate_premium_certificate(event, student, template, certificate_folder)


def generate_basic_certificate(event, student, certificate_folder):
    """Enhanced basic certificate generation"""
    filename = f"certificate_{student.id}_{event.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(certificate_folder, filename)
    
    try:
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        
        # ADD BACKGROUND IMAGE SUPPORT
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        
        # Draw background image if available, otherwise use default background
        background_drawn = False
        if hasattr(event, 'background_path') and event.background_path:
            background_image = os.path.join(upload_folder, event.background_path)
            if os.path.exists(background_image):
                try:
                    c.drawImage(background_image, 0, 0, width, height, preserveAspectRatio=False)
                    background_drawn = True
                    print("✓ Background image drawn in basic certificate")
                except Exception as e:
                    print(f"✗ Error drawing background in basic certificate: {e}")
        
        # Only use default background if no image was drawn
        if not background_drawn:
            c.setFillColor(HexColor('#FAFAFA'))
            c.rect(0, 0, width, height, fill=1)
        
        # ADD LOGO IMAGE SUPPORT
        if hasattr(event, 'logo_path') and event.logo_path:
            logo_image = os.path.join(upload_folder, event.logo_path)
            if os.path.exists(logo_image):
                try:
                    c.drawImage(logo_image, 60, height - 130, width=100, height=100,
                               preserveAspectRatio=True, mask='auto')
                    print("✓ Logo image drawn in basic certificate")
                except Exception as e:
                    print(f"✗ Error drawing logo in basic certificate: {e}")
        
        # Border
        #c.setStrokeColor(gold)
        #c.setLineWidth(4)
        #c.rect(40, 40, width-80, height-80)
        
        # Title with custom font
        title_font = get_font("StoryScript", "Helvetica-Bold")
        c.setFont(title_font, 36)
        c.setFillColor(gold)
        c.drawCentredString(width/2, height-180, "CERTIFICATE OF ACHIEVEMENT")
        
        # Decorative line
        c.setStrokeColor(HexColor("#FBFBFB"))
        c.setLineWidth(2)
        c.line(150, height-200, width-150, height-200)
        
        # Content
        body_font = get_font("StoryScript", "Helvetica")
        c.setFont(body_font, 18)
        c.setFillColor(black)
        c.drawCentredString(width/2, height-240, "This is to certify that")
        
        c.setFont(title_font, 30)
        c.setFillColor(gold)
        c.drawCentredString(width/2, height-300, student.name.upper())
        
        c.setFont(body_font, 16)
        c.setFillColor(black)
        event_type_text = ""
        if hasattr(event, 'event_type') and event.event_type:
            event_type_text = f" ({event.event_type.value})"
        
        c.drawCentredString(width/2, height-340, f"has successfully participated in{event_type_text}")
        
        c.setFont(title_font, 22)
        c.setFillColor(gold)
        c.drawCentredString(width/2, height-380, event.title)
        
        # Event details
        c.setFont(body_font, 14)
        c.setFillColor(black)
        
        if hasattr(event, 'organizer') and event.organizer:
            c.drawCentredString(width/2, height-420, f"Organized by: {event.organizer}")
        
        if hasattr(event, 'location') and event.location:
            c.drawCentredString(width/2, height-440, f"Location: {event.location}")
        
        if hasattr(event, 'start_date') and event.start_date:
            if hasattr(event, 'end_date') and event.end_date and event.start_date != event.end_date:
                c.drawCentredString(width/2, height-460, f"Date: {event.start_date.strftime('%B %d, %Y')} - {event.end_date.strftime('%B %d, %Y')}")
            else:
                c.drawCentredString(width/2, height-480, f"Date: {event.start_date.strftime('%B %d, %Y')}")
        elif hasattr(event, 'date') and event.date:
            c.drawCentredString(width/2, height-460, f"Date: {event.date.strftime('%B %d, %Y')}")
        
        # ADD SIGNATURE IMAGE SUPPORT
        if hasattr(event, 'signature_path') and event.signature_path:
            signature_image = os.path.join(upload_folder, event.signature_path)
            if os.path.exists(signature_image):
                try:
                    c.drawImage(signature_image, width - 200, 100, 
                               width=120, height=50, preserveAspectRatio=True, mask='auto')
                    print("✓ Signature image drawn in basic certificate")
                except Exception as e:
                    print(f"✗ Error drawing signature in basic certificate: {e}")
        
        # Signature line and text
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.line(width - 200, 90, width - 80, 90)
        c.setFont(body_font, 12)
        c.drawCentredString(width - 140, 70, "Authorized Signature")
        
        # Certificate ID
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor('#888888'))
        cert_id = f"Certificate ID: CERT-{event.id}-{student.id}-{datetime.now().strftime('%Y%m%d')}"
        c.drawCentredString(width/2, 50, cert_id)
        
        c.save()
        print(f"✓ Basic certificate saved: {filepath}")
        return filepath
    
    except Exception as e:
        print(f"Error generating basic certificate: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_certificate_pdf(event, student, certificate_folder, template_id=None, certificate_type="default"):
    """Main function to generate certificate (NO RANKING SUPPORT)"""
    template = None
    
    if template_id:
        template = CertificateTemplate.query.get(template_id)
    
    # Certificate type selection (NO RANKING PARAMETERS)
    if certificate_type == "custom_font":
        return generate_custom_font_certificate(event, student, certificate_folder)
    elif certificate_type == "enhanced":
        return generate_enhanced_certificate(event, student, certificate_folder)
    elif certificate_type == "basic":
        return generate_basic_certificate(event, student, certificate_folder)
    elif certificate_type == "premium" and template:
        return generate_premium_certificate(event, student, template, certificate_folder)
    
    # Auto-detection logic
    event_type = ""
    if hasattr(event, 'event_type') and event.event_type:
        event_type = event.event_type.value.lower()
    
    event_title = event.title.lower() if hasattr(event, 'title') else ""
    
    if ('webinar' in event_title or 'flask' in event_title or 'development' in event_title):
        return generate_custom_font_certificate(event, student, certificate_folder)
    
    if (event_type in ['lecture', 'seminar'] or 'research' in event_title):
        return generate_basic_certificate(event, student, certificate_folder)
    
    if template:
        return generate_premium_certificate(event, student, template, certificate_folder)
    
    return generate_enhanced_certificate(event, student, certificate_folder)


def generate_bulk_certificates(event, students, certificate_folder, template_id=None, certificate_type="default"):
    """Generate bulk certificates (NO RANKING SUPPORT)"""
    pdf_paths = []
    
    for student in students:
        try:
            pdf_path = generate_certificate_pdf(event, student, certificate_folder, template_id, certificate_type)
            pdf_paths.append(pdf_path)
            print(f"Generated certificate for {student.name}: {pdf_path}")
        except Exception as e:
            print(f"Failed to generate certificate for {student.name}: {e}")
            pdf_paths.append(None)
    
    return pdf_paths


# Standalone function for testing (kept for compatibility)
def create_certificate_with_custom_font(name, output_file="certificate_custom_font.pdf", 
                                       border_image="static/images/border.jpg",
                                       sign="static/images/sign1.png", 
                                       logo="static/images/ampics_logo.png"):
    """Standalone certificate generation function (for testing)"""
    
    # Mock event and student objects for standalone use
    class MockEvent:
        def __init__(self):
            self.title = "Flask Web Development"
            self.description = "1.5-hours webinar on Flask Web Development"
            self.id = 1
    
    class MockStudent:
        def __init__(self, name):
            self.name = name
            self.id = 1
    
    # Create mock objects
    event = MockEvent()
    student = MockStudent(name)
    
    # Generate certificate using the integrated function
    certificate_folder = os.path.dirname(output_file) or "."
    return generate_custom_font_certificate(
        event, student, certificate_folder, 
        border_image=border_image, 
        sign=sign, 
        logo=logo
    )
