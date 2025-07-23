import React from 'react';
import { 
  Card, CardContent, Typography, Grid, Box, Stepper, Step, 
  StepLabel, StepContent, Paper, Chip 
} from '@mui/material';

const steps = [
  {
    label: '1. データ収集と前処理',
    description: '高評価・最多コメントの日本語レビューを収集し、機械学習向けに整形',
    details: [
      'プラットフォームからレビュー抽出',
      'テキストの正規化・トークン化',
      'ストップワード除去・形態素解析'
    ],
    techniques: ['Text Cleaning', 'Tokenization', 'Normalization']
  },
  {
    label: '2. 特徴量エンジニアリング（ベクトル化）',
    description: 'レビューを数値ベクトル（TF-IDF）に変換',
    details: [
      'build_tfidf()でTF-IDF行列X作成（N-gram対応）',
      'ノイズ除去（min_df/max_df）と特徴数制御',
      '語彙の確認・調整'
    ],
    techniques: ['TF-IDF', 'Vectorization', 'N-grams']
  },
  {
    label: '3. K-meansクラスタリング',
    description: '類似レビューをグループ化し、パターンを発見',
    details: [
      'シルエット分析で適切なクラスタ数kを決定',
      'K-means実行しクラスタIDを付与',
      '各クラスタの特徴語・レビュー例を確認・可視化'
    ],
    techniques: ['K-means', 'Silhouette Analysis', 'Cluster Validation']
  },
  {
    label: '4. LDAトピックモデリング',
    description: '1レビューに複数話題が含まれる構造を抽出',
    details: [
      'LDA学習し、レビューを話題分布に変換',
      'トピック語彙の確認・ラベリング',
      '各レビューに主トピックを付与'
    ],
    techniques: ['LDA', 'Topic Modeling', 'Probabilistic Analysis']
  },
  {
    label: '5. 感情分析（ルールベース）',
    description: 'ネガティブ語句の有無でレビューの感情を自動判定',
    details: [
      '_NEG_KEYWORDS によるスコア付け',
      'トピックやクラスタごとの不満度を可視化・分析',
      '高評価なのに不満が多いレビューの検出'
    ],
    techniques: ['Rule-based Classification', 'Sentiment Scoring']
  },
  {
    label: '6. 可視化・分析',
    description: 'クラスタ／トピックの傾向を多角的に可視化',
    details: [
      'クラスタサイズ棒グラフ',
      'クラスタ別 N-gram 頻度グラフ',
      'トピック出現率の折れ線比較',
      'クラスタ×トピック ヒートマップ',
      '高評価 vs 最多コメントの偏り比較',
      'Streamlit でインタラクティブUI構築'
    ],
    techniques: ['Data Visualization', 'Interactive Charts', 'Statistical Analysis']
  }
];

export default function ResearchSteps() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        研究ステップ
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Stepper orientation="vertical">
                {steps.map((step) => (
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
              研究目的
            </Typography>
            <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
              <li>顧客フィードバックのパターンを特定</li>
              <li>高評価レビューと最多コメントレビューを比較</li>
              <li>レビューから有益なトピックを抽出</li>
              <li>感情分布を分析</li>
              <li>レストランに対する実践的な洞察を提供</li>
            </Box>
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3, mt: 2, bgcolor: '#f0f8ff' }}>
            <Typography variant="h6" gutterBottom color="primary">
              技術スタック
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