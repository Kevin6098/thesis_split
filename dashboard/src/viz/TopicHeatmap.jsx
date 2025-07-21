import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert } from '@mui/material';

export default function TopicHeatmap({ dataset }) {
  const svgRef = useRef();
  const [error, setError] = useState(null);

  useEffect(() => {
    const drawHeatmap = async () => {
      try {
        // Mock heatmap data - cluster x topic proportions
        const mockData = dataset === 'high_rating' ? [
          // Format: cluster, topic, proportion
          [0, 0, 0.15], [0, 1, 0.08], [0, 2, 0.12], [0, 3, 0.18], [0, 4, 0.05], [0, 5, 0.22], [0, 6, 0.10], [0, 7, 0.10],
          [1, 0, 0.25], [1, 1, 0.15], [1, 2, 0.08], [1, 3, 0.12], [1, 4, 0.03], [1, 5, 0.18], [1, 6, 0.12], [1, 7, 0.07],
          [2, 0, 0.12], [2, 1, 0.10], [2, 2, 0.28], [2, 3, 0.15], [2, 4, 0.02], [2, 5, 0.08], [2, 6, 0.15], [2, 7, 0.10],
          [3, 0, 0.18], [3, 1, 0.20], [3, 2, 0.05], [3, 3, 0.22], [3, 4, 0.08], [3, 5, 0.12], [3, 6, 0.08], [3, 7, 0.07],
          [4, 0, 0.05], [4, 1, 0.03], [4, 2, 0.02], [4, 3, 0.08], [4, 4, 0.65], [4, 5, 0.05], [4, 6, 0.07], [4, 7, 0.05],
          [5, 0, 0.08], [5, 1, 0.35], [5, 2, 0.05], [5, 3, 0.10], [5, 4, 0.02], [5, 5, 0.15], [5, 6, 0.15], [5, 7, 0.10],
          [6, 0, 0.10], [6, 1, 0.08], [6, 2, 0.12], [6, 3, 0.15], [6, 4, 0.03], [6, 5, 0.12], [6, 6, 0.30], [6, 7, 0.10],
          [7, 0, 0.12], [7, 1, 0.05], [7, 2, 0.08], [7, 3, 0.10], [7, 4, 0.02], [7, 5, 0.08], [7, 6, 0.15], [7, 7, 0.40]
        ] : [
          [0, 0, 0.20], [0, 1, 0.12], [0, 2, 0.08], [0, 3, 0.15], [0, 4, 0.10], [0, 5, 0.15], [0, 6, 0.10], [0, 7, 0.10],
          [1, 0, 0.08], [1, 1, 0.35], [1, 2, 0.12], [1, 3, 0.10], [1, 4, 0.08], [1, 5, 0.12], [1, 6, 0.08], [1, 7, 0.07],
          [2, 0, 0.12], [2, 1, 0.15], [2, 2, 0.30], [2, 3, 0.12], [2, 4, 0.05], [2, 5, 0.10], [2, 6, 0.08], [2, 7, 0.08],
          [3, 0, 0.10], [3, 1, 0.08], [3, 2, 0.15], [3, 3, 0.25], [3, 4, 0.12], [3, 5, 0.15], [3, 6, 0.08], [3, 7, 0.07],
          [4, 0, 0.15], [4, 1, 0.10], [4, 2, 0.08], [4, 3, 0.12], [4, 4, 0.30], [4, 5, 0.10], [4, 6, 0.08], [4, 7, 0.07],
          [5, 0, 0.08], [5, 1, 0.05], [5, 2, 0.10], [5, 3, 0.12], [5, 4, 0.08], [5, 5, 0.40], [5, 6, 0.10], [5, 7, 0.07],
          [6, 0, 0.05], [6, 1, 0.08], [6, 2, 0.05], [6, 3, 0.10], [6, 4, 0.08], [6, 5, 0.12], [6, 6, 0.45], [6, 7, 0.07],
          [7, 0, 0.12], [7, 1, 0.05], [7, 2, 0.08], [7, 3, 0.10], [7, 4, 0.05], [7, 5, 0.08], [7, 6, 0.12], [7, 7, 0.40],
          [8, 0, 0.18], [8, 1, 0.08], [8, 2, 0.12], [8, 3, 0.15], [8, 4, 0.10], [8, 5, 0.12], [8, 6, 0.15], [8, 7, 0.10]
        ];

        // Clear previous chart
        d3.select(svgRef.current).selectAll('*').remove();

        // Set dimensions
        const margin = { top: 60, right: 60, bottom: 60, left: 60 };
        const width = 500;
        const height = 400;

        const svg = d3.select(svgRef.current)
          .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom);

        const g = svg.append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);

        // Get unique clusters and topics
        const clusters = [...new Set(mockData.map(d => d[0]))].sort((a, b) => a - b);
        const topics = [...new Set(mockData.map(d => d[1]))].sort((a, b) => a - b);

        // Scales
        const xScale = d3.scaleBand()
          .domain(topics)
          .range([0, width])
          .padding(0.05);

        const yScale = d3.scaleBand()
          .domain(clusters)
          .range([0, height])
          .padding(0.05);

        const colorScale = d3.scaleSequential()
          .interpolator(d3.interpolateBlues)
          .domain([0, d3.max(mockData, d => d[2])]);

        // Add axes
        g.append('g')
          .attr('transform', `translate(0,${height})`)
          .call(d3.axisBottom(xScale).tickFormat(d => `Topic ${d}`))
          .selectAll('text')
          .style('text-anchor', 'end')
          .attr('dx', '-.8em')
          .attr('dy', '.15em')
          .attr('transform', 'rotate(-45)');

        g.append('g')
          .call(d3.axisLeft(yScale).tickFormat(d => `Cluster ${d}`));

        // Add axis labels
        g.append('text')
          .attr('transform', `translate(${width / 2}, ${height + 50})`)
          .style('text-anchor', 'middle')
          .style('font-size', '12px')
          .text('LDA Topics');

        g.append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 0 - margin.left)
          .attr('x', 0 - (height / 2))
          .attr('dy', '1em')
          .style('text-anchor', 'middle')
          .style('font-size', '12px')
          .text('K-means Clusters');

        // Add heatmap rectangles
        g.selectAll('.cell')
          .data(mockData)
          .enter().append('rect')
          .attr('class', 'cell')
          .attr('x', d => xScale(d[1]))
          .attr('y', d => yScale(d[0]))
          .attr('width', xScale.bandwidth())
          .attr('height', yScale.bandwidth())
          .attr('fill', d => colorScale(d[2]))
          .attr('stroke', '#fff')
          .attr('stroke-width', 1)
          .on('mouseover', function(event, d) {
            // Tooltip
            const tooltip = d3.select('body').append('div')
              .attr('class', 'tooltip')
              .style('position', 'absolute')
              .style('background', 'rgba(0, 0, 0, 0.8)')
              .style('color', 'white')
              .style('padding', '8px')
              .style('border-radius', '4px')
              .style('font-size', '12px')
              .style('pointer-events', 'none');

            tooltip.html(`Cluster ${d[0]} → Topic ${d[1]}<br/>Proportion: ${(d[2] * 100).toFixed(1)}%`)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 10) + 'px');
          })
          .on('mouseout', function() {
            d3.selectAll('.tooltip').remove();
          });

        // Add proportion text in cells
        g.selectAll('.cell-text')
          .data(mockData.filter(d => d[2] > 0.1)) // Only show text for significant proportions
          .enter().append('text')
          .attr('class', 'cell-text')
          .attr('x', d => xScale(d[1]) + xScale.bandwidth() / 2)
          .attr('y', d => yScale(d[0]) + yScale.bandwidth() / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'middle')
          .style('font-size', '10px')
          .style('fill', 'white')
          .style('font-weight', 'bold')
          .text(d => (d[2] * 100).toFixed(0) + '%');

        // Add color legend
        const legendWidth = 200;
        const legendHeight = 10;
        
        const legend = svg.append('g')
          .attr('transform', `translate(${margin.left}, ${height + margin.top + 80})`);

        const legendScale = d3.scaleLinear()
          .domain(colorScale.domain())
          .range([0, legendWidth]);

        const legendAxis = d3.axisBottom(legendScale)
          .ticks(5)
          .tickFormat(d => (d * 100).toFixed(0) + '%');

        // Create gradient for legend
        const defs = svg.append('defs');
        const gradient = defs.append('linearGradient')
          .attr('id', 'legend-gradient');

        gradient.selectAll('stop')
          .data(d3.range(0, 1.1, 0.1))
          .enter().append('stop')
          .attr('offset', d => (d * 100) + '%')
          .attr('stop-color', d => colorScale(d * colorScale.domain()[1]));

        legend.append('rect')
          .attr('width', legendWidth)
          .attr('height', legendHeight)
          .style('fill', 'url(#legend-gradient)');

        legend.append('g')
          .attr('transform', `translate(0, ${legendHeight})`)
          .call(legendAxis);

        legend.append('text')
          .attr('x', legendWidth / 2)
          .attr('y', -5)
          .attr('text-anchor', 'middle')
          .style('font-size', '11px')
          .text('Topic Proportion');

        setError(null);
      } catch (err) {
        setError('Failed to load heatmap data');
        console.error('Topic heatmap error:', err);
      }
    };

    drawHeatmap();
  }, [dataset]);

  if (error) {
    return (
      <Alert severity="info">
        {error}. Using simulated data for demonstration.
      </Alert>
    );
  }

  return (
    <Paper elevation={1} sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Cluster-Topic Heatmap - {dataset === 'high_rating' ? 'High Rating' : 'Most Commented'}
      </Typography>
      <Box ref={svgRef} />
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        Shows the proportion of each topic within each cluster. Darker colors indicate higher proportions.
      </Typography>
    </Paper>
  );
}