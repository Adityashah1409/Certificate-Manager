import json
from models import CertificateTemplate, db

# Predefined template configurations
PREDEFINED_TEMPLATES = {
    "elegant_royal": {
        "name": "Elegant Royal",
        "description": "Luxurious royal blue and gold design",
        "colors": {
            "primary": "#1E3A8A",
            "secondary": "#D4AF37", 
            "accent": "#8B4513",
            "text": "#2D3748"
        },
        "fonts": {
            "title": {"family": "Helvetica-Bold", "size": 42},
            "subtitle": {"family": "Helvetica-Oblique", "size": 18},
            "name": {"family": "Helvetica-Bold", "size": 36},
            "content": {"family": "Helvetica", "size": 16}
        },
        "layout": {
            "border_width": 4,
            "margin": 40
        }
    },
    
    "modern_professional": {
        "name": "Modern Professional",
        "description": "Clean, contemporary design for corporate events",
        "colors": {
            "primary": "#2563EB",
            "secondary": "#64748B",
            "accent": "#F59E0B",
            "text": "#1F2937"
        },
        "fonts": {
            "title": {"family": "Helvetica-Bold", "size": 38},
            "subtitle": {"family": "Helvetica", "size": 16},
            "name": {"family": "Helvetica-Bold", "size": 32},
            "content": {"family": "Helvetica", "size": 15}
        }
    },

    "classic_black_white": {
        "name": "Classic Black & White",
        "description": "Timeless black and white design with metallic accents",
        "colors": {
            "primary": "#000000",
            "secondary": "#FFFFFF",
            "accent": "#C0C0C0",
            "text": "#2D2D2D"
        },
        "fonts": {
            "title": {"family": "Helvetica-Bold", "size": 40},
            "name": {"family": "Helvetica-Bold", "size": 34},
            "content": {"family": "Helvetica", "size": 14}
        }
    }
}

def create_default_templates():
    """Create default certificate templates"""
    try:
        for template_key, template_data in PREDEFINED_TEMPLATES.items():
            # Check if template already exists
            existing_template = CertificateTemplate.query.filter_by(name=template_data["name"]).first()
            
            if not existing_template:
                template = CertificateTemplate(
                    name=template_data["name"],
                    description=template_data["description"],
                    template_type='predefined',
                    is_active=True
                )
                
                # Set template configuration
                template.template_config = {
                    "colors": template_data["colors"],
                    "fonts": template_data["fonts"],
                    "layout": template_data.get("layout", {})
                }
                
                db.session.add(template)
        
        db.session.commit()
        print("Default templates created successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default templates: {e}")