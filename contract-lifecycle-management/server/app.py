"""
Flask API Server for Contract Lifecycle Management
Provides REST API endpoints for the React frontend
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from datetime import datetime
import json

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.insert(0, os.path.abspath(scripts_dir))

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/contracts/generate', methods=['POST'])
def generate_contract():
    """
    Generate a contract using specified approach

    Expected request body:
    {
        "data": {
            "customerName": "...",
            "primaryContact": "...",
            ...
        },
        "approach": "opensource" | "aspose"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        contract_data = data.get('data')
        approach = data.get('approach', 'opensource')

        if not contract_data:
            return jsonify({'success': False, 'error': 'Contract data is required'}), 400

        if approach not in ['opensource', 'aspose']:
            return jsonify({'success': False, 'error': 'Invalid approach. Use "opensource" or "aspose"'}), 400

        # Import the generation module
        from generate_contract_api import generate_contract_with_data

        # Generate the contract
        start_time = datetime.now()
        docx_path, pdf_path = generate_contract_with_data(contract_data)
        end_time = datetime.now()

        total_time = (end_time - start_time).total_seconds()

        return jsonify({
            'success': True,
            'docxPath': os.path.basename(docx_path) if docx_path else None,
            'pdfPath': os.path.basename(pdf_path) if pdf_path else None,
            'metrics': {
                'totalTime': total_time
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/contracts', methods=['GET'])
def list_contracts():
    """Get list of all generated contracts"""
    try:
        if not os.path.exists(OUTPUT_DIR):
            return jsonify([])

        files = []
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(('.docx', '.pdf')):
                files.append(filename)

        # Sort by modification time (newest first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)

        return jsonify(files)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contracts/download', methods=['GET'])
def download_contract():
    """Download a generated contract file"""
    try:
        filename = request.args.get('path')

        if not filename:
            return jsonify({'error': 'Filename is required'}), 400

        # Security: ensure filename doesn't contain path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({'error': 'Invalid filename'}), 400

        file_path = os.path.join(OUTPUT_DIR, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 80)
    print("Contract Lifecycle Management API Server")
    print("=" * 80)
    print(f"Server running on: http://localhost:5000")
    print(f"Frontend should connect to: http://localhost:5000/api")
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 80)
    print("\nAvailable endpoints:")
    print("  GET  /api/health")
    print("  POST /api/contracts/generate")
    print("  GET  /api/contracts")
    print("  GET  /api/contracts/download?path=<filename>")
    print("\n" + "=" * 80)

    app.run(debug=True, host='0.0.0.0', port=5000)
