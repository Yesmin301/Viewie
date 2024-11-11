import ast
import os

import graphviz


class ViewieCodeVisualizer:
    def __init__(self):
        # No display_widget needed
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
