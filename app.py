from flask import Flask, request, render_template_string, make_response
import base64
import xml.etree.ElementTree as ET

app = Flask(__name__)

FLAG = base64.b64encode(b"STURSEC{XX3_F0UN6}").decode('utf-8')
TOKEN = "secure-token-1234"

@app.route('/')
def index():
    # Send the token in a header for obfuscation
    response = make_response('''
    <!doctype html>
    <title>Broken XML Parser</title>
    <h1>XML Data Processor</h1>
    <p>Upload an XML file to process it. Only valid XML content is accepted.</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="token">Token:</label>
        <input type="text" id="token" name="token" placeholder="Enter your token"><br><br>
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    ''')
    response.headers['X-TOKEN-HINT'] = TOKEN[::-1]  # Reverse the token as a hint
    return response

@app.route('/upload', methods=['POST'])
def upload():
    token = request.form.get('token')
    if token != TOKEN:
        return "<h2>Invalid Token</h2>", 403

    try:
        xml_data = request.files['file'].read().decode('utf-8')
        if "<!DOCTYPE" in xml_data or "SYSTEM" in xml_data:
            return "<h2>Invalid XML content detected</h2>", 400

        parsed_data = ET.fromstring(xml_data)  # Vulnerable XML parsing
        return f"<h2>Parsed XML:</h2><pre>{ET.tostring(parsed_data, encoding='unicode')}</pre>"
    except Exception as e:
        return f"<h2>Error:</h2><pre>{str(e)}</pre>"

if __name__ == '__main__':
    with open('/flag.txt', 'w') as f:
        f.write(FLAG)  # Store the Base64 encoded flag
    app.run(host='0.0.0.0', port=5001)

