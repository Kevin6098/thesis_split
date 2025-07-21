import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert, Grid } from '@mui/material';

export default function CrossDatasetAnalysis() {
  const scatterRef = useRef();
  const lineRef = useRef();
  const [error, setError] = useState(null);

  useEffect(() => {
    const drawAnalysis = async () => {
      try {
        // Mock cross-dataset analysis data
        const scatterData = [
          { topic: 0, high_rating_prevalence: 9.8, most_commented_prevalence: 11.2, label: 'Food Quality', avg_sentiment_hr: 0.85, avg_sentiment_mc: 0.55 },
          { topic: 1, high_rating_prevalence: 20.7, most_commented_prevalence: 19.9, label: 'Service', avg_sentiment_hr: 0.92, avg_sentiment_mc: 0.48 },
          { topic: 2, high_rating_prevalence: 11.0, most_commented_prevalence: 14.6, label: 'Pricing', avg_sentiment_hr: 0.65, avg_sentiment_mc: 0.30 },
          { topic: 3, high_rating_prevalence: 16.6, most_commented_prevalence: 13.6, label: 'Booking', avg_sentiment_hr: 0.88, avg_sentiment_mc: 0.70 },
          { topic: 4, high_rating_prevalence: 8.1, most_commented_prevalence: 9.6, label: 'Cuisine', avg_sentiment_hr: 0.95, avg_sentiment_mc: 0.68 },
          { topic: 5, high_rating_prevalence: 12.0, most_commented_prevalence: 12.0, label: 'Atmosphere', avg_sentiment_hr: 0.82, avg_sentiment_mc: 0.80 },
          { topic: 6, high_rating_prevalence: 11.9, most_commented_prevalence: 10.4, label: 'Staff', avg_sentiment_hr: 0.90, avg_sentiment_mc: 0.85 },
          { topic: 7, high_rating_prevalence: 9.9, most_commented_prevalence: 8.5, label: 'Location', avg_sentiment_hr: 0.75, avg_sentiment_mc: 0.72 }
        ];

        const timelineData = [
          { dataset: 'High Rating', overall_sentiment: 0.78, engagement_topics: ['Service', 'Food Quality', 'Booking'] },
          { dataset: 'Most Commented', overall_sentiment: 0.62, engagement_topics: ['Pricing', 'Service', 'Food Quality'] }
        ];

        drawScatterPlot(scatterData);
        drawSentimentComparison(timelineData);
        setError(null);
      } catch (err) {
        setError('Failed to load cross-dataset analysis data');
        console.error('Cross-dataset analysis error:', err);
      }
    };

    const drawScatterPlot = (data) => {
      // Clear previous chart
      d3.select(scatterRef.current).selectAll('*').remove();

      const margin = { top: 20, right: 60, bottom: 60, left: 60 };
      const width = 500 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      const svg = d3.select(scatterRef.current)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // Scales
      const xScale = d3.scaleLinear()
        .domain(d3.extent(data, d => d.high_rating_prevalence))
        .nice()
        .range([0, width]);

      const yScale = d3.scaleLinear()
        .domain(d3.extent(data, d => d.most_commented_prevalence))
        .nice()
        .range([height, 0]);

      const colorScale = d3.scaleLinear()
        .domain([0, 1])
        .range(['#f44336', '#4caf50']);

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
        .text('High-Rating Prevalence (%)');

      g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .style('font-size', '12px')
        .text('Most-Commented Prevalence (%)');

      // Add diagonal reference line
      const diagonal = d3.line()
        .x(d => xScale(d))
        .y(d => yScale(d));

      const minVal = Math.min(xScale.domain()[0], yScale.domain()[0]);
      const maxVal = Math.max(xScale.domain()[1], yScale.domain()[1]);

      g.append('path')
        .datum([minVal, maxVal])
        .attr('d', diagonal)
        .attr('stroke', '#ccc')
        .attr('stroke-dasharray', '3,3')
        .attr('stroke-width', 1);

      // Add circles
      g.selectAll('.circle')
        .data(data)
        .enter().append('circle')
        .attr('class', 'circle')
        .attr('cx', d => xScale(d.high_rating_prevalence))
        .attr('cy', d => yScale(d.most_commented_prevalence))
        .attr('r', 8)
        .attr('fill', d => colorScale((d.avg_sentiment_hr + d.avg_sentiment_mc) / 2))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
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

          tooltip.html(`${d.label}<br/>HR: ${d.high_rating_prevalence}%<br/>MC: ${d.most_commented_prevalence}%<br/>Avg Sentiment: ${((d.avg_sentiment_hr + d.avg_sentiment_mc) / 2 * 100).toFixed(1)}%`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
        })
        .on('mouseout', function() {
          d3.selectAll('.tooltip').remove();
        });

      // Add labels
      g.selectAll('.label')
        .data(data)
        .enter().append('text')
        .attr('class', 'label')
        .attr('x', d => xScale(d.high_rating_prevalence))
        .attr('y', d => yScale(d.most_commented_prevalence) - 12)
        .attr('text-anchor', 'middle')
        .style('font-size', '10px')
        .style('fill', '#333')
        .style('font-weight', 'bold')
        .text(d => d.label);
    };

    const drawSentimentComparison = (data) => {
      // Clear previous chart
      d3.select(lineRef.current).selectAll('*').remove();

      const margin = { top: 20, right: 30, bottom: 60, left: 60 };
      const width = 400 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;

      const svg = d3.select(lineRef.current)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // Scales
      const xScale = d3.scaleBand()
        .domain(data.map(d => d.dataset))
        .range([0, width])
        .padding(0.1);

      const yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);

      // Add axes
      g.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale));

      g.append('g')
        .call(d3.axisLeft(yScale).tickFormat(d3.format('.0%')));

      // Add axis labels
      g.append('text')
        .attr('transform', `translate(${width / 2}, ${height + 50})`)
        .style('text-anchor', 'middle')
        .style('font-size', '12px')
        .text('Dataset');

      g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .style('font-size', '12px')
        .text('Overall Sentiment');

      // Add bars
      g.selectAll('.bar')
        .data(data)
        .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.dataset))
        .attr('width', xScale.bandwidth())
        .attr('y', d => yScale(d.overall_sentiment))
        .attr('height', d => height - yScale(d.overall_sentiment))
        .attr('fill', d => d.dataset === 'High Rating' ? '#1976d2' : '#dc004e')
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

          tooltip.html(`${d.dataset}<br/>Sentiment: ${(d.overall_sentiment * 100).toFixed(1)}%<br/>Top Topics: ${d.engagement_topics.join(', ')}`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
        })
        .on('mouseout', function() {
          d3.selectAll('.tooltip').remove();
        });

      // Add percentage labels
      g.selectAll('.label')
        .data(data)
        .enter().append('text')
        .attr('class', 'label')
        .attr('x', d => xScale(d.dataset) + xScale.bandwidth() / 2)
        .attr('y', d => yScale(d.overall_sentiment) - 5)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#333')
        .style('font-weight', 'bold')
        .text(d => `${(d.overall_sentiment * 100).toFixed(1)}%`);
    };

    drawAnalysis();
  }, []);

  if (error) {
    return (
      <Alert severity="info">
        {error}. Using simulated data for demonstration.
      </Alert>
    );
  }

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Topic Prevalence Correlation
            </Typography>
            <Box ref={scatterRef} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Each point represents a topic. Position shows prevalence in each dataset, 
              color indicates average sentiment. Points above the diagonal line are more 
              prevalent in most-commented reviews.
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Overall Sentiment Comparison
            </Typography>
            <Box ref={lineRef} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Comparison of overall sentiment between the two datasets. 
              Hover for engagement topic details.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}