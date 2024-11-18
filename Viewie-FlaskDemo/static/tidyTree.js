import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';

export function renderTidyTree(classes) {
    const width = 928;

    // Convert the classes data into a format suitable for d3.hierarchy
    // Prepare the data for D3.js
    const data = {
        name: "Root",
        children: classes.map(cls => ({
            name: cls[0], // Class name
            children: [
                ...cls[1].attributes.map(attr => ({ name: attr, type: "attribute" })), // Map attributes
                ...cls[1].methods.map(method => ({ name: method, type: "method" })) // Map methods
            ]
        }))
    };

    const root = d3.hierarchy(data);
    const dx = 10;
    const dy = width / (root.height + 1);

    const tree = d3.tree().nodeSize([dx, dy]);

    root.sort((a, b) => d3.ascending(a.data.name, b.data.name));
    tree(root);

    let x0 = Infinity;
    let x1 = -x0;
    root.each(d => {
        if (d.x > x1) x1 = d.x;
        if (d.x < x0) x0 = d.x;
    });

    const height = x1 - x0 + dx * 2;

    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-dy / 3, x0 - dx, width, height])
        .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");

    const link = svg.append("g")
        .attr("fill", "none")
        .attr("stroke", "#555")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 1.5)
        .selectAll()
        .data(root.links())
        .join("path")
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x));

    const node = svg.append("g")
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 3)
        .selectAll()
        .data(root.descendants())
        .join("g")
        .attr("transform", d => `translate(${d.y},${d.x})`);

    node.append("circle")
        .attr("fill", d => d.children ? "#555" : "#999")
        .attr("r", 2.5);

    node.append("text")
        .attr("dy", "0.31em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => d.data.name)
        .attr("stroke", "white")
        .attr("paint-order", "stroke");

    // Append the SVG to the visualization container
    d3.select("#visualization").html('').append(() => svg.node());
}