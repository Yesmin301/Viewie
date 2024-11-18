import * as tidyTree from './tidyTree.js';
import * as forceGraph from './forceDirectedGraph.js';

const UML_Image = '<img src="/UML_Diagram_Pictures/uml_diagram.png" alt="UML Diagram">';
const umlDiagramShow = document.getElementById('showUML');
const force = document.getElementById('showForceDirected');
const tidy = document.getElementById('showTidyTree');
const visualization = document.getElementById('visualization');

let classes = [];

// File input element
const fileUpload = document.getElementById('fileUpload');

// Handle file input change
fileUpload.addEventListener('change', function(event) {
    const files = event.target.files;
    let combinedCode = '';

    if (files.length > 0) {
        for (let file of files) {
            if (file.name.endsWith('.py')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    combinedCode += e.target.result + '\n';  // Concatenate file contents
                    document.getElementById('code').value = combinedCode;  // Populate textarea
                };
                reader.readAsText(file);
            } else {
                document.getElementById('output').innerText = 'Please upload valid .py files';
            }
        }
    }
});

document.getElementById('codeForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const code = document.getElementById('code').value;  // Get the code from the textarea

    // Check if code is empty
    if (!code.trim()) {
        document.getElementById('output').innerText = 'Please provide code to upload!';
        return;
    }

    try {
        // Send the combined code to the backend
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }), // Send combined code in JSON format
        });

        const data = await response.json();

        if (response.ok) {
            // Display success message and classes info
            document.getElementById('output').innerText = data.message;
            classes = data.classes;

            // Set event listeners for visualizations
            umlDiagramShow.addEventListener("click", function() {
                visualization.innerHTML = UML_Image;
            });

            force.addEventListener("click", function() {
                visualization.innerHTML = '';
                visualization.appendChild(forceGraph.renderForceDirectedGraph(classes));
            });

            tidy.addEventListener("click", function() {
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

document.getElementById('exportPDF').addEventListener("click", async function() {
    // Check if the visualization container has any content (whether it's an image, graph, or tree)
    if (visualization.innerHTML.trim() === "") {
        alert('No visualization available to export.');
        return;
    }

    try {
        // Request the server to export the PDF
        const response = await fetch('/export_pdf', {
            method: 'POST',
        });

        // Log the response for debugging
        const text = await response.text();  // Get the raw response text
        console.log("Server response:", text);

        // Check if the response is valid JSON
        const data = JSON.parse(text);  // Parse the response as JSON

        if (response.ok) {
            // Successfully received PDF URL
            const pdfUrl = data.pdf_url;

            // Create a link element to trigger download
            const downloadLink = document.createElement('a');
            downloadLink.href = pdfUrl;
            downloadLink.download = 'uml_diagram.pdf';  // Optional: specify filename
            downloadLink.click();  // Trigger the download
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error during PDF export:', error);  // Log error details
        alert('Error exporting to PDF: ' + error.message);
    }
});