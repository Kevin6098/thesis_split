import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, TextField, Card, CardContent, Grid, 
  Chip, FormControl, InputLabel, Select, MenuItem, 
  Pagination, Paper, Divider 
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

export default function SearchEngine() {
  const [searchTerm, setSearchTerm] = useState('');
  const [dataset, setDataset] = useState('all');
  const [cluster, setCluster] = useState('all');
  const [sentiment, setSentiment] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // デモ用のモックデータ
  const mockResults = [
    {
      id: 1,
      comment: "美味しい料理と素晴らしいサービスでした。特に寿司が新鮮で、大将の技術も素晴らしかったです。",
      dataset: "high_rating",
      cluster: 5,
      topic: 1,
      sentiment: "positive",
      sentiment_score: 0.1
    },
    {
      id: 2,
      comment: "値段が高すぎると思います。料理の質は良いですが、コストパフォーマンスが悪いです。",
      dataset: "most_commented",
      cluster: 2,
      topic: 3,
      sentiment: "negative",
      sentiment_score: 0.8
    },
    // さらにモック結果を追加...
  ];

  useEffect(() => {
    if (searchTerm) {
      setLoading(true);
      // API 呼び出しをシミュレート
      setTimeout(() => {
        setResults(mockResults.filter(result => 
          result.comment.includes(searchTerm) &&
          (dataset === 'all' || result.dataset === dataset) &&
          (cluster === 'all' || result.cluster.toString() === cluster) &&
          (sentiment === 'all' || result.sentiment === sentiment)
        ));
        setLoading(false);
      }, 500);
    } else {
      setResults([]);
    }
  }, [searchTerm, dataset, cluster, sentiment]);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        検索エンジン
      </Typography>
      
      <Card elevation={3} sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom color="primary">
            レビュー検索
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="検索ワード"
                variant="outlined"
                value={searchTerm}
                onChange={handleSearch}
                placeholder="レビューを検索するキーワードを入力..."
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>データセット</InputLabel>
                <Select
                  value={dataset}
                  label="データセット"
                  onChange={(e) => setDataset(e.target.value)}
                >
                  <MenuItem value="all">すべて</MenuItem>
                  <MenuItem value="high_rating">高評価</MenuItem>
                  <MenuItem value="most_commented">最多コメント</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>クラスタ</InputLabel>
                <Select
                  value={cluster}
                  label="クラスタ"
                  onChange={(e) => setCluster(e.target.value)}
                >
                  <MenuItem value="all">すべて</MenuItem>
                  {[0,1,2,3,4,5,6,7,8].map(i => (
                    <MenuItem key={i} value={i.toString()}>クラスタ {i}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>感情</InputLabel>
                <Select
                  value={sentiment}
                  label="感情"
                  onChange={(e) => setSentiment(e.target.value)}
                >
                  <MenuItem value="all">すべて</MenuItem>
                  <MenuItem value="positive">ポジティブ</MenuItem>
                  <MenuItem value="negative">ネガティブ</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <Typography>検索中...</Typography>
        </Box>
      )}

      {results.length > 0 && (
        <>
          <Typography variant="h6" gutterBottom>
            {results.length} 件の結果が見つかりました
          </Typography>
          <Grid container spacing={2}>
            {results.slice((currentPage - 1) * 10, currentPage * 10).map((result) => (
              <Grid item xs={12} key={result.id}>
                <Paper elevation={1} sx={{ p: 3 }}>
                  <Typography variant="body1" paragraph>
                    {result.comment}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    <Chip 
                      label={result.dataset === 'high_rating' ? '高評価' : '最多コメント'} 
                      color="primary" 
                      size="small" 
                    />
                    <Chip 
                      label={`クラスタ ${result.cluster}`} 
                      color="secondary" 
                      size="small" 
                    />
                    <Chip 
                      label={`トピック ${result.topic}`} 
                      color="info" 
                      size="small" 
                    />
                    <Chip 
                      label={result.sentiment === 'positive' ? 'ポジティブ' : 'ネガティブ'} 
                      color={result.sentiment === 'positive' ? 'success' : 'error'} 
                      size="small" 
                    />
                    <Chip 
                      label={`スコア: ${result.sentiment_score}`} 
                      variant="outlined" 
                      size="small" 
                    />
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
          
          {results.length > 10 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination 
                count={Math.ceil(results.length / 10)} 
                page={currentPage} 
                onChange={(event, value) => setCurrentPage(value)} 
                color="primary" 
              />
            </Box>
          )}
        </>
      )}

      {searchTerm && !loading && results.length === 0 && (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography color="text.secondary">
            "{searchTerm}" に一致する結果はありません
          </Typography>
        </Box>
      )}
    </Box>
  );
}