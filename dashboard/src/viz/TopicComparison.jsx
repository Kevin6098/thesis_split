import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert } from '@mui/material';

export default function TopicComparison() {
  const svgRef = useRef();
  const [error, setError] = useState(null);

  useEffect(() => {
    const drawComparison = async () => {
      try {
        // Mock comparative topic prevalence data
        const topicData = [
          { topic: 0, high_rating: 9.8, most_commented: 11.2, label: 'Food Quality' },
          { topic: 1, high_rating: 20.7, most_commented: 19.9, label: 'Service Experience' },
          { topic: 2, high_rating: 11.0, most_commented: 14.6, label: 'Pricing & Value' },
          { topic: 3, high_rating: 16.6, most_commented: 13.6, label: 'Booking & Timing' },
          { topic: 4, high_rating: 8.1, most_commented: 9.6, label: 'Specific Cuisine' },
          { topic: 5, high_rating: 12.0, most_commented: 12.0, label: 'Atmosphere' },
          { topic: 6, high_rating: 11.9, most_commented: 10.4, label: 'Staff Interaction' },
          { topic: 7, high_rating: 9.9, most_commented: 8.5, label: 'Location & Access' }
        ];

        // Clear previous chart
        d3.select(svgRef.current).selectAll('*').remove();

        // Set dimensions
        const margin = { top: 20, right: 80, bottom: 60, left: 120 };
        const width = 700 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const svg = d3.select(svgRef.current)
          .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom);

        const g = svg.append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);

        // Scales
        const yScale = d3.scaleBand()
          .domain(topicData.map(d => d.label))
          .range([0, height])
          .padding(0.2);

        const xScale = d3.scaleLinear()
          .domain([0, d3.max(topicData, d => Math.max(d.high_rating, d.most_commented))])
          .nice()
          .range([0, width]);

        // Add axes
        g.append('g')
          .attr('transform', `translate(0,${height})`)
          .call(d3.axisBottom(xScale));

        g.append('g')
          .call(d3.axisLeft(yScale));

        // Add axis labels
        g.append('text')
          .attr('transform', `translate(${width / 2}, ${height + 50})`)
          .style('text-anchor', 'middle')
          .style('font-size', '12px')
          .text('トピック出現率 (%)');

        // Add bars for high_rating
        g.selectAll('.bar-high')
          .data(topicData)
          .enter().append('rect')
          .attr('class', 'bar-high')
          .attr('y', d => yScale(d.label))
          .attr('height', yScale.bandwidth() / 2)
          .attr('x', 0)
          .attr('width', d => xScale(d.high_rating))
          .attr('fill', '#1976d2')
          .attr('opacity', 0.8)
          .on('mouseover', function(event, d) {
            const tooltip = d3.select('body').append('div')
              .attr('class', 'tooltip')
              .style('position', 'absolute')
              .style('background', 'rgba(0, 0, 0, 0.8)')
              .style('color', 'white')
              .style('padding', '8px')
              .style('border-radius', '4px')
              .style('font-size', '12px')
              .style('pointer-events', 'none');

            tooltip.html(`${d.label}<br/>高評価: ${d.high_rating}%`)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 10) + 'px');
          })
          .on('mouseout', function() {
            d3.selectAll('.tooltip').remove();
          });

        // Add bars for most_commented
        g.selectAll('.bar-most')
          .data(topicData)
          .enter().append('rect')
          .attr('class', 'bar-most')
          .attr('y', d => yScale(d.label) + yScale.bandwidth() / 2)
          .attr('height', yScale.bandwidth() / 2)
          .attr('x', 0)
          .attr('width', d => xScale(d.most_commented))
          .attr('fill', '#dc004e')
          .attr('opacity', 0.8)
          .on('mouseover', function(event, d) {
            const tooltip = d3.select('body').append('div')
              .attr('class', 'tooltip')
              .style('position', 'absolute')
              .style('background', 'rgba(0, 0, 0, 0.8)')
              .style('color', 'white')
              .style('padding', '8px')
              .style('border-radius', '4px')
              .style('font-size', '12px')
              .style('pointer-events', 'none');

            tooltip.html(`${d.label}<br/>最多コメント: ${d.most_commented}%`)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 10) + 'px');
          })
          .on('mouseout', function() {
            d3.selectAll('.tooltip').remove();
          });

        // Add value labels
        g.selectAll('.label-high')
          .data(topicData)
          .enter().append('text')
          .attr('class', 'label-high')
          .attr('x', d => xScale(d.high_rating) + 3)
          .attr('y', d => yScale(d.label) + yScale.bandwidth() / 4)
          .attr('dy', '0.35em')
          .style('font-size', '10px')
          .style('fill', '#1976d2')
          .text(d => `${d.high_rating}%`);

        g.selectAll('.label-most')
          .data(topicData)
          .enter().append('text')
          .attr('class', 'label-most')
          .attr('x', d => xScale(d.most_commented) + 3)
          .attr('y', d => yScale(d.label) + (3 * yScale.bandwidth()) / 4)
          .attr('dy', '0.35em')
          .style('font-size', '10px')
          .style('fill', '#dc004e')
          .text(d => `${d.most_commented}%`);

        // Add legend
        const legend = svg.append('g')
          .attr('transform', `translate(${width + margin.left + 10}, ${margin.top + 20})`);

        legend.append('rect')
          .attr('x', 0)
          .attr('y', 0)
          .attr('width', 15)
          .attr('height', 15)
          .attr('fill', '#1976d2')
          .attr('opacity', 0.8);

        legend.append('text')
          .attr('x', 20)
          .attr('y', 12)
          .style('font-size', '12px')
          .text('高評価');

        legend.append('rect')
          .attr('x', 0)
          .attr('y', 25)
          .attr('width', 15)
          .attr('height', 15)
          .attr('fill', '#dc004e')
          .attr('opacity', 0.8);

        legend.append('text')
          .attr('x', 20)
          .attr('y', 37)
          .style('font-size', '12px')
          .text('最多コメント');

        setError(null);
      } catch (err) {
        setError('Failed to load topic comparison data');
        console.error('Topic comparison error:', err);
      }
    };

    drawComparison();
  }, []);

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
        トピック出現率比較：高評価 vs 最多コメント
      </Typography>
      <Box ref={svgRef} />
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        トピック出現率の違いを比較分析しています。バーにカーソルを合わせると正確な割合が表示されます。
      </Typography>
    </Paper>
  );
}