import os
import ast
import graphviz
from flask import Flask, render_template, request, send_from_directory, jsonify
from fpdf import FPDF

app = Flask(__name__)


class ViewieCodeVisualizer:
    def __init__(self):
        pass

    def parse_code(self, code):
        try:
            tree = ast.parse(code)
            return tree, None  # Return the AST tree and None for error message
        except SyntaxError as e:
            return None, str(e)  # Return None and the error message

    def code_extraction(self, tree):
        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                attributes = []  # To collect attributes

                # Extract attributes defined in the class
                for body_item in node.body:
                    if isinstance(body_item, ast.Assign):
                        for target in body_item.targets:
                            if isinstance(target, ast.Name):
                                attributes.append(target.id)

                classes.append((class_name, {"methods": method_names, "attributes": attributes}))

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)  # We still capture top-level functions, if needed

        return classes, functions

    def uml_generation(self, classes, functions, output_directory):
        dot = graphviz.Digraph()

        for class_name, details in classes:
            dot.node(class_name, shape='box')

            # Add attributes to the class
            if "attributes" in details:
                for attribute in details["attributes"]:
                    dot.node(f"{class_name}.{attribute}", label=attribute, shape="plaintext")
                    dot.edge(class_name, f"{class_name}.{attribute}", style="dashed")  # Dashed line for attributes

            # Add methods to the class
            if "methods" in details:
                for method in details["methods"]:
                    dot.edge(class_name, method, label=method)

        for function in functions:
            dot.node(function, shape="ellipse")

        uml_file_path = os.path.join(output_directory, 'uml_diagram')
        uml_pic = dot.render(uml_file_path, format='png')

        return uml_pic

    def export_to_pdf(self, image_path, output_directory):
        """ Converts PNG to PDF and saves it in the output directory while maintaining the aspect ratio. """
        try:
            # Create a PDF object
            pdf = FPDF()
            pdf.add_page()

            # Add the image to the PDF
            pdf.image(image_path, x=10, y=10, w=180)  # Adjust the width (w) as needed

            # Save the PDF
            pdf_file_path = os.path.join(output_directory, 'uml_diagram.pdf')
            pdf.output(pdf_file_path)

            return pdf_file_path, None  # Return the PDF file path and None as the error message (success case)

        except Exception as e:
            return None, str(e)  # Return None and the error message in case of failure


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
    return send_from_directory('UML_Diagram_Pictures', filename)


if __name__ == '__main__':
    app.run(debug=True)
