import os

from flask import Flask, render_template, request, send_file
from viewiebackend import ViewieCodeVisualizer

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    code = data.get('code')

    if not code:
        return {'error': 'No code provided'}, 400

    visualizer = ViewieCodeVisualizer()

    tree, error_message = visualizer.parse_code(code)
    if error_message:
        return {'error': f'Failed to parse code: {error_message}'}, 400
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


@app.route('/UML_Diagram_Pictures/<path:filename>', methods=['GET'])
def get_uml(filename):
    return send_file(os.path.join('UML_Diagram_Pictures', filename))


if __name__ == '__main__':
    app.run(debug=True)
