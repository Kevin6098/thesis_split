import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import HomeIcon from '@mui/icons-material/Home';
import TimelineIcon from '@mui/icons-material/Timeline';
import StarIcon from '@mui/icons-material/Star';
import CommentIcon from '@mui/icons-material/Comment';
import SearchIcon from '@mui/icons-material/Search';
import MergeTypeIcon from '@mui/icons-material/MergeType';
import SummarizeIcon from '@mui/icons-material/Summarize';

const drawerWidth = 280;

const items = [
  { text: 'Introduction',           path: '/', icon: <HomeIcon /> },
  { text: 'Research Steps',         path: '/research-steps', icon: <TimelineIcon /> },
  { text: 'High-Rating Results',    path: '/high-rating', icon: <StarIcon /> },
  { text: 'Most-Commented Results', path: '/most-commented', icon: <CommentIcon /> },
  { text: 'Search Engine',          path: '/search', icon: <SearchIcon /> },
  { text: 'Mixed Topics',           path: '/mixed-topics', icon: <MergeTypeIcon /> },
  { text: 'Conclusion',             path: '/conclusion', icon: <SummarizeIcon /> },
];

export default function NavigationDrawer() {
  const { pathname } = useLocation();
  
  return (
    <Drawer
      variant="permanent"
      anchor="left"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': { 
          width: drawerWidth, 
          boxSizing: 'border-box',
          backgroundColor: '#f5f5f5'
        },
      }}
    >
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            Thesis Analysis
          </Typography>
        </Box>
      </Toolbar>
      <Divider />
      <List>
        {items.map(({ text, path, icon }) => (
          <ListItemButton
            key={text}
            component={Link}
            to={path}
            selected={pathname === path}
            sx={{
              '&.Mui-selected': {
                backgroundColor: 'primary.main',
                color: 'white',
                '&:hover': {
                  backgroundColor: 'primary.dark',
                },
                '& .MuiListItemIcon-root': {
                  color: 'white',
                },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>
              {icon}
            </ListItemIcon>
            <ListItemText 
              primary={text} 
              primaryTypographyProps={{ fontSize: '0.9rem' }}
            />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}