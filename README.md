# Healthcare Data Analysis

A simple, beginner-friendly tool for analyzing healthcare CSV files. Upload any CSV and get instant summaries, statistics, group-by analysis, and medium-sized charts.

## Features

- **Auto-detect columns** — Automatically finds common healthcare columns (age, BMI, glucose, gender, disease, outcome)
- **Data quality metrics** — Shows rows, missing values, duplicates
- **Basic analysis** — Mean, max, min for numeric columns
- **Group-by stats** — Average values grouped by category
- **Correlation analysis** — See relationships between numeric columns
- **Charts** — Bar, pie, histogram, and correlation heatmap
- **Works with any CSV** — Flexible column name matching

## Project Files

- `streamlit_app.py` — Main Streamlit web app
- `healthcare_analysis_notebook.ipynb` — Jupyter Notebook version (same analysis)
- `requirements.txt` — Python package dependencies

## Requirements

- Python 3.7 or higher
- Virtual environment (recommended)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501` in your browser. Upload a CSV file to start analyzing.

### 3. Run the Notebook (Optional)

```bash
jupyter notebook healthcare_analysis_notebook.ipynb
```

## Example CSV Columns

The app auto-detects these columns (or similar names):

- **age** — Patient age
- **bmi** — Body Mass Index
- **glucose** — Blood glucose level
- **gender** / **sex** — Patient gender
- **disease** / **diagnosis** / **condition** — Health condition
- **outcome** / **target** / **result** — Analysis outcome

If your CSV has different column names, the app will still work—it uses smart name matching.

## How It Works

1. Upload a CSV file
2. App cleans data (removes missing values, standardizes text)
3. Auto-detects meaningful columns
4. Displays data quality, statistics, and charts
5. Shows group-by analysis and correlations

## Tips

- CSV files should have headers (column names in the first row)
- Data rows with missing values are removed during cleaning
- Charts are medium-sized for easy viewing
- Use the app with any healthcare or medical dataset

## Author

Created as a beginner-friendly mini project for learning data analysis with Python, Streamlit, and Jupyter.
