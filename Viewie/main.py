import os
from flask import Flask, render_template, request, send_file, jsonify
from viewiebackend import ViewieCodeVisualizer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    code = data.get('code')  # This will be the combined code content of multiple files

    if not code:
        return {'error': 'No code provided'}, 400

    visualizer = ViewieCodeVisualizer()

    # Parse the combined Python code using AST
    tree, error_message = visualizer.parse_code(code)
    if error_message:
        return {'error': f'Failed to parse code: {error_message}'}, 400

    # Extract classes and functions from the combined code
    classes, functions = visualizer.code_extraction(tree)

    # Prepare to return classes data along with UML file
    output_directory = 'UML_Diagram_Pictures'
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    uml_file_path = visualizer.uml_generation(classes, functions, output_directory)

    filename = os.path.basename(uml_file_path)

    return {
        'message': f'UML generated and saved as "{output_directory}/{filename}"',
        'uml_file': filename,
        'classes': classes
    }

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    output_directory = 'UML_Diagram_Pictures'
    uml_file_path = os.path.join(output_directory, 'uml_diagram.png')

    if not os.path.exists(uml_file_path):
        return jsonify({'error': 'No UML diagram available to export'}), 400

    visualizer = ViewieCodeVisualizer()

    pdf_file_path, error_message = visualizer.export_to_pdf(uml_file_path, output_directory)

    if error_message:
        return jsonify({'error': f'Failed to export to PDF: {error_message}'}), 400

    # Send the download link to the client
    return jsonify({'pdf_url': f'/UML_Diagram_Pictures/{os.path.basename(pdf_file_path)}'})

@app.route('/UML_Diagram_Pictures/<path:filename>', methods=['GET'])
def get_uml_or_pdf(filename):
    return send_file(os.path.join('UML_Diagram_Pictures', filename))

if __name__ == '__main__':
    app.run(debug=True)
