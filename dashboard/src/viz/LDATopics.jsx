import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Box, Typography, Paper, Alert, Grid, Card, CardContent } from '@mui/material';

export default function LDATopics({ dataset }) {
  const svgRef = useRef();
  const [error, setError] = useState(null);
  const [topicData, setTopicData] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        // Mock topic data - replace with actual data fetch
        const mockTopics = dataset === 'high_rating' ? [
          {
            topic: 0,
            prevalence: 9.8,
            words: ['料理', '美味しい', 'サービス', '雰囲気', '満足'],
            description: '料理の質・サービス'
          },
          {
            topic: 1,
            prevalence: 20.7,
            words: ['寿司', '新鮮', '大将', '技術', '職人'],
            description: '寿司・職人技'
          },
          {
            topic: 2,
            prevalence: 11.0,
            words: ['価格', '高い', 'コスパ', '値段', '安い'],
            description: '価格・価値'
          },
          {
            topic: 3,
            prevalence: 16.6,
            words: ['予約', '時間', '待ち', '訪問', '開店'],
            description: '予約・時間管理'
          },
          {
            topic: 4,
            prevalence: 8.1,
            words: ['ラーメン', 'スープ', '麺', '醤油', '味'],
            description: 'ラーメン関連'
          },
          {
            topic: 5,
            prevalence: 12.0,
            words: ['雰囲気', '店内', '内装', '音楽', '照明'],
            description: '雰囲気・空間'
          },
          {
            topic: 6,
            prevalence: 11.9,
            words: ['スタッフ', '接客', '対応', '笑顔', '親切'],
            description: 'スタッフ・サービス'
          },
          {
            topic: 7,
            prevalence: 9.9,
            words: ['立地', 'アクセス', '駅', '場所', '便利'],
            description: '立地・アクセス'
          }
        ] : [
          {
            topic: 0,
            prevalence: 11.2,
            words: ['高い', '料理', '残念', '評価', '期待'],
            description: '落胆・期待'
          },
          {
            topic: 1,
            prevalence: 19.9,
            words: ['時間', '遅い', '待ち', '開店', '到着'],
            description: '時間的課題'
          },
          {
            topic: 2,
            prevalence: 14.6,
            words: ['予約', '電話', 'コース', '料理', '訪問'],
            description: '予約・コース'
          },
          {
            topic: 3,
            prevalence: 13.6,
            words: ['東京', '料理', '美味しい', '評価', '人気'],
            description: '東京の人気店'
          },
          {
            topic: 4,
            prevalence: 9.6,
            words: ['人気', '予約', '訪問', '評価', '料理'],
            description: '人気・混雑店'
          },
          {
            topic: 5,
            prevalence: 12.0,
            words: ['寿司', '大将', '美味しい', '予約', '残念'],
            description: '寿司体験'
          },
          {
            topic: 6,
            prevalence: 10.4,
            words: ['ラーメン', '醤油', 'スープ', '評価', '平日'],
            description: 'ラーメン店レビュー'
          },
          {
            topic: 7,
            prevalence: 8.5,
            words: ['評価', '点数', '名店', '訪問', '料理'],
            description: '評価・有名店'
          }
        ];

        setTopicData(mockTopics);
        drawWordCloud(mockTopics);
        setError(null);
      } catch (err) {
        setError('Failed to load topic data');
        console.error('LDA topics error:', err);
      }
    };

    const drawWordCloud = (topics) => {
      // Clear previous chart
      d3.select(svgRef.current).selectAll('*').remove();

      // Create a simple bar chart showing topic prevalence
      const margin = { top: 20, right: 30, bottom: 40, left: 100 };
      const width = 600 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      const svg = d3.select(svgRef.current)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // Scales
      const yScale = d3.scaleBand()
        .domain(topics.map(d => `トピック ${d.topic}`))
        .range([0, height])
        .padding(0.1);

      const xScale = d3.scaleLinear()
        .domain([0, d3.max(topics, d => d.prevalence)])
        .nice()
        .range([0, width]);

      // Color scale
      const colorScale = d3.scaleOrdinal()
        .domain(topics.map(d => d.topic))
        .range(d3.schemeCategory10);

      // Add axes
      g.append('g')
        .call(d3.axisLeft(yScale));

      g.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale));

      // Add bars
      g.selectAll('.bar')
        .data(topics)
        .enter().append('rect')
        .attr('class', 'bar')
        .attr('y', d => yScale(`トピック ${d.topic}`))
        .attr('height', yScale.bandwidth())
        .attr('x', 0)
        .attr('width', d => xScale(d.prevalence))
        .attr('fill', d => colorScale(d.topic))
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

          tooltip.html(`${d.description}<br/>出現率: ${d.prevalence}%<br/>単語: ${d.words.join(', ')}`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
        })
        .on('mouseout', function() {
          d3.select(this).attr('opacity', 0.8);
          d3.selectAll('.tooltip').remove();
        });

      // Add percentage labels
      g.selectAll('.label')
        .data(topics)
        .enter().append('text')
        .attr('class', 'label')
        .attr('y', d => yScale(`トピック ${d.topic}`) + yScale.bandwidth() / 2)
        .attr('x', d => xScale(d.prevalence) + 5)
        .attr('dy', '0.35em')
        .style('font-size', '11px')
        .style('fill', '#333')
        .text(d => `${d.prevalence}%`);
    };

    loadData();
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
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          トピック出現率 - {dataset === 'high_rating' ? '高評価' : '最多コメント'}
        </Typography>
        <Box ref={svgRef} />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          バーにカーソルを合わせるとトピックの詳細と上位単語が表示されます。
        </Typography>
      </Paper>

      <Grid container spacing={2}>
        {topicData.map((topic) => (
          <Grid item xs={12} md={6} key={topic.topic}>
            <Card elevation={1} sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" color="primary" gutterBottom>
                  トピック {topic.topic}: {topic.description}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  出現率: {topic.prevalence}%
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {topic.words.map((word, idx) => (
                    <Box
                      key={idx}
                      sx={{
                        background: '#e3f2fd',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontSize: '12px',
                        color: '#1976d2'
                      }}
                    >
                      {word}
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}