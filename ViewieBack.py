import ast
from tkinter import *
import graphviz


class ViewieCodeVisualizer:
    def __init__(self, display_widget):
        self.display_widget = display_widget

    def parse_code(self, code):
        try:
            tree = ast.parse(code)
            return tree  # Return the AST tree
        except SyntaxError as e:
            self.display_widget.insert(END, f"Error parsing code: {e}\n")
            return None

    def code_extraction(self, tree):
        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append((class_name, method_names))
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return classes, functions

    def uml_generation(self, classes, functions):
        dot = graphviz.Digraph()

        for class_name, methods in classes:
            dot.node(class_name, shape="box")
            for method in methods:
                dot.edge(class_name, method, label=method)

        for function in functions:
            dot.node(function, shape="ellipse")

        dot.render('uml_diagram', format='png')
        return "uml_diagram.png"


