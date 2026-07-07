"""
Merge multiple DOCX section files into one complete contract document
This demonstrates the multi-file template approach mentioned in TODO.md
"""
from docx import Document
from docxtpl import DocxTemplate
from datetime import datetime
import os

# Configuration
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

# Section files in order
SECTION_FILES = [
    "section-1-customer-info.docx",
    "section-2-sites-info.docx",
    "section-3-efl-info.docx",
    "section-4-nrg-terms.docx",
    "section-5-customer-rights.docx"
]

# Sample contract data
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
}


def merge_docx_sections(section_files, output_path):
    """
    Merge multiple DOCX files into one document

    Args:
        section_files: List of DOCX file paths to merge
        output_path: Path where merged document will be saved
    """

    # Create a new document based on the first section
    merged_doc = Document(section_files[0])

    # Append content from remaining sections
    for section_file in section_files[1:]:
        print(f"  Merging: {os.path.basename(section_file)}")

        # Load the section document
        section_doc = Document(section_file)

        # Add a page break before each new section (optional)
        # merged_doc.add_page_break()

        # Copy all elements from the section
        for element in section_doc.element.body:
            merged_doc.element.body.append(element)

    # Save the merged document
    merged_doc.save(output_path)
    print(f"  Merged document saved: {output_path}")

    return output_path


def generate_contract_from_sections():
    """
    Generate a complete contract by:
    1. Rendering each section template with data
    2. Merging all sections into one document
    """

    print("\n" + "="*80)
    print("MULTI-SECTION CONTRACT GENERATION")
    print("="*80)
    print(f"\nTemplates directory: {TEMPLATES_DIR}")
    print(f"Output directory: {OUTPUT_DIR}\n")

    # Step 1: Render each section with data
    print("[1/3] Rendering individual sections with data...")

    rendered_sections = []
    temp_dir = os.path.join(OUTPUT_DIR, "temp_sections")
    os.makedirs(temp_dir, exist_ok=True)

    for section_file in SECTION_FILES:
        section_path = os.path.join(TEMPLATES_DIR, section_file)

        if not os.path.exists(section_path):
            print(f"  [WARNING] Section not found: {section_file} - SKIPPING")
            continue

        print(f"  Rendering: {section_file}")

        try:
            # Load section template
            doc = DocxTemplate(section_path)

            # Render with data
            doc.render(CONTRACT_DATA)

            # Save rendered section temporarily
            temp_section_path = os.path.join(temp_dir, f"rendered_{section_file}")
            doc.save(temp_section_path)

            rendered_sections.append(temp_section_path)

        except Exception as e:
            print(f"  [ERROR] Failed to render {section_file}: {e}")
            continue

    if not rendered_sections:
        print("\n[ERROR] No sections were successfully rendered!")
        return None

    print(f"  Successfully rendered {len(rendered_sections)} sections")

    # Step 2: Merge all rendered sections
    print("\n[2/3] Merging sections into complete contract...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"contract_merged_{timestamp}.docx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        merged_path = merge_docx_sections(rendered_sections, output_path)
    except Exception as e:
        print(f"  [ERROR] Failed to merge sections: {e}")
        import traceback
        traceback.print_exc()
        return None

    # Step 3: Cleanup temporary files
    print("\n[3/3] Cleaning up temporary files...")
    for temp_file in rendered_sections:
        try:
            os.remove(temp_file)
        except:
            pass

    try:
        os.rmdir(temp_dir)
    except:
        pass

    print("\n" + "="*80)
    print("CONTRACT GENERATION COMPLETE")
    print("="*80)
    print(f"\nGenerated file: {merged_path}")
    print(f"Customer: {CONTRACT_DATA['customerName']}")
    print(f"Period: {CONTRACT_DATA['startDate']} - {CONTRACT_DATA['endDate']}")
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Create the 5 section files in assets/templates/:")
    print("   - section-1-customer-info.docx")
    print("   - section-2-sites-info.docx")
    print("   - section-3-efl-info.docx")
    print("   - section-4-nrg-terms.docx")
    print("   - section-5-customer-rights.docx")
    print("2. Copy content from pc-template.docx into each section file")
    print("3. Run this script again to test merging")
    print("="*80 + "\n")

    return merged_path


if __name__ == "__main__":
    generate_contract_from_sections()
