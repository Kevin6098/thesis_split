import React from 'react';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import TopicComparison from '../viz/TopicComparison.jsx';
import CrossDatasetAnalysis from '../viz/CrossDatasetAnalysis.jsx';

export default function MixedTopics() {
  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        Mixed Topics Analysis
      </Typography>
      
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom color="primary">
                Cross-Dataset Topic Comparison
              </Typography>
              <Typography variant="body1" paragraph>
                Comparative analysis of topics discovered in high-rating versus most-commented reviews, 
                revealing differences in customer focus and discussion patterns.
              </Typography>
              <TopicComparison />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom color="primary">
                Integrated Analysis Dashboard
              </Typography>
              <Typography variant="body1" paragraph>
                Comprehensive view combining insights from both datasets to understand 
                the complete landscape of customer feedback patterns.
              </Typography>
              <CrossDatasetAnalysis />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ bgcolor: '#f8f9fa' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Key Findings
              </Typography>
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
                <li>High-rating reviews focus more on food quality and service</li>
                <li>Most-commented reviews discuss pricing and value more frequently</li>
                <li>Negative sentiment is more prevalent in most-commented reviews</li>
                <li>Certain topics appear consistently across both datasets</li>
                <li>Restaurant atmosphere is discussed differently in each dataset</li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ bgcolor: '#f0f8ff' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Business Implications
              </Typography>
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
                <li>Focus on food quality to achieve high ratings</li>
                <li>Address pricing concerns to reduce negative comments</li>
                <li>Monitor most-commented reviews for improvement areas</li>
                <li>Leverage high-rating review patterns for marketing</li>
                <li>Balance quality and value proposition effectively</li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}