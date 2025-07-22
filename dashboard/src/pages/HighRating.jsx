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
        高評価レビュー結果
      </Typography>
      
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="高評価レビュー分析タブ">
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
              シルエット分析は、各データポイントが所属するクラスタと
              他クラスタとの類似度を比較することで、最適なクラスタ数を決定するのに役立ちます。
            </Typography>
            <SilhouetteChart dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={1}>
            <Typography variant="h5" gutterBottom color="primary">
              クラスタ分布
            </Typography>
            <Typography variant="body1" paragraph>
              各クラスタに属するレビュー数と、その特徴を可視化し、
              顧客セグメントの規模と特性を示します。
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} lg={8}>
                <ClusterDistribution dataset="high_rating" />
              </Grid>
              <Grid item xs={12} lg={4}>
                <Card elevation={1} sx={{ bgcolor: '#f8f9fa', height: 'fit-content' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      クラスタの洞察
                    </Typography>
                    <Typography variant="body2">
                      各クラスタは顧客フィードバックの独自パターンを表し、
                      多様な食事体験や嗜好を把握するのに役立ちます。
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
              Latent Dirichlet Allocation により、高評価レビューに潜む
              主要トピックを抽出します。
            </Typography>
            <LDATopics dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={3}>
            <Typography variant="h5" gutterBottom color="primary">
              クラスタ-トピック関係ヒートマップ
            </Typography>
            <Typography variant="body1" paragraph>
              各クラスタがどのトピックと関連しているかを示し、
              顧客セグメントと議論テーマの関係性を明らかにします。
            </Typography>
            <TopicHeatmap dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={4}>
            <Typography variant="h5" gutterBottom color="primary">
              感情分布
            </Typography>
            <Typography variant="body1" paragraph>
              高評価レビュー内のクラスタおよびトピックごとの
              感情パターンを分析します。
            </Typography>
            <SentimentAnalysis dataset="high_rating" />
          </TabPanel>
          
          <TabPanel value={value} index={5}>
            <Typography variant="h5" gutterBottom color="primary">
              代表的なレビュー引用
            </Typography>
            <Typography variant="body1" paragraph>
              各クラスタの特徴とテーマを最もよく表すサンプルレビューを紹介します。
            </Typography>
            <RepresentativeQuotes dataset="high_rating" />
          </TabPanel>
        </CardContent>
      </Card>
    </Box>
  );
}