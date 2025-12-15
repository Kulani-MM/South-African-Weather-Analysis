# South African Weather Analysis 🌦️

Analyze and visualize weather trends across South African cities using Python, Pandas, Matplotlib, Plotly, and Dash.

---

## Features

- Clean and analyze historical weather data
- Calculate average temperatures by city, date, and month
- Identify top 5 hottest and coldest cities
- Generate static visualizations using Matplotlib
- Create interactive plots with Plotly
- Explore city-specific temperature trends using a Dash web app

---

---
## Check it out
[Weather Dashbard](https://sa-weather-dashboard.onrender.com)

## Getting Started

### Quick Start (Demo Mode)

Want to try it out immediately? Just clone and run - no API key needed!

```bash
git clone https://github.com/Kulani-MM/South-African-Weather-Analysis.git
cd South-African-Weather-Analysis
python -m venv .venv
source .venv/bin/activate   # On Mac/Linux
# .venv\Scripts\activate    # On Windows
pip install -r requirements.txt
python weather_analysis.py
```

The app will automatically run in **demo mode** with sample data.

### Live Mode (Real-time Weather Data)

To use live weather data from OpenWeatherMap:

1. **Get a FREE API key:**
   - Visit [https://openweathermap.org/api](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key

2. **Create a `.env` file** in the project root:
   ```bash
   OPENWEATHER_API_KEY=your_api_key_here
   ```

3. **Run the app:**
   ```bash
   python weather_analysis.py
   ```

The app will automatically detect your API key and use live data!

### Prerequisites

Make sure you have Python 3 installed. Recommended to use a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate   # On Mac/Linux
.venv\Scripts\activate      # On Windows

