# Japanese Restaurant Reviews Analysis Dashboard

An interactive React + D3.js dashboard for exploring the results of Japanese restaurant reviews analysis using clustering, topic modeling, and sentiment analysis.

## Features

- **Interactive Navigation**: Left sidebar navigation with 7 main sections
- **Multiple Analysis Views**: Silhouette analysis, clustering results, LDA topics, sentiment analysis
- **Comparative Analysis**: Side-by-side comparison of high-rating vs most-commented reviews
- **Search Engine**: Filter and search through reviews by cluster, topic, and sentiment
- **Representative Quotes**: Browse sample reviews from each cluster
- **Cross-dataset Analysis**: Integrated insights from both datasets

## Navigation Structure

1. **Introduction**: Overview of the research and dashboard features
2. **Research Steps**: Detailed methodology and technical approach
3. **High-Rating Results**: Complete analysis of high-rating reviews with tabs for:
   - Silhouette Analysis
   - Clustering Results
   - LDA Topics
   - Topic-Cluster Heatmap
   - Sentiment Analysis
   - Representative Quotes
4. **Most-Commented Results**: Same analysis structure for most-commented reviews
5. **Search Engine**: Interactive search and filtering capabilities
6. **Mixed Topics**: Cross-dataset comparative analysis
7. **Conclusion**: Key findings and business implications

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Python 3.8+ (for data export scripts)

### Installation

1. **Install dependencies**:
   ```bash
   cd dashboard
   npm install
   ```

2. **Export data from your analysis** (optional - mock data is included):
   ```bash
   # From the project root directory
   python dashboard/export_scripts/export_dashboard_data.py
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser** and navigate to `http://localhost:5173`

### Building for Production

```bash
npm run build
npm run preview
```

## Technical Stack

- **Frontend**: React 18 with React Router for navigation
- **UI Components**: Material-UI (MUI) for professional design
- **Visualizations**: D3.js for interactive charts and graphs
- **Build Tool**: Vite for fast development and building
- **Styling**: Emotion (CSS-in-JS) with MUI theme system

## Data Format

The dashboard expects JSON files in the `public/data/` directory:

- `high_rating_silhouette.json`: Silhouette scores for different k values
- `high_rating_cluster_distribution.json`: Cluster size distribution
- `high_rating_lda_topics.json`: LDA topic analysis results
- `high_rating_sentiment.json`: Sentiment analysis results
- `high_rating_quotes.json`: Representative quotes by cluster
- Similar files for `most_commented` dataset

## Chart Types

### Silhouette Analysis
- Line chart showing silhouette scores vs number of clusters
- Optimal k value highlighted

### Cluster Distribution
- Bar chart showing review count per cluster
- Interactive tooltips with percentages

### LDA Topics
- Horizontal bar chart of topic prevalence
- Topic cards with top words and descriptions

### Topic Heatmap
- Cluster × Topic heatmap showing relationships
- Color-coded proportions with legend

### Sentiment Analysis
- Pie chart for overall sentiment distribution
- Bar chart for sentiment by cluster

### Search Results
- Paginated table with filtering capabilities
- Chip-based metadata display

### Cross-dataset Comparison
- Scatter plot comparing topic prevalence
- Side-by-side bar charts for sentiment

## Customization

### Adding New Visualizations

1. Create a new component in `src/viz/`
2. Import and use D3.js for data visualization
3. Add Material-UI components for layout
4. Include in the appropriate page component

### Modifying the Navigation

Edit `src/components/NavigationDrawer.jsx` to add or modify navigation items.

### Updating Data

Replace JSON files in `public/data/` or modify the export script to match your data structure.

## Development

### Project Structure

```
dashboard/
├── public/
│   └── data/           # JSON data files
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Main page components
│   ├── viz/            # D3.js visualization components
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── package.json
└── vite.config.js
```

### Running Tests

```bash
npm test
```

### Linting

```bash
npm run lint
```

## Deployment

The dashboard can be deployed to any static hosting service:

- **Vercel**: Connect your GitHub repository
- **Netlify**: Drag and drop the `dist` folder
- **GitHub Pages**: Use GitHub Actions for automated deployment

Build command: `npm run build`
Publish directory: `dist`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of a thesis research and is intended for academic purposes.