import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert, Grid } from '@mui/material';

export default function SentimentAnalysis({ dataset }) {
  const pieRef = useRef();
  const barRef = useRef();
  const [error, setError] = useState(null);

  useEffect(() => {
    const drawCharts = async () => {
      try {
        // Mock sentiment data
        const sentimentData = dataset === 'high_rating' ? {
          overall: { positive: 0.78, negative: 0.22 },
          byCluster: [
            { cluster: 0, positive: 0.85, negative: 0.15 },
            { cluster: 1, positive: 0.92, negative: 0.08 },
            { cluster: 2, positive: 0.65, negative: 0.35 },
            { cluster: 3, positive: 0.88, negative: 0.12 },
            { cluster: 4, positive: 0.95, negative: 0.05 },
            { cluster: 5, positive: 0.82, negative: 0.18 },
            { cluster: 6, positive: 0.90, negative: 0.10 },
            { cluster: 7, positive: 0.75, negative: 0.25 }
          ]
        } : {
          overall: { positive: 0.62, negative: 0.38 },
          byCluster: [
            { cluster: 0, positive: 0.55, negative: 0.45 },
            { cluster: 1, positive: 0.48, negative: 0.52 },
            { cluster: 2, positive: 0.70, negative: 0.30 },
            { cluster: 3, positive: 0.75, negative: 0.25 },
            { cluster: 4, positive: 0.68, negative: 0.32 },
            { cluster: 5, positive: 0.80, negative: 0.20 },
            { cluster: 6, positive: 0.85, negative: 0.15 },
            { cluster: 7, positive: 0.72, negative: 0.28 },
            { cluster: 8, positive: 0.60, negative: 0.40 }
          ]
        };

        drawPieChart(sentimentData.overall);
        drawBarChart(sentimentData.byCluster);
        setError(null);
      } catch (err) {
        setError('Failed to load sentiment data');
        console.error('Sentiment analysis error:', err);
      }
    };

    const drawPieChart = (overallData) => {
      // Clear previous chart
      d3.select(pieRef.current).selectAll('*').remove();

      const width = 300;
      const height = 300;
      const radius = Math.min(width, height) / 2;

      const svg = d3.select(pieRef.current)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      const g = svg.append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

      const color = d3.scaleOrdinal()
        .domain(['positive', 'negative'])
        .range(['#4caf50', '#f44336']);

      const pie = d3.pie()
        .value(d => d.value);

      const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

      const data = [
        { label: 'ポジティブ', value: overallData.positive },
        { label: 'ネガティブ', value: overallData.negative }
      ];

      const arcs = g.selectAll('.arc')
        .data(pie(data))
        .enter().append('g')
        .attr('class', 'arc');

      arcs.append('path')
        .attr('d', arc)
        .attr('fill', d => color(d.data.label.toLowerCase()))
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

          tooltip.html(`${d.data.label}: ${(d.data.value * 100).toFixed(1)}%`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
        })
        .on('mouseout', function() {
          d3.selectAll('.tooltip').remove();
        });

      arcs.append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('font-weight', 'bold')
        .style('fill', 'white')
        .text(d => `${(d.data.value * 100).toFixed(1)}%`);
    };

    const drawBarChart = (clusterData) => {
      // Clear previous chart
      d3.select(barRef.current).selectAll('*').remove();

      const margin = { top: 20, right: 30, bottom: 40, left: 60 };
      const width = 500 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;

      const svg = d3.select(barRef.current)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // Scales
      const xScale = d3.scaleBand()
        .domain(clusterData.map(d => d.cluster))
        .range([0, width])
        .padding(0.1);

      const yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);

      // Add axes
      g.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => `C${d}`));

      g.append('g')
        .call(d3.axisLeft(yScale).tickFormat(d3.format('.0%')));

      // Add axis labels
      g.append('text')
        .attr('transform', `translate(${width / 2}, ${height + 35})`)
        .style('text-anchor', 'middle')
        .style('font-size', '12px')
        .text('クラスタ');

      g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .style('font-size', '12px')
        .text('ポジティブ感情比率');

      // Add bars
      g.selectAll('.bar')
        .data(clusterData)
        .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.cluster))
        .attr('width', xScale.bandwidth())
        .attr('y', d => yScale(d.positive))
        .attr('height', d => height - yScale(d.positive))
        .attr('fill', d => d.positive > 0.7 ? '#4caf50' : d.positive > 0.5 ? '#ff9800' : '#f44336')
        .attr('opacity', 0.8)
        .on('mouseover', function(event, d) {
          d3.select(this).attr('opacity', 1);
          
          const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('position', 'absolute')
            .style('background', 'rgba(0, 0, 0, 0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('font-size', '12px')
            .style('pointer-events', 'none');

          tooltip.html(`クラスタ ${d.cluster}<br/>ポジティブ: ${(d.positive * 100).toFixed(1)}%<br/>ネガティブ: ${(d.negative * 100).toFixed(1)}%`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
        })
        .on('mouseout', function() {
          d3.select(this).attr('opacity', 0.8);
          d3.selectAll('.tooltip').remove();
        });

      // Add percentage labels on bars
      g.selectAll('.label')
        .data(clusterData)
        .enter().append('text')
        .attr('class', 'label')
        .attr('x', d => xScale(d.cluster) + xScale.bandwidth() / 2)
        .attr('y', d => yScale(d.positive) - 5)
        .attr('text-anchor', 'middle')
        .style('font-size', '10px')
        .style('fill', '#333')
        .text(d => `${(d.positive * 100).toFixed(0)}%`);
    };

    drawCharts();
  }, [dataset]);

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
        <Grid item xs={12} md={6}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              全体感情分布
            </Typography>
            <Box ref={pieRef} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {dataset === 'high_rating' ? '高評価' : '最多コメント'}レビューの感情内訳
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              クラスタ別感情
            </Typography>
            <Box ref={barRef} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              各クラスタごとのポジティブ感情比率
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}