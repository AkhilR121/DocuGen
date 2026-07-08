"""
Template Validator - Detects Word field codes in DOCX templates
Prevents "Error: Reference source not found" in generated PDFs

Usage:
    python validate_templates.py <template_path> [--strict]
    python validate_templates.py assets/templates/pc-templates/*.docx
"""
import zipfile
from lxml import etree
import os
import sys
import argparse


class TemplateValidator:
    """Validates DOCX templates for problematic field codes"""

    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

    @staticmethod
    def detect_field_codes(template_path):
        """
        Detect field codes in a DOCX template

        Returns:
            dict: {
                'has_fields': bool,
                'field_types': list of field types found,
                'field_count': int,
                'details': list of field details
            }
        """
        result = {
            'has_fields': False,
            'field_types': set(),
            'field_count': 0,
            'details': []
        }

        try:
            with zipfile.ZipFile(template_path, 'r') as docx_zip:
                # Read the main document XML
                xml_content = docx_zip.read('word/document.xml')
                tree = etree.fromstring(xml_content)

                # Detect complex fields (fldChar)
                fld_chars = tree.findall(f'.//{TemplateValidator.WORD_NAMESPACE}fldChar')

                # Detect field instruction text
                instr_texts = tree.findall(f'.//{TemplateValidator.WORD_NAMESPACE}instrText')

                # Detect simple fields
                fld_simples = tree.findall(f'.//{TemplateValidator.WORD_NAMESPACE}fldSimple')

                # Parse instruction text to identify field types
                for instr in instr_texts:
                    text = instr.text or ''
                    # Extract field type (first word of instruction)
                    field_type = text.strip().split()[0] if text.strip() else 'UNKNOWN'
                    result['field_types'].add(field_type)
                    result['details'].append({
                        'type': 'complex',
                        'field_type': field_type,
                        'instruction': text.strip()
                    })

                # Parse simple fields
                for fld_simple in fld_simples:
                    instr = fld_simple.get(f'{TemplateValidator.WORD_NAMESPACE}instr', '')
                    field_type = instr.strip().split()[0] if instr.strip() else 'UNKNOWN'
                    result['field_types'].add(field_type)
                    result['details'].append({
                        'type': 'simple',
                        'field_type': field_type,
                        'instruction': instr.strip()
                    })

                result['field_count'] = len(instr_texts) + len(fld_simples)
                result['has_fields'] = result['field_count'] > 0
                result['field_types'] = list(result['field_types'])

        except Exception as e:
            result['error'] = str(e)

        return result

    @staticmethod
    def validate_template(template_path, reject_on_fields=True):
        """
        Validate a template and optionally reject if field codes found

        Args:
            template_path: Path to DOCX template
            reject_on_fields: If True, validation fails when fields detected

        Returns:
            dict: {'valid': bool, 'message': str, 'details': dict}
        """
        if not os.path.exists(template_path):
            return {
                'valid': False,
                'message': f'Template not found: {template_path}',
                'details': {}
            }

        detection = TemplateValidator.detect_field_codes(template_path)

        if detection.get('error'):
            return {
                'valid': False,
                'message': f'Validation error: {detection["error"]}',
                'details': detection
            }

        if detection['has_fields']:
            problematic_types = {'REF', 'PAGEREF', 'HYPERLINK', 'TOC', 'INDEX'}
            found_problematic = problematic_types.intersection(set(detection['field_types']))

            if found_problematic and reject_on_fields:
                return {
                    'valid': False,
                    'message': f'Template contains problematic field codes: {", ".join(found_problematic)}',
                    'details': detection
                }
            else:
                return {
                    'valid': not reject_on_fields,
                    'message': f'Warning: Template contains {detection["field_count"]} field codes',
                    'details': detection
                }

        return {
            'valid': True,
            'message': 'Template is clean (no field codes detected)',
            'details': detection
        }


def validate_all_templates(template_paths, strict=True):
    """
    Validate multiple templates

    Args:
        template_paths: List of template file paths
        strict: If True, reject templates with any field codes

    Returns:
        bool: True if all templates valid, False otherwise
    """
    print("=" * 80)
    print("TEMPLATE VALIDATION")
    print("=" * 80)

    results = []
    for template_path in template_paths:
        template_name = os.path.basename(template_path)
        result = TemplateValidator.validate_template(template_path, reject_on_fields=strict)

        status = "[PASS]" if result['valid'] else "[FAIL]"
        print(f"\n{status} {template_name}")
        print(f"       {result['message']}")

        if result['details'].get('field_types'):
            print(f"       Field types found: {', '.join(result['details']['field_types'])}")

        results.append({
            'template': template_name,
            'path': template_path,
            'result': result
        })

    # Summary
    passed = sum(1 for r in results if r['result']['valid'])
    failed = len(results) - passed

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(results)} templates")
    print("=" * 80)

    if failed > 0:
        print("\nTo fix failed templates:")
        print("  python scripts/clean_template_fields.py")
        print("\nOr clean individual templates:")
        for r in results:
            if not r['result']['valid']:
                print(f"  python scripts/clean_template_fields.py {r['path']}")

    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate DOCX templates for Word field codes'
    )
    parser.add_argument(
        'templates',
        nargs='+',
        help='Template file paths to validate'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        default=True,
        help='Reject templates with any field codes (default: True)'
    )

    args = parser.parse_args()

    # Validate templates
    all_valid = validate_all_templates(args.templates, strict=args.strict)

    # Exit with appropriate code
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
