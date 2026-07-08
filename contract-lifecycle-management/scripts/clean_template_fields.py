"""
Utility to clean Microsoft Word field codes from DOCX templates
Removes field codes that cause "Error: Reference source not found" in PDFs

This script converts all Word field codes to plain text, which is equivalent to:
  Opening in Word -> Ctrl+A -> Ctrl+Shift+F9 -> Save
"""
from docx import Document
import os
import shutil
import subprocess
from datetime import datetime


def is_tracked_by_git(file_path):
    """Check if file is tracked by Git"""
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', file_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(file_path)) or '.'
        )
        return result.returncode == 0
    except Exception:
        return False


def backup_template(template_path):
    """
    Create a backup of the original template
    Only creates manual backup if file is NOT tracked by Git
    """
    # Check if Git is tracking this file
    if is_tracked_by_git(template_path):
        print(f"[GIT] Template is version controlled - no manual backup needed")
        print(f"      Restore with: git checkout HEAD -- {os.path.basename(template_path)}")
        return None

    # Not in Git - create manual backup
    backup_dir = os.path.join(os.path.dirname(template_path), 'backup')
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(template_path)
    backup_path = os.path.join(backup_dir, f"{filename}.backup_{timestamp}")

    shutil.copy2(template_path, backup_path)
    print(f"[BACKUP] Created: {backup_path}")
    return backup_path


def clean_field_codes(template_path):
    """
    Remove all Word field codes from a DOCX template

    This converts field codes like { REF bookmark } to plain text,
    eliminating "Error: Reference source not found" errors in PDFs.
    """
    print(f"\n[CLEANING] {os.path.basename(template_path)}")

    try:
        # Load document
        doc = Document(template_path)

        # Track what we remove
        fields_removed = 0

        # Remove field character elements (complex fields)
        for element in list(doc.element.body.iter()):
            tag = element.tag

            # Remove field characters
            if tag.endswith('}fldChar'):
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
                    fields_removed += 1

            # Remove field instruction text
            elif tag.endswith('}instrText'):
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
                    fields_removed += 1

        # Remove simple fields (fldSimple)
        for element in list(doc.element.body.iter()):
            if element.tag.endswith('}fldSimple'):
                # Extract the text content
                text_content = ''.join(element.itertext())

                # Replace field with text
                parent = element.getparent()
                if parent is not None:
                    # Create a text run with the content
                    from docx.oxml import parse_xml
                    from docx.oxml.ns import qn

                    w_namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

                    # Create a new run element with the text
                    new_run = parse_xml(f'<w:r xmlns:w="{w_namespace[1:-1]}"><w:t>{text_content}</w:t></w:r>')

                    # Replace field with plain text run
                    parent.replace(element, new_run)
                    fields_removed += 1

        # Save cleaned template
        doc.save(template_path)

        if fields_removed > 0:
            print(f"[OK] Removed {fields_removed} field code elements")
            return True
        else:
            print(f"[OK] No field codes found (template was already clean)")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to clean template: {e}")
        import traceback
        traceback.print_exc()
        return False


def clean_all_templates():
    """Clean all templates (both main contract and section templates)"""

    print("=" * 80)
    print("CLEANING WORD FIELD CODES FROM TEMPLATES")
    print("=" * 80)
    print("\nThis removes field codes that cause 'Error: Reference source not found'")
    print("Equivalent to: Word -> Ctrl+A -> Ctrl+Shift+F9 -> Save\n")

    # Define all templates to clean
    templates_config = [
        # Main contract template
        {
            'name': 'pc-template.docx',
            'path': os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'pc-template.docx')
        },
        # Section templates
        {
            'name': 'S1_Customer_Info.docx',
            'path': os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'pc-templates', 'S1_Customer_Info.docx')
        },
        {
            'name': 'S2_Sites_Info.docx',
            'path': os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'pc-templates', 'S2_Sites_Info.docx')
        },
        {
            'name': 'S3_EFL_Info.docx',
            'path': os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'pc-templates', 'S3_EFL_Info.docx')
        },
        {
            'name': 'S4_NRG_Term_and_Service.docx',
            'path': os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'pc-templates', 'S4_NRG_Term_and_Service.docx')
        },
        {
            'name': 'S5_Rights_as_Customer_Placeholder.docx',
            'path': os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'pc-templates', 'S5_Rights_as_Customer_Placeholder.docx')
        }
    ]

    cleaned_count = 0
    backup_paths = []
    processed_count = 0

    for template_config in templates_config:
        template_name = template_config['name']
        template_path = template_config['path']

        if not os.path.exists(template_path):
            print(f"\n[SKIP] {template_name} - Not found at {template_path}")
            continue

        processed_count += 1

        # Backup original
        backup_path = backup_template(template_path)
        if backup_path:
            backup_paths.append(backup_path)

        # Clean field codes
        was_cleaned = clean_field_codes(template_path)
        if was_cleaned:
            cleaned_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("CLEANING COMPLETE")
    print("=" * 80)
    print(f"\nTemplates found: {processed_count}")
    print(f"Templates cleaned: {cleaned_count}")
    print(f"Templates already clean: {processed_count - cleaned_count}")

    if any(backup_paths):
        print(f"\nManual backups created (not in Git):")
        for backup_path in backup_paths:
            if backup_path:
                print(f"  - {backup_path}")

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. Test generators:")
    print("   python scripts/generate_contract_open_source.py  # Main contract")
    print("   python scripts/generate_s1_customer_info_open_source.py  # Section 1")
    print("   python scripts/generate_s2_sites_info_open_source.py  # Section 2")
    print("   ... etc")
    print("\n2. Check generated PDFs:")
    print("   - Open output/*.pdf files")
    print("   - Verify NO 'Error: Reference source not found' messages")
    print("\n3. Validate templates (optional):")
    print("   python scripts/validate_templates.py assets/templates/*.docx assets/templates/pc-templates/*.docx")
    print()


if __name__ == "__main__":
    clean_all_templates()
