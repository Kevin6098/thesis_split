import React, { useState } from 'react';
import { Box, Typography, Tabs, Tab, Card, CardContent, Grid } from '@mui/material';
import SilhouetteChart from '../viz/SilhouetteChart.jsx';
import ClusterDistribution from '../viz/ClusterDistribution.jsx';
import LDATopics from '../viz/LDATopics.jsx';
import TopicHeatmap from '../viz/TopicHeatmap.jsx';
import SentimentAnalysis from '../viz/SentimentAnalysis.jsx';
import RepresentativeQuotes from '../viz/RepresentativeQuotes.jsx';

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function HighRating() {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        High-Rating Results
      </Typography>
      
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="high-rating analysis tabs">
              <Tab label="Silhouette Analysis" />
              <Tab label="Clustering Results" />
              <Tab label="LDA Topics" />
              <Tab label="Topic-Cluster Heatmap" />
              <Tab label="Sentiment Analysis" />
              <Tab label="Representative Quotes" />
            </Tabs>
          </Box>
          
          <TabPanel value={value} index={0}>
            <Typography variant="h5" gutterBottom color="primary">
              Silhouette Analysis for Optimal K
            </Typography>
            <Typography variant="body1" paragraph>
              Silhouette analysis helps determine the optimal number of clusters by measuring 
              how similar each point is to its own cluster compared to other clusters.
            </Typography>
            <SilhouetteChart dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={1}>
            <Typography variant="h5" gutterBottom color="primary">
              Cluster Distribution
            </Typography>
            <Typography variant="body1" paragraph>
              Distribution of reviews across different clusters, showing the relative size 
              and characteristics of each customer segment.
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} lg={8}>
                <ClusterDistribution dataset="high_rating" />
              </Grid>
              <Grid item xs={12} lg={4}>
                <Card elevation={1} sx={{ bgcolor: '#f8f9fa', height: 'fit-content' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Cluster Insights
                    </Typography>
                    <Typography variant="body2">
                      Each cluster represents a distinct pattern in customer feedback, 
                      helping identify different types of dining experiences and preferences.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={value} index={2}>
            <Typography variant="h5" gutterBottom color="primary">
              LDA Topic Analysis
            </Typography>
            <Typography variant="body1" paragraph>
              Latent Dirichlet Allocation reveals the underlying topics discussed in high-rating reviews.
            </Typography>
            <LDATopics dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={3}>
            <Typography variant="h5" gutterBottom color="primary">
              Cluster-Topic Relationship Heatmap
            </Typography>
            <Typography variant="body1" paragraph>
              This heatmap shows how different clusters align with discovered topics, 
              revealing the relationship between customer segments and discussion themes.
            </Typography>
            <TopicHeatmap dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={4}>
            <Typography variant="h5" gutterBottom color="primary">
              Sentiment Distribution
            </Typography>
            <Typography variant="body1" paragraph>
              Analysis of sentiment patterns across clusters and topics in high-rating reviews.
            </Typography>
            <SentimentAnalysis dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={5}>
            <Typography variant="h5" gutterBottom color="primary">
              Representative Quotes
            </Typography>
            <Typography variant="body1" paragraph>
              Sample reviews that best represent each cluster's characteristics and themes.
            </Typography>
            <RepresentativeQuotes dataset="high_rating" />
          </TabPanel>
        </CardContent>
      </Card>
    </Box>
  );
}