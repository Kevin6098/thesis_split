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
        最多コメントレビュー結果
      </Typography>
      
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="最多コメントレビュー分析タブ">
              <Tab label="シルエット分析" />
              <Tab label="クラスタリング結果" />
              <Tab label="LDAトピック" />
              <Tab label="トピック-クラスタヒートマップ" />
              <Tab label="感情分析" />
              <Tab label="代表的なレビュー" />
            </Tabs>
          </Box>
          
          <TabPanel value={value} index={0}>
            <Typography variant="h5" gutterBottom color="primary">
              最適クラスタ数のシルエット分析
            </Typography>
            <Typography variant="body1" paragraph>
              最多コメントレビューに対するシルエット分析で、最適なクラスタ設定を決定します。
            </Typography>
            <SilhouetteChart dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={1}>
            <Typography variant="h5" gutterBottom color="primary">
              クラスタ分布
            </Typography>
            <Typography variant="body1" paragraph>
              最多コメントレビューをクラスタごとに分布させ、エンゲージメントのパターンと議論の要因を明らかにします。
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} lg={8}>
                <ClusterDistribution dataset="most_commented" />
              </Grid>
              <Grid item xs={12} lg={4}>
                <Card elevation={1} sx={{ bgcolor: '#f8f9fa', height: 'fit-content' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      エンゲージメントの洞察
                    </Typography>
                    <Typography variant="body2">
                      最多コメントレビューは、多くの場合、賛否両論の意見、卓越した体験、または特定の側面についての詳細な議論を反映しています。
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={value} index={2}>
            <Typography variant="h5" gutterBottom color="primary">
              LDAトピック分析
            </Typography>
            <Typography variant="body1" paragraph>
              最多コメントレビューのトピック分析により、顧客のエンゲージメントと議論を促進する要因が明らかになります。
            </Typography>
            <LDATopics dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={3}>
            <Typography variant="h5" gutterBottom color="primary">
              クラスタ-トピック関係ヒートマップ
            </Typography>
            <Typography variant="body1" paragraph>
              最多コメントレビューにおける顧客エンゲージメントクラスタと議論トピックの関係を示します。
            </Typography>
            <TopicHeatmap dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={4}>
            <Typography variant="h5" gutterBottom color="primary">
              感情分布
            </Typography>
            <Typography variant="body1" paragraph>
              最多コメントレビューにおける感情パターンを分析し、エンゲージメントと感情の相関を示します。
            </Typography>
            <SentimentAnalysis dataset="most_commented" />
          </TabPanel>
          
          <TabPanel value={value} index={5}>
            <Typography variant="h5" gutterBottom color="primary">
              代表的なレビュー引用
            </Typography>
            <Typography variant="body1" paragraph>
              最多コメントデータにおける各クラスタの特徴を示すサンプルレビューを紹介します。
            </Typography>
            <RepresentativeQuotes dataset="most_commented" />
          </TabPanel>
        </CardContent>
      </Card>
    </Box>
  );
}