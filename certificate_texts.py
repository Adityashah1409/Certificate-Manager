# certificate_texts.py
from enum import Enum

class EventType(Enum):
    SEMINAR = "Seminar"
    WORKSHOP = "Workshop"
    WEBINAR = "Webinar"
    CONFERENCE = "Conference"
    LECTURE = "Lecture"
    TRAINING = "Training"
    COMPETITION = "Competition"
    HACKATHON = "Hackathon"

# Certificate text configurations by event type (NO RANKING SUPPORT)
CERTIFICATE_TEXT_CONFIG = {
    EventType.SEMINAR: {
        'title': 'Certificate of Participation',
        'subtitle': 'This certificate is proudly presented to',
        'accomplishment': 'for attending the seminar on',
        'closing': 'and demonstrating keen interest in learning.'
    },
    
    EventType.WORKSHOP: {
        'title': 'Certificate of Completion',
        'subtitle': 'This certificate is proudly awarded to',
        'accomplishment': 'for successfully completing the workshop on',
        'closing': 'and gaining practical skills in the subject.'
    },
    
    EventType.WEBINAR: {
        'title': 'Certificate of Attendance',
        'subtitle': 'This certificate is presented to',
        'accomplishment': 'for attending the webinar on',
        'closing': 'and engaging in virtual learning.'
    },
    
    EventType.CONFERENCE: {
        'title': 'Certificate of Presentation',
        'subtitle': 'This certificate is awarded to',
        'accomplishment': 'for presenting a paper at the conference on',
        'closing': 'and contributing to academic discourse.'
    },
    
    EventType.LECTURE: {
        'title': 'Certificate of Appreciation',
        'subtitle': 'This certificate is presented to',
        'accomplishment': 'for delivering an insightful lecture on',
        'closing': 'and sharing valuable knowledge.'
    },
    
    EventType.TRAINING: {
        'title': 'Certificate of Training',
        'subtitle': 'This certificate is awarded to',
        'accomplishment': 'for completing training in',
        'closing': 'and developing professional competency.'
    },
    
    EventType.COMPETITION: {
        'title': 'Certificate of Achievement',
        'subtitle': 'This certificate is proudly awarded to',
        'accomplishment': 'for outstanding performance in',
        'closing': 'and demonstrating exceptional skills.'
    },
    
    EventType.HACKATHON: {
        'title': 'Certificate of Innovation',
        'subtitle': 'This certificate is presented to',
        'accomplishment': 'for participating and demonstrating innovation in',
        'closing': 'and showcasing creative problem-solving abilities.'
    }
}

# Default configuration for unknown event types
DEFAULT_CERTIFICATE_TEXT = {
    'title': 'Certificate of Achievement',
    'subtitle': 'This certificate is proudly presented to',
    'accomplishment': 'for successfully participating in',
    'closing': 'and demonstrating commitment to excellence.'
}

def get_certificate_text_config(event_type):
    """Get certificate text configuration for given event type"""
    if isinstance(event_type, str):
        try:
            event_type = EventType(event_type)
        except ValueError:
            return DEFAULT_CERTIFICATE_TEXT
    
    return CERTIFICATE_TEXT_CONFIG.get(event_type, DEFAULT_CERTIFICATE_TEXT)

def format_certificate_text(event, student):
    """Format certificate text based on event type and details (NO RANKING)"""
    event_type = getattr(event, 'event_type', None)
    config = get_certificate_text_config(event_type)
    
    # Get event title
    event_title = getattr(event, 'title', 'the event')
    
    # Format accomplishment text
    accomplishment_text = f"{config['accomplishment']} {event_title}"
    
    return {
        'title': config['title'],
        'subtitle': config['subtitle'],
        'accomplishment': accomplishment_text,
        'closing': config['closing']
    }
