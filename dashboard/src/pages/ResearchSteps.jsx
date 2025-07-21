import React from 'react';
import { 
  Card, CardContent, Typography, Grid, Box, Stepper, Step, 
  StepLabel, StepContent, Paper, Chip 
} from '@mui/material';

const steps = [
  {
    label: 'Data Collection & Preprocessing',
    description: 'Collected Japanese restaurant reviews from high-rating and most-commented categories',
    details: [
      'Raw data extraction from review platforms',
      'Text cleaning and normalization',
      'Japanese text preprocessing',
      'Stop word removal and tokenization'
    ],
    techniques: ['Text Cleaning', 'Tokenization', 'Normalization']
  },
  {
    label: 'Feature Engineering',
    description: 'Converted text data into numerical representations for machine learning',
    details: [
      'TF-IDF vectorization',
      'N-gram feature extraction',
      'Dimensionality consideration',
      'Feature selection optimization'
    ],
    techniques: ['TF-IDF', 'Vectorization', 'N-grams']
  },
  {
    label: 'K-means Clustering',
    description: 'Applied unsupervised clustering to group similar reviews',
    details: [
      'Optimal cluster number determination using silhouette analysis',
      'K-means algorithm implementation',
      'Cluster validation and interpretation',
      'Representative sample extraction'
    ],
    techniques: ['K-means', 'Silhouette Analysis', 'Cluster Validation']
  },
  {
    label: 'Topic Modeling (LDA)',
    description: 'Discovered latent topics using Latent Dirichlet Allocation',
    details: [
      'LDA model training and optimization',
      'Topic coherence evaluation',
      'Topic-document probability distribution',
      'Topic labeling and interpretation'
    ],
    techniques: ['LDA', 'Topic Modeling', 'Probabilistic Analysis']
  },
  {
    label: 'Sentiment Analysis',
    description: 'Analyzed sentiment patterns using rule-based approaches',
    details: [
      'Japanese negative keyword identification',
      'Rule-based sentiment classification',
      'Sentiment score computation',
      'Sentiment distribution analysis'
    ],
    techniques: ['Rule-based Classification', 'Sentiment Scoring']
  },
  {
    label: 'Visualization & Analysis',
    description: 'Created interactive visualizations and comprehensive analysis',
    details: [
      'Cluster distribution visualization',
      'Topic prevalence analysis',
      'Heatmap generation for cluster-topic relationships',
      'Interactive dashboard development'
    ],
    techniques: ['Data Visualization', 'Interactive Charts', 'Statistical Analysis']
  }
];

export default function ResearchSteps() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        Research Methodology
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Stepper orientation="vertical">
                {steps.map((step, index) => (
                  <Step key={step.label} active={true}>
                    <StepLabel>
                      <Typography variant="h6" color="primary">
                        {step.label}
                      </Typography>
                    </StepLabel>
                    <StepContent>
                      <Typography variant="body1" paragraph sx={{ mb: 2 }}>
                        {step.description}
                      </Typography>
                      <Box component="ul" sx={{ pl: 2, mb: 2 }}>
                        {step.details.map((detail, idx) => (
                          <li key={idx}>
                            <Typography variant="body2" sx={{ mb: 0.5 }}>
                              {detail}
                            </Typography>
                          </li>
                        ))}
                      </Box>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {step.techniques.map((technique) => (
                          <Chip 
                            key={technique} 
                            label={technique} 
                            size="small" 
                            color="primary" 
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, bgcolor: '#f8f9fa' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Research Objectives
            </Typography>
            <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
              <li>Identify patterns in customer feedback</li>
              <li>Compare high-rating vs most-commented reviews</li>
              <li>Extract meaningful topics from reviews</li>
              <li>Analyze sentiment distributions</li>
              <li>Provide actionable insights for restaurants</li>
            </Box>
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3, mt: 2, bgcolor: '#f0f8ff' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Technical Stack
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Chip label="Python" size="small" />
              <Chip label="Scikit-learn" size="small" />
              <Chip label="Pandas" size="small" />
              <Chip label="React + D3.js" size="small" />
              <Chip label="Material-UI" size="small" />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}