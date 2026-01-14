import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

export default function GraphVisualization({ graphData }) {
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
    if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
      return;
    }

    const elements = [
      ...graphData.nodes.map((node) => ({
        data: { id: node.id, label: node.label },
      })),
      ...graphData.edges.map((edge) => ({
        data: {
          id: `${edge.source}-${edge.target}`,
          source: edge.source,
          target: edge.target,
          label: edge.label,
        },
      })),
    ];

    const layout = {
      name: "cose",
      directed: false,
      animate: true,
      animationDuration: 500,
    };

    const stylesheet = [
      {
        selector: "node",
        style: {
          "background-color": "#3b82f6",
          label: "data(label)",
          color: "#ffffff",
          "text-valign": "center",
          "text-halign": "center",
          width: "50px",
          height: "50px",
          "font-size": "12px",
        },
      },
      {
        selector: "edge",
        style: {
          "line-color": "#cbd5e1",
          "target-arrow-color": "#cbd5e1",
          "target-arrow-shape": "triangle",
          label: "data(label)",
          "font-size": "10px",
          color: "#64748b",
        },
      },
    ];

    if (containerRef.current) {
      cyRef.current = cytoscape({
        container: containerRef.current,
        elements: elements,
        layout: layout,
        style: stylesheet,
      });
    }

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [graphData]);

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div className="text-center text-gray-500 p-8">
        No entities found to visualize
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="w-full h-96 bg-white rounded-lg border border-gray-200"
    />
  );
}
