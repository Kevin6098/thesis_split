import React from 'react';
import { Card, CardContent, Typography, Grid, Paper, Box } from '@mui/material';

export default function Introduction() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        はじめに
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom color="primary">
                研究概要
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                本ダッシュボードは、日本のレストランレビューを包括的に分析し、
                異なる評価カテゴリーにおける顧客の感情パターンとトピック分布を明らかにします。
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                本研究では、K-means クラスタリング、Latent Dirichlet Allocation（LDA）トピックモデリング、
                感情分析などの高度な自然言語処理技術を用いて、顧客フィードバックから有用な洞察を抽出します。
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                高評価レビューと最多コメントレビューの 2 つの主要データセットを分析し、
                顧客満足度の傾向とエンゲージメント行動を比較検討します。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, bgcolor: '#f8f9fa' }}>
            <Typography variant="h6" gutterBottom color="primary">
              主な機能
            </Typography>
            <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
              <li>インタラクティブなクラスタリングの可視化</li>
              <li>トピックモデリング分析</li>
              <li>感情分布パターン</li>
              <li>比較分析ツール</li>
              <li>検索・フィルタリング機能</li>
              <li>代表的レビュー引用の探索</li>
            </Box>
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3, mt: 2, bgcolor: '#f0f8ff' }}>
            <Typography variant="h6" gutterBottom color="primary">
              ナビゲーションガイド
            </Typography>
            <Typography variant="body2" sx={{ lineHeight: 1.6 }}>
              左側のナビゲーションドロワーを使用して、各分析セクションを閲覧してください。
              各セクションにはインタラクティブな可視化と詳細な洞察が含まれています。
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}