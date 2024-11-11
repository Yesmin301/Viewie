import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';

export function renderForceDirectedGraph(classes) {
    // Define dimensions
    const width = 1500;
    const height = 1000;


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
    console.log('Data for Force-Directed Graph:', data); // Log data

    // Create a hierarchy from the data
    const root = d3.hierarchy(data);
    const links = root.links();  // Create links from hierarchy
    const nodes = root.descendants();  // Create nodes from hierarchy

    // Start the force simulation
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.data.name).distance(100).strength(1)) // Ensure .id() points correctly
        .force("charge", d3.forceManyBody().strength(-50))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    // Create the container SVG
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto;");

    // Append links
    const link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line");

    // Append nodes
    const node = svg.append("g")
        .attr("fill", "#fff")
        .attr("stroke", "#000")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("fill", d => d.data.type === "method" ? "#000" : "#aaa")
        .attr("r", 3.5)
        .call(drag(simulation)); // Attach drag behavior

    node.append("title").text(d => d.data.name);

    // Update positions on tick
    simulation.on("tick", () => {
        console.log('REPEAT REPEAT TICK IS FIRING HOLY')
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });

    return svg.node();
}

// Drag functionality
const drag = simulation => {
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}