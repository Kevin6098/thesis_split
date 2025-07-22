import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import NavigationDrawer from './components/NavigationDrawer.jsx';
import Introduction      from './pages/Introduction.jsx';
import ResearchSteps     from './pages/ResearchSteps.jsx';
import HighRating        from './pages/HighRating.jsx';
import MostCommented     from './pages/MostCommented.jsx';
import SearchEngine      from './pages/SearchEngine.jsx';
import MixedTopics       from './pages/MixedTopics.jsx';
import Conclusion        from './pages/Conclusion.jsx';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const drawerWidth = 280;

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: 'flex' }}>
          <CssBaseline />
          <AppBar 
            position="fixed" 
            sx={{ 
              width: `calc(100% - ${drawerWidth}px)`, 
              ml: `${drawerWidth}px` 
            }}
          >
            <Toolbar>
              <Typography variant="h6" noWrap component="div">
                飲食店における口コミ数と評価の関係性の分析
              </Typography>
            </Toolbar>
          </AppBar>
          <NavigationDrawer />
          <Box 
            component="main" 
            sx={{ 
              flexGrow: 1, 
              bgcolor: 'background.default', 
              p: 3,
              width: { sm: `calc(100% - ${drawerWidth}px)` }
            }}
          >
            <Toolbar />
            <Routes>
              <Route path="/"                 element={<Introduction />} />
              <Route path="/research-steps"   element={<ResearchSteps />} />
              <Route path="/high-rating"      element={<HighRating />} />
              <Route path="/most-commented"   element={<MostCommented />} />
              <Route path="/search"           element={<SearchEngine />} />
              <Route path="/mixed-topics"     element={<MixedTopics />} />
              <Route path="/conclusion"       element={<Conclusion />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}