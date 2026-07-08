"""
Utility module for automatic template cleaning
Ensures templates are field-code-free before document generation
"""
from docx import Document
import os
import hashlib
import json


class TemplateCleaner:
    """
    Automatic template cleaner with caching to avoid redundant cleaning
    """

    CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'output', '.template_cache')

    @staticmethod
    def _get_file_hash(file_path):
        """Calculate MD5 hash of a file"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    @staticmethod
    def _is_template_clean(template_path):
        """
        Check if template has already been cleaned (using cache)

        Returns:
            bool: True if template is already clean, False if needs cleaning
        """
        os.makedirs(TemplateCleaner.CACHE_DIR, exist_ok=True)

        cache_file = os.path.join(
            TemplateCleaner.CACHE_DIR,
            f"{os.path.basename(template_path)}.cache.json"
        )

        # Get current file hash
        current_hash = TemplateCleaner._get_file_hash(template_path)

        # Check cache
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    if cache_data.get('hash') == current_hash and cache_data.get('cleaned'):
                        return True
            except Exception:
                pass

        return False

    @staticmethod
    def _mark_template_clean(template_path):
        """Mark template as cleaned in cache"""
        os.makedirs(TemplateCleaner.CACHE_DIR, exist_ok=True)

        cache_file = os.path.join(
            TemplateCleaner.CACHE_DIR,
            f"{os.path.basename(template_path)}.cache.json"
        )

        cache_data = {
            'hash': TemplateCleaner._get_file_hash(template_path),
            'cleaned': True,
            'template': os.path.basename(template_path)
        }

        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)

    @staticmethod
    def clean_field_codes_inplace(template_path, force=False):
        """
        Clean field codes from a template (modifies the file in-place)
        Uses caching to skip already-cleaned templates

        Args:
            template_path: Path to the template file
            force: If True, clean even if cache says it's already clean

        Returns:
            bool: True if template was cleaned, False if it was already clean
        """
        if not force and TemplateCleaner._is_template_clean(template_path):
            return False  # Already clean

        try:
            # Load document
            doc = Document(template_path)

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

                        w_namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

                        # Create a new run element with the text
                        new_run = parse_xml(f'<w:r xmlns:w="{w_namespace[1:-1]}"><w:t>{text_content}</w:t></w:r>')

                        # Replace field with plain text run
                        parent.replace(element, new_run)
                        fields_removed += 1

            # Save cleaned template
            doc.save(template_path)

            # Mark as clean in cache
            TemplateCleaner._mark_template_clean(template_path)

            return fields_removed > 0

        except Exception as e:
            print(f"[WARNING] Failed to auto-clean template {os.path.basename(template_path)}: {e}")
            return False

    @staticmethod
    def ensure_template_clean(template_path, verbose=False):
        """
        Ensure a template is clean before use (idempotent operation)

        Args:
            template_path: Path to the template file
            verbose: If True, print status messages

        Returns:
            bool: True if successful (either was clean or was cleaned)
        """
        if not os.path.exists(template_path):
            if verbose:
                print(f"[ERROR] Template not found: {template_path}")
            return False

        try:
            was_cleaned = TemplateCleaner.clean_field_codes_inplace(template_path)

            if verbose:
                if was_cleaned:
                    print(f"[AUTO-CLEAN] Cleaned field codes from {os.path.basename(template_path)}")
                else:
                    print(f"[OK] Template already clean: {os.path.basename(template_path)}")

            return True

        except Exception as e:
            if verbose:
                print(f"[ERROR] Failed to clean template: {e}")
            return False


# Convenience function for use in generation scripts
def ensure_clean(template_path, verbose=False):
    """
    Convenience wrapper for ensuring a template is clean

    Usage in generation scripts:
        from utils.template_cleaner import ensure_clean
        ensure_clean(TEMPLATE_PATH, verbose=True)
    """
    return TemplateCleaner.ensure_template_clean(template_path, verbose=verbose)
