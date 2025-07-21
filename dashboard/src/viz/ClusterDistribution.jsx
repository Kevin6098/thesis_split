import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert } from '@mui/material';

export default function ClusterDistribution({ dataset }) {
  const svgRef = useRef();
  const [error, setError] = useState(null);

  useEffect(() => {
    const drawChart = async () => {
      try {
        // Mock data for demonstration - replace with actual data fetch
        const mockData = dataset === 'high_rating' ? [
          { cluster: 0, count: 142, percentage: 9.8 },
          { cluster: 1, count: 298, percentage: 20.7 },
          { cluster: 2, count: 158, percentage: 11.0 },
          { cluster: 3, count: 239, percentage: 16.6 },
          { cluster: 4, count: 116, percentage: 8.1 },
          { cluster: 5, count: 173, percentage: 12.0 },
          { cluster: 6, count: 171, percentage: 11.9 },
          { cluster: 7, count: 142, percentage: 9.9 },
        ] : [
          { cluster: 0, count: 156, percentage: 11.2 },
          { cluster: 1, count: 278, percentage: 19.9 },
          { cluster: 2, count: 203, percentage: 14.6 },
          { cluster: 3, count: 189, percentage: 13.6 },
          { cluster: 4, count: 134, percentage: 9.6 },
          { cluster: 5, count: 167, percentage: 12.0 },
          { cluster: 6, count: 145, percentage: 10.4 },
          { cluster: 7, count: 119, percentage: 8.5 },
          { cluster: 8, count: 139, percentage: 10.0 },
        ];

        // Clear previous chart
        d3.select(svgRef.current).selectAll('*').remove();

        // Set dimensions
        const margin = { top: 20, right: 30, bottom: 60, left: 60 };
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
        const xScale = d3.scaleBand()
          .domain(mockData.map(d => d.cluster))
          .range([0, width])
          .padding(0.1);

        const yScale = d3.scaleLinear()
          .domain([0, d3.max(mockData, d => d.count)])
          .nice()
          .range([height, 0]);

        // Color scale
        const colorScale = d3.scaleOrdinal()
          .domain(mockData.map(d => d.cluster))
          .range(d3.schemeSet3);

        // Add axes
        g.append('g')
          .attr('transform', `translate(0,${height})`)
          .call(d3.axisBottom(xScale));

        g.append('g')
          .call(d3.axisLeft(yScale));

        // Add axis labels
        g.append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 0 - margin.left)
          .attr('x', 0 - (height / 2))
          .attr('dy', '1em')
          .style('text-anchor', 'middle')
          .text('Number of Reviews');

        g.append('text')
          .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 10})`)
          .style('text-anchor', 'middle')
          .text('Cluster ID');

        // Add bars
        g.selectAll('.bar')
          .data(mockData)
          .enter().append('rect')
          .attr('class', 'bar')
          .attr('x', d => xScale(d.cluster))
          .attr('width', xScale.bandwidth())
          .attr('y', d => yScale(d.count))
          .attr('height', d => height - yScale(d.count))
          .attr('fill', d => colorScale(d.cluster))
          .attr('stroke', '#fff')
          .attr('stroke-width', 1)
          .on('mouseover', function(event, d) {
            // Highlight bar
            d3.select(this).attr('opacity', 0.8);
            
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

            tooltip.html(`Cluster ${d.cluster}<br/>Count: ${d.count}<br/>Percentage: ${d.percentage}%`)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 10) + 'px');
          })
          .on('mouseout', function() {
            d3.select(this).attr('opacity', 1);
            d3.selectAll('.tooltip').remove();
          });

        // Add count labels on bars
        g.selectAll('.label')
          .data(mockData)
          .enter().append('text')
          .attr('class', 'label')
          .attr('x', d => xScale(d.cluster) + xScale.bandwidth() / 2)
          .attr('y', d => yScale(d.count) - 5)
          .attr('text-anchor', 'middle')
          .style('font-size', '11px')
          .style('fill', '#333')
          .text(d => d.count);

        setError(null);
      } catch (err) {
        setError('Failed to load cluster distribution data');
        console.error('Cluster distribution chart error:', err);
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
        Cluster Distribution - {dataset === 'high_rating' ? 'High Rating' : 'Most Commented'}
      </Typography>
      <Box ref={svgRef} />
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        Distribution of reviews across different clusters. Hover over bars for details.
      </Typography>
    </Paper>
  );
}