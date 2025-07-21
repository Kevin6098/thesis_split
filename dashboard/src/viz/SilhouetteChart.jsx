import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert } from '@mui/material';

export default function SilhouetteChart({ dataset }) {
  const svgRef = useRef();
  const [error, setError] = useState(null);

  useEffect(() => {
    const drawChart = async () => {
      try {
        // Mock data for demonstration - replace with actual data fetch
        const mockData = [
          { k: 2, silhouette: 0.41 },
          { k: 3, silhouette: 0.38 },
          { k: 4, silhouette: 0.35 },
          { k: 5, silhouette: 0.42 },
          { k: 6, silhouette: 0.45 },
          { k: 7, silhouette: 0.48 },
          { k: 8, silhouette: 0.52 },
          { k: 9, silhouette: 0.49 },
          { k: 10, silhouette: 0.46 },
          { k: 11, silhouette: 0.43 },
          { k: 12, silhouette: 0.40 }
        ];

        // Adjust data based on dataset
        const data = dataset === 'high_rating' ? mockData : 
          mockData.map(d => ({ ...d, silhouette: d.silhouette + (Math.random() - 0.5) * 0.1 }));

        // Clear previous chart
        d3.select(svgRef.current).selectAll('*').remove();

        // Set dimensions
        const margin = { top: 20, right: 40, bottom: 40, left: 50 };
        const width = 600 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        // Create SVG
        const svg = d3.select(svgRef.current)
          .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom);

        const g = svg.append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);

        // Scales
        const xScale = d3.scaleLinear()
          .domain(d3.extent(data, d => d.k))
          .range([0, width]);

        const yScale = d3.scaleLinear()
          .domain([0, d3.max(data, d => d.silhouette) * 1.1])
          .range([height, 0]);

        // Line generator
        const line = d3.line()
          .x(d => xScale(d.k))
          .y(d => yScale(d.silhouette))
          .curve(d3.curveMonotoneX);

        // Add axes
        g.append('g')
          .attr('transform', `translate(0,${height})`)
          .call(d3.axisBottom(xScale).tickFormat(d3.format('d')));

        g.append('g')
          .call(d3.axisLeft(yScale));

        // Add axis labels
        g.append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 0 - margin.left)
          .attr('x', 0 - (height / 2))
          .attr('dy', '1em')
          .style('text-anchor', 'middle')
          .text('Silhouette Score');

        g.append('text')
          .attr('transform', `translate(${width / 2}, ${height + margin.bottom})`)
          .style('text-anchor', 'middle')
          .text('Number of Clusters (k)');

        // Add line
        g.append('path')
          .datum(data)
          .attr('fill', 'none')
          .attr('stroke', '#1976d2')
          .attr('stroke-width', 2)
          .attr('d', line);

        // Add points
        g.selectAll('.dot')
          .data(data)
          .enter().append('circle')
          .attr('class', 'dot')
          .attr('cx', d => xScale(d.k))
          .attr('cy', d => yScale(d.silhouette))
          .attr('r', 4)
          .attr('fill', '#1976d2')
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

            tooltip.html(`k=${d.k}<br/>Silhouette: ${d.silhouette.toFixed(3)}`)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 10) + 'px');
          })
          .on('mouseout', function() {
            d3.selectAll('.tooltip').remove();
          });

        // Highlight optimal k
        const optimalK = data.reduce((max, d) => d.silhouette > max.silhouette ? d : max);
        g.append('circle')
          .attr('cx', xScale(optimalK.k))
          .attr('cy', yScale(optimalK.silhouette))
          .attr('r', 8)
          .attr('fill', 'none')
          .attr('stroke', '#dc004e')
          .attr('stroke-width', 2);

        g.append('text')
          .attr('x', xScale(optimalK.k))
          .attr('y', yScale(optimalK.silhouette) - 15)
          .attr('text-anchor', 'middle')
          .style('font-size', '12px')
          .style('fill', '#dc004e')
          .style('font-weight', 'bold')
          .text(`Optimal k=${optimalK.k}`);

        setError(null);
      } catch (err) {
        setError('Failed to load silhouette data');
        console.error('Silhouette chart error:', err);
      }
    };

    drawChart();
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
        Silhouette Analysis - {dataset === 'high_rating' ? 'High Rating' : 'Most Commented'}
      </Typography>
      <Box ref={svgRef} />
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        Higher silhouette scores indicate better-defined clusters. The optimal k is highlighted in red.
      </Typography>
    </Paper>
  );
}