"""
Test script to verify automatic template cleaning works correctly
"""
import os
import sys

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from utils.template_cleaner import TemplateCleaner


def test_auto_cleaning():
    """Test the auto-cleaning functionality"""

    print("=" * 80)
    print("TESTING AUTOMATIC TEMPLATE CLEANING")
    print("=" * 80)

    # Define templates to test
    base_dir = os.path.join(SCRIPT_DIR, '..')

    templates = [
        {
            'name': 'Main Contract Template',
            'path': os.path.join(base_dir, 'assets', 'templates', 'pc-template.docx')
        },
        {
            'name': 'S1 - Customer Info',
            'path': os.path.join(base_dir, 'assets', 'templates', 'pc-templates', 'S1_Customer_Info.docx')
        },
        {
            'name': 'S2 - Sites Info',
            'path': os.path.join(base_dir, 'assets', 'templates', 'pc-templates', 'S2_Sites_Info.docx')
        },
        {
            'name': 'S3 - EFL Info',
            'path': os.path.join(base_dir, 'assets', 'templates', 'pc-templates', 'S3_EFL_Info.docx')
        },
        {
            'name': 'S4 - NRG Terms',
            'path': os.path.join(base_dir, 'assets', 'templates', 'pc-templates', 'S4_NRG_Term_and_Service.docx')
        },
        {
            'name': 'S5 - Customer Rights',
            'path': os.path.join(base_dir, 'assets', 'templates', 'pc-templates', 'S5_Rights_as_Customer_Placeholder.docx')
        }
    ]

    print("\n[Phase 1] First-time cleaning (will modify templates if needed)\n")

    results = []

    for template in templates:
        if not os.path.exists(template['path']):
            print(f"[SKIP] {template['name']} - Not found")
            results.append({'name': template['name'], 'status': 'not_found'})
            continue

        try:
            was_cleaned = TemplateCleaner.clean_field_codes_inplace(template['path'], force=False)

            if was_cleaned:
                print(f"[CLEANED] {template['name']}")
                results.append({'name': template['name'], 'status': 'cleaned'})
            else:
                print(f"[OK] {template['name']} - Already clean (cached)")
                results.append({'name': template['name'], 'status': 'cached'})

        except Exception as e:
            print(f"[ERROR] {template['name']} - {e}")
            results.append({'name': template['name'], 'status': 'error', 'error': str(e)})

    print("\n[Phase 2] Cached lookup test (should be instant)\n")

    for template in templates:
        if not os.path.exists(template['path']):
            continue

        try:
            was_cleaned = TemplateCleaner.clean_field_codes_inplace(template['path'], force=False)

            if was_cleaned:
                print(f"[WARNING] {template['name']} - Unexpected cleaning (cache miss)")
            else:
                print(f"[OK] {template['name']} - Cache hit [PASS]")

        except Exception as e:
            print(f"[ERROR] {template['name']} - {e}")

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    cleaned_count = sum(1 for r in results if r['status'] == 'cleaned')
    cached_count = sum(1 for r in results if r['status'] == 'cached')
    error_count = sum(1 for r in results if r['status'] == 'error')
    not_found_count = sum(1 for r in results if r['status'] == 'not_found')

    print(f"\nTemplates found: {len(results) - not_found_count}")
    print(f"Templates cleaned: {cleaned_count}")
    print(f"Templates already clean (cached): {cached_count}")
    print(f"Errors: {error_count}")

    if error_count > 0:
        print("\n[ERRORS]")
        for r in results:
            if r['status'] == 'error':
                print(f"  - {r['name']}: {r.get('error', 'Unknown error')}")

    print(f"\nCache location: {TemplateCleaner.CACHE_DIR}")
    print("\n[SUCCESS] AUTO-CLEANING TEST COMPLETE")
    print()


if __name__ == "__main__":
    test_auto_cleaning()
