import os
import ast
from fpdf import FPDF
import graphviz

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


#@app.route('/UML_Diagram_Pictures/<path:filename>', methods=['GET'])
#def get_uml_or_pdf(filename):
#    return send_from_directory('UML_Diagram_Pictures', filename)

