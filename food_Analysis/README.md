# Indian Cuisine Analysis 🥘

An interactive dashboard built with [Streamlit](https://streamlit.io/) to explore the rich diversity, flavors, and nutritional characteristics of Indian dishes.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## Features

- **Overall Overview:** A quick glance at the rich Indian cuisine.
- **Map Distribution:** A choreopleth map showcasing the state-by-state dominance of Vegetarian vs Non-Vegetarian diets.
- **Individual Analysis:** Extensively filter dishes by Region, State, Diet, Prep Time, Flavor Profiles, and Health Status. Includes interactive summaries and plots.
- **Comparison Tool:** Compare two dishes head-to-head based on Preparation Time or Health Score. Case-insensitive search supported!

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd food_Analysis
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Data
The dataset used in this application includes comprehensive details about hundreds of Indian dishes. Various CSV files inside the `Data/` folder power the analysis, alongside spatial GeoJSON boundaries for rendering maps.

## Author

This project is part of a broader data analytics portfolio showcasing exploratory data analysis (EDA) techniques and interactive frontend development.
