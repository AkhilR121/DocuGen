"""
CLM POC - Commercial/Licensing Approach
Uses: Aspose.Words for Python (all operations)
"""
import aspose.words as aw
from datetime import datetime
import os
import sys
import time

# Configuration
TEMPLATE_PATH = "assets/templates/pc-template.docx"
OUTPUT_DIR = "output"

# Hardcoded contract data
CONTRACT_DATA = {
    "customerName": "Test Customer One",
    "primaryContact": "primary contact name",
    "addressLine1": "901 louisiana st",
    "city": "Houston",
    "state": "Texas",
    "zip": "77002",
    "emailAddress": "tempemail@gmail.com",
    "billingAddressLine": "1901 louisiana st",
    "billingCity": "Houston",
    "billingState": "Texas",
    "billingZip": "77102",
    "language": "English",
    "contractPrice": "1.57",
    "startDate": "07/01/2026",
    "endDate": "06/30/2027",
    "contractDuration": "12 months",
    "sites": [
        {
            "esiid": "9999999",
            "startOption": "move-in",
            "startDate": "07/01/2026",
            "addressLine": "901 louisiana st",
            "city": "Houston",
            "state": "Texas",
            "zip": "77002",
        },
        {
            "esiid": "8888888",
            "startOption": "switch",
            "startDate": "07/01/2026",
            "addressLine": "901 louisiana st",
            "city": "Houston",
            "state": "Texas",
            "zip": "77002",
        },
        {
            "esiid": "7777777",
            "startOption": "switch",
            "startDate": "07/01/2026",
            "addressLine": "901 louisiana st",
            "city": "Houston",
            "state": "Texas",
            "zip": "77002",
        },
    ]
}


def insert_sites_table(doc, sites):
    """Insert sites table after the MVI paragraph"""
    if not sites:
        return

    # Find the paragraph with "MVI = Move-In"
    target_para_index = -1
    for i, para in enumerate(doc.get_child_nodes(aw.NodeType.PARAGRAPH, True)):
        para_text = para.as_paragraph().get_text()
        if "MVI = Move-In" in para_text:
            target_para_index = i
            break

    if target_para_index == -1:
        print("[WARNING] Could not find MVI paragraph, skipping sites table")
        return

    # Get the parent section
    target_para = doc.get_child_nodes(aw.NodeType.PARAGRAPH, True)[target_para_index].as_paragraph()
    parent_section = target_para.parent_section

    # Create table with builder
    builder = aw.DocumentBuilder(doc)
    builder.move_to(target_para)
    builder.move_to_paragraph(target_para_index, 0)

    # Start table
    table = builder.start_table()

    # Add header row
    headers = ["SERVICE ADDRESS", "ESI ID", "START OPTION\nMVI / SWI / REN", "START DATE\nif applicable"]
    for i, header_text in enumerate(headers):
        builder.insert_cell()
        from aspose.pydrawing import Color
        builder.cell_format.shading.background_pattern_color = Color.light_gray
        builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
        builder.font.bold = True
        builder.write(header_text)
    builder.end_row()

    # Add data rows
    builder.font.bold = False
    builder.paragraph_format.alignment = aw.ParagraphAlignment.LEFT

    for site in sites:
        # Service Address
        builder.insert_cell()
        address = f"{site.get('addressLine', '')}\n{site.get('city', '')} {site.get('state', '')} {site.get('zip', '')}"
        builder.write(address)

        # ESI ID
        builder.insert_cell()
        builder.write(site.get('esiid', ''))

        # Start Option
        builder.insert_cell()
        start_option = site.get('startOption', '').lower()
        if start_option == 'move-in':
            builder.write("X Move-in\n  Switch")
        elif start_option == 'switch':
            builder.write("  Move-in\nX Switch")
        else:
            builder.write("  Move-in\n  Switch")

        # Start Date
        builder.insert_cell()
        builder.write(site.get('startDate', ''))

        builder.end_row()

    builder.end_table()

    print(f"      Inserted sites table with {len(sites)} rows")


def generate_contract():
    """Generate contract using Aspose.Words approach"""

    print("=" * 80)
    print("CLM POC - COMMERCIAL/LICENSING APPROACH")
    print("Library: Aspose.Words for Python")
    print("=" * 80)

    total_start = time.time()

    # Step 1: Load template
    print(f"\n[1/4] Loading template: {TEMPLATE_PATH}")
    if not os.path.exists(TEMPLATE_PATH):
        print(f"ERROR: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

    try:
        doc = aw.Document(TEMPLATE_PATH)
        print("[OK] Template loaded")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Step 2: Populate data and save DOCX
    print(f"\n[2/4] Populating data and generating DOCX...")
    print(f"      Customer: {CONTRACT_DATA['customerName']}")
    print(f"      Location: {CONTRACT_DATA['city']}, {CONTRACT_DATA['state']}")
    print(f"      Period: {CONTRACT_DATA['startDate']} - {CONTRACT_DATA['endDate']}")

    docx_start = time.time()

    try:
        # Replace all placeholders using Find & Replace
        options = aw.replacing.FindReplaceOptions()

        for field, value in CONTRACT_DATA.items():
            if field != "sites":  # Skip sites array
                placeholder = "{{ " + field + " }}"  # Single space on each side
                doc.range.replace(placeholder, str(value), options)

        # Insert sites table after the MVI paragraph
        insert_sites_table(doc, CONTRACT_DATA.get("sites", []))

        # Save DOCX
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        docx_filename = f"contract_aspose_{timestamp}.docx"
        docx_path = os.path.join(OUTPUT_DIR, docx_filename)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        doc.save(docx_path)

        docx_time = time.time() - docx_start

        print(f"[OK] DOCX generated: {docx_path}")
        print(f"      Time taken: {docx_time:.3f} seconds")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Step 3: Convert to PDF using Aspose.Words
    pdf_filename = f"contract_aspose_{timestamp}.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    print(f"\n[3/4] Converting DOCX to PDF using Aspose.Words...")

    pdf_start = time.time()

    try:
        # Direct PDF conversion with high fidelity
        doc.save(pdf_path, aw.SaveFormat.PDF)

        pdf_time = time.time() - pdf_start

        print(f"[OK] PDF generated: {pdf_path}")
        print(f"      Time taken: {pdf_time:.3f} seconds")

    except Exception as e:
        print(f"ERROR: PDF conversion failed: {e}")
        pdf_path = None
        pdf_time = 0

    # Summary
    total_time = time.time() - total_start

    print("\n" + "=" * 80)
    print("GENERATION COMPLETE - COMMERCIAL APPROACH")
    print("=" * 80)
    print(f"\nPerformance Metrics:")
    print(f"  DOCX Generation:    {docx_time:.3f} seconds")
    if pdf_path:
        print(f"  PDF Conversion:     {pdf_time:.3f} seconds")
        print(f"  Total Time:         {total_time:.3f} seconds")
    else:
        print(f"  PDF Conversion:     FAILED")
        print(f"  Total Time (DOCX):  {docx_time:.3f} seconds")

    print(f"\nGenerated Files:")
    print(f"  DOCX: {os.path.abspath(docx_path)}")
    if pdf_path:
        print(f"  PDF:  {os.path.abspath(pdf_path)}")
    print()

    print("Note: Aspose.Words runs in evaluation mode without license.")
    print("      Evaluation watermark will appear on output documents.")
    print("      For production, acquire license from: https://purchase.aspose.com/")
    print()

    return docx_path, pdf_path


if __name__ == "__main__":
    generate_contract()
