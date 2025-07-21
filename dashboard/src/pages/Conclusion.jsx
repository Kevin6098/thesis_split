import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Paper, Divider } from '@mui/material';

export default function Conclusion() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        Conclusion
      </Typography>
      
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom color="primary">
                Research Summary
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                This comprehensive analysis of Japanese restaurant reviews has revealed significant 
                insights into customer feedback patterns, sentiment distributions, and topic preferences 
                across different engagement categories. Through the application of advanced NLP techniques 
                including K-means clustering, LDA topic modeling, and sentiment analysis, we have 
                successfully identified distinct customer segments and their characteristic concerns.
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                The comparative analysis between high-rating and most-commented reviews demonstrates 
                clear differences in customer focus areas, with high-rating reviews emphasizing 
                food quality and service excellence, while most-commented reviews often center 
                around value proposition and pricing concerns.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Key Contributions
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1.5 } }}>
                <li>
                  <strong>Methodological Framework:</strong> Developed a comprehensive approach 
                  for analyzing Japanese restaurant reviews using clustering and topic modeling
                </li>
                <li>
                  <strong>Comparative Insights:</strong> Identified distinct patterns between 
                  high-rating and most-commented review categories
                </li>
                <li>
                  <strong>Interactive Dashboard:</strong> Created a user-friendly visualization 
                  platform for exploring complex analysis results
                </li>
                <li>
                  <strong>Practical Applications:</strong> Provided actionable insights for 
                  restaurant management and customer experience improvement
                </li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Technical Achievements
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1.5 } }}>
                <li>
                  <strong>Clustering Optimization:</strong> Successfully determined optimal 
                  cluster numbers using silhouette analysis
                </li>
                <li>
                  <strong>Topic Discovery:</strong> Extracted meaningful topics from Japanese 
                  text using LDA modeling
                </li>
                <li>
                  <strong>Sentiment Classification:</strong> Implemented rule-based sentiment 
                  analysis tailored for Japanese restaurant reviews
                </li>
                <li>
                  <strong>Visualization Innovation:</strong> Developed interactive D3.js 
                  visualizations for complex data exploration
                </li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 3, bgcolor: '#f8f9fa' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Business Impact & Recommendations
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  For Restaurant Owners
                </Typography>
                <Box component="ul" sx={{ pl: 2, fontSize: '0.9rem' }}>
                  <li>Monitor cluster patterns to understand customer segments</li>
                  <li>Focus on food quality and service to achieve high ratings</li>
                  <li>Address pricing concerns highlighted in most-commented reviews</li>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  For Platform Developers
                </Typography>
                <Box component="ul" sx={{ pl: 2, fontSize: '0.9rem' }}>
                  <li>Implement topic-based review categorization</li>
                  <li>Provide sentiment-aware recommendation systems</li>
                  <li>Enable cluster-based user segmentation</li>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  For Researchers
                </Typography>
                <Box component="ul" sx={{ pl: 2, fontSize: '0.9rem' }}>
                  <li>Extend analysis to other languages and domains</li>
                  <li>Explore temporal patterns in review data</li>
                  <li>Investigate deeper sentiment analysis techniques</li>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        
        <Grid item xs={12}>
          <Card elevation={2} sx={{ bgcolor: '#e3f2fd' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                Future Research Directions
              </Typography>
              <Typography variant="body1" paragraph>
                This research opens several avenues for future investigation, including 
                temporal analysis of review patterns, integration of additional data sources 
                such as restaurant metadata and customer demographics, and the application 
                of advanced deep learning techniques for more nuanced sentiment and topic analysis.
              </Typography>
              <Typography variant="body1">
                The interactive dashboard framework developed in this study can serve as a 
                foundation for real-time review monitoring systems and could be extended to 
                support predictive analytics for restaurant performance forecasting.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}