import React from 'react';
import { Card, CardContent, Typography, Grid, Paper, Box } from '@mui/material';

export default function Introduction() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        Introduction
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom color="primary">
                Research Overview
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                This dashboard presents a comprehensive analysis of Japanese restaurant reviews, 
                focusing on understanding customer sentiment patterns and topic distributions 
                across different rating categories.
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                The study employs advanced natural language processing techniques including 
                K-means clustering, Latent Dirichlet Allocation (LDA) topic modeling, and 
                sentiment analysis to extract meaningful insights from customer feedback.
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                Two primary datasets are analyzed: high-rating reviews and most-commented reviews, 
                allowing for comparative analysis of customer satisfaction patterns and 
                engagement behaviors.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, bgcolor: '#f8f9fa' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Key Features
            </Typography>
            <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
              <li>Interactive clustering visualization</li>
              <li>Topic modeling analysis</li>
              <li>Sentiment distribution patterns</li>
              <li>Comparative analysis tools</li>
              <li>Search and filtering capabilities</li>
              <li>Representative quote exploration</li>
            </Box>
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3, mt: 2, bgcolor: '#f0f8ff' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Navigation Guide
            </Typography>
            <Typography variant="body2" sx={{ lineHeight: 1.6 }}>
              Use the navigation drawer on the left to explore different sections of the analysis. 
              Each section contains interactive visualizations and detailed insights.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}