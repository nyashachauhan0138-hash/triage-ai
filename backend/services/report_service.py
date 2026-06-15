from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


import uuid

class ReportService:

    @staticmethod
    def generate(data):

        unique_id = str(uuid.uuid4())
        filename = f"triage_report_{unique_id}.pdf"

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        elements = []

        title = Paragraph(
            "TriageAI Report",
            styles["Title"]
        )

        elements.append(title)
        elements.append(Spacer(1, 12))

        for key, value in data.items():

            elements.append(
                Paragraph(
                    f"<b>{key}</b>: {value}",
                    styles["BodyText"]
                )
            )

            elements.append(Spacer(1, 8))

        doc.build(elements)

        return filename