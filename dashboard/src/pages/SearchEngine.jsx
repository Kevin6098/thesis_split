import React, { useState, useEffect } from "react";
import {
  Box, Typography, TextField, Card, CardContent, Grid,
  Pagination, Paper, Divider, Chip, FormControl, InputLabel, Select, MenuItem
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { createClient } from "@supabase/supabase-js";

// ─── Supabase client ────────────────────────────────────────
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error("Supabase credentials not found. Please check your .env file.");
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);



const PAGE_SIZE = 10;

export default function SearchEngine() {
  const [searchTerm, setSearchTerm] = useState("");
  const [dataset,   setDataset]   = useState("all");
  const [page,      setPage]      = useState(1);

  const [results, setResults] = useState([]);
  const [total,   setTotal]   = useState(0);
  const [loading, setLoading] = useState(false);

  const handleSearch = (e) => { setSearchTerm(e.target.value); setPage(1); };

  // fetch from Supabase whenever search term / dataset / page changes
  useEffect(() => {
    const fetchResults = async () => {
      if (!searchTerm.trim()) { setResults([]); setTotal(0); return; }

      setLoading(true);

      try {
        console.log(`Searching for: "${searchTerm}" in dataset: "${dataset}"`);
        
        let query = supabase.from("all_reviews")
                           .select("*", { count: "exact" })
                           .ilike("comment", `%${searchTerm}%`);

        if (dataset !== "all") {
          query = query.eq("dataset", dataset);
          console.log(`Filtering by dataset: ${dataset}`);
        }

        const from = (page - 1) * PAGE_SIZE;
        const to   = from + PAGE_SIZE - 1;
        console.log(`Pagination: from ${from} to ${to}`);
        
        const { data, count, error } = await query.range(from, to);

        if (error) {
          console.error("Supabase error:", error); 
          setResults([]); 
          setTotal(0);
        } else {
          console.log(`✅ Search successful! Found ${count} total results, showing ${data?.length || 0} on this page`);
          if (data && data.length > 0) {
            console.log("Sample result:", data[0]);
          }
          setResults(data ?? []); 
          setTotal(count ?? 0);
        }
      } catch (err) {
        console.error("Search error:", err);
        setResults([]);
        setTotal(0);
      }
      
      setLoading(false);
    };

    fetchResults();
  }, [searchTerm, dataset, page]);

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto" }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: "bold" }}>
        検索エンジン
      </Typography>



      {/* ─────────────── Filters ─────────────── */}
      <Card elevation={3} sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom color="primary">
            レビュー検索
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <TextField
                fullWidth
                label="検索ワード"
                variant="outlined"
                value={searchTerm}
                onChange={handleSearch}
                placeholder="レビューを検索するキーワードを入力..."
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: "action.active" }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>データセット</InputLabel>
                <Select
                  value={dataset}
                  label="データセット"
                  onChange={(e) => { setDataset(e.target.value); setPage(1); }}
                >
                  <MenuItem value="all">すべて</MenuItem>
                  <MenuItem value="high_rating">高評価</MenuItem>
                  <MenuItem value="most_commented">最多コメント</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* ─────────────── Results ─────────────── */}
      {loading && (
        <Box sx={{ textAlign: "center", my: 4 }}><Typography>検索中…</Typography></Box>
      )}

      {!loading && searchTerm && total === 0 && (
        <Box sx={{ textAlign: "center", my: 4 }}>
          <Typography color="text.secondary">"{searchTerm}" に一致する結果はありません</Typography>
        </Box>
      )}

      {!loading && results.length > 0 && (
        <>
          <Typography variant="h6" gutterBottom>{total} 件の結果が見つかりました</Typography>
          <Grid container spacing={2}>
            {results.map((r, index) => (
              <Grid item xs={12} key={`${r.dataset}-${index}`}>
                <Paper elevation={1} sx={{ p: 3 }}>
                  <Typography variant="body1" paragraph>{r.comment}</Typography>
                  <Divider sx={{ my: 2 }} />
                  <Chip
                    label={r.dataset === "high_rating" ? "高評価" : "最多コメント"}
                    color="primary" size="small"
                  />
                </Paper>
              </Grid>
            ))}
          </Grid>

          {total > PAGE_SIZE && (
            <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
              <Pagination
                count={Math.ceil(total / PAGE_SIZE)}
                page={page}
                onChange={(_, p) => setPage(p)}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
}