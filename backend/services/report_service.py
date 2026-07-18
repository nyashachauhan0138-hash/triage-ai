from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import uuid

class ReportService:

    @staticmethod
    def generate(data):
        unique_id = str(uuid.uuid4())
        filename = f"triage_report_{unique_id}.pdf"

        # Create document template with standard margins
        doc = SimpleDocTemplate(
            filename,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()
        
        # Define clean, custom styles for a premium medical layout
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1A365D'), # Deep Navy
            spaceAfter=15
        )
        
        header_style = ParagraphStyle(
            'ReportHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#2C5282'), # Navy accent
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor('#2D3748'), # Charcoal
            spaceAfter=8
        )
        
        bullet_style = ParagraphStyle(
            'ReportBullet',
            parent=body_style,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4
        )

        elements = []

        # 1. Title Block
        elements.append(Paragraph("TriageAI Medical Assessment Report", title_style))
        elements.append(Paragraph(f"<b>Assessment ID:</b> {unique_id[:8].upper()}-{unique_id[9:13].upper()}", body_style))
        elements.append(Spacer(1, 15))

        # Fields we want to ignore in the final patient PDF report
        ignore_keys = {"next_question", "triage_complete", "message", "emergency_mode"}

        # Ordered key mappings for clean formatting and presentation
        key_mappings = {
            "symptoms": "Reported Symptoms",
            "extracted_symptoms": "Extracted Symptoms",
            "body_regions": "Affected Body Regions",
            "severity_score": "Clinical Severity Score",
            "care_level": "Recommended Care Level",
            "local_severity_prediction": "Local ML Severity Prediction",
            "emergency_flag": "Emergency Flag",
            "possible_diseases": "Suspected / Expected Diseases",
            "recommended_tests": "Recommended Diagnostic Tests",
            "recommendation": "Recommendations",
            "summary": "Clinical Summary"
        }

        # Format and append each relevant field
        for raw_key, label in key_mappings.items():
            if raw_key in ignore_keys or raw_key not in data:
                continue
                
            val = data[raw_key]
            
            # Skip empty or null values
            if val is None or val == "" or (isinstance(val, list) and len(val) == 0):
                continue

            # Add a sub-heading for the section
            elements.append(Paragraph(label, header_style))

            # Format the content based on its type
            if isinstance(val, list):
                for item in val:
                    # Render as clean bullet points
                    elements.append(Paragraph(f"• {item}", bullet_style))
            else:
                # Format boolean/scores/text nicely
                if isinstance(val, bool):
                    val_str = "Yes" if val else "No"
                else:
                    val_str = str(val).capitalize() if isinstance(val, str) else str(val)
                elements.append(Paragraph(val_str, body_style))
                
            elements.append(Spacer(1, 4))

        # Build PDF
        doc.build(elements)
        return filename