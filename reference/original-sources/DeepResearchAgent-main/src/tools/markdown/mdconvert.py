import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

import tempfile
from typing import Any
import os

import camelot
from litellm import transcription
from markitdown import MarkItDown
from markitdown._markitdown import DocumentConverterResult
import pymupdf
import pdfplumber
from PIL import Image
import pillow_heif

# Register HEIF opener for PIL
pillow_heif.register_heif_opener()

from src.logger import logger
from src.models import model_manager


def read_tables_from_stream(file_stream):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp_pdf:
        temp_pdf.write(file_stream.read())
        temp_pdf.flush()
        tables = camelot.read_pdf(temp_pdf.name, flavor="lattice")
        return tables

def transcribe_audio(file_stream, audio_format):

    if "whisper" in model_manager.registered_models:
        # Use the Whisper model for transcription
        model = model_manager.registered_models["whisper"]
        result = model(
            file_stream=file_stream,
        )
    else:
        response = transcription(model="gpt-4o-transcribe", file=file_stream).json()
        result = response.get("text", "No transcription available.")

    return result

class AudioWhisperConverter:
    """Custom audio converter using transcription service"""

    def convert(self, local_path: str, **kwargs: Any) -> DocumentConverterResult:
        md_content = ""

        # Figure out the audio format for transcription from file path
        file_extension = os.path.splitext(local_path)[1].lower()
        if file_extension == ".wav":
            audio_format = "wav"
        elif file_extension == ".mp3":
            audio_format = "mp3"
        elif file_extension in [".mp4", ".m4a"]:
            audio_format = "mp4"
        else:
            audio_format = None

        # Transcribe
        if audio_format:
            try:
                with open(local_path, 'rb') as file_stream:
                    transcript = transcribe_audio(file_stream, audio_format=audio_format)
                    if transcript:
                        md_content += "### Audio Transcript:\n" + transcript
            except (FileNotFoundError, Exception) as e:
                logger.warning(f"Audio transcription failed: {e}")
                md_content = "Audio file detected but transcription failed."

        return DocumentConverterResult(markdown=md_content.strip())

class PdfWithTableConverter:
    """Custom PDF converter using pymupdf and pdfplumber"""

    def convert(self, local_path: str, **kwargs: Any) -> DocumentConverterResult:
        md_content = ""

        try:
            # Use pymupdf for basic text extraction
            doc = pymupdf.open(local_path)
            text_content = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text_content += f"## Page {page_num + 1}\n\n"
                text_content += page.get_text() + "\n\n"
            doc.close()

            md_content += text_content

            # Use pdfplumber for table extraction
            try:
                with pdfplumber.open(local_path) as pdf:
                    tables_found = False
                    for page_num, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        if tables:
                            if not tables_found:
                                md_content += "\n## Extracted Tables\n\n"
                                tables_found = True

                            for table_idx, table in enumerate(tables):
                                md_content += f"### Table {table_idx + 1} (Page {page_num + 1})\n\n"
                                # Convert table to markdown
                                if table and len(table) > 0:
                                    # Create header row
                                    header = table[0]
                                    md_content += "| " + " | ".join(str(cell) if cell else "" for cell in header) + " |\n"
                                    md_content += "| " + " | ".join("---" for _ in header) + " |\n"

                                    # Add data rows
                                    for row in table[1:]:
                                        md_content += "| " + " | ".join(str(cell) if cell else "" for cell in row) + " |\n"
                                    md_content += "\n"

            except Exception as e:
                logger.warning(f"Table extraction failed: {e}")

        except Exception as e:
            logger.warning(f"PDF conversion failed: {e}")
            md_content = "PDF file detected but conversion failed."

        return DocumentConverterResult(markdown=md_content.strip())

class MarkitdownConverter:
    def __init__(self,
                 use_llm: bool = False,
                 model_id: str = None,
                 timeout: int = 30):

        self.timeout = timeout
        self.use_llm = use_llm
        self.model_id = model_id

        if use_llm:
            client = model_manager.registered_models(model_id).http_client
            self.client = MarkItDown(
                llm_client=client,
                llm_model=model_id,
            )
        else:
            self.client = MarkItDown()

        # Register custom converters as standalone processors
        self.pdf_converter = PdfWithTableConverter()
        self.audio_converter = AudioWhisperConverter()

    def convert(self, source: str, **kwargs: Any):
        try:
            # Check if source is a file with custom converter
            if os.path.isfile(source):
                file_extension = os.path.splitext(source)[1].lower()

                # Use custom PDF converter for PDFs
                if file_extension == '.pdf':
                    return self.pdf_converter.convert(source, **kwargs)

                # Use custom audio converter for audio files
                elif file_extension in ['.wav', '.mp3', '.mp4', '.m4a']:
                    return self.audio_converter.convert(source, **kwargs)

            # Fall back to standard MarkItDown for other files
            result = self.client.convert(source, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error during conversion: {e}")
            return None
