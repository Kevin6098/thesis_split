import React from 'react';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import TopicComparison from '../viz/TopicComparison.jsx';
import CrossDatasetAnalysis from '../viz/CrossDatasetAnalysis.jsx';

export default function MixedTopics() {
  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        複合トピック分析
      </Typography>
      
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom color="primary">
                データセット横断トピック比較
              </Typography>
              <Typography variant="body1" paragraph>
                高評価レビューと最多コメントレビューで抽出されたトピックを比較分析し、顧客の関心領域と議論パターンの違いを明らかにします。
              </Typography>
              <TopicComparison />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom color="primary">
                統合分析ダッシュボード
              </Typography>
              <Typography variant="body1" paragraph>
                両データセットの洞察を組み合わせ、顧客フィードバックパターンの全体像を把握する包括的ビューです。
              </Typography>
              <CrossDatasetAnalysis />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ bgcolor: '#f8f9fa' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                主な発見
              </Typography>
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
                <li>高評価レビューは料理の質とサービスにより重点を置く</li>
                <li>最多コメントレビューは価格と価値についてより頻繁に議論する</li>
                <li>否定的感情は最多コメントレビューでより顕著である</li>
                <li>特定のトピックは両データセットで一貫して現れる</li>
                <li>レストランの雰囲気は各データセットで異なる形で議論される</li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ bgcolor: '#f0f8ff' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                ビジネスへの示唆
              </Typography>
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
                <li>高評価を得るために料理の質に重点を置く</li>
                <li>価格に関する懸念に対応して否定的コメントを減らす</li>
                <li>改善点を把握するため最多コメントレビューを監視する</li>
                <li>高評価レビューのパターンをマーケティングに活用する</li>
                <li>質と価値提案のバランスを効果的に取る</li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}