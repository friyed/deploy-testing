from flask import Flask, request, jsonify
import json
import base64
import os
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_FILE_PATH = 'saved-html.json'

@app.route("/") 
def mainpage():
    return "Protolyst web-clipping"

@app.route('/saved-html', methods=["GET", "POST"])
def savedhtml():
    if request.method == "GET":
        with open("saved-html.json", "r") as f:
            data = json.load(f)
            return jsonify(data)

    if request.method != 'POST':
        return 'Invalid request method. Use POST.'

    request_json = request.get_json()

    if 'html_content' not in request_json:
        return jsonify({'error': 'Missing HTML content in the request JSON'})

    html_content = base64.b64decode(request_json['html_content']).decode('utf-8')

    if not html_content:
        return jsonify({'error': 'Empty HTML content. Provide valid HTML data'})

    # Load existing HTML data from the JSON file
    html_data = load_html_data()

    # Append the new HTML content
    html_data.append(html_content)

    # Save the updated HTML data back to the JSON file
    save_html_data(html_data)

    return jsonify({'message': 'HTML saved successfully'}) 

@app.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method. Use POST.'})

    request_json = request.get_json()

    if 'email' not in request_json or 'password' not in request_json:
        return jsonify({'error': 'Missing email or password in the request JSON'})

    email = request_json['email']
    password = request_json['password']

    # Add login logic here 

    #return message just for example
    return jsonify({'message': 'Login successful'})

@app.route('/workspaces')
def get_workspaces():
    with open('workspaces.json', 'r') as file:
        workspaces_data = json.load(file)
    workspaces_list = workspaces_data['workspaces']
    return jsonify({'workspaces': workspaces_list})

@app.route('/folders')
def get_folders():
    with open('folders.json', 'r') as file:
        folders_data = json.load(file)
    folders_list = folders_data['folders']
    return jsonify({'folders': folders_list})


def load_html_data():
    if os.path.exists(HTML_FILE_PATH):
        with open(HTML_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_html_data(html_data):
    with open(HTML_FILE_PATH, 'w') as file:
        json.dump(html_data, file, indent=2)

if __name__ == "__main__":
    app.run("localhost", 7000)
