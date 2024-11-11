import * as tidyTree from './tidyTree.js'
import * as forceGraph from './forceDirectedGraph.js'


const UML_Image = '<img src="/UML_Diagram_Pictures/uml_diagram.png" alt="UML Diagram">';
const umlDiagramShow = document.getElementById('showUML');
const force = document.getElementById('showForceDirected');
const tidy = document.getElementById('showTidyTree');
const visualization = document.getElementById('visualization');

let classes = [];

document.getElementById('codeForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const code = document.getElementById('code').value;

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({code}),
        });

        const data = await response.json();

        if (response.ok) {

            // Display output text
            document.getElementById('output').innerText = data.message;
            classes = data.classes;

            console.log('This is the classes:', classes)

            // Set event listeners for visualizations

                // Display UML Diagram
            umlDiagramShow.addEventListener("click", function(){
                visualization.innerHTML = UML_Image;
            });
                // Display Force-Directed Graph
            force.addEventListener("click", function(){
                visualization.innerHTML = '';
                visualization.appendChild(forceGraph.renderForceDirectedGraph(classes));
            });

                // Display Tidy Tree Graph
            tidy.addEventListener("click", function(){
                visualization.innerHTML = '';
                tidyTree.renderTidyTree(classes);
            });

        } else {
            document.getElementById('output').innerText = data.error;
        }
    } catch (error) {
        document.getElementById('output').innerText = 'An error occurred: ' + error.message;
    }
});
