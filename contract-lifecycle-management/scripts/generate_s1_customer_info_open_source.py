"""
Section 1: Customer Info Generation - Open-Source Approach
Uses: docxtpl (Jinja2) + LibreOffice for PDF conversion
Similar pattern to generate_contract_api.py
"""
from docxtpl import DocxTemplate
from datetime import datetime
import os
import sys
import subprocess
import time

# Add scripts directory to path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from utils.template_cleaner import ensure_clean

# Configuration
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "templates", "pc-templates", "S1_Customer_Info.docx")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"


def generate_s1_customer_info(customer_data: dict):
    """
    Generate Section 1: Customer Info document

    Args:
        customer_data: Dictionary containing customer information

    Returns:
        tuple: (docx_path, pdf_path, docx_time, pdf_time) or (docx_path, None, docx_time, 0) if PDF fails
    """

    print(f"\n[S1] Generating Customer Info for: {customer_data.get('customerName')}")

    total_start = time.time()

    # Ensure template is clean and load it
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template not found at {TEMPLATE_PATH}")

    # Auto-clean template to remove field codes
    ensure_clean(TEMPLATE_PATH)

    doc = DocxTemplate(TEMPLATE_PATH)

    # Populate data
    docx_start = time.time()
    doc.render(customer_data)

    # Save DOCX
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    docx_filename = f"s1_customer_info_{timestamp}.docx"
    docx_path = os.path.join(OUTPUT_DIR, docx_filename)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc.save(docx_path)

    docx_time = time.time() - docx_start
    print(f"[OK] DOCX generated: {docx_path}")
    print(f"      Time taken: {docx_time:.3f} seconds")

    # Convert to PDF
    pdf_filename = f"s1_customer_info_{timestamp}.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    pdf_start = time.time()
    success = convert_to_pdf_libreoffice(docx_path, pdf_path)
    pdf_time = time.time() - pdf_start

    if success:
        print(f"[OK] PDF generated: {pdf_path}")
        print(f"      Time taken: {pdf_time:.3f} seconds")
    else:
        print(f"[FAILED] PDF conversion unsuccessful")
        pdf_path = None
        pdf_time = 0

    return docx_path, pdf_path, docx_time, pdf_time


def convert_to_pdf_libreoffice(docx_path: str, pdf_path: str) -> bool:
    """Convert DOCX to PDF using LibreOffice headless mode"""

    if not os.path.exists(LIBREOFFICE_PATH):
        print(f"[WARN] LibreOffice not found at: {LIBREOFFICE_PATH}")
        return False

    try:
        output_dir = os.path.dirname(os.path.abspath(pdf_path))
        docx_abs_path = os.path.abspath(docx_path)

        cmd = [
            LIBREOFFICE_PATH,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            docx_abs_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.returncode == 0

    except Exception as e:
        print(f"[ERROR] PDF conversion failed: {e}")
        return False


# Sample data for testing
SAMPLE_DATA = {
    "customerName": "Delray Oil Refining Company",
    "primaryContact": "John Smith",
    "addressLine1": "901 Louisiana St",
    "city": "Houston",
    "state": "Texas",
    "zip": "77002",
    "emailAddress": "john.smith@delrayoil.com",
    "billingAddressLine": "1901 Louisiana St",
    "billingCity": "Houston",
    "billingState": "Texas",
    "billingZip": "77102",
    "language": "English"
}


if __name__ == "__main__":
    print("=" * 80)
    print("SECTION 1: CUSTOMER INFO GENERATION - OPEN-SOURCE APPROACH")
    print("Library: docxtpl (Jinja2) + LibreOffice")
    print("=" * 80)

    try:
        print(f"\n[1/3] Loading template and generating DOCX...")
        print(f"      Customer: {SAMPLE_DATA['customerName']}")

        total_start = time.time()
        docx_path, pdf_path, docx_time, pdf_time = generate_s1_customer_info(SAMPLE_DATA)
        total_time = time.time() - total_start

        print("\n" + "=" * 80)
        print("GENERATION COMPLETE - SECTION 1")
        print("=" * 80)
        print(f"\nPerformance Metrics:")
        print(f"  DOCX Generation:    {docx_time:.3f} seconds")
        if pdf_path:
            print(f"  PDF Conversion:     {pdf_time:.3f} seconds")
        print(f"  Total Time:         {total_time:.3f} seconds")

        print(f"\nGenerated Files:")
        print(f"  DOCX: {os.path.abspath(docx_path)}")
        if pdf_path:
            print(f"  PDF:  {os.path.abspath(pdf_path)}")
        print()
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
