import React from 'react';
import { 
  Card, CardContent, Typography, Grid, Box, Stepper, Step, 
  StepLabel, StepContent, Paper, Chip 
} from '@mui/material';

const steps = [
  {
    label: 'データ収集と前処理',
    description: '高評価および最多コメントカテゴリから日本のレストランレビューを収集',
    details: [
      'レビュー プラットフォームからの生データ抽出',
      'テキストのクレンジングと正規化',
      '日本語テキストの前処理',
      'ストップワード除去とトークン化'
    ],
    techniques: ['Text Cleaning', 'Tokenization', 'Normalization']
  },
  {
    label: '特徴量エンジニアリング',
    description: '機械学習用にテキストデータを数値表現に変換',
    details: [
      'TF-IDF ベクトル化',
      'N-gram 特徴抽出',
      '次元数の検討',
      '特徴量選択の最適化'
    ],
    techniques: ['TF-IDF', 'Vectorization', 'N-grams']
  },
  {
    label: 'K-means クラスタリング',
    description: '教師なしクラスタリングを適用して類似レビューをグループ化',
    details: [
      'シルエット分析による最適クラスタ数の決定',
      'K-means アルゴリズムの実装',
      'クラスタの検証と解釈',
      '代表サンプルの抽出'
    ],
    techniques: ['K-means', 'Silhouette Analysis', 'Cluster Validation']
  },
  {
    label: 'トピックモデリング（LDA）',
    description: 'Latent Dirichlet Allocation を用いて潜在トピックを抽出',
    details: [
      'LDA モデルの学習と最適化',
      'トピック一貫性の評価',
      'トピック–ドキュメント確率分布',
      'トピックのラベリングと解釈'
    ],
    techniques: ['LDA', 'Topic Modeling', 'Probabilistic Analysis']
  },
  {
    label: '感情分析',
    description: 'ルールベース手法で感情パターンを分析',
    details: [
      '日本語ネガティブキーワードの識別',
      'ルールベースの感情分類',
      '感情スコアの算出',
      '感情分布の分析'
    ],
    techniques: ['Rule-based Classification', 'Sentiment Scoring']
  },
  {
    label: '可視化と分析',
    description: 'インタラクティブな可視化と包括的解析を作成',
    details: [
      'クラスタ分布の可視化',
      'トピック出現頻度の分析',
      'クラスタ・トピック関係のヒートマップ生成',
      'インタラクティブダッシュボードの開発'
    ],
    techniques: ['Data Visualization', 'Interactive Charts', 'Statistical Analysis']
  }
];

export default function ResearchSteps() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        研究手法
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