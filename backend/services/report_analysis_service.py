# pyrefly: ignore [missing-import]
import os
import base64
from pypdf import PdfReader
from PIL import Image
from pathlib import Path
from services.groq_service import GroqService, _get_client
from services.symptom_classifier_service import SymptomClassifierService
from utils.helpers import extract_json

class ReportAnalysisService:

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extracts selectable text from a PDF file.
        """
        try:
            reader = PdfReader(pdf_path)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            return extracted_text.strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""

    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """
        Extracts medical details from a PNG/JPG using Groq's multimodal Llama Vision model.
        """
        try:
            # Read and encode image to base64
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            # Get groq client
            client = _get_client()
            
            # Query the vision model
            response = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": "Extract all medical findings, lab test values, diagnostic observations, and patient symptoms from this medical report. Output a clear, structured summary of the clinical details."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{encoded_string}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.2
            )
            
            extracted_text = response.choices[0].message.content if response.choices else ""
            print(f"Vision model successfully extracted text from image.")
            return extracted_text.strip()
        except Exception as e:
            print(f"Error extracting text from image {image_path}: {e}")
            import traceback
            traceback.print_exc()
            return ""

    @classmethod
    def analyze_report(cls, file_path: str) -> dict:
        """
        Analyzes the uploaded PDF/Image report and runs it through the triage engine.
        """
        ext = os.path.splitext(file_path)[1].lower()
        extracted_text = ""

        if ext == ".pdf":
            print(f"Analyzing PDF report: {file_path}")
            extracted_text = cls.extract_text_from_pdf(file_path)
            if not extracted_text:
                return {
                    "error": "Could not extract text from PDF. If it is a scanned document, please upload it as an image (PNG/JPG)."
                }
        elif ext in [".png", ".jpg", ".jpeg"]:
            print(f"Analyzing Image report: {file_path}")
            extracted_text = cls.extract_text_from_image(file_path)
            if not extracted_text:
                return {
                    "error": "Failed to read text from the image. Please verify the image quality."
                }
        else:
            return {
                "error": "Unsupported file format. Please upload a PDF, PNG, or JPG file."
            }

        # Query the Triage LLM with the extracted medical text
        print(f"Sending extracted text to Triage engine (Length: {len(extracted_text)})")
        from models.chat import Message
        dummy_messages = [
            Message(role="user", content=f"Here is a medical report/lab results summary: \n\n{extracted_text}\n\nPlease analyze my symptoms and triage my state.")
        ]
        
        from services.triage import TriageCoordinator
        triage_data = TriageCoordinator.triage(dummy_messages)

        # Run local custom-trained classifier on the extracted text
        local_prediction = SymptomClassifierService.predict(extracted_text[:1000]) # Pass snippet
        triage_data["local_severity_prediction"] = local_prediction
        triage_data["emergency_mode"] = triage_data["emergency_flag"]
        triage_data["extracted_report_text"] = extracted_text

        return triage_data
