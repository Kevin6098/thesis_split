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

export default function MostCommented() {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        Most-Commented Results
      </Typography>
      
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="most-commented analysis tabs">
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
              Silhouette analysis for most-commented reviews to determine the optimal clustering configuration.
            </Typography>
            <SilhouetteChart dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={1}>
            <Typography variant="h5" gutterBottom color="primary">
              Cluster Distribution
            </Typography>
            <Typography variant="body1" paragraph>
              Distribution of most-commented reviews across clusters, revealing engagement patterns 
              and discussion drivers.
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} lg={8}>
                <ClusterDistribution dataset="most_commented" />
              </Grid>
              <Grid item xs={12} lg={4}>
                <Card elevation={1} sx={{ bgcolor: '#f8f9fa', height: 'fit-content' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Engagement Insights
                    </Typography>
                    <Typography variant="body2">
                      Most-commented reviews often reflect controversial opinions, 
                      exceptional experiences, or detailed discussions about specific aspects.
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
              Topic analysis of most-commented reviews reveals what drives customer engagement and discussion.
            </Typography>
            <LDATopics dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={3}>
            <Typography variant="h5" gutterBottom color="primary">
              Cluster-Topic Relationship Heatmap
            </Typography>
            <Typography variant="body1" paragraph>
              Relationship between customer engagement clusters and discussion topics in most-commented reviews.
            </Typography>
            <TopicHeatmap dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={4}>
            <Typography variant="h5" gutterBottom color="primary">
              Sentiment Distribution
            </Typography>
            <Typography variant="body1" paragraph>
              Sentiment patterns in most-commented reviews, showing how engagement correlates with sentiment.
            </Typography>
            <SentimentAnalysis dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={5}>
            <Typography variant="h5" gutterBottom color="primary">
              Representative Quotes
            </Typography>
            <Typography variant="body1" paragraph>
              Sample reviews that exemplify the characteristics of each cluster in most-commented data.
            </Typography>
            <RepresentativeQuotes dataset="most_commented" />
          </TabPanel>
        </CardContent>
      </Card>
    </Box>
  );
}