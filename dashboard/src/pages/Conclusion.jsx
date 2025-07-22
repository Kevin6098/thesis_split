import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Paper, Divider } from '@mui/material';

export default function Conclusion() {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        結論
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom color="primary">
                研究概要
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                本研究では、日本のレストランレビューを包括的に分析し、顧客のフィードバックパターン、
                感情の分布、トピックの嗜好をエンゲージメントの異なるカテゴリ間で明らかにしました。
                K-means クラスタリング、LDA トピックモデリング、感情分析などの高度な NLP 技術を適用することで、
                異なる顧客セグメントとその特徴的な関心事を特定することに成功しました。
              </Typography>
              <Typography variant="body1" paragraph sx={{ lineHeight: 1.8 }}>
                高評価レビューと最多コメントレビューを比較分析した結果、顧客の関心領域に明確な違いが見られました。
                高評価レビューは料理の質とサービスの卓越性を強調する一方で、
                最多コメントレビューは価値提案や価格に関する懸念に焦点を当てる傾向がありました。
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                主要な貢献
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1.5 } }}>
                <li>
                  <strong>方法論的枠組み：</strong> クラスター分析とトピックモデリングを用いて
                  日本のレストランレビューを分析する包括的アプローチを構築
                </li>
                <li>
                  <strong>比較的洞察：</strong> 高評価レビューと最多コメントレビューのカテゴリー間で
                  明確なパターンを特定
                </li>
                <li>
                  <strong>インタラクティブダッシュボード：</strong> 複雑な分析結果を探索できる
                  ユーザーフレンドリーな可視化プラットフォームを作成
                </li>
                <li>
                  <strong>実践的応用：</strong> レストラン経営と顧客体験向上のための
                  実用的な洞察を提供
                </li>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                技術的成果
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1.5 } }}>
                <li>
                  <strong>クラスタ最適化：</strong> シルエット分析により最適なクラスタ数を決定
                </li>
                <li>
                  <strong>トピック発見：</strong> LDA モデリングを用いて日本語テキストから
                  有用なトピックを抽出
                </li>
                <li>
                  <strong>感情分類：</strong> 日本のレストランレビューに特化した
                  ルールベースの感情分析を実装
                </li>
                <li>
                  <strong>可視化の革新：</strong> 複雑なデータ探索のための
                  インタラクティブな D3.js 可視化を開発
                </li>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 3, bgcolor: '#f8f9fa' }}>
            <Typography variant="h6" gutterBottom color="primary">
              ビジネスへの影響と提言
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  レストラン経営者向け
                </Typography>
                <Box component="ul" sx={{ pl: 2, fontSize: '0.9rem' }}>
                  <li>クラスタパターンを監視して顧客セグメントを把握</li>
                  <li>高評価を獲得するために料理の質とサービスに注力</li>
                  <li>最多コメントレビューで指摘された価格に関する懸念に対応</li>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  プラットフォーム開発者向け
                </Typography>
                <Box component="ul" sx={{ pl: 2, fontSize: '0.9rem' }}>
                  <li>トピックベースのレビュー分類を実装</li>
                  <li>感情を考慮した推薦システムを提供</li>
                  <li>クラスタベースのユーザーセグメンテーションを可能にする</li>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  研究者向け
                </Typography>
                <Box component="ul" sx={{ pl: 2, fontSize: '0.9rem' }}>
                  <li>他言語および他ドメインへの分析を拡張</li>
                  <li>レビューデータの時間的パターンを調査</li>
                  <li>より高度な感情分析手法を探究</li>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Card elevation={2} sx={{ bgcolor: '#e3f2fd' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="primary">
                将来の研究課題
              </Typography>
              <Typography variant="body1" paragraph>
                本研究は今後の研究に向け、多くの可能性を開きました。
                たとえばレビューの時間的パターンの分析、レストランのメタデータや
                顧客属性など追加データソースの統合、より精緻な感情・トピック分析を
                実現するための高度なディープラーニング手法の適用などが挙げられます。
              </Typography>
              <Typography variant="body1">
                本研究で開発したインタラクティブ・ダッシュボードの枠組みは、
                リアルタイムのレビュー監視システムの基盤として機能し、
                レストランの業績を予測するための予測分析をサポートするよう
                拡張することも可能です。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}