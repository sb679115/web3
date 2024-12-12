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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Broken XML Parser - Sturtle Security</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            background: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }

        .header {
            background: #4CAF50;
            color: #fff;
            text-align: center;
            padding: 20px;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
        }

        .content {
            padding: 20px;
            text-align: center;
        }

        .content p {
            margin-bottom: 20px;
            color: #555;
        }

        .form-container {
            margin-top: 20px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }

        input[type="text"],
        input[type="file"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        input[type="submit"] {
            background: #4CAF50;
            color: #fff;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 16px;
            border-radius: 4px;
        }

        input[type="submit"]:hover {
            background: #45a049;
        }

        .footer {
            text-align: center;
            background: #f4f4f9;
            padding: 10px;
            font-size: 14px;
            color: #777;
        }

        .footer a {
            color: #4CAF50;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Broken XML Parser</h1>
        </div>
        <div class="content">
            <p>Welcome to Sturtle Security's XML Data Processor. Upload an XML file to process it. Only valid XML content is accepted.</p>
            <form action="/upload" method="post" enctype="multipart/form-data" class="form-container">
                <label for="token">Token:</label>
                <input type="text" id="token" name="token" placeholder="Enter your token" required>

                <label for="file">Upload XML File:</label>
                <input type="file" name="file" id="file" required>

                <input type="submit" value="Upload">
            </form>
        </div>
    </div>
    <div class="footer">
        &copy; 2024 Sturtle Security. All rights reserved. | <a href="#">Privacy Policy</a>
    </div>
</body>
</html>
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

