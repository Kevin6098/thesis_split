import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Card, CardContent, Grid, Chip, 
  FormControl, InputLabel, Select, MenuItem, Alert 
} from '@mui/material';

export default function RepresentativeQuotes({ dataset }) {
  const [selectedCluster, setSelectedCluster] = useState('all');
  const [quotes, setQuotes] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadQuotes = () => {
      try {
        // Mock representative quotes data
        const mockQuotes = dataset === 'high_rating' ? {
          0: [
            {
              comment: "本庄の住宅街にひっそりと佇む、日本料理のお店。店名は金沢の美しい「ひがし茶屋街」に因んでおられます。明石の蛸と蓴菜。海胆と鱒、上品な取り合わせ。",
              sentiment: "positive",
              sentiment_score: 0.1,
              topic: 0
            },
            {
              comment: "以前から行きたかったのですが、他にも色々行かねばならない店が多く後回しになり、ようやく行くことができました。",
              sentiment: "positive", 
              sentiment_score: 0.05,
              topic: 3
            }
          ],
          1: [
            {
              comment: "坂出駅から徒歩5.6分くらい？のところにある有名なうどん屋さん。うどん屋さんといっても製麺所で、1時間だけうどんを提供しています。",
              sentiment: "positive",
              sentiment_score: 0.02,
              topic: 7
            },
            {
              comment: "利用状況と注意点・平日15:30ごろ・2人平日だったため並ばずに入ることができたが、整理券用の機械が置いてあった。",
              sentiment: "positive",
              sentiment_score: 0.0,
              topic: 3
            }
          ],
          2: [
            {
              comment: "2020年から予約制になったようですね。伺ったのは2019年、写真フォルダから出てきました。あの日は確か１日中雨、湯河原に友人と旅行に行った際に湯河原といえば飯田商店ということで、覚悟して行きました。",
              sentiment: "positive",
              sentiment_score: 0.0,
              topic: 3
            }
          ],
          // Add more clusters...
        } : {
          0: [
            {
              comment: "値段が高すぎると思います。料理の質は良いですが、コストパフォーマンスが悪いです。残念でした。",
              sentiment: "negative",
              sentiment_score: 0.6,
              topic: 2
            }
          ],
          1: [
            {
              comment: "開店時間に遅れて到着したため、かなり待つことになりました。時間管理がもう少し良ければと思います。",
              sentiment: "negative",
              sentiment_score: 0.4,
              topic: 1
            }
          ]
          // Add more clusters...
        };

        if (selectedCluster === 'all') {
          const allQuotes = Object.values(mockQuotes).flat();
          setQuotes(allQuotes);
        } else {
          setQuotes(mockQuotes[selectedCluster] || []);
        }
        setError(null);
      } catch (err) {
        setError('Failed to load representative quotes');
        console.error('Representative quotes error:', err);
      }
    };

    loadQuotes();
  }, [dataset, selectedCluster]);

  const clusters = dataset === 'high_rating' ? 
    [0, 1, 2, 3, 4, 5, 6, 7] : 
    [0, 1, 2, 3, 4, 5, 6, 7, 8];

  if (error) {
    return (
      <Alert severity="info">
        {error}. Using simulated data for demonstration.
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Select Cluster</InputLabel>
          <Select
            value={selectedCluster}
            label="Select Cluster"
            onChange={(e) => setSelectedCluster(e.target.value)}
          >
            <MenuItem value="all">All Clusters</MenuItem>
            {clusters.map(cluster => (
              <MenuItem key={cluster} value={cluster}>
                Cluster {cluster}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {quotes.length === 0 ? (
        <Typography color="text.secondary">
          No quotes available for the selected cluster.
        </Typography>
      ) : (
        <Grid container spacing={2}>
          {quotes.map((quote, index) => (
            <Grid item xs={12} key={index}>
              <Card elevation={1} sx={{ borderLeft: `4px solid ${quote.sentiment === 'positive' ? '#4caf50' : '#f44336'}` }}>
                <CardContent>
                  <Typography variant="body1" paragraph sx={{ lineHeight: 1.6 }}>
                    "{quote.comment}"
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
                    <Chip 
                      label={quote.sentiment} 
                      color={quote.sentiment === 'positive' ? 'success' : 'error'} 
                      size="small" 
                    />
                    <Chip 
                      label={`Score: ${quote.sentiment_score.toFixed(2)}`} 
                      variant="outlined" 
                      size="small" 
                    />
                    <Chip 
                      label={`Topic ${quote.topic}`} 
                      color="info" 
                      size="small" 
                    />
                    <Chip 
                      label={dataset === 'high_rating' ? 'High Rating' : 'Most Commented'} 
                      color="primary" 
                      size="small" 
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      
      <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
        Representative quotes are selected based on their cluster membership and sentiment characteristics. 
        The colored border indicates sentiment polarity.
      </Typography>
    </Box>
  );
}