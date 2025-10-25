from flask import Flask, request, jsonify
from flask_cors import CORS
from ftplib import FTP
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# FTP credentials - store these in a .env file
FTP_HOST = os.getenv('FTP_HOST', 'tervingo.com')
FTP_USER = os.getenv('FTP_USER', '')
FTP_PASS = os.getenv('FTP_PASS', '')
FTP_PATH = '/public_html/Felisarium'

def upload_file_to_ftp(filename, content):
    try:
        # Convert content to bytes
        content_bytes = content.encode('utf-8')
        
        # Connect to FTP server
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Navigate to the correct directory
        ftp.cwd(FTP_PATH)
        
        # Upload the file
        ftp.storbinary(f'STOR {filename}', io.BytesIO(content_bytes))
        
        # Close FTP connection
        ftp.quit()
        
        return {'message': 'File uploaded successfully'}, 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'error': str(e)}, 500

@app.route('/upload-felisadas', methods=['POST'])
def upload_felisadas():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    return jsonify(*upload_file_to_ftp('felisadas.txt', content))

@app.route('/upload-otros', methods=['POST'])
def upload_otros():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    return jsonify(*upload_file_to_ftp('otros.txt', content))

@app.route('/upload-serranadas', methods=['POST'])
def upload_serranadas():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    return jsonify(*upload_file_to_ftp('serranadas.txt', content))

if __name__ == '__main__':
    app.run(port=5000, debug=True)